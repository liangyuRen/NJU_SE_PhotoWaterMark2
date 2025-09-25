#!/usr/bin/env python3
"""
Photo Watermark 2 启动脚本

简化的启动方式，便于本地测试
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """启动应用程序"""
    try:
        print("正在启动 Photo Watermark 2...")
        print("项目路径:", project_root)

        from photo_watermark.main import main as app_main
        app_main()

    except ImportError as e:
        print(f"导入错误: {e}")
        print("请确保安装了所需依赖: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()