<template>
  <!--This page authenticates the user and grants access to the application -->
  <div class="login my-5">
    <h1 class="text-center"><strong>Login</strong></h1>
    <form @submit.prevent="login">
      <div class="m-4">
        <label class="form-label">
          <div class="text-muted">Email Address</div>
        </label>
        <input type="email" class="form-control" v-model="emailField" required />
      </div>

      <div class="m-4">
        <label class="form-label">
          <div class="text-muted">Password</div>
        </label>
        <input type="password" class="form-control" v-model="passwordField" required />
      </div>

      <div class="mx-4 d-grid">
        <button type="submit" class="btn btn-primary">Log In</button>
      </div>
    </form>
  </div>
</template>

<script>
import { authenticate } from "@/api";
import { dangerToast, successToast } from "@/utils";

export default {
  name: "Login",

  data() {
    return {
      // The email entered by the user
      emailField: "",
      // The password entered by the user
      passwordField: "",
    };
  },

  methods: {
    async login() {
      // Logs the user into the app
      let res;
      try {
        res = await authenticate({
          email: this.emailField,
          password: this.passwordField,
        });

        successToast(res.message);

        // Sets the user's data to be accessed when using the application
        this.$store.dispatch("login", res);
        // Loads all routes available to the user
        this.$store.dispatch("loadRoutes", this.$router.options.routes);
        // Pushes the user to the initial page
        this.$router.push("/assets");
      } catch (error) {
        dangerToast(error.response.data.message);
      }
    },
  },
};
</script>
