"""用户数据存储 API：把对话、设置、个人模型等数据落盘到 userdata/ 目录，方便迁移和查看。

约定目录：
    userdata/
        profile.json          # 用户偏好（用户名、主题、设置等）
        conversations.json    # 所有历史对话（含 problem 字段）
        custom_models.json    # 用户自建模型
        problem_<id>.md      # 每道错题一个独立 markdown（自动生成）
        backups/             # 自动备份目录
"""
import os
import re
import time
import json
from datetime import datetime
from flask import Blueprint, request, jsonify, send_from_directory, abort

user_bp = Blueprint("user", __name__)

# 落盘目录
USERDATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "userdata")
BACKUP_DIR = os.path.join(USERDATA_DIR, "backups")
os.makedirs(USERDATA_DIR, exist_ok=True)
os.makedirs(BACKUP_DIR, exist_ok=True)


def _safe_path(name: str) -> str:
    """防止路径穿越。"""
    if "/" in name or "\\" in name or ".." in name:
        abort(400, "非法文件名")
    return os.path.join(USERDATA_DIR, name)


def _read(name: str, default):
    p = _safe_path(name)
    if not os.path.exists(p):
        return default
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def _write(name: str, data) -> None:
    p = _safe_path(name)
    tmp = p + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, p)


# === 读 / 写 整块数据 ===
@user_bp.route("/userdata/<name>", methods=["GET"])
def get_userdata(name):
    if not name.endswith(".json"):
        abort(400, "只支持 .json 文件")
    return jsonify(_read(name, default=None) if False else _read(name, default={}) or {})


@user_bp.route("/userdata/<name>", methods=["PUT", "POST"])
def put_userdata(name):
    if not name.endswith(".json"):
        abort(400, "只支持 .json 文件")
    data = request.get_json(force=True, silent=True)
    if data is None:
        return jsonify({"error": "body 必须是 JSON"}), 400
    # 自动备份上一版
    old = _read(name, default=None)
    if old:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        _write(os.path.join("backups", f"{name}.{ts}.bak"), old)
    _write(name, data)
    return jsonify({"ok": True, "size": os.path.getsize(_safe_path(name))})


# === 把每个对话导出为独立 Markdown 文件 ===
@user_bp.route("/userdata/export-md", methods=["POST"])
def export_md():
    """把 convs: [{id,title,ts,messages,problem}] 列表写入 userdata/problems/ 下，每个对话一个 .md"""
    data = request.get_json(force=True)
    convs = data.get("conversations", [])
    out_dir = os.path.join(USERDATA_DIR, "problems")
    os.makedirs(out_dir, exist_ok=True)
    n = 0
    for c in convs:
        cid = re.sub(r"[^\w\-]+", "_", c.get("id", f"conv_{int(time.time())}"))[:64]
        fp = os.path.join(out_dir, f"{cid}.md")
        title = c.get("title", "未命名")
        ts = c.get("ts", 0)
        date = datetime.fromtimestamp(ts / 1000).strftime("%Y-%m-%d %H:%M") if ts else "未知时间"
        p = c.get("problem") or {}
        lines = [f"# {title}", f"", f"**时间**：{date}"]
        if p.get("platform") or p.get("id") or p.get("link"):
            lines.append("")
            lines.append("## 题目基本信息")
            if p.get("platform"): lines.append(f"- **平台**：{p['platform']}")
            if p.get("id"): lines.append(f"- **题号**：{p['id']}")
            if p.get("link"): lines.append(f"- **链接**：{p['link']}")
        if p.get("code"):
            lines.append("")
            lines.append("## 用户代码")
            lines.append("")
            lang = ""
            first = p["code"].splitlines()[0] if p["code"] else ""
            if "def " in p["code"] or "import " in p["code"] or "print(" in p["code"]:
                lang = "python"
            elif "#include" in p["code"] or "using namespace" in p["code"]:
                lang = "cpp"
            elif "public static" in p["code"] or "public class" in p["code"]:
                lang = "java"
            lines.append(f"```{lang}")
            lines.append(p["code"].rstrip())
            lines.append("```")
        lines.append("")
        lines.append("## 对话记录")
        lines.append("")
        for m in c.get("messages", []):
            role = "用户" if m.get("role") == "user" else "AI"
            content = (m.get("content") or "").rstrip()
            lines.append(f"### {role}")
            lines.append("")
            lines.append(content)
            lines.append("")
        with open(fp, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        n += 1
    return jsonify({"ok": True, "files": n, "dir": out_dir})


# === 列出已导出的错题文件 ===
@user_bp.route("/userdata/problems", methods=["GET"])
def list_problems():
    out_dir = os.path.join(USERDATA_DIR, "problems")
    os.makedirs(out_dir, exist_ok=True)
    items = []
    for fn in sorted(os.listdir(out_dir), reverse=True):
        if not fn.endswith(".md"):
            continue
        fp = os.path.join(out_dir, fn)
        st = os.stat(fp)
        items.append({"name": fn, "size": st.st_size, "mtime": st.st_mtime})
    return jsonify({"items": items, "dir": out_dir})


@user_bp.route("/userdata/problems/<name>", methods=["GET"])
def read_problem(name):
    if "/" in name or ".." in name or not name.endswith(".md"):
        abort(400, "非法文件名")
    out_dir = os.path.join(USERDATA_DIR, "problems")
    return send_from_directory(out_dir, name, mimetype="text/markdown")
