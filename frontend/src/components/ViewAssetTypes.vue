<template>
  <!-- This component allows for CRUD operations on asset types -->
  <div class="d-flex justify-content-center gap-5 mt-5">
    <!-- Contains a list of all asset types -->
    <div id="container" class="d-flex flex-column">
      <div class="list-group">
        <a
          @click="getAssetType(assetType.asset_type_id)"
          class="text-start list-group-item list-group-item-action text-break"
          v-for="assetType in allAssetTypes"
          :key="assetType.asset_type_id"
          :class="{
            'active text-white':
              currentAssetType && assetType.asset_type_id == currentAssetType.asset_type_id,
          }"
        >
          {{ assetType.asset_type_name }}
        </a>
        <input
          @click="toggleCreateMode"
          type="button"
          class="text-center list-group-item list-group-item-action text-break bg-success text-white fake-success"
          value="Add new Asset Type"
        />
      </div>
    </div>

    <!-- Contains the currently selected asset type for viewing/ updating -->
    <div class="d-flex flex-column" id="current-asset-type" v-if="currentAssetType && !createState">
      <div
        class="d-flex gap-3 justify-content-between mb-4"
        v-if="this.currentAssetType.asset_type_id != 0"
      >
        <input @click="toggleEdit" class="btn btn-primary w-100" type="button" :value="editReset" />

        <input
          v-if="editState"
          @click="handleSavePressed"
          class="btn btn-success w-100"
          type="button"
          value="Save"
        />

        <input @click="handleDelete" class="btn btn-danger w-100" type="button" value="Delete" />
      </div>

      <input
        v-if="this.currentAssetType.asset_type_id != 0"
        @keyup="editAssetTypeName"
        ref="assetTypeName"
        class="form-control fw-bold mb-3"
        type="text"
        :value="currentAssetType.asset_type_name"
        disabled
      />
      <p v-else class="form-control fw-bold mb-3">{{ currentAssetType.asset_type_name }}</p>
      <p v-if="createState">
        Created by: {{ currentAssetType.created_by.user_name.first_name }}
        {{ currentAssetType.created_by.user_name.last_name }}
        <span v-if="currentAssetType.created_by.email"
          >({{ currentAssetType.created_by.email }})</span
        >
      </p>
      <p>Created on: {{ formatDate(currentAssetType.created_on) }}</p>
      <p v-if="this.currentAssetType.asset_type_id != 0">
        Last updated: {{ formatDate(currentAssetType.last_updated) }}
      </p>
      <p v-if="this.currentAssetType.asset_type_id != 0">
        Inherits from: {{ currentAssetType.parent_name }}
      </p>
      <h3 class="border-bottom pb-1">Attributes</h3>
      <div
        v-if="this.currentAssetType.parent_attributes && this.currentAssetType.asset_type_id != 0"
        class="d-flex flex-column gap-3 mt-3 border-bottom pb-4 mb-2"
      >
        <div
          class="d-flex gap-2 w-100"
          v-for="attribute in currentAssetType.parent_attributes"
          :key="attribute.asset_attribute_id"
        >
          <p class="form-control w-100 m-0">
            {{ attribute.attribute_name }}
          </p>
          <div class="w-50">
            <p
              class="m-0"
              v-for="attribute_type in attribute_types"
              :key="attribute_type.type_id"
              :value="attribute_type.type_id"
            >
              <span
                class="form-control"
                v-if="attribute_type.type_id == attribute.attribute_type_id"
                >{{ attribute_type.type_name }}</span
              >
            </p>
          </div>
        </div>
      </div>

      <!-- Contains the list of attributes -->
      <div ref="attributeList" class="d-flex flex-column gap-3 mt-3">
        <div
          v-for="attribute in currentAssetType.attributes"
          :key="attribute.asset_attribute_id"
          type="text"
          spellcheck="false"
          class="d-inline-flex gap-2 w-100"
        >
          <input
            type="text"
            class="form-control w-100"
            :value="attribute.attribute_name"
            :id="attribute.asset_attribute_id"
            @keyup="editAttributeValue"
            v-if="this.currentAssetType.asset_type_id != 0"
            disabled
          />
          <p v-else class="form-control w-100 m-0">{{ attribute.attribute_name }}</p>
          <select
            v-model="attribute.attribute_type_id"
            ref="attributeTypes"
            class="form-select w-50"
            v-if="this.currentAssetType.asset_type_id != 0"
            disabled
          >
            <option
              @change="editAttributeType"
              v-for="attribute_type in attribute_types"
              :key="attribute_type.type_id"
              :value="attribute_type.type_id"
            >
              {{ attribute_type.type_name }}
            </option>
          </select>
          <div v-else class="w-50">
            <p
              class="m-0"
              v-for="attribute_type in attribute_types"
              :key="attribute_type.type_id"
              :value="attribute_type.type_id"
            >
              <span
                class="form-control"
                v-if="attribute_type.type_id == attribute.attribute_type_id"
                >{{ attribute_type.type_name }}</span
              >
            </p>
          </div>

          <input
            type="button"
            @click="toggleDeleteAttribute"
            class="btn btn-danger w-25"
            value="Delete"
            v-if="editState"
          />
        </div>

        <input
          v-if="this.currentAssetType.asset_type_id != 0"
          @click="addAttribute"
          type="button"
          value="Add new attribute"
          class="btn btn-success w-100"
        />
      </div>
    </div>

    <!-- Opens the create component -->
    <div v-if="createState" class="createAssetType">
      <CreateAssetType @newAssetTypeCreated="getAssetTypes" :allAssetTypes="allAssetTypes" />
    </div>
  </div>
</template>

<script>
import {
  fetchAssetTypes,
  fetchAssetType,
  removeAssetType,
  updateAssetType,
  getAttributeTypes,
} from "@/api";
import { dangerToast, formatDate, successToast } from "@/utils";
import CreateAssetType from "@/components/CreateAssetType.vue";

export default {
  name: "ViewAssetTypes",
  components: {
    CreateAssetType,
  },

  data() {
    return {
      // Stores a list of all the names of the asset types
      allAssetTypes: null,
      // Stores the currently selected full assest type
      currentAssetType: null,
      // Used to revert back if changes are cancelled
      currentAssetTypeDefault: null,
      // Enables the edit features if true
      editState: false,
      // The text in the edit button (toggles between Edit/ Reset)
      editReset: "Edit",
      // Used to give new attributes an ID that can then be detected and changed by the server
      tempAttributeID: 0,
      // Contains the IDs of any deleted attributes
      deletedAttributes: new Set(),
      // Stores the types of attributes
      attribute_types: [],
      // Toggles between showing the create component and the view component
      createState: false,
    };
  },

  setup() {
    return {
      // Formats the date time to a consitent structure
      formatDate,
    };
  },

  mounted() {
    this.getAssetTypes();
    this.loadAttributeTypes();
  },

  methods: {
    toggleCreateMode() {
      // Sets the current asset type to none and enables the create mode
      this.currentAssetType = {};
      this.currentAssetTypeDefault = null;
      this.createState = true;
    },

    async getAssetTypes() {
      // Gets the names of the asset types from the server
      let res;
      try {
        res = await fetchAssetTypes();
        this.allAssetTypes = res;
      } catch (error) {
        console.log(error);
      }
    },

    async getAssetType(id) {
      // Gets a specific full asset type

      // Toggle Edit off if there is a previous asset type loaded.
      if (this.currentAssetType) {
        this.toggleEditOff();
      }
      // If the create state is active set it to false
      if (this.createState) {
        this.createState = false;
      }

      try {
        const assetType = await fetchAssetType(id);
        this.currentAssetType = assetType;
        // Creates a full unique copy of the selected asset type
        this.currentAssetTypeDefault = JSON.parse(JSON.stringify(this.currentAssetType));
      } catch (error) {
        console.log(error);
      }
    },

    async toggleEdit() {
      // Toggles the edit features
      if (!this.editState) {
        this.toggleEditOn();
      } else {
        this.toggleEditOff();
        // Loads the asset type if changes are made
        await this.getAssetType(this.currentAssetType.asset_type_id);
      }
    },

    toggleEditOff() {
      // Turns the edit features off
      this.editReset = "Edit";
      this.editState = false;
      this.deletedAttributes.clear();
      if (!this.$refs.attributeList) {
        return;
      }
      const { children } = this.$refs.attributeList;
      for (let attribute of children) {
        try {
          attribute.firstChild.disabled = true;
          attribute.firstChild.classList.remove("pe-none");
          attribute.firstChild.classList.remove("alert-danger");
          attribute.children.item(1).disabled = true;
          attribute.children.item(1).classList.remove("pe-none");
          attribute.children.item(1).classList.remove("alert-danger");
          attribute.lastChild.classList.remove("btn-primary");
          attribute.lastChild.classList.add("btn-danger");
          attribute.lastChild.value = "Delete";
          attribute.lastChild.disabled = true;
        } catch (error) {
          // The last child of children is the add button so the catch can be ignored
        }
      }
      if (this.$refs.assetTypeName) {
        this.$refs.assetTypeName.disabled = true;
      }
    },

    toggleEditOn() {
      // Turns the edit features on
      this.editReset = "Reset";
      this.editState = true;
      const { children } = this.$refs.attributeList;
      for (let attribute of children) {
        // All the inputs are enabled
        try {
          attribute.firstChild.disabled = false;
          attribute.children.item(1).disabled = false;
          attribute.lastChild.disabled = false;
        } catch (error) {
          // The last child of children is the add button so the catch can be ignored
        }
      }
      this.$refs.assetTypeName.disabled = false;
    },

    handleSavePressed() {
      // validates the asset type before saving
      const attributesAsSet = new Set();
      let attributeChangesFound = false;
      let attributeTypeChangesFound = false;

      let index = 0;
      while (index < this.currentAssetType.attributes.length) {
        // Performs validation of attributes
        let attribute = this.currentAssetType.attributes[index];
        // Checks if the attribute has been deleted
        if (this.deletedAttributes.has(attribute.asset_attribute_id)) {
          this.currentAssetType.attributes.splice(index, 1);
          continue;
        }

        // Checks the attribute has a name
        if (!attribute.attribute_name) {
          dangerToast("Cannot have empty attribute.");
          return;
        }

        // Checks the attribute has a type
        if (!attribute.attribute_type_id) {
          dangerToast("Attribute must have a Type.");
          return;
        }

        // Checks default attributes have changes.
        if (
          this.currentAssetTypeDefault.attributes[index] &&
          attribute.attribute_name != this.currentAssetTypeDefault.attributes[index].attribute_name
        ) {
          attributeChangesFound = true;
        }

        // Checks default attribute types have changes
        if (
          this.currentAssetTypeDefault.attributes[index] &&
          attribute.attribute_type_id !=
            this.currentAssetTypeDefault.attributes[index].attribute_type_id
        ) {
          attributeTypeChangesFound = true;
        }

        // Adds to set of attributes
        attributesAsSet.add(attribute.attribute_name);
        index++;
      }

      // Checks changes have occurred
      if (
        !attributeChangesFound &&
        !attributeTypeChangesFound &&
        this.currentAssetTypeDefault.asset_type_name == this.currentAssetType.asset_type_name &&
        this.currentAssetType.attributes.length == this.currentAssetTypeDefault.attributes.length
      ) {
        dangerToast("No changes made.");
        return;
      }

      // Checks there are no duplicate attributes
      if (attributesAsSet.size != this.currentAssetType.attributes.length) {
        dangerToast("Cannot have duplicate attributes.");
        return;
      }

      // Checks the Asset Type name is not taken
      if (
        this.allAssetTypes.find(
          (assetType) => assetType.asset_type_name === this.currentAssetType.asset_type_name
        ) &&
        this.currentAssetType.asset_type_name != this.currentAssetTypeDefault.asset_type_name
      ) {
        dangerToast("Cannot have duplicate Asset Type names.");
        return;
      }

      // Checks the Asset Type name is not blank
      if (!this.currentAssetType.asset_type_name) {
        dangerToast("Asset Type must have a name.");
        return;
      }
      this.saveChanges();
    },

    async saveChanges() {
      // Send the request to the server to update the asset type
      if (confirm("Are you sure you want to save changes?")) {
        try {
          await updateAssetType(this.currentAssetType);
          this.toggleEditOff();
          await this.getAssetType(this.currentAssetType.asset_type_id);
          this.getAssetTypes();

          // Updates the default
          this.currentAssetTypeDefault = JSON.parse(JSON.stringify(this.currentAssetType));
          successToast("Changes saved.");
        } catch (error) {
          dangerToast(error.response.data.message);
          this.toggleEditOff();
          await this.getAssetType(this.currentAssetType.asset_type_id);
        }
      }
    },

    async handleDelete() {
      // Deletes the asset type
      if (confirm("Are you sure you want to delete this?")) {
        try {
          let res = await removeAssetType(this.currentAssetType.asset_type_id);
          await this.getAssetTypes();
          this.currentAssetType = null;
          successToast(`Asset type "${res[0].asset_type_name}" deleted.`);
        } catch (error) {
          console.log(error);
        }
      }
    },

    addAttribute() {
      // Adds an attribute to the list of attributes

      // the tempID is decremented
      this.tempAttributeID--;
      // The new attribue is pushed into the list
      this.currentAssetType.attributes.push({
        asset_attribute_id: this.tempAttributeID,
        asset_type_id: 0,
        attribute_name: "",
      });
      const { children } = this.$refs.attributeList;
      // On the next tick, the new box gains focus
      this.$nextTick(() => {
        children[children.length - 2].firstChild.disabled = false;
        children[children.length - 2].children.item(1).disabled = false;
        children[children.length - 2].lastChild.disabled = false;
        children[children.length - 2].firstChild.focus();
        // If not already, edit mode is turned on
        if (!this.editState) {
          this.toggleEditOn();
        }
      });
    },

    editAttributeType(event) {
      // Update the type of the attribute on change
      for (let attribute of this.currentAssetType.attributes) {
        if (attribute.asset_attribute_id == event.target.id) {
          attribute.attribute_type_id = event.target.value;
          break;
        }
      }
    },

    editAttributeValue(event) {
      // Update the name of the attribute on change
      for (let attribute of this.currentAssetType.attributes) {
        if (attribute.asset_attribute_id == event.target.id) {
          attribute.attribute_name = event.target.value;
          break;
        }
      }
    },

    editAssetTypeName(event) {
      // The type name is upadted on change
      this.currentAssetType.asset_type_name = event.target.value;
    },

    toggleDeleteAttribute(event) {
      // Toggles attributes being deleted/ restored
      if (event.target.value == "Undo") {
        this.restoreAttribute(event);
      } else {
        this.deleteAttribute(event);
      }
    },

    deleteAttribute(event) {
      // Deletes an attribute on the frontend
      event.target.classList.remove("btn-danger");
      console.log(event.target);
      event.target.value = "Undo";
      event.target.classList.add("btn-primary");
      let typeMenu = event.target.previousElementSibling;
      let attributeBox = typeMenu.previousElementSibling;
      typeMenu.classList.add("alert-danger");
      typeMenu.classList.add("pe-none");
      attributeBox.classList.add("alert-danger");
      attributeBox.classList.add("pe-none");
      this.deletedAttributes.add(
        parseInt(event.target.previousElementSibling.previousElementSibling.id)
      );
    },

    restoreAttribute(event) {
      // Restores delteted attributes on the frontend
      event.target.classList.add("btn-danger");
      event.target.value = "Delete";
      event.target.classList.remove("btn-primary");
      let typeMenu = event.target.previousElementSibling;
      let attributeBox = typeMenu.previousElementSibling;
      typeMenu.classList.remove("pe-none");
      typeMenu.classList.remove("alert-danger");
      attributeBox.classList.remove("pe-none");
      attributeBox.classList.remove("alert-danger");
      this.deletedAttributes.delete(
        parseInt(event.target.previousElementSibling.previousElementSibling.id)
      );
    },

    async loadAttributeTypes() {
      // Loads the attribute types
      this.attribute_types = await getAttributeTypes();
    },
  },
};
</script>

<style>
#container {
  max-width: 20rem;
  width: 20rem;
  min-width: 15rem;
}

#current-asset-type,
.createAssetType {
  width: 30rem;
}
.fake-success:hover {
  background-color: #26a888 !important;
  border-color: #1aa381 !important;
}
</style>
