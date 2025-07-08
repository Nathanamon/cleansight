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
          title="Poubelles vides uploadées"
          :value="statistics.emptyBins"
          icon="fas fa-trash"
          icon-bg-color="bg-green-500"
          :trend="statistics.emptyTrend"
        />
        
        <stat-card
          title="Poubelles pleines uploadées"
          :value="statistics.fullBins"
          icon="fas fa-trash-alt"
          icon-bg-color="bg-red-500"
          :trend="statistics.fullTrend"
        />
        <stat-card
          title="Poubelles pleines vidées"
          :value="statistics.emptiedBins"
          icon="fas fa-trash-alt"
          icon-bg-color="bg-indigo-500"
          :trend="statistics.emptiedTrend"
        />
      </div>

      <!-- Trash Map Section -->
<div class="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
  <h3 class="text-lg font-semibold text-gray-900 mb-4">
    <i class="fas fa-map-marked-alt mr-2 text-green-600"></i>
    Carte des poubelles
  </h3>
  <TrashMap
    :poubelles="mapPoubelles"
    :center="mapCenter"
    @bin-emptied="handleBinEmptied"
  />
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
          <safe-chart
            chart-id="dailyChart"
            type="line"
            :data="rawDailyChartData"
            :options="rawDailyChartOptions"
          />
        </div>

        <!-- Correlation Météo / Poubelles pleines -->
        <div class="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">
            <i class="fas fa-cloud-sun-rain mr-2 text-blue-500"></i>
            Corrélation Météo / Poubelles pleines
          </h3>
          <safe-chart
            chart-id="weatherTrashChart"
            type="bar"
            :data="rawWeatherTrashChartData"
            :options="rawWeatherTrashChartOptions"
          />
        </div>
        
        <!-- Heures de pic de remplissage -->
        <div class="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">
            <i class="fas fa-clock mr-2 text-orange-500"></i>
            Heures de pic de remplissage
          </h3>
          <safe-chart
            chart-id="peakHoursChart"
            type="radar"
            :data="rawPeakHoursChartData"
            :options="rawPeakHoursChartOptions
          />
        </div>
        
        
        <!-- District Distribution Chart -->
        <div class="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">
            <i class="fas fa-map-marker-alt mr-2 text-green-500"></i>
            Répartition par arrondissements
          </h3>
          <safe-chart
            chart-id="districtChart"
            type="doughnut"
            :data="rawDistrictChartData"
            :options="rawDistrictChartOptions"
          />

        </div>
        
        <!-- Taux moyen de remplissage par arrondissement -->
        <!-- <div class="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">
            <i class="fas fa-chart-bar mr-2 text-indigo-500"></i>
            Taux moyen de remplissage par arrondissement
          </h3>
          <chart-component
            v-if="hasFillRateData"
            chart-id="fillRateChart"
            type="bar"
            :data="rawFillRateChartData"
            :options="rawFillRateChartOptions"
          />
        </div> -->

        <!-- Fiabilité de la classification automatique -->
        <div class="bg-white rounded-xl shadow-sm p-6 border border-gray-200">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">
            <i class="fas fa-robot mr-2"></i>
            Fiabilité de la classification automatique
          </h3>
          <safe-chart
            chart-id="accuracyChart"
            type="bar"
            :data="rawClassificationAccuracyData"
            :options="rawClassificationAccuracyOptions"
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
import SafeChart from '../components/SafeChart.vue'
import RecentImages from '../components/RecentImages.vue'
import { toRaw } from 'vue'

function toRawClone(obj) {
  try {
    return JSON.parse(JSON.stringify(toRaw(obj)))
  } catch {
    return {}
  }
}


