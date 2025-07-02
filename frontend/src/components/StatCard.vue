<template>
  <div class="bg-white rounded-xl shadow-sm p-6 border border-gray-100 hover:shadow-md transition-shadow duration-200">
    <div class="flex items-center justify-between">
      <div class="flex-1">
        <p class="text-sm font-medium text-gray-600">{{ title }}</p>
        <p class="text-3xl font-bold text-gray-900 mt-2">
          {{ formattedValue }}
        </p>
        
        <!-- Trend indicator -->
        <div v-if="trend !== null" class="flex items-center mt-3">
          <div :class="[
            'flex items-center px-2 py-1 rounded-full text-xs font-medium',
            trend > 0 ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
          ]">
            <i :class="[
              'fas mr-1',
              trend > 0 ? 'fa-arrow-up' : 'fa-arrow-down'
            ]"></i>
            {{ Math.abs(trend) }}%
          </div>
          <span class="text-gray-500 text-xs ml-2">vs période précédente</span>
        </div>
      </div>
      
      <!-- Icon -->
      <div :class="[
        'w-16 h-16 rounded-full flex items-center justify-center ml-4',
        iconBgColor
      ]">
        <i :class="icon + ' text-2xl text-white'"></i>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StatCard',
  props: {
    title: {
      type: String,
      required: true
    },
    value: {
      type: [Number, String],
      required: true
    },
    icon: {
      type: String,
      required: true
    },
    iconBgColor: {
      type: String,
      default: 'bg-blue-500'
    },
    trend: {
      type: Number,
      default: null
    }
  },
  computed: {
    formattedValue() {
      if (typeof this.value === 'number') {
        return this.value.toLocaleString('fr-FR');
      }
      return this.value;
    }
  }
}
</script>