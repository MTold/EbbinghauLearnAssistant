import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { apiClient, type User, type AuthResponse } from '../api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  const isLoggedIn = computed(() => !!token.value && !!user.value)

  function initFromStorage() {
    const savedToken = localStorage.getItem('token')
    const savedUser = localStorage.getItem('user')

    if (savedToken && savedUser) {
      try {
        token.value = savedToken
        user.value = JSON.parse(savedUser)
      } catch {
        logout()
      }
    }
  }

  async function register(username: string, email: string, password: string) {
    loading.value = true
    error.value = null

    try {
      const response: AuthResponse = await apiClient.auth.register(username, email, password)
      setAuth(response)
      return true
    } catch (e: any) {
      error.value = e.response?.data?.detail || '注册失败，请重试'
      return false
    } finally {
      loading.value = false
    }
  }

  async function login(username: string, password: string) {
    loading.value = true
    error.value = null

    try {
      const response: AuthResponse = await apiClient.auth.login(username, password)
      setAuth(response)
      return true
    } catch (e: any) {
      error.value = e.response?.data?.detail || '登录失败，请检查用户名和密码'
      return false
    } finally {
      loading.value = false
    }
  }

  function setAuth(response: AuthResponse) {
    token.value = response.access_token
    user.value = response.user
    localStorage.setItem('token', response.access_token)
    localStorage.setItem('user', JSON.stringify(response.user))
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  async function fetchCurrentUser() {
    if (!token.value) return false

    try {
      const userData = await apiClient.auth.getMe()
      user.value = userData
      localStorage.setItem('user', JSON.stringify(userData))
      return true
    } catch {
      logout()
      return false
    }
  }

  return {
    user,
    token,
    loading,
    error,
    isLoggedIn,
    initFromStorage,
    register,
    login,
    logout,
    fetchCurrentUser,
  }
})
