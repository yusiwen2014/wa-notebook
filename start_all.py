#!/usr/bin/env python3
"""一键启动 WA错题本后端 + baidu-2api + DDG2API

支持 macOS / Windows / Linux。
依赖：
  - Python 3.10+（已创建 venv 虚拟环境）
  - Node.js 18+（用于运行 DDG2API）

用法：
  python start_all.py
"""
import os
import sys
import subprocess
import time
import signal
import platform

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SYSTEM = platform.system().lower()


def get_venv_python():
    """获取当前虚拟环境的 Python 解释器"""
    if hasattr(sys, "real_prefix") or (hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix):
        # 已经在虚拟环境中
        return sys.executable
    # 未在虚拟环境中，尝试自动寻找 venv
    if SYSTEM == "windows":
        return os.path.join(PROJECT_ROOT, "venv", "Scripts", "python.exe")
    return os.path.join(PROJECT_ROOT, "venv", "bin", "python")


def get_node():
    """获取 node 可执行文件"""
    return "node"


def start_service(name, cmd, cwd):
    """启动子服务"""
    print(f"[启动] {name}")
    if SYSTEM == "windows":
        p = subprocess.Popen(cmd, cwd=cwd, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
    else:
        p = subprocess.Popen(cmd, cwd=cwd, shell=True)
    processes.append((name, p))
    return p


def stop_all():
    """停止所有服务"""
    print("\n[停止] 正在关闭所有服务...")
    for name, p in processes:
        try:
            p.terminate()
            print(f"[停止] {name}")
        except Exception:
            pass
    sys.exit(0)


signal.signal(signal.SIGINT, lambda s, f: stop_all())
if SYSTEM != "windows":
    signal.signal(signal.SIGTERM, lambda s, f: stop_all())

processes = []


def main():
    venv_python = get_venv_python()
    node = get_node()

    if not os.path.exists(venv_python):
        print(f"[错误] 未找到虚拟环境 Python: {venv_python}")
        print("请先创建虚拟环境：python -m venv venv")
        sys.exit(1)

    # 1. 启动 baidu-2api (端口 8000)
    start_service(
        "baidu-2api",
        f"{venv_python} main.py",
        os.path.join(PROJECT_ROOT, "third_party", "baidu-2api"),
    )

    # 2. 启动 DDG2API (端口 3000)
    start_service(
        "DDG2API",
        f"{node} index.js",
        os.path.join(PROJECT_ROOT, "third_party", "DDG2API"),
    )

    # 3. 启动 WA错题本主后端 (端口 8083)
    start_service(
        "WA后端",
        f"{venv_python} run.py",
        PROJECT_ROOT,
    )

    print("\n所有服务已启动：")
    print("  - baidu-2api: http://127.0.0.1:8000")
    print("  - DDG2API:    http://127.0.0.1:3000")
    print("  - WA主后端:   http://127.0.0.1:8083")
    print("按 Ctrl+C 停止所有服务\n")

    while True:
        time.sleep(1)
        for name, p in processes:
            ret = p.poll()
            if ret is not None:
                print(f"[警告] {name} 已退出，返回码: {ret}")


if __name__ == "__main__":
    main()
