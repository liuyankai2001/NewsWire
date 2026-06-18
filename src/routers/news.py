from fastapi import APIRouter
from fastapi.params import Depends,Query
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

@router.get("/list")
async def get_news(
        category_id:int = Query(...,alias="categoryId"),
        page:int = 1,
        page_size:int = Query(10,alias="pageSize",le=100),
        db:AsyncSession = Depends(get_database)
):
    offset = (page-1)*page_size
    news_list = await news.get_news_list(db,category_id,offset,page_size)
    total = await news.get_news_count(db,category_id)
    has_more = (offset+len(news_list)) < total
    return {
        "code":200,
        "message":"获取新闻列表成功",
        "data":{
            "list":news_list,
            "total":total,
            "hasMore":has_more
        }
    }

