<template>
  <div class="flex min-h-screen bg-gray-50">
    <!-- Sidebar -->
    <Sidebar />

    <!-- Contenu principal -->
    <div class="flex-1 p-6 overflow-y-auto">
      <div class="max-w-7xl mx-auto">
        <!-- En-tête -->
        <div
          class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6"
          v-show="!isModalOpen"
        >
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <div class="w-8 h-8 text-green-600">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0..." />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </div>
              <div>
                <h1 class="text-2xl font-bold text-gray-900">Gestion des Règles de Classification</h1>
                <p class="text-gray-600">Gérez les règles d'analyse d'images pour la détection de poubelles</p>
              </div>
            </div>
            <div class="flex gap-3 flex-wrap">
              <button
                @click="exportRules"
                class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center gap-2 transition-colors"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M8 7H5a2 2 0 00-2 2v9a2 2 0..." />
                </svg>
                Exporter JSON
              </button>
              <button
                @click="saveRulesToServer"
                class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg flex items-center gap-2 transition-colors"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M17 16l4-4m0 0l-4-4m4 4H7" />
                </svg>
                Sauvegarder sur le serveur
              </button>
              <button
                @click="openModal()"
                class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg flex items-center gap-2 transition-colors"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                </svg>
                Nouvelle Règle
              </button>
            </div>
          </div>
    </div>

      <!-- Stats -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center gap-3">
            <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                      d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </div>
            <div>
              <p class="text-sm text-gray-600">Total des règles</p>
              <p class="text-2xl font-bold text-gray-900">{{ rules.length }}</p>
            </div>
          </div>
        </div>
        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center gap-3">
            <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <p class="text-sm text-gray-600">Règles actives</p>
              <p class="text-2xl font-bold text-gray-900">{{ activeRulesCount }}</p>
            </div>
          </div>
        </div>
        <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div class="flex items-center gap-3">
            <div class="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <p class="text-sm text-gray-600">Règles inactives</p>
              <p class="text-2xl font-bold text-gray-900">{{ inactiveRulesCount }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Rules List -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200">
        <div class="p-6 border-b border-gray-200">
          <h2 class="text-xl font-semibold text-gray-900">Liste des Règles</h2>
        </div>
        <div class="divide-y divide-gray-200">
          <div
            v-for="(rule, index) in rules"
            :key="index"
            :class="['p-6', { 'opacity-60': !rule.enabled }]"
          >
            <div class="flex items-start justify-between">
              <div class="flex-1">
                <div class="flex items-center gap-3 mb-2">
                  <span class="text-2xl">{{ getRuleTypeIcon(rule.name) }}</span>
                  <span :class="['px-3 py-1 rounded-full text-xs font-medium', getRuleTypeColor(rule.name)]">
                    {{ getRuleTypeLabel(rule.name) }}
                  </span>
                  <span v-if="rule.enabled" class="inline-flex items-center gap-1 text-green-600 text-sm">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                    </svg>
                    Active
                  </span>
                  <span v-else class="inline-flex items-center gap-1 text-gray-400 text-sm">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21" />
                    </svg>
                    Inactive
                  </span>
                </div>
                <h3 class="font-semibold text-gray-900 mb-1">{{ rule.name }}</h3>
                <p class="text-gray-600 mb-3">{{ rule.message }}</p>
                <div class="space-y-2">
                  <p class="text-sm font-medium text-gray-700">Conditions:</p>
                  <div
                    v-for="(condition, condIndex) in rule.conditions"
                    :key="condIndex"
                    class="flex items-center gap-2 text-sm bg-gray-50 p-2 rounded"
                  >
                    <span class="font-mono bg-blue-100 text-blue-800 px-2 py-1 rounded">
                      {{ condition.key }}
                    </span>
                    <span class="text-gray-600">{{ condition.op }}</span>
                    <span class="font-mono bg-purple-100 text-purple-800 px-2 py-1 rounded">
                      {{ condition.value }}
                    </span>
                  </div>
                </div>
              </div>
              <div class="flex items-center gap-2 ml-4">
                <button
                  @click="toggleRule(rule.name)"
                  :class="[
                    'p-2 rounded-lg transition-colors',
                    rule.enabled 
                      ? 'bg-green-100 text-green-600 hover:bg-green-200' 
                      : 'bg-gray-100 text-gray-400 hover:bg-gray-200'
                  ]"
                >
                  <svg v-if="rule.enabled" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                  <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21" />
                  </svg>
                </button>
                <button
                  @click="openModal(rule)"
                  class="p-2 bg-blue-100 text-blue-600 rounded-lg hover:bg-blue-200 transition-colors"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                </button>
                <button
                  @click="deleteRule(rule.name)"
                  class="p-2 bg-red-100 text-red-600 rounded-lg hover:bg-red-200 transition-colors"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Modal -->
      <div
        v-if="isModalOpen"
        class="fixed inset-0 bg-white/30 backdrop-blur-sm flex items-center justify-center z-50 p-4"
      >
        <div class="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto mx-auto">
          <div class="p-6 border-b border-gray-200">
            <div class="flex items-center justify-between">
              <h3 class="text-lg font-semibold text-gray-900">
                {{ editingRule ? 'Modifier la règle' : 'Nouvelle règle' }}
              </h3>
              <button
                @click="closeModal"
                class="p-2 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>
          
          <div class="p-6 space-y-6">
            <!-- Nom -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Nom de la règle *
              </label>
              <input
                v-model="newRule.name"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                placeholder="ex: poubelle_pleine_condition1"
              />
            </div>

            <!-- Message -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Message *
              </label>
              <input
                v-model="newRule.message"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                placeholder="ex: 💡 Poubelle pleine détectée"
              />
            </div>

            <!-- Statut -->
            <div>
              <label class="flex items-center gap-2">
                <input
                  v-model="newRule.enabled"
                  type="checkbox"
                  class="rounded text-green-600 focus:ring-green-500"
                />
                <span class="text-sm font-medium text-gray-700">Règle active</span>
              </label>
            </div>

            <!-- Conditions -->
            <div>
              <div class="flex items-center justify-between mb-3">
                <label class="block text-sm font-medium text-gray-700">
                  Conditions *
                </label>
                <button
                  @click="addCondition"
                  class="text-green-600 hover:text-green-700 text-sm flex items-center gap-1"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                  </svg>
                  Ajouter condition
                </button>
              </div>
              
              <div class="space-y-3">
                <div
                  v-for="(condition, index) in newRule.conditions"
                  :key="index"
                  class="flex items-center gap-3 p-3 bg-gray-50 rounded-lg"
                >
                  <select
                    v-model="condition.key"
                    class="px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  >
                    <option value="">Choisir...</option>
                    <option v-for="key in featureKeys" :key="key" :value="key">
                      {{ key }}
                    </option>
                  </select>
                  
                  <select
                    v-model="condition.op"
                    class="px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  >
                    <option v-for="op in operators" :key="op.value" :value="op.value">
                      {{ op.label }}
                    </option>
                  </select>
                  
                  <input
                    v-model.number="condition.value"
                    type="number"
                    step="0.01"
                    class="px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-green-500 focus:border-transparent"
                    placeholder="Valeur"
                  />
                  
                  <button
                    v-if="newRule.conditions.length > 1"
                    @click="removeCondition(index)"
                    class="p-2 text-red-600 hover:bg-red-100 rounded transition-colors"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <div class="p-6 border-t border-gray-200 flex justify-end gap-3">
            <button
              @click="closeModal"
              class="px-4 py-2 text-gray-600 hover:text-gray-800 transition-colors"
            >
              Annuler
            </button>
            <button
              @click="saveRule"
              class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
            >
              {{ editingRule ? 'Modifier' : 'Ajouter' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import Sidebar from '@/components/Sidebar.vue'
import { useUiStore } from '@/stores/ui'

export default {
    components: {
        Sidebar
    },
  name: 'RulesManagement',
  setup() {
    const ui = useUiStore()
    const rules = ref([])
    const isModalOpen = ref(false)
    const editingRule = ref(null)
    const newRule = ref({
      name: '',
      message: '',
      enabled: true,
      conditions: [{ key: '', op: '<=', value: '' }]
    })

    // Opérateurs disponibles
    const operators = [
      { value: '<', label: '< (inférieur)' },
      { value: '<=', label: '≤ (inférieur ou égal)' },
      { value: '>', label: '> (supérieur)' },
      { value: '>=', label: '≥ (supérieur ou égal)' },
      { value: '==', label: '= (égal)' },
      { value: '!=', label: '≠ (différent)' }
    ]

    // Clés de caractéristiques disponibles
    const featureKeys = [
      'contour_count',
      'mean_r',
      'mean_g', 
      'mean_b',
      'file_size',
      'brightness',
      'contrast',
      'saturation'
    ]

    // Computed properties
    const activeRulesCount = computed(() => rules.value.filter(r => r.enabled).length)
    const inactiveRulesCount = computed(() => rules.value.filter(r => !r.enabled).length)

    // Méthodes
    const loadInitialRules = async () => {
      try {
        const res = await fetch(`${import.meta.env.VITE_API_URL}/rules`)
        if (res.ok) {
          rules.value = await res.json()
        }
      } catch (e) {
        console.error('Erreur chargement des règles:', e)
      }
    }
    const saveRulesToServer = async () => {
      try {
        await fetch(`${import.meta.env.VITE_API_URL}/rules`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(rules.value)
        })
      } catch (e) {
        console.error('Erreur sauvegarde règles:', e)
      }
    }  
    const openModal = (rule = null) => {
      if (rule) {
        editingRule.value = rule
        newRule.value = { ...rule, conditions: [...rule.conditions] }
      } else {
        editingRule.value = null
        newRule.value = {
          name: '',
          message: '',
          enabled: true,
          conditions: [{ key: '', op: '<=', value: '' }]
        }
      }
      isModalOpen.value = true
      ui.showHeader = false
    }

    const closeModal = () => {
      isModalOpen.value = false
      ui.showHeader = true
      editingRule.value = null
      newRule.value = {
        name: '',
        message: '',
        enabled: true,
        conditions: [{ key: '', op: '<=', value: '' }]
      }
    }

    const saveRule = () => {
      if (!newRule.value.name || !newRule.value.message ||
          newRule.value.conditions.some(c => !c.key || c.value === '')) {
        alert('Veuillez remplir tous les champs obligatoires')
        return
      }

      if (editingRule.value) {
        // Modifier règle existante
        const index = rules.value.findIndex(rule => rule.name === editingRule.value.name)
        if (index !== -1) {
          rules.value[index] = { ...newRule.value }
        }
      } else {
        // Ajouter nouvelle règle
        rules.value.push({ ...newRule.value })
      }
      closeModal()
      saveRulesToServer()
    }

    const deleteRule = (ruleName) => {
      if (confirm('Êtes-vous sûr de vouloir supprimer cette règle ?')) {
        rules.value = rules.value.filter(rule => rule.name !== ruleName)
        saveRulesToServer()
      }
    }

    const toggleRule = (ruleName) => {
      const rule = rules.value.find(r => r.name === ruleName)
      if (rule) {
        rule.enabled = !rule.enabled
        saveRulesToServer()
      }
    }

    const addCondition = () => {
      newRule.value.conditions.push({ key: '', op: '<=', value: '' })
    }

    const removeCondition = (index) => {
      newRule.value.conditions.splice(index, 1)
    }

    const exportRules = () => {
      const dataStr = JSON.stringify(rules.value, null, 2)
      const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr)
      const exportFileDefaultName = 'rules.json'
      
      const linkElement = document.createElement('a')
      linkElement.setAttribute('href', dataUri)
      linkElement.setAttribute('download', exportFileDefaultName)
      linkElement.click()
    }

    const getRuleTypeColor = (ruleName) => {
      if (ruleName.includes('poubelle_pleine')) return 'bg-red-100 text-red-800'
      if (ruleName.includes('poubelle_vide')) return 'bg-green-100 text-green-800'
      return 'bg-gray-100 text-gray-800'
    }

    const getRuleTypeIcon = (ruleName) => {
      if (ruleName.includes('poubelle_pleine')) return '🗑️'
      if (ruleName.includes('poubelle_vide')) return '✅'
      return '📋'
    }

    const getRuleTypeLabel = (ruleName) => {
      if (ruleName.includes('poubelle_pleine')) return 'Poubelle Pleine'
      if (ruleName.includes('poubelle_vide')) return 'Poubelle Vide'
      return 'Autre'
    }

    // Lifecycle
    onMounted(() => {
      loadInitialRules()
    })
    return {
      rules,
      isModalOpen,
      editingRule,
      newRule,
      operators,
      featureKeys,
      activeRulesCount,
      inactiveRulesCount,
      openModal,
      closeModal,
      saveRule,
      deleteRule,
      toggleRule,
      addCondition,
      removeCondition,
      exportRules,
      saveRulesToServer,
      getRuleTypeColor,
      getRuleTypeIcon,
      getRuleTypeLabel,
      ui
    }
  }
}
</script>
