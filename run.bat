@echo off
echo 正在启动 Photo Watermark 2...
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Python，请先安装Python 3.7+
    pause
    exit /b 1
)

REM 尝试安装依赖
echo 检查并安装依赖...
pip install pillow >nul 2>&1

REM 启动程序
echo 启动应用程序...
python run.py

if %errorlevel% neq 0 (
    echo.
    echo 程序启动失败，按任意键退出...
    pause >nul
)