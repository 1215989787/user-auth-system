from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return handler(source_type)
    
    @classmethod
    def validate(cls, v):
        if isinstance(v, cls):
            return v
        if isinstance(v, str):
            if not ObjectId.is_valid(v):
                raise ValueError("Invalid ObjectId")
            return cls(v)
        if isinstance(v, ObjectId):
            return cls(str(v))
        raise ValueError("Invalid ObjectId")

class UserModel(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    
    # 基本信息
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    hashed_password: Optional[str] = None
    
    # 个人信息
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    gender: Optional[str] = None  # male, female, other
    birthday: Optional[datetime] = None
    bio: Optional[str] = None
    
    # 认证信息
    is_active: bool = True
    is_verified: bool = False
    email_verified: bool = False
    phone_verified: bool = False
    
    # 微信信息
    wechat_openid: Optional[str] = None
    wechat_unionid: Optional[str] = None
    
    # VIP信息
    is_vip: bool = False
    vip_level: int = 0  # 0: 普通用户, 1: VIP, 2: SVIP
    vip_expire_time: Optional[datetime] = None
    vip_balance: float = 0.0
    
    # 时间戳
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "username": "testuser",
                "email": "test@example.com",
                "phone": "13800138000",
                "nickname": "测试用户",
                "is_active": True,
                "is_vip": False
            }
        }

class VerificationCodeModel(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    phone: Optional[str] = None
    email: Optional[str] = None
    code: str
    type: str  # login, register, reset
    is_used: bool = False
    expires_at: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class UserSessionModel(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    refresh_token: str
    device_info: Optional[str] = None
    ip_address: Optional[str] = None
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class VIPSubscriptionModel(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    plan_type: str  # monthly, yearly, lifetime
    amount: float
    currency: str = "CNY"
    status: str = "active"  # active, expired, cancelled
    start_date: datetime = Field(default_factory=datetime.utcnow)
    end_date: datetime
    payment_method: Optional[str] = None
    transaction_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str} 