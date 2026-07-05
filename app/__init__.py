from flask import Flask
from flask_cors import CORS
from app.config import settings
from app.api import ai


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "wa-notebook-secret-key"
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    app.register_blueprint(ai.ai_bp, url_prefix="/api/ai")

    @app.route("/health")
    def health():
        return {"status": "ok", "app": settings.app_name, "version": settings.version}

    return app
