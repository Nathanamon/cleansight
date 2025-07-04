<template>
  <div class="flex min-h-screen bg-gray-100">
    <!-- Sidebar (visible uniquement ici) -->
    <Sidebar />

    <!-- Main Content -->
    <div class="flex-1 p-6 space-y-6 overflow-y-auto">
      <!-- Page Header -->
      <div class="flex justify-between items-center">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p class="text-gray-600 mt-1">Vue d'ensemble de la gestion des poubelles</p>
        </div>
        <div class="flex items-center space-x-4">
          <button
            @click="refreshData"
            :disabled="isLoading"
            class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
          >
            <i :class="['fas fa-sync-alt mr-2', { 'animate-spin': isLoading }]"></i>
            Actualiser
          </button>
          <div class="text-sm text-gray-500">
            Dernière mise à jour: {{ lastUpdate }}
          </div>
        </div>
      </div>

      <!-- Statistics Cards -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <stat-card
          title="Total Images Uploadées"
          :value="statistics.totalImages"
          icon="fas fa-images"
          icon-bg-color="bg-blue-500"
          :trend="statistics.imagesTrend"
        />
        
        <stat-card
          title="Poubelles Vides"
          :value="statistics.emptyBins"
          icon="fas fa-trash"
          icon-bg-color="bg-green-500"
          :trend="statistics.emptyTrend"
        />
        
        <stat-card
          title="Poubelles Pleines"
          :value="statistics.fullBins"
          icon="fas fa-trash-alt"
          icon-bg-color="bg-red-500"
          :trend="statistics.fullTrend"
        />
      </div>

      <!-- Trash Map Section -->
<div class="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
  <h3 class="text-lg font-semibold text-gray-900 mb-4">
    <i class="fas fa-map-marked-alt mr-2 text-green-600"></i>
    Carte des poubelles
  </h3>
  <TrashMap :poubelles="mapPoubelles" :center="[48.8566, 2.3522]" />
</div>

      <!-- Charts Section -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Daily Evolution Chart -->
        <div class="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-semibold text-gray-900">
              <i class="fas fa-chart-line mr-2 text-blue-500"></i>
              Évolution quotidienne des uploads
            </h3>
            <select
              v-model="selectedPeriod"
              @change="updateChartData"
              class="text-sm border border-gray-300 rounded-md px-3 py-1"
            >
              <option value="7">7 derniers jours</option>
              <option value="30">30 derniers jours</option>
              <option value="90">3 derniers mois</option>
            </select>
          </div>
          <chart-component
            chart-id="dailyChart"
            type="line"
            :data="dailyChartData"
            :options="dailyChartOptions"
          />
        </div>

        <!-- District Distribution Chart -->
        <div class="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">
            <i class="fas fa-map-marker-alt mr-2 text-green-500"></i>
            Répartition par arrondissements
          </h3>
          <chart-component
            chart-id="districtChart"
            type="doughnut"
            :data="districtChartData"
            :options="districtChartOptions"
          />
        </div>
        <!-- Correlation Météo / Poubelles pleines -->
<div class="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
  <h3 class="text-lg font-semibold text-gray-900 mb-4">
    <i class="fas fa-cloud-sun-rain mr-2 text-blue-500"></i>
    Corrélation Météo / Poubelles pleines
  </h3>
  <chart-component
    chart-id="weatherTrashChart"
    type="bar"
    :data="weatherTrashChartData"
    :options="weatherTrashChartOptions"
  />
</div>
<!-- Taux moyen de remplissage par arrondissement -->
<div class="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
  <h3 class="text-lg font-semibold text-gray-900 mb-4">
    <i class="fas fa-chart-bar mr-2 text-indigo-500"></i>
    Taux moyen de remplissage par arrondissement
  </h3>
  <chart-component
    chart-id="fillRateChart"
    type="bar"
    :data="fillRateChartData"
    :options="fillRateChartOptions"
  />
</div>
<!-- Heures de pic de remplissage -->
<div class="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
  <h3 class="text-lg font-semibold text-gray-900 mb-4">
    <i class="fas fa-clock mr-2 text-orange-500"></i>
    Heures de pic de remplissage
  </h3>
  <chart-component
    chart-id="peakHoursChart"
    type="radar"
    :data="peakHoursChartData"
    :options="peakHoursChartOptions"
  />
</div>
<!-- Fiabilité de la classification automatique -->
<div class="bg-white rounded-xl shadow-sm p-6 border border-gray-200">
  <h3 class="text-lg font-semibold text-gray-900 mb-4">
    <i class="fas fa-robot mr-2"></i>
    Fiabilité de la classification automatique
  </h3>
  <chart-component
    chart-id="accuracyChart"
    type="bar"
    :data="classificationAccuracyData"
    :options="classificationAccuracyOptions"
  />
