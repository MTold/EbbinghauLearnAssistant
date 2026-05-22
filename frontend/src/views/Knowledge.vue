<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useLearningStore } from '../stores/learning'
import LearningItem from '../components/LearningItem.vue'

const store = useLearningStore()

const selectedCategory = ref('全部')
const searchQuery = ref('')
const editingItem = ref<number | null>(null)
const editForm = ref({ title: '', content: '', category: '' })

onMounted(async () => {
  await store.fetchItems()
  await store.fetchStats()
})

watch(selectedCategory, async () => {
  await store.fetchItems(selectedCategory.value === '全部' ? undefined : selectedCategory.value)
})

const filteredItems = computed(() => {
  if (!searchQuery.value) return store.items
  const query = searchQuery.value.toLowerCase()
  return store.items.filter(
    item =>
      item.title.toLowerCase().includes(query) ||
      item.content.toLowerCase().includes(query)
  )
})

function startEdit(item: typeof store.items[0]) {
  editingItem.value = item.id
  editForm.value = {
    title: item.title,
    content: item.content,
    category: item.category,
  }
}

function cancelEdit() {
  editingItem.value = null
  editForm.value = { title: '', content: '', category: '' }
}

async function saveEdit(id: number) {
  await store.updateItem(id, editForm.value)
  cancelEdit()
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
  <div class="knowledge-page">
    <header class="page-header">
      <h1 class="page-title">知识管理</h1>
      <p class="page-subtitle">管理所有学习内容</p>
    </header>

    <div class="toolbar">
      <div class="search-box">
        <input
          v-model="searchQuery"
          type="text"
          class="search-input"
          placeholder="搜索学习内容..."
        />
      </div>

      <div class="category-tabs">
        <button
          v-for="cat in store.categories"
          :key="cat"
          :class="['category-tab', { active: selectedCategory === cat }]"
          @click="selectedCategory = cat"
        >
          {{ cat }}
        </button>
      </div>
    </div>

    <div class="knowledge-stats">
      <div class="stat-item">
        <span class="stat-value">{{ store.items.length }}</span>
        <span class="stat-label">总计</span>
      </div>
      <div class="stat-item stat-due">
        <span class="stat-value">{{ store.dueTodayItems.length }}</span>
        <span class="stat-label">待复习</span>
      </div>
      <div class="stat-item stat-completed">
        <span class="stat-value">{{ store.completedItems.length }}</span>
        <span class="stat-label">已完成</span>
      </div>
    </div>

    <div v-if="store.error" class="error-message">
      {{ store.error }}
    </div>

    <div v-if="loading && store.items.length === 0" class="loading">
      <div class="spinner"></div>
      <p>加载中...</p>
    </div>

    <div v-else-if="filteredItems.length === 0" class="empty-state">
      <div class="empty-icon">📚</div>
      <h3>暂无学习内容</h3>
      <p>去首页添加新的学习内容吧</p>
    </div>

    <div v-else class="items-list">
      <div v-for="item in filteredItems" :key="item.id" class="item-wrapper">
        <template v-if="editingItem === item.id">
          <div class="edit-form">
            <input
              v-model="editForm.title"
              type="text"
              class="edit-input"
              placeholder="标题"
            />
            <textarea
              v-model="editForm.content"
              class="edit-textarea"
              placeholder="内容"
              rows="3"
            ></textarea>
            <input
              v-model="editForm.category"
              type="text"
              class="edit-input"
              placeholder="分类"
            />
            <div class="edit-actions">
              <button @click="saveEdit(item.id)" class="btn-save">保存</button>
              <button @click="cancelEdit" class="btn-cancel">取消</button>
            </div>
          </div>
        </template>
        <template v-else>
          <LearningItem
            :item="item"
            @review="handleReview"
            @delete="handleDelete"
          />
          <button @click="startEdit(item)" class="btn-edit">
            编辑
          </button>
        </template>
      </div>
    </div>
  </div>
</template>

<style scoped>
.knowledge-page {
  padding: 32px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 24px;
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

.toolbar {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.search-box {
  flex: 1;
  min-width: 200px;
}

.search-input {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 10px;
  font-size: 0.95rem;
  transition: all 0.2s ease;
}

.search-input:focus {
  outline: none;
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.category-tabs {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.category-tab {
  padding: 10px 16px;
  background: #fff;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.category-tab:hover {
  border-color: #cbd5e1;
}

.category-tab.active {
  background: #4f46e5;
  border-color: #4f46e5;
  color: white;
}

.knowledge-stats {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
}

.stat-item {
  background: #fff;
  padding: 16px 24px;
  border-radius: 12px;
  text-align: center;
  border: 1px solid #e2e8f0;
}

.stat-value {
  display: block;
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
}

.stat-label {
  font-size: 0.85rem;
  color: #64748b;
}

.stat-due {
  background: #fffbeb;
  border-color: #f59e0b;
}

.stat-due .stat-value {
  color: #d97706;
}

.stat-completed {
  background: #ecfdf5;
  border-color: #10b981;
}

.stat-completed .stat-value {
  color: #059669;
}

.error-message {
  background: #fee2e2;
  color: #dc2626;
  padding: 12px 16px;
  border-radius: 8px;
  margin-bottom: 16px;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 60px;
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
  to { transform: rotate(360deg); }
}

.empty-state {
  text-align: center;
  padding: 60px;
  background: #fff;
  border-radius: 16px;
  border: 2px dashed #e2e8f0;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 16px;
}

.empty-state h3 {
  color: #475569;
  margin-bottom: 8px;
}

.empty-state p {
  color: #94a3b8;
}

.items-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.item-wrapper {
  position: relative;
}

.btn-edit {
  position: absolute;
  top: 20px;
  right: 20px;
  padding: 8px 16px;
  background: #e2e8f0;
  color: #475569;
  border: none;
  border-radius: 6px;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-edit:hover {
  background: #cbd5e1;
}

.edit-form {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  border: 2px solid #4f46e5;
}

.edit-input,
.edit-textarea {
  width: 100%;
  padding: 12px;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  margin-bottom: 12px;
  font-size: 0.95rem;
  font-family: inherit;
}

.edit-input:focus,
.edit-textarea:focus {
  outline: none;
  border-color: #4f46e5;
}

.edit-actions {
  display: flex;
  gap: 8px;
}

.btn-save {
  padding: 10px 20px;
  background: #4f46e5;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
}

.btn-cancel {
  padding: 10px 20px;
  background: #e2e8f0;
  color: #475569;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
}

@media (max-width: 768px) {
  .knowledge-page {
    padding: 20px;
  }

  .toolbar {
    flex-direction: column;
  }
}
</style>
