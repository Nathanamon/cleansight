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
        <!-- Navigation links (shown for both states) -->
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

        <!-- Actions based on authentication state -->
        <div v-if="!isAuthenticated" class="flex items-center gap-4">
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

        <!-- Authenticated user menu -->
        <div v-else class="flex items-center gap-4">
          <button 
            class="bg-gradient-to-r from-green-600 to-green-400 text-white border-none py-3 px-6 rounded-full cursor-pointer font-semibold transition-transform duration-300 text-sm hover:-translate-y-1 hover:shadow-lg hover:shadow-green-600/30"
            @click="navigateToUpload"
          >
            Analyser Image
          </button>
          <button 
            class="bg-blue-600 text-white border-none py-3 px-6 rounded-full cursor-pointer font-semibold transition-all duration-300 text-sm hover:bg-blue-700 hover:-translate-y-1"
            @click="navigateToDashboard"
          >
            Mon Dashboard
          </button>
          
          <!-- User menu dropdown -->
          <div class="relative">
            <button 
              class="flex items-center gap-2 p-2 rounded-full hover:bg-gray-100 transition-colors duration-300"
              @click="toggleUserMenu"
            >
              <div class="w-10 h-10 bg-gradient-to-r from-green-600 to-green-400 rounded-full flex items-center justify-center text-white font-semibold">
                {{ userInitials }}
              </div>
              <svg 
                class="w-4 h-4 text-gray-600 transition-transform duration-300"
                :class="{ 'rotate-180': isUserMenuOpen }"
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </button>

            <!-- Dropdown menu -->
            <div 
              class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 transition-all duration-300 ease-in-out"
              :class="isUserMenuOpen ? 'opacity-100 visible translate-y-0' : 'opacity-0 invisible -translate-y-2'"
            >
              <div class="py-2">
                <div class="px-4 py-2 text-sm text-gray-700 border-b border-gray-100">
                  <div class="font-medium">{{ userName }}</div>
                  <div class="text-gray-500">{{ userEmail }}</div>
                </div>
                <hr class="my-1">
                <button 
                  class="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors duration-200"
                  @click="logout"
                >
                  Déconnexion
                </button>
              </div>
            </div>
          </div>
        </div>
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
          v-if="!isAuthenticated"
          class="bg-transparent text-green-600 border-2 border-green-600 py-2 px-4 rounded-full cursor-pointer font-semibold transition-all duration-300 text-sm hover:bg-green-600 hover:text-white hover:-translate-y-1"
          @click="navigateToDashboard"
        >
          Connexion
        </button>
        <button 
          v-else
          class="bg-blue-600 text-white border-none py-2 px-4 rounded-full cursor-pointer font-semibold transition-all duration-300 text-sm hover:bg-blue-700 hover:-translate-y-1"
          @click="navigateToDashboard"
        >
          Dashboard
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

        <!-- User info for authenticated mobile users -->
        <div v-if="isAuthenticated" class="border-b border-gray-100 pb-3">
          <div class="flex items-center gap-3 py-2">
            <div class="w-10 h-10 bg-gradient-to-r from-green-600 to-green-400 rounded-full flex items-center justify-center text-white font-semibold">
              {{ userInitials }}
            </div>
            <div>
              <div class="font-medium text-gray-800">{{ userName }}</div>
              <div class="text-sm text-gray-500">{{ userEmail }}</div>
            </div>
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
            v-if="!isAuthenticated"
            class="w-full bg-transparent text-green-600 border-2 border-green-600 py-3 px-6 rounded-full cursor-pointer font-semibold transition-all duration-300 text-sm hover:bg-green-600 hover:text-white hover:-translate-y-1"
            @click="navigateToDashboard"
          >
            Connexion
          </button>
          
          <div v-else class="space-y-2">
            <button 
              class="w-full bg-blue-600 text-white border-none py-3 px-6 rounded-full cursor-pointer font-semibold transition-all duration-300 text-sm hover:bg-blue-700 hover:-translate-y-1"
              @click="navigateToDashboard"
            >
              Mon Dashboard
            </button>
            <button 
              class="w-full bg-gray-600 text-white border-none py-3 px-6 rounded-full cursor-pointer font-semibold transition-all duration-300 text-sm hover:bg-gray-700 hover:-translate-y-1"
              @click="navigateToProfile"
            >
              Mon Profil
            </button>
            <button 
              class="w-full bg-red-600 text-white border-none py-3 px-6 rounded-full cursor-pointer font-semibold transition-all duration-300 text-sm hover:bg-red-700 hover:-translate-y-1"
              @click="logout"
            >
              Déconnexion
            </button>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useRouter } from "vue-router";

