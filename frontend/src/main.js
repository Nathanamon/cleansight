import { createApp } from "vue";
import { createPinia } from "pinia";
import "./style.css";
import App from "./App.vue";

// ✅ Ajoute l'import du router
import router from "./router";

const app = createApp(App);
app.use(createPinia());
app.use(router);
app.mount("#app");

// ✅ Import du CSS pour Leaflet
import "leaflet/dist/leaflet.css";

