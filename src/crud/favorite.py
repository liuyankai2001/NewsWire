from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.favorite import Favorite


# 检查收藏状态：当前用户 是否 收藏了这一条新闻
async def is_new_favorite(
        db:AsyncSession,
        user_id:int,
        news_id:int
)->bool:
    query = select(Favorite).where(Favorite.user_id==user_id,Favorite.news_id==news_id)
    result = await db.execute(query)
    return result.scalar_one_or_none() is not None

async def add_news_favorite(
        db:AsyncSession,
        user_id:int,
        news_id:int
):
    favorite = Favorite(user_id=user_id,news_id=news_id)
    db.add(favorite)
    await db.commit()
    await db.refresh(favorite)
    return favorite

async def remove_news_favorite(db:AsyncSession,user_id:int,news_id):
    query = delete(Favorite).where(Favorite.user_id==user_id,Favorite.news_id==news_id)
    result = await db.execute(query)
    await db.commit()
    return result.rowcount > 0