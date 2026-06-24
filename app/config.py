"""
WA错题本 - 应用配置
"""

import os
from pathlib import Path


# 项目根目录（基于本文件位置）
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
DB_PATH = os.path.join(DATA_DIR, "wa_notebook.db")


class Settings:
    app_name = "WA错题本"
    version = "0.0.2"
    debug = True
    host = "127.0.0.1"
    port = 8081
    # 使用绝对路径确保无论从哪启动都能找到数据库
    database_url = f"sqlite+aiosqlite:///{DB_PATH}"
    supported_platforms = ["luogu", "codeforces"]


settings = Settings()

# 确保 data 目录存在
Path(DATA_DIR).mkdir(exist_ok=True)
