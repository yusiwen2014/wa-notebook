"""
WA错题本 - FastAPI 应用入口
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.config import settings
from app.models.database import init_db
from app.api.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时
    await init_db()
    print(f"\n🚀 {settings.app_name} v{settings.version} 启动成功")
    print(f"   📂 数据库: {settings.database_url}")
    print(f"   🌐 地址: http://{settings.host}:{settings.port}")
    print(f"   📖 API文档: http://{settings.host}:{settings.port}/docs\n")

    yield

    # 关闭时
    print("\n👋 应用已关闭")


app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="面向 OI/ACM 竞赛选手的智能错题管理平台",
    lifespan=lifespan,
)

# 注册 API 路由
app.include_router(api_router)

# 挂载静态文件
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    """首页"""
    return FileResponse("static/index.html")


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "ok", "version": settings.version}
