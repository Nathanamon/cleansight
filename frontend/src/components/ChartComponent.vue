<template>
  <div class="relative h-80">
    <canvas ref="canvas" class="w-full h-full"></canvas>
  </div>
</template>

<script>
import { Chart, registerables } from 'chart.js'
Chart.register(...registerables)

export default {
  name: 'ChartComponent',
  props: {
    chartId: String,
    type: String,
    data: Object,
    options: Object,
    width: Number,
    height: Number
  },
  data() {
    return {
      chart: null
    }
  },
  mounted() {
    this.createChart();
  },
  beforeUnmount() {
    if (this.chart) this.chart.destroy();
  },
  watch: {
    data: {
      handler() {
        this.updateChart();
      },
      deep: true
    }
  },
  methods: {
    createChart() {
      const ctx = this.$refs.canvas.getContext('2d');
      if (ctx) {
        this.chart = new Chart(ctx, {
          type: this.type,
          data: this.data,
          options: {
            responsive: true,
            maintainAspectRatio: false,
            ...this.defaultOptions,
            ...this.options
          }
        });
      }
    },
    updateChart() {
      if (this.chart) {
        this.chart.data = this.data;
        this.chart.update();
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
      };

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
        };
      }

      return baseOptions;
    }
  }
}
</script>
