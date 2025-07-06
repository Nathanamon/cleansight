import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const csrfToken = ref(null)

  function login(userData, token) {
    user.value = userData
    csrfToken.value = token
    localStorage.setItem('authToken', 'true')
    localStorage.setItem('userData', JSON.stringify(userData))
    if (token) {
      localStorage.setItem('csrfToken', token)
    }
  }

  function restoreFromLocalStorage() {
    const token = localStorage.getItem('csrfToken')
    const u = localStorage.getItem('userData')
    if (token) csrfToken.value = token
    if (u) {
      try {
        user.value = JSON.parse(u)
      } catch {
        user.value = null
      }
    }
  }

  function logout() {
    user.value = null
    csrfToken.value = null
    localStorage.removeItem('authToken')
    localStorage.removeItem('csrfToken')
    localStorage.removeItem('userData')
  }

  return { user, csrfToken, login, restoreFromLocalStorage, logout }
})