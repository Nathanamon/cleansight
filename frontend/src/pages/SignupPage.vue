<template>
  <div class="min-h-screen bg-gradient-to-br from-emerald-50 via-green-50 to-teal-50 flex items-center justify-center p-6">
    <div class="bg-white/80 backdrop-blur-sm rounded-3xl shadow-2xl w-full max-w-lg border border-green-100 relative overflow-hidden">
      
      <!-- Éléments décoratifs -->
      <div class="absolute -top-20 -right-20 w-40 h-40 bg-gradient-to-bl from-green-200/30 to-emerald-200/30 rounded-full blur-sm"></div>
      <div class="absolute -bottom-16 -left-16 w-32 h-32 bg-gradient-to-tr from-teal-200/30 to-green-200/30 rounded-full blur-sm"></div>
      <div class="absolute top-12 right-12 w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
      <div class="absolute bottom-24 left-10 w-1 h-1 bg-emerald-400 rounded-full animate-pulse delay-1000"></div>
      
      <div class="relative z-10 p-8">
        <!-- En-tête avec logo et titre -->
        <div class="text-center mb-8">
          <div class="w-20 h-20 mx-auto mb-6 rounded-2xl overflow-hidden shadow-lg bg-gradient-to-br from-green-500 to-emerald-600 flex items-center justify-center">
            <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"/>
            </svg>
          </div>
          <h1 class="text-3xl font-bold text-gray-800 mb-2">Rejoignez CleanSight</h1>
          <p class="text-gray-600">Créez votre compte en quelques étapes</p>
        </div>

        <!-- Barre de progression -->
        <div class="mb-8">
          <div class="flex items-center justify-between text-xs text-gray-500 mb-2">
            <span>Informations</span>
            <span>Vérification</span>
            <span>Terminé</span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2">
            <div class="bg-gradient-to-r from-green-500 to-emerald-500 h-2 rounded-full transition-all duration-500" :style="{ width: progressWidth }"></div>
          </div>
        </div>

        <!-- Messages -->
        <div v-if="message" class="mb-6 p-4 rounded-xl" :class="messageClass">
          <div class="flex items-center">
            <svg v-if="messageType === 'error'" class="w-5 h-5 mr-3 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            <svg v-else class="w-5 h-5 mr-3 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            <p class="text-sm">{{ message }}</p>
          </div>
        </div>

        <!-- Formulaire d'inscription -->
        <form @submit.prevent="handleSignup" class="space-y-6">
          <!-- Champ Prénom/Nom -->
          <div class="grid grid-cols-2 gap-4">
            <div class="space-y-2">
              <label class="block text-sm font-semibold text-gray-700">Prénom</label>
              <div class="relative group">
                <input
                  type="text"
                  v-model="firstName"
                  placeholder="Jean"
                  required
                  class="w-full px-4 py-4 pl-12 border border-gray-300 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-green-500 transition-all duration-300 group-hover:border-green-300"
                />
                <svg class="absolute left-4 top-4 w-5 h-5 text-gray-400 group-hover:text-green-500 transition-colors duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                </svg>
              </div>
            </div>
            <div class="space-y-2">
              <label class="block text-sm font-semibold text-gray-700">Nom</label>
              <div class="relative group">
                <input
                  type="text"
                  v-model="lastName"
                  placeholder="Dupont"
                  required
                  class="w-full px-4 py-4 pl-12 border border-gray-300 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-green-500 transition-all duration-300 group-hover:border-green-300"
                />
                <svg class="absolute left-4 top-4 w-5 h-5 text-gray-400 group-hover:text-green-500 transition-colors duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                </svg>
              </div>
            </div>
          </div>

          <!-- Champ Email -->
          <div class="space-y-2">
            <label class="block text-sm font-semibold text-gray-700">Adresse email</label>
            <div class="relative group">
              <input
                type="email"
                v-model="email"
                placeholder="jean.dupont@email.com"
                required
                class="w-full px-4 py-4 pl-12 border border-gray-300 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-green-500 transition-all duration-300 group-hover:border-green-300"
                :class="{ 'border-red-300': emailError, 'border-green-300': emailValid }"
              />
              <svg class="absolute left-4 top-4 w-5 h-5 text-gray-400 group-hover:text-green-500 transition-colors duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207"/>
              </svg>
              <div v-if="emailValid" class="absolute right-4 top-4">
                <svg class="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                </svg>
              </div>
            </div>
            <p v-if="emailError" class="text-xs text-red-500 mt-1">{{ emailError }}</p>
          </div>

          <!-- Champ Mot de passe -->
          <div class="space-y-2">
            <label class="block text-sm font-semibold text-gray-700">Mot de passe</label>
            <div class="relative group">
              <input
                :type="showPassword ? 'text' : 'password'"
                v-model="password"
                placeholder="••••••••••"
                required
                class="w-full px-4 py-4 pl-12 pr-12 border border-gray-300 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-green-500 transition-all duration-300 group-hover:border-green-300"
                :class="{ 'border-red-300': passwordError, 'border-green-300': passwordValid }"
              />
              <svg class="absolute left-4 top-4 w-5 h-5 text-gray-400 group-hover:text-green-500 transition-colors duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
              </svg>
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute right-4 top-4 text-gray-400 hover:text-gray-600 transition-colors duration-200"
              >
                <svg v-if="showPassword" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21"/>
                </svg>
                <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                </svg>
              </button>
            </div>
            
            <!-- Indicateur de force du mot de passe -->
            <div class="space-y-2">
              <div class="flex space-x-1">
                <div class="h-1 flex-1 rounded-full transition-colors duration-300" :class="passwordStrengthColor[0]"></div>
                <div class="h-1 flex-1 rounded-full transition-colors duration-300" :class="passwordStrengthColor[1]"></div>
                <div class="h-1 flex-1 rounded-full transition-colors duration-300" :class="passwordStrengthColor[2]"></div>
                <div class="h-1 flex-1 rounded-full transition-colors duration-300" :class="passwordStrengthColor[3]"></div>
              </div>
              <p class="text-xs" :class="passwordStrengthTextColor">{{ passwordStrengthText }}</p>
            </div>
          </div>

          <!-- Confirmation mot de passe -->
          <div class="space-y-2">
            <label class="block text-sm font-semibold text-gray-700">Confirmer le mot de passe</label>
            <div class="relative group">
              <input
                type="password"
                v-model="confirmPassword"
                placeholder="••••••••••"
                required
                class="w-full px-4 py-4 pl-12 border border-gray-300 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-green-500 transition-all duration-300 group-hover:border-green-300"
                :class="{ 'border-red-300': confirmPasswordError, 'border-green-300': confirmPasswordValid }"
              />
              <svg class="absolute left-4 top-4 w-5 h-5 text-gray-400 group-hover:text-green-500 transition-colors duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.012-3.07a1 1 0 00-1.414-1.414l-.094.083L9 13.293l-3.793-3.793a1 1 0 00-1.497 1.32l.083.094L9 16.207 20.207 5a1 1 0 00-.083-1.32z"/>
              </svg>
              <div v-if="confirmPasswordValid" class="absolute right-4 top-4">
                <svg class="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                </svg>
              </div>
            </div>
            <p v-if="confirmPasswordError" class="text-xs text-red-500 mt-1">{{ confirmPasswordError }}</p>
          </div>

          <!-- Conditions d'utilisation -->
          <div class="space-y-4">
            <label class="flex items-start space-x-3 cursor-pointer group">
              <input 
                type="checkbox" 
                v-model="acceptTerms" 
                required
                class="w-5 h-5 text-green-600 border-gray-300 rounded focus:ring-green-500 focus:ring-2 mt-0.5"
              />
              <span class="text-sm text-gray-600 group-hover:text-gray-800 transition-colors duration-200 leading-relaxed">
                J'accepte les 
                <router-link 
                  to="/terms" 
                  class="text-green-600 hover:text-green-700 font-medium hover:underline"
                >
                  conditions d'utilisation
                </router-link>
                et la 
                <router-link 
                  to="/privacy" 
                  class="text-green-600 hover:text-green-700 font-medium hover:underline"
                >
                  politique de confidentialité
                </router-link>
              </span>
            </label>
            <label class="flex items-start space-x-3 cursor-pointer group">
              <input 
                type="checkbox" 
                v-model="acceptNewsletter" 
                class="w-5 h-5 text-green-600 border-gray-300 rounded focus:ring-green-500 focus:ring-2 mt-0.5"
              />
              <span class="text-sm text-gray-600 group-hover:text-gray-800 transition-colors duration-200">
                Je souhaite recevoir les actualités et offres de CleanSight
              </span>
            </label>
          </div>

          <!-- Bouton de création de compte -->
          <button
            type="submit"
            :disabled="loading || !formValid"
            class="w-full mt-8 bg-gradient-to-r from-green-600 to-emerald-600 text-white py-4 px-6 rounded-xl font-semibold hover:from-green-700 hover:to-emerald-700 transform hover:scale-[1.02] active:scale-[0.98] transition-all duration-200 shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
          >
            <span v-if="loading" class="flex items-center justify-center">
              <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Création en cours...
            </span>
            <span v-else>Créer mon compte</span>
          </button>
        </form>

        <!-- Séparateur -->
        <div class="flex items-center my-8">
          <div class="flex-1 border-t border-gray-200"></div>
          <span class="px-4 text-sm text-gray-500 bg-white">ou</span>
          <div class="flex-1 border-t border-gray-200"></div>
        </div>

        <!-- Lien vers connexion -->
        <div class="text-center">
          <p class="text-sm text-gray-600">
            Vous avez déjà un compte ?
            <router-link 
              to="/login" 
              class="text-green-600 hover:text-green-700 font-semibold hover:underline transition-colors duration-200 ml-1"
            >
              Connectez-vous
            </router-link>
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
      firstName: "",
      lastName: "",
      email: "",
      password: "",
      confirmPassword: "",
      showPassword: false,
      acceptTerms: false,
      acceptNewsletter: false,
      loading: false,
      message: "",
      messageType: "error"
    };
  },
  computed: {
    progressWidth() {
      if (this.loading) return "66%";
      if (this.formValid) return "33%";
      return "10%";
    },
    
    messageClass() {
      return this.messageType === 'error' 
        ? 'bg-red-50 border border-red-200 text-red-700'
        : 'bg-green-50 border border-green-200 text-green-700';
    },
    
    emailValid() {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return this.email && emailRegex.test(this.email);
    },
    
    emailError() {
      if (!this.email) return "";
      return this.emailValid ? "" : "Format d'email invalide";
    },
    
    passwordStrength() {
      let strength = 0;
      if (this.password.length >= 8) strength++;
      if (/[a-z]/.test(this.password)) strength++;
      if (/[A-Z]/.test(this.password)) strength++;
      if (/[0-9]/.test(this.password)) strength++;
      if (/[^A-Za-z0-9]/.test(this.password)) strength++;
      return Math.min(strength, 4);
    },
    
    passwordStrengthColor() {
      const colors = ['bg-gray-200', 'bg-gray-200', 'bg-gray-200', 'bg-gray-200'];
      const strengthColors = ['bg-red-400', 'bg-orange-400', 'bg-yellow-400', 'bg-green-400'];
      
      for (let i = 0; i < this.passwordStrength; i++) {
        colors[i] = strengthColors[Math.min(this.passwordStrength - 1, 3)];
      }
      return colors;
    },
    
    passwordStrengthText() {
      const texts = ["", "Faible", "Moyen", "Bon", "Excellent"];
      return texts[this.passwordStrength] || "";
    },
    
    passwordStrengthTextColor() {
      const colors = ["", "text-red-500", "text-orange-500", "text-yellow-600", "text-green-600"];
      return colors[this.passwordStrength] || "";
    },
    
    passwordValid() {
      return this.password.length >= 8 && this.passwordStrength >= 2;
    },
    
    passwordError() {
      if (!this.password) return "";
      if (this.password.length < 8) return "Le mot de passe doit contenir au moins 8 caractères";
      return "";
    },
    
    confirmPasswordValid() {
      return this.confirmPassword && this.password === this.confirmPassword;
    },
    
    confirmPasswordError() {
      if (!this.confirmPassword) return "";
      return this.confirmPasswordValid ? "" : "Les mots de passe ne correspondent pas";
    },
    
    formValid() {
      return this.firstName && 
             this.lastName && 
             this.emailValid && 
             this.passwordValid && 
             this.confirmPasswordValid && 
             this.acceptTerms;
    }
  },
  methods: {
    async handleSignup() {
      this.message = "";
      this.messageType = "error";
      this.loading = true;
      
      try {
        const res = await fetch(`${import.meta.env.VITE_API_URL}/signup`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ 
            firstName: this.firstName,
            lastName: this.lastName,
            email: this.email, 
            password: this.password,
            newsletter: this.acceptNewsletter
          })
        });
        
        const data = await res.json();
        
        if (res.ok) {
          this.messageType = "success";
          this.message = "Compte créé avec succès ! Redirection vers la connexion...";
          
          // Délai pour montrer le message de succès
          setTimeout(() => {
            this.$router.push("/login");
          }, 2000);
        } else {
          this.message = data.error || "Impossible de créer le compte. Veuillez réessayer.";
        }
      } catch (error) {
        this.message = "Erreur de connexion. Vérifiez votre connexion internet.";
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
/* Animations personnalisées */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.fade-in {
  animation: fadeIn 0.5s ease-out;
}

/* Styles pour les focus states améliorés */
input:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(34, 197, 94, 0.1);
}

/* Animation pour la barre de progression */
.progress-bar {
  transition: width 0.5s ease-in-out;
}

/* Hover effects pour les liens */
a {
  position: relative;
}

a:hover::after {
  content: '';
  position: absolute;
  width: 100%;
  height: 1px;
  bottom: -1px;
  left: 0;
  background-color: currentColor;
  transform: scaleX(0);
  animation: underlineExpand 0.3s ease-out forwards;
}

@keyframes underlineExpand {
  to { transform: scaleX(1); }
}

/* Animation pour les checkboxes */
input[type="checkbox"] {
  transition: all 0.2s ease-in-out;
}

input[type="checkbox"]:checked {
  transform: scale(1.05);
}
</style>