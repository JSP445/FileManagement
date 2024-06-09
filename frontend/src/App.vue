<template>
  <!-- This main component displays all things used throughout the entire application -->
  <div id="nav">
    <div
      v-if="isAuthenticated"
      class="navigation | d-flex justify-content-between align-items-center w-100 mb-4 p-3 border-bottom border-1 bg-white px-4"
    >
      <!-- Displays the navigation bar for all accessible routes -->
      <div class="navbar navbar-expand-lg navbar-light justify-content-center">
        <router-link class="nav-link" :to="route.path" v-for="route in routes" :key="route.name"
          >{{ route.name }}
        </router-link>
      </div>

      <!-- Displays log out button -->
      <div class="d-flex align-items-center gap-3">
        <p class="m-0 text-end">
          Currently logged in as: <span>{{ currentUser.email }}</span>
        </p>
        <button type="button" class="btn btn-danger px-4 | logoutBtn" @click="logout">
          Log Out
        </button>
      </div>
    </div>
    <router-view class="" />
  </div>
</template>

<script>
import { successToast } from "@/utils";

export default {
  computed: {
    isAuthenticated() {
      return this.$store.getters.isAuthenticated;
    },
    currentUser() {
      return this.$store.getters.currentUser;
    },
    routes() {
      return this.$store.getters.routes;
    },
  },

  methods: {
    logout() {
      // Logs the user out of the app
      this.$store.dispatch("logout");
      successToast("Logout Successful.");
    },

    setDropdownId(name) {
      if (name === "Admin") {
        return "navbarDropdown";
      }
    },
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

@media screen and (max-width: 63rem) {
  .navigation {
    flex-direction: column-reverse;
  }
}
.logoutBtn {
  white-space: nowrap;
}
</style>
