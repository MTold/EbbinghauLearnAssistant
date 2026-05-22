<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { apiClient, type OverviewStats, type TrendsResponse } from '../api'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart, PieChart, BarChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
} from 'echarts/components'

use([
  CanvasRenderer,
  LineChart,
  PieChart,
  BarChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
])

const overview = ref<OverviewStats | null>(null)
const trends = ref<TrendsResponse | null>(null)
const loading = ref(true)
const selectedDays = ref(30)

onMounted(async () => {
  await fetchData()
})

async function fetchData() {
  loading.value = true
  try {
    const [overviewData, trendsData] = await Promise.all([
      apiClient.stats.getOverview(),
      apiClient.stats.getTrends(selectedDays.value)
    ])
    overview.value = overviewData
    trends.value = trendsData
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

async function changeDays(days: number) {
  selectedDays.value = days
  await fetchData()
}

const pieOption = computed(() => {
  if (!overview.value) return {}
  const data = overview.value.category_distribution
  const pieData = Object.entries(data).map(([name, value]) => ({ name, value }))
  
  return {
    title: {
      text: '知识分类分布',
      left: 'center',
      textStyle: { fontSize: 16, fontWeight: 600, color: '#1e293b' }
    },
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      right: 20,
      top: 'center'
    },
    series: [
      {
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 18,
            fontWeight: 'bold'
          }
        },
        labelLine: { show: false },
        data: pieData.length > 0 ? pieData : [{ name: '暂无数据', value: 0 }]
      }
    ],
    color: ['#4f46e5', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4', '#ec4899']
  }
})

const lineOption = computed(() => {
  if (!trends.value) return {}
  const dates = trends.value.learning_trend.map(d => d.date.slice(5))
  const learningData = trends.value.learning_trend.map(d => d.count)
  const reviewData = trends.value.review_trend.map(d => d.count)

  return {
    title: {
      text: '学习与复习趋势',
      left: 'center',
      textStyle: { fontSize: 16, fontWeight: 600, color: '#1e293b' }
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'cross' }
    },
    legend: {
      data: ['新增学习', '复习完成'],
      bottom: 0
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',
      top: '15%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: dates,
      axisLabel: { fontSize: 11 }
    },
    yAxis: {
      type: 'value',
      minInterval: 1
    },
    series: [
      {
        name: '新增学习',
        type: 'line',
        smooth: true,
        data: learningData,
        areaStyle: {
          color: {
            type: 'linear',
            x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(79, 70, 229, 0.3)' },
              { offset: 1, color: 'rgba(79, 70, 229, 0.05)' }
            ]
          }
        },
        lineStyle: { color: '#4f46e5', width: 2 },
        itemStyle: { color: '#4f46e5' }
      },
      {
        name: '复习完成',
        type: 'line',
        smooth: true,
        data: reviewData,
        areaStyle: {
          color: {
            type: 'linear',
            x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(16, 185, 129, 0.3)' },
              { offset: 1, color: 'rgba(16, 185, 129, 0.05)' }
            ]
          }
        },
        lineStyle: { color: '#10b981', width: 2 },
        itemStyle: { color: '#10b981' }
      }
    ]
  }
})

const statusOption = computed(() => {
  if (!overview.value) return {}
  return {
    title: {
      text: '复习进度分布',
      left: 'center',
      textStyle: { fontSize: 16, fontWeight: 600, color: '#1e293b' }
    },
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      right: 20,
      top: 'center'
    },
    series: [
      {
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        data: [
          { name: '待复习', value: overview.value.pending, itemStyle: { color: '#64748b' } },
          { name: '今日待复习', value: overview.value.due_today, itemStyle: { color: '#f59e0b' } },
          { name: '已完成', value: overview.value.completed, itemStyle: { color: '#10b981' } }
        ]
      }
    ]
  }
})

const reviewRateOption = computed(() => {
  if (!overview.value) return {}
  const onTime = overview.value.on_time_reviews
  const late = overview.value.late_reviews
  const total = onTime + late

  return {
    title: {
      text: '复习准时率',
      left: 'center',
      textStyle: { fontSize: 16, fontWeight: 600, color: '#1e293b' }
    },
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      right: 20,
      top: 'center'
    },
    series: [
      {
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        data: total > 0
          ? [
              { name: '准时复习', value: onTime, itemStyle: { color: '#10b981' } },
              { name: '延迟复习', value: late, itemStyle: { color: '#f59e0b' } }
            ]
          : [{ name: '暂无数据', value: 1, itemStyle: { color: '#e2e8f0' } }]
      }
    ]
  }
})
</script>

