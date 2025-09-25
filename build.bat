@echo off
echo === Photo Watermark 2 Windows 构建脚本 ===

REM 安装依赖
echo 安装构建依赖...
python -m pip install pyinstaller pillow

REM 清理之前的构建
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"

REM 构建可执行文件
echo 开始构建可执行文件...
pyinstaller --onefile --windowed --name "PhotoWatermark2" --add-data "photo_watermark;photo_watermark" --hidden-import "PIL._tkinter_finder" --hidden-import "tkinter" --hidden-import "tkinter.ttk" --hidden-import "tkinter.filedialog" --hidden-import "tkinter.messagebox" --hidden-import "tkinter.simpledialog" run.py

if exist "dist\PhotoWatermark2.exe" (
    echo.
    echo ✅ 构建成功！
    echo 📦 可执行文件: dist\PhotoWatermark2.exe
    dir "dist\PhotoWatermark2.exe"
    echo.
    echo 🎉 构建完成！可执行文件位于 dist\ 目录中
) else (
    echo ❌ 构建失败！未找到可执行文件
    exit /b 1
)

pause