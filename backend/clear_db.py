import motor.motor_asyncio
import asyncio

MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "user_auth_system"

async def clear_collections():
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    collections = ["users", "user_sessions", "verification_codes", "vipsubscriptions"]
    for col in collections:
        result = await db[col].delete_many({})
        print(f"已清空集合 {col}，删除文档数: {result.deleted_count}")
    client.close()
    print("✅ 数据库清理完成！")

if __name__ == "__main__":
    asyncio.run(clear_collections()) 