<script setup lang="ts">
import LearningItem from './LearningItem.vue'
import type { LearningItem as LearningItemType } from '../api'

defineProps<{
  items: LearningItemType[]
  loading?: boolean
}>()

const emit = defineEmits<{
  review: [id: number]
  delete: [id: number]
}>()
</script>

<template>
  <div class="learning-list">
    <div v-if="loading && items.length === 0" class="loading">
      <div class="spinner"></div>
      <p>加载中...</p>
    </div>

    <div v-else-if="items.length === 0" class="empty-state">
      <div class="empty-icon">📚</div>
      <h3>还没有学习内容</h3>
      <p>添加你的第一个学习内容，开始艾宾浩斯复习之旅</p>
    </div>

    <div v-else class="items-grid">
      <LearningItem
        v-for="item in items"
        :key="item.id"
        :item="item"
        @review="emit('review', $event)"
        @delete="emit('delete', $event)"
      />
    </div>
  </div>
</template>

<style scoped>
.learning-list {
  min-height: 200px;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: #64748b;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #e2e8f0;
  border-top-color: #4f46e5;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 12px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 16px;
}

.empty-state h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #475569;
  margin: 0 0 8px;
}

.empty-state p {
  color: #94a3b8;
  font-size: 0.95rem;
  margin: 0;
  max-width: 280px;
}

.items-grid {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
</style>
