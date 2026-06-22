import uuid
from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.users import User, UserToken
from src.schemas.users import UserRequest
from src.utils import security

async def get_user_by_username(db:AsyncSession,username:str):
    query = select(User).where(User.username==username)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def create_user(db:AsyncSession,user_data:UserRequest):
    # 密码加密
    hashed_password = security.get_hash_password(user_data.password)
    user = User(username=user_data.username,password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

# 生成token
async def create_token(db:AsyncSession,user_id:int):
    # 生成token + 设置过期时间 -> 查询数据库当前用户是否有token -> 有：更新，无：添加
    token = str(uuid.uuid4())
    expires_at = datetime.now() + timedelta(days=7)
    query = select(UserToken).where(UserToken.id==user_id)
    result = await db.execute(query)
    user_token = result.scalar_one_or_none()

    if user_token:
        user_token.token = token
        user_token.expires_at = expires_at
    else:
        user_token = UserToken(user_id=user_id,token=token,expires_at=expires_at)
        db.add(user_token)
        await db.commit()
    return token

async def authenticate_user(db:AsyncSession,username:str,password:str):
    user = await get_user_by_username(db,username)
    if not user:
        return None
    if not security.verify_password(password,user.password):
        return None
    return user