<template>
  <!-- This component displays the information of an asset and allows it to be edited -->
  <form @submit.prevent="saveChanges">
    <div class="modal-container">
      <div class="modal-header">
        <h3 v-if="!editMode">{{ asset.asset_name }}</h3>
        <input v-if="editMode" type="text" v-model="edit.assetName" @change="setChanged" required />
        <div>
          <button type="submit" class="btn btn-success w-10 mx-1" v-if="editMode">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              fill="currentColor"
              class="bi bi-save-fill"
              viewBox="0 0 16 16"
            >
              <path
                d="M8.5 1.5A1.5 1.5 0 0 1 10 0h4a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2a2 2 0 0 1 2-2h6c-.314.418-.5.937-.5 1.5v7.793L4.854 6.646a.5.5 0 1 0-.708.708l3.5 3.5a.5.5 0 0 0 .708 0l3.5-3.5a.5.5 0 0 0-.708-.708L8.5 9.293V1.5z"
              />
            </svg>
            Save
          </button>
          <button type="button" class="btn btn-info w-10 mx-1" v-if="editMode" @click="setViewMode">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              fill="currentColor"
              class="bi bi-pencil-fill"
              viewBox="0 0 16 16"
            >
              <path
                d="M12.854.146a.5.5 0 0 0-.707 0L10.5 1.793 14.207 5.5l1.647-1.646a.5.5 0 0 0 0-.708l-3-3zm.646 6.061L9.793 2.5 3.293 9H3.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.207l6.5-6.5zm-7.468 7.468A.5.5 0 0 1 6 13.5V13h-.5a.5.5 0 0 1-.5-.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.5-.5V10h-.5a.499.499 0 0 1-.175-.032l-.179.178a.5.5 0 0 0-.11.168l-2 5a.5.5 0 0 0 .65.65l5-2a.5.5 0 0 0 .168-.11l.178-.178z"
              />
            </svg>
            Cancel
          </button>
          <button
            type="button"
            class="btn btn-primary w-10 mx-1"
            v-if="!editMode && canEdit"
            @click="setEditMode"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              fill="currentColor"
              class="bi bi-pencil-fill"
              viewBox="0 0 16 16"
            >
              <path
                d="M12.854.146a.5.5 0 0 0-.707 0L10.5 1.793 14.207 5.5l1.647-1.646a.5.5 0 0 0 0-.708l-3-3zm.646 6.061L9.793 2.5 3.293 9H3.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.207l6.5-6.5zm-7.468 7.468A.5.5 0 0 1 6 13.5V13h-.5a.5.5 0 0 1-.5-.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.5-.5V10h-.5a.499.499 0 0 1-.175-.032l-.179.178a.5.5 0 0 0-.11.168l-2 5a.5.5 0 0 0 .65.65l5-2a.5.5 0 0 0 .168-.11l.178-.178z"
              />
            </svg>
            Edit
          </button>
          <button
            type="button"
            class="btn btn-danger w-10 mx-1"
            v-if="canEdit"
            @click="deleteAsset"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              fill="white"
              class="bi bi-trash3-fill"
              viewBox="0 0 16 16"
            >
              <path
                d="M11 1.5v1h3.5a.5.5 0 0 1 0 1h-.538l-.853 10.66A2 2 0 0 1 11.115 16h-6.23a2 2 0 0 1-1.994-1.84L2.038 3.5H1.5a.5.5 0 0 1 0-1H5v-1A1.5 1.5 0 0 1 6.5 0h3A1.5 1.5 0 0 1 11 1.5Zm-5 0v1h4v-1a.5.5 0 0 0-.5-.5h-3a.5.5 0 0 0-.5.5ZM4.5 5.029l.5 8.5a.5.5 0 1 0 .998-.06l-.5-8.5a.5.5 0 1 0-.998.06Zm6.53-.528a.5.5 0 0 0-.528.47l-.5 8.5a.5.5 0 0 0 .998.058l.5-8.5a.5.5 0 0 0-.47-.528ZM8 4.5a.5.5 0 0 0-.5.5v8.5a.5.5 0 0 0 1 0V5a.5.5 0 0 0-.5-.5Z"
              />
            </svg>
            Delete
          </button>
        </div>
      </div>

      <div class="modal-body overflow-auto" style="height: 50vh">
        <table class="table table-borderless">
          <tbody>
            <tr>
              <td>Asset Type:</td>
              <td>{{ assetTypeName }}</td>
            </tr>
            <tr>
              <td>Created By:</td>
              <td>
                {{ asset.created_by.user_name.first_name }}
                {{ asset.created_by.user_name.last_name }} ({{ asset.created_by.email }})
              </td>
            </tr>
            <tr>
              <td>Created On:</td>
              <td>{{ formatDate(asset.created_on) }}</td>
            </tr>
            <tr>
              <td>Last Updated:</td>
              <td>{{ formatDate(asset.last_updated) }}</td>
            </tr>
          </tbody>
        </table>

        <p class="text-black">Tags:</p>
        <vue-tags-input
          v-if="editMode"
          v-model="tag"
          :tags="tags"
          :autocomplete-items="filteredTags"
          @tags-changed="
            (newTags) => {
              setChanged();
              return (tags = newTags);
            }
          "
        />
        <vue-horizontal responsive v-if="!editMode">
          <div class="mx-1" v-for="tag in tags" :key="tag.text">
            <p class="list-group-item">{{ tag.text }}</p>
          </div>
        </vue-horizontal>

        <p class="text-black">Projects:</p>

        <vue-tags-input
          v-if="editMode"
          v-model="project"
          :tags="projects"
          :autocomplete-items="filteredProjects"
          :add-only-from-autocomplete="true"
          @tags-changed="
            (newProjects) => {
              setChanged();
              return (projects = newProjects);
            }
          "
        />

        <vue-horizontal responsive v-if="!editMode">
          <div class="mx-1" v-for="project in asset.projects" :key="project.project_id">
            <a class="list-group-item">{{ project.project_name }}</a>
          </div>
        </vue-horizontal>

        <p class="text-black">Attributes:</p>
        <table class="table table-striped table-bordered">
          <thead>
            <tr>
              <th>Name</th>
              <th>Value</th>
            </tr>
          </thead>

          <tbody v-if="!editMode">
            <tr v-for="attribute in asset.attribute_values" :key="attribute.asset_attribute_id">
              <td>
                {{ getAttribute(attribute.asset_attribute_type_id) }}
              </td>
              <td>{{ attribute.attribute_value }}</td>
            </tr>
          </tbody>

          <tbody v-if="editMode">
            <tr v-for="attribute in edit.attributes" :key="attribute.asset_attribute_id">
              <td>
                {{ attribute.attribute_name }}
              </td>
              <td>
                <input
                  :type="attribute.attribute_type_id == 2 ? 'number' : 'text'"
                  v-model="attribute.attribute_value"
                  @change="setChanged"
                  required
                />
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="modal-footer flex-nowrap" :class="{ 'justify-content-between': canEdit }">
        <slot class="d-flex flex-row">
          <button
            type="button"
            class="btn btn-info w-100"
            @click="$emit('associated')"
            v-if="!associatedVisible && hasAssociated"
          >
            Associated Assets
          </button>
          <button type="button" class="btn btn-primary w-100" @click="$emit('comments')">
            Comments
          </button>

          <button
            type="button"
            class="btn btn-secondary w-100"
            v-if="!editMode"
            @click="$emit('close')"
          >
            Close
          </button>
        </slot>
      </div>
    </div>
  </form>
