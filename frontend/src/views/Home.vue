<script setup lang="ts">
import { onMounted } from 'vue'
import { useLearningStore } from '../stores/learning'
import StatsBar from '../components/StatsBar.vue'
import LearningForm from '../components/LearningForm.vue'
import LearningList from '../components/LearningList.vue'

const store = useLearningStore()

onMounted(async () => {
  await store.fetchItems()
  await store.fetchStats()
})

async function handleAddItem(title: string, content: string, category: string) {
  await store.addItem(title, content, category)
}

async function handleReview(id: number) {
  await store.reviewItem(id)
}

async function handleDelete(id: number) {
  if (confirm('确定要删除这条学习内容吗？')) {
    await store.deleteItem(id)
  }
}
</script>

<template>
  <div class="home-page">
    <header class="page-header">
      <h1 class="page-title">欢迎回来</h1>
      <p class="page-subtitle">今天也要坚持复习哦</p>
    </header>

    <StatsBar :stats="store.stats" />

    <div class="home-grid">
      <section class="add-section">
        <LearningForm @submit="handleAddItem" />
      </section>

      <section class="review-section">
        <h2 class="section-title">
          <span v-if="store.dueTodayItems.length > 0" class="due-badge">
            {{ store.dueTodayItems.length }} 条待复习
          </span>
          <span v-else>今日复习完成</span>
        </h2>

        <div v-if="store.error" class="error-message">
          {{ store.error }}
        </div>

        <LearningList
          :items="store.dueTodayItems.length > 0 ? store.dueTodayItems : store.items.slice(0, 5)"
          :loading="store.loading"
          @review="handleReview"
          @delete="handleDelete"
        />
      </section>
    </div>
  </div>
</template>

<style scoped>
.home-page {
  padding: 32px;
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 32px;
}

.page-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 8px;
}

.page-subtitle {
  color: #64748b;
  font-size: 1.1rem;
}

.home-grid {
  display: grid;
  grid-template-columns: 400px 1fr;
  gap: 32px;
}

.section-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.due-badge {
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: white;
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 500;
}

.error-message {
  background: #fee2e2;
  color: #dc2626;
  padding: 12px 16px;
  border-radius: 8px;
  margin-bottom: 16px;
  font-size: 0.9rem;
}

@media (max-width: 1024px) {
  .home-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .home-page {
    padding: 20px;
  }

  .page-title {
    font-size: 1.5rem;
  }
}
</style>
