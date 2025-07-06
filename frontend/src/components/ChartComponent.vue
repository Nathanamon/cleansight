<template>
  <div class="relative h-80">
    <canvas ref="canvas" class="w-full h-full"></canvas>
  </div>
</template>

<script>
import { defineComponent, nextTick, toRaw } from 'vue'
import { Chart, registerables } from 'chart.js'
import isEqual from 'lodash/isEqual'

// Enregistrement unique de Chart.js
if (!Chart._cleansightRegistered) {
  Chart.register(...registerables)
  Chart._cleansightRegistered = true
}

// Utilitaire : conversion deep clone sécurisée
function safeClone(obj) {
  try {
    return JSON.parse(JSON.stringify(toRaw(obj || {})))
  } catch {
    return {}
  }
}

export default defineComponent({
  name: 'ChartComponent',
  props: {
    chartId: String,
    type: String,
    data: Object,
    options: Object
  },
  data() {
    return {
      chart: null,
      resizeObserver: null
    }
  },
  async mounted() {
    await nextTick()
    await this.createChart()
    await nextTick()
    this.resizeChart()
    this.initResizeObserver()
    window.addEventListener('resize', this.resizeChart)
  },
  beforeUnmount() {
    if (this.chart?.destroy) {
      this.chart.destroy()
      this.chart = null
    }
    window.removeEventListener('resize', this.resizeChart)
    if (this.resizeObserver) {
      this.resizeObserver.disconnect()
      this.resizeObserver = null
    }
  },
  watch: {
    data: {
      handler(newVal) {
        if (
          newVal &&
          typeof newVal === 'object' &&
          Array.isArray(newVal.datasets) &&
          newVal.datasets.every(ds => Array.isArray(ds.data))
        ) {
          this.updateChart()
        } else {
          console.warn('🔁 Données ignorées : format invalide pour chart.js')
        }
      },
      deep: true,
      flush: 'post'
    }
  },
  methods: {
    async waitForVisible() {
      const el = this.$el
      while (el && (el.offsetWidth === 0 || el.offsetHeight === 0)) {
        await new Promise(resolve => requestAnimationFrame(resolve))
      }
    },
    async createChart() {
      await this.waitForVisible()

      if (this.chart?.destroy) {
        this.chart.destroy()
        this.chart = null
      }

      const canvas = this.$refs.canvas
      const ctx = canvas?.getContext('2d')
      if (!ctx || !canvas?.parentNode || !this.data || !Array.isArray(this.data.datasets)) {
        console.warn('⛔ ChartComponent: Données invalides ou canvas introuvable, création annulée.')
        return
      }

      const safeData = safeClone(this.data)
      const safeOptions = safeClone(this.options)

      try {
        this.chart = new Chart(ctx, {
          type: this.type,
          data: safeData,
          options: {
            responsive: true,
            maintainAspectRatio: false,
            ...this.defaultOptions,
            ...safeOptions
          }
        })
      } catch (err) {
        console.error('⛔ ChartComponent: erreur lors de la création du graphique', err)
      }
    },


    async updateChart() {
  if (!this.data || !Array.isArray(this.data.datasets)) {
    console.warn('⛔ ChartComponent: Données invalides, update annulé.')
    return
  }

  if (!this.chart || !this.chart.canvas?.isConnected) {
    console.warn('⛔ ChartComponent: chart manquant ou canvas déconnecté. Création forcée.')
    await this.createChart()
    return
  }

  try {
    await this.waitForVisible()

    const safeData = safeClone(this.data)

    // Vérifie que labels et data sont cohérents
    const isValid = (
      Array.isArray(safeData.labels) &&
      safeData.datasets.every(ds => Array.isArray(ds.data)) &&
      safeData.datasets.every(ds => ds.data.length === safeData.labels.length)
    )

    if (!isValid) {
      console.warn('⛔ ChartComponent: données invalides (longueurs incohérentes)')
      return
    }

    const hasChanged = !isEqual(this.chart.data.labels, safeData.labels) ||
                       !isEqual(this.chart.data.datasets, safeData.datasets)

    if (hasChanged) {
      this.chart.data.labels = safeData.labels

      // Mutation profonde des datasets pour préserver l'animation
      this.chart.data.datasets.forEach((target, i) => {
        const source = safeData.datasets[i]
        if (source) {
          Object.assign(target, source)
        }
      })

      this.chart.update()
      this.resizeChart()
    } else {
      console.log('📊 Données inchangées — aucune mise à jour nécessaire')
    }

  } catch (err) {
    console.error('⛔ ChartComponent: erreur lors de updateChart', err)
  }
}


  },
  computed: {
    defaultOptions() {
      const baseOptions = {
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              usePointStyle: true,
              padding: 20
            }
          }
        }
      }

      if (this.type === 'line' || this.type === 'bar') {
        return {
          ...baseOptions,
          scales: {
            y: {
              beginAtZero: true,
              grid: { color: 'rgba(0,0,0,0.1)' }
            },
            x: {
              grid: { display: false }
            }
          }
        }
      }

      return baseOptions
    }
  }
})
</script>
