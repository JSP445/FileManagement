<template>
  <!-- This component displays all the logs of operations happened on the system -->
  <div>
    <div class="d-flex gap-3 justify-content-center my-4">
      <input
        @click="handlePageSelection"
        type="button"
        class="btn btn-info w-100 logBtn"
        value="Asset Types Log"
        :class="{ 'btn-success': selectedPage == 'Asset Types Log' }"
      />

      <input
        @click="handlePageSelection"
        type="button"
        class="btn btn-info w-100 logBtn"
        value="Assets Log"
        :class="{ 'btn-success': selectedPage == 'Assets Log' }"
      />

      <input
        @click="handlePageSelection"
        type="button"
        class="btn btn-info w-100 logBtn"
        value="Users Log"
        :class="{ 'btn-success': selectedPage == 'Users Log' }"
      />

      <input
        @click="handlePageSelection"
        type="button"
        class="btn btn-info w-100 logBtn"
        value="Projects Log"
        :class="{ 'btn-success': selectedPage == 'Projects Log' }"
      />
    </div>
    <div class="d-flex justify-content-center gap-5 mt-5 overflow-auto" style="height: 72.5vh">
      <div v-if="selectedPage == 'Asset Types Log'">
        <div v-for="log in logs" :key="log.id" class="card logCard my-3">
          <div class="card-body">
            <h4 class="card-title">{{ log.asset_type_name }} | {{ log.operation }}</h4>
            <h5 class="card-subtitle">{{ log.email }} | {{ formatDate(log.time) }}</h5>
            <p class="card-text">{{ log.description }}</p>
          </div>
        </div>
      </div>

      <div v-if="selectedPage == 'Assets Log'">
        <div v-for="log in logs" :key="log.id" class="card logCard my-3">
          <div class="card-body">
            <h4 class="card-title">{{ log.asset_name }} | {{ log.operation }}</h4>
            <h5 class="card-subtitle">{{ log.email }} | {{ formatDate(log.time) }}</h5>
            <p class="card-text">{{ log.description }}</p>
          </div>
        </div>
      </div>

      <div v-if="selectedPage == 'Users Log'">
        <div v-for="log in logs" :key="log.id" class="card logCard my-3">
          <div class="card-body">
            <h4 class="card-title">{{ log.subject }} | {{ log.operation }}</h4>
            <h5 class="card-subtitle">
              {{ log.subject_role }} <br />
              {{ log.admin }} | {{ formatDate(log.time) }}
            </h5>
          </div>
        </div>
      </div>

      <div v-if="selectedPage == 'Projects Log'">
        <div v-for="log in logs" :key="log.id" class="card logCard my-3">
          <div class="card-body">
            <h4 class="card-title">{{ log.project_name }} | {{ log.operation }}</h4>
            <h5 class="card-subtitle">{{ log.email }} | {{ formatDate(log.time) }}</h5>
            <p class="card-text">{{ log.description }}</p>
          </div>
        </div>
      </div>
      <p v-show="selectedPage && logs.length == 0">No {{ selectedPage }}s found</p>
    </div>
  </div>
</template>

<script>
import { assetTypeLogs, userLogs, assetLogs, projectLogs } from "@/api";
import { formatDate } from "@/utils";

export default {
  data() {
    return {
      // Defines the currently selected page
      selectedPage: null,
      // A list of the logs for the selected page
      logs: [],
    };
  },

  setup() {
    return {
      formatDate,
    };
  },

  methods: {
    async handlePageSelection(event) {
      // Loads the selected audit logs from the database
      try {
        switch (event.target.value) {
          case "Asset Types Log":
            this.logs = await assetTypeLogs();
            break;
          case "Assets Log":
            this.logs = await assetLogs();
            break;
          case "Users Log":
            this.logs = await userLogs();
            break;
          case "Projects Log":
            this.logs = await projectLogs();
            break;
        }
        this.selectedPage = event.target.value;
      } catch (error) {
        console.log(error);
      }
    },
  },
};
</script>

<style scoped>
.logBtn {
  color: white;
  max-width: 20rem;
}

.logCard {
  width: 40rem;
}
</style>
