from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings

class Database:
    client: AsyncIOMotorClient = None
    database = None

db = Database()

async def connect_to_mongo():
    """连接到MongoDB数据库"""
    db.client = AsyncIOMotorClient(settings.mongodb_url)
    db.database = db.client[settings.mongodb_database]
    print(f"✅ 已连接到MongoDB数据库: {settings.mongodb_database}")

async def close_mongo_connection():
    """关闭MongoDB连接"""
    if db.client:
        db.client.close()
        print("🔌 已关闭MongoDB连接")

def get_database():
    """获取数据库实例"""
    return db.database 