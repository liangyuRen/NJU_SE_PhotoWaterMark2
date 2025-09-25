"""
Photo Watermark 2 主程序入口

启动应用程序的主入口点
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from photo_watermark.gui.main_window import MainWindow
from photo_watermark.utils.app_config import AppConfig

def main():
    """应用程序主入口"""
    try:
        # 初始化应用配置
        config = AppConfig()

        # 创建并启动主窗口
        app = MainWindow(config)
        app.run()

    except Exception as e:
        print(f"应用程序启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()