export default {
  name: 'Dashboard',
  components: {
    Sidebar,
    StatCard,
    ChartComponent,
    SafeChart,
    RecentImages,
    TrashMap,
    /* TrashWeatherStats */
  },
  data() {
    return {
      isLoading: false,
      mapRefreshInterval: null,
      chartRefreshInterval: null,
      selectedPeriod: '7',
      statistics: {
        totalImages: 0,
        emptyBins: 0,
        fullBins: 0,
        emptiedBins: 0,
        imagesTrend: 0,
        emptyTrend: 0,
        emptiedTrend: 0,
        fullTrend: 0
      },
      dailyData: { labels: [], full: [], empty: [] },
      accuracyData: { labels: [], correct: [], incorrect: [] },
      weatherData: { labels: [], full: [], humidity: [] },
      fillRateData: { labels: [], rate: [] },
      peakHoursData: { labels: [], rate: [] },
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
        text: 'Humidité (%)'
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


      mapPoubelles: [],
      recentImages: []
    }
  },
  computed: {
    hasDailyData() {
    return this.dailyData.labels.length > 0 &&
           this.dailyData.full.length > 0 &&
           this.dailyData.empty.length > 0
    },
hasWeatherTrashData() {
  return (
    Array.isArray(this.weatherData?.labels) &&
    this.weatherData.labels.length > 0 &&
    Array.isArray(this.weatherData.full) &&
    this.weatherData.full.length > 0 &&
    Array.isArray(this.weatherData.humidity) &&
    this.weatherData.humidity.length > 0
  )
},
hasPeakHoursData() {
  return (
    Array.isArray(this.peakHoursData?.labels) &&
    this.peakHoursData.labels.length > 0 &&
    Array.isArray(this.peakHoursData?.rate) &&
    this.peakHoursData.rate.length > 0
  )
},
hasDistrictData() {
  const labels = this.districtChartData.labels
  const data = this.districtChartData.datasets[0]?.data || []
  return Array.isArray(labels) && labels.length > 0 && labels.length === data.length
},
hasFillRateData() {
  const labels = this.fillRateChartData.labels || []
  const data = this.fillRateChartData.datasets[0]?.data || []
  return labels.length > 0 && labels.length === data.length
},
hasClassificationAccuracyData() {
  const chartData = this.classificationAccuracyData
  const labels = chartData.labels || []
  const datasets = chartData.datasets || []

  return (
    labels.length > 0 &&
    datasets.length === 2 &&
    datasets.every(ds => ds.data.length === labels.length)
  )
},


    
    rawDailyChartData() {
      return toRawClone(this.dailyChartData)
    },
    rawDailyChartOptions() {
      return toRawClone(this.dailyChartOptions)
    },
    rawDistrictChartData() {
      return toRawClone(this.districtChartData)
    },
    rawDistrictChartOptions() {
      return toRawClone(this.districtChartOptions)
    },
    rawClassificationAccuracyData() {
      return toRawClone(this.classificationAccuracyData)
    },
    rawClassificationAccuracyOptions() {
      return toRawClone(this.classificationAccuracyOptions)
    },
    rawWeatherTrashChartData() {
      return toRawClone(this.weatherTrashChartData)
    },
    rawWeatherTrashChartOptions() {
      return toRawClone(this.weatherTrashChartOptions)
    },
    rawFillRateChartData() {
      return toRawClone(this.fillRateChartData)
    },
    rawFillRateChartOptions() {
      return toRawClone(this.fillRateChartOptions)
    },
    rawPeakHoursChartData() {
      return toRawClone(this.peakHoursChartData)
    },
    rawPeakHoursChartOptions() {
      return toRawClone(this.peakHoursChartOptions)
    },
    lastUpdate() {
      return new Date().toLocaleString('fr-FR');
    },
    mapCenter() {
      if (this.mapPoubelles.length > 0) {
        const avgLat = this.mapPoubelles.reduce((s, p) => s + p.latitude, 0) / this.mapPoubelles.length;
        const avgLon = this.mapPoubelles.reduce((s, p) => s + p.longitude, 0) / this.mapPoubelles.length;
        return [avgLat, avgLon];
      }
      return [48.8566, 2.3522];
    },
    dailyChartData() {
  const hasValidData =
    Array.isArray(this.dailyData?.labels) &&
    this.dailyData.labels.length > 0 &&
    Array.isArray(this.dailyData.full) &&
    this.dailyData.full.length > 0 &&
    Array.isArray(this.dailyData.empty) &&
    this.dailyData.empty.length > 0

  if (!hasValidData) {
    return { labels: [], datasets: [] }
  }

  return {
    labels: this.dailyData.labels,
    datasets: [
      {
        label: 'Poubelles Pleines',
        data: this.dailyData.full,
        borderColor: 'rgb(239, 68, 68)',
        backgroundColor: 'rgba(239, 68, 68, 0.1)',
        tension: 0.4,
        fill: true
      },
      {
        label: 'Poubelles Vides',
        data: this.dailyData.empty,
        borderColor: 'rgb(34, 197, 94)',
        backgroundColor: 'rgba(34, 197, 94, 0.1)',
        tension: 0.4,
        fill: true
      }
    ]
  }
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
    const counts = {}

    for (const bin of this.mapPoubelles) {
      const address = bin.address || bin.location?.address || ""
      const match = address.match(/75(\d{3})/)
      if (match) {
        const arrondissement = match[1]  // ex: '015' → 15e
        counts[arrondissement] = (counts[arrondissement] || 0) + 1
      }
    }

    // Tri par arrondissement numérique croissant
    const sortedArr = Object.keys(counts).sort((a, b) => parseInt(a) - parseInt(b))

    return {
      labels: sortedArr.map(num => `${parseInt(num)}e`),
      datasets: [{
        data: sortedArr.map(num => counts[num]),
        backgroundColor: [
          '#EF4444', '#F97316', '#EAB308', '#22C55E', '#06B6D4',
          '#3B82F6', '#8B5CF6', '#EC4899', '#F59E0B', '#84CC16',
          '#10B981', '#6366F1', '#D946EF', '#F43F5E', '#0EA5E9',
          '#FACC15', '#4ADE80', '#14B8A6', '#A855F7', '#E11D48'
        ],
        borderWidth: 0
      }]
    }
  },
    classificationAccuracyData() {
  const labels = Array.isArray(this.accuracyData.labels) ? this.accuracyData.labels : []
  const correct = Array.isArray(this.accuracyData.correct) ? this.accuracyData.correct : []
  const incorrect = Array.isArray(this.accuracyData.incorrect) ? this.accuracyData.incorrect : []

  const length = Math.min(labels.length, correct.length, incorrect.length)

  return {
    labels: labels.slice(0, length),
    datasets: [
      {
        label: 'Correctement classées',
        data: correct.slice(0, length).map(val => (typeof val === 'number' ? val : 0)),
        backgroundColor: 'rgba(132, 204, 22, 0.8)'
      },
      {
        label: 'Corrigées manuellement',
        data: incorrect.slice(0, length).map(val => (typeof val === 'number' ? val : 0)),
        backgroundColor: 'rgba(251, 191, 36, 0.8)'
      }
    ]
  }
},

     weatherTrashChartData() {
      return {
        labels: this.weatherData.labels,
        datasets: [
          {
            label: 'Poubelles pleines',
            data: this.weatherData.full,
            backgroundColor: 'rgba(34, 197, 94, 0.6)',
            yAxisID: 'y'
          },
          {
            label: 'Humidité (%)',
            data: this.weatherData.humidity,
            backgroundColor: 'rgba(59, 130, 246, 0.6)',
            yAxisID: 'y1'
          }
        ]
      }
    },
    fillRateChartData() {
  const labels = Array.isArray(this.fillRateData.labels) ? this.fillRateData.labels : []
  const rates = Array.isArray(this.fillRateData.rate) ? this.fillRateData.rate : []

  const sanitizedRates = rates.map(val => (typeof val === 'number' ? val : 0))
  const length = Math.min(labels.length, sanitizedRates.length)

  return {
    labels: labels.slice(0, length),
    datasets: [
      {
        label: 'Taux de remplissage (%)',
        data: sanitizedRates.slice(0, length),
        backgroundColor: 'rgba(99, 102, 241, 0.6)'
      }
    ]
  }
},

    peakHoursChartData() {
      return {
        labels: this.peakHoursData.labels,
        datasets: [
          {
            label: 'Remplissage',
            data: this.peakHoursData.rate,
            backgroundColor: 'rgba(249, 115, 22, 0.3)',
            borderColor: 'rgb(249, 115, 22)',
            pointBackgroundColor: 'rgb(249, 115, 22)'
          }
        ]
      }
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
    await this.loadMapData()
    // Refresh map data every 30s so new uploads appear quickly without
    // leaving the map empty for too long between updates
    this.mapRefreshInterval = setInterval(() => {
      this.loadMapData()
    }, 5000)
    // Refresh chart data every 5 seconds
    this.chartRefreshInterval = setInterval(() => {
      this.loadDashboardData()
    }, 5000)
  },

  beforeUnmount() {
    if (this.mapRefreshInterval) {
      clearInterval(this.mapRefreshInterval)
    }
    if (this.chartRefreshInterval) {
      clearInterval(this.chartRefreshInterval)
    }
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
          this.statistics.emptiedBins = data.emptied_bins || 0
        }
        const rec = await fetch(import.meta.env.VITE_API_URL + '/dashboard/recent')
        if (rec.ok) {
          const imgs = await rec.json()
            this.recentImages = imgs.map(img => ({
              id: img.id,
              filename: img.filename,
              status: img.annotation,
              location: img.location || 'Paris',
              uploadTime: new Date(img.date_upload).toLocaleString('fr-FR'),
              thumbnail: (() => {
                const base = import.meta.env.VITE_API_URL
                const raw = img.thumbnail || `/uploads/${img.filename}`
                if (raw.startsWith('http')) return raw
                const encoded = raw.replace(img.filename, encodeURIComponent(img.filename))
                return `${base}${encoded}`
              })(),
            }))
        }
        const daily = await fetch(`${import.meta.env.VITE_API_URL}/dashboard/daily?days=${this.selectedPeriod}`)
        if (daily.ok) {
          this.dailyData = await daily.json()
        }
        const acc = await fetch(`${import.meta.env.VITE_API_URL}/dashboard/accuracy`)
        if (acc.ok) {
          this.accuracyData = await acc.json()
        }
                const weather = await fetch(`${import.meta.env.VITE_API_URL}/dashboard/weather_trash?days=${this.selectedPeriod}`)
        if (weather.ok) {
          this.weatherData = await weather.json()
        }
        const fill = await fetch(`${import.meta.env.VITE_API_URL}/dashboard/fill_rate`)
        if (fill.ok) {
          this.fillRateData = await fill.json()
        }
        const peak = await fetch(`${import.meta.env.VITE_API_URL}/dashboard/peak_hours`)
        if (peak.ok) {
          this.peakHoursData = await peak.json()
        }
        await this.$nextTick()
        window.dispatchEvent(new Event('resize'))
      } catch (e) {
        console.error('Erreur chargement dashboard:', e)
      }
    },
    async loadMapData() {
      try {
        const res = await fetch(import.meta.env.VITE_API_URL + '/dashboard/map')
        if (res.ok) {
          const items = await res.json()
          this.mapPoubelles = items
            .filter(p => p.etat !== 'vide' && p.etat !== 'vidée')
            .map(p => ({
              ...p,
              latitude: parseFloat(p.latitude),
              longitude: parseFloat(p.longitude),
              address: p.address || 'Adresse inconnue',
              thumbnail: (() => {
                const base = import.meta.env.VITE_API_URL
                const raw = p.thumbnail || `/uploads/${p.filename}`
                if (raw.startsWith('http')) return raw
                const encoded = raw.replace(p.filename, encodeURIComponent(p.filename))
                return `${base}${encoded}`
              })(),
              thumbnail: `${import.meta.env.VITE_API_URL}/uploads/${encodeURIComponent(p.filename)}`
            }))
        }
      } catch (e) {
        console.error('Erreur chargement carte:', e)
      }
    },
    async refreshData() {
      this.isLoading = true;
      try {
        await this.loadDashboardData();
        await this.loadMapData();
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
    async updateChartData() {
      const [daily, weather] = await Promise.all([
        fetch(`${import.meta.env.VITE_API_URL}/dashboard/daily?days=${this.selectedPeriod}`),
        fetch(`${import.meta.env.VITE_API_URL}/dashboard/weather_trash?days=${this.selectedPeriod}`)
      ])

      if (daily.ok) {
        this.dailyData = await daily.json()
      }
      if (weather.ok) {
        this.weatherData = await weather.json()
      }
      await this.$nextTick()
      window.dispatchEvent(new Event('resize'))
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
    },
    handleBinEmptied(id) {
      const idx = this.mapPoubelles.findIndex(p => p.id === id)
      if (idx > -1) this.mapPoubelles.splice(idx, 1)
    }
  }
}
</script>
