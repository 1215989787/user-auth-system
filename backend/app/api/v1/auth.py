from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.schemas.user import (
    UserRegister, UserLogin, WechatLogin, LoginResponse, 
    VerificationCodeRequest, VerificationCodeResponse, MessageResponse
)
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.api.deps import get_current_active_user
from app.models.user import UserModel

router = APIRouter(prefix="/auth", tags=["认证"])

@router.post("/register", response_model=LoginResponse)
async def register(user_data: UserRegister):
    """用户注册"""
    user, message = await AuthService.register_user(user_data)
    if not user:
        if message == "该用户已注册":
            raise HTTPException(status_code=409, detail={"code": "USER_EXISTS", "msg": message})
        else:
            raise HTTPException(status_code=400, detail={"code": "REGISTER_FAILED", "msg": message})
    
    # 创建令牌
    access_token, refresh_token = AuthService.create_tokens(user)
    
    # 保存会话
    await AuthService.save_user_session(str(user.id), refresh_token)
    
    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=user
    )

@router.post("/login", response_model=LoginResponse)
async def login(login_data: UserLogin):
    """用户登录"""
    user, message = await AuthService.login_user(login_data)
    if not user:
        raise HTTPException(status_code=400, detail=message)
    
    # 创建令牌
    access_token, refresh_token = AuthService.create_tokens(user)
    
    # 保存会话
    await AuthService.save_user_session(str(user.id), refresh_token)
    
    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=user
    )

@router.post("/wechat/login", response_model=LoginResponse)
async def wechat_login(wechat_data: WechatLogin):
    """微信登录"""
    user, message = await AuthService.wechat_login(wechat_data)
    if not user:
        raise HTTPException(status_code=400, detail=message)
    
    # 创建令牌
    access_token, refresh_token = AuthService.create_tokens(user)
    
    # 保存会话
    await AuthService.save_user_session(str(user.id), refresh_token)
    
    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=user
    )

@router.post("/verification-code", response_model=VerificationCodeResponse)
async def send_verification_code(code_request: VerificationCodeRequest):
    """发送验证码"""
    if code_request.phone:
        # 发送短信验证码
        code, expires_in = await AuthService.create_verification_code(
            phone=code_request.phone, code_type=code_request.type
        )
        # 这里应该调用短信服务发送验证码
        # 目前只是返回验证码用于测试
        return VerificationCodeResponse(
            message=f"验证码已发送到 {code_request.phone}，验证码: {code}",
            expires_in=expires_in
        )
    
    elif code_request.email:
        # 发送邮件验证码
        code, expires_in = await AuthService.create_verification_code(
            email=code_request.email, code_type=code_request.type
        )
        # 这里应该调用邮件服务发送验证码
        # 目前只是返回验证码用于测试
        return VerificationCodeResponse(
            message=f"验证码已发送到 {code_request.email}，验证码: {code}",
            expires_in=expires_in
        )
    
    else:
        raise HTTPException(status_code=400, detail="请提供手机号或邮箱")

@router.post("/refresh", response_model=dict)
async def refresh_token(refresh_token: str):
    """刷新访问令牌"""
    access_token = await AuthService.refresh_access_token(refresh_token)
    if not access_token:
        raise HTTPException(status_code=401, detail="无效的刷新令牌")
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout", response_model=MessageResponse)
async def logout(request: Request):
    """用户登出"""
    try:
        body = await request.json()
        refresh_token = body.get("refresh_token")
        if not refresh_token:
            raise HTTPException(status_code=400, detail="缺少refresh_token参数")
        
        success = await AuthService.logout_user(refresh_token)
        if not success:
            raise HTTPException(status_code=400, detail="登出失败")
        
        return MessageResponse(message="登出成功")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"登出失败: {str(e)}")

@router.get("/me", response_model=dict)
async def get_current_user_info(current_user: UserModel = Depends(get_current_active_user)):
    """获取当前用户信息"""
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