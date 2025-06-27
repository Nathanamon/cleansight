<template>
    <div class="home-page">
      <!-- Navigation Header -->
      <nav class="navbar">
        <div class="nav-container">
          <div class="nav-brand">
            <img src="@/assets/logo.png" alt="CleanSight Logo" class="logo" />
            <h1 class="brand-name">CleanSight</h1>
          </div>
          <div class="nav-menu" @click="toggleMobileMenu">
            <span class="nav-item" @click="scrollToSection('features')">Fonctionnalités</span>
            <span class="nav-item" @click="scrollToSection('how-it-works')">Comment ça marche</span>
            <span class="nav-item" @click="scrollToSection('impact')">Impact</span>
            <button class="cta-button" @click="scrollToSection('upload')">Commencer</button>
          </div>       </div>
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
              Prévenez les dépôts sauvages grâce à l'IA. Notre plateforme détecte automatiquement 
              l'état des poubelles pour une gestion optimisée des déchets urbains.
            </p>
            <div class="hero-buttons">
              <button class="primary-button" @click="scrollToSection('upload')">
                <span class="button-icon">📷</span>
                Analyser une Image
              </button>
              <button class="secondary-button" @click="scrollToSection('how-it-works')">
                <span class="button-icon">🎥</span>
                Voir la Démo
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
                <div class="detection-box">
                  🗑️ État: <strong>Pleine</strong>
                </div>
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
            <div class="feature-card" v-for="feature in features" :key="feature.id" 
                 @mouseenter="animateCard" @mouseleave="resetCard">
              <div class="feature-icon">{{ feature.icon }}</div>
              <h3 class="feature-title">{{ feature.title }}</h3>
              <p class="feature-description">{{ feature.description }}</p>
            </div>
          </div>
        </div>
      </section>
  
      <!-- How It Works Section -->
      <section id="how-it-works" class="how-it-works-section">
        <div class="container">
          <h2 class="section-title">Comment ça Marche</h2>
          <div class="steps-container">
            <div class="step" v-for="(step, index) in steps" :key="step.id" 
                 :class="{ active: activeStep === index }" @click="setActiveStep(index)">
              <div class="step-number">{{ index + 1 }}</div>
              <div class="step-content">
                <h3 class="step-title">{{ step.title }}</h3>
                <p class="step-description">{{ step.description }}</p>
              </div>
              <div class="step-visual">{{ step.icon }}</div>
            </div>
          </div>
        </div>
      </section>
  
      <!-- Statistics Section -->
      <section class="stats-section">
        <div class="container">
          <div class="stats-grid">
            <div class="stat-item" v-for="stat in statistics" :key="stat.id">
              <div class="stat-number" ref="statNumbers">{{ displayedStats[stat.id] }}</div>
              <div class="stat-label">{{ stat.label }}</div>
            </div>
          </div>
        </div>
      </section>
  
      <!-- Upload Section -->
      <section id="upload" class="upload-section">
        <div class="container">
          <h2 class="section-title">Testez Notre Solution</h2>
          <div class="upload-container">
            <div class="upload-area" 
                 :class="{ 'drag-over': isDragOver, 'uploading': isUploading }"
                 @drop="handleDrop" 
                 @dragover.prevent="isDragOver = true"
                 @dragleave="isDragOver = false"
                 @click="triggerFileInput">
              <input type="file" ref="fileInput" @change="handleFileSelect" accept="image/*" hidden>
              <div class="upload-content">
                <div class="upload-icon">📸</div>
                <p class="upload-text">
                  <span v-if="!isUploading">Glisser-déposer une image ou cliquer pour sélectionner</span>
                  <span v-else>Analyse en cours...</span>
                </p>
                <div class="upload-formats">Formats acceptés: JPG, PNG, WebP</div>
              </div>
              <div v-if="isUploading" class="upload-progress">
                <div class="progress-bar">
                  <div class="progress-fill" :style="{ width: uploadProgress + '%' }"></div>
                </div>
              </div>
            </div>
            
            <div v-if="analysisResult" class="analysis-result">
              <h3>Résultat de l'Analyse</h3>
              <div class="result-content">
                <div class="result-status" :class="analysisResult.status.toLowerCase()">
                  {{ analysisResult.status }}
                </div>
                <div class="result-confidence">
                  Confiance: {{ analysisResult.confidence }}%
                </div>
                <div class="result-details">
                  <div class="detail-item">
                    <span>Taille:</span> {{ analysisResult.fileSize }}
                  </div>
                  <div class="detail-item">
                    <span>Dimensions:</span> {{ analysisResult.dimensions }}
                  </div>
                  <div class="detail-item">
                    <span>Luminosité moyenne:</span> {{ analysisResult.brightness }}
                  </div>
                </div>
              </div>
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
                Notre plateforme s'inscrit dans une démarche Green IT et contribue directement 
                à la réduction de l'empreinte écologique urbaine en prévenant les dépôts sauvages 
                avant qu'ils ne se forment.
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
              <img src="@/assets/logo.png" alt="CleanSight Logo" class="footer-logo" />
              <p>Tous vigilants, tous propres</p>
            </div>
            <div class="footer-links">
              <div class="footer-section">
                <h4>Projet</h4>
                <a href="#" @click="scrollToSection('features')">Fonctionnalités</a>
                <a href="#" @click="scrollToSection('how-it-works')">Comment ça marche</a>
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
  import { ref, reactive, onMounted, nextTick } from 'vue'
  import { useRouter } from 'vue-router'
  export default {
    name: 'HomePage',
    setup() {
      const activeStep = ref(0)
      const isDragOver = ref(false)
      const isUploading = ref(false)
      const uploadProgress = ref(0)
      const analysisResult = ref(null)
      const fileInput = ref(null)
      const displayedStats = reactive({
        images: 0,
        accuracy: 0,
        reduction: 0,
        cities: 0
      })
  
      const features = [
        {
          id: 1,
          icon: '🎯',
          title: 'Détection Automatique',
          description: 'Analyse instantanée de l\'état des poubelles (vide, pleine, débordante) grâce à l\'IA'
        },
        {
          id: 2,
          icon: '🗺️',
          title: 'Cartographie Dynamique',
          description: 'Visualisation en temps réel des zones à risque de débordement sur une carte interactive'
        },
        {
          id: 3,
          icon: '📊',
          title: 'Tableau de Bord',
          description: 'Statistiques complètes et graphiques interactifs pour optimiser la gestion des déchets'
        },
        {
          id: 4,
          icon: '⚡',
          title: 'Prédiction Préventive',
          description: 'Anticipation des zones à risque pour une action préventive efficace'
        }
      ]
  
      const steps = [
        {
          id: 1,
          icon: '📸',
          title: 'Collecte d\'Images',
          description: 'Les citoyens, agents ou caméras embarquées capturent des images de poubelles'
        },
        {
          id: 2,
          icon: '🤖',
          title: 'Analyse IA',
          description: 'Notre algorithme analyse automatiquement l\'état de chaque poubelle'
        },
        {
          id: 3,
          icon: '📍',
          title: 'Géolocalisation',
          description: 'Les données sont enrichies avec localisation, date et métadonnées'
        },
        {
          id: 4,
          icon: '🚨',
          title: 'Alerte Préventive',
          description: 'Les services municipaux sont alertés avant que le problème ne s\'aggrave'
        }
      ]
  
      const statistics = [
        { id: 'images', value: 1247, label: 'Images Analysées' },
        { id: 'accuracy', value: 94, label: '% de Précision' },
        { id: 'reduction', value: 67, label: '% Réduction Dépôts' },
        { id: 'cities', value: 12, label: 'Villes Testées' }
      ]
  
      const scrollToSection = (sectionId) => {
        const element = document.getElementById(sectionId)
        if (element) {
          element.scrollIntoView({ behavior: 'smooth' })
        }
      }
  
      const setActiveStep = (index) => {
        activeStep.value = index
      }
  
      const animateCard = (event) => {
        event.currentTarget.style.transform = 'translateY(-10px) scale(1.02)'
      }
  
      const resetCard = (event) => {
        event.currentTarget.style.transform = 'translateY(0) scale(1)'
      }
  
      const triggerFileInput = () => {
        fileInput.value.click()
      }
  
      const handleFileSelect = (event) => {
        const file = event.target.files[0]
        if (file) {
          processFile(file)
        }
      }
  
      const handleDrop = (event) => {
        event.preventDefault()
        isDragOver.value = false
        const file = event.dataTransfer.files[0]
        if (file && file.type.startsWith('image/')) {
          processFile(file)
        }
      }
  
      const processFile = (file) => {
        isUploading.value = true
        uploadProgress.value = 0
        analysisResult.value = null
  
        // Simulate upload progress
        const progressInterval = setInterval(() => {
          uploadProgress.value += Math.random() * 30
          if (uploadProgress.value >= 100) {
            clearInterval(progressInterval)
            uploadProgress.value = 100
            
            // Simulate analysis result after upload
            setTimeout(() => {
              isUploading.value = false
              analysisResult.value = {
                status: Math.random() > 0.5 ? 'Pleine' : 'Vide',
                confidence: Math.floor(Math.random() * 20 + 80),
                fileSize: `${(file.size / 1024).toFixed(1)} KB`,
                dimensions: '800x600',
                brightness: Math.floor(Math.random() * 100 + 100)
              }
            }, 1000)
          }
        }, 200)
      }
  
      const animateStats = () => {
        statistics.forEach(stat => {
          let current = 0
          const increment = stat.value / 50
          const timer = setInterval(() => {
            current += increment
            if (current >= stat.value) {
              displayedStats[stat.id] = stat.value
              clearInterval(timer)
            } else {
              displayedStats[stat.id] = Math.floor(current)
            }
          }, 50)
        })
      }
  
      onMounted(() => {
        // Animate statistics when component mounts
        setTimeout(animateStats, 1000)
        
        // Auto-rotate steps every 3 seconds
        setInterval(() => {
          activeStep.value = (activeStep.value + 1) % steps.length
        }, 3000)
      })
  
      return {
        activeStep,
        isDragOver,
        isUploading,
        uploadProgress,
        analysisResult,
        fileInput,
        displayedStats,
        features,
        steps,
        statistics,
        scrollToSection,
        setActiveStep,
        animateCard,
        resetCard,
        triggerFileInput,
        handleFileSelect,
        handleDrop
      }
    }
  }
  </script>
 <style scoped>
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }
  
  .home-page {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
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
  
  .logo {
    height: 40px;
    width: auto;
  }
  
  .brand-name {
    font-size: 1.5rem;
    font-weight: 700;
    color: #6B8E23;
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
  }
  
  .nav-item:hover {
    color: #6B8E23;
  }
  
  .cta-button {
    background: linear-gradient(135deg, #6B8E23, #8FBC8F);
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 25px;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.3s ease;
  }
  
  .cta-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(107, 142, 35, 0.3);
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
    color: #6B8E23;
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
  
  .primary-button, .secondary-button {
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
    background: linear-gradient(135deg, #6B8E23, #8FBC8F);
    color: white;
  }
  
  .primary-button:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(107, 142, 35, 0.4);
  }
  
  .secondary-button {
    background: white;
    color: #6B8E23;
    border: 2px solid #6B8E23;
  }
  
  .secondary-button:hover {
    background: #6B8E23;
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
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-20px); }
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
    0% { opacity: 1; }
    50% { opacity: 0.5; }
    100% { opacity: 1; }
  }
  
  .detection-box {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 10px;
    margin-bottom: 0.5rem;
    font-size: 1.1rem;
  }
  
  .location, .timestamp {
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
    background: url("data:image/svg+xml,%3Csvg viewBox='0 0 1200 120' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M0,120 C150,20 300,20 600,60 C900,100 1050,100 1200,60 L1200,120 Z' fill='%23ffffff'/%3E%3C/svg%3E") repeat-x;
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
  
  /* How It Works Section */
  .how-it-works-section {
    padding: 6rem 0;
    background: linear-gradient(135deg, #f8fffe 0%, #e8f5e8 100%);
  }
  
  .steps-container {
    display: grid;
    gap: 2rem;
  }
  
  .step {
    display: grid;
    grid-template-columns: 80px 1fr 100px;
    gap: 2rem;
    align-items: center;
    background: white;
    padding: 2rem;
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    cursor: pointer;
    transition: all 0.3s ease;
    border: 2px solid transparent;
  }
  
  .step.active {
    border-color: #6B8E23;
    transform: scale(1.02);
  }
  
  .step-number {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background: linear-gradient(135deg, #6B8E23, #8FBC8F);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    font-weight: 700;
  }
  
  .step-title {
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: #333;
  }
  
  .step-description {
    color: #666;
    line-height: 1.6;
  }
  
  .step-visual {
    font-size: 3rem;
    text-align: center;
  }
  
  /* Statistics Section */
  .stats-section {
    padding: 4rem 0;
    background: linear-gradient(135deg, #6B8E23, #8FBC8F);
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
  
  /* Upload Section */
  .upload-section {
    padding: 6rem 0;
    background: white;
  }
  
  .upload-container {
    max-width: 800px;
    margin: 0 auto;
  }
  
  .upload-area {
    border: 3px dashed #ddd;
    border-radius: 20px;
    padding: 4rem 2rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
  }
  
  .upload-area:hover,
  .upload-area.drag-over {
    border-color: #6B8E23;
    background: rgba(107, 142, 35, 0.05);
  }
  
  .upload-area.uploading {
    border-color: #6B8E23;
    background: rgba(107, 142, 35, 0.1);
  }
  
  .upload-icon {
    font-size: 4rem;
    margin-bottom: 1rem;
  }
  
  .upload-text {
    font-size: 1.25rem;
    color: #333;
    margin-bottom: 1rem;
  }
  
  .upload-formats {
    color: #666;
    font-size: 0.9rem;
  }
  
  .upload-progress {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 6px;
    background: rgba(0, 0, 0, 0.1);
  }
  
  .progress-bar {
    height: 100%;
    background: #f0f0f0;
  }
  
  .progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #6B8E23, #8FBC8F);
    transition: width 0.3s ease;
  }
  
  .analysis-result {
    margin-top: 2rem;
    background: #f8f9fa;
    padding: 2rem;
    border-radius: 15px;
    border: 1px solid #e9ecef;
  }
  
  .analysis-result h3 {
    margin-bottom: 1.5rem;
    color: #333;
  }
  
  .result-content {
    display: grid;
    gap: 1rem;
  }
  
  .result-status {
    font-size: 1.5rem;
    font-weight: 700;
    padding: 0.5rem 1rem;
    border-radius: 10px;
    text-align: center;
  }
  
  .result-status.pleine {
    background: #ffebee;
    color: #c62828;
  }
  
  .result-status.vide {
    background: #e8f5e9;
    color: #2e7d32;
  }
  
  .result-confidence {
    font-size: 1.25rem;
    text-align: center;
    color: #666;
  }
  
  .result-details {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 1rem;
    margin-top: 1rem;
  }
  
  .detail-item {
    background: white;
    padding: 1rem;
    border-radius: 10px;
    text-align: center;
  }
  
  .detail-item span {
    display: block;
    font-weight: 600;
    color: #333;
    margin-bottom: 0.5rem;
  }
  
  /* Impact Section */
  .impact-section {
    padding: 6rem 0;
    background: linear-gradient(135deg, #f8fffe 0%, #e8f5e8 100%);
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
</style scoped>