export default {
  name: "Header",
  setup() {
    const router = useRouter();
    const isMobileMenuOpen = ref(false);
    const isUserMenuOpen = ref(false);
    
    // États d'authentification (à connecter avec votre store/service d'auth)
    const isAuthenticated = ref(false);
    const user = ref({
      name: '',
      email: '',
      firstName: '',
      lastName: ''
    });

    // Computed properties pour l'affichage utilisateur
    const userName = computed(() => {
      return user.value.name || `${user.value.firstName} ${user.value.lastName}`.trim();
    });

    const userEmail = computed(() => {
      return user.value.email;
    });

    const userInitials = computed(() => {
      if (user.value.firstName && user.value.lastName) {
        return `${user.value.firstName.charAt(0)}${user.value.lastName.charAt(0)}`.toUpperCase();
      }
      if (user.value.name) {
        const names = user.value.name.split(' ');
        return names.length > 1 
          ? `${names[0].charAt(0)}${names[names.length - 1].charAt(0)}`.toUpperCase()
          : names[0].charAt(0).toUpperCase();
      }
      return user.value.email ? user.value.email.charAt(0).toUpperCase() : 'U';
    });

    // Méthodes d'authentification (à adapter selon votre système)
    const checkAuthStatus = () => {
      // Exemple : vérifier le token dans localStorage ou appeler votre service d'auth
      const token = localStorage.getItem('authToken');
      const userData = localStorage.getItem('userData');
      
      if (token && userData) {
        isAuthenticated.value = true;
        user.value = JSON.parse(userData);
      }
    };

    const logout = () => {
      // Nettoyer l'authentification
      isAuthenticated.value = false;
      user.value = { name: '', email: '', firstName: '', lastName: '' };
      localStorage.removeItem('authToken');
      localStorage.removeItem('userData');
      window.dispatchEvent(new CustomEvent('auth-changed', { detail: { authenticated: false } }));
      
      // Fermer les menus
      isMobileMenuOpen.value = false;
      isUserMenuOpen.value = false;
      
      // Rediriger vers la page d'accueil
      router.push('/');
    };

    // Méthodes de navigation existantes
    const scrollToSection = (sectionId) => {
      isMobileMenuOpen.value = false;
      isUserMenuOpen.value = false;
      
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
      isUserMenuOpen.value = false;
      router.push("/upload");
    };

    const navigateToDashboard = () => {
      isMobileMenuOpen.value = false;
      isUserMenuOpen.value = false;
      router.push(isAuthenticated.value ? "/dashboard" : "/login");
    };

    const navigateToProfile = () => {
      isMobileMenuOpen.value = false;
      isUserMenuOpen.value = false;
      router.push("/profile");
    };

    const navigateToSettings = () => {
      isMobileMenuOpen.value = false;
      isUserMenuOpen.value = false;
      router.push("/settings");
    };

    const toggleMobileMenu = () => {
      isMobileMenuOpen.value = !isMobileMenuOpen.value;
      if (isMobileMenuOpen.value) {
        isUserMenuOpen.value = false;
      }
    };

    const toggleUserMenu = () => {
      isUserMenuOpen.value = !isUserMenuOpen.value;
    };

    // Fermer les menus quand on clique ailleurs
    const handleClickOutside = (event) => {
      if (!event.target.closest('.relative')) {
        isUserMenuOpen.value = false;
      }
    };
    
    const handleAuthChanged = (e) => {
      setAuthenticationState(e.detail.authenticated, e.detail.user);
    };

    onMounted(() => {
      checkAuthStatus();
      document.addEventListener('click', handleClickOutside);
      window.addEventListener('auth-changed', handleAuthChanged);
    });

    onUnmounted(() => {
      document.removeEventListener('click', handleClickOutside);
      window.removeEventListener('auth-changed', handleAuthChanged);
    });

    // Méthode publique pour mettre à jour l'état d'authentification
    const setAuthenticationState = (authenticated, userData = null) => {
      isAuthenticated.value = authenticated;
      if (userData) {
        user.value = userData;
      }
    };

    return {
      isMobileMenuOpen,
      isUserMenuOpen,
      isAuthenticated,
      user,
      userName,
      userEmail,
      userInitials,
      scrollToSection,
      navigateToUpload,
      navigateToDashboard,
      navigateToProfile,
      navigateToSettings,
      toggleMobileMenu,
      toggleUserMenu,
      logout,
      setAuthenticationState,
      checkAuthStatus
    };
  },
};
</script>

<style scoped>
/* Ajout d'une transition pour le dropdown */
.relative .absolute {
  z-index: 1000;
}
</style>