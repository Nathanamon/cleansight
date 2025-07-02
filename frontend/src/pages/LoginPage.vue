<template>
  <div class="min-h-screen bg-gradient-to-br from-green-50 via-white to-emerald-50 flex items-center justify-center p-4">
    <div class="bg-white rounded-3xl shadow-2xl p-8 w-full max-w-md border border-green-100 relative overflow-hidden">
      
      <!-- Décoration d'arrière-plan -->
      <div class="absolute top-0 right-0 w-32 h-32 bg-gradient-to-bl from-green-100 to-transparent rounded-full -translate-y-16 translate-x-16 opacity-50"></div>
      <div class="absolute bottom-0 left-0 w-24 h-24 bg-gradient-to-tr from-emerald-100 to-transparent rounded-full translate-y-12 -translate-x-12 opacity-50"></div>
      
      <!-- Section logo -->
      <div class="w-30 h-30 mx-auto mb-4 rounded-2xl overflow-hidden shadow-lg">
        <img 
          src="../assets/logo.png" 
          alt="CleanSight Logo" 
          class="w-full h-full object-cover"
        />
      </div>

      <!-- Titre de connexion -->
      <div class="text-center mb-8">
        <h2 class="text-2xl font-bold text-gray-800 mb-2">Connexion</h2>
        <p class="text-gray-600 text-sm">Accédez à votre espace personnel</p>
      </div>

      <!-- Formulaire -->
      <form @submit.prevent="handleLogin" class="space-y-6">
        
        <!-- Email -->
        <div class="space-y-2">
          <label class="block text-sm font-medium text-gray-700">Email</label>
          <div class="relative">
            <input
              type="email"
              v-model="email"
              placeholder="votre@email.com"
              required
              class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-green-500 transition-all duration-200 pl-11"
            />
            <svg class="absolute left-3 top-3.5 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207"></path>
            </svg>
          </div>
        </div>

        <!-- Mot de passe -->
        <div class="space-y-2">
          <label class="block text-sm font-medium text-gray-700">Mot de passe</label>
          <div class="relative">
            <input
              type="password"
              v-model="password"
              placeholder="••••••••"
              required
              class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-green-500 transition-all duration-200 pl-11"
            />
            <svg class="absolute left-3 top-3.5 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
            </svg>
          </div>
        </div>

        <!-- Options -->
        <div class="flex items-center justify-between text-sm">
          <label class="flex items-center space-x-2 cursor-pointer">
            <input 
              type="checkbox" 
              v-model="remember" 
              class="w-4 h-4 text-green-600 border-gray-300 rounded focus:ring-green-500"
            />
            <span class="text-gray-700">Se souvenir de moi</span>
          </label>
          <a href="#" class="text-green-600 hover:text-green-700 font-medium transition-colors duration-200">
            Mot de passe oublié ?
          </a>
        </div>

        <!-- Bouton de connexion -->
        <button 
          type="submit" 
          class="w-full bg-gradient-to-r from-green-600 to-emerald-600 text-white py-3 px-4 rounded-xl font-semibold hover:from-green-700 hover:to-emerald-700 transform hover:scale-[1.02] transition-all duration-200 shadow-lg hover:shadow-xl"
        >
          Se connecter
        </button>
      </form>
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
    };
  },
  methods: {
    handleLogin() {
      // Remplace ceci par ta logique réelle de connexion
      console.log("Connexion avec :", this.email, this.password, this.remember);
    },
  },
};
</script>