from fastapi import APIRouter, HTTPException
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

@router.get("/detail")
async def get_news_detail(news_id:int=Query(..., alias="id"),db:AsyncSession = Depends(get_database)):
    news_detail = await news.get_news_detail(db,news_id)
    if not news_detail:
        raise HTTPException(status_code=404,detail="新闻不存在")
    views_response = await news.increase_news_views(db,news_id)
    if not views_response:
        raise HTTPException(status_code=404, detail="更新浏览量失败")
    relation_news = await news.get_related_news(db,news_id,news_detail.id)
    return {
        "message":"success",
        "code":200,
        "data":{
            "id":news_detail.id,
            "title":news_detail.title,
            "content":news_detail.content,
            "image":news_detail.image,
            "author":news_detail.author,
            "publishTime":news_detail.publish_time,
            "categoryId":news_detail.category_id,
            "views":news_detail.views,
            "relatedNews":relation_news,
        }
    }