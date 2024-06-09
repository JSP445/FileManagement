<template>
  <!-- This component displays all assets associated with the asset -->
  <form @submit.prevent="">
    <div class="modal-container">
      <div class="modal-header">
        <h3>Associated Assets</h3>
      </div>

      <div class="modal-body" style="height: 50vh; overflow-y: scroll; overflow-x: hidden">
        <div class="card mb-1" v-for="asset in associatedAssets" :key="asset.asset_name">
          <div class="card-header py-1">
            <a href="#" @click="switchModal(asset.asset_id)">{{ asset.asset_name }}</a>
          </div>
          <div class="card-body py-1">Asset Type: {{ asset.asset_type.asset_type_name }}</div>
          <div class="card-footer pt-1">
            tags:
            <vue-horizontal responsive style="margin: auto">
              <div v-for="tag in asset.tags" :key="tag.text">
                <p class="list-group-item">{{ tag.tag_name }}</p>
              </div>
            </vue-horizontal>
          </div>
        </div>
      </div>

      <div class="modal-footer">
        <slot>
          <button type="button" class="btn btn-danger px-5" @click="$emit('associated')">
            Close
          </button>
        </slot>
      </div>
    </div>
  </form>
</template>

<script>
import VueHorizontal from "vue-horizontal";
export default {
  name: "AssociatedAssets",
  props: [
    // List of all associated assets
    "associatedAssets",
  ],
  emits: [
    // Opens the pop-up
    "openModal",
    // Determines associated assets view
    "associated",
  ],

  components: {
    VueHorizontal,
  },

  methods: {
    switchModal(id) {
      // Switches to viewing the selected associated asset
      this.$emit("openModal", id);
    },
  },
};
</script>
