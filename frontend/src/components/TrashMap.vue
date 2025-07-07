<!-- src/components/TrashMap.vue -->
<template>
  <div>
    <l-map :zoom="zoom" :center="center" style="height: 60vh; width: 100%;">
      <l-tile-layer :url="tileUrl" :attribution="tileAttribution" />

      <l-marker
        v-for="p in poubelles"
        :key="p.id"
        :lat-lng="[p.latitude, p.longitude]"
        :icon="getIcon(p.etat)"
      >
        <l-popup>
          <div class="text-sm">
            <p><strong>ID :</strong> {{ p.id }}</p>
            <p><strong>État :</strong> {{ p.etat }}</p>
            <p><strong>Adresse :</strong> {{ p.address || 'Adresse inconnue' }}</p>
            <p><strong>Heure :</strong> {{ formatDate(p.timestamp) }}</p>
            <button
              class="mt-2 bg-green-600 text-white px-3 py-1 rounded text-xs"
              @click="markAsEmpty(p)"
            >
              Marquer vidée
            </button>
          </div>
        </l-popup>

        <l-circle
          v-if="p.etat === 'débordante'"
          :lat-lng="[p.latitude, p.longitude]"
          :radius="100"
          color="#E3342F"
          fill-color="#E3342F"
          :fill-opacity="0.3"
        />
      </l-marker>
    </l-map>

    <div class="mt-6 flex justify-center gap-6 text-sm font-medium text-gray-700">
      <span><span class="inline-block w-3 h-3 rounded-full mr-2" style="background:#F77F38"></span>Pleine</span>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import { LMap, LTileLayer, LMarker, LPopup, LCircle } from '@vue-leaflet/vue-leaflet'
import L from 'leaflet'
import { computed } from 'vue'
import { toRefs } from 'vue'

// Props
const props = defineProps({
  poubelles: {
    type: Array,
    required: true
  },
  center: {
    type: Array,
    default: () => [48.8566, 2.3522]
  },
  zoom: {
    type: Number,
    default: 14
  }
})

const { poubelles, center, zoom } = toRefs(props)
const emit = defineEmits(['bin-emptied'])
const auth = useAuthStore()

async function markAsEmpty(bin) {
  const headers = { 'Content-Type': 'application/json' }
  if (auth.csrfToken) headers['X-CSRF-Token'] = auth.csrfToken

  try {
    const res = await fetch(`${import.meta.env.VITE_API_URL}/images/${bin.id}`, {
      method: 'PATCH',
      credentials: 'same-origin',
      headers,
      body: JSON.stringify({ annotation: 'vidée' })
    })
    if (res.ok) {
      emit('bin-emptied', bin.id)
    } else {
      console.error('Erreur mise à jour:', res.status)
    }
  } catch (e) {
    console.error('Erreur réseau:', e)
  }
}




// Constantes Leaflet
const tileUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
const tileAttribution = '&copy; OpenStreetMap contributors'

// Couleurs selon état
const getColor = (etat) => {
  if (etat === 'vide' || etat === 'vidée') return '#5DBB4E'
  if (etat === 'pleine') return '#F77F38'
  if (etat === 'débordante') return '#E3342F'
  return 'gray'
}

const getIcon = (etat) =>
  new L.DivIcon({
    className: '',
    html: `<div style="background:${getColor(etat)};width:20px;height:20px;border-radius:50%;border:2px solid white;"></div>`,
  })

const formatDate = (ts) => new Date(ts).toLocaleString()
</script>
