from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime

# 基础用户模式
class UserBase(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    gender: Optional[str] = None
    bio: Optional[str] = None

# 用户创建
class UserCreate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: Optional[str] = None
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    gender: Optional[str] = None
    birthday: Optional[datetime] = None
    bio: Optional[str] = None
    wechat_openid: Optional[str] = None
    wechat_unionid: Optional[str] = None

# 用户注册
class UserRegister(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: Optional[str] = None
    verification_code: Optional[str] = None
    login_type: str  # password, sms, wechat

# 用户登录
class UserLogin(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: Optional[str] = None
    verification_code: Optional[str] = None
    login_type: str  # password, sms, wechat

# 微信登录
class WechatLogin(BaseModel):
    code: str
    state: Optional[str] = None

# 验证码请求
class VerificationCodeRequest(BaseModel):
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    type: str  # login, register, reset

# 用户信息更新
class UserUpdate(BaseModel):
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    gender: Optional[str] = None
    birthday: Optional[datetime] = None
    bio: Optional[str] = None

# 密码修改
class PasswordChange(BaseModel):
    old_password: str
    new_password: str

# 手机/邮箱绑定
class BindRequest(BaseModel):
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    verification_code: str

# 用户响应
class UserResponse(BaseModel):
    id: str
    username: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    gender: Optional[str] = None
    birthday: Optional[datetime] = None
    bio: Optional[str] = None
    is_active: bool
    is_verified: bool
    email_verified: bool
    phone_verified: bool
    is_vip: bool
    vip_level: int
    vip_expire_time: Optional[datetime] = None
    vip_balance: float
    created_at: datetime
    last_login: Optional[datetime] = None

    @validator('id', pre=True)
    def validate_id(cls, v):
        if hasattr(v, '__str__'):
            return str(v)
        return v

    class Config:
        from_attributes = True
        populate_by_name = True

# 登录响应
class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse

# VIP订阅
class VIPSubscriptionCreate(BaseModel):
    plan_type: str  # monthly, yearly, lifetime
    amount: float
    currency: str = "CNY"
    payment_method: Optional[str] = None

class VIPSubscriptionResponse(BaseModel):
    id: str
    user_id: str
    plan_type: str
    amount: float
    currency: str
    status: str
    start_date: datetime
    end_date: datetime
    payment_method: Optional[str] = None
    transaction_id: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

# 验证码响应
class VerificationCodeResponse(BaseModel):
    message: str
    expires_in: int  # 秒数

# 通用响应
class MessageResponse(BaseModel):
    message: str 