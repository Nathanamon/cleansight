<template>
  <div class="home-page font-sans text-gray-800 leading-relaxed">
    <!-- Hero Section -->
    <section class="relative min-h-screen bg-gradient-to-br from-green-50 to-green-100 flex items-center pt-20 overflow-hidden">
      <div class="max-w-6xl mx-auto px-8 grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
        <div>
          <h1 class="text-6xl font-extrabold leading-tight mb-6 text-slate-800">
            Surveillance Intelligente des
            <span class="text-green-600 relative">Poubelles Urbaines</span>
          </h1>
          <p class="text-xl text-gray-600 mb-10 leading-relaxed">
            Prévenez les dépôts sauvages grâce à l'IA. Notre plateforme détecte
            automatiquement l'état des poubelles pour une gestion optimisée des
            déchets urbains.
          </p>
          <div class="flex gap-4 flex-wrap">
            <button 
              class="flex items-center gap-2 bg-gradient-to-r from-green-600 to-green-400 text-white py-4 px-8 rounded-full text-lg font-semibold cursor-pointer transition-all duration-300 border-none hover:-translate-y-1 hover:shadow-xl hover:shadow-green-600/40"
              @click="navigateToUpload"
            >
              <span class="text-xl">📷</span>
              Analyser une Image
            </button>
            <button
              class="hidden md:flex items-center gap-2 bg-white text-green-600 border-2 border-green-600 py-4 px-8 rounded-full text-lg font-semibold cursor-pointer transition-all duration-300 hover:bg-green-600 hover:text-white hover:-translate-y-1"
              @click="scrollToSection('features')"
            >
              <span class="text-xl">🔍</span>
              Découvrir Plus
            </button>
          </div>
        </div>
        <div class="hidden lg:flex justify-center">
  <div class="bg-white rounded-3xl p-12 shadow-2xl border border-green-200/20 animate-bounce w-full max-w-md">
    <div class="flex items-center gap-3 mb-6 font-bold text-gray-800 text-lg">
      <div class="w-4 h-4 rounded-full bg-red-500 animate-pulse"></div>
      <span>Poubelle Détectée</span>
    </div>
    <div class="space-y-4">
      <div class="bg-gray-50 p-6 rounded-xl text-xl">
        🗑️ État: <strong>Pleine</strong>
      </div>
      <div class="text-gray-600 text-base">📍 Rue de la République</div>
      <div class="text-gray-600 text-base">⏰ Il y a 5 minutes</div>
    </div>
  </div>
</div>
      </div>
      <div class="absolute bottom-0 left-0 w-full h-24 bg-white" 
           style="clip-path: polygon(0 60%, 100% 0%, 100% 100%, 0% 100%);">
      </div>
    </section>

    <!-- Features Section -->
    <section id="features" class="py-32 bg-white">
      <div class="max-w-7xl mx-auto px-4">
        <h2 class="text-center text-5xl font-bold mb-16 text-slate-800">
          Fonctionnalités Clés
        </h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-10">
          <div
            v-for="feature in features"
            :key="feature.id"
            class="bg-white p-10 rounded-3xl text-center shadow-xl border border-green-100/20 transition-all duration-300 cursor-pointer hover:shadow-2xl hover:shadow-green-600/20 hover:-translate-y-2 hover:scale-105"
            @mouseenter="animateCard"
            @mouseleave="resetCard"
          >
            <div class="text-5xl mb-6">
              {{ feature.icon }}
            </div>
            <h3 class="text-2xl font-semibold mb-4 text-gray-800">
              {{ feature.title }}
            </h3>
            <p class="text-gray-600 leading-relaxed">
              {{ feature.description }}
            </p>
          </div>
        </div>
      </div>
    </section>


    <!-- Dashboard Preview Section -->
    <section id="dashboard" class="py-24 bg-gradient-to-br from-green-50 to-green-100">
      <div class="max-w-6xl mx-auto px-8">
        <h2 class="text-center text-5xl font-bold mb-12 text-slate-800">
          Tableau de Bord Interactif
        </h2>
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center max-w-5xl mx-auto">
          <div class="bg-white rounded-2xl shadow-2xl overflow-hidden">
            <div class="bg-gray-50 p-4 flex items-center gap-4 border-b border-gray-200">
              <div class="flex gap-2">
                <div class="w-3 h-3 rounded-full bg-red-500"></div>
                <div class="w-3 h-3 rounded-full bg-yellow-500"></div>
                <div class="w-3 h-3 rounded-full bg-green-500"></div>
              </div>
              <span class="text-gray-600 font-medium">CleanSight Dashboard</span>
            </div>
            <div class="p-8 grid gap-6">
              <div class="bg-gray-50 p-8 rounded-xl text-center border-2 border-dashed border-gray-300">
                <div class="text-3xl mb-2">📊</div>
                <p class="text-gray-600">Graphiques et Statistiques</p>
              </div>
              <div class="bg-gray-50 p-8 rounded-xl text-center border-2 border-dashed border-gray-300">
                <div class="text-3xl mb-2">🗺️</div>
                <p class="text-gray-600">Carte Interactive</p>
              </div>
            </div>
          </div>
          <div>
            <h3 class="text-3xl mb-4 text-gray-800 font-semibold">
              Accédez aux Données Complètes
            </h3>
            <p class="text-gray-600 mb-8 leading-relaxed">
              Visualisez les tendances, analysez les performances et optimisez
              la gestion des déchets avec notre dashboard complet.
            </p>
            <button 
              class="flex items-center gap-2 bg-gradient-to-r from-green-600 to-green-400 text-white py-4 px-8 rounded-full text-lg font-semibold cursor-pointer transition-all duration-300 border-none hover:-translate-y-1 hover:shadow-xl hover:shadow-green-600/40"
              @click="navigateToDashboard"
            >
              <span class="text-xl">🔐</span>
              Se Connecter au Dashboard
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- Statistics Section -->
    <section class="py-16 bg-gradient-to-r from-green-600 to-green-400">
      <div class="max-w-6xl mx-auto px-8">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          <div 
            v-for="stat in statistics" 
            :key="stat.id"
            class="text-center text-white"
          >
            <div class="text-5xl font-extrabold mb-2">
              {{ displayedStats[stat.id] }}
            </div>
            <div class="text-lg opacity-90">
              {{ stat.label }}
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Impact Section -->
    <section id="impact" class="py-24 bg-white">
      <div class="max-w-6xl mx-auto px-8">
        <h2 class="text-center text-5xl font-bold mb-12 text-slate-800">
          Impact Environnemental
        </h2>
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
          <div>
            <h3 class="text-3xl mb-6 text-gray-800 font-semibold">
              Une Solution AI for Good
            </h3>
            <p class="text-gray-600 mb-8 leading-relaxed">
              Notre plateforme s'inscrit dans une démarche Green IT et contribue
              directement à la réduction de l'empreinte écologique urbaine en
              prévenant les dépôts sauvages avant qu'ils ne se forment.
            </p>
            <ul class="space-y-4">
              <li class="text-gray-600 text-lg">- Réduction des déchets abandonnés</li>
              <li class="text-gray-600 text-lg">- Optimisation des tournées de collecte</li>
              <li class="text-gray-600 text-lg">- Amélioration du cadre de vie urbain</li>
              <li class="text-gray-600 text-lg">- Sensibilisation citoyenne</li>
            </ul>
          </div>
          <div class="flex justify-center items-center">
            <div class="flex gap-8 text-7xl animate-bounce">
              <div>🌳</div>
              <div>🏙️</div>
              <div>♻️</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from "vue";
