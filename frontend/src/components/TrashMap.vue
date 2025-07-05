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
      <span><span class="inline-block w-3 h-3 rounded-full mr-2" style="background:#5DBB4E"></span>Vide</span>
      <span><span class="inline-block w-3 h-3 rounded-full mr-2" style="background:#F77F38"></span>Pleine</span>
      <span><span class="inline-block w-3 h-3 rounded-full mr-2" style="background:#E3342F"></span>Débordante</span>
    </div>
  </div>
</template>

<script setup>
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



// Constantes Leaflet
const tileUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
const tileAttribution = '&copy; OpenStreetMap contributors'

// Couleurs selon état
const getColor = (etat) => {
  if (etat === 'vide') return '#5DBB4E'
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
