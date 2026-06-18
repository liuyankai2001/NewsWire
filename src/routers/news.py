from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.crud import news
from src.config.db_conf import get_database

router = APIRouter(prefix="/api/news",tags=['news'])

@router.get("/categories")
async def get_categories(skip:int=0,limit:int=100,db:AsyncSession=Depends(get_database)):
    categories = await news.get_categories(db,skip,limit)
    return {
        "msg": "获取分类成功",
        "code":200,
        "data":categories
    }

