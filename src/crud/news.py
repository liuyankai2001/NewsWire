from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.news import CateGory,News

async def get_categories(db:AsyncSession,skip:int=0,limit:int=100):
    stmt = select(CateGory).offset(skip).limit(limit)
    results = await db.execute(stmt)
    categories = results.scalars().all()
    return categories

async def get_news_list(db:AsyncSession,category_id:int,skip:int=0,limit=10):
    stmt = select(News).where(News.category_id==category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_news_count(db:AsyncSession,category_id:int):
    stmt = select(func.count(News.id)).where(News.category_id==category_id)
    result = await db.execute(stmt)
    return result.scalar_one()

async def get_news_detail(db:AsyncSession,news_id):
    stmt = select(News).where(News.id==news_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def increase_news_views(db:AsyncSession,news_id):
    stmt = update(News).where(News.id==news_id).values(views = News.views+1)
    result = await db.execute(stmt)
    return result.rowcount>0