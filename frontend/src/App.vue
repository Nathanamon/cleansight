<script setup>
import Header from './components/Header.vue'
import Footer from './components/Footer.vue'
import { useRoute } from 'vue-router'

const route = useRoute()

// Désactiver le padding pour certaines routes (ex : page de connexion)
const noPaddingRoutes = ['/login']
const shouldApplyPadding = !noPaddingRoutes.includes(route.path)
</script>

<template>
  <div>
    <Header />

    <!-- wrapper global avec padding conditionnel -->
    <div :class="shouldApplyPadding ? 'pt-24' : ''">
      <router-view />
    </div>
    <Footer />
  </div>
</template>
