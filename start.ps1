# WA错题本 一键启动脚本 (Windows)
# 右键 → 使用 PowerShell 运行，或在终端执行: .\start.ps1

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $ScriptDir

if (-not (Test-Path "venv")) {
    Write-Host "[WA] 未找到虚拟环境，正在创建..." -ForegroundColor Yellow
    python -m venv venv
}

& .\venv\Scripts\Activate.ps1

$flaskInstalled = pip show flask 2>$null
if (-not $flaskInstalled) {
    Write-Host "[WA] 正在安装依赖..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

Write-Host ""
Write-Host "[WA] 启动 WA错题本 v0.1.0..." -ForegroundColor Cyan
Write-Host "[WA] 访问地址: http://127.0.0.1:8083" -ForegroundColor Cyan
Write-Host "[WA] 按 Ctrl+C 停止服务" -ForegroundColor Gray
Write-Host ""

python run.py
