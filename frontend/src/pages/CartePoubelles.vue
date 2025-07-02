<template>
  <div class="px-4 py-6 mt-24">
    <h2 class="text-3xl font-bold text-center mb-6 text-[#357A38]">Localisation des poubelles</h2>

    <l-map :zoom="14" :center="[48.8566, 2.3522]" style="height: 60vh; width: 100%;">
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

    <!-- Légende -->
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

// Tu peux remplacer ceci par une API plus tard
const poubelles = [
  {
    id: 1,
    latitude: 48.8566,
    longitude: 2.3522,
    etat: 'vide',
    timestamp: '2025-06-30T12:00:00Z',
  },
  {
    id: 2,
    latitude: 48.857,
    longitude: 2.355,
    etat: 'pleine',
    timestamp: '2025-06-30T12:05:00Z',
  },
  {
    id: 3,
    latitude: 48.854,
    longitude: 2.35,
    etat: 'débordante',
    timestamp: '2025-06-30T12:10:00Z',
  },
]

const tileUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
const tileAttribution = '&copy; OpenStreetMap contributors'

const getColor = (etat) => {
  if (etat === 'vide') return '#5DBB4E'       // vert clair CleanSight
  if (etat === 'pleine') return '#F77F38'     // orange toit
  if (etat === 'débordante') return '#E3342F' // vert foncé
  return 'gray'
}

const getIcon = (etat) =>
  new L.DivIcon({
    className: '',
    html: `<div style="background:${getColor(etat)};width:20px;height:20px;border-radius:50%;border:2px solid white;"></div>`,
  })

const formatDate = (ts) => new Date(ts).toLocaleString()
</script>

<style scoped>
/* Ajout futur si besoin */
</style>
