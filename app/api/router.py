"""
WA错题本 - API 路由汇总
"""

from app.api.submission import bp as submission_bp
from app.api.stats import bp as stats_bp

__all__ = ["submission_bp", "stats_bp"]
