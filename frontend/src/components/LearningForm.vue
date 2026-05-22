<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits<{
  submit: [title: string, content: string, category: string]
}>()

const title = ref('')
const content = ref('')
const category = ref('默认')
const isSubmitting = ref(false)

async function handleSubmit() {
  if (!title.value.trim() || !content.value.trim()) {
    return
  }

  isSubmitting.value = true
  try {
    emit('submit', title.value.trim(), content.value.trim(), category.value.trim() || '默认')
    title.value = ''
    content.value = ''
    category.value = '默认'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <form @submit.prevent="handleSubmit" class="learning-form">
    <h2 class="form-title">添加学习内容</h2>

    <div class="form-group">
      <label for="title" class="form-label">标题</label>
      <input
        id="title"
        v-model="title"
        type="text"
        class="form-input"
        placeholder="例如：英语单词 Unit 1"
        required
        maxlength="100"
      />
    </div>

    <div class="form-group">
      <label for="category" class="form-label">分类</label>
      <input
        id="category"
        v-model="category"
        type="text"
        class="form-input"
        placeholder="例如：英语、编程、数学"
        maxlength="50"
      />
    </div>

    <div class="form-group">
      <label for="content" class="form-label">学习内容</label>
      <textarea
        id="content"
        v-model="content"
        class="form-textarea"
        placeholder="输入今天学习的内容..."
        rows="4"
        required
        maxlength="1000"
      ></textarea>
    </div>

    <button
      type="submit"
      class="submit-btn"
      :disabled="isSubmitting || !title.trim() || !content.trim()"
    >
      <span v-if="isSubmitting">添加中...</span>
      <span v-else>添加并生成复习计划</span>
    </button>
  </form>
</template>

<style scoped>
.learning-form {
  background: #fff;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.form-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 20px;
}

.form-group {
  margin-bottom: 16px;
}

.form-label {
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
  color: #475569;
  margin-bottom: 6px;
}

.form-input,
.form-textarea {
  width: 100%;
  padding: 12px 14px;
  border: 2px solid #e2e8f0;
  border-radius: 10px;
  font-size: 0.95rem;
  transition: all 0.2s ease;
  box-sizing: border-box;
  font-family: inherit;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.form-input::placeholder,
.form-textarea::placeholder {
  color: #94a3b8;
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
}

.submit-btn {
  width: 100%;
  padding: 14px 24px;
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(79, 70, 229, 0.4);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
