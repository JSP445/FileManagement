<template>
  <!-- This component displays all users and allows their roles to be edited -->
  <div class="d-flex justify-content-center gap-5 mt-5">
    <div id="container" class="d-flex flex-column">
      <h1 class="body-bg">Manage Users</h1>
      <div class="list-group">
        <a
          @click="selectUser(user)"
          class="text-start list-group-item list-group-item-action text-break"
          v-for="user in users"
          :key="user.email"
          :class="{
            'active text-white': currentUser && user.email == currentUser.email,
          }"
        >
          {{ user.email }}
        </a>

        <button
          @click="toggleCreateMode"
          type="button"
          class="text-center list-group-item list-group-item-action text-break bg-success text-white"
        >
          Add User
        </button>
      </div>
    </div>

    <div class="d-flex flex-column" id="current-user" v-if="currentUser && !createState">
      <div
        class="d-flex gap-3 justify-content-between mb-4"
        v-if="currentUser.email != 'admin@example.com'"
      >
        <button type="button" class="btn btn-primary w-100" v-if="editMode" @click="setViewMode">
          Reset
        </button>
        <button type="button" class="btn btn-success w-100" v-if="editMode" @click="saveChanges">
          Save
        </button>

        <button type="button" class="btn btn-primary w-100" v-if="!editMode" @click="setEditMode">
          Edit
        </button>
        <button type="button" class="btn btn-danger w-100" @click="deleteUser">Delete</button>
      </div>

      <p class="fw-bold">
        {{ currentUser.email }}
      </p>
      <p class="fw-bold mt-3">Role:</p>

      <select
        v-model="currentUserRole"
        class="form-select mb-3"
        :class="{ 'fw-bold': !editMode }"
        :disabled="!editMode"
      >
        <option v-for="role in allRoles" :key="role.role_id">
          {{ role.name }}
        </option>
      </select>
    </div>

    <div v-if="createState" class="createUser">
      <Register @loadUsers="loadUsers" />
    </div>
  </div>
</template>

<script>
import { getUsers, deleteUser, getRoles, changeUserRole } from "@/api";
import { dangerToast, successToast } from "@/utils";
import Register from "@/components/Register.vue";

export default {
  components: {
    Register,
  },

  data() {
    return {
      // The user currently being viewed
      currentUser: null,
      // A list of all users
      users: [],
      // Enables registration features if true
      createState: false,
      // A list of all roles
      allRoles: [],
      // The name of the role of the currently selected user
      currentUserRole: "",
      // Enables role editing if true
      editMode: false,
    };
  },

  methods: {
    selectUser(user) {
      // Gets current user's details
      this.currentUser = user;
      this.createState = false;
      this.currentUserRole = this.allRoles.find((role) => role.role_id === user.role_id).name;
    },

    async loadUsers() {
      // Loads all users from the database
      try {
        this.users = await getUsers();
      } catch (error) {
        console.log(error);
      }
    },

    async deleteUser() {
      // Removes the selected user from the database
      let res;
      if (confirm("Are you sure you want to delete this user?")) {
        try {
          res = await deleteUser(this.currentUser.id);
          successToast(`User "${res.email}" successfully deleted.`);
          this.loadUsers();
          this.currentUser = null;
        } catch (error) {
          dangerToast(error.response.data.message);
        }
      }
    },

    async saveChanges() {
      // Updates the selected user's role
      const role_id = this.allRoles.find((role) => role.name === this.currentUserRole).role_id;

      const user = {
        user_id: this.currentUser.id,
        role_id: role_id,
      };

      try {
        let res;

        res = await changeUserRole(user);
        successToast(res.message);
        this.setViewMode();
      } catch (error) {
        dangerToast(error.response.data.message);
      }
    },

    setEditMode() {
      // Displays editable fields
      this.editMode = true;
    },

    setViewMode() {
      // Stops ability to edit
      this.editMode = false;
    },

    async loadRoles() {
      // Loads all roles from the database
      try {
        this.allRoles = await getRoles();
      } catch (error) {
        console.log(error);
      }
    },

    toggleCreateMode() {
      // Sets state to create a new user
      this.currentUser = null;
      this.createState = true;
    },
  },

  mounted() {
    this.loadUsers();
    this.loadRoles();
  },
};
</script>

<style scoped>
#current-user,
.createUser {
  width: 30rem;
}
</style>
