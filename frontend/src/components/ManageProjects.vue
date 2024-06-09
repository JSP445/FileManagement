<template>
  <!-- This component displays all projects and allows them to be edited -->
  <div class="mb-3">
    <transition name="fade">
      <div v-if="modalVisible" :class="{ 'modal-mask': modalVisible }">
        <div
          class="d-flex w-100 h-100 align-items-center justify-content-center position-absolute gap-3"
        >
          <AssetInfo
            v-bind:asset="selectedAsset"
            v-bind:assetTypeName="assetTypeName"
            v-bind:assetTypeAttributes="assetTypeAttributes"
            @close="closeModal"
            class="w-50"
          />
        </div>
      </div>
    </transition>

    <div class="d-flex justify-content-center gap-5 mt-5">
      <div id="container" class="d-flex flex-column">
        <div class="list-group">
          <a
            @click="fetchProject(project.project_id)"
            class="text-start list-group-item list-group-action text-break"
            v-for="project in projects"
            :key="project.project_id"
          >
            {{ project.project_name }}
          </a>
        </div>
        <br />
        <input
          v-if="!isAddMode"
          @click="isAddMode = true"
          type="button"
          class="btn btn-primary w-100 adminBtn"
          value="Add Project"
        />
      </div>
      <div class="d-flex flex-column" id="current-asset-type" v-if="currentProject || isAddMode">
        <div v-if="isAddMode">
          <AddProject
            @newProjectCreated="
              () => {
                fetchProjects(), (isAddMode = false);
              }
            "
          />
        </div>

        <div v-if="!isAddMode">
          <div class="d-flex gap-3 justify-content-between mb-4">
            <input
              @click="toggleEdit(false)"
              class="btn btn-primary w-100"
              type="button"
              :value="editReset"
            />

            <input
              v-if="isEditMode"
              @click="handleSave"
              class="btn btn-success w-100"
              type="button"
              value="Save"
            />

            <input
              @click="handleDelete"
              class="btn btn-danger w-100"
              type="button"
              value="Delete"
            />
          </div>

          <input
            v-model="currentProject.project_name"
            ref="project_name"
            autocomplete="off"
            type="text"
            class="form-control"
            @change="setChanged"
            disabled
          />
          <br />
          <div>
            Created by: {{ currentProject.created_by.user_name.first_name }}
            {{ currentProject.created_by.user_name.last_name }} ({{
              currentProject.created_by.email
            }})
          </div>
          <div>Created on: {{ formatDate(currentProject.created_on) }}</div>

          <br />
          <label class="w-100 text-start">Description:</label>
          <div class="input-group">
            <textarea
              ref="project_description"
              class="form-control"
              aria-label="With textarea"
              v-model="currentProject.project_description"
              @change="setChanged"
              disabled
            ></textarea>
          </div>
          <br />
          <div id="assets" v-if="currentProject.assets.length > 0 || isEditMode">
            <p>Assets:</p>

            <vue-horizontal responsive v-if="!isEditMode">
              <div class="mx-1" v-for="asset in currentProject.assets" :key="asset.asset_id">
                <a class="list-group-item" @click="openModal(asset)">{{ asset.asset_name }}</a>
              </div>
            </vue-horizontal>

            <vue-tags-input
              v-if="isEditMode"
              v-model="asset"
              :tags="assets"
              :autocomplete-items="filteredAssets"
              :add-only-from-autocomplete="true"
              @tags-changed="
                (newAssets) => {
                  setChanged();
                  return (assets = newAssets);
                }
              "
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {
  getProjects,
  getProject,
  getAsset,
  fetchAssetType,
  getAssets,
  editProject,
  deleteProject,
} from "@/api";
import { dangerToast, formatDate, successToast } from "@/utils";
import AddProject from "@/components/AddProject.vue";
import AssetInfo from "@/components/AssetInfo.vue";
import VueHorizontal from "vue-horizontal";
import VueTagsInput from "@sipec/vue3-tags-input";

