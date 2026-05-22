import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { apiClient, type LearningItem, type Stats } from '../api'

export const useLearningStore = defineStore('learning', () => {
  const items = ref<LearningItem[]>([])
  const stats = ref<Stats>({ total_items: 0, pending_today: 0, completed_all: 0, categories_count: 0 })
  const loading = ref(false)
  const error = ref<string | null>(null)

  const dueTodayItems = computed(() =>
    items.value.filter(item => item.status === 'due_today')
  )

  const completedItems = computed(() =>
    items.value.filter(item => item.status === 'completed')
  )

  const pendingItems = computed(() =>
    items.value.filter(item => item.status === 'pending')
  )

  const categories = computed(() => {
    const cats = new Set(items.value.map(item => item.category))
    return ['全部', ...Array.from(cats)]
  })

  async function fetchItems(category?: string) {
    loading.value = true
    error.value = null
    try {
      items.value = await apiClient.items.getAll(category)
    } catch (e: any) {
      error.value = '获取数据失败，请检查后端服务是否运行'
      console.error(e)
    } finally {
      loading.value = false
    }
  }

  async function fetchStats() {
    try {
      stats.value = await apiClient.stats.get()
    } catch (e) {
      console.error(e)
    }
  }

  async function addItem(title: string, content: string, category: string = '默认') {
    loading.value = true
    error.value = null
    try {
      const newItem = await apiClient.items.create(title, content, category)
      items.value.unshift(newItem)
      await fetchStats()
    } catch (e: any) {
      error.value = e.response?.data?.detail || '添加失败，请重试'
      console.error(e)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function updateItem(id: number, data: { title?: string; content?: string; category?: string }) {
    try {
      const updatedItem = await apiClient.items.update(id, data)
      const index = items.value.findIndex(item => item.id === id)
      if (index !== -1) {
        items.value[index] = updatedItem
      }
      return updatedItem
    } catch (e: any) {
      error.value = e.response?.data?.detail || '更新失败，请重试'
      console.error(e)
      throw e
    }
  }

  async function deleteItem(id: number) {
    try {
      await apiClient.items.delete(id)
      items.value = items.value.filter(item => item.id !== id)
      await fetchStats()
    } catch (e: any) {
      error.value = e.response?.data?.detail || '删除失败，请重试'
      console.error(e)
      throw e
    }
  }

  async function reviewItem(id: number) {
    try {
      const updatedItem = await apiClient.items.review(id)
      const index = items.value.findIndex(item => item.id === id)
      if (index !== -1) {
        items.value[index] = updatedItem
      }
      await fetchStats()
      return updatedItem
    } catch (e: any) {
      error.value = e.response?.data?.detail || '复习记录失败，请重试'
      console.error(e)
      throw e
    }
  }

  return {
    items,
    stats,
    loading,
    error,
    dueTodayItems,
    completedItems,
    pendingItems,
    categories,
    fetchItems,
    fetchStats,
    addItem,
    updateItem,
    deleteItem,
    reviewItem,
  }
})
