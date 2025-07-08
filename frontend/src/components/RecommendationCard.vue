<template>
  <div :class="['p-5 rounded-xl shadow-sm border transition relative', cardColor]">
    <div v-if="severity === 'high'" class="absolute top-2 right-2 flex h-3 w-3">
      <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
      <span class="relative inline-flex rounded-full h-3 w-3 bg-red-500"></span>
    </div>
    <div class="flex items-center gap-4">
      <div class="text-2xl">
        <i :class="[icon, 'text-gray-700']"></i>
      </div>
      <div>
        <h3 class="text-lg font-semibold text-gray-800">{{ title }}</h3>
        <p class="text-sm text-gray-600 mt-1">{{ description }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RecommendationCard',
  props: {
    title: String,
    description: String,
    icon: {
      type: String,
      default: 'fas fa-lightbulb'
    },
    severity: {
      type: String,
      default: 'low',
      validator: val => ['low', 'medium', 'high'].includes(val)
    }
  },
  computed: {
    cardColor() {
      switch (this.severity) {
        case 'high': return 'border-red-300 bg-red-50';
        case 'medium': return 'border-yellow-300 bg-yellow-50';
        case 'low': return 'border-green-300 bg-green-50';
        default: return 'border-gray-200 bg-white';
      }
    }
  }
}
</script>

