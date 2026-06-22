

from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from src.routers import news
from src.routers import users
from src.utils.exception_handlers import register_exception_handlers

app = FastAPI()

# 注册异常处理器
register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],    # 允许的源，开发阶段允许所有源，生产环境需要指定源
    allow_credentials=True,   # 允许携带cookie
    allow_methods=['*'],      # 允许的请求方法
    allow_headers=["*"]       # 允许的请求头
)

app.include_router(news.router)

app.include_router(users.router)


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="localhost", port=8000, reload=True)
