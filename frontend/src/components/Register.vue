<template>
  <!-- This component allows the user to register new details -->
  <div class="register">
    <h1 class="text-center"><strong>Create New User</strong></h1>
    <form @submit.prevent="register">
      <div class="m-4">
        <label class="form-label">
          <div class="text-muted">Email address</div>
        </label>
        <input type="email" required class="form-control" v-model="emailField" />
      </div>

      <div class="m-4">
        <label class="form-label">
          <div class="text-muted">Password</div>
        </label>
        <input type="password" required class="form-control" v-model="passwordField" />
      </div>

      <div class="m-4">
        <label class="form-label">
          <div class="text-muted">Confirm Password</div>
        </label>
        <input type="password" required class="form-control" v-model="confPasswordField" />
      </div>

      <div class="m-4">
        <label class="form-label">
          <div class="text-muted">Role</div>
        </label>
        <select v-model="roleField" class="form-select">
          <option v-for="role in roles" :key="role.role_id">
            {{ role.name }}
          </option>
        </select>
      </div>

      <div class="mx-4">
        <div class="d-grid">
          <button type="submit" class="btn btn-primary">Create Account</button>
        </div>
      </div>
    </form>
  </div>
</template>

<script>
import { getRoles, register } from "@/api";
import { dangerToast, successToast } from "@/utils";

export default {
  name: "Register",

  emits: [
    // Reloads users in previous page
    "loadUsers",
  ],

  data() {
    return {
      // The details of the user to be added
      emailField: "",
      passwordField: "",
      confPasswordField: "",
      roleField: "Viewer",
      // A list of all roles
      roles: [],
    };
  },

  methods: {
    async register(e) {
      // Registers a new user in the database
      e.preventDefault();

      // Validates password fields
      if (this.passwordField != this.confPasswordField) {
        dangerToast("Passwords must match.");
        return;
      }
      let res;

      try {
        res = await register({
          email: this.emailField,
          password: this.passwordField,
          role_id: this.roles.find((role) => role.name === this.roleField).role_id,
        });
        this.resetFields();

        successToast(res.message);

        // Reloads users in ManageUsers page
        this.$emit("loadUsers");
        this.$router.push("/login");
      } catch (error) {
        dangerToast(error.response.data.message);
      }
    },

    async getRoles() {
      // Loads all roles from the database
      try {
        this.roles = await getRoles();
      } catch (error) {
        console.log(error);
      }
    },

    resetFields() {
      // Resets all fields when a user is created
      this.emailField = "";
      this.passwordField = "";
      this.confPasswordField = "";
      this.roleField = "Viewer";
    },
  },

  mounted() {
    this.getRoles();
  },
};
</script>
