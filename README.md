# 艾宾浩斯复习助手

基于艾宾浩斯遗忘曲线，帮助你科学规划复习时间的 Web 应用。

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Vue](https://img.shields.io/badge/Vue-3.x-green.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-teal.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 功能特性

- ✅ **用户认证** - 注册、登录、JWT 认证
- ✅ **知识管理** - 添加、编辑、删除学习内容，支持分类
- ✅ **艾宾浩斯复习计划** - 自动生成科学的复习间隔
  - 第1次复习: 1天后
  - 第2次复习: 3天后
  - 第3次复习: 7天后
  - 第4次复习: 14天后
  - 第5次复习: 30天后
  - 第6次复习: 60天后
  - 第7次复习: 90天后
- ✅ **逾期处理** - 漏复习后自动重新计算下次复习时间
- ✅ **数据分析** - 复习统计图表、学习趋势分析
- ✅ **响应式设计** - 支持桌面端和移动端

## 技术栈

### 前端
- Vue 3 + TypeScript
- Vite 5.x
- Vue Router 4.x
- Pinia (状态管理)
- ECharts 5.x (图表)
- Axios

### 后端
- FastAPI
- SQLModel (ORM)
- SQLite
- PyJWT (认证)
- PassLib (密码加密)

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/MTold/EbbinghauLearnAssistant.git
cd EbbinghauLearnAssistant
```

### 2. 启动后端

```bash
cd backend
pip install -r requirements.txt
python main.py
```

后端服务将在 `http://localhost:8000` 启动。

### 3. 启动前端

```bash
cd frontend
npm install
npm run dev
```

前端服务将在 `http://localhost:5173` 启动。

### 4. 访问应用

打开浏览器访问 `http://localhost:5173`，注册账号后即可使用。

## 或使用启动脚本

```bash
chmod +x start.sh
./start.sh
```

## 生产环境部署

详见 [DEPLOY.md](./DEPLOY.md)

## 项目结构

```
ebbinghaus/
├── backend/              # 后端
│   ├── main.py           # API 入口
│   ├── models.py         # 数据模型
│   ├── auth.py          # 认证逻辑
│   ├── database.py      # 数据库配置
│   └── requirements.txt # Python 依赖
├── frontend/              # 前端
│   ├── src/
│   │   ├── views/        # 页面组件
│   │   ├── components/   # 通用组件
│   │   ├── stores/       # Pinia 状态
│   │   ├── api/          # API 客户端
│   │   └── router/       # 路由配置
│   └── package.json
├── SPEC.md              # 项目规范
├── DEPLOY.md            # 部署指南
└── start.sh             # 启动脚本
```

## API 文档

启动后端后访问 `http://localhost:8000/docs` 查看完整的 API 文档。

## 许可证

MIT License
