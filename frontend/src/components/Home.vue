<template>
  <div class="home-page">
    <!-- Navigation Header -->
    <nav class="navbar">
      <div class="nav-container">
        <div class="nav-brand">
          <div class="logo-container">
            <div class="logo-placeholder">🧹</div>
          </div>
          <h1 class="brand-name">CleanSight</h1>
        </div>
        <div class="nav-menu">
          <span class="nav-item" @click="scrollToSection('features')"
            >Fonctionnalités</span
          >
          <span class="nav-item" @click="scrollToSection('dashboard')"
            >Dashboard</span
          >
          <span class="nav-item" @click="scrollToSection('impact')"
            >Impact</span
          >
          <button class="cta-button" @click="navigateToUpload">
            Analyser Image
          </button>
          <button class="login-button" @click="navigateToDashboard">
            Connexion
          </button>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-container">
        <div class="hero-content">
          <h1 class="hero-title">
            Surveillance Intelligente des
            <span class="highlight">Poubelles Urbaines</span>
          </h1>
          <p class="hero-subtitle">
            Prévenez les dépôts sauvages grâce à l'IA. Notre plateforme détecte
            automatiquement l'état des poubelles pour une gestion optimisée des
            déchets urbains.
          </p>
          <div class="hero-buttons">
            <button class="primary-button" @click="navigateToUpload">
              <span class="button-icon">📷</span>
              Analyser une Image
            </button>
            <button
              class="secondary-button"
              @click="scrollToSection('features')"
            >
              <span class="button-icon">🔍</span>
              Découvrir Plus
            </button>
          </div>
        </div>
        <div class="hero-visual">
          <div class="floating-card">
            <div class="card-header">
              <div class="status-indicator full"></div>
              <span>Poubelle Détectée</span>
            </div>
            <div class="card-content">
              <div class="detection-box">🗑️ État: <strong>Pleine</strong></div>
              <div class="location">📍 Rue de la République</div>
              <div class="timestamp">⏰ Il y a 5 minutes</div>
            </div>
          </div>
        </div>
      </div>
      <div class="hero-wave"></div>
    </section>

    <!-- Features Section -->
    <section id="features" class="features-section">
      <div class="container">
        <h2 class="section-title">Fonctionnalités Clés</h2>
        <div class="features-grid">
          <div
            class="feature-card"
            v-for="feature in features"
            :key="feature.id"
            @mouseenter="animateCard"
            @mouseleave="resetCard"
          >
            <div class="feature-icon">{{ feature.icon }}</div>
            <h3 class="feature-title">{{ feature.title }}</h3>
            <p class="feature-description">{{ feature.description }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Dashboard Preview Section -->
    <section id="dashboard" class="dashboard-section">
      <div class="container">
        <h2 class="section-title">Tableau de Bord Interactif</h2>
        <div class="dashboard-preview">
          <div class="dashboard-mockup">
            <div class="mockup-header">
              <div class="mockup-nav">
                <div class="nav-dot"></div>
                <div class="nav-dot"></div>
                <div class="nav-dot"></div>
              </div>
              <span class="mockup-title">CleanSight Dashboard</span>
            </div>
            <div class="mockup-content">
              <div class="chart-placeholder">
                <div class="chart-icon">📊</div>
                <p>Graphiques et Statistiques</p>
              </div>
              <div class="map-placeholder">
                <div class="map-icon">🗺️</div>
                <p>Carte Interactive</p>
              </div>
            </div>
          </div>
          <div class="dashboard-info">
            <h3>Accédez aux Données Complètes</h3>
            <p>
              Visualisez les tendances, analysez les performances et optimisez
              la gestion des déchets avec notre dashboard complet.
            </p>
            <button class="dashboard-cta" @click="navigateToDashboard">
              <span class="button-icon">🔐</span>
              Se Connecter au Dashboard
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- Statistics Section -->
    <section class="stats-section">
      <div class="container">
        <div class="stats-grid">
          <div class="stat-item" v-for="stat in statistics" :key="stat.id">
            <div class="stat-number">{{ displayedStats[stat.id] }}</div>
            <div class="stat-label">{{ stat.label }}</div>
          </div>
        </div>
      </div>
    </section>

    <!-- Impact Section -->
    <section id="impact" class="impact-section">
      <div class="container">
        <h2 class="section-title">Impact Environnemental</h2>
        <div class="impact-content">
          <div class="impact-text">
            <h3>Une Solution AI for Good</h3>
            <p>
              Notre plateforme s'inscrit dans une démarche Green IT et contribue
              directement à la réduction de l'empreinte écologique urbaine en
              prévenant les dépôts sauvages avant qu'ils ne se forment.
            </p>
            <ul class="impact-list">
              <li>✅ Réduction des déchets abandonnés</li>
              <li>✅ Optimisation des tournées de collecte</li>
              <li>✅ Amélioration du cadre de vie urbain</li>
              <li>✅ Sensibilisation citoyenne</li>
            </ul>
          </div>
          <div class="impact-visual">
            <div class="environment-animation">
              <div class="tree">🌳</div>
              <div class="city">🏙️</div>
              <div class="recycling">♻️</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
      <div class="container">
        <div class="footer-content">
          <div class="footer-brand">
            <div class="footer-logo">🧹</div>
            <p>Tous vigilants, tous propres</p>
          </div>
          <div class="footer-links">
            <div class="footer-section">
              <h4>Projet</h4>
              <a href="#" @click="scrollToSection('features')"
                >Fonctionnalités</a
              >
              <a href="#" @click="scrollToSection('dashboard')">Dashboard</a>
              <a href="#" @click="scrollToSection('impact')">Impact</a>
            </div>
            <div class="footer-section">
              <h4>À propos</h4>
              <a href="#">Efrei Paris</a>
              <a href="#">Master Camp Data 2025</a>
              <a href="#">Ahmed Ghazi BLAIECH</a>
            </div>
          </div>
        </div>
        <div class="footer-bottom">
          <p>&copy; 2025 CleanSight - Wild Dump Prevention Project</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from "vue";
import { useRouter } from "vue-router";

export default {
  name: "HomePage",
  setup() {
    const router = useRouter();
    const displayedStats = reactive({
      images: 0,
      accuracy: 0,
      reduction: 0,
      cities: 0,
    });

    const features = [
      {
        id: 1,
        icon: "🎯",
        title: "Détection Automatique",
        description:
          "Analyse instantanée de l'état des poubelles (vide, pleine, débordante) grâce à l'IA",
      },
      {
        id: 2,
        icon: "🗺️",
        title: "Cartographie Dynamique",
        description:
          "Visualisation en temps réel des zones à risque de débordement sur une carte interactive",
      },
      {
        id: 3,
        icon: "📊",
        title: "Tableau de Bord",
        description:
          "Statistiques complètes et graphiques interactifs pour optimiser la gestion des déchets",
      },
      {
        id: 4,
        icon: "⚡",
        title: "Prédiction Préventive",
        description:
          "Anticipation des zones à risque pour une action préventive efficace",
      },
    ];

    const statistics = [
      { id: "images", value: 1247, label: "Images Analysées" },
      { id: "accuracy", value: 94, label: "% de Précision" },
      { id: "reduction", value: 67, label: "% Réduction Dépôts" },
      { id: "cities", value: 12, label: "Villes Testées" },
    ];

    const scrollToSection = (sectionId) => {
      const element = document.getElementById(sectionId);
      if (element) {
        element.scrollIntoView({ behavior: "smooth" });
      }
    };

    const navigateToUpload = () => {
      // Navigate to upload page
      router.push("/upload");
    };

    const navigateToDashboard = () => {
      // Navigate to login/dashboard page
      router.push("/login");
    };

    const animateCard = (event) => {
      event.currentTarget.style.transform = "translateY(-10px) scale(1.02)";
    };

    const resetCard = (event) => {
      event.currentTarget.style.transform = "translateY(0) scale(1)";
    };

    const animateStats = () => {
      statistics.forEach((stat) => {
        let current = 0;
        const increment = stat.value / 50;
        const timer = setInterval(() => {
          current += increment;
          if (current >= stat.value) {
            displayedStats[stat.id] = stat.value;
            clearInterval(timer);
          } else {
            displayedStats[stat.id] = Math.floor(current);
          }
        }, 50);
      });
    };

    onMounted(() => {
      // Animate statistics when component mounts
      setTimeout(animateStats, 1000);
    });

    return {
      displayedStats,
      features,
      statistics,
      scrollToSection,
      navigateToUpload,
      navigateToDashboard,
      animateCard,
      resetCard,
    };
  },
};
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.home-page {
  font-family: "Inter", -apple-system, BlinkMacSystemFont, sans-serif;
  line-height: 1.6;
  color: #333;
}

/* Navigation */
.navbar {
  position: fixed;
  top: 0;
  width: 100%;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  z-index: 1000;
  padding: 1rem 0;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 2rem;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logo-container {
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-placeholder {
  font-size: 2.5rem;
  background: linear-gradient(135deg, #6b8e23, #8fbc8f);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  filter: drop-shadow(2px 2px 4px rgba(0, 0, 0, 0.1));
}

.brand-name {
  font-size: 1.75rem;
  font-weight: 700;
  color: #6b8e23;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
}

.nav-menu {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.nav-item {
  color: #666;
  cursor: pointer;
  transition: color 0.3s ease;
  font-weight: 500;
  padding: 0.5rem 0;
}

.nav-item:hover {
  color: #6b8e23;
}

.cta-button,
.login-button {
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 25px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
  font-size: 0.9rem;
}

.cta-button {
  background: linear-gradient(135deg, #6b8e23, #8fbc8f);
  color: white;
  margin-right: 1rem;
}

.cta-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(107, 142, 35, 0.3);
}

.login-button {
  background: transparent;
  color: #6b8e23;
  border: 2px solid #6b8e23;
}

.login-button:hover {
  background: #6b8e23;
  color: white;
  transform: translateY(-2px);
}

/* Hero Section */
.hero-section {
  position: relative;
  min-height: 100vh;
  background: linear-gradient(135deg, #f8fffe 0%, #e8f5e8 100%);
  display: flex;
  align-items: center;
  padding-top: 80px;
  overflow: hidden;
}

.hero-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 800;
  line-height: 1.2;
  margin-bottom: 1.5rem;
  color: #2c3e50;
}

.highlight {
  color: #6b8e23;
  position: relative;
}

.hero-subtitle {
  font-size: 1.25rem;
  color: #666;
  margin-bottom: 2.5rem;
  line-height: 1.6;
}

.hero-buttons {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.primary-button,
.secondary-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 2rem;
  border-radius: 30px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
}

.primary-button {
  background: linear-gradient(135deg, #6b8e23, #8fbc8f);
  color: white;
}

.primary-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(107, 142, 35, 0.4);
}

.secondary-button {
  background: white;
  color: #6b8e23;
  border: 2px solid #6b8e23;
}

.secondary-button:hover {
  background: #6b8e23;
  color: white;
  transform: translateY(-3px);
}

.floating-card {
  background: white;
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  animation: float 3s ease-in-out infinite;
  border: 1px solid rgba(107, 142, 35, 0.2);
}

@keyframes float {
  0%,
  100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
}

.card-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
  font-weight: 600;
  color: #333;
}

.status-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #ff6b6b;
}

.status-indicator.full {
  background: #ff6b6b;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
  100% {
    opacity: 1;
  }
}

.detection-box {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 10px;
  margin-bottom: 0.5rem;
  font-size: 1.1rem;
}

.location,
.timestamp {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.hero-wave {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 100px;
  background: url("data:image/svg+xml,%3Csvg viewBox='0 0 1200 120' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M0,120 C150,20 300,20 600,60 C900,100 1050,100 1200,60 L1200,120 Z' fill='%23ffffff'/%3E%3C/svg%3E")
    repeat-x;
  background-size: 1200px 120px;
}

/* Features Section */
.features-section {
  padding: 6rem 0;
  background: white;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.section-title {
  text-align: center;
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 3rem;
  color: #2c3e50;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
}

.feature-card {
  background: white;
  padding: 2.5rem;
  border-radius: 20px;
  text-align: center;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(107, 142, 35, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
}

.feature-card:hover {
  box-shadow: 0 20px 40px rgba(107, 142, 35, 0.2);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 1.5rem;
}

.feature-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #333;
}

.feature-description {
  color: #666;
  line-height: 1.6;
}

/* Dashboard Section */
.dashboard-section {
  padding: 6rem 0;
  background: linear-gradient(135deg, #f8fffe 0%, #e8f5e8 100%);
}

.dashboard-preview {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
  max-width: 1000px;
  margin: 0 auto;
}

.dashboard-mockup {
  background: white;
  border-radius: 15px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.mockup-header {
  background: #f8f9fa;
  padding: 1rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  border-bottom: 1px solid #e9ecef;
}

.mockup-nav {
  display: flex;
  gap: 0.5rem;
}

.nav-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #dee2e6;
}

.nav-dot:first-child {
  background: #ff5f56;
}

.nav-dot:nth-child(2) {
  background: #ffbd2e;
}

.nav-dot:nth-child(3) {
  background: #27ca3f;
}

.mockup-title {
  color: #666;
  font-weight: 500;
}

.mockup-content {
  padding: 2rem;
  display: grid;
  gap: 1.5rem;
}

.chart-placeholder,
.map-placeholder {
  background: #f8f9fa;
  padding: 2rem;
  border-radius: 10px;
  text-align: center;
  border: 2px dashed #dee2e6;
}

.chart-icon,
.map-icon {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.dashboard-info h3 {
  font-size: 2rem;
  margin-bottom: 1rem;
  color: #333;
}

.dashboard-info p {
  color: #666;
  margin-bottom: 2rem;
  line-height: 1.6;
}

.dashboard-cta {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: linear-gradient(135deg, #6b8e23, #8fbc8f);
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 30px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.dashboard-cta:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(107, 142, 35, 0.4);
}

/* Statistics Section */
.stats-section {
  padding: 4rem 0;
  background: linear-gradient(135deg, #6b8e23, #8fbc8f);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
}

.stat-item {
  text-align: center;
  color: white;
}

.stat-number {
  font-size: 3rem;
  font-weight: 800;
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: 1.1rem;
  opacity: 0.9;
}

/* Impact Section */
.impact-section {
  padding: 6rem 0;
  background: white;
}

.impact-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
}

.impact-text h3 {
  font-size: 2rem;
  margin-bottom: 1.5rem;
  color: #333;
}

.impact-text p {
  color: #666;
  margin-bottom: 2rem;
  line-height: 1.6;
}

.impact-list {
  list-style: none;
  padding: 0;
}

.impact-list li {
  margin-bottom: 1rem;
  color: #666;
  font-size: 1.1rem;
}

.impact-visual {
  display: flex;
  justify-content: center;
  align-items: center;
}

.environment-animation {
  display: flex;
  gap: 2rem;
  font-size: 4rem;
  animation: bounce 2s ease-in-out infinite;
}

@keyframes bounce {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

/* Footer */
.footer {
  background: #2c3e50;
  color: white;
  padding: 3rem 0 1rem;
}

.footer-content {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 2rem;
  margin-bottom: 2rem;
}

.footer-brand {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.footer-logo {
  font-size: 3rem;
}

.footer-links {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
}

.footer-section h4 {
  margin-bottom: 1rem;
  color: #6b8e23;
}

.footer-section a {
  display: block;
  color: #bbb;
  text-decoration: none;
  margin-bottom: 0.5rem;
  cursor: pointer;
  transition: color 0.3s ease;
}

.footer-section a:hover {
  color: #6b8e23;
}

.footer-bottom {
  border-top: 1px solid #444;
  padding-top: 1rem;
  text-align: center;
  color: #bbb;
}

/* Responsive Design */
@media (max-width: 768px) {
  .nav-menu {
    flex-direction: column;
    gap: 1rem;
  }

  .hero-container {
    grid-template-columns: 1fr;
    text-align: center;
  }

  .hero-title {
    font-size: 2.5rem;
  }

  .dashboard-preview,
  .impact-content {
    grid-template-columns: 1fr;
  }

  .cta-button,
  .login-button {
    padding: 0.5rem 1rem;
    font-size: 0.8rem;
  }
}
</style>
