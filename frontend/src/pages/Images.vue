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
            <option value="vidée">Poubelles vidées</option>
            <!-- <option value="maintenance">En maintenance</option> -->
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
              class="w-full h-72 object-contain bg-white"

            />
            <div v-else class="w-full h-72 flex items-center justify-center bg-gray-100">
              <i class="fas fa-image text-4xl text-gray-400"></i>
            </div>

<!-- Overlay amélioré -->
<div
  class="absolute inset-0 bg-black/70 text-white px-4 py-4 opacity-0 group-hover:opacity-100 group-hover:translate-y-0 translate-y-2 transition-all duration-300 text-sm flex flex-col justify-between"
>
  <!-- Haut : Informations générales -->
  <div class="space-y-1">
    <div class="truncate">
      <i class="fas fa-map-marker-alt mr-2 text-gray-300"></i>
      {{ image.location }}
    </div>
    <div>
      <i class="fas fa-calendar-alt mr-2 text-gray-300"></i>
      {{ formatDate(image.uploadDate) }}
    </div>
    <div v-if="image.size">
      <i class="fas fa-file-image mr-2 text-gray-300"></i>
      {{ image.size }}
    </div>
  </div>

  <!-- Bas : Météo -->
  <div class="pt-3 mt-3 border-t border-white/20 text-xs space-y-1 leading-snug">
    <div class="flex items-center gap-1">
  <span class="text-lg">{{ getWeatherIcon(image.weather.description) }}</span>
  <span class="capitalize">{{ image.weather.description }}</span>
</div>
    <div v-if="image.weather.temperature !== null" class="flex items-center gap-1">
      <i class="fas fa-thermometer-half text-gray-300"></i>
      {{ image.weather.temperature.toFixed(1) }}°C
    </div>
    <div v-if="image.weather.humidity !== null" class="flex items-center gap-1">
      <i class="fas fa-tint text-gray-300"></i>
      {{ image.weather.humidity }}% humidité
    </div>
    <div v-if="image.weather.wind !== null" class="flex items-center gap-1">
      <i class="fas fa-wind text-gray-300"></i>
      {{ image.weather.wind }} km/h vent
    </div>
  </div>
</div>

          </div>

          <!-- Image Info -->
          <div class="p-4">
            <div class="flex items-center justify-between mb-2">
              <h3 class="font-medium text-gray-900 truncate">{{ image.filename }}</h3>
              <StatusBadge :status="image.status" size="xs" />
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


<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import Sidebar from '../components/Sidebar.vue'
import StatusBadge from '../components/StatusBadge.vue'
import { useAuthStore } from '@/stores/auth'

const viewMode = ref('grid')
const searchQuery = ref('')
const selectedStatus = ref('')
const selectedDate = ref('')
const currentPage = ref(1)
const itemsPerPage = 12
const images = ref([])
const auth = useAuthStore()

function formatAddress(address) {
  if (!address || typeof address !== 'string') return 'Adresse inconnue'

  const parts = address.split(',').map(p => p.trim())
  
  // Recherche du code postal (5 chiffres)
  const postalMatch = parts.find(p => /\b\d{5}\b/.test(p))
  const postalCode = postalMatch || ''
  
  // Recherche d’un nom de rue (généralement au début)
  const street = parts[0] || ''

  // Ajoute un arrondissement si présent
  const arrondissement = parts.find(p => /Paris\s?\d{1,2}e/.test(p)) || ''

  // Construire une version courte
  if (postalCode && street) {
    return `${street}, ${postalCode} ${arrondissement || ''}`.trim()
  }

  // Fallback
  return address
}

function getWeatherIcon(description) {
  if (!description) return '❓'
  const d = description.toLowerCase()

  if (d.includes('soleil') || d.includes('ensoleillé')) return '☀️'
  if (d.includes('nuage')) return '☁️'
  if (d.includes('pluie') || d.includes('pluvieux')) return '🌧️'
  if (d.includes('averse') || d.includes('pluvieux')) return '🌧️'
  if (d.includes('orage') || d.includes('tonnerre')) return '🌩️'
  if (d.includes('neige')) return '❄️'
  if (d.includes('brume') || d.includes('brouillard')) return '🌫️'
  if (d.includes('vent')) return '💨'

  return '🌈' // défaut sympa
}

