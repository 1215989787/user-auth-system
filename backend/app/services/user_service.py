from app.models.user import UserModel, VerificationCodeModel, PyObjectId
from app.schemas.user import UserCreate, UserUpdate, PasswordChange, BindRequest, VIPSubscriptionCreate
from app.core.security import verify_password, get_password_hash
from app.core.database import get_database
from datetime import datetime, timedelta
from typing import Optional, List, Tuple
import os
import shutil
from PIL import Image
import uuid
import random
import string
from bson import ObjectId

class UserService:
    
    @staticmethod
    async def get_user_by_id(user_id: str) -> Optional[UserModel]:
        """根据ID获取用户"""
        db = get_database()
        user_data = await db.users.find_one({"_id": ObjectId(user_id)})
        if user_data:
            if not isinstance(user_data["_id"], PyObjectId):
                user_data["_id"] = PyObjectId(user_data["_id"])
            return UserModel(**user_data)
        return None
    
    @staticmethod
    async def get_user_by_username(username: str) -> Optional[UserModel]:
        """根据用户名获取用户"""
        db = get_database()
        user_data = await db.users.find_one({"username": username})
        if user_data:
            if not isinstance(user_data["_id"], PyObjectId):
                user_data["_id"] = PyObjectId(user_data["_id"])
            return UserModel(**user_data)
        return None
    
    @staticmethod
    async def get_user_by_email(email: str) -> Optional[UserModel]:
        """根据邮箱获取用户"""
        db = get_database()
        user_data = await db.users.find_one({"email": email})
        if user_data:
            if not isinstance(user_data["_id"], PyObjectId):
                user_data["_id"] = PyObjectId(user_data["_id"])
            return UserModel(**user_data)
        return None
    
    @staticmethod
    async def get_user_by_phone(phone: str) -> Optional[UserModel]:
        """根据手机号获取用户"""
        db = get_database()
        user_data = await db.users.find_one({"phone": phone})
        if user_data:
            if not isinstance(user_data["_id"], PyObjectId):
                user_data["_id"] = PyObjectId(user_data["_id"])
            return UserModel(**user_data)
        return None
    
    @staticmethod
    async def create_user(user_data: UserCreate) -> Tuple[Optional[UserModel], str]:
        """创建新用户"""
        db = get_database()
        
        # 检查用户名是否已存在
        if user_data.username:
            existing_user = await UserService.get_user_by_username(user_data.username)
            if existing_user:
                return None, "该用户已注册"
        
        # 检查邮箱是否已存在
        if user_data.email:
            existing_user = await UserService.get_user_by_email(user_data.email)
            if existing_user:
                return None, "该用户已注册"
        
        # 检查手机号是否已存在
        if user_data.phone:
            existing_user = await UserService.get_user_by_phone(user_data.phone)
            if existing_user:
                return None, "该用户已注册"
        
        # 创建用户模型
        user_dict = user_data.dict()
        if user_data.password:
            user_dict["hashed_password"] = get_password_hash(user_data.password)
            del user_dict["password"]
        
        user_dict["created_at"] = datetime.utcnow()
        user_dict["updated_at"] = datetime.utcnow()
        
        # 插入数据库
        result = await db.users.insert_one(user_dict)
        user_dict["_id"] = PyObjectId(result.inserted_id)
        
        return UserModel(**user_dict), "用户创建成功"
    
    @staticmethod
    async def update_user_profile(user_id: str, user_data: UserUpdate) -> Tuple[Optional[UserModel], str]:
        """更新用户资料"""
        user = await UserService.get_user_by_id(user_id)
        if not user:
            return None, "用户不存在"
        
        # 更新字段
        update_data = user_data.dict(exclude_unset=True)
        update_data["updated_at"] = datetime.utcnow()
        
        db = get_database()
        await db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
        
        # 返回更新后的用户
        updated_user = await UserService.get_user_by_id(user_id)
        return updated_user, "资料更新成功"
    
    @staticmethod
    async def change_password(user_id: str, password_data: PasswordChange) -> Tuple[bool, str]:
        """修改密码"""
        user = await UserService.get_user_by_id(user_id)
        if not user or not user.hashed_password:
            return False, "用户不存在或未设置密码"
        
        # 验证旧密码
        if not verify_password(password_data.old_password, user.hashed_password):
            return False, "旧密码错误"
        
        # 验证新密码强度
        if len(password_data.new_password) < 6:
            return False, "新密码长度至少6位"
        
        # 更新密码
        db = get_database()
        await db.users.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    "hashed_password": get_password_hash(password_data.new_password),
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        return True, "密码修改成功"
    
    @staticmethod
    async def verify_user_credentials(username_or_email: str, password: str) -> Optional[UserModel]:
        """验证用户凭据"""
        # 尝试通过用户名或邮箱查找用户
        user = await UserService.get_user_by_username(username_or_email)
        if not user:
            user = await UserService.get_user_by_email(username_or_email)
        
        if not user or not user.hashed_password:
            return None
        
        if not verify_password(password, user.hashed_password):
            return None
        
        return user
    
    @staticmethod
    async def generate_verification_code(phone: str = None, email: str = None, code_type: str = "register") -> str:
        """生成验证码"""
        code = ''.join(random.choices(string.digits, k=6))
        
        # 创建验证码记录
        verification_code = VerificationCodeModel(
            phone=phone,
            email=email,
            code=code,
            type=code_type,
            expires_at=datetime.utcnow() + timedelta(minutes=5)
        )
        
        db = get_database()
        await db.verification_codes.insert_one(verification_code.dict())
        
        return code
    
    @staticmethod
    async def verify_code(phone: str = None, email: str = None, code: str = None, code_type: str = "register") -> bool:
        """验证验证码"""
        db = get_database()
        
        # 查找验证码
        query = {
            "code": code,
            "type": code_type,
            "is_used": False,
            "expires_at": {"$gt": datetime.utcnow()}
        }
        
        if phone:
            query["phone"] = phone
        elif email:
            query["email"] = email
        
        verification_code = await db.verification_codes.find_one(query)
        
        if not verification_code:
            return False
        
        # 标记验证码为已使用
        await db.verification_codes.update_one(
            {"_id": verification_code["_id"]},
            {"$set": {"is_used": True}}
        )
        
        return True
    
    @staticmethod
    async def get_vip_info(user_id: str) -> dict:
        """获取VIP信息"""
        user = await UserService.get_user_by_id(user_id)
        if not user:
            return {}
        
        return {
            "is_vip": user.is_vip,
            "vip_level": user.vip_level,
            "vip_expire_time": user.vip_expire_time,
            "vip_balance": user.vip_balance,
            "vip_benefits": UserService.get_vip_benefits(user.vip_level)
        }
    
    @staticmethod
    def get_vip_benefits(vip_level: int) -> List[str]:
        """获取VIP权益"""
        benefits = {
            0: ["基础功能"],
            1: ["基础功能", "无广告", "高清画质", "优先客服"],
            2: ["基础功能", "无广告", "高清画质", "优先客服", "专属内容", "无限下载"]
        }
        return benefits.get(vip_level, ["基础功能"]) 