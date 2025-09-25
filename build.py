#!/usr/bin/env python3
"""
Photo Watermark 2 构建脚本
使用 PyInstaller 创建可执行文件
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def main():
    """主构建函数"""
    print("=== Photo Watermark 2 构建脚本 ===")

    # 获取项目根目录
    project_root = Path(__file__).parent.absolute()
    dist_dir = project_root / "dist"
    build_dir = project_root / "build"

    print(f"项目根目录: {project_root}")

    # 清理之前的构建
    if dist_dir.exists():
        print("清理之前的构建文件...")
        shutil.rmtree(dist_dir)
    if build_dir.exists():
        shutil.rmtree(build_dir)

    # 安装依赖
    print("安装构建依赖...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller", "pillow"])

    # PyInstaller 构建命令
    cmd = [
        "pyinstaller",
        "--onefile",  # 单文件模式
        "--windowed",  # 无控制台窗口
        "--name", "PhotoWatermark2",
        "--icon", str(project_root / "assets" / "icon.ico") if (project_root / "assets" / "icon.ico").exists() else None,
        "--add-data", f"{project_root / 'photo_watermark'};photo_watermark",
        "--hidden-import", "PIL._tkinter_finder",
        "--hidden-import", "tkinter",
        "--hidden-import", "tkinter.ttk",
        "--hidden-import", "tkinter.filedialog",
        "--hidden-import", "tkinter.messagebox",
        "--hidden-import", "tkinter.simpledialog",
        "run.py"
    ]

    # 移除空的icon参数
    cmd = [arg for arg in cmd if arg is not None]

    print("开始构建可执行文件...")
    print(f"执行命令: {' '.join(cmd)}")

    try:
        # 在项目根目录执行构建
        os.chdir(project_root)
        subprocess.check_call(cmd)

        print("\n✅ 构建成功！")

        # 检查输出文件
        exe_file = dist_dir / "PhotoWatermark2.exe"
        if exe_file.exists():
            file_size = exe_file.stat().st_size / (1024 * 1024)  # MB
            print(f"📦 可执行文件: {exe_file}")
            print(f"📊 文件大小: {file_size:.1f} MB")
        else:
            print("❌ 未找到可执行文件")
            return False

        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ 构建失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 构建过程中出现错误: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
    print("\n🎉 构建完成！可执行文件位于 dist/ 目录中")