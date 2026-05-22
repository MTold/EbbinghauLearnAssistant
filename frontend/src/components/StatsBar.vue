<script setup lang="ts">
import type { Stats } from '../api'

defineProps<{
  stats: Stats
}>()
</script>

<template>
  <div class="stats-bar">
    <div class="stat-card">
      <div class="stat-icon stat-icon-total">📚</div>
      <div class="stat-content">
        <span class="stat-value">{{ stats.total_items }}</span>
        <span class="stat-label">总学习</span>
      </div>
    </div>

    <div class="stat-card stat-card-highlight">
      <div class="stat-icon stat-icon-due">🔥</div>
      <div class="stat-content">
        <span class="stat-value">{{ stats.pending_today }}</span>
        <span class="stat-label">今日待复习</span>
      </div>
    </div>

    <div class="stat-card">
      <div class="stat-icon stat-icon-done">✅</div>
      <div class="stat-content">
        <span class="stat-value">{{ stats.completed_all }}</span>
        <span class="stat-label">已完成</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.stats-bar {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 14px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
}

.stat-card-highlight {
  background: linear-gradient(135deg, #fef3c7, #fff);
  border-color: #f59e0b;
}

.stat-icon {
  font-size: 1.75rem;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
}

.stat-icon-total {
  background: #ede9fe;
}

.stat-icon-due {
  background: #fee2e2;
}

.stat-icon-done {
  background: #d1fae5;
}

.stat-content {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  line-height: 1.2;
}

.stat-label {
  font-size: 0.8rem;
  color: #64748b;
}

@media (max-width: 640px) {
  .stats-bar {
    grid-template-columns: 1fr;
  }
}
</style>
