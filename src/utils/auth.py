# 根据token查询用户，最终返回用户
# from http.client import HTTPException

from fastapi import Header
from fastapi import Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.config.db_conf import get_database
from src.crud import users

async def get_current_user(authorization:str=Header(...,alias="Authorization"),db:AsyncSession = Depends(get_database)):
    # Bearer xxxxxxxxx
    token = authorization.split(" ")[1]
    user = await users.get_user_by_token(db,token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="无效的令牌")
    return user