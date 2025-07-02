<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-white to-green-50 pt-36 pb-8 px-4 sm:px-6 lg:px-8">
    <div class="max-w-3xl mx-auto">
      <!-- Header avec icône -->
      <div class="text-center mb-12">
        <div class="mx-auto w-16 h-16 bg-gradient-to-r from-green-400 to-blue-500 rounded-full flex items-center justify-center mb-6 shadow-lg">
          <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
          </svg>
        </div>
        <h1 class="text-4xl font-bold text-gray-900 mb-4">
          Analyse de Poubelle
        </h1>
        <p class="text-lg text-gray-600 max-w-2xl mx-auto leading-relaxed">
          Téléversez une image de votre poubelle pour une analyse intelligente et des recommandations personnalisées
        </p>
      </div>

      <!-- Carte principale -->
      <div class="bg-white rounded-2xl shadow-xl border border-gray-100 overflow-hidden">
        <div class="bg-gradient-to-r from-green-500 to-blue-600 px-8 py-6">
          <h2 class="text-xl font-semibold text-white flex items-center">
            <svg class="w-6 h-6 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
            </svg>
            Téléverser votre image
          </h2>
          <p class="text-green-100 text-sm mt-2">
            Formats supportés : JPG, PNG, WebP • Taille max : 10MB
          </p>
        </div>
        
        <div class="p-8">
          <ImageUpload />
        </div>
      </div>

      <!-- Section d'informations -->
      <div class="mt-12 grid md:grid-cols-3 gap-6">
        <div class="bg-white rounded-xl p-6 shadow-lg border border-gray-100 hover:shadow-xl transition-shadow duration-300">
          <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
            <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
          <h3 class="font-semibold text-gray-900 mb-2">Analyse Rapide</h3>
          <p class="text-gray-600 text-sm">Identification automatique des déchets en quelques secondes</p>
        </div>

        <div class="bg-white rounded-xl p-6 shadow-lg border border-gray-100 hover:shadow-xl transition-shadow duration-300">
          <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
            <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
            </svg>
          </div>
          <h3 class="font-semibold text-gray-900 mb-2">IA Avancée</h3>
          <p class="text-gray-600 text-sm">Technologie de reconnaissance d'image de pointe</p>
        </div>

        <div class="bg-white rounded-xl p-6 shadow-lg border border-gray-100 hover:shadow-xl transition-shadow duration-300">
          <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
            <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
            </svg>
          </div>
          <h3 class="font-semibold text-gray-900 mb-2">Conseils Experts</h3>
          <p class="text-gray-600 text-sm">Recommandations personnalisées pour optimiser vos déchets</p>
        </div>
      </div>

      <!-- Footer -->
      <div class="mt-16 text-center">
        <p class="text-gray-500 text-sm">
          Votre vie privée est protégée • Les images sont traitées de manière sécurisée
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import ImageUpload from '../components/ImageUpload.vue'
</script>