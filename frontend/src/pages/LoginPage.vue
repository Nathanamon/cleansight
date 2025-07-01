<template>
  <div class="min-h-screen bg-gradient-to-br from-green-50 via-white to-emerald-50 flex items-center justify-center p-4 relative overflow-hidden">
    <!-- Éléments de fond animés -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-1/4 left-1/4 w-64 h-64 bg-gradient-to-r from-green-200/20 to-emerald-200/20 rounded-full blur-3xl animate-pulse-slow"></div>
      <div class="absolute bottom-1/4 right-1/4 w-48 h-48 bg-gradient-to-r from-emerald-200/20 to-green-200/20 rounded-full blur-3xl animate-pulse-slow" style="animation-delay: 2s;"></div>
    </div>

    <div class="bg-white/80 backdrop-blur-sm rounded-3xl shadow-2xl p-8 w-full max-w-md border border-green-100/50 relative overflow-hidden transform transition-all duration-500 hover:shadow-3xl animate-fade-in-up">
      
      <!-- Décorations flottantes -->
      <div class="absolute top-0 right-0 w-32 h-32 bg-gradient-to-bl from-green-100/60 to-transparent rounded-full -translate-y-16 translate-x-16 animate-float"></div>
      <div class="absolute bottom-0 left-0 w-24 h-24 bg-gradient-to-tr from-emerald-100/60 to-transparent rounded-full translate-y-12 -translate-x-12 animate-float-reverse"></div>
      
      <!-- Barre de progression en haut -->
      <div class="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-green-500 to-emerald-500 transform origin-left scale-x-0 animate-scale-x"></div>

      <!-- Logo avec animation -->
      <div class="w-24 h-24 mx-auto mb-6 rounded-2xl overflow-hidden shadow-lg transform transition-all duration-300 hover:scale-105 hover:rotate-2 animate-bounce-in">
        <img src="../assets/logo.png" alt="CleanSight Logo" class="w-full h-full object-cover"/>
      </div>

      <!-- En-tête avec animation de texte -->
      <div class="text-center mb-8 animate-fade-in-up" style="animation-delay: 0.3s;">
        <h2 class="text-3xl font-bold bg-gradient-to-r from-green-700 to-emerald-700 bg-clip-text text-transparent mb-3">
          Connexion
        </h2>
        <p class="text-gray-600 text-sm transform transition-all duration-300 hover:text-gray-700">
          Accédez à votre espace personnel
        </p>
      </div>

      <!-- Message d'erreur/succès avec animation -->
      <transition
        enter-active-class="transition-all duration-300"
        enter-from-class="opacity-0 transform -translate-y-2"
        enter-to-class="opacity-100 transform translate-y-0"
        leave-active-class="transition-all duration-200"
        leave-from-class="opacity-100 transform translate-y-0"
        leave-to-class="opacity-0 transform -translate-y-2"
      >
        <div v-if="message" class="mb-6 p-4 rounded-xl border animate-shake" :class="messageClasses">
          <div class="flex items-center">
            <svg v-if="messageType === 'error'" class="w-5 h-5 mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
            </svg>
            <svg v-else class="w-5 h-5 mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
            </svg>
            <p class="text-sm font-medium">{{ message }}</p>
          </div>
        </div>
      </transition>

      <!-- Formulaire de connexion -->
      <form @submit.prevent="handleLogin" class="space-y-6 animate-fade-in-up" style="animation-delay: 0.5s;">
        <!-- Email -->
        <div class="space-y-2">
          <label class="block text-sm font-semibold text-gray-700 transition-colors duration-200" 
                 :class="{ 'text-green-600': emailFocused }">
            Email
          </label>
          <div class="relative group">
            <input
              type="email"
              v-model="email"
              placeholder="votre@email.com"
              required
              @focus="emailFocused = true"
              @blur="emailFocused = false"
              class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-4 focus:ring-green-100 focus:border-green-500 transition-all duration-300 pl-12 hover:border-gray-300 group-hover:shadow-md"
              :class="{ 'border-green-500 shadow-lg': emailFocused }"
            />
            <svg class="absolute left-3 top-3.5 w-5 h-5 transition-colors duration-300" 
                 :class="emailFocused ? 'text-green-500' : 'text-gray-400'" 
                 fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207"/>
            </svg>
            <!-- Indicateur de validation -->
            <transition
              enter-active-class="transition-all duration-200"
              enter-from-class="opacity-0 scale-50"
              enter-to-class="opacity-100 scale-100"
            >
              <svg v-if="email && isValidEmail" class="absolute right-3 top-3.5 w-5 h-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
              </svg>
            </transition>
          </div>
        </div>

        <!-- Mot de passe -->
        <div class="space-y-2">
          <label class="block text-sm font-semibold text-gray-700 transition-colors duration-200" 
                 :class="{ 'text-green-600': passwordFocused }">
            Mot de passe
          </label>
          <div class="relative group">
            <input
              :type="showPassword ? 'text' : 'password'"
              v-model="password"
              placeholder="••••••••"
              required
              @focus="passwordFocused = true"
              @blur="passwordFocused = false"
              class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-4 focus:ring-green-100 focus:border-green-500 transition-all duration-300 pl-12 pr-12 hover:border-gray-300 group-hover:shadow-md"
              :class="{ 'border-green-500 shadow-lg': passwordFocused }"
            />
            <svg class="absolute left-3 top-3.5 w-5 h-5 transition-colors duration-300" 
                 :class="passwordFocused ? 'text-green-500' : 'text-gray-400'" 
                 fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
            </svg>
            <!-- Bouton pour afficher/masquer le mot de passe -->
            <button
              type="button"
              @click="showPassword = !showPassword"
              class="absolute right-3 top-3.5 w-5 h-5 text-gray-400 hover:text-gray-600 transition-colors duration-200 focus:outline-none"
            >
              <svg v-if="showPassword" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21"/>
              </svg>
              <svg v-else fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
              </svg>
            </button>
          </div>
        </div>

        <!-- Options -->
        <div class="flex items-center justify-between text-sm pt-2">
          <label class="flex items-center space-x-2 cursor-pointer group">
            <input 
              type="checkbox" 
              v-model="remember" 
              class="w-4 h-4 text-green-600 border-gray-300 rounded focus:ring-green-500 focus:ring-2 transition-all duration-200"
            />
            <span class="text-gray-700 group-hover:text-gray-900 transition-colors duration-200">Se souvenir de moi</span>
          </label>
            <router-link 
                to="/forgot-password"
                class="text-green-600 hover:text-green-700 font-medium hover:underline"
              >
                Mot de passe oublié ?
            </router-link>
        </div>

        <!-- Bouton Connexion -->
        <button
          type="submit"
          :disabled="loading || !isFormValid"
          class="w-full mt-6 bg-gradient-to-r from-green-600 to-emerald-600 text-white py-4 rounded-xl font-semibold hover:from-green-700 hover:to-emerald-700 transform hover:scale-[1.02] transition-all duration-300 shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none relative overflow-hidden group"
        >
          <!-- Effet de brillance au survol -->
          <div class="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000"></div>
          
          <span v-if="loading" class="flex items-center justify-center relative z-10">
            <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
            </svg>
            Connexion en cours...
          </span>
          <span v-else class="relative z-10">Se connecter</span>
        </button>
      </form>

      <!-- Séparateur stylisé -->
      <div class="flex items-center my-8 animate-fade-in-up" style="animation-delay: 0.7s;">
        <div class="flex-1 h-px bg-gradient-to-r from-transparent via-gray-300 to-transparent"></div>
        <span class="px-4 text-xs text-gray-500 bg-white rounded-full border border-gray-200 font-medium">
          ou
        </span>
        <div class="flex-1 h-px bg-gradient-to-r from-transparent via-gray-300 to-transparent"></div>
      </div>

      <!-- Bouton d'inscription -->
      <button
        @click="goToSignup"
        class="w-full border-2 border-green-600 text-green-600 py-3 rounded-xl font-semibold hover:bg-green-50 hover:border-green-700 hover:text-green-700 transform hover:scale-[1.02] transition-all duration-300 shadow-sm hover:shadow-md animate-fade-in-up"
        style="animation-delay: 0.9s;"
      >
        <span class="flex items-center justify-center">
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"/>
          </svg>
          Créer un compte
        </span>
      </button>

      <!-- Badge de sécurité -->
      <div class="text-center mt-6 animate-fade-in-up" style="animation-delay: 1.1s;">
        <div class="inline-flex items-center space-x-2 text-xs text-gray-500 bg-gray-50 px-3 py-2 rounded-full">
          <svg class="w-4 h-4 text-green-500" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clip-rule="evenodd"/>
          </svg>
          <span>Connexion sécurisée SSL</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "LoginPage",
  data() {
    return {
      email: "",
      password: "",
      remember: false,
      loading: false,
      message: "",
      messageType: "error", // 'error' ou 'success'
      emailFocused: false,
      passwordFocused: false,
      showPassword: false
    }
  },
  computed: {
    isValidEmail() {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      return emailRegex.test(this.email)
    },
    isFormValid() {
      return this.email && this.password && this.isValidEmail
    },
    messageClasses() {
      return this.messageType === 'error' 
        ? 'bg-red-50 border-red-200 text-red-600'
        : 'bg-green-50 border-green-200 text-green-600'
    }
  },
  methods: {
    async handleLogin() {
      this.message = ""
      this.loading = true
      
      try {
        const res = await fetch(`${import.meta.env.VITE_API_URL}/login`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ 
            email: this.email, 
            password: this.password,
            remember: this.remember
          })
        })
        
        const data = await res.json()
        
        if (res.ok) {
          this.messageType = "success"
          this.message = "Connexion réussie ! Redirection..."
          
          // Simulation d'une pause pour l'UX
          setTimeout(() => {
            this.$router.push("/dashboard")
          }, 1000)
        } else {
          this.messageType = "error"
          this.message = data.error || "Identifiants invalides"
        }
      } catch (error) {
        this.messageType = "error"
        this.message = "Erreur réseau, veuillez réessayer."
      } finally {
        this.loading = false
      }
    },
    
    goToSignup() {
      this.$router.push("/signup")
    }
  }
}
</script>

