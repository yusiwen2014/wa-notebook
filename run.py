# WA错题本 - Python 启动脚本
# 使用方法: python run.py

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,          # 开发模式热重载
        log_level="info",
        # 以下参数可选，用于生产环境：
        # workers=4,          # worker 进程数
        # ssl_certfile="...", # HTTPS 证书
        # ssl_keyfile="...",
    )
