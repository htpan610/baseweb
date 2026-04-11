# base-web

## 快速启动
超级用户账号：admin
超级用户密码：epyy96325

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