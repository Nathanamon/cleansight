<template>
  <div class="flex min-h-screen bg-gray-50">
    <!-- Sidebar -->
    <Sidebar />

    <!-- Main Content -->
    <div class="flex-1 p-6 mt-20 space-y-6 overflow-y-auto">
      <!-- Page Header -->
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

      <!-- Recommendations List -->
      <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
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
      recommendations: [
        {
          title: 'Augmenter la fréquence de collecte dans le 15ème',
          description: 'Plus de 32% des poubelles débordantes sont localisées dans cet arrondissement.',
          icon: 'fas fa-map-marker-alt',
          severity: 'high'
        },
        {
          title: 'Planifier un entretien pour les bacs signalés en maintenance',
          description: '5 bacs ont été marqués en maintenance depuis plus de 48h.',
          icon: 'fas fa-tools',
          severity: 'medium'
        },
        {
          title: 'Optimiser la tournée du lundi matin',
          description: 'Le taux de remplissage est faible le lundi. Une tournée tous les 2 lundis est suffisante.',
          icon: 'fas fa-route',
          severity: 'low'
        },
        {
          title: 'Analyser l’augmentation soudaine d’uploads dans le 11ème',
          description: 'Une hausse de 80% d’images uploadées a été détectée sur 3 jours.',
          icon: 'fas fa-chart-line',
          severity: 'medium'
        },
        {
          title: 'Ajouter une poubelle rue de Vaugirard',
          description: 'Zone à forte densité de dépôts sauvages détectés sur les dernières images.',
          icon: 'fas fa-plus-square',
          severity: 'high'
        }
      ]
    };
  },
  methods: {
    refreshRecommendations() {
      console.log('Actualisation des recommandations IA...');
      // API call à l'IA possible ici
    }
  }
}
</script>
