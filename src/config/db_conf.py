from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

URL = "mysql+aiomysql://root:root@localhost:3306/news_app?charset=utf8mb4"

async_engine = create_async_engine(
    url=URL,
    echo=True,  # 可选，输出 SQL 日志
    pool_size=20,   # 设置连接池活跃数量
    max_overflow=10 # 设置额外的连接数量
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,  # 绑定异步引擎
    class_=AsyncSession,  # 指定会话类
    expire_on_commit=False
)

async def get_database():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise