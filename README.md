# AI News 📰

基于 **FastAPI + Vue 3** 的全栈新闻资讯平台，支持新闻浏览、用户系统、收藏、浏览历史、AI 对话等功能，移动端优先设计。

## ✨ 功能特性

| 模块 | 功能 |
|------|------|
| 🏠 **新闻浏览** | 分类筛选、分页加载、无限滚动、下拉刷新 |
| 📝 **新闻详情** | 富文本渲染、浏览量统计、相关推荐 |
| 👤 **用户系统** | 注册/登录、个人信息编辑、密码修改、Token 认证 |
| ⭐ **收藏管理** | 添加/取消收藏、收藏列表、清空收藏 |
| 🕐 **浏览历史** | 自动记录、分页查看、单条删除、一键清空 |
| 🤖 **AI 对话** | 基于通义千问的智能问答，SSE 流式响应 |
| 🌐 **国际化** | 中英文双语切换 |
| 🎨 **主题切换** | 浅色/深色/蓝色/绿色四种主题 |
| ⚡ **Redis 缓存** | 新闻分类、列表接口缓存，提升响应速度 |

## 🛠 技术栈

### 后端

| 技术 | 用途 |
|------|------|
| Python ≥ 3.12 | 运行环境 |
| FastAPI | Web 框架 |
| Uvicorn | ASGI 服务器 |
| SQLAlchemy 2.0 | 异步 ORM |
| aiomysql | MySQL 异步驱动 |
| Redis | 缓存 |
| bcrypt + Passlib | 密码加密 |

### 前端

| 技术 | 用途 |
|------|------|
| Vue 3 | 前端框架 |
| Vite | 构建工具 |
| Vant 4 | 移动端 UI 组件库 |
| Pinia | 状态管理 |
| Vue Router | 路由 |
| Axios | HTTP 客户端 |
| vue-i18n | 国际化 |
| marked + DOMPurify | Markdown 渲染 & XSS 防护 |

## 📁 项目结构

```
ai_news/
├── main.py                      # 后端入口
├── pyproject.toml               # Python 依赖配置
├── sql/
│   └── database.sql             # 数据库建表 & 种子数据
│
├── src/                         # 后端源码
│   ├── config/
│   │   ├── db_conf.py           # MySQL 异步引擎 & 会话工厂
│   │   └── cache_conf.py        # Redis 客户端 & 通用缓存方法
│   ├── models/                  # SQLAlchemy ORM 模型
│   │   ├── news.py              # News & CateGory
│   │   ├── users.py             # User & UserToken
│   │   ├── favorite.py          # Favorite
│   │   └── history.py           # History
│   ├── schemas/                 # Pydantic 请求/响应模型
│   │   ├── base.py              # 新闻字段基类
│   │   ├── users.py             # 用户 Schema
│   │   ├── favorite.py          # 收藏 Schema
│   │   └── history.py           # 历史 Schema
│   ├── routers/                 # API 路由
│   │   ├── news.py              # 新闻接口
│   │   ├── users.py             # 用户接口
│   │   ├── favorite.py          # 收藏接口
│   │   └── history.py           # 浏览历史接口
│   ├── crud/                    # 数据库操作层
│   │   ├── news.py              # 新闻 CRUD
│   │   ├── news_cache.py        # 带缓存的新闻 CRUD
│   │   ├── users.py             # 用户 CRUD
│   │   ├── favorite.py          # 收藏 CRUD
│   │   └── history.py           # 历史 CRUD
│   ├── cache/                   # 缓存键定义
│   │   └── news_cache.py        # 新闻缓存读写
│   └── utils/                   # 工具模块
│       ├── auth.py              # Token 认证中间件
│       ├── security.py          # 密码哈希 & 校验
│       ├── response.py          # 统一响应格式
│       ├── exception.py         # 全局异常处理
│       └── exception_handlers.py
│
└── xwzx-news/                   # 前端源码
    ├── vite.config.js
    └── src/
        ├── main.js              # Vue 入口
        ├── App.vue              # 根组件
        ├── config/api.js        # API 基础配置
        ├── router/index.js      # 路由定义 (11 条)
        ├── store/               # Pinia 状态管理
        ├── i18n/                # 中英文国际化
        ├── components/          # 公共组件
        │   ├── NewsItem.vue     # 新闻卡片
        │   └── TabBar.vue       # 底部导航栏
        └── views/               # 页面视图
            ├── Home.vue         # 首页
            ├── NewsDetail.vue   # 新闻详情
            ├── Category.vue     # 分类概览
            ├── AIChat.vue       # AI 对话
            ├── Login.vue        # 登录
            ├── Register.vue     # 注册
            ├── My.vue           # 个人中心
            ├── Profile.vue      # 个人信息
            ├── Settings.vue     # 设置
            ├── Favorite.vue     # 收藏列表
            └── History.vue      # 历史记录
```

