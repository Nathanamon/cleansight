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
    path: "/carte",
    name: "Carte",
    component: () => import("./pages/CartePoubelles.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
