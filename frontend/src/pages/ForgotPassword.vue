<template>
  <div class="min-h-screen bg-gradient-to-br from-green-50 via-white to-emerald-50 flex items-center justify-center p-4">
    <div class="bg-white rounded-3xl shadow-2xl p-8 w-full max-w-md border border-green-100 relative overflow-hidden">
      
      <!-- Décorations -->
      <div class="absolute top-0 right-0 w-32 h-32 bg-gradient-to-bl from-green-100 to-transparent rounded-full -translate-y-16 translate-x-16 opacity-50"></div>
      <div class="absolute bottom-0 left-0 w-24 h-24 bg-gradient-to-tr from-emerald-100 to-transparent rounded-full translate-y-12 -translate-x-12 opacity-50"></div>
      
      <!-- Logo -->
      <div class="w-30 h-30 mx-auto mb-4 rounded-2xl overflow-hidden shadow-lg">
        <img src="../assets/logo.png" alt="CleanSight Logo" class="w-full h-full object-cover"/>
      </div>

      <!-- Titre et description -->
      <div class="text-center mb-8">
        <h2 class="text-2xl font-bold text-gray-800 mb-3">Mot de passe oublié</h2>
        <p class="text-gray-600 text-sm leading-relaxed">
          Entrez votre adresse email et nous vous enverrons un lien pour réinitialiser votre mot de passe.
        </p>
      </div>

      <!-- Formulaire -->
      <form @submit.prevent="sendResetLink" class="space-y-6">
        <!-- Email -->
        <div class="space-y-2">
          <label class="block text-sm font-medium text-gray-700">Adresse email</label>
          <div class="relative">
            <input
              v-model="email"
              type="email"
              required
              placeholder="votre@email.com"
              class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-green-500 transition-all duration-200 pl-11"
            />
            <svg class="absolute left-3 top-3.5 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207"/>
            </svg>
          </div>
        </div>

        <!-- Bouton d'envoi -->
        <button
          type="submit"
          :disabled="loading"
          class="w-full bg-gradient-to-r from-green-600 to-emerald-600 text-white py-3 px-4 rounded-xl font-semibold hover:from-green-700 hover:to-emerald-700 transform hover:scale-[1.02] transition-all duration-200 shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <span v-if="loading" class="flex items-center justify-center">
            <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Envoi en cours...
          </span>
          <span v-else class="flex items-center justify-center">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
            </svg>
            Envoyer le lien
          </span>
        </button>
      </form>

      <!-- Messages -->
      <div v-if="message" class="mt-6">
        <div :class="[
          'p-4 rounded-xl text-sm font-medium text-center transition-all duration-300',
          messageType === 'success' 
            ? 'bg-green-50 text-green-700 border border-green-200' 
            : 'bg-red-50 text-red-700 border border-red-200'
        ]">
          <div class="flex items-center justify-center">
            <svg v-if="messageType === 'success'" class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
            </svg>
            <svg v-else class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
            </svg>
            {{ message }}
          </div>
        </div>
      </div>

      <!-- Retour à la connexion -->
      <div class="mt-6 text-center">
        <button
          @click="goToLogin"
          class="text-green-600 hover:text-green-700 font-medium transition-colors duration-200 text-sm flex items-center justify-center mx-auto group"
        >
          <svg class="w-4 h-4 mr-2 transform group-hover:-translate-x-1 transition-transform duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
          </svg>
          Retour à la connexion
        </button>
      </div>

      <!-- Informations supplémentaires -->
      <div class="mt-8 p-4 bg-blue-50 rounded-xl border border-blue-100">
        <div class="flex items-start">
          <svg class="w-5 h-5 text-blue-500 mt-0.5 mr-3 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"/>
          </svg>
          <div>
            <p class="text-sm text-blue-700 font-medium mb-1">Besoin d'aide ?</p>
            <p class="text-xs text-blue-600 leading-relaxed">
              Si vous ne recevez pas l'email, vérifiez vos spams ou contactez notre support.
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const email = ref('')
const loading = ref(false)
const message = ref('')
const messageType = ref('success') // 'success' ou 'error'

async function sendResetLink() {
  loading.value = true
  message.value = ''
  
  try {
    const res = await fetch(`${import.meta.env.VITE_API_URL}/auth/forgot-password`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: email.value })
    })
    
    if (res.ok) {
      message.value = 'Un lien de réinitialisation a été envoyé à votre adresse email !'
      messageType.value = 'success'
      // Optionnel : vider le champ email après succès
      email.value = ''
    } else {
      const err = await res.json()
      message.value = err.error || 'Échec de l\'envoi. Veuillez réessayer.'
      messageType.value = 'error'
    }
  } catch (error) {
    message.value = 'Erreur réseau. Vérifiez votre connexion et réessayez.'
    messageType.value = 'error'
  } finally {
    loading.value = false
  }
}

function goToLogin() {
  router.push('/login')
}
</script>