## 🚀 快速开始

### 环境要求

- Python ≥ 3.12
- Node.js ≥ 18
- MySQL ≥ 5.7（或 MariaDB）
- Redis ≥ 6.0

### 1. 克隆项目

```bash
git clone https://github.com/liuyankai2001/NewsWire.git
cd NewsWire
```

### 2. 初始化数据库

**方式一：一键导入 SQL（推荐）**

```bash
mysql -u root -p < sql/database.sql
```

该脚本包含：建库、7 张表结构、8 个默认分类、100+ 条示例新闻。

**方式二：手动创建**

```sql
CREATE DATABASE news_app CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

表结构由 SQLAlchemy 自动生成（需在 `main.py` 中添加 `Base.metadata.create_all`）。

修改 `src/config/db_conf.py` 中的连接信息：

```python
URL = "mysql+aiomysql://用户名:密码@localhost:3306/news_app?charset=utf8mb4"
```

### 3. 启动后端

```bash
# 安装 uv (Python 包管理器)
pip install uv

# 安装依赖
uv sync

# 启动服务
python main.py
```

后端运行在 `http://localhost:8000`，API 文档：

- Swagger UI：`http://localhost:8000/docs`
- ReDoc：`http://localhost:8000/redoc`

### 4. 启动前端

```bash
cd xwzx-news
npm install
npm run dev
```

前端运行在 `http://localhost:5173`。

> ⚠️ **Windows 用户**：Windows 上常见的 Redis (MSOpenTech fork, 基于 3.2) 不支持 RESP3 协议。本项目已配置 `protocol=2` 兼容，无需额外处理。

## 📡 API 接口

### 新闻 `/api/news`

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/news/categories` | 获取新闻分类 |
| GET | `/api/news/list?categoryId=&page=&pageSize=` | 新闻列表（分页） |
| GET | `/api/news/detail?id=` | 新闻详情 & 相关推荐 |

### 用户 `/api/user`

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|:--:|
| POST | `/api/user/register` | 注册 | - |
| POST | `/api/user/login` | 登录 | - |
| GET | `/api/user/info` | 获取个人信息 | ✅ |
| PUT | `/api/user/update` | 更新个人信息 | ✅ |
| PUT | `/api/user/password` | 修改密码 | ✅ |

### 收藏 `/api/favorite`

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|:--:|
| GET | `/api/favorite/check?newsId=` | 检查是否收藏 | ✅ |
| POST | `/api/favorite/add` | 添加收藏 | ✅ |
| DELETE | `/api/favorite/remove?newsId=` | 取消收藏 | ✅ |
| GET | `/api/favorite/list` | 收藏列表（分页） | ✅ |
| DELETE | `/api/favorite/clear` | 清空收藏 | ✅ |

### 浏览历史 `/api/history`

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|:--:|
| POST | `/api/history/add` | 记录浏览 | ✅ |
| GET | `/api/history/list` | 历史列表（分页） | ✅ |
| DELETE | `/api/history/delete/{id}` | 删除单条 | ✅ |
| DELETE | `/api/history/clear` | 清空历史 | ✅ |

## 🔐 认证机制

采用 **Token** 认证，Token 为 UUID v4，登录/注册后返回，有效期 7 天。请求时将 Token 放入 `Authorization` 头：

```bash
curl -H "Authorization: your-token-here" http://localhost:8000/api/user/info
```

## 💾 缓存策略

| 数据类型 | Redis Key | TTL |
|---------|-----------|:--:|
| 新闻分类 | `news:categories` | 2 小时 |
| 新闻列表 | `news_list:{category_id}:{page}:{page_size}` | 30 分钟 |

缓存未命中时自动回源数据库并回写缓存。

## 🎨 前端亮点

- **移动端适配**：Vant 4 组件库，适配手机屏幕
- **多主题**：浅色 / 深色 / 蓝色 / 绿色，偏好持久化
- **中英文**：vue-i18n，文本集中管理
- **离线容错**：收藏和历史同步到 localStorage，网络异常时使用本地数据
- **下拉刷新 & 无限滚动**：首页新闻列表流畅体验

## ⚙️ 配置项

| 文件 | 内容 |
|------|------|
| `src/config/db_conf.py` | MySQL 连接串、连接池 |
| `src/config/cache_conf.py` | Redis 地址、协议 |
| `xwzx-news/src/config/api.js` | 后端 API 地址、AI 配置 |

## 📄 License

MIT

---

**作者**：[@liuyankai2001](https://github.com/liuyankai2001)