<template>
  <div class="analytics-page">
    <header class="page-header">
      <h1 class="page-title">数据分析</h1>
      <p class="page-subtitle">查看你的学习统计和分析报告</p>
    </header>

    <div class="days-selector">
      <span class="selector-label">时间范围：</span>
      <button
        v-for="days in [7, 14, 30, 60]"
        :key="days"
        :class="['days-btn', { active: selectedDays === days }]"
        @click="changeDays(days)"
      >
        {{ days }}天
      </button>
    </div>

    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>加载中...</p>
    </div>

    <template v-else>
      <div class="stats-overview">
        <div class="stat-card">
          <div class="stat-icon">📚</div>
          <div class="stat-content">
            <span class="stat-value">{{ overview?.total_items || 0 }}</span>
            <span class="stat-label">总知识</span>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">✅</div>
          <div class="stat-content">
            <span class="stat-value">{{ overview?.total_reviews || 0 }}</span>
            <span class="stat-label">总复习</span>
          </div>
        </div>
        <div class="stat-card stat-highlight">
          <div class="stat-icon">🎯</div>
          <div class="stat-content">
            <span class="stat-value">{{ trends?.on_time_rate.toFixed(1) || 100 }}%</span>
            <span class="stat-label">准时率</span>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">📊</div>
          <div class="stat-content">
            <span class="stat-value">{{ Object.keys(overview?.category_distribution || {}).length }}</span>
            <span class="stat-label">分类数</span>
          </div>
        </div>
      </div>

      <div class="charts-grid">
        <div class="chart-card chart-wide">
          <VChart :option="lineOption" style="height: 350px;" autoresize />
        </div>

        <div class="chart-card">
          <VChart :option="pieOption" style="height: 300px;" autoresize />
        </div>

        <div class="chart-card">
          <VChart :option="statusOption" style="height: 300px;" autoresize />
        </div>

        <div class="chart-card">
          <VChart :option="reviewRateOption" style="height: 300px;" autoresize />
        </div>
      </div>

      <div class="detail-stats">
        <h3 class="detail-title">详细统计</h3>
        <div class="detail-grid">
          <div class="detail-item">
            <span class="detail-label">按时复习次数</span>
            <span class="detail-value success">{{ overview?.on_time_reviews || 0 }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">延迟复习次数</span>
            <span class="detail-value warning">{{ overview?.late_reviews || 0 }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">待复习</span>
            <span class="detail-value">{{ overview?.pending || 0 }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">今日待复习</span>
            <span class="detail-value warning">{{ overview?.due_today || 0 }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">已完成</span>
            <span class="detail-value success">{{ overview?.completed || 0 }}</span>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<style scoped>
.analytics-page {
  padding: 32px;
  max-width: 1400px;
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

.days-selector {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 24px;
}

.selector-label {
  color: #64748b;
  font-weight: 500;
}

.days-btn {
  padding: 8px 16px;
  background: #fff;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.days-btn:hover {
  border-color: #4f46e5;
}

.days-btn.active {
  background: #4f46e5;
  border-color: #4f46e5;
  color: white;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 80px;
  color: #64748b;
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #e2e8f0;
  border-top-color: #4f46e5;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.stats-overview {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 32px;
}

.stat-card {
  background: #fff;
  border-radius: 16px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  border: 1px solid #e2e8f0;
  transition: all 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
}

.stat-card.stat-highlight {
  background: linear-gradient(135deg, #ecfdf5, #fff);
  border-color: #10b981;
}

.stat-icon {
  font-size: 2rem;
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f1f5f9;
  border-radius: 12px;
}

.stat-highlight .stat-icon {
  background: #d1fae5;
}

.stat-value {
  display: block;
  font-size: 1.75rem;
  font-weight: 700;
  color: #1e293b;
}

.stat-label {
  font-size: 0.9rem;
  color: #64748b;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
  margin-bottom: 32px;
}

.chart-card {
  background: #fff;
  border-radius: 16px;
  padding: 24px;
  border: 1px solid #e2e8f0;
}

.chart-wide {
  grid-column: span 2;
}

.detail-stats {
  background: #fff;
  border-radius: 16px;
  padding: 24px;
  border: 1px solid #e2e8f0;
}

.detail-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 20px;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 16px;
}

.detail-item {
  text-align: center;
  padding: 16px;
  background: #f8fafc;
  border-radius: 12px;
}

.detail-label {
  display: block;
  font-size: 0.85rem;
  color: #64748b;
  margin-bottom: 8px;
}

.detail-value {
  display: block;
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
}

.detail-value.success {
  color: #10b981;
}

.detail-value.warning {
  color: #f59e0b;
}

@media (max-width: 1024px) {
  .stats-overview {
    grid-template-columns: repeat(2, 1fr);
  }

  .charts-grid {
    grid-template-columns: 1fr;
  }

  .chart-wide {
    grid-column: span 1;
  }

  .detail-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .analytics-page {
    padding: 20px;
  }

  .stats-overview {
    grid-template-columns: 1fr;
  }

  .detail-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
