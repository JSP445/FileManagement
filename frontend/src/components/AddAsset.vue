<template>
  <!-- This component allows for the creation of new assets -->
  <div class="addAsset addAssetContainer | m-auto">
    <form @submit.prevent="addAsset">
      <div class="mx-2 my-4">
        <label>Asset Name</label>
        <input
          v-model="assetName"
          class="form-control"
          type="text"
          placeholder="Asset Name"
          required
        />
      </div>

      <div class="mx-2 my-4">
        <label>Asset Type</label>
        <select v-model="assetType" class="form-select" @change="setAttributes" required>
          <option v-for="type in assetTypes" :key="type.asset_type_id">
            {{ type.asset_type_name }}
          </option>
        </select>
      </div>

      <!-- Creates input boxes for all the attriubtes of the type -->
      <div class="mx-2 my-2" v-if="attributes.length != 0">
        <label class="h3 border-bottom pb-1 w-100">Attributes</label>
        <br />

        <div v-for="attribute in attributes" :key="attribute.attribute_id">
          <label class="mt-2">{{ attribute.name }}</label>
          <input
            v-model="attribute.value"
            :type="attribute.type_id == 2 ? 'number' : 'text'"
            placeholder="Attribute value"
            class="w-100 form-control"
            required
          />
        </div>
        <br />
      </div>

      <div class="mx-2 mb-4">
        <label>Tags</label>
        <vue-tags-input
          v-model="tag"
          :tags="tags"
          :autocomplete-items="filteredTags"
          @tags-changed="(newTags) => (tags = newTags)"
        />
      </div>

      <div class="mx-2 mb-4">
        <label>Projects</label>
        <vue-tags-input
          v-model="project"
          placeholder="Add Project"
          :tags="projects"
          :autocomplete-items="filteredProjects"
          :add-only-from-autocomplete="true"
          @tags-changed="(newProjects) => (projects = newProjects)"
        />
      </div>
      <div class="d-flex gap-4 mx-2">
        <button class="btn btn-success w-100">Add Asset</button>
        <input
          type="button"
          class="btn btn-secondary w-100"
          value="View Assets"
          @click="$emit('close')"
        />
      </div>
    </form>
  </div>
</template>

<script>
import { fetchAllAssetTypes, addAsset, tagNames, getProjects } from "@/api";
import { dangerToast, successToast } from "@/utils";
import VueTagsInput from "@sipec/vue3-tags-input";

export default {
  name: "addAssets",
  components: {
    VueTagsInput,
  },

  data() {
    return {
      // Contains the current entered project
      project: "",
      // All the selected projects
      projects: [],
      // All the projects currently in the system
      allProjects: [],
      // Stores the name of the new asset
      assetName: "",
      // The type of the new asset
      assetType: "",
      // Any attributes the new asset has
      attributes: [],
      // All the asset types in the system
      assetTypes: null,
      // Contains the current entered tag
      tag: "",
      // All the selected tags
      tags: [],
      // All the tags currently in the sytem
      allTags: [],
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
    async addAsset(e) {
      // Creates a new asset and stores it in the database

      // Removes default form behaviour as the submit is custom
      e.preventDefault();

      let asset = {
        asset_name: this.assetName,
        asset_type_id: this.assetTypes.find((type) => type.asset_type_name == this.assetType)
          .asset_type_id,
        attributes: {},
        tag_names: this.tags.map((tag) => tag.text),
        project_names: this.projects.map((project) => project.text),
      };
      this.attributes.forEach(
        (attribute) => (asset.attributes[attribute.name] = attribute.value.toString())
      );

      let res;
      try {
        res = await addAsset(asset);
        this.resetFields();
        successToast(`Asset "${res.asset_name}" successfully created.`);
      } catch (error) {
        dangerToast(error.response.data.message);
      }
    },

    resetFields() {
      // Resets input fields once a new asset is made
      this.assetName = "";
      this.assetType = "";
      this.attributes = [];
      this.tags = [];
      this.projects = [];
    },

    async loadAssetTypes() {
      // Loads all asset types from the database
      try {
        this.assetTypes = await fetchAllAssetTypes();
      } catch (error) {
        console.log(error);
      }
    },

    setAttributes() {
      // Sets all the attribute names for the selected asset type
      this.attributes = [];

      let baseAssetType = this.assetTypes.find(
        (asset_type) => asset_type.asset_type_name == this.assetType
      );

      let assetAttributes = [];
      assetAttributes.push(...baseAssetType.attributes);
      console.log(assetAttributes);

      while (baseAssetType.inherited_from != baseAssetType.asset_type_id) {
        baseAssetType = this.assetTypes.find(
          (asset_type) => asset_type.asset_type_id == baseAssetType.inherited_from
        );
        assetAttributes.push(...baseAssetType.attributes);
      }

      assetAttributes.forEach((attribute) =>
        this.attributes.push({
          name: attribute.attribute_name,
          value: "",
          type_id: attribute.attribute_type_id,
        })
      );
    },

    async loadProjects() {
      // Loads all projects from the database
      let res;
      try {
        res = await getProjects();
      } catch (error) {
        console.log(error);
      }

      this.allProjects = res.map(({ project_name }) => ({
        text: project_name,
      }));
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
    this.loadAssetTypes();
    this.loadTags();
    this.loadProjects();
  },
};
</script>

<style scoped>
.no-border {
  border: 0;
  box-shadow: none;
}
.addAssetContainer {
  width: clamp(20rem, 70%, 40rem);
}
</style>
