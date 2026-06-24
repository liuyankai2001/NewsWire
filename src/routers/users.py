from fastapi import APIRouter, HTTPException
from fastapi.params import Depends,Query
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.db_conf import get_database
from src.models.users import User
from src.schemas.users import UserRequest, UserAuthResponse, UserInfoResponse, UserUpdateRequestion, \
    UserChangePasswordRequest
from src.crud import users
from src.utils.auth import get_current_user
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

@router.post("/login")
async def login(user_data:UserRequest,db:AsyncSession=Depends(get_database)):
    # 登录逻辑：验证用户是否存在 -> 验证密码 -> 生成token -> 相应结果
    user = await users.authenticate_user(db,user_data.username,user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="用户名或密码错误")
    token = await  users.create_token(db,user.id)
    response_data = UserAuthResponse(token=token, user_info=UserInfoResponse.model_validate(user))
    return success_response("登录成功",data=response_data)

# 查Token用户 -> 封装crud -》 功能整合成一个工具函数
@router.get("/info")
async def get_user_info(user:User=Depends(get_current_user)):
    return success_response(messagse="获取用户信息成功",data=UserInfoResponse.model_validate(user))

@router.put("/update")
async def update_user_info(user_data:UserUpdateRequestion,user:User=Depends(get_current_user),db:AsyncSession=Depends(get_database)):
    user = await users.update_user(db,user.username,user_data)
    return success_response("更新信息成功",data=UserInfoResponse.model_validate(user))

@router.put("/password")
async def update_password(password_data:UserChangePasswordRequest,user:User=Depends(get_current_user),db:AsyncSession=Depends(get_database)):
    res_change_pwd = await users.change_password(db,user,password_data.old_password,password_data.new_password)
    if not res_change_pwd:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="修改密码失败，请稍后再试")
    return success_response("修改密码成功")