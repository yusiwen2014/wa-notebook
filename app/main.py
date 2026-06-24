"""
WA错题本 - Flask 应用入口
"""

import asyncio
import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from app.config import settings
from app.models.database import init_db
from app.api.submission import bp as submission_bp
from app.api.stats import bp as stats_bp
from app.api.chat import chat_bp as chat_bp

# 项目根目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(PROJECT_ROOT, "static")

app = Flask(__name__, static_folder=STATIC_DIR, static_url_path="/static")
CORS(app)

app.register_blueprint(submission_bp)
app.register_blueprint(stats_bp)
app.register_blueprint(chat_bp)

_first_request_done = False


@app.before_request
def before_first():
    global _first_request_done
    if not _first_request_done:
        _first_request_done = True
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(init_db())
        print(f"\n🚀 {settings.app_name} v{settings.version} 启动成功")
        print(f"   📂 数据库: {settings.database_url}")
        print(f"   🌐 地址: http://{settings.host}:{settings.port}\n")


@app.route("/")
def root():
    return send_from_directory(STATIC_DIR, "index.html")


@app.route("/health")
def health_check():
    return jsonify({"status": "ok", "version": settings.version})


if __name__ == "__main__":
    app.run(host=settings.host, port=settings.port, debug=settings.debug)
