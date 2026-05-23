<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from './stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const navItems = [
  { path: '/', label: '首页', icon: '🏠' },
  { path: '/knowledge', label: '知识管理', icon: '📚' },
  { path: '/analytics', label: '数据分析', icon: '📊' },
]

const isActive = (path: string) => route.path === path

function handleLogout() {
  authStore.logout()
  router.push('/login')
}
</script>

<template>
  <div class="app-layout">
    <aside class="sidebar">
      <div class="sidebar-header">
        <h1 class="logo">艾宾浩斯</h1>
        <span class="logo-subtitle">复习助手</span>
      </div>

      <nav class="sidebar-nav">
        <router-link
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          :class="['nav-item', { active: isActive(item.path) }]"
        >
          <span class="nav-icon">{{ item.icon }}</span>
          <span class="nav-label">{{ item.label }}</span>
        </router-link>
      </nav>

      <div class="sidebar-footer">
        <div class="user-info">
          <span class="user-name">{{ authStore.user?.username }}</span>
          <span class="user-email">{{ authStore.user?.email }}</span>
        </div>
        <button @click="handleLogout" class="logout-btn">
          退出登录
        </button>
      </div>
    </aside>

    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<style scoped>
.app-layout {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 260px;
  background: linear-gradient(180deg, #1e1b4b 0%, #312e81 100%);
  color: white;
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
}

.sidebar-header {
  padding: 32px 24px;
  text-align: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo {
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0;
  background: linear-gradient(135deg, #a78bfa, #818cf8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.logo-subtitle {
  display: block;
  font-size: 0.8rem;
  opacity: 0.7;
  margin-top: 4px;
}

.sidebar-nav {
  flex: 1;
  padding: 24px 16px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  border-radius: 10px;
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  transition: all 0.2s ease;
  margin-bottom: 8px;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

.nav-item.active {
  background: rgba(255, 255, 255, 0.15);
  color: white;
}

.nav-icon {
  font-size: 1.25rem;
}

.nav-label {
  font-weight: 500;
}

.sidebar-footer {
  padding: 24px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.user-info {
  margin-bottom: 16px;
}

.user-name {
  display: block;
  font-weight: 600;
  margin-bottom: 4px;
}

.user-email {
  display: block;
  font-size: 0.8rem;
  opacity: 0.6;
}

.logout-btn {
  width: 100%;
  padding: 10px 16px;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background 0.2s ease;
}

.logout-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.main-content {
  flex: 1;
  margin-left: 260px;
  background: #f8fafc;
  min-height: 100vh;
}

@media (max-width: 768px) {
  .sidebar {
    width: 100%;
    height: auto;
    position: fixed;
    bottom: 0;
    top: auto;
    flex-direction: row;
  }

  .sidebar-header,
  .sidebar-footer {
    display: none;
  }

  .sidebar-nav {
    display: flex;
    justify-content: space-around;
    padding: 8px;
    width: 100%;
  }

  .nav-item {
    flex-direction: column;
    padding: 8px;
    margin: 0;
    font-size: 0.75rem;
  }

  .nav-icon {
    font-size: 1.25rem;
  }

  .main-content {
    margin-left: 0;
    margin-bottom: 80px;
  }
}
</style>
