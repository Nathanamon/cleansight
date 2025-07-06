<template>
  <div class="relative h-80">
    <canvas ref="canvas" class="w-full h-full"></canvas>
  </div>
</template>

<script>
import { defineComponent, nextTick } from 'vue'
import { Chart, registerables } from 'chart.js'

Chart.register(...registerables)

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

      const ctx = this.$refs.canvas?.getContext('2d')
      if (!ctx || !this.data || !Array.isArray(this.data.datasets)) {
        console.warn('⛔ ChartComponent: Données invalides, création annulée.')
        return
      }

      const safeData = JSON.parse(JSON.stringify(this.data || {}))
      const safeOptions = JSON.parse(JSON.stringify(this.options || {}))


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
    },
    updateChart() {
      if (!this.chart || !this.data || !Array.isArray(this.data.datasets)) {
        console.warn('⛔ ChartComponent: Données invalides, update annulé.')
        return
      }
      this.chart.data = this.data
      this.chart.update()
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
