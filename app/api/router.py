"""
API 路由汇总
"""

from fastapi import APIRouter
from app.api.submission import router as submission_router
from app.api.stats import router as stats_router

api_router = APIRouter()

api_router.include_router(submission_router)
api_router.include_router(stats_router)
