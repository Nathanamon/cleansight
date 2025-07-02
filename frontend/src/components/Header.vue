<template>
  <nav class="fixed top-0 w-full bg-white/95 backdrop-blur-sm z-50 py-4 border-b border-black/10">
    <div class="max-w-6xl mx-auto flex justify-between items-center px-8">
      <div class="flex items-center gap-4">
        <router-link to="/" class="flex items-center justify-center gap-4">
          <div class="w-20 h-20 rounded-2xl overflow-hidden shadow-lg">
            <img src="../assets/logo.png" alt="CleanSight Logo" class="w-full h-full object-cover" />
          </div>
          <span class="text-3xl font-bold text-green-600 drop-shadow-sm">
            CleanSight
          </span>
        </router-link>
      </div>
      <div class="flex items-center gap-8">
        <span 
          class="text-gray-600 cursor-pointer transition-colors duration-300 font-medium py-2 hover:text-green-600"
          @click="scrollToSection('features')"
        >
          Fonctionnalités
        </span>
        <span 
          class="text-gray-600 cursor-pointer transition-colors duration-300 font-medium py-2 hover:text-green-600"
          @click="scrollToSection('dashboard')"
        >
          Dashboard
        </span>
        <span 
          class="text-gray-600 cursor-pointer transition-colors duration-300 font-medium py-2 hover:text-green-600"
          @click="scrollToSection('impact')"
        >
          Impact
        </span>
        <button 
          class="bg-gradient-to-r from-green-600 to-green-400 text-white border-none py-3 px-6 rounded-full cursor-pointer font-semibold transition-transform duration-300 text-sm mr-4 hover:-translate-y-1 hover:shadow-lg hover:shadow-green-600/30"
          @click="navigateToUpload"
        >
          Analyser Image
        </button>
        <button 
          class="bg-transparent text-green-600 border-2 border-green-600 py-3 px-6 rounded-full cursor-pointer font-semibold transition-all duration-300 text-sm hover:bg-green-600 hover:text-white hover:-translate-y-1"
          @click="navigateToCarte"
        >
          Localisation 
        </button>
        <button 
          class="bg-transparent text-green-600 border-2 border-green-600 py-3 px-6 rounded-full cursor-pointer font-semibold transition-all duration-300 text-sm hover:bg-green-600 hover:text-white hover:-translate-y-1"
          @click="navigateToDashboard"
        >
          Connexion
        </button>
      </div>
    </div>
  </nav>
</template>

<script>
import { useRouter } from "vue-router";

export default {
  name: "Header",
  setup() {
    const router = useRouter();

    const scrollToSection = (sectionId) => {
      if (router.currentRoute.value.path === "/") {
        const element = document.getElementById(sectionId);
        if (element) {
          element.scrollIntoView({ behavior: "smooth" });
        }
      } else {
        router.push({ path: "/", hash: `#${sectionId}` });
      }
    };

    const navigateToUpload = () => {
      router.push("/upload");
    };

    const navigateToDashboard = () => {
      router.push("/login");
    };

    const navigateToCarte = () => {
      router.push("/carte");
    }; // 👈 ICI il manquait cette accolade fermante

    return {
      scrollToSection,
      navigateToUpload,
      navigateToDashboard,
      navigateToCarte,
    };
  },
};
</script>
