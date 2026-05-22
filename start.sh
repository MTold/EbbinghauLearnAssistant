#!/bin/bash

# 艾宾浩斯复习助手启动脚本

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/backend"
FRONTEND_DIR="$SCRIPT_DIR/frontend"

echo "🚀 启动艾宾浩斯复习助手..."

# 检查后端依赖
if [ ! -d "$BACKEND_DIR/venv" ] && [ ! -f "$BACKEND_DIR/requirements.txt" ]; then
    echo "❌ 后端依赖文件不存在"
    exit 1
fi

# 检查前端依赖
if [ ! -d "$FRONTEND_DIR/node_modules" ]; then
    echo "📦 安装前端依赖..."
    cd "$FRONTEND_DIR" && npm install
fi

# 启动后端
echo "🔧 启动后端服务 (FastAPI)..."
cd "$BACKEND_DIR"
python main.py &
BACKEND_PID=$!

sleep 2

# 检查后端是否启动成功
if ! curl -s http://localhost:8000/api/stats > /dev/null 2>&1; then
    echo "❌ 后端服务启动失败"
    exit 1
fi

# 启动前端
echo "🎨 启动前端服务 (Vite)..."
cd "$FRONTEND_DIR"
npm run dev -- --host &
FRONTEND_PID=$!

sleep 3

# 检查前端是否启动成功
if curl -s http://localhost:5173 > /dev/null 2>&1; then
    echo ""
    echo "✅ 服务启动成功！"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🌐 前端地址: http://localhost:5173"
    echo "🔧 后端地址: http://localhost:8000"
    echo "📚 API 文档: http://localhost:8000/docs"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "按 Ctrl+C 停止服务"
    echo ""

    # 等待用户中断
    trap "echo '🛑 停止服务...' && kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" SIGINT SIGTERM
    wait
else
    echo "❌ 前端服务启动失败"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi
