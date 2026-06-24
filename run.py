# WA错题本 - Python 启动脚本
# 使用方法: python run.py

import asyncio
from app.main import app
from app.config import settings

if __name__ == "__main__":
    app.run(host=settings.host, port=settings.port, debug=settings.debug)
