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
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
