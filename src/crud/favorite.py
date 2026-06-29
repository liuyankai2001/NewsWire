from sqlalchemy import select, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.favorite import Favorite
from src.models.news import News


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

# 获取某个用户的收藏列表
async def get_favorite_list(
    db:AsyncSession,
    user_id:int,
    page:int=1,
    page_size:int=10
):
    # 总量+收藏的新闻列表
    query = select(func.count()).where(Favorite.user_id==user_id)
    count_result = await db.execute(query)
    total = count_result.scalar_one()

    # 获取收藏列表 - 联表join() + 收藏时间排序呢 + 分页
    query = (select(News,Favorite.created_at.label("favorite_time"),Favorite.id.label("favorite_id"))
     .join(Favorite,Favorite.news_id==News.id)
     .where(Favorite.user_id==user_id)
     .order_by(Favorite.created_at.desc())
     .offset((page-1)*page_size)
     .limit(page_size))
    result = await db.execute(query)
    rows = result.all()
    return rows,total