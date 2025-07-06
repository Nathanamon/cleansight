<template>
  <div class="flex min-h-screen bg-gray-100">
    <!-- Sidebar -->
    <Sidebar />

    <!-- Main Content -->
    <div class="flex-1 p-6 space-y-6 overflow-y-auto">
      <!-- Page Header -->
      <div class="flex justify-between items-center">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">Galerie d'Images</h1>
          <p class="text-gray-600 mt-1">Toutes les images uploadées des poubelles</p>
        </div>
        <div class="flex items-center space-x-4">
          <!-- <button
            @click="openUploadModal"
            class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            <i class="fas fa-upload mr-2"></i>
            Uploader des images
          </button> -->
          <div class="flex border border-gray-300 rounded-lg overflow-hidden">
            <button
              @click="viewMode = 'grid'"
              :class="[
                'px-3 py-2 text-sm',
                viewMode === 'grid' ? 'bg-blue-600 text-white' : 'bg-white text-gray-600 hover:bg-gray-50'
              ]"
            >
              <i class="fas fa-th"></i>
            </button>
            <button
              @click="viewMode = 'list'"
              :class="[
                'px-3 py-2 text-sm',
                viewMode === 'list' ? 'bg-blue-600 text-white' : 'bg-white text-gray-600 hover:bg-gray-50'
              ]"
            >
              <i class="fas fa-list"></i>
            </button>
          </div>
        </div>
      </div>

      <!-- Filters -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
        <div class="flex flex-wrap items-center gap-4">
          <!-- Search -->
          <div class="relative flex-1 min-w-64">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Rechercher par nom de fichier ou localisation..."
              class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
            <i class="fas fa-search absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400"></i>
          </div>

          <!-- Status Filter -->
          <select
            v-model="selectedStatus"
            class="border border-gray-300 rounded-lg px-3 py-2"
          >
            <option value="">Tous les statuts</option>
            <option value="pleine">Poubelles pleines</option>
            <option value="vide">Poubelles vides</option>
            <option value="maintenance">En maintenance</option>
          </select>

          <!-- Date Filter -->
          <input
            v-model="selectedDate"
            type="date"
            class="border border-gray-300 rounded-lg px-3 py-2"
          />

          <!-- Clear Filters -->
          <button
            @click="clearFilters"
            class="px-4 py-2 text-gray-600 hover:text-gray-800 transition-colors"
          >
            <i class="fas fa-times mr-1"></i>
            Effacer les filtres
          </button>
        </div>
      </div>

      <!-- Empty state -->
      <div v-if="totalImages === 0" class="text-center text-gray-500 py-10">
        Aucune image disponible pour le moment.
      </div>

      <!-- Grid View -->
      <div v-if="viewMode === 'grid' && totalImages > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        <div
          v-for="image in paginatedImages"
          :key="image.id"
          class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-md transition-shadow cursor-pointer group"
          @click="openImageModal(image)"
        >
          <!-- Image avec overlay -->
          <div class="relative aspect-w-16 aspect-h-12 bg-gray-200 group">
            <img
              v-if="image.thumbnail"
              :src="image.thumbnail"
              :alt="image.filename"
              class="w-full h-48 object-cover"
            />
            <div v-else class="w-full h-48 flex items-center justify-center bg-gray-100">
              <i class="fas fa-image text-4xl text-gray-400"></i>
            </div>

            <!-- Overlay -->
            <div class="absolute inset-0 bg-black/60 text-white p-4 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex flex-col justify-center text-sm">
              <div class="flex items-center mb-1">
                <i class="fas fa-map-marker-alt w-4 mr-2"></i>
                {{ image.location }}
              </div>
              <div class="flex items-center mb-1">
                <i class="fas fa-calendar w-4 mr-2"></i>
                {{ formatDate(image.uploadDate) }}
              </div>
              <div class="flex items-center">
                <i class="fas fa-file-image w-4 mr-2"></i>
                {{ image.size }}
              </div>
            </div>
          </div>

          <!-- Image Info -->
          <div class="p-4">
            <div class="flex items-center justify-between mb-2">
              <h3 class="font-medium text-gray-900 truncate">{{ image.filename }}</h3>
              <status-badge :status="image.status" size="xs" />
            </div>

            <!-- Actions -->
            <div class="flex items-center justify-between mt-4 pt-4 border-t border-gray-100">
              <button
                @click.stop="downloadImage(image)"
                class="text-blue-600 hover:text-blue-700 text-sm font-medium"
              >
                <i class="fas fa-download mr-1"></i>
                Télécharger
              </button>
              <button
                @click.stop="markAsEmpty(image)"
                class="text-green-600 hover:text-green-700 text-sm font-medium"
              >
                <i class="fas fa-check mr-1"></i>
                Marquer vidée
              </button>
              <button
                @click.stop="deleteImage(image)"
                class="text-red-600 hover:text-red-700 text-sm font-medium"
              >
                <i class="fas fa-trash mr-1"></i>
                Supprimer
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Pagination -->
      <div v-if="totalImages > 0" class="flex items-center justify-between">
        <div class="text-sm text-gray-500">
          Affichage de {{ startIndex + 1 }} à {{ endIndex }} sur {{ totalImages }} images
        </div>
        <div class="flex items-center space-x-2">
          <button
            @click="previousPage"
            :disabled="currentPage === 1"
            class="px-3 py-2 border border-gray-300 rounded-md text-sm text-gray-500 hover:text-gray-700 disabled:opacity-50"
          >
            <i class="fas fa-chevron-left"></i>
          </button>
          <span class="text-sm text-gray-700">
            Page {{ currentPage }} sur {{ totalPages }}
          </span>
          <button
            @click="nextPage"
            :disabled="currentPage === totalPages"
            class="px-3 py-2 border border-gray-300 rounded-md text-sm text-gray-500 hover:text-gray-700 disabled:opacity-50"
          >
            <i class="fas fa-chevron-right"></i>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import Sidebar from '../components/Sidebar.vue'
