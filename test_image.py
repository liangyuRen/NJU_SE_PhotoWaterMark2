#!/usr/bin/env python3
"""
创建测试图片

生成一些测试用的图片文件，用于验证水印功能
"""

from PIL import Image, ImageDraw, ImageFont
import os


def create_test_images():
    """创建测试图片"""
    # 确保test_images目录存在
    test_dir = "test_images"
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)

    # 创建几张不同尺寸和颜色的测试图片
    test_configs = [
        {"name": "test_landscape.jpg", "size": (800, 600), "color": (70, 130, 180)},
        {"name": "test_portrait.jpg", "size": (600, 800), "color": (255, 182, 193)},
        {"name": "test_square.png", "size": (500, 500), "color": (144, 238, 144)},
        {"name": "test_small.png", "size": (300, 200), "color": (255, 218, 185)},
    ]

    for config in test_configs:
        # 创建图片
        img = Image.new('RGB', config["size"], config["color"])
        draw = ImageDraw.Draw(img)

        # 添加一些图案
        width, height = config["size"]

        # 绘制一些线条
        for i in range(0, width, 50):
            draw.line([(i, 0), (i, height)], fill=(255, 255, 255), width=1)
        for i in range(0, height, 50):
            draw.line([(0, i), (width, i)], fill=(255, 255, 255), width=1)

        # 添加文本
        try:
            # 尝试使用默认字体
            font = ImageFont.load_default()
        except:
            font = None

        text = f"Test Image\n{width}x{height}"
        text_x = width // 2 - 50
        text_y = height // 2 - 20

        draw.text((text_x, text_y), text, fill=(0, 0, 0), font=font)

        # 保存图片
        file_path = os.path.join(test_dir, config["name"])

        if config["name"].endswith('.jpg'):
            img.save(file_path, 'JPEG', quality=90)
        else:
            img.save(file_path, 'PNG')

        print(f"创建测试图片: {file_path}")

    print(f"\n测试图片已保存到 {test_dir} 目录")
    print("现在可以在 Photo Watermark 2 中导入这些图片进行测试！")


if __name__ == "__main__":
    create_test_images()