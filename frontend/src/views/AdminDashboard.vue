<template>
  <!-- This page displays components locked to administrators -->
  <div class="mb-3">
    <div class="d-flex gap-5 justify-content-center bg-white p-3 border | adminBtns">
      <div
        class="underline adminBtnContainer | w-100"
        :class="{ 'underline-success': selectedPage == 'Asset Types' }"
      >
        <input
          @click="handlePageSelection"
          type="button"
          class="btn adminBtn w-100 py-3 text-black"
          style="box-shadow: none"
          value="Asset Types"
        />
      </div>

      <div
        class="underline adminBtnContainer | w-100"
        :class="{ 'underline-success': selectedPage == 'Users' }"
      >
        <input
          @click="handlePageSelection"
          type="button"
          class="btn adminBtn w-100 py-3 text-black"
          style="box-shadow: none"
          value="Users"
        />
      </div>
      <div
        class="underline adminBtnContainer | w-100"
        :class="{ 'underline-success': selectedPage == 'Audit Log' }"
      >
        <input
          @click="handlePageSelection"
          type="button"
          class="btn w-100 adminBtn w-100 py-3 text-black"
          style="box-shadow: none"
          value="Audit Log"
        />
      </div>
    </div>

    <div v-if="selectedPage == 'Asset Types'">
      <ViewAssetTypes />
    </div>

    <div v-if="selectedPage == 'Users'">
      <ManageUsers />
    </div>

    <div v-if="selectedPage == 'Audit Log'">
      <AuditLog />
    </div>
  </div>
</template>

<script>
import ViewAssetTypes from "@/components/ViewAssetTypes.vue";
import ManageUsers from "@/components/ManageUsers.vue";
import ProjectView from "@/components/ManageProjects.vue";
import AuditLog from "@/components/AuditLog.vue";

export default {
  name: "AdminDashboard",
  components: {
    ViewAssetTypes,
    ManageUsers,
    ProjectView,
    AuditLog,
  },

  data() {
    return {
      // The sub-page being viewed
      selectedPage: null,
    };
  },

  methods: {
    handlePageSelection(event) {
      // Load the component that was clicked
      this.selectedPage = event.target.value;
    },
  },
};
</script>

<style>
.adminBtn,
.adminBtnContainer {
  max-width: 25rem;
}
@media screen and (max-width: 30rem) {
  .adminBtns {
    flex-wrap: wrap;
  }
}
</style>
