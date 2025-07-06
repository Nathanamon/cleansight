<template>
  <div class="space-y-6">
    <!-- Popup de confirmation -->
    <transition name="popup">
      <div
        v-if="showValidationPopup"
        class="fixed inset-0 backdrop-blur-sm bg-white bg-opacity-10 flex items-center justify-center z-50"
        @click="showValidationPopup = false"
      >
        <div 
          class="bg-white rounded-lg p-6 max-w-sm mx-4 shadow-2xl border transform transition-all duration-300"
          @click.stop
        >
          <div class="flex items-center justify-center mb-4">
            <svg class="w-12 h-12 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-center mb-2">Image enregistrée !</h3>
          <p class="text-gray-600 text-center mb-4">Votre image a été validée et enregistrée avec succès.</p>
          <button
            @click="showValidationPopup = false"
            class="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition"
          >
            OK
          </button>
        </div>
      </div>
    </transition>

    <!-- Étape 1 : Zone de téléchargement -->
    <div v-if="!prediction">
      <div
        @dragover.prevent
        @drop.prevent="handleDrop"
        class="border-2 border-dashed border-gray-300 rounded-xl flex flex-col items-center justify-center p-8 text-gray-500 hover:border-blue-400 hover:bg-blue-50 transition cursor-pointer"
        @click="$refs.fileInput.click()"
      >
        <input type="file" accept="image/*" ref="fileInput" @change="onFileChange" class="hidden" />
        <svg class="w-10 h-10 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 15.75V19.5A1.5 1.5 0 004.5 21h15a1.5 1.5 0 001.5-1.5v-3.75M16.5 10.5L12 6m0 0L7.5 10.5M12 6v12" />
        </svg>
        <p class="text-sm text-center">Glissez une image ici ou cliquez pour sélectionner</p>
      </div>
      <div v-if="preview" class="mt-4">
        <img :src="preview" class="max-h-64 w-full object-contain border rounded" />
        <button @click="predict" class="mt-4 w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">
          Analyser automatiquement
        </button>
      </div>
    </div>

    <!-- Étape 2 : Annotation prédite + modification -->
    <div v-else>
      <img :src="preview" class="max-h-64 w-full object-contain border rounded mb-4" />

      <div class="text-center">
        <p class="text-sm text-gray-500">Annotation automatique :</p>
        <span
          class="inline-block px-3 py-1 rounded-full text-white"
          :class="prediction === 'pleine' ? 'bg-red-500' : 'bg-green-500'"
        >
          {{ prediction }}
        </span>
      </div>

      <div class="flex justify-center gap-4 mt-4">
        <label><input type="radio" value="pleine" v-model="annotation" /> Pleine</label>
        <label><input type="radio" value="vide" v-model="annotation" /> Vide</label>
      </div>

      <button
        @click="validate"
        class="mt-6 w-full bg-green-600 text-white py-2 rounded hover:bg-green-700"
        :disabled="loading"
      >
        Valider et enregistrer
      </button>

      <p v-if="message" class="mt-2 text-center text-sm text-gray-600">{{ message }}</p>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import { ref, onMounted, watch } from 'vue'


onMounted(() => {
  auth.restoreFromLocalStorage()
})


function getCookie(name) {
  return document.cookie
    .split('; ')
    .find(c => c.startsWith(name + '='))?.split('=')[1] || null
}

const auth = useAuthStore()
const preview = ref(null)
const fichier = ref(null)
const prediction = ref(null)
const annotation = ref(null)
const loading = ref(false)
const message = ref('')
const fileInput = ref(null)
const showValidationPopup = ref(false)

function onFileChange(e) {
  fichier.value = e.target.files[0]
  preview.value = URL.createObjectURL(fichier.value)
  prediction.value = null
  annotation.value = null
  message.value = ''
}

function handleDrop(e) {
  const dropped = e.dataTransfer.files[0]
  if (!dropped) return
  fichier.value = dropped
  preview.value = URL.createObjectURL(dropped)
  prediction.value = null
  annotation.value = null
  message.value = ''
}

async function predict() {
  const formData = new FormData()
  formData.append('image', fichier.value)
  loading.value = true
  try {
    const res = await fetch(import.meta.env.VITE_API_URL + '/predict', {
      method: 'POST',
      body: formData,
      credentials: 'include'
    })
    const data = await res.json()
    // Correction : utilisation d'une valeur par défaut si data.label est undefined/null
    prediction.value = data.label || 'vide'
    annotation.value = prediction.value
  } catch (e) {
    message.value = "Erreur lors de la prédiction."
    console.error('Erreur prédiction:', e)
  } finally {
    loading.value = false
  }
}

async function validate() {
  if (!annotation.value) {
    message.value = "Veuillez choisir une annotation."
    return
  }

  const formData = new FormData()
  formData.append('image', fichier.value)
  formData.append('label', annotation.value)
  formData.append('annotation_auto', prediction.value || '')

  loading.value = true

  try {
    const csrfToken = auth.csrfToken;
    if (!csrfToken) {
      throw new Error("CSRF token manquant")
    }

    const res = await fetch(import.meta.env.VITE_API_URL + '/validate', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'X-CSRF-Token': csrfToken
      },
      body: formData
    })

    if (res.ok) {
      showValidationPopup.value = true
      fichier.value = null
      preview.value = null
      prediction.value = null
      annotation.value = null
      message.value = ''
    } else {
      const data = await res.json().catch(() => ({}))
      message.value = data?.error || "Erreur lors de l'enregistrement."
    }
  } catch (e) {
    message.value = "Erreur réseau."
    console.error('Erreur validation:', e)
  } finally {
    loading.value = false
  }
}

</script>

<style scoped>
input[type='radio'] {
  margin-right: 4px;
}

/* Transitions pour le popup */
.popup-enter-active, .popup-leave-active {
  transition: all 0.3s ease;
}

.popup-enter-from {
  opacity: 0;
  transform: scale(0.8);
}

.popup-leave-to {
  opacity: 0;
  transform: scale(0.8);
}

.popup-enter-to {
  opacity: 1;
  transform: scale(1);
}
</style>