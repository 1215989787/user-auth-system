from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.core.database import connect_to_mongo, close_mongo_connection
from app.api.v1 import router as api_router
import os

# 创建FastAPI应用
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="用户认证系统API",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件
if os.path.exists(settings.upload_dir):
    app.mount("/uploads", StaticFiles(directory=settings.upload_dir), name="uploads")

# 包含API路由
app.include_router(api_router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    """应用启动时连接MongoDB"""
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时断开MongoDB连接"""
    await close_mongo_connection()

@app.get("/")
def read_root():
    return {
        "message": "欢迎使用用户认证系统",
        "version": settings.app_version,
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 