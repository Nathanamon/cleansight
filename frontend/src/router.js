import { createRouter, createWebHistory } from "vue-router";
const routes = [
  {
    path: "/",
    name: "Home",
    component: () => import("./components/Home.vue"),
  },
  {
    path: "/connexion",
    name: "Login",
    component: () => import("./components/Login.vue"),
  },
  {
    path: "/upload",
    name: "Upload",
    component: () => import("./components/UploadPage.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