</div>




      </div>
      

      <!-- Recent Images Section -->
      <recent-images
        :images="recentImages"
        @view-image="handleViewImage"
        @download-image="handleDownloadImage"
        @delete-image="handleDeleteImage"
      />
    </div>
  </div>
</template>

<script>
import TrashMap from '../components/TrashMap.vue'
import Sidebar from '../components/Sidebar.vue'
import StatCard from '../components/StatCard.vue'
import ChartComponent from '../components/ChartComponent.vue'
import RecentImages from '../components/RecentImages.vue'
import { map } from 'leaflet'


export default {
  name: 'Dashboard',
  components: {
    Sidebar,
    StatCard,
    ChartComponent,
    RecentImages,
    TrashMap,
    /* TrashWeatherStats */
  },
  data() {
    return {
      isLoading: false,
      selectedPeriod: '7',
      statistics: {
        totalImages: 0,
        emptyBins: 0,
        fullBins: 0,
        imagesTrend: 0,
        emptyTrend: 0,
        fullTrend: 0
      },
      weatherTrashChartData: {
  labels: ['01/07', '02/07', '03/07', '04/07', '05/07'],
  datasets: [
    {
      label: 'Poubelles pleines',
      data: [12, 8, 16, 20, 10],
      backgroundColor: 'rgba(34, 197, 94, 0.6)',
      yAxisID: 'y'
    },
    {
      label: 'Pluie (mm)',
      data: [5, 0, 15, 30, 2],
      backgroundColor: 'rgba(59, 130, 246, 0.6)',
      yAxisID: 'y1'
    }
  ]
},
weatherTrashChartOptions: {
  responsive: true,
  interaction: {
    mode: 'index',
    intersect: false
  },
  stacked: false,
  scales: {
    y: {
      type: 'linear',
      position: 'left',
      title: {
        display: true,
        text: 'Poubelles pleines'
      },
      beginAtZero: true
    },
    y1: {
      type: 'linear',
      position: 'right',
      title: {
        display: true,
        text: 'Pluie (mm)'
      },
      beginAtZero: true,
      grid: {
        drawOnChartArea: false
      }
    }
  },
  plugins: {
    tooltip: {
      mode: 'index',
      intersect: false
    },
    legend: {
      position: 'top'
    }
  }
},
fillRateChartData: {
  labels: ['3e', '7e', '10e', '13e', '15e', '17e', '18e', '19e'],
  datasets: [
    {
      label: 'Taux de remplissage (%)',
      data: [62, 75, 90, 68, 81, 50, 87, 72],
      backgroundColor: 'rgba(99, 102, 241, 0.6)'
    }
  ]
},
fillRateChartOptions: {
  indexAxis: 'y',
  scales: {
    x: {
      beginAtZero: true,
      max: 100,
      title: {
        display: true,
        text: 'Pourcentage (%)'
      }
    }
  },
  plugins: {
    legend: {
      display: false
    },
    tooltip: {
      callbacks: {
        label: ctx => `${ctx.raw}%`
      }
    }
  }
},
peakHoursChartData: {
  labels: ['00h-06h', '06h-09h', '09h-12h', '12h-15h', '15h-18h', '18h-21h', '21h-00h'],
  datasets: [
    {
      label: 'Remplissage',
      data: [20, 35, 65, 80, 70, 50, 30],
      backgroundColor: 'rgba(249, 115, 22, 0.3)',
      borderColor: 'rgb(249, 115, 22)',
      pointBackgroundColor: 'rgb(249, 115, 22)'
    }
  ]
},
peakHoursChartOptions: {
  scales: {
    r: {
      beginAtZero: true,
      max: 100,
      ticks: {
        stepSize: 20
      },
      pointLabels: {
        font: {
          size: 12
        }
      }
    }
  },
  plugins: {
    legend: {
      position: 'top'
    }
  }
},
classificationAccuracyData: {
  labels: ['27/06', '28/06', '29/06', '30/06', '01/07'],
  datasets: [
    {
      label: 'Correctement classées',
      data: [80, 90, 85, 88, 92],
      backgroundColor: 'rgba(132, 204, 22, 0.8)'
    },
    {
      label: 'Corrigées manuellement',
      data: [20, 10, 15, 12, 8],
      backgroundColor: 'rgba(251, 191, 36, 0.8)'
    }
  ]
},
classificationAccuracyOptions: {
  responsive: true,
  plugins: {
    tooltip: {
      mode: 'index',
      intersect: false
    },
    legend: {
      position: 'top'
    }
  },
  scales: {
    x: {
      stacked: true
    },
    y: {
      stacked: true,
      beginAtZero: true,
      max: 100,
      title: {
        display: true,
        text: 'Pourcentage des images'
      }
    }
  }
},


      mapPoubelles: [
        { id: 1, latitude: 48.8566, longitude: 2.3522, etat: 'vide', timestamp: '2025-06-30T12:00:00Z' },
        { id: 2, latitude: 48.857, longitude: 2.355, etat: 'pleine', timestamp: '2025-06-30T12:05:00Z' },
        { id: 3, latitude: 48.858, longitude: 2.360, etat: 'débordante', timestamp: '2025-06-30T12:10:00Z' }
      ],
      recentImages: []
    }
  },
  computed: {
    lastUpdate() {
      return new Date().toLocaleString('fr-FR');
    },
    dailyChartData() {
      const labels = this.generateDateLabels();
      return {
        labels,
        datasets: [
          {
            label: 'Poubelles Pleines',
            data: this.generateRandomData(labels.length, 10, 30),
            borderColor: 'rgb(239, 68, 68)',
            backgroundColor: 'rgba(239, 68, 68, 0.1)',
            tension: 0.4,
            fill: true
          },
          {
            label: 'Poubelles Vides',
            data: this.generateRandomData(labels.length, 20, 50),
            borderColor: 'rgb(34, 197, 94)',
            backgroundColor: 'rgba(34, 197, 94, 0.1)',
            tension: 0.4,
            fill: true
          }
        ]
      };
    },
    dailyChartOptions() {
      return {
        interaction: {
          intersect: false,
          mode: 'index'
        },
        plugins: {
          tooltip: {
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            titleColor: 'white',
            bodyColor: 'white'
          }
        }
      };
    },
    districtChartData() {
      return {
        labels: ['1er', '2ème', '3ème', '4ème', '5ème', '6ème', '7ème', '8ème', '9ème', '10ème'],
        datasets: [{
          data: [45, 32, 28, 67, 43, 39, 52, 61, 38, 29],
          backgroundColor: [
            '#EF4444', '#F97316', '#EAB308', '#22C55E', '#06B6D4',
            '#3B82F6', '#8B5CF6', '#EC4899', '#F59E0B', '#84CC16'
          ],
          borderWidth: 0,
          hoverBorderWidth: 2,
          hoverBorderColor: '#fff'
        }]
      };
    },
    districtChartOptions() {
      return {
        cutout: '60%',
        plugins: {
          tooltip: {
            callbacks: {
              label: (context) => {
                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                const percentage = ((context.raw / total) * 100).toFixed(1);
                return `${context.label}: ${context.raw} (${percentage}%)`;
              }
            }
          }
        }
      };
    }
  },
  
  async mounted() {
    await this.loadDashboardData()
  },

  methods: {
    async loadDashboardData() {
      try {
        const res = await fetch(import.meta.env.VITE_API_URL + '/dashboard/summary')
        if (res.ok) {
          const data = await res.json()
          this.statistics.totalImages = data.total_images
          this.statistics.emptyBins = data.empty_bins
          this.statistics.fullBins = data.full_bins
        }
        const rec = await fetch(import.meta.env.VITE_API_URL + '/dashboard/recent')
        if (rec.ok) {
          const imgs = await rec.json()
          this.recentImages = imgs.map(img => ({
            id: img.id,
            filename: img.filename,
            status: img.annotation,
            location: 'Paris',
            uploadTime: new Date(img.date_upload).toLocaleString('fr-FR'),
            thumbnail: `${import.meta.env.VITE_API_URL}/uploads/${img.filename}`
          }))
        }
      } catch (e) {
        console.error('Erreur chargement dashboard:', e)
      }
    },
    async refreshData() {
      this.isLoading = true;
      try {
        this.loadDashboardData();
        this.$emit('show-notification', {
          type: 'success',
          message: 'Données actualisées avec succès'
        });
      } catch (error) {
        this.$emit('show-notification', {
          type: 'error',
          message: 'Erreur lors de l\'actualisation des données'
        });
      } finally {
        this.isLoading = false;
      }
    },
    updateChartData() {
      console.log('Mise à jour des données pour la période:', this.selectedPeriod);
    },
    generateDateLabels() {
      const days = parseInt(this.selectedPeriod);
      const labels = [];
      const today = new Date();
      for (let i = days - 1; i >= 0; i--) {
        const date = new Date(today);
        date.setDate(date.getDate() - i);
        labels.push(date.toLocaleDateString('fr-FR', { weekday: 'short', day: 'numeric' }));
      }
      return labels;
    },
    generateRandomData(length, min, max) {
      return Array.from({ length }, () =>
        Math.floor(Math.random() * (max - min + 1)) + min
      );
    },
    handleViewImage(image) {
      console.log('Voir image:', image);
    },
    handleDownloadImage(image) {
      console.log('Télécharger image:', image);
    },
    handleDeleteImage(image) {
      const index = this.recentImages.findIndex(img => img.id === image.id);
      if (index > -1) {
        this.recentImages.splice(index, 1);
      }
    }
  }
}
</script>
