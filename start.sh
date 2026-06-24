#!/usr/bin/env bash
# WA错题本 - 通用启动脚本
# 兼容 bash / zsh / fish (fish 用户请运行: bash start.sh)

set -e

# 获取脚本所在目录（项目根目录）
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_PYTHON="$PROJECT_DIR/venv/bin/python"

if [ ! -f "$VENV_PYTHON" ]; then
    echo "❌ 错误: 未找到虚拟环境 Python: $VENV_PYTHON"
    echo "请先执行以下命令安装依赖:"
    echo "  cd $PROJECT_DIR"
    echo "  python -m venv venv"
    echo "  ./venv/bin/pip install -r requirements.txt"
    exit 1
fi

cd "$PROJECT_DIR"
echo "🚀 正在启动 WA错题本..."
exec "$VENV_PYTHON" run.py
