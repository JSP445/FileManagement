<template>
  <!-- This page displays all assets, which can be sorted and filtered -->
  <div class="mb-3">
    <transition name="fade">
      <div>
        <div v-if="modalVisible" :class="{ 'modal-mask': modalVisible }">
          <div
            class="d-flex w-100 h-100 align-items-center justify-content-center position-absolute gap-3"
          >
            <AssociatedAssets
              v-if="associatedAssets.length !== 0 && associatedVisible && !commentsOpen"
              v-bind:associatedAssets="associatedAssets"
              @openModal="openModal"
              @associated="associatedVisible = !associatedVisible"
              class="w-25"
            />

            <AssetInfo
              v-if="!commentsOpen"
              v-bind:asset="selectedAsset"
              v-bind:assetTypeName="assetTypeName"
              :associatedVisible="associatedVisible"
              :assetTypeAttributes="assetTypeAttributes"
              :hasAssociated="associatedAssets.length !== 0"
              @comments="commentsOpen = true"
              @close="closeModal"
              @associated="associatedVisible = !associatedVisible"
              class="w-50"
            />

            <Comments
              v-if="commentsOpen"
              v-bind:asset="selectedAsset"
              @replyTo="
                (id) => {
                  replyingTo = id;
                  isCommenting = true;
                }
              "
              @close="closeModal"
              @asset="commentsOpen = false"
              ref="comments"
              class="w-50"
            />

            <AddComment
              v-if="isCommenting && commentsOpen"
              :asset="selectedAsset"
              :replyTo="replyingTo"
              @close="closeAddComment"
              class="w-25"
            />
          </div>
        </div>
      </div>
    </transition>

    <div class="viewAssets">
      <div v-show="!createState" class="w-100 bg-white border-top border-bottom p-4 mb-5">
        <!-- Contains all the filtes that can be used -->
        <div
          class="filterContainer | d-flex w-100 gap-3 align-items-end justify-content-center m-auto"
        >
          <div class="w-50">
            <label>Filter:</label>
            <select class="form-select" v-model="filter.selected">
              <option selected value="name">Name</option>
              <option value="created_by">Creator</option>
              <option value="asset_type">Asset Type</option>
              <option value="created_date">Created Date</option>
              <option value="last_updated">Last Updated</option>
              <option value="tag">Tag</option>
              <option value="project">Project</option>
            </select>
          </div>

          <div class="w-100">
            <div class="filter" v-if="filter.selected == 'name'">
              <label>By name:</label>
              <input v-model="filter.name" class="form-control" type="text" />
            </div>
            <div class="filter" v-else-if="filter.selected == 'created_by'">
              <label>By Creator:</label>
              <input v-model="filter.created_by" class="form-control" type="text" />
            </div>
            <div class="filter" v-else-if="filter.selected == 'asset_type'">
              <label>By Type:</label>
              <input v-model="filter.asset_type" class="form-control w-100" type="text" />
            </div>

            <div class="filter" v-else-if="filter.selected == 'created_date'">
              <label>By created date:</label>
              <Datepicker
                class="w-100"
                v-model="filter.created_on"
                :enable-time-picker="false"
                range
              />
            </div>

            <div class="filter" v-else-if="filter.selected == 'last_updated'">
              <label>By last updated:</label>
              <Datepicker
                class="w-100"
                v-model="filter.last_updated"
                :enable-time-picker="false"
                range
              />
            </div>

            <div class="filter" v-show="filter.selected == 'tag'">
              <label>By tag:</label>
              <vue-tags-input
                class="w-100"
                style="max-width: 100%"
                v-model="filter.tag"
                :tags="filter.tags"
                :autocomplete-items="filteredTags"
                :add-only-from-autocomplete="true"
                @tags-changed="(newTags) => (filter.tags = newTags)"
              />
            </div>

            <div class="filter" v-show="filter.selected == 'project'">
              <label>By project:</label>
              <vue-tags-input
                class="w-100"
                style="max-width: 100%"
                placeholder="Add Project"
                v-model="filter.project"
                :tags="filter.projects"
                :autocomplete-items="filteredProjects"
                :add-only-from-autocomplete="true"
                @tags-changed="(newTags) => (filter.projects = newTags)"
              />
            </div>
          </div>
        </div>

        <!-- Displays all active filters -->
        <div class="mt-4 d-flex flex-wrap justify-content-center align-items-center gap-3">
          <p
            v-if="
              filter.name ||
              filter.created_by ||
              filter.created_on ||
              filter.last_updated ||
              filter.asset_type ||
              filter.tags.length ||
              filter.projects.length
            "
            class="fw-bold"
            style="margin-bottom: 0"
          >
            Current active filters:
          </p>

          <div class="d-flex gap-2 align-items-center" v-if="filter.name">
            <p class="" style="margin-bottom: 0">Name: {{ filter.name }}</p>
            <input
              type="button"
              class="closeBtn | btn btn-danger"
              value="&#10006;"
              @click="filter.name = ''"
            />
          </div>

          <div class="d-flex gap-2 align-items-center" v-if="filter.created_by">
            <p class="" style="margin-bottom: 0">Creator: {{ filter.created_by }}</p>
            <input
              type="button"
              class="closeBtn | btn btn-danger"
              value="&#10006;"
              @click="filter.created_by = ''"
            />
          </div>

          <div class="d-flex gap-2 align-items-center" v-if="filter.created_on">
            <p class="" style="margin-bottom: 0">
              Created on: {{ displayDate(filter.created_on) }}
            </p>
            <input
              type="button"
              class="closeBtn | btn btn-danger"
              value="&#10006;"
              @click="filter.created_on = null"
            />
          </div>

          <div class="d-flex gap-2 align-items-center" v-if="filter.last_updated">
            <p class="" style="margin-bottom: 0">
              Last updated: {{ displayDate(filter.last_updated) }}
            </p>
            <input
              type="button"
              class="closeBtn | btn btn-danger"
              value="&#10006;"
              @click="filter.last_updated = null"
            />
          </div>

          <div class="d-flex gap-2 align-items-center" v-if="filter.asset_type">
            <p class="" style="margin-bottom: 0">Type: {{ filter.asset_type }}</p>
            <input
              type="button"
              class="closeBtn | btn btn-danger"
              value="&#10006;"
              @click="filter.asset_type = ''"
            />
          </div>

          <div class="d-flex gap-2 align-items-center" v-if="filter.tags.length">
            <p class="" style="margin-bottom: 0" v-bind="onlyTagsText">
              Tags: {{ filter.tagsText }}
            </p>
            <input
              type="button"
              class="closeBtn | btn btn-danger"
              value="&#10006;"
              @click="
                filter.tags = [];
                filter.tag = '';
              "
            />
          </div>

          <div class="d-flex gap-2 align-items-center" v-if="filter.projects.length">
            <p class="" style="margin-bottom: 0" v-bind="onlyProjectsText">
              Projects: {{ filter.projectsText }}
            </p>
            <input
              type="button"
              class="closeBtn | btn btn-danger"
              value="&#10006;"
              @click="
                filter.projects = [];
                filter.project = '';
              "
            />
          </div>
        </div>
      </div>

      <!-- Displays component for adding assets -->
      <div v-if="createState">
        <AddAsset
          @close="
            createState = false;
            loadAssets();
          "
        />
      </div>

      <div v-else>
        <div class="m-auto d-flex flex-column align-items-center justify-content-center pb-5 gap-4">
          <!-- Displays all sorting options -->
          <div
            class="assetSortContainer | d-flex align-items-center gap-4 flex-wrap justify-content-center"
          >
            <label class="h5 fw-bold mb-0" style="white-space: nowrap">Sort by</label>
            <select
              v-model="sort.sortBy"
              class="form-select"
              style="width: 35ch"
              @change="sortAssets"
            >
              <option value="asset_name">Name</option>
              <option value="created_by">Created By</option>
              <option value="created_on">Created On</option>
              <option value="last_updated">Last Updated</option>
            </select>

            <div>
              <input
                type="button"
                class="btn btn-primary w-100"
                value="Ascending"
                @click="
                  ({ target }) => {
                    if (sort.sortRadio == 'desc') {
                      target.value = 'Ascending';
                      sort.sortRadio = 'asc';
                    } else {
                      target.value = 'Descending';
                      sort.sortRadio = 'desc';
                    }
                    sortAssets();
                  }
                "
              />
            </div>
          </div>
          <input
            type="button"
            class="btn btn-success py-2 px-5"
            value="Add new Asset"
            @click="createState = !createState"
            style="width: clamp(3rem, 70%, 33rem)"
          />
          <h3 class="mt-5" v-if="!filteredAssets.length">No Assets</h3>
        </div>

        <!-- Displays all assets -->
        <div class="assetCardContainer | d-grid gap-3 px-4" style="max-width: 120rem; margin: auto">
          <div
            v-for="asset in filteredAssets"
            :key="asset.asset_id"
            class="gridItem | d-flex justify-content-center flex-grow-1"
          >
            <div class="assetCard | bg-white border" style="border-radius: 15px; width: 30rem">
              <h5 class="fw-bold border-bottom p-4 text-center">{{ asset.asset_name }}</h5>
              <div class="p-4">
                <p>
                  Created by:
                  {{ asset.created_by.user_name.first_name }}
                  {{ asset.created_by.user_name.last_name }} ({{ asset.created_by.email }})
                </p>
                <p>Created on: {{ formatDate(asset.created_on) }}</p>
                <p>Last Updated: {{ formatDate(asset.last_updated) }}</p>
              </div>

              <div class="d-flex justify-content-between gap-3 px-4 pb-4">
                <button
                  type="button"
                  class="btn btn-primary w-100"
                  @click="openModal(asset.asset_id)"
                >
                  Details
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AssociatedAssets from "@/components/AssociatedAssets.vue";
import AddAsset from "@/components/AddAsset.vue";
import Comments from "@/components/Comments.vue";
import AddComment from "@/components/AddComment.vue";
import { associateAsset, fetchAssetType, getAssets, getProjects, tagNames } from "@/api";
import AssetInfo from "@/components/AssetInfo.vue";
import VueTagsInput from "@sipec/vue3-tags-input";
import Datepicker from "vue3-date-time-picker";
import "vue3-date-time-picker/dist/main.css";
import { formatDate } from "@/utils";

