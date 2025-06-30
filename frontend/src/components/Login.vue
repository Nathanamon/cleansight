<template>
  <div class="container">
    <div class="login-box">
      <div class="logo-section">
        <img src="@/assets/logo.png" alt="CleanSight Logo" class="logo" />
        <h1>CleanSight</h1>
        <p class="slogan">TOUS VIGILANTS, TOUS PROPRE</p>
      </div>

      <h2>Connexion</h2>
      <p class="subtext">Accédez à votre espace personnel</p>

      <form @submit.prevent="handleLogin">
        <label>Email</label>
        <input type="email" v-model="email" placeholder="votre@email.com" required />

        <label>Mot de passe</label>
        <input type="password" v-model="password" placeholder="••••••••" required />

        <div class="options">
          <label>
            <input type="checkbox" v-model="remember" />
            Se souvenir de moi
          </label>
          <a href="#">Mot de passe oublié ?</a>
        </div>

        <button type="submit" class="login-btn">Se connecter</button>

        <div class="divider">ou</div>

        <button class="social-btn google">
          Continuer avec Google
        </button>
        <button class="social-btn facebook">
          Continuer avec Facebook
        </button>

        <p class="signup">
          Pas encore de compte ? <a href="#">Créer un compte</a>
        </p>
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
      remember: false
    };
  },
  methods: {
    handleLogin() {
      // Remplace ceci par ta logique réelle de connexion
      console.log("Connexion avec :", this.email, this.password, this.remember);
    }
  }
};
</script>

<style setup>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(to bottom right, #e6f5ec, #ffffff);
  min-height: 100vh;
  font-family: Arial, sans-serif;
}

.login-box {
  background: white;
  border-radius: 20px;
  padding: 2rem;
  max-width: 400px;
  width: 100%;
  box-shadow: 0 10px 25px rgba(0, 128, 0, 0.1);
}

.logo-section {
  text-align: center;
  margin-bottom: 1.5rem;
}

.logo {
  height: 60px;
  margin-bottom: 0.5rem;
}

.logo-section h1 {
  color: #2d8c4a;
  font-size: 24px;
  font-weight: bold;
}

.slogan {
  color: #4caf50;
  font-size: 13px;
  font-weight: 600;
}

h2 {
  text-align: center;
  color: #222;
}

.subtext {
  text-align: center;
  color: #666;
  font-size: 14px;
  margin-bottom: 1rem;
}

form {
  display: flex;
  flex-direction: column;
}

label {
  font-size: 14px;
  margin: 0.5rem 0 0.2rem;
  color: #444;
}

input[type="email"],
input[type="password"] {
  padding: 0.6rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  margin-bottom: 0.8rem;
  font-size: 14px;
}

.options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 13px;
  margin-bottom: 1rem;
}

.options a {
  color: #2d8c4a;
  text-decoration: none;
}

.login-btn {
  background-color: #2d8c4a;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 0.7rem;
  font-weight: bold;
  margin-bottom: 1rem;
  cursor: pointer;
}

.login-btn:hover {
  background-color: #256c3b;
}

.divider {
  text-align: center;
  margin: 1rem 0;
  color: #888;
  font-size: 13px;
}

.social-btn {
  padding: 0.6rem;
  border-radius: 8px;
  border: 1px solid #ccc;
  font-size: 14px;
  margin-bottom: 0.5rem;
  cursor: pointer;
}

.google {
  background-color: white;
}

.facebook {
  background-color: #f5f5f5;
}

.signup {
  text-align: center;
  font-size: 13px;
  margin-top: 1rem;
}

.signup a {
  color: #2d8c4a;
  font-weight: bold;
  text-decoration: none;
}
</style>
