import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import path from "path"; // ✅ Ajout pour l’alias
import tailwindcss from '@tailwindcss/vite'


// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    tailwindcss(), // ✅ Ajout du plugin Tailwind CSS
  ],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"), // ✅ Déclare @ comme racine de src
    },
  },
});