import StatusBadge from '../components/StatusBadge.vue'
import { useAuthStore } from '@/stores/auth'

export default {
  name: 'Images',
  components: {
    Sidebar,
    StatusBadge
  },
  data() {
    return {
      viewMode: 'grid',
      searchQuery: '',
      selectedStatus: '',
      selectedDate: '',
      currentPage: 1,
      itemsPerPage: 12,
      images: [], // This will be populated with images from the backend
    }
  },
  computed: {
    filteredImages() {
      let filtered = this.images;
      if (this.searchQuery) {
        filtered = filtered.filter(image =>
          image.filename.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          image.location.toLowerCase().includes(this.searchQuery.toLowerCase())
        );
      }
      if (this.selectedStatus) {
        filtered = filtered.filter(image => image.status === this.selectedStatus);
      }
      if (this.selectedDate) {
        filtered = filtered.filter(image =>
          image.uploadDate.startsWith(this.selectedDate)
        );
      }
      return filtered;
    },
    totalImages() {
      return this.filteredImages.length;
    },
    totalPages() {
      return Math.ceil(this.totalImages / this.itemsPerPage);
    },
    startIndex() {
      return (this.currentPage - 1) * this.itemsPerPage;
    },
    endIndex() {
      return Math.min(this.startIndex + this.itemsPerPage, this.totalImages);
    },
    paginatedImages() {
      return this.filteredImages.slice(this.startIndex, this.endIndex);
    }
  },
  async mounted() {
    await this.loadImages()
  },
  methods: {
    async loadImages() {
      try {
        const res = await fetch(import.meta.env.VITE_API_URL + '/images', {
          credentials: 'include'
        })
        if (res.ok) {
          const data = await res.json()
          console.log('Images chargées:', data)
          this.images = data.map(img => ({
            id: img.id,
            filename: img.filename,
            status: img.annotation,
            location: 'Paris',
            uploadDate: img.date_upload,
            size: img.taille ? `${(img.taille / 1024).toFixed(0)} KB` : '',
            thumbnail: `${import.meta.env.VITE_API_URL}/uploads/${img.filename}`
          }))
        }
      } catch (e) {
        console.error('Erreur chargement images:', e)
      }
    },
    openUploadModal() {
      console.log('Ouvrir modal d\'upload');
    },
    openImageModal(image) {
      console.log('Ouvrir modal d\'image:', image);
    },
    downloadImage(image) {
      console.log('Télécharger image:', image);
    },
    async markAsEmpty(image) {
      const auth = useAuthStore()
      const headers = {
        'Content-Type': 'application/json'
      }
      if (auth.csrfToken) {
        headers['X-CSRF-Token'] = auth.csrfToken
      }

      try {
        const res = await fetch(
          `${import.meta.env.VITE_API_URL}/images/${image.id}`,
          {
            method: 'PATCH',
            credentials: 'include',
            headers,
            body: JSON.stringify({ annotation: 'vide' })
          }
        )
        if (res.ok) {
          image.status = 'vide'
        } else {
          console.error('Erreur mise à jour image:', res.status)
        }
      } catch (e) {
        console.error('Erreur mise à jour image:', e)
      }
    },
    async deleteImage(image) {
      if (!confirm("Êtes-vous sûr de vouloir supprimer cette image ?")) {
        return
      }

      const auth = useAuthStore()
      const headers = {}
      if (auth.csrfToken) {
        headers['X-CSRF-Token'] = auth.csrfToken
      }

      try {
        const res = await fetch(
          `${import.meta.env.VITE_API_URL}/images/${image.id}`,
          {
            method: 'DELETE',
            credentials: 'include',
            headers
          }
        )
        if (res.ok) {
          const index = this.images.findIndex(img => img.id === image.id)
          if (index > -1) this.images.splice(index, 1)
        } else {
          console.error('Erreur suppression image:', res.status)
        }
      } catch (e) {
        console.error('Erreur suppression image:', e)
      }
    },
    clearFilters() {
      this.searchQuery = '';
      this.selectedStatus = '';
      this.selectedDate = '';
      this.currentPage = 1;
    },
    nextPage() {
      if (this.currentPage < this.totalPages) this.currentPage++;
    },
    previousPage() {
      if (this.currentPage > 1) this.currentPage--;
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleString('fr-FR');
    }
  },
  watch: {
    filteredImages() {
      this.currentPage = 1;
    }
  }
}
</script>