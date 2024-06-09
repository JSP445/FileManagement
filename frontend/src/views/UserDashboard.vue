<template>
  <!-- This page allows any user to edit their name and password -->
  <div class="mb-3">
    <div class="d-flex justify-content-center gap-5" v-if="selectedPage == 'Dashboard'">
      <div>
        <div class="text-center my-5">
          <p>Email: {{ email }}</p>
          <p>Name: {{ firstName }} {{ lastName }}</p>
        </div>
        <div class="d-flex gap-3 justify-content-center">
          <button @click="selectPage" value="Change Name" type="button" class="btn btn-primary">
            Change Name
          </button>

          <button @click="selectPage" value="Change Password" type="button" class="btn btn-primary">
            Change Password
          </button>
        </div>
      </div>
      <div>
        <h1>Recent Activity</h1>
        <div v-for="log in logs" :key="log.id" class="card logCard my-2 vw-50">
          <div class="card-body">
            <h4 class="card-title">{{ log.name }} | {{ log.operation }}</h4>
            <h5 class="card-subtitle">{{ formatDate(log.time) }}</h5>
            <p class="card-text">{{ log.description }}</p>
          </div>
        </div>
      </div>
    </div>

    <div v-if="selectedPage == 'Change Name'" class="text-center">
      <form @submit.prevent="updateName">
        <p>Current name: {{ firstName }} {{ lastName }}</p>
        <div>
          <label for="changeFirstName" class="form">Change first name</label>
          <br />
          <input type="text" class="w-30" v-model="user.firstName" required />
        </div>
        <br />

        <div>
          <label for="changeLastName" class="form">Change last name</label>
          <br />
          <input type="text" class="w-30" v-model="user.lastName" required />
        </div>
        <br />
        <div class="d-flex gap-3 justify-content-center">
          <button type="button" class="btn btn-danger" @click="backPage">Cancel</button>
          <button type="submit" class="btn btn-primary">Submit</button>
        </div>
      </form>
    </div>

    <div v-if="selectedPage == 'Change Password'" class="text-center">
      <form @submit.prevent="changePassword">
        <div>
          <label for="currentPassword" class="form">Current Password:</label>
          <br />
          <input type="password" class="w-30" v-model="password.current" required />
        </div>
        <br />

        <div>
          <label for="newPassword" class="form">New Password:</label>
          <br />
          <input type="password" class="w-30" v-model="password.new" required />
        </div>
        <br />

        <div>
          <label for="confirmPassword" class="form">Confirm Password:</label>
          <br />
          <input type="password" class="w-30" v-model="password.confirm" required />
        </div>
        <br />

        <div class="d-flex gap-3 justify-content-center">
          <button type="button" class="btn btn-danger" @click="backPage">Cancel</button>
          <button type="submit" class="btn btn-primary">Submit</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { updatePassword, updateUserDetails, getMyLogs } from "@/api";
import { dangerToast, formatDate, successToast } from "@/utils";

export default {
  setup() {
    return {
      formatDate,
    };
  },
  data() {
    return {
      logs: [],
      // The name form data entered by the user
      user: {
        firstName: this.$store.getters.currentUser.firstName,
        lastName: this.$store.getters.currentUser.lastName,
      },
      // The name form data entered by the user
      password: {
        current: "",
        new: "",
        confirm: "",
      },
      // The page currently being viewed
      selectedPage: "Dashboard",
    };
  },

  computed: {
    firstName() {
      return this.$store.getters.currentUser.firstName;
    },
    lastName() {
      return this.$store.getters.currentUser.lastName;
    },
    email() {
      return this.$store.getters.currentUser.email;
    },
  },

  methods: {
    selectPage(event) {
      // Load the component that was clicked
      this.selectedPage = event.target.value;
    },

    backPage() {
      // Returns to the dashboard and resets all input fields
      this.selectedPage = "Dashboard";
      this.user.firstName = this.$store.getters.currentUser.firstName;
      this.user.lastName = this.$store.getters.currentUser.lastName;

      this.password = {
        current: "",
        new: "",
        confirm: "",
      };
    },

    async getLogs() {
      this.logs = await getMyLogs({ email: this.email });
      console.log(this.logs);
    },

    async updateName() {
      // Updates the first and last name of the user
      if (!confirm("Are you sure you want to save your changes?")) {
        return;
      }
      try {
        let res = await updateUserDetails({
          first_name: this.user.firstName,
          last_name: this.user.lastName,
        });

        // Updates the users name in the store
        this.$store.commit("updateName", this.user);
        successToast(res.message);

        this.selectedPage = "Dashboard";
      } catch (error) {
        dangerToast(error.response.data.message);
      }
    },

    async changePassword() {
      // Updates the password of the user
      if (!confirm("Are you sure you want to save your changes?")) {
        return;
      }
      try {
        let res = await updatePassword({
          current_password: this.password.current,
          new_password: this.password.new,
          confirm_password: this.password.confirm,
        });
        successToast(res.message);

        this.backPage();
      } catch (error) {
        dangerToast(error.response.data.message);
      }
    },
  },

  async mounted() {
    this.getLogs();
  },
};
</script>
