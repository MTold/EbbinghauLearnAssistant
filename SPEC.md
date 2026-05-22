# 艾宾浩斯复习助手 - 项目规范

## 1. 项目概述

- **项目名称**: Ebbinghaus Review (艾宾浩斯复习助手)
- **项目类型**: 前后端分离的Web应用
- **核心功能**: 基于艾宾浩斯遗忘曲线，管理系统学习内容并自动生成复习计划
- **目标用户**: 需要高效记忆和复习各类知识点的学习者

## 2. 技术栈

### 前端
- **构建工具**: Vite 5.x
- **框架**: Vue 3 + TypeScript
- **路由**: Vue Router 4.x
- **状态管理**: Pinia
- **HTTP客户端**: Axios
- **图表**: ECharts 5.x
- **样式**: 原生CSS (含CSS变量)

### 后端
- **框架**: FastAPI (Python 3.10+)
- **数据库**: SQLite (通过SQLModel/ORM)
- **认证**: JWT (PyJWT)
- **密码加密**: PassLib + Bcrypt
- **API风格**: RESTful JSON API

## 3. 功能列表

### 3.1 用户认证
- **用户注册**: 输入用户名、邮箱、密码
- **用户登录**: 用户名/邮箱 + 密码登录
- **JWT认证**: 访问受保护API时携带Token
- **用户登出**: 清除本地Token

### 3.2 学习内容管理
- **添加学习内容**: 输入标题和学习内容描述
- **查看学习列表**: 显示所有学习内容及其复习状态
- **编辑学习内容**: 修改标题和内容
- **删除学习内容**: 移除不再需要复习的内容
- **知识分类**: 支持为学习内容添加分类标签

### 3.3 复习计划生成
- **艾宾浩斯间隔**: 学习后按以下间隔生成复习节点
  - 第1次复习: 1天后
  - 第2次复习: 3天后
  - 第3次复习: 7天后
  - 第4次复习: 14天后
  - 第5次复习: 30天后
  - 第6次复习: 60天后
  - 第7次复习: 90天后

### 3.4 复习功能
- **今日复习按钮**: 点击标记当日复习完成
- **过期复习处理**: 如果某天漏复习，后续复习时间从实际复习日期重新计算
- **复习历史记录**: 查看每次复习的时间和状态

### 3.5 状态展示
- **今日待复习**: 显示今天需要复习的内容数量
- **进度指示**: 显示每个学习项的复习进度（第几次/共几次）

### 3.6 数据分析
- **复习完成率**: 按时复习 vs 延迟复习的占比
- **学习趋势图**: 每日/每周新增学习数量
- **复习趋势图**: 每日/每周复习完成数量
- **分类统计**: 各分类学习内容数量分布
- **进度分布**: 各复习阶段的学习项数量

## 4. 数据模型

### 用户 (User)
```python
{
    "id": int,                    # 唯一标识
    "username": str,              # 用户名（唯一）
    "email": str,                 # 邮箱（唯一）
    "password_hash": str,         # 密码哈希
    "created_at": datetime,       # 注册时间
}
```

### 学习内容 (LearningItem)
```python
{
    "id": int,                    # 唯一标识
    "user_id": int,              # 所属用户ID
    "title": str,                 # 标题
    "content": str,               # 学习内容描述
    "category": str,              # 分类标签
    "created_at": datetime,       # 创建时间
    "review_count": int,          # 已完成复习次数
    "last_reviewed_at": datetime, # 最后一次复习时间
    "next_review_at": datetime,   # 下次复习时间
    "status": str                 # "pending" | "due_today" | "completed"
}
```

### 复习记录 (ReviewLog)
```python
{
    "id": int,
    "item_id": int,              # 关联的学习内容ID
    "reviewed_at": datetime,     # 复习时间
    "was_on_time": bool          # 是否按时复习
}
```

## 5. API 设计

### 认证
- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录
- `GET /api/auth/me` - 获取当前用户信息

### 学习内容
- `GET /api/items` - 获取当前用户的所有学习内容
- `POST /api/items` - 添加新的学习内容
- `PUT /api/items/{id}` - 更新学习内容
- `DELETE /api/items/{id}` - 删除学习内容
- `POST /api/items/{id}/review` - 标记为已复习

