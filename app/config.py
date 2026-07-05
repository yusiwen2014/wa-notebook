import os
from pathlib import Path

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
DB_PATH = os.path.join(DATA_DIR, "wa_notebook.db")


class Settings:
    app_name = "WA错题本"
    version = "0.0.3"
    debug = True
    host = "127.0.0.1"
    port = 8083
    database_url = f"sqlite:///{DB_PATH}"
    supported_platforms = ["luogu", "codeforces"]


settings = Settings()
Path(DATA_DIR).mkdir(exist_ok=True)