export default {
  name: "Project",
  components: {
    VueTagsInput,
    VueHorizontal,
    AddProject,
    AssetInfo,
  },

  setup() {
    return {
      formatDate,
    };
  },

  data() {
    return {
      // The asset entered in the field when editing
      asset: "",
      // A list of all asset names
      assets: [],
      // A list of all assets
      allAssets: [],
      // Enables a confirmation message when discarding a project if true
      isChange: false,
      // The value of the button for editing and reseting edits
      editReset: "Edit",
      // An asset being viewed in a modal
      selectedAsset: null,
      // The project currently being viewed
      currentProject: null,
      // The attributes of the selected asset
      assetTypeAttributes: null,
      // The name of the asset type of the selected asset
      assetTypeName: null,
      // Determines if the asset info modal is displayed
      modalVisible: false,
      // Determines if new projects can be added
      isAddMode: false,
      // Enables the editing features if true
      isEditMode: false,
      // A list of all projects
      projects: [],
    };
  },

  computed: {
    filteredAssets() {
      // Filters assets for autocomplete fields
      return this.allAssets
        .filter((asset) => !this.assets.includes(asset))
        .filter((asset) => asset.asset_name.toLowerCase().includes(this.asset.toLowerCase()))
        .map(({ asset_name }) => ({ text: asset_name }));
    },
  },

  methods: {
    async openModal(asset) {
      // Opens details for a selected asset
      try {
        this.closeModal();
        let assetType = await fetchAssetType(asset.asset_type_id);
        this.assetTypeName = assetType.asset_type_name;
        this.assetTypeAttributes = assetType.attributes;
        this.selectedAsset = await getAsset(asset.asset_id);
        this.modalVisible = true;
      } catch (error) {
        console.log(error);
      }
    },

    setChanged() {
      // Determines if the project has been changed, to inform users if they are discarding changes
      this.isChange = true;
    },

    closeModal() {
      // Closes the asset details modal
      this.modalVisible = false;
      this.selectedAsset = null;
    },

    async toggleEdit(isAssetChange) {
      // Changes between editing mode and viewing mode
      this.isEditMode = !this.isEditMode;
      if (!this.isEditMode) {
        if (this.isChange) {
          if (!confirm("Do you want to discard your changes?")) {
            return;
          }
          this.isChange = false;
          if (isAssetChange == false) {
            // Gets the details of the selected project
            await this.fetchProject(this.currentProject.project_id);
          }
        }
        this.editReset = "Edit";
      } else {
        this.editReset = "Reset";
      }
      // Sets fields to be edited
      this.asset = "";
      this.$refs.project_name.disabled = !this.$refs.project_name.disabled;
      this.$refs.project_description.disabled = !this.$refs.project_description.disabled;
    },

    async handleSave() {
      // Updates a project in the database
      if (!confirm("Do you want to save your changes?")) {
        return;
      }
      // Sets data to update on the project
      let data = {
        project_name: this.currentProject.project_name,
        project_description: this.currentProject.project_description,
        assets: this.assets.map(({ text }) => text),
      };

      try {
        let res = await editProject(this.currentProject.project_id, data);
        successToast("Updated project.");
        this.currentProject = res;
        this.fetchProjects();
        this.isChange = false;
        this.toggleEdit();
      } catch (error) {
        dangerToast(error.response.data.message);
      }
    },

    async handleDelete() {
      // Removes a project in the database
      if (!confirm("Are you sure you want to delete this project?")) {
        return;
      }
      try {
        let res;
        res = await deleteProject(this.currentProject.project_id);
        successToast(`Project "${res.project_name}" deleted.`);
        this.currentProject = null;
        this.isChange = false;
        this.fetchProjects();
      } catch (error) {
        console.log(error);
      }
    },

    async fetchProject(id) {
      // Loads a project for a given id
      try {
        if (this.isEditMode) {
          this.toggleEdit(true);
        }
        this.currentProject = await getProject(id);
        this.assets = this.currentProject.assets.map(({ asset_name }) => ({
          text: asset_name,
        }));
      } catch (error) {
        console.log(error);
      }
    },

    async fetchAssets() {
      // Loads all assets from the database
      let res;
      try {
        res = await getAssets();
        this.allAssets = res;
      } catch (error) {
        console.log(error);
      }
    },

    async fetchProjects() {
      // Loads all projects from the database
      let res;
      try {
        res = await getProjects();
        this.projects = res;
      } catch (error) {
        console.log(error);
      }
    },
  },

  mounted() {
    this.fetchProjects();
    this.fetchAssets();
  },
};
</script>

<style scoped>
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
</style>
