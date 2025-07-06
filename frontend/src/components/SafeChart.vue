<template>
  <div>
    <ChartComponent
      v-if="isValidData"
      :chart-id="chartId"
      :type="type"
      :data="data"
      :options="options"
    />
    <div v-else class="text-gray-400 text-center italic py-6">
      Données insuffisantes pour générer le graphique.
    </div>
  </div>
</template>

<script>
import ChartComponent from './ChartComponent.vue'

export default {
  name: 'SafeChart',
  components: { ChartComponent },
  props: {
    chartId: String,
    type: String,
    data: Object,
    options: Object
  },
  computed: {
    isValidData() {
      return (
        this.data &&
        Array.isArray(this.data.datasets) &&
        this.data.datasets.length > 0 &&
        this.data.datasets.some(ds => Array.isArray(ds.data) && ds.data.length > 0)
      )
    }
  }
}
</script>
