<template>
  
  <footer class="bg-slate-800 text-white py-12">
    <div class="max-w-6xl mx-auto px-8">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
        <div class="flex flex-col gap-4">
          <a href="/" class="w-20 h-20 mx-auto mb-4 rounded-2xl overflow-hidden shadow-lg block">
            <img src="../assets/logo.png" alt="CleanSight Logo" class="w-full h-full object-cover" />
          </a>
        </div>
        <div class="space-y-4">
          <h4 class="text-green-400 font-semibold mb-4">Projet</h4>
          <a 
            href="#" 
            @click="scrollToSection('features')"
            class="block text-gray-300 hover:text-green-400 transition-colors duration-300 cursor-pointer mb-2"
          >
            Fonctionnalités
          </a>
          <a 
            href="#" 
            @click="scrollToSection('dashboard')"
            class="block text-gray-300 hover:text-green-400 transition-colors duration-300 cursor-pointer mb-2"
          >
            Dashboard
          </a>
          <a 
            href="#" 
            @click="scrollToSection('impact')"
            class="block text-gray-300 hover:text-green-400 transition-colors duration-300 cursor-pointer mb-2"
          >
            Impact
          </a>
        </div>
        <div class="space-y-4">
          <h4 class="text-green-400 font-semibold mb-4">À propos</h4>
            <div class="block text-gray-300 mb-2">
            Efrei Paris
            </div>
            <div class="block text-gray-300 mb-2">
            Master Camp Data 2025
            </div>
            <div class="block text-gray-300 mb-2">
            GreenAI Collective
            </div>
        </div>
      </div>
      <div class="border-t border-gray-600 pt-4 text-center">
        <p class="text-gray-400">&copy; 2025 CleanSight - Wild Dump Prevention Project - GreenAI Collective</p>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: "Footer",
  setup() {
    const scrollToSection = (sectionId) => {
      if (router.currentRoute.value.path === "/") {
        // Si on est déjà sur la home page, on peut scroller directement
        const element = document.getElementById(sectionId);
        if (element) {
          element.scrollIntoView({ behavior: "smooth" });
        }
      } else {
        // Sinon, on redirige vers la page d'accueil avec un hash
        router.push({ path: "/", hash: `#${sectionId}` });
      }
    };

    return {
      scrollToSection,
    };
  },
};
</script>