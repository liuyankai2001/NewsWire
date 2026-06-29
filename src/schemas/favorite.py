from datetime import datetime

from pydantic import BaseModel,Field,ConfigDict

from src.schemas.base import NewsItemBase


class FavoriteCheckResponse(BaseModel):
    is_favorite:bool = Field(...,alias="isFavorite")

class FavoriteAddRequest(BaseModel):
    news_id:int = Field(...,alias="newsId")


class FavoriteNewsItemResponse(NewsItemBase):
    favorite_id:int = Field(alias="favoriteId")
    favorite_time:datetime = Field(alias="favoriteTime")
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )

# 收藏接口响应模型类
class FavoriteResponse(BaseModel):
    list:list[FavoriteNewsItemResponse]
    total:int
    has_more:bool
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )