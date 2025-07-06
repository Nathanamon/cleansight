<template>
  <div class="relative h-80">
    <canvas ref="canvas" class="w-full h-full"></canvas>
  </div>
</template>

<script>
import { defineComponent, nextTick, toRaw } from 'vue'
import { Chart, registerables } from 'chart.js'

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
    this.createChart()
    // Force an initial resize in case the component was hidden on mount
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
      deep: false,
      flush: 'post'
    }
  },
  methods: {
    createChart() {
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
    resizeChart() {
      if (this.chart?.resize) {
        this.chart.resize()
      } else {
        // Fallback: trigger global resize for Chart.js to recalculate dimensions
        window.dispatchEvent(new Event('resize'))
      }
    },
    initResizeObserver() {
      const el = this.$el
      if (typeof ResizeObserver !== 'undefined' && el) {
        this.resizeObserver = new ResizeObserver(() => this.resizeChart())
        this.resizeObserver.observe(el)
      }
    },
    updateChart() {
      if (!this.data || !Array.isArray(this.data.datasets)) {
        console.warn('⛔ ChartComponent: Données invalides, update annulé.')
        return
      }

      if (!this.chart) {
        this.createChart()
        return
      }

      if (!this.chart.canvas?.parentNode) {
        console.warn('⛔ ChartComponent: canvas détaché, update annulé.')
        return
      }

      try {
        const safeData = safeClone(this.data)
        this.chart.data = safeData
        this.chart.update()
        this.resizeChart()
      } catch (err) {
        console.error('⛔ ChartComponent: erreur lors de la mise à jour du graphique', err)
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