<style scoped>
/* Animations personnalisées */
@keyframes fade-in-up {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes bounce-in {
  0% {
    opacity: 0;
    transform: scale(0.3);
  }
  50% {
    transform: scale(1.05);
  }
  70% {
    transform: scale(0.9);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes scale-x {
  from {
    transform: scaleX(0);
  }
  to {
    transform: scaleX(1);
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
  }
  50% {
    transform: translateY(-10px) rotate(5deg);
  }
}

@keyframes float-reverse {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
  }
  50% {
    transform: translateY(10px) rotate(-5deg);
  }
}

@keyframes pulse-slow {
  0%, 100% {
    opacity: 0.5;
  }
  50% {
    opacity: 0.8;
  }
}

@keyframes shake {
  0%, 100% {
    transform: translateX(0);
  }
  25% {
    transform: translateX(-2px);
  }
  75% {
    transform: translateX(2px);
  }
}

/* Classes d'animation */
.animate-fade-in-up {
  animation: fade-in-up 0.6s ease-out forwards;
  opacity: 0;
}

.animate-bounce-in {
  animation: bounce-in 0.8s ease-out forwards;
}

.animate-scale-x {
  animation: scale-x 2s ease-out forwards;
  animation-delay: 0.5s;
}

.animate-float {
  animation: float 6s ease-in-out infinite;
}

.animate-float-reverse {
  animation: float-reverse 8s ease-in-out infinite;
}

.animate-pulse-slow {
  animation: pulse-slow 4s ease-in-out infinite;
}

.animate-shake {
  animation: shake 0.5s ease-in-out;
}

/* Ombre personnalisée */
.shadow-3xl {
  box-shadow: 0 35px 60px -12px rgba(0, 0, 0, 0.25);
}

/* Scrollbar personnalisée si nécessaire */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb {
  background: linear-gradient(to bottom, #10b981, #059669);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(to bottom, #059669, #047857);
}
</style>