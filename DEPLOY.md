# 艾宾浩斯复习助手 - Ubuntu 部署指南

## 环境要求

- Ubuntu 20.04+ (本文档使用 22.04)
- Python 3.10+
- Node.js 18+
- Nginx
- SQLite (内置，无需额外安装)

---

## 方式一：开发环境部署（快速启动）

```bash
# 1. 更新系统
sudo apt update && sudo apt upgrade -y

# 2. 安装依赖
sudo apt install -y python3-pip nodejs npm git

# 3. 克隆项目
cd /opt
sudo git clone <你的项目地址> ebbinghaus
sudo chown -R $USER:$USER ebbinghaus
cd ebbinghaus

# 4. 安装后端依赖
cd backend
pip3 install -r requirements.txt

# 5. 安装前端依赖
cd ../frontend
npm install

# 6. 启动服务
# 终端1：启动后端
cd ../backend
python3 main.py

# 终端2：启动前端
cd ../frontend
npm run dev
```

访问 `http://服务器IP:5173`

---

## 方式二：生产环境部署（systemd + Nginx）

### 1. 安装依赖

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装 Python、Node.js、Nginx
sudo apt install -y python3-pip python3-venv nodejs npm git nginx ufw

# 安装 Gunicorn (生产级 WSGI 服务器)
pip3 install gunicorn
```

### 2. 创建项目目录并配置权限

```bash
# 创建项目目录
sudo mkdir -p /var/www/ebbinghaus
sudo chown -R www-data:www-data /var/www/ebbinghaus

# 复制项目文件到该目录（如果使用 Git）
# sudo git clone <你的项目地址> /var/www/ebbinghaus

# 或者直接复制当前项目
sudo cp -r /path/to/你的项目/* /var/www/ebbinghaus/

# 设置权限
sudo chown -R www-data:www-data /var/www/ebbinghaus
```

### 3. 配置后端

```bash
cd /var/www/ebbinghaus/backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
pip install gunicorn

# 初始化数据库
python3 -c "from database import init_db; init_db()"
```

### 4. 创建 Systemd 服务（后端）

```bash
sudo nano /etc/systemd/system/ebbinghaus-backend.service
```

写入以下内容：

```ini
[Unit]
Description=Ebbinghaus Backend API
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/ebbinghaus/backend
Environment="PATH=/var/www/ebbinghaus/backend/venv/bin"
ExecStart=/var/www/ebbinghaus/backend/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 main:app --timeout 120 --access-logfile /var/log/ebbinghaus/access.log --error-logfile /var/log/ebbinghaus/error.log
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# 创建日志目录
sudo mkdir -p /var/log/ebbinghaus
sudo chown www-data:www-data /var/log/ebbinghaus

# 启动服务
sudo systemctl daemon-reload
sudo systemctl start ebbinghaus-backend
sudo systemctl enable ebbinghaus-backend

# 检查状态
sudo systemctl status ebbinghaus-backend
```

### 5. 构建前端

```bash
cd /var/www/ebbinghaus/frontend

# 安装依赖
npm install

# 构建生产版本
npm run build
```

构建后的文件会在 `dist/` 目录。

### 6. 配置 Nginx

```bash
sudo nano /etc/nginx/sites-available/ebbinghaus
```

写入以下配置：

```nginx
server {
    listen 80;
    server_name your_domain.com;  # 替换为你的域名或IP

    # 前端静态文件
    root /var/www/ebbinghaus/frontend/dist;
    index index.html;

    # 前端路由
    location / {
        try_files $uri $uri/ /index.html;
    }

    # API 代理到后端
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```

```bash
# 启用站点
sudo ln -s /etc/nginx/sites-available/ebbinghaus /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default  # 删除默认站点

# 测试配置
sudo nginx -t

# 重载 Nginx
sudo systemctl reload nginx
```

### 7. 配置防火墙

```bash
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS (后续配置)
sudo ufw enable
```

### 8. 配置 HTTPS (可选但推荐)

使用 Let's Encrypt 免费证书：

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your_domain.com
```

### 9. 验证部署

```bash
# 检查后端状态
sudo systemctl status ebbinghaus-backend

# 检查 Nginx 状态
sudo systemctl status nginx

# 测试 API
curl http://127.0.0.1:8000/api/stats
```

访问 `http://your_domain.com` 或 `http://服务器IP`

---

## 常用命令

```bash
# 重启后端
sudo systemctl restart ebbinghaus-backend

# 查看后端日志
sudo journalctl -u ebbinghaus-backend -f

# 重载 Nginx
sudo systemctl reload nginx

# 重启 Nginx
sudo systemctl restart nginx

# 更新代码后重新部署
cd /var/www/ebbinghaus
sudo git pull
cd backend && source venv/bin/activate && pip install -r requirements.txt
cd ../frontend && npm install && npm run build
sudo systemctl restart ebbinghaus-backend
```

---

## 目录结构（部署后）

```
/var/www/ebbinghaus/
├── backend/
│   ├── venv/              # Python 虚拟环境
│   ├── main.py
│   ├── models.py
│   ├── auth.py
│   ├── database.py
│   ├── requirements.txt
│   └── ebbinghaus.db     # SQLite 数据库
└── frontend/
    ├── dist/              # 构建后的静态文件
    ├── src/
    └── package.json

/var/log/ebbinghaus/
├── access.log
└── error.log
```

---

## 故障排除

### 后端无法启动
```bash
# 检查日志
sudo journalctl -u ebbinghaus-backend -n 50

# 手动测试
cd /var/www/ebbinghaus/backend
source venv/bin/activate
python3 main.py
```

### 数据库错误
```bash
# 重新初始化
cd /var/www/ebbinghaus/backend
rm ebbinghaus.db
python3 -c "from database import init_db; init_db()"
```

### Nginx 502 错误
```bash
# 检查后端是否运行
sudo systemctl status ebbinghaus-backend

# 检查端口
sudo ss -tlnp | grep 8000
```
