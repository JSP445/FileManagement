<template>
  <!-- This component allows for the creation of asset types with their attributes -->
  <div class="d-flex flex-column justify-content-center align-items-center">
    <form @submit.prevent="submitNewType" class="d-flex flex-column w-100 gap-2">
      <div>
        <label class="w-100 text-start">
          Asset Type Name
          <input
            v-model="FormData.asset_type_name"
            id="asset_type_name"
            autocomplete="off"
            type="text"
            class="form-control"
          />
        </label>
      </div>

      <div>
        <label class="w-100 text-start">
          Asset Attribute
          <input
            ref="attributeInput"
            @keyup.enter="addAttribute"
            v-model="assetAttribute"
            id="asset_attribute"
            autocomplete="off"
            type="text"
            class="form-control"
          />
        </label>
      </div>

      <div>
        <select
          required
          v-model="attribute_type"
          class="form-select mt-2"
          aria-label="Default select example"
        >
          <option selected disabled value="Attribute Type">Attribute Type</option>
          <option
            v-for="attribute_type in attribute_types"
            :key="attribute_type.type_id"
            :value="attribute_type"
          >
            {{ attribute_type.type_name }}
          </option>
        </select>
      </div>

      <div>
        <select
          required
          class="form-select mt-2"
          aria-label="Default select example"
          v-model="FormData.parent_asset_type"
        >
          <option selected disabled value="Attribute Type">Parent Asset Types</option>
          <option
            v-for="assetType in allAssetTypes"
            :key="assetType.asset_type_id"
            :value="assetType.asset_type_id"
          >
            {{ assetType.asset_type_name }}
          </option>
        </select>
      </div>

      <input
        @click="addAttribute"
        class="btn btn-primary mt-4"
        value="Add Attribute"
        type="button"
      />
      <input
        @click="removeAttribute"
        class="btn btn-primary"
        value="Remove last Attribute"
        type="button"
      />
      <input type="submit" value="Submit new Type" class="btn btn-success" />
    </form>

    <!-- Contains a list of attributes -->
    <div class="mt-5 w-100">
      <ul class="list-unstyled w-100">
        <h3 class="text-start border-bottom text-center">Attributes</h3>
        <li v-for="attribute in attributeList" :key="attribute.index" class="text-start">
          "{{ attribute.name }}" of type "{{ attribute.type_name }}"
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import { addAssetType, getAttributeTypes } from "@/api";
import { dangerToast, successToast, warningToast } from "@/utils";

export default {
  name: "CreateAssetType",
  components: {},

  data() {
    return {
      // Contains all the attributes currently created
      attributeList: [],
      // Contains the types of the attributes
      attribute_types: [],
      // The default value in the dropdown
      attribute_type: "Attribute Type",
      // An empty attribute
      assetAttribute: "",
      // This contains the data to submit to the server
      FormData: {
        asset_type_name: "",
        attributes: [],
        parent_asset_type: 0,
      },
    };
  },

  props: {
    // A list of asset types to ensure duplicates arent made
    allAssetTypes: Array,
  },

  methods: {
    async loadAttributeTypes() {
      // Loads all attribute types from the database
      this.attribute_types = await getAttributeTypes();
    },

    addAttribute() {
      // Validates and adds a new attribute for the asset type
      if (this.attribute_type == "Attribute Type") {
        warningToast("Please select an attribute type.");
        return;
      }
      // Validates the attribute isnt empty
      if (this.assetAttribute.trim() == "") {
        warningToast("Please enter an asset attribute.");
        return;
      }
      if (!this.attributeList.includes(this.assetAttribute)) {
        this.attributeList.push({
          name: this.assetAttribute,
          type_id: this.attribute_type["type_id"],
          type_name: this.attribute_type["type_name"],
        });
      }
      this.assetAttribute = "";
      // Gives focus back to the input box
      this.$refs.attributeInput.focus();
    },

    removeAttribute() {
      // Removes the last attribute from the asset type
      this.attributeList.pop(this.lastAdded);
      this.$refs.attributeInput.focus();
    },

    async submitNewType() {
      // Creates a new asset type and stores it in the database
      this.FormData.attributes = this.attributeList;
      try {
        await addAssetType(this.FormData);
        this.resetFields();

        successToast("Successfully added new asset type.");
        this.$emit("newAssetTypeCreated", true);
      } catch (error) {
        dangerToast(error.response.data.message);
      }
    },

    resetFields() {
      // Resets input fields once a new asset type is made
      this.attribute_type = "Attribute Type";
      this.attributeList = [];
      this.FormData = {
        asset_type_name: "",
        attributes: [],
        parent_asset_type: 0,
      };
    },
  },

  mounted() {
    this.loadAttributeTypes();
  },
};
</script>
