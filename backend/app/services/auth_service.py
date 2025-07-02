from app.models.user import UserModel, VerificationCodeModel, UserSessionModel, PyObjectId
from app.schemas.user import UserRegister, UserLogin, WechatLogin
from app.core.security import (
    verify_password, get_password_hash, create_access_token, 
    create_refresh_token, verify_token
)
from app.core.database import get_database
from app.services.user_service import UserService
from datetime import datetime, timedelta
import requests
from typing import Optional, Tuple
import re
from bson import ObjectId

class AuthService:
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """验证手机号格式"""
        pattern = r'^1[3-9]\d{9}$'
        return bool(re.match(pattern, phone))
    
    @staticmethod
    def validate_password(password: str) -> bool:
        """验证密码强度"""
        if len(password) < 6:
            return False
        return True
    
    @staticmethod
    async def get_user_by_identifier(identifier: str) -> Optional[UserModel]:
        """通过用户名、邮箱或手机号获取用户"""
        # 尝试通过用户名查找
        user = await UserService.get_user_by_username(identifier)
        if user:
            return user
        
        # 尝试通过邮箱查找
        user = await UserService.get_user_by_email(identifier)
        if user:
            return user
        
        # 尝试通过手机号查找
        user = await UserService.get_user_by_phone(identifier)
        if user:
            return user
        
        return None
    
    @staticmethod
    async def create_verification_code(phone: str = None, email: str = None, 
                                     code_type: str = "login") -> Tuple[str, int]:
        """创建验证码"""
        code = await UserService.generate_verification_code(phone, email, code_type)
        return code, 300  # 5分钟过期
    
    @staticmethod
    async def verify_code(phone: str = None, email: str = None, 
                         code: str = None, code_type: str = "login") -> bool:
        """验证验证码"""
        return await UserService.verify_code(phone, email, code, code_type)
    
    @staticmethod
    async def register_user(user_data: UserRegister) -> Tuple[Optional[UserModel], str]:
        """注册用户"""
        # 验证登录类型
        if user_data.login_type == "password":
            if not user_data.username or not user_data.password:
                return None, "用户名和密码不能为空"
            
            if not AuthService.validate_password(user_data.password):
                return None, "密码长度至少6位"
            
            # 检查用户名是否已存在
            existing_user = await UserService.get_user_by_username(user_data.username)
            if existing_user:
                return None, "该用户已注册"
            
            # 创建用户
            from ..schemas.user import UserCreate
            user_create = UserCreate(
                username=user_data.username,
                password=user_data.password,
                nickname=user_data.username
            )
            
            user, message = await UserService.create_user(user_create)
            return user, message
            
        elif user_data.login_type == "sms":
            if not user_data.phone or not user_data.verification_code:
                return None, "手机号和验证码不能为空"
            
            if not AuthService.validate_phone(user_data.phone):
                return None, "手机号格式不正确"
            
            # 验证验证码
            if not await AuthService.verify_code(phone=user_data.phone, 
                                               code=user_data.verification_code, 
                                               code_type="register"):
                return None, "验证码错误或已过期"
            
            # 检查手机号是否已存在
            existing_user = await UserService.get_user_by_phone(user_data.phone)
            if existing_user:
                return None, "该用户已注册"
            
            # 创建用户
            from ..schemas.user import UserCreate
            user_create = UserCreate(
                phone=user_data.phone,
                nickname=f"用户{user_data.phone[-4:]}"
            )
            
            user, message = await UserService.create_user(user_create)
            if user:
                # 更新手机号验证状态
                db = get_database()
                await db.users.update_one(
                    {"_id": user.id},
                    {"$set": {"phone_verified": True}}
                )
            
            return user, message
        
        else:
            return None, "不支持的登录类型"
    
    @staticmethod
    async def login_user(login_data: UserLogin) -> Tuple[Optional[UserModel], str]:
        """用户登录"""
        if login_data.login_type == "password":
            if not login_data.username or not login_data.password:
                return None, "用户名和密码不能为空"
            
            user = await AuthService.get_user_by_identifier(login_data.username)
            if not user or not user.hashed_password:
                return None, "用户名或密码错误"
            
            if not verify_password(login_data.password, user.hashed_password):
                return None, "用户名或密码错误"
            
        elif login_data.login_type == "sms":
            if not login_data.phone or not login_data.verification_code:
                return None, "手机号和验证码不能为空"
            
            if not AuthService.validate_phone(login_data.phone):
                return None, "手机号格式不正确"
            
            # 验证验证码
            if not await AuthService.verify_code(phone=login_data.phone, 
                                               code=login_data.verification_code, 
                                               code_type="login"):
                return None, "验证码错误或已过期"
            
            user = await UserService.get_user_by_phone(login_data.phone)
            if not user:
                return None, "用户不存在"
        
        else:
            return None, "不支持的登录类型"
        
        if not user.is_active:
            return None, "账户已被禁用"
        
        # 更新最后登录时间
        db = get_database()
        await db.users.update_one(
            {"_id": user.id},
            {"$set": {"last_login": datetime.utcnow()}}
        )
        
        return user, "登录成功"
    
    @staticmethod
    async def wechat_login(wechat_data: WechatLogin) -> Tuple[Optional[UserModel], str]:
        """微信登录"""
        from ..core.config import settings
        
        if not settings.wechat_app_id or not settings.wechat_app_secret:
            return None, "微信登录未配置"
        
        try:
            # 获取微信access_token
            token_url = "https://api.weixin.qq.com/sns/oauth2/access_token"
            token_params = {
                "appid": settings.wechat_app_id,
                "secret": settings.wechat_app_secret,
                "code": wechat_data.code,
                "grant_type": "authorization_code"
            }
            
            response = requests.get(token_url, params=token_params)
            token_data = response.json()
            
            if "errcode" in token_data:
                return None, f"微信登录失败: {token_data.get('errmsg', '未知错误')}"
            
            access_token = token_data.get("access_token")
            openid = token_data.get("openid")
            
            if not access_token or not openid:
                return None, "获取微信用户信息失败"
            
            # 获取用户信息
            user_info_url = "https://api.weixin.qq.com/sns/userinfo"
            user_params = {
                "access_token": access_token,
                "openid": openid,
                "lang": "zh_CN"
            }
            
            response = requests.get(user_info_url, params=user_params)
            user_info = response.json()
            
            if "errcode" in user_info:
                return None, f"获取微信用户信息失败: {user_info.get('errmsg', '未知错误')}"
            
            # 查找或创建用户
            db = get_database()
            user_data = await db.users.find_one({"wechat_openid": openid})
            
            if user_data:
                user_data["_id"] = PyObjectId(user_data["_id"])
                user = UserModel(**user_data)
                # 更新最后登录时间
                await db.users.update_one(
                    {"_id": user.id},
                    {"$set": {"last_login": datetime.utcnow()}}
                )
                return user, "登录成功"
            else:
                # 创建新用户
                from ..schemas.user import UserCreate
                user_create = UserCreate(
                    wechat_openid=openid,
                    wechat_unionid=user_info.get("unionid"),
                    nickname=user_info.get("nickname", f"微信用户{openid[-6:]}"),
                    avatar=user_info.get("headimgurl")
                )
                
                user, message = await UserService.create_user(user_create)
                return user, message
                
        except Exception as e:
            return None, f"微信登录异常: {str(e)}"
    
    @staticmethod
    def create_tokens(user: UserModel) -> Tuple[str, str]:
        """创建访问令牌和刷新令牌"""
        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token = create_refresh_token(data={"sub": str(user.id)})
        return access_token, refresh_token
    
    @staticmethod
    async def save_user_session(user_id: str, refresh_token: str, 
                               device_info: str = None, ip_address: str = None) -> UserSessionModel:
        """保存用户会话"""
        # 保证user_id为PyObjectId类型
        from app.models.user import PyObjectId
        if not isinstance(user_id, PyObjectId):
            user_id = PyObjectId(user_id)
        session = UserSessionModel(
            user_id=user_id,
            refresh_token=refresh_token,
            device_info=device_info,
            ip_address=ip_address,
            expires_at=datetime.utcnow() + timedelta(days=7)
        )
        
        db = get_database()
        await db.user_sessions.insert_one(session.dict())
        return session
    
    @staticmethod
    async def refresh_access_token(refresh_token: str) -> Optional[str]:
        """刷新访问令牌"""
        try:
            payload = verify_token(refresh_token)
            user_id = payload.get("sub")
            if not user_id:
                return None
            
            # 验证刷新令牌是否在数据库中
            db = get_database()
            session_data = await db.user_sessions.find_one({
                "refresh_token": refresh_token,
                "is_active": True,
                "expires_at": {"$gt": datetime.utcnow()}
            })
            
            if not session_data:
                return None
            
            # 创建新的访问令牌
            access_token = create_access_token(data={"sub": user_id})
            return access_token
            
        except Exception:
            return None
    
    @staticmethod
    async def logout_user(refresh_token: str) -> bool:
        """用户登出"""
        try:
            db = get_database()
            result = await db.user_sessions.update_one(
                {"refresh_token": refresh_token},
                {"$set": {"is_active": False}}
            )
            return result.modified_count > 0
        except Exception:
            return False 