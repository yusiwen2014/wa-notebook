#!/bin/bash
# WA错题本 一键启动脚本 (macOS / Linux)

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

if [ ! -d "venv" ]; then
    echo "[WA] 未找到虚拟环境，正在创建..."
    python3 -m venv venv
fi

source venv/bin/activate

if ! pip show flask >/dev/null 2>&1; then
    echo "[WA] 正在安装依赖..."
    pip install -r requirements.txt
fi

echo "[WA] 启动 WA错题本 v0.1.0..."
echo "[WA] 访问地址: http://127.0.0.1:8083"
echo "[WA] 按 Ctrl+C 停止服务"
echo ""

python run.py
