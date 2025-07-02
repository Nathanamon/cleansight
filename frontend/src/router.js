import { createRouter, createWebHistory } from "vue-router";
const routes = [
  {
    path: "/",
    name: "Home",
    component: () => import("./pages/HomePage.vue"),
  },
  {
    path: "/login",
    name: "Login",
    component: () => import("./pages/LoginPage.vue"),
  },
  {
    path: "/upload",
    name: "Upload",
    component: () => import("./pages/UploadPage.vue"),
  },
  {
    path: "/dashboard",
    name: "Dashboard",
    component: () => import("./pages/Dashboard.vue"),
  },
  {
    path: "/images",
    name: "Images",
    component: () => import("./pages/Images.vue"),
  },
  {
    path: "/recommendations",
    name: "Recommendations",
    component: () => import("./pages/Recommendations.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
