<template>
  <div class="flex min-h-screen bg-gray-100">
    <!-- Sidebar -->
    <Sidebar />

    <!-- Main Content -->
    <div class="flex-1 p-6 space-y-6 overflow-y-auto">
      <!-- ... tout le contenu existant ici ... -->
      <!-- Page Header -->
      <div class="flex justify-between items-center">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">Galerie d'Images</h1>
          <p class="text-gray-600 mt-1">Toutes les images uploadées des poubelles</p>
        </div>
        <div class="flex items-center space-x-4">
          <button
            @click="openUploadModal"
            class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            <i class="fas fa-upload mr-2"></i>
            Uploader des images
          </button>
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

    <!-- Images Grid/List -->
    <div v-if="viewMode === 'grid'" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      <div
        v-for="image in filteredImages"
        :key="image.id"
        class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-md transition-shadow cursor-pointer"
        @click="openImageModal(image)"
      >
        <!-- Image -->
        <div class="aspect-w-16 aspect-h-12 bg-gray-200">
          <img
            v-if="image.thumbnail"
            :src="image.thumbnail"
            :alt="image.filename"
            class="w-full h-48 object-cover"
          />
          <div v-else class="w-full h-48 flex items-center justify-center bg-gray-100">
            <i class="fas fa-image text-4xl text-gray-400"></i>
          </div>
        </div>
        
        <!-- Image Info -->
        <div class="p-4">
          <div class="flex items-center justify-between mb-2">
            <h3 class="font-medium text-gray-900 truncate">{{ image.filename }}</h3>
            <status-badge :status="image.status" size="xs" />
          </div>
          
          <div class="space-y-1 text-sm text-gray-500">
            <div class="flex items-center">
              <i class="fas fa-map-marker-alt w-4 mr-2"></i>
              {{ image.location }}
            </div>
            <div class="flex items-center">
              <i class="fas fa-calendar w-4 mr-2"></i>
              {{ formatDate(image.uploadDate) }}
            </div>
            <div class="flex items-center">
              <i class="fas fa-file-image w-4 mr-2"></i>
              {{ image.size }}
            </div>
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

    <!-- List View -->
    <div v-else class="bg-white rounded-xl shadow-sm border border-gray-100">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Image
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Statut
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Localisation
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Date
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Taille
              </th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr
              v-for="image in filteredImages"
              :key="image.id"
              class="hover:bg-gray-50 cursor-pointer"
              @click="openImageModal(image)"
            >
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="w-12 h-12 bg-gray-200 rounded-lg flex items-center justify-center mr-4">
                    <img
                      v-if="image.thumbnail"
                      :src="image.thumbnail"
                      :alt="image.filename"
                      class="w-full h-full object-cover rounded-lg"
                    />
                    <i v-else class="fas fa-image text-gray-400"></i>
                  </div>
                  <div>
                    <div class="text-sm font-medium text-gray-900">{{ image.filename }}</div>
                    <div class="text-sm text-gray-500">{{ image.id }}</div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <status-badge :status="image.status" />
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {{ image.location }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ formatDate(image.uploadDate) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ image.size }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <button
                  @click.stop="downloadImage(image)"
                  class="text-blue-600 hover:text-blue-900 mr-4"
                >
                  <i class="fas fa-download"></i>
                </button>
                <button
                  @click.stop="deleteImage(image)"
                  class="text-red-600 hover:text-red-900"
                >
                  <i class="fas fa-trash"></i>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Pagination -->
    <div class="flex items-center justify-between">
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
      images: [
        {
          id: 1,
          filename: 'poubelle_001.jpg',
          status: 'pleine',
          location: '15ème arrondissement',
          uploadDate: '2025-07-02T10:30:00',
          size: '2.3 MB',
          thumbnail: null
        },
        {
          id: 2,
          filename: 'poubelle_002.jpg',
          status: 'vide',
          location: '7ème arrondissement',
          uploadDate: '2025-07-02T09:15:00',
          size: '1.8 MB',
          thumbnail: null
        },
        {
          id: 3,
          filename: 'poubelle_003.jpg',
          status: 'pleine',
          location: '11ème arrondissement',
          uploadDate: '2025-07-02T08:45:00',
          size: '2.1 MB',
          thumbnail: null
        },
        {
          id: 4,
          filename: 'poubelle_004.jpg',
          status: 'vide',
          location: '3ème arrondissement',
          uploadDate: '2025-07-01T16:20:00',
          size: '1.9 MB',
          thumbnail: null
        },
        {
          id: 5,
          filename: 'poubelle_005.jpg',
          status: 'maintenance',
          location: '16ème arrondissement',
          uploadDate: '2025-07-01T14:10:00',
          size: '2.0 MB',
          thumbnail: null
        }
      ]
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
  methods: {
    openUploadModal() {
      console.log('Ouvrir modal d\'upload');
    },
    openImageModal(image) {
      console.log('Ouvrir modal d\'image:', image);
    },
    downloadImage(image) {
      console.log('Télécharger image:', image);
    },
    deleteImage(image) {
      if (confirm('Êtes-vous sûr de vouloir supprimer cette image ?')) {
        const index = this.images.findIndex(img => img.id === image.id);
        if (index > -1) this.images.splice(index, 1);
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