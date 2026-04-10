# base-web

## 快速启动

```bash
# 1. 后端
cd backend
uv sync          # 安装依赖
uv run python manage.py migrate
uv run python manage.py runserver

# 2. 前端（新终端）
cd frontend
npm install
npm run dev