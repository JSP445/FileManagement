<template>
  <!-- This component allows the user to create a new project -->
  <div>
    <h1>Projects</h1>
    <form @submit="submitNewProject" class="d-flex flex-column w-100 gap-2">
      <label class="w-100 text-start">
        Project name
        <input
          v-model="FormData.name"
          id="project_name"
          autocomplete="off"
          type="text"
          class="form-control"
          @change="setChanged"
        />
      </label>

      <label class="w-100 text-start">
        Project Description
        <div class="input-group">
          <textarea
            class="form-control"
            aria-label="With textarea"
            v-model="FormData.description"
            @change="setChanged"
          ></textarea>
        </div>
      </label>

      Choose assets to add to project
      <div style="height: 200px" class="w-100 text-start overflow-auto">
        <div class="form-check" v-for="assets in allAssets" :key="assets.asset_id">
          <input
            class="form-check-input"
            type="checkbox"
            value=""
            @change="() => (addAsset(assets.asset_id), setChanged())"
          />
          <label class="form-check-label">
            {{ assets.asset_name }}
          </label>
        </div>
      </div>

      <input @click="addProject" type="button" value="Add project" class="btn btn-success" />
      <input @click="handleCancel" type="button" value="Cancel" class="btn btn-danger" />
    </form>
  </div>
</template>

<script>
import { dangerToast, successToast, warningToast } from "@/utils";
import { getAssets, addProject } from "@/api";

export default {
  name: "AddProject",
  components: {},

  data() {
    return {
      // Enables a confirmation message when discarding a project if true
      isChanged: false,
      // Stores a list of all assets
      allAssets: [],
      // Contains the project data to submit to the server
      FormData: {
        name: "",
        description: "",
        assets: [],
      },
    };
  },

  mounted() {
    this.getAssets();
  },

  methods: {
    addAsset(asset_id) {
      // Adds or removes an asset from the project
      this.FormData.assets.includes(asset_id)
        ? this.FormData.assets.pop(asset_id)
        : this.FormData.assets.push(asset_id);
    },

    handleCancel() {
      // Returns to all projects display if user cancels project creation
      if (this.isChanged) {
        if (!confirm("Do you want to discard in progress project?")) {
          return;
        }
      }
      this.$emit("newProjectCreated", true);
    },

    setChanged() {
      // Determines if the project has been changed, to inform users if they are discarding changes
      this.isChanged = true;
    },

    async addProject() {
      // Creates a new project and adds it to the database

      // Validates that project name isn't empty
      if (this.FormData.name.trim() == "") {
        warningToast("Enter a project name.");
        return;
      }

      // Validates that project name isn't empty
      if (this.FormData.description.trim() == "") {
        warningToast("Enter a project description.");
        return;
      }
      try {
        await addProject(this.FormData);
        successToast("Successfully added new project.");

        // Resets the fields in the form
        this.FormData.name = "";
        this.FormData.description = "";
        this.FormData.assets = [];

        this.$emit("newProjectCreated", true);
      } catch (error) {
        dangerToast(error.response.data.message);
      }
    },

    async getAssets() {
      // Loads all assets from the database
      let res;
      try {
        res = await getAssets();
        this.allAssets = res;
      } catch (error) {
        console.log(error);
      }
    },
  },
};
</script>
