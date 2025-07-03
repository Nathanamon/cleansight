<template>
  <nav class="fixed top-0 w-full bg-white/95 backdrop-blur-sm z-50 py-4 border-b border-black/10">
    <div class="max-w-6xl mx-auto flex justify-between items-center px-4 sm:px-8">
      <!-- Logo -->
      <div class="flex items-center gap-2 sm:gap-4">
        <router-link to="/" class="flex items-center justify-center gap-2 sm:gap-4">
          <div class="w-12 h-12 sm:w-16 sm:h-16 lg:w-20 lg:h-20 rounded-2xl overflow-hidden shadow-lg">
            <img src="../assets/logo.png" alt="CleanSight Logo" class="w-full h-full object-cover" />
          </div>
          <span class="text-xl sm:text-2xl lg:text-3xl font-bold text-green-600 drop-shadow-sm">
            CleanSight
          </span>
        </router-link>
      </div>

      <!-- Desktop Navigation -->
      <div class="hidden lg:flex items-center gap-8">
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
          @click="navigateToDashboard"
        >
          Connexion
        </button>
      </div>

      <!-- Mobile Navigation Buttons (visible on medium screens) -->
      <div class="hidden md:flex lg:hidden items-center gap-3">
        <button 
          class="bg-gradient-to-r from-green-600 to-green-400 text-white border-none py-2 px-4 rounded-full cursor-pointer font-semibold transition-transform duration-300 text-sm hover:-translate-y-1 hover:shadow-lg hover:shadow-green-600/30"
          @click="navigateToUpload"
        >
          Analyser
        </button>
        <button 
          class="bg-transparent text-green-600 border-2 border-green-600 py-2 px-4 rounded-full cursor-pointer font-semibold transition-all duration-300 text-sm hover:bg-green-600 hover:text-white hover:-translate-y-1"
          @click="navigateToDashboard"
        >
          Connexion
        </button>
      </div>

      <!-- Mobile Menu Button -->
      <button 
        class="md:hidden p-2 rounded-lg hover:bg-gray-100 transition-colors duration-300"
        @click="toggleMobileMenu"
      >
        <svg 
          class="w-6 h-6 text-gray-600" 
          fill="none" 
          stroke="currentColor" 
          viewBox="0 0 24 24"
        >
          <path 
            v-if="!isMobileMenuOpen"
            stroke-linecap="round" 
            stroke-linejoin="round" 
            stroke-width="2" 
            d="M4 6h16M4 12h16M4 18h16"
          />
          <path 
            v-else
            stroke-linecap="round" 
            stroke-linejoin="round" 
            stroke-width="2" 
            d="M6 18L18 6M6 6l12 12"
          />
        </svg>
      </button>
    </div>

    <!-- Mobile Menu -->
    <div 
      class="md:hidden bg-white/95 backdrop-blur-sm border-t border-black/10 transition-all duration-300 ease-in-out"
      :class="isMobileMenuOpen ? 'max-h-96 opacity-100' : 'max-h-0 opacity-0 overflow-hidden'"
    >
      <div class="px-4 py-4 space-y-4">
        <!-- Navigation Links -->
        <div class="space-y-3">
          <div 
            class="text-gray-600 cursor-pointer transition-colors duration-300 font-medium py-2 hover:text-green-600 border-b border-gray-100 pb-2"
            @click="scrollToSection('features')"
          >
            Fonctionnalités
          </div>
          <div 
            class="text-gray-600 cursor-pointer transition-colors duration-300 font-medium py-2 hover:text-green-600 border-b border-gray-100 pb-2"
            @click="scrollToSection('dashboard')"
          >
            Dashboard
          </div>
          <div 
            class="text-gray-600 cursor-pointer transition-colors duration-300 font-medium py-2 hover:text-green-600 border-b border-gray-100 pb-2"
            @click="scrollToSection('impact')"
          >
            Impact
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="space-y-3 pt-4">
          <button 
            class="w-full bg-gradient-to-r from-green-600 to-green-400 text-white border-none py-3 px-6 rounded-full cursor-pointer font-semibold transition-transform duration-300 text-sm hover:-translate-y-1 hover:shadow-lg hover:shadow-green-600/30"
            @click="navigateToUpload"
          >
            Analyser Image
          </button>
          <button 
            class="w-full bg-transparent text-green-600 border-2 border-green-600 py-3 px-6 rounded-full cursor-pointer font-semibold transition-all duration-300 text-sm hover:bg-green-600 hover:text-white hover:-translate-y-1"
            @click="navigateToDashboard"
          >
            Connexion
          </button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from "vue-router";

export default {
  name: "Header",
  setup() {
    const router = useRouter();
    const isMobileMenuOpen = ref(false);

    const scrollToSection = (sectionId) => {
      // Fermer le menu mobile après clic
      isMobileMenuOpen.value = false;
      
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
      isMobileMenuOpen.value = false;
      router.push("/upload");
    };

    const navigateToDashboard = () => {
      isMobileMenuOpen.value = false;
      router.push("/login");
    };

    const navigateToCarte = () => {
      isMobileMenuOpen.value = false;
      router.push("/carte");
    };

    const toggleMobileMenu = () => {
      isMobileMenuOpen.value = !isMobileMenuOpen.value;
    };

    return {
      isMobileMenuOpen,
      scrollToSection,
      navigateToUpload,
      navigateToDashboard,
      navigateToCarte,
      toggleMobileMenu,
    };
  },
};
</script>