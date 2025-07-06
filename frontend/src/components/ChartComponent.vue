<template>
  <div class="relative h-80">
    <canvas ref="canvas" class="w-full h-full"></canvas>
  </div>
</template>

<script>
import { defineComponent, nextTick, toRaw } from 'vue'
import { Chart, registerables } from 'chart.js'

// Ensure Chart.js components are registered only once
if (!Chart._cleansightRegistered) {
  Chart.register(...registerables)
  Chart._cleansightRegistered = true
}

function toPlain(value, seen = new Map()) {
  if (value === null || typeof value !== 'object') {
  
  const result = Array.isArray(raw) ? [] : {}
  seen.set(raw, result)

  Object.keys(raw).forEach(key => {
    result[key] = toPlain(raw[key], seen)
  })

  return result
  }

  const raw = toRaw(value)
  if (seen.has(raw)) {
    return seen.get(raw)
  }

  const result = Array.isArray(raw) ? [] : {}
  seen.set(raw, result)

  Object.keys(raw).forEach(key => {
    result[key] = toPlain(raw[key], seen)
  })

  return result
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
      chart: null
    }
  },
  async mounted() {
    await nextTick()
    this.createChart()
  },
  beforeUnmount() {
    if (this.chart && typeof this.chart.destroy === 'function') {
      this.chart.destroy()
      this.chart = null
    }
  },
  watch: {
    data: {
      handler(newVal) {
        // Validation stricte
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
      deep: false
    }
  },
  methods: {
    createChart() {
      if (this.chart && typeof this.chart.destroy === 'function') {
        this.chart.destroy()
        this.chart = null
      }

      const canvas = this.$refs.canvas
      const ctx = canvas?.getContext('2d')
      if (!ctx || !canvas?.parentNode || !this.data || !Array.isArray(this.data.datasets)) {
        console.warn('⛔ ChartComponent: Données invalides ou canvas introuvable, création annulée.')
        return
      }

      const safeData = toPlain(this.data || {})
      const safeOptions = toPlain(this.options || {})



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
    updateChart() {
     if (
        !this.chart ||
        !this.chart.canvas ||
        !this.chart.canvas.parentNode ||
        !this.data ||
        !Array.isArray(this.data.datasets)
      ) {
        console.warn('⛔ ChartComponent: Données invalides ou canvas détaché, update annulé.')
        return
      }
      try {
        const safeData = toPlain(this.data || {})
        this.chart.data = safeData
        this.chart.update()
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
