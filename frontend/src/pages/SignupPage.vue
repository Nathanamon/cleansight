<template>
  <div class="min-h-screen bg-gradient-to-br from-green-50 via-white to-emerald-50 flex items-center justify-center p-4 relative overflow-hidden">
    <!-- Décor animé -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none z-0">
      <div class="absolute top-1/4 left-1/4 w-64 h-64 bg-gradient-to-r from-green-200/20 to-emerald-200/20 rounded-full blur-3xl animate-pulse-slow"></div>
      <div class="absolute bottom-1/4 right-1/4 w-48 h-48 bg-gradient-to-r from-emerald-200/20 to-green-200/20 rounded-full blur-3xl animate-pulse-slow" style="animation-delay:2s;"></div>
    </div>

    <div class="relative z-10 w-full max-w-md">
      <!-- Stepper -->
      <div class="flex justify-center mb-8 gap-2">
        <span class="w-3 h-3 rounded-full bg-green-500 shadow"></span>
        <span class="w-3 h-3 rounded-full bg-emerald-400 opacity-60"></span>
        <span class="w-3 h-3 rounded-full bg-gray-300 opacity-30"></span>
      </div>
      <div class="bg-white/90 backdrop-blur-lg rounded-3xl shadow-2xl px-7 py-10 sm:p-10 border border-green-100/50 relative animate-fade-in-up">
        <!-- Logo -->
        <div class="flex justify-center mb-6">
          <img src="../assets/logo.png" alt="CleanSight Logo" class="h-20 w-20 rounded-2xl shadow-lg border border-green-100"/>
        </div>

        <!-- En-tête -->
        <div class="text-center mb-7">
          <h2 class="text-2xl font-bold bg-gradient-to-r from-green-700 to-emerald-700 bg-clip-text text-transparent mb-2">Créer un compte agent</h2>
          <p class="text-gray-500 text-sm">Réservé aux agents de la Ville de Paris</p>
        </div>

        <!-- Feedback -->
        <transition
          enter-active-class="transition-all duration-300"
          enter-from-class="opacity-0 -translate-y-2"
          enter-to-class="opacity-100 translate-y-0"
          leave-active-class="transition-all duration-200"
          leave-from-class="opacity-100 translate-y-0"
          leave-to-class="opacity-0 -translate-y-2"
        >
          <div v-if="message" class="mb-6 p-3 rounded-xl border animate-shake text-sm flex items-center gap-2" :class="messageClasses">
            <span v-if="messageType === 'error'" aria-label="Erreur" class="text-red-400">⚠️</span>
            <span v-else class="text-green-600">✅</span>
            <span>{{ message }}</span>
          </div>
        </transition>

        <!-- Formulaire -->
        <form @submit.prevent="handleSignup" class="space-y-5">
          <!-- Code agent -->
          <div>
            <label class="block text-xs font-bold text-gray-700 mb-1">Code agent Paris <span class="text-red-500">*</span></label>
            <input
              v-model="agentCode"
              type="text"
              required
              maxlength="10"
              autocomplete="off"
              placeholder="AGP-3921"
              class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-green-100 focus:border-green-500 transition-all"
              :class="{'border-green-500 ring-2 shadow-lg': agentCodeFocused}"
              @focus="agentCodeFocused = true"
              @blur="agentCodeFocused = false"
              aria-describedby="agentHelp"
            />
            <p id="agentHelp" v-if="agentCode && !isValidAgentCode" class="text-xs text-red-500 mt-1">Format attendu : <b>AGP-xxxx</b></p>
          </div>
          <!-- Email -->
          <div>
            <label class="block text-xs font-bold text-gray-700 mb-1">Adresse email professionnelle <span class="text-red-500">*</span></label>
            <input
              v-model="email"
              type="email"
              required
              autocomplete="off"
              placeholder="prenom.nom@paris.fr"
              class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-green-100 focus:border-green-500 transition-all"
              :class="{'border-green-500 ring-2 shadow-lg': emailFocused}"
              @focus="emailFocused = true"
              @blur="emailFocused = false"
              aria-describedby="emailHelp"
            />
            <p id="emailHelp" v-if="email && !isValidEmail" class="text-xs text-red-500 mt-1">L’email doit se terminer par <b>@paris.fr</b></p>
          </div>
          <!-- Prénom -->
          <div>
            <label class="block text-xs font-bold text-gray-700 mb-1">Prénom <span class="text-red-500">*</span></label>
            <input
              v-model="firstName"
              type="text"
              required
              placeholder="Jean"
              class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-green-100 focus:border-green-500 transition-all"
            />
          </div>
          <!-- Nom -->
          <div>
            <label class="block text-xs font-bold text-gray-700 mb-1">Nom <span class="text-red-500">*</span></label>
            <input
              v-model="lastName"
              type="text"
              required
              placeholder="Dupont"
              class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-green-100 focus:border-green-500 transition-all"
            />
          </div>
          <!-- Mot de passe -->
          <div>
            <label class="block text-xs font-bold text-gray-700 mb-1">Mot de passe <span class="text-red-500">*</span></label>
            <div class="relative">
              <input
                :type="showPassword ? 'text' : 'password'"
                v-model="password"
                required
                placeholder="••••••••"
                class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-green-100 focus:border-green-500 transition-all pr-10"
                :class="{'border-green-500 ring-2 shadow-lg': passwordFocused}"
                @focus="passwordFocused = true"
                @blur="passwordFocused = false"
                aria-describedby="pwdHelp"
              />
              <button type="button" @click="showPassword = !showPassword"
                class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-green-700 focus:outline-none"
                :aria-label="showPassword ? 'Masquer' : 'Afficher'">
                <svg v-if="showPassword" fill="none" stroke="currentColor" viewBox="0 0 24 24" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21"/></svg>
                <svg v-else fill="none" stroke="currentColor" viewBox="0 0 24 24" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
              </button>
            </div>
            <p id="pwdHelp" class="text-xs text-gray-400 mt-1">8 caractères minimum, mélangez chiffres et lettres.</p>
          </div>
          <!-- Confirmation mot de passe -->
          <div>
            <label class="block text-xs font-bold text-gray-700 mb-1">Confirmer le mot de passe <span class="text-red-500">*</span></label>
            <input
              v-model="confirmPassword"
              :type="showPassword ? 'text' : 'password'"
              required
              placeholder="Confirmez le mot de passe"
              class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-green-100 focus:border-green-500 transition-all"
              :class="{'border-green-500 ring-2 shadow-lg': confirmPasswordFocused}"
              @focus="confirmPasswordFocused = true"
              @blur="confirmPasswordFocused = false"
            />
            <p v-if="confirmPassword && password !== confirmPassword" class="text-xs text-red-500 mt-1">Les mots de passe ne correspondent pas</p>
          </div>
          <!-- Conditions -->
          <div class="flex items-start space-x-3">
            <input 
              type="checkbox"
              v-model="acceptTerms"
              required
              class="w-5 h-5 text-green-600 border-gray-300 rounded focus:ring-green-500 focus:ring-2 mt-1"
              aria-label="J’accepte les conditions"
            />
            <span class="text-xs text-gray-600">
              J’accepte les 
              <router-link to="/terms" class="text-green-600 hover:underline">conditions d’utilisation</router-link>
              et la 
              <router-link to="/privacy" class="text-green-600 hover:underline">politique de confidentialité</router-link>.
            </span>
          </div>
          <!-- Bouton inscription -->
          <button
            type="submit"
            :disabled="loading || !isFormValid"
            class="w-full mt-6 bg-gradient-to-r from-green-600 to-emerald-600 text-white py-4 rounded-xl font-semibold hover:from-green-700 hover:to-emerald-700 transform hover:scale-[1.02] transition-all duration-200 shadow-lg hover:shadow-xl disabled:opacity-60 disabled:cursor-not-allowed"
          >
            <span v-if="loading" class="flex items-center justify-center">
              <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
              </svg>
              Création du compte...
            </span>
            <span v-else>Créer mon compte agent</span>
          </button>
        </form>
        <!-- Retour connexion -->
        <div class="text-center mt-8">
          <p class="text-xs text-gray-500">
            Vous avez déjà un compte ?
            <router-link to="/login" class="text-green-700 font-semibold hover:underline ml-1">Connexion</router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "SignupPage",
  data() {
    return {
      agentCode: "",
      email: "",
      firstName: "",
      lastName: "",
      password: "",
      confirmPassword: "",
      acceptTerms: false,
      loading: false,
      message: "",
      messageType: "error",
      showPassword: false,
      agentCodeFocused: false,
      emailFocused: false,
      passwordFocused: false,
      confirmPasswordFocused: false,
    }
  },
  computed: {
    isValidAgentCode() {
      return /^AGP-\d{4,6}$/i.test(this.agentCode)
    },
    isValidEmail() {
      return /^[a-z0-9._-]+@([a-z0-9-]+\.)?paris\.fr$/i.test(this.email)
    },
    isFormValid() {
      return (
        this.isValidAgentCode &&
        this.isValidEmail &&
        this.firstName &&
        this.lastName &&
        this.password &&
        this.confirmPassword &&
        this.password === this.confirmPassword &&
        this.acceptTerms
      )
    },
    messageClasses() {
      return this.messageType === 'error'
        ? 'bg-red-50 border-red-200 text-red-600'
        : 'bg-green-50 border-green-200 text-green-600'
    }
  },
  methods: {
    async handleSignup() {
      this.message = ""
      this.loading = true

      if (!this.isFormValid) {
        this.message = "Merci de vérifier vos informations."
        this.messageType = "error"
        this.loading = false
        return
      }

      try {
        const res = await fetch(
          `${import.meta.env.VITE_API_URL}/auth/signup`,
          {
            method: "POST",
            credentials: "include",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              email: this.email,
              password: this.password,
              agent_code: this.agentCode,
              first_name: this.firstName,
              last_name: this.lastName
            })
          }
        )
        const data = await res.json()
        if (res.ok) {
          this.messageType = "success"
          this.message = "Compte agent créé avec succès !"
          // Récupère la destination de redirection depuis les query params ou met une valeur par défaut
          const redirect = this.$route.query.redirect || "/dashboard"
          setTimeout(() => this.$router.push(redirect), 1600)
        } else {
          this.messageType = "error"
          this.message = data.error || "Erreur lors de l’inscription"
        }
      } catch (e) {
        this.messageType = "error"
        this.message = "Erreur réseau"
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
/* Reprends tes animations ici ou laisse les tiennes si tu veux */
@keyframes fade-in-up { from { opacity: 0; transform: translateY(24px);} to { opacity: 1; transform: none;}}
@keyframes shake { 0%,100%{transform:translateX(0);} 25%{transform:translateX(-2px);} 75%{transform:translateX(2px);}}
@keyframes pulse-slow{0%,100%{opacity:0.5;}50%{opacity:0.8;}}
.animate-fade-in-up{animation:fade-in-up 0.8s cubic-bezier(.45,.05,.55,.95) both;}
.animate-shake{animation:shake 0.5s;}
.animate-pulse-slow{animation:pulse-slow 4s ease-in-out infinite;}
.shadow-3xl{box-shadow:0 35px 60px -12px rgba(0,0,0,0.22);}
</style>