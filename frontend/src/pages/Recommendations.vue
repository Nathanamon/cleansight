<template>
  <div class="flex min-h-screen bg-gray-50">
    <Sidebar />
    <div class="flex-1 p-6 mt-20 space-y-6 overflow-y-auto">
      <div class="flex justify-between items-center">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">Recommandations IA</h1>
          <p class="text-gray-600 mt-1">Suggestions intelligentes basées sur les données collectées</p>
        </div>
        <button
          @click="refreshRecommendations"
          class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          <i class="fas fa-sync-alt mr-2"></i> Actualiser
        </button>
      </div>

      <!-- Empty State -->
      <div v-if="recommendations.length === 0" class="text-gray-500 text-sm">
        Aucune recommandation disponible pour le moment.
      </div>

      <!-- Dynamic Recommendations -->
      <div
        v-else
        class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6"
      >
        <RecommendationCard
          v-for="(rec, index) in recommendations"
          :key="index"
          :title="rec.title"
          :description="rec.description"
          :icon="rec.icon"
          :severity="rec.severity"
        />
      </div>
    </div>
  </div>
</template>

<script>
import Sidebar from '../components/Sidebar.vue'
import RecommendationCard from '../components/RecommendationCard.vue'

export default {
  name: 'Recommendations',
  components: {
    Sidebar,
    RecommendationCard
  },
  data() {
  return {
    recommendations: [],
    isLoading: false,
    error: null
  };
},
mounted() {
  this.loadRecommendations();
},
methods: {
  async loadRecommendations() {
    this.isLoading = true;
    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/dashboard/recommendations`);
      if (!res.ok) throw new Error("Échec du chargement des recommandations");
      const data = await res.json();
      this.recommendations = data.map(rec => ({
        title: rec.title,
        description: rec.text || rec.description,
        severity: rec.severity || 'medium',
        icon: this.chooseIcon(rec.severity)
      }));
    } catch (err) {
      this.error = err.message;
    } finally {
      this.isLoading = false;
    }
  },
  chooseIcon(severity) {
    if (severity === 'high') return 'fas fa-exclamation-triangle';
    if (severity === 'low') return 'fas fa-check-circle';
    return 'fas fa-lightbulb';
  }
},

  async mounted() {
  const res = await fetch(`${import.meta.env.VITE_API_URL}/dashboard/recommendations`);
  if (res.ok) {
    this.recommendations = await res.json();
  } else {
    console.error('Erreur chargement recommandations');
  }
},
  methods: {
    async refreshRecommendations() {
      try {
        const res = await fetch(`${import.meta.env.VITE_API_URL}/dashboard/recommendations`)
        if (res.ok) {
          const data = await res.json()
          this.recommendations = data
        } else {
          this.recommendations = []
          console.warn('Erreur chargement recommandations :', res.status)
        }
      } catch (e) {
        console.error('Erreur réseau recommandations :', e)
        this.recommendations = []
      }
    },
    async refreshRecommendations() {
  const res = await fetch(`${import.meta.env.VITE_API_URL}/dashboard/generate_recommendations`, {
    method: "POST",
  });
  if (res.ok) {
    this.fetchRecommendations(); // recharge le fichier JSON
  } else {
    console.error("Échec de génération");
  }
},
async fetchRecommendations() {
  const res = await fetch(`${import.meta.env.VITE_API_URL}/static/recommendations.json`);
  this.recommendations = await res.json();
}

  }
}
</script>
