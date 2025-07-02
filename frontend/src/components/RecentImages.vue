<template>
  <div class="bg-white rounded-xl shadow-sm border border-gray-100">
    <!-- Header -->
    <div class="p-6 border-b border-gray-200">
      <div class="flex items-center justify-between">
        <h3 class="text-lg font-semibold text-gray-900">
          <i class="fas fa-clock mr-2 text-purple-500"></i>
          5 Dernières images uploadées
        </h3>
        <button class="text-sm text-blue-600 hover:text-blue-700 font-medium">
          Voir tout
        </button>
      </div>
    </div>

    <!-- Images List -->
    <div class="p-6">
      <div class="space-y-4">
        <div
          v-for="image in images"
          :key="image.id"
          class="flex items-center space-x-4 p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors cursor-pointer"
          @click="viewImage(image)"
        >
          <!-- Image Thumbnail -->
          <div class="w-16 h-16 bg-gray-200 rounded-lg flex items-center justify-center flex-shrink-0">
            <img
              v-if="image.thumbnail"
              :src="image.thumbnail"
              :alt="image.filename"
              class="w-full h-full object-cover rounded-lg"
            />
            <i v-else class="fas fa-image text-2xl text-gray-400"></i>
          </div>

          <!-- Image Info -->
          <div class="flex-1 min-w-0">
            <div class="flex items-center justify-between">
              <h4 class="font-medium text-gray-900 truncate">
                {{ image.filename }}
              </h4>
              <status-badge :status="image.status" />
            </div>
            
            <div class="flex items-center space-x-4 mt-2 text-sm text-gray-500">
              <span class="flex items-center">
                <i class="fas fa-map-marker-alt mr-1"></i>
                {{ image.location }}
              </span>
              <span class="flex items-center">
                <i class="fas fa-clock mr-1"></i>
                {{ image.uploadTime }}
              </span>
            </div>
          </div>

          <!-- Actions -->
          <div class="flex items-center space-x-2">
            <button
              @click.stop="downloadImage(image)"
              class="p-2 text-gray-400 hover:text-gray-600 transition-colors"
              title="Télécharger"
            >
              <i class="fas fa-download"></i>
            </button>
            <button
              @click.stop="deleteImage(image)"
              class="p-2 text-gray-400 hover:text-red-600 transition-colors"
              title="Supprimer"
            >
              <i class="fas fa-trash"></i>
            </button>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="images.length === 0" class="text-center py-8">
        <i class="fas fa-images text-4xl text-gray-300 mb-4"></i>
        <p class="text-gray-500">Aucune image uploadée récemment</p>
      </div>
    </div>
  </div>
</template>

<script>
import StatusBadge from './StatusBadge.vue'

export default {
  name: 'RecentImages',
  components: {
    StatusBadge
  },
  props: {
    images: {
      type: Array,
      default: () => []
    }
  },
  emits: ['view-image', 'download-image', 'delete-image'],
  methods: {
    viewImage(image) {
      this.$emit('view-image', image);
    },
    downloadImage(image) {
      this.$emit('download-image', image);
    },
    deleteImage(image) {
      this.$emit('delete-image', image);
    }
  }
}
</script>