export default {
  data() {
    return {
      // A list of all assets
      assets: [],
      // Determines if the asset info modal is displayed
      modalVisible: false,
      // Determines if associated assets are displayed in it's modals
      associatedVisible: false,
      // The asset for which asset info is displayed
      selectedAsset: {},
      // The name of the asset type of the selected asset
      assetTypeName: "",
      // The attributes of the selected asset
      assetTypeAttributes: [],
      // All assets associated with the selected asset
      associatedAssets: [],

      // The sorting method applied to the view
      sort: {
        sortBy: "asset_name",
        sortRadio: "asc",
      },

      // All filters applied to the view
      filter: {
        name: "",
        created_by: "",
        created_on: null,
        last_updated: null,
        asset_type: "",
        tag: "",
        tags: [],
        project: "",
        projects: [],
        selected: "name",
        projectsText: [],
        tagsText: [],
      },

      // The parent comment replied to in the comment modal
      replyingTo: null,
      // Determines if user is adding a comment
      isCommenting: false,
      // Determines whether the comment modal is open
      commentsOpen: false,
      // A list of all tags
      allTags: [],
      // A list of all projects
      allProjects: [],
      // The start date of a date filter
      startFilter: null,
      // The end date of a date filter
      endFilter: null,
      // Determines whether new assets can be added
      createState: false,
    };
  },

  setup() {
    return {
      formatDate,
    };
  },

  components: {
    AssetInfo,
    AssociatedAssets,
    Comments,
    Datepicker,
    VueTagsInput,
    AddComment,
    AddAsset,
  },

  computed: {
    filteredAssets() {
      // Applies all filters to the assets view

      // Filters by asset name
      let filtered = this.assets.filter((row) =>
        row.asset_name.toLowerCase().includes(this.filter.name.toLowerCase())
      );

      // Filters by created by
      filtered = filtered.filter((row) =>
        row.created_by.user_name.first_name
          .toLowerCase()
          .includes(this.filter.created_by.toLowerCase())
      );

      // Filters by created on
      if (this.filter.created_on) {
        this.setDateFilter(this.filter.created_on);

        filtered = filtered.filter(
          (row) =>
            this.startFilter.getTime() <= Date.parse(row.created_on) &&
            Date.parse(row.created_on) <= this.endFilter.getTime()
        );
      }

      // Filters by last updated
      if (this.filter.last_updated) {
        this.setDateFilter(this.filter.last_updated);

        filtered = filtered.filter(
          (row) =>
            this.startFilter.getTime() <= Date.parse(row.last_updated) &&
            Date.parse(row.last_updated) <= this.endFilter.getTime()
        );
      }

      // Filters by asset type
      filtered = filtered.filter((row) =>
        row.asset_type.asset_type_name.toLowerCase().includes(this.filter.asset_type.toLowerCase())
      );

      // Filters by tags
      let tagNames = this.filter.tags.map((tag) => tag.text);
      filtered = filtered.filter((asset) => {
        let assetTags = asset.tags.map((tag) => tag.tag_name);
        return tagNames.every((tag) => assetTags.includes(tag));
      });

      // Filter by projects
      let projectNames = this.filter.projects.map((project) => project.text);
      filtered = filtered.filter((asset) => {
        let assetProjects = asset.projects.map((project) => project.project_name);
        return projectNames.every((project) => assetProjects.includes(project));
      });

      return filtered;
    },

    filteredTags() {
      // Filters tags for autocomplete fields
      return this.allTags.filter((tag) => {
        return tag.text.toLowerCase().includes(this.filter.tag.toLowerCase());
      });
    },

    filteredProjects() {
      // Filters projects for autocomplete fields
      return this.allProjects.filter((project) => {
        return project.text.toLowerCase().includes(this.filter.project.toLowerCase());
      });
    },

    onlyProjectsText() {
      // Displays only project name for project filters
      this.filter.projectsText = this.filter.projects.map((project) => {
        return project.text;
      });
    },

    onlyTagsText() {
      // Displays only tag names for tag filters
      this.filter.tagsText = this.filter.tags.map((tag) => {
        return tag.text;
      });
    },
  },

  methods: {
    async openModal(id) {
      // Opens the details for an asset
      this.closeModal();
      try {
        this.selectedAsset = this.assets.find((asset) => asset.asset_id === id);

        let data = await fetchAssetType(this.selectedAsset.asset_type_id);
        this.assetTypeName = data.asset_type_name;
        this.assetTypeAttributes = data.attributes;

        this.modalVisible = true;
        this.assetTypeAttributes.push(...data.parent_attributes);

        this.loadAssociatedAssets();
      } catch (error) {
        console.log(error);
      }
    },

    closeModal() {
      // Closes modals
      this.modalVisible = false;
      this.associatedVisible = false;
      this.commentsOpen = false;
      this.isCommenting = false;
      this.selectedAsset = {};
      this.loadAssets();
    },

    openComments(id) {
      // Opens the comments for an asset
      this.selectedAsset = this.assets.find((asset) => asset.asset_id === id);
      this.commentsOpen = true;
    },

    closeAddComment() {
      // Closes the modal for adding a new comment
      this.isCommenting = false;
      this.$refs.comments.getComments();
    },

    async loadAssets() {
      // Loads all asset cards from the database
      this.assets = await getAssets();
      this.sortAssets();
    },

    displayDate(dates) {
      // Returns the filters applied to dates in a reader-friendly format
      const firstDate = this.formatDate(dates[0]);

      // Displays start and end date if both are provided, and they are different
      if (dates[1]) {
        const secondDate = this.formatDate(dates[1]);
        if (firstDate != secondDate) {
          return firstDate + ", " + secondDate;
        }
      }
      return firstDate;
    },

    setDateFilter(dates) {
      // Sets the initial state for the date filters
      this.startFilter = new Date(dates[0]);
      this.endFilter = new Date(dates[1] ? dates[1] : dates[0]);

      // Sets an extra day so all assets with dates on the selected day are displayed
      this.endFilter.setDate(this.endFilter.getDate() + 1);

      // Sets hours so all assets with the dates are displayed regardless of time
      this.startFilter.setHours(0, 0, 0, 0);
      this.endFilter.setHours(0, 0, 0, 0);
    },

    async loadAssociatedAssets() {
      // Loads all assets associated with the currently detailed asset
      try {
        let res = await associateAsset(this.selectedAsset.asset_id);

        // Assigns all associated assets
        this.associatedAssets = res.map((associated) => ({
          ...associated,
          ...this.assets.find((asset) => asset.asset_id === associated.asset_id),
        }));
      } catch (error) {
        console.log(error);
      }
    },

    compareAssets(assetA, assetB) {
      // Determines order of assets when sorting by fields
      if (assetA[this.sort.sortBy] > assetB[this.sort.sortBy]) {
        return 1;
      }
      return -1;
    },

    sortAssets() {
      // Sorts order assets are displayed in
      this.assets.sort(this.compareAssets);
      if (this.sort.sortRadio === "desc") {
        this.assets.reverse();
      }
    },

    replyTo(index) {
      // Sets a new comment to reply to a given comment
      this.isCommenting = true;
      this.replyingTo = index;
    },

    async loadTags() {
      // Loads all tags from the database
      let res;
      try {
        res = await tagNames();
      } catch (error) {
        console.log(error);
      }

      this.allTags = res.map((tag) => {
        return { text: tag.tag_name };
      });
    },

    async loadProjects() {
      // Loads all projects from the database
      let res;
      try {
        res = await getProjects();
      } catch (error) {
        console.log(error);
      }

      this.allProjects = res.map((project) => {
        return { text: project.project_name };
      });
    },
  },

  async mounted() {
    this.loadAssets();
    this.loadTags();
    this.loadProjects();
  },
};
</script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.9s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: table;
}

.assetCardContainer {
  grid-template-columns: repeat(auto-fit, minmax(25em, 1fr));
}

.filterContainer {
  /* grid-template-columns: repeat(3, minmax(0, 1fr)); */
  max-width: 60rem;
}

.ti-new-tag-input-wrapper {
  margin: 0 !important;
  padding: 0 !important;
}

.vue-tags-input {
  border-radius: 0.25rem;

  border: 1px solid #ced4da;
}

.ti-input {
  padding: 0.175rem !important;
  border: 0 !important;
}

.ti-new-tag-input {
  padding: 0.375rem 0.75rem !important;
  font-size: 1rem;
  font-weight: 400;
  line-height: 1.5;
}

.closeBtn {
  padding-block: 0rem !important;
  padding-inline: 0.4rem !important;
}
</style>
