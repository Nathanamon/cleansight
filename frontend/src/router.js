import { createRouter, createWebHistory } from "vue-router";
const routes = [
  {
    path: "/",
    name: "Home",
    component: () => import("./pages/HomePage.vue"),
  },
  {
    path: "/signup",
    name: "Signup",
    component: () => import("./pages/SignupPage.vue"),
  },
  {
    path: "/terms",
    name: "Terms",
    component: () => import("./pages/TermsPage.vue"),
  },
  {
    path: "/privacy",
    name: "Privacy",
    component: () => import("./pages/PrivacyPage.vue"),
  },
  {
    path: "/login",
    name: "Login",
    component: () => import("./pages/LoginPage.vue"),
  },
  {
    path: "/forgot-password",
    name: "ForgotPassword",
    component: () => import("./pages/ForgotPassword.vue"),
  },
  {
    path: "/upload",
    name: "Upload",
    component: () => import("./pages/UploadPage.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
