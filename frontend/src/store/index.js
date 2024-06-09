import { createStore } from "vuex";
import router from "@/router";
import createPersistedState from "vuex-persistedstate";

export default createStore({
  strict: true,
  state: {
    id: -1,
    email: "",
    role: "",
    name: {
      first: "",
      last: "",
    },
    securityLevel: 0,
    isAuthenticated: false,
    routes: [],
  },

  mutations: {
    setUserData(state, payload) {
      // Stores data of the current user
      state.id = payload.id;
      state.email = payload.email;
      state.role = payload.role;
      state.securityLevel = payload.level;
      state.name.first = payload.fname;
      state.name.last = payload.lname;
      localStorage.token = payload.token;
    },

    login(state) {
      // Allow user to access routes
      state.isAuthenticated = true;
    },

    logout(state) {
      // Reset user's details and access
      state.isAuthenticated = false;
      state.email = "";
      state.role = "";
      state.securityLevel = 0;
    },

    loadRoutes(state, payload) {
      // Stores all routes the user can access
      state.routes = payload;
    },

    updateName(state, payload) {
      // Stores the name of the user, so it can be changed when updated
      state.name.first = payload.firstName;
      state.name.last = payload.lastName;
    }
  },

  actions: {
    login(context, userData) {
      // Sets the user's data after they initially login
      context.commit("setUserData", userData);
      context.commit("login");
    },

    logout(context) {
      // Removes the user's token and logs them out
      context.commit("logout");
      let token = localStorage.getItem("token");
      if (token) {
        localStorage.removeItem("token");
      }
      router.push("/login");
    },

    loadRoutes(context, data) {
      // Loads all routes the user can access based on their role
      let routes = data.filter(
        (route) => route.meta.securityLevel <= context.state.securityLevel && route.name != "Login"
      );
      context.commit("loadRoutes", routes);
    },
  },

  getters: {
    isAuthenticated(state) {
      return state.isAuthenticated;
    },

    securityLevel(state) {
      return state.securityLevel;
    },

    currentUser(state) {
      return { 
        id: state.id,
        email: state.email,
        firstName: state.name.first,
        lastName: state.name.last,
      };
    },

    routes(state) {
      return state.routes;
    }
  },

  plugins: [createPersistedState()],
});
