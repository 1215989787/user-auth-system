from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import (
    UserUpdate, PasswordChange, MessageResponse
)
from app.services.user_service import UserService
from app.api.deps import get_current_active_user
from app.models.user import UserModel

router = APIRouter(prefix="/users", tags=["用户管理"])

@router.get("/profile", response_model=dict)
async def get_user_profile(current_user: UserModel = Depends(get_current_active_user)):
    """获取用户资料"""
    return {
        "id": str(current_user.id),
        "username": current_user.username,
        "email": current_user.email,
        "phone": current_user.phone,
        "nickname": current_user.nickname,
        "avatar": current_user.avatar,
        "gender": current_user.gender,
        "birthday": current_user.birthday,
        "bio": current_user.bio,
        "is_active": current_user.is_active,
        "is_verified": current_user.is_verified,
        "email_verified": current_user.email_verified,
        "phone_verified": current_user.phone_verified,
        "is_vip": current_user.is_vip,
        "vip_level": current_user.vip_level,
        "vip_expire_time": current_user.vip_expire_time,
        "vip_balance": current_user.vip_balance,
        "created_at": current_user.created_at,
        "last_login": current_user.last_login
    }

@router.put("/profile", response_model=dict)
async def update_user_profile(
    user_data: UserUpdate,
    current_user: UserModel = Depends(get_current_active_user)
):
    """更新用户资料"""
    user, message = await UserService.update_user_profile(str(current_user.id), user_data)
    if not user:
        raise HTTPException(status_code=400, detail=message)
    return user

@router.post("/change-password", response_model=MessageResponse)
async def change_password(
    password_data: PasswordChange,
    current_user: UserModel = Depends(get_current_active_user)
):
    """修改密码"""
    success, message = await UserService.change_password(str(current_user.id), password_data)
    if not success:
        raise HTTPException(status_code=400, detail=message)
    return MessageResponse(message=message)

@router.get("/vip/info", response_model=dict)
async def get_vip_info(current_user: UserModel = Depends(get_current_active_user)):
    """获取VIP信息"""
    return await UserService.get_vip_info(str(current_user.id)) 