import { createApp } from "vue";
import { createPinia } from "pinia";
import { useAuthStore } from "@/stores/auth";

import "./style.css";
import App from "./App.vue";

// ✅ Ajoute l'import du router
import router from "./router";



const app = createApp(App);
const pinia = createPinia();
app.use(pinia);

const auth = useAuthStore(pinia);

// Redirect to homepage whenever the user state becomes unauthenticated
auth.$subscribe((_mutation, state) => {
  if (!state.user && router.currentRoute.value.path !== '/') {
    router.push('/');
  }
});

// Listen for global auth change events
window.addEventListener('auth-changed', (e) => {
  if (e?.detail?.authenticated && e.detail.user) {
    auth.user = e.detail.user;
    localStorage.setItem('userData', JSON.stringify(e.detail.user));
    localStorage.setItem('authToken', 'true');
  } else if (!e?.detail?.authenticated) {
    auth.logout();
    router.push('/');
  } else {
    auth.restoreFromLocalStorage();
  }
});

router.beforeEach((to, from, next) => {
  // Restore auth state on navigation
  if (auth.restoreFromLocalStorage) auth.restoreFromLocalStorage();

  const protectedPaths = ["/dashboard", "/images", "/recommendations", "/rules"];
  if (protectedPaths.includes(to.path) && !auth.user) {
    next("/");
  } else {
    next();
  }
});



app.use(router);
app.mount("#app");

// ✅ Import du CSS pour Leaflet
import "leaflet/dist/leaflet.css";

