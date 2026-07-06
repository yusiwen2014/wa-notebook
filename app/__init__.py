from flask import Flask, send_from_directory
import os
from flask_cors import CORS
from app.config import settings
from app.api import ai, userdata


def create_app():
    app = Flask(__name__, static_folder=None)
    app.config["SECRET_KEY"] = "wa-notebook-secret-key"
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    app.register_blueprint(ai.ai_bp, url_prefix="/api/ai")
    app.register_blueprint(userdata.user_bp, url_prefix="/api")

    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    @app.route("/")
    def index():
        return send_from_directory(PROJECT_ROOT, "app.html")

    @app.route("/app")
    def app_page():
        return send_from_directory(PROJECT_ROOT, "app.html")

    @app.route("/health")
    def health():
        return {"status": "ok", "app": settings.app_name, "version": settings.version}

    return app