async function loadImages() {
  try {
    const headers = {}
    if (auth.csrfToken) {
      headers['X-CSRF-Token'] = auth.csrfToken
    }
    const res = await fetch(`${import.meta.env.VITE_API_URL}/images`, {
      credentials: 'include',
      headers
    })
    
    if (res.ok) {
      const data = await res.json()
      console.log('Images reçues depuis l’API :', data)
      images.value = data.map(img => ({
  id: img.id,
  filename: img.filename,
  status: img.annotation,
  location: formatAddress(img.metadata?.location?.address),
  uploadDate: img.date_upload,
  size: img.taille ? `${(img.taille / 1024).toFixed(0)} KB` : '',
  thumbnail: `${import.meta.env.VITE_API_URL}/uploads/${encodeURIComponent(img.filename)}`,
  weather: img.metadata?.weather
    ? {
        description: img.metadata.weather.description || 'Inconnu',
        temperature: img.metadata.weather.temperature ?? null,
        humidity: img.metadata.weather.humidity ?? null,
        wind: img.metadata.weather.wind_speed ?? null
      }
    : {
        description: 'Inconnu',
        temperature: null,
        humidity: null,
        wind: null
      }
}))
    }
  } catch (e) {
    console.error('Erreur chargement images:', e)
  }
}
function openUploadModal() {
  console.log("Ouvrir modal d'upload")
}
function openImageModal(image) {
  console.log("Ouvrir modal d'image:", image)
}
function downloadImage(image) {
  console.log('Télécharger image:', image)
}


async function deleteImage(image) {
  if (!confirm("Êtes-vous sûr de vouloir supprimer cette image ?")) return

  const headers = {}
  if (auth.csrfToken) {
    headers['X-CSRF-Token'] = auth.csrfToken
  }
  try {
    const res = await fetch(`${import.meta.env.VITE_API_URL}/images/${image.id}`, {
      method: 'DELETE',
      credentials: 'include',
      headers
    })
    if (res.ok) {
      const index = images.value.findIndex(img => img.id === image.id)
      if (index > -1) images.value.splice(index, 1)
    } else {
      console.error('Erreur suppression image:', res.status)
    }
  } catch (e) {
    console.error('Erreur suppression image:', e)
  }
}

function clearFilters() {
  searchQuery.value = ''
  selectedStatus.value = ''
  selectedDate.value = ''
  currentPage.value = 1
}

function nextPage() {
  if (currentPage.value < totalPages.value) currentPage.value++
}
function previousPage() {
  if (currentPage.value > 1) currentPage.value--
}
function formatDate(dateString) {
  return new Date(dateString).toLocaleString('fr-FR')
}

const filteredImages = computed(() => {
  let filtered = images.value
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    filtered = filtered.filter(img =>
      img.filename.toLowerCase().includes(q) ||
      img.location.toLowerCase().includes(q)
    )
  }
  if (selectedStatus.value) {
    filtered = filtered.filter(img => img.status === selectedStatus.value)
  }
  if (selectedDate.value) {
    filtered = filtered.filter(img => img.uploadDate.startsWith(selectedDate.value))
  }
  return filtered
})

const totalImages = computed(() => filteredImages.value.length)
const totalPages = computed(() => Math.ceil(totalImages.value / itemsPerPage))
const startIndex = computed(() => (currentPage.value - 1) * itemsPerPage)
const endIndex = computed(() => Math.min(startIndex.value + itemsPerPage, totalImages.value))
const paginatedImages = computed(() => filteredImages.value.slice(startIndex.value, endIndex.value))

watch(filteredImages, () => {
  currentPage.value = 1
})

onMounted(() => {
  if (auth.restoreFromLocalStorage) auth.restoreFromLocalStorage()
  loadImages()
})
</script>