### 复习记录
- `GET /api/items/{id}/logs` - 获取某内容的复习历史

### 统计与分析
- `GET /api/stats` - 获取基础统计信息
- `GET /api/stats/overview` - 获取数据概览（图表用）
- `GET /api/stats/trends` - 获取趋势数据

## 6. 前端页面结构

### 页面列表
1. **登录页** (`/login`) - 用户登录
2. **注册页** (`/register`) - 用户注册
3. **首页/仪表盘** (`/`) - 今日待复习 + 快速统计
4. **知识管理** (`/knowledge`) - 所有知识列表 + 管理功能
5. **数据分析** (`/analytics`) - 图表分析页面

### 组件
- `LoginForm.vue` - 登录表单
- `RegisterForm.vue` - 注册表单
- `LearningForm.vue` - 添加学习内容表单
- `LearningList.vue` - 学习内容列表
- `LearningItem.vue` - 单个学习项卡片
- `StatsBar.vue` - 统计栏
- `ChartCard.vue` - 图表卡片组件
- `Sidebar.vue` - 侧边导航栏
- `Header.vue` - 顶部导航栏

## 7. 视觉设计

### 主题配色
- **主色**: `#4F46E5` (靛蓝色 - 专业、专注)
- **次要色**: `#10B981` (翠绿色 - 表示完成/成功)
- **警告色**: `#F59E0B` (琥珀色 - 表示待复习)
- **危险色**: `#DC2626` (红色 - 删除/错误)
- **背景色**: `#F8FAFC` (浅灰白)
- **卡片背景**: `#FFFFFF`
- **文字主色**: `#1E293B`
- **文字次色**: `#64748B`
- **侧边栏**: `#1E1B4B` (深靛蓝)

### 字体
- 主字体: "Inter", "PingFang SC", system-ui, sans-serif
- 标题字重: 600-700
- 正文字重: 400

### 间距
- 基础单位: 8px
- 卡片间距: 16px
- 页面边距: 24px

### 交互效果
- 按钮悬停: 轻微上浮 + 阴影加深
- 卡片悬停: 边框高亮
- 复习完成: 绿色渐变动画
- 页面切换: 平滑过渡动画

## 8. 项目结构

```
/Users/yeonh/同济/艾宾浩斯/
├── SPEC.md
├── start.sh
├── backend/
│   ├── main.py              # FastAPI主应用
│   ├── models.py            # 数据模型
│   ├── database.py          # 数据库配置
│   ├── auth.py              # 认证逻辑
│   └── requirements.txt
└── frontend/
    ├── index.html
    ├── package.json
    ├── vite.config.ts
    ├── tsconfig.json
    └── src/
        ├── main.ts
        ├── App.vue
        ├── router/
        │   └── index.ts     # 路由配置
        ├── stores/
        │   ├── learning.ts
        │   └── auth.ts      # 认证状态
        ├── api/
        │   ├── index.ts      # API基类
        │   ├── auth.ts       # 认证API
        │   └── learning.ts   # 学习API
        ├── views/
        │   ├── Login.vue
        │   ├── Register.vue
        │   ├── Home.vue
        │   ├── Knowledge.vue
        │   └── Analytics.vue
        ├── components/
        │   ├── LearningForm.vue
        │   ├── LearningList.vue
        │   ├── LearningItem.vue
        │   ├── StatsBar.vue
        │   ├── Sidebar.vue
        │   ├── Header.vue
        │   └── ChartCard.vue
        └── style.css
```

## 9. 验收标准

1. ✅ 用户可以注册和登录
2. ✅ 可以添加新的学习内容
3. ✅ 自动生成基于艾宾浩斯曲线的复习计划
4. ✅ 显示今日待复习内容
5. ✅ 点击复习按钮后自动计算下次复习时间
6. ✅ 漏复习后，下次复习时间从实际复习日期重新计算
7. ✅ 知识管理页面可查看、编辑、删除所有知识
8. ✅ 数据分析页面展示复习统计图表
9. ✅ 前后端正常通信，数据持久化到数据库
10. ✅ JWT认证保护用户数据安全
