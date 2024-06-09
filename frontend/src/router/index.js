import { createRouter, createWebHistory } from "vue-router";
import Login from "@/views/Login.vue";
import About from "@/views/About.vue";
import ViewAssets from "@/views/ViewAssets.vue";
import store from "@/store/index.js";
import AdminDashboard from "@/views/AdminDashboard.vue";
import UserDashboard from "@/views/UserDashboard.vue";
import ProjectView from "@/components/ManageProjects.vue";

// All main pages in the application and their accessibility
const routes = [
  {
    path: "/about",
    name: "About",
    component: About,
    meta: {
      loginRequired: true,
      securityLevel: 0,
    },
  },

  {
    path: "/login",
    name: "Login",
    component: Login,
    meta: {
      loginRequired: false,
      securityLevel: 0,
    },
  },

  {
    path: "/assets",
    name: "Assets",
    component: ViewAssets,
    meta: {
      loginRequired: true,
      securityLevel: 25,
    },
  },

  {
    path: "/projects",
    name: "Projects",
    component: ProjectView,
    meta: {
      loginRequired: true,
      securityLevel: 100,
    },
  },

  {
    path: "/admin",
    name: "Admin",
    component: AdminDashboard,
    meta: {
      loginRequired: true,
      securityLevel: 100,
    },
  },

  {
    path: "/user/dashboard",
    name: "Dashboard",
    component: UserDashboard,
    meta: {
      loginRequired: true,
      securityLevel: 25,
    },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  if (to.meta.loginRequired && !store.getters.isAuthenticated) {
    next("/login");
  } else if (store.getters.isAuthenticated && to.name == "Login") {
    // Can't access page while logged in
    next(from.path);
  } else if (store.getters.securityLevel < to.meta.securityLevel) {
    next("/");
  } else {
    next();
  }
});

export default router;
