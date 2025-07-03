<template>
  <div class="w-64 h-screen bg-white shadow-xl flex flex-col justify-between">
    <!-- Header -->
    <div>
      <div class="p-6 border-b border-gray-200">
        <h1 class="text-2xl font-extrabold text-green-600 flex items-center">
          <i class="fas fa-recycle mr-2"></i>
          CleanSight
        </h1>
        <p class="text-sm text-gray-500 mt-1">Tous vigilants, tous propres</p>
      </div>

      <!-- Navigation -->
      <nav class="mt-6 flex-1">
        <div class="px-4 space-y-2">
          <router-link
            v-for="tab in tabs"
            :key="tab.id"
            :to="'/' + tab.id"
            class="block"
          >
            <div
              :class="[
                'w-full flex items-center px-4 py-3 rounded-lg text-sm font-medium transition-colors duration-150',
                $route.path.startsWith('/' + tab.id)
                  ? 'bg-green-100 text-green-700 border-r-4 border-green-500'
                  : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
              ]"
            >
              <i
                :class="[tab.icon, 'text-lg mr-3',
                  $route.path.startsWith('/' + tab.id) ? 'text-green-600' : 'text-gray-400']"
              ></i>
              {{ tab.name }}
            </div>
          </router-link>
        </div>
      </nav>
    </div>

    <!-- Footer -->
    <div class="p-4 border-t border-gray-200 text-center text-xs text-gray-400">
      <p>© 2025 <span class="font-semibold text-green-600">CleanSight</span></p>
      <p>GreenAI Collective</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Sidebar',
  data() {
    return {
      tabs: [
        { id: 'dashboard', name: 'Dashboard', icon: 'fas fa-tachometer-alt' },
        { id: 'images', name: 'Images', icon: 'fas fa-images' },
        { id: 'recommendations', name: 'Recommandations', icon: 'fas fa-lightbulb' },
        { id: 'rules', name: 'Règles', icon: 'fas fa-lightbulb' }
      ]
    }
  }
}
</script>

<style scoped>
/* Désactive le focus ring natif */
:focus {
  outline: none;
}
</style>
