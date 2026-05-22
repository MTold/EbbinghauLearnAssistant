<script setup lang="ts">
import { computed } from 'vue'
import type { LearningItem } from '../api'

const props = defineProps<{
  item: LearningItem
}>()

const emit = defineEmits<{
  review: [id: number]
  delete: [id: number]
}>()

const statusLabel = computed(() => {
  switch (props.item.status) {
    case 'due_today':
      return '今日待复习'
    case 'completed':
      return '已完成'
    default:
      return '待复习'
  }
})

const statusClass = computed(() => {
  switch (props.item.status) {
    case 'due_today':
      return 'status-due'
    case 'completed':
      return 'status-completed'
    default:
      return 'status-pending'
  }
})

const progressText = computed(() => {
  return `${props.item.review_count} / ${props.item.total_reviews}`
})

const progressPercent = computed(() => {
  return (props.item.review_count / props.item.total_reviews) * 100
})

const nextReviewText = computed(() => {
  if (props.item.status === 'completed') {
    return '全部复习完成'
  }
  const next = new Date(props.item.next_review_at)
  const now = new Date()
  const diff = Math.ceil((next.getTime() - now.getTime()) / (1000 * 60 * 60 * 24))

  if (diff <= 0) {
    return '今日'
  } else if (diff === 1) {
    return '明天'
  } else {
    return `${diff} 天后`
  }
})

function formatDate(dateStr: string): string {
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', {
    month: 'short',
    day: 'numeric',
  })
}
</script>

<template>
  <div :class="['learning-item', statusClass]">
    <div class="item-header">
      <h3 class="item-title">{{ item.title }}</h3>
      <span :class="['status-badge', statusClass]">{{ statusLabel }}</span>
    </div>

    <p class="item-content">{{ item.content }}</p>

    <div class="progress-section">
      <div class="progress-bar">
        <div class="progress-fill" :style="{ width: progressPercent + '%' }"></div>
      </div>
      <span class="progress-text">{{ progressText }}</span>
    </div>

    <div class="item-footer">
      <span class="next-review">下次复习: {{ nextReviewText }}</span>
      <span class="created-date">添加于 {{ formatDate(item.created_at) }}</span>
    </div>

    <div class="item-actions">
      <button
        v-if="item.status !== 'completed'"
        @click="emit('review', item.id)"
        class="btn-review"
      >
        {{ item.status === 'due_today' ? '立即复习' : '提前复习' }}
      </button>
      <button @click="emit('delete', item.id)" class="btn-delete">
        删除
      </button>
    </div>
  </div>
</template>

<style scoped>
.learning-item {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  border: 2px solid #e2e8f0;
  transition: all 0.2s ease;
}

.learning-item:hover {
  border-color: #cbd5e1;
}

.learning-item.status-due {
  border-color: #f59e0b;
  background: linear-gradient(135deg, #fffbeb 0%, #fff 100%);
}

.learning-item.status-completed {
  border-color: #10b981;
  background: linear-gradient(135deg, #ecfdf5 0%, #fff 100%);
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.item-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
  flex: 1;
}

.status-badge {
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 500;
}

.status-badge.status-due {
  background: #fef3c7;
  color: #d97706;
}

.status-badge.status-completed {
  background: #d1fae5;
  color: #059669;
}

.status-badge.status-pending {
  background: #e2e8f0;
  color: #64748b;
}

.item-content {
  color: #64748b;
  font-size: 0.9rem;
  line-height: 1.5;
  margin: 0 0 16px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.progress-section {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.progress-bar {
  flex: 1;
  height: 8px;
  background: #e2e8f0;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #4f46e5, #7c3aed);
  border-radius: 4px;
  transition: width 0.3s ease;
}

.status-completed .progress-fill {
  background: linear-gradient(90deg, #10b981, #059669);
}

.progress-text {
  font-size: 0.8rem;
  color: #64748b;
  font-weight: 500;
  min-width: 50px;
  text-align: right;
}

.item-footer {
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
  color: #94a3b8;
  margin-bottom: 16px;
}

.item-actions {
  display: flex;
  gap: 8px;
}

.btn-review {
  flex: 1;
  padding: 10px 16px;
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-review:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.4);
}

.btn-delete {
  padding: 10px 16px;
  background: #fee2e2;
  color: #dc2626;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-delete:hover {
  background: #fecaca;
}
</style>
