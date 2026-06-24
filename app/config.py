"""
WA错题本 - 应用配置
"""

from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    """应用全局配置"""

    # 应用信息
    app_name: str = "WA错题本"
    version: str = "0.0.1"
    debug: bool = True

    # 服务器
    host: str = "127.0.0.1"
    port: int = 8000

    # 数据库
    database_url: str = "sqlite+aiosqlite:///./data/wa_notebook.db"

    # 支持的 OJ 平台
    supported_platforms: list[str] = ["luogu", "codeforces"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

# 确保 data 目录存在
Path("./data").mkdir(exist_ok=True)
