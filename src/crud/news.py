from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.news import CateGory

async def get_categories(db:AsyncSession,skip:int=0,limit:int=100):
    stmt = select(CateGory).offset(skip).limit(limit)
    results = await db.execute(stmt)
    categories = results.scalars().all()
    return categories