</template>

<script>
import { dangerToast, formatDate, successToast } from "@/utils";
import { getProjects, deleteAsset, updateAsset, tagNames } from "@/api";
import VueTagsInput from "@sipec/vue3-tags-input";
import VueHorizontal from "vue-horizontal";

export default {
  name: "AssetInfo",
  props: [
    // The asset for which the info is being displayed
    "asset",
    // The attributes of the asset's asset type
    "assetTypeAttributes",
    // The name of the asset type of the asset
    "assetTypeName",
    // Used to display the associayted assets if it is true
    "associatedVisible",
    // Checks if asset has any associated assets, so a blank pop-up doesn't display
    "hasAssociated",
  ],
  emits: [
    // Closes the pop-up
    "close",
    // Toggles visibility the associated assets
    "associated",
  ],

  components: {
    VueTagsInput,
    VueHorizontal,
  },

  setup() {
    return {
      formatDate,
    };
  },

  data() {
    return {
      // The  project and tag entered in the fields when editing
      project: "",
      tag: "",
      // A list of all project and tag names
      projects: [],
      tags: [],
      // A list of all projects and tags
      allProjects: [],
      allTags: [],
      // Enables the editing features if true
      editMode: false,
      // Object containing edits made to the asset
      edit: {},
      // The security required to make edits to assets
      requiredSecurity: 50,
      // Allows user to edit if they have the required security level
      canEdit: false,
    };
  },

  computed: {
    filteredProjects() {
      // Filters projects for autocomplete fields
      return this.allProjects.filter((project) => {
        return project.text.toLowerCase().includes(this.project.toLowerCase());
      });
    },

    filteredTags() {
      // Filters tags for autocomplete fields
      return this.allTags.filter((tag) => {
        return tag.text.toLowerCase().includes(this.tag.toLowerCase());
      });
    },
  },

  methods: {
    getAttribute(id) {
      // Gets the attribute name for a given id
      return this.assetTypeAttributes.find((attribute) => attribute.asset_attribute_id === id)
        .attribute_name;
    },

    async deleteAsset() {
      // Removes an asset from the database
      let res;
      if (confirm("Are you sure you want to delete this asset?")) {
        try {
          res = await deleteAsset({ asset_id: this.asset.asset_id });
          successToast(`Asset "${res[0].asset_name}" deleted.`);
          this.$emit("close");
        } catch (error) {
          dangerToast(error.respose.data.message);
        }
      }
    },

    async saveChanges() {
      // Updates an asset in the database
      if (!this.edit.changed || !confirm("Are you sure you want to save your changes?")) {
        this.$emit("close");
        return;
      }

      // Sets data to update on the asset
      let data = {
        asset_id: this.asset.asset_id,
        asset_name: this.edit.assetName,
        attributes: {},
        tag_names: this.tags.map((tag) => tag.text),
        project_names: this.projects.map((project) => project.text),
      };
      // Sets the attributes to update on the asset
      this.edit.attributes.forEach((attribute) => {
        const id = attribute.asset_attribute_type_id;
        data.attributes[id] = attribute.attribute_value.toString();
      });

      try {
        let res = await updateAsset(data);
        successToast(res.message);
        this.$emit("close");
      } catch (error) {
        dangerToast(error.response.data.message);
      }
    },

    setEditMode() {
      // Sets fields for editing an asset
      this.editMode = true;
      this.edit.assetName = this.asset.asset_name;
      this.edit.changed = false;
      this.edit.attributes = [];

      // Sets all the current attributes of the asset
      this.asset.attribute_values.forEach((attribute) =>
        this.edit.attributes.push({
          asset_attribute_type_id: attribute.asset_attribute_type_id,
          attribute_value: attribute.attribute_value,
          attribute_name: attribute.attribute_name.attribute_name,
          attribute_type_id: attribute.attribute_name.attribute_type_id,
        })
      );
    },

    setViewMode() {
      // Stops the asset editing fields from displaying
      if (!this.edit.changed || confirm("Are you sure you want to discard your changes?")) {
        this.editMode = false;
      }
    },

    setChanged() {
      // Determines if the asset has been changed, to inform users if they are discarding changes
      this.edit.changed = true;
    },

    async loadProjects() {
      // Loads all projects from the database
      let res;
      try {
        res = await getProjects();
        this.allProjects = res.map(({ project_name }) => ({
          text: project_name,
        }));
      } catch (error) {
        console.log(error);
      }
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
  },

  mounted() {
    // Determines if user can edit assets
    this.canEdit = this.$store.getters.securityLevel >= this.requiredSecurity;

    this.loadTags();
    this.loadProjects();
    this.tags = this.asset.tags.map((tag) => {
      let object = {};
      object.text = tag.tag_name;
      return object;
    });
    this.projects = this.asset.projects.map(({ project_name }) => ({
      text: project_name,
    }));
  },
};
</script>
