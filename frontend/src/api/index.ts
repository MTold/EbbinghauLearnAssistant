import axios from 'axios'

const api = axios.create({
  baseURL: 'http://118.25.178.241:8000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export interface User {
  id: number
  username: string
  email: string
  created_at: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
  user: User
}

export interface LearningItem {
  id: number
  title: string
  content: string
  category: string
  created_at: string
  review_count: number
  last_reviewed_at: string | null
  next_review_at: string
  status: 'pending' | 'due_today' | 'completed'
  total_reviews: number
}

export interface ReviewLog {
  id: number
  item_id: number
  reviewed_at: string
  was_on_time: boolean
}

export interface Stats {
  total_items: number
  pending_today: number
  completed_all: number
  categories_count: number
}

export interface CategoryDistribution {
  [key: string]: number
}

export interface OverviewStats {
  total_items: number
  total_reviews: number
  on_time_reviews: number
  late_reviews: number
  due_today: number
  completed: number
  pending: number
  category_distribution: CategoryDistribution
}

export interface TrendDataPoint {
  date: string
  count: number
}

export interface TrendsResponse {
  learning_trend: TrendDataPoint[]
  review_trend: TrendDataPoint[]
  on_time_rate: number
}

export const apiClient = {
  auth: {
    register: async (username: string, email: string, password: string): Promise<AuthResponse> => {
      const response = await api.post('/auth/register', { username, email, password })
      return response.data
    },
    login: async (username: string, password: string): Promise<AuthResponse> => {
      const response = await api.post('/auth/login', { username, password })
      return response.data
    },
    getMe: async (): Promise<User> => {
      const response = await api.get('/auth/me')
      return response.data
    },
  },

  items: {
    getAll: async (category?: string): Promise<LearningItem[]> => {
      const params = category && category !== '全部' ? { category } : {}
      const response = await api.get('/items', { params })
      return response.data
    },
    create: async (title: string, content: string, category: string): Promise<LearningItem> => {
      const response = await api.post('/items', { title, content, category })
      return response.data
    },
    update: async (id: number, data: { title?: string; content?: string; category?: string }): Promise<LearningItem> => {
      const response = await api.put(`/items/${id}`, data)
      return response.data
    },
    delete: async (id: number): Promise<void> => {
      await api.delete(`/items/${id}`)
    },
    review: async (id: number): Promise<LearningItem> => {
      const response = await api.post(`/items/${id}/review`)
      return response.data
    },
    getLogs: async (id: number): Promise<ReviewLog[]> => {
      const response = await api.get(`/items/${id}/logs`)
      return response.data
    },
  },

  stats: {
    get: async (): Promise<Stats> => {
      const response = await api.get('/stats')
      return response.data
    },
    getOverview: async (): Promise<OverviewStats> => {
      const response = await api.get('/stats/overview')
      return response.data
    },
    getTrends: async (days: number = 30): Promise<TrendsResponse> => {
      const response = await api.get('/stats/trends', { params: { days } })
      return response.data
    },
  },
}
