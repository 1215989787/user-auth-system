from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # 应用配置
    app_name: str = "用户认证系统"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # MongoDB配置
    mongodb_url: str = "mongodb://localhost:27017"
    mongodb_database: str = "user_auth_system"
    
    # JWT配置
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # 微信配置
    wechat_app_id: Optional[str] = None
    wechat_app_secret: Optional[str] = None
    
    # 短信配置
    sms_api_key: Optional[str] = None
    sms_api_secret: Optional[str] = None
    
    # 邮件配置
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None
    
    # Redis配置
    redis_url: str = "redis://localhost:6379"
    
    # 文件上传配置
    upload_dir: str = "uploads"
    max_file_size: int = 5 * 1024 * 1024  # 5MB
    
    class Config:
        env_file = ".env"

settings = Settings()

# 确保上传目录存在
os.makedirs(settings.upload_dir, exist_ok=True) 