import { useRouter } from "vue-router";

export default {
  name: "Home",
  setup() {
    const router = useRouter();
    const displayedStats = reactive({
      images: 0,
      accuracy: 0,
      reduction: 0,
      cities: 0,
    });

    const features = [
      {
        id: 1,
        icon: "🎯",
        title: "Détection Automatique",
        description:
          "Analyse instantanée de l'état des poubelles (vide, pleine, débordante) grâce à des règles simples de détenction",
      },
      {
        id: 2,
        icon: "🗺️",
        title: "Cartographie Dynamique",
        description:
          "Visualisation en temps réel des zones à risque de débordement sur une carte interactive",
      },
      {
        id: 3,
        icon: "📊",
        title: "Tableau de Bord",
        description:
          "Statistiques complètes et graphiques interactifs pour optimiser la gestion des déchets",
      },
      {
        id: 4,
        icon: "⚡",
        title: "Prédiction Préventive",
        description:
          "Anticipation des zones à risque pour une action préventive efficace",
      },
    ];

    const statistics = [
      { id: "images", value: 1247, label: "Images Analysées" },
      { id: "accuracy", value: 94, label: "% de Précision" },
      { id: "reduction", value: 67, label: "% Réduction Dépôts" },
      { id: "cities", value: 12, label: "Villes Testées" },
    ];

    const scrollToSection = (sectionId) => {
      const element = document.getElementById(sectionId);
      if (element) {
        element.scrollIntoView({ behavior: "smooth" });
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
    };

    const animateCard = (event) => {
      event.currentTarget.style.transform = "translateY(-10px) scale(1.02)";
    };

    const resetCard = (event) => {
      event.currentTarget.style.transform = "translateY(0) scale(1)";
    };

    const animateStats = () => {
      statistics.forEach((stat) => {
        let current = 0;
        const increment = stat.value / 50;
        const timer = setInterval(() => {
          current += increment;
          if (current >= stat.value) {
            displayedStats[stat.id] = stat.value;
            clearInterval(timer);
          } else {
            displayedStats[stat.id] = Math.floor(current);
          }
        }, 50);
      });
    };

    onMounted(() => {
      setTimeout(animateStats, 1000);
    });

    return {
      displayedStats,
      features,
      statistics,
      scrollToSection,
      navigateToUpload,
      navigateToDashboard,
      animateCard,
      resetCard,
    };
  },
};
</script>

<style scoped>
@keyframes bounce {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
}

.animate-bounce {
  animation: bounce 3s ease-in-out infinite;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .hero-container {
    grid-template-columns: 1fr;
    text-align: center;
  }
  
  .hero-title {
    font-size: 2.5rem;
  }
  
  .dashboard-preview,
  .impact-content {
    grid-template-columns: 1fr;
  }
}</style>