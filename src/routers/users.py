from fastapi import APIRouter, HTTPException
from fastapi.params import Depends,Query
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.db_conf import get_database
from src.schemas.users import UserRequest, UserAuthResponse, UserInfoResponse
from src.crud import users
from src.utils.response import success_response

router = APIRouter(prefix="/api/user",tags=['users'])




@router.post("/register")
async def register(user_data:UserRequest,db:AsyncSession=Depends(get_database),):
    # 验证用户是否存在 -> 创建用户 -> 生成Token -> 相应结果
    existing_user = await users.get_user_by_username(db=db,username=user_data.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="用户已经存在")
    user = await users.create_user(db,user_data)
    token = await users.create_token(db,user.id)

    # return {
    #     "code":200,
    #     "message":"注册成功",
    #     "data":{
    #         "token":token,
    #         "userInfo":{
    #             "id":user.id,
    #             "username":user_data.username,
    #             "bio":user.bio,
    #             "avatar":user.avatar
    #         }
    #
    #     }
    # }
    response_data = UserAuthResponse(token=token,userInfo=UserInfoResponse.model_validate(user))
    return success_response(messagse="注册成功",data=response_data)