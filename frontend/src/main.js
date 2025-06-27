import { createApp } from "vue";
import "./style.css";
import App from "./App.vue";

// ✅ Ajoute l'import du router
import router from "./router";

// ✅ Monte l'app avec le router
createApp(App).use(router).mount("#app");
