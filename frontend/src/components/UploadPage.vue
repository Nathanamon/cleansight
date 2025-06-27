<template>
  <div class="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-2xl mx-auto">
      <h2 class="text-2xl font-bold text-gray-800 mb-6 text-center">
        Téléversement d'une image de poubelle
      </h2>
      <ImageUpload />
    </div>
  </div>
</template>

<script setup>
import ImageUpload from './ImageUpload.vue'
</script>
