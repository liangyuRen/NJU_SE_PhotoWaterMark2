"""
图像处理核心模块

负责图片的加载、处理、水印添加等核心功能
"""

from PIL import Image, ImageDraw, ImageFont
from typing import List, Tuple, Optional
import os


class ImageProcessor:
    """图像处理器类"""

    SUPPORTED_FORMATS = {
        'input': ['.jpg', '.jpeg', '.png', '.bmp', '.tiff'],
        'output': ['.jpg', '.jpeg', '.png']
    }

    def __init__(self):
        """初始化图像处理器"""
        self.current_image = None
        self.original_image = None

    def load_image(self, image_path: str) -> bool:
        """
        加载图片文件

        Args:
            image_path: 图片文件路径

        Returns:
            bool: 加载成功返回True，失败返回False
        """
        try:
            self.original_image = Image.open(image_path)
            self.current_image = self.original_image.copy()
            return True
        except Exception as e:
            print(f"加载图片失败: {e}")
            return False

    def add_text_watermark(
        self,
        text: str,
        position: Tuple[int, int],
        font_path: Optional[str] = None,
        font_size: int = 36,
        color: Tuple[int, int, int] = (255, 255, 255),
        opacity: int = 128
    ) -> bool:
        """
        添加文本水印

        Args:
            text: 水印文本
            position: 水印位置 (x, y)
            font_path: 字体文件路径
            font_size: 字体大小
            color: 文字颜色 RGB
            opacity: 透明度 (0-255)

        Returns:
            bool: 添加成功返回True
        """
        if not self.current_image:
            return False

        try:
            # 创建透明图层
            watermark = Image.new('RGBA', self.current_image.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(watermark)

            # 设置字体
            try:
                if font_path and os.path.exists(font_path):
                    font = ImageFont.truetype(font_path, font_size)
                else:
                    font = ImageFont.load_default()
            except:
                font = ImageFont.load_default()

            # 绘制文本
            text_color = (*color, opacity)
            draw.text(position, text, font=font, fill=text_color)

            # 合并图层
            if self.current_image.mode != 'RGBA':
                self.current_image = self.current_image.convert('RGBA')

            self.current_image = Image.alpha_composite(self.current_image, watermark)
            return True

        except Exception as e:
            print(f"添加文本水印失败: {e}")
            return False

    def add_image_watermark(
        self,
        watermark_path: str,
        position: Tuple[int, int],
        size: Optional[Tuple[int, int]] = None,
        opacity: int = 128
    ) -> bool:
        """
        添加图片水印

        Args:
            watermark_path: 水印图片路径
            position: 水印位置 (x, y)
            size: 水印大小 (width, height)，None表示保持原大小
            opacity: 透明度 (0-255)

        Returns:
            bool: 添加成功返回True
        """
        if not self.current_image:
            return False

        try:
            # 加载水印图片
            watermark_img = Image.open(watermark_path)

            # 调整大小
            if size:
                watermark_img = watermark_img.resize(size, Image.Resampling.LANCZOS)

            # 确保图片有透明度通道
            if watermark_img.mode != 'RGBA':
                watermark_img = watermark_img.convert('RGBA')

            # 调整透明度
            alpha = watermark_img.getchannel('A')
            alpha = alpha.point(lambda p: int(p * opacity / 255))
            watermark_img.putalpha(alpha)

            # 合并图片
            if self.current_image.mode != 'RGBA':
                self.current_image = self.current_image.convert('RGBA')

            self.current_image.paste(watermark_img, position, watermark_img)
            return True

        except Exception as e:
            print(f"添加图片水印失败: {e}")
            return False

    def save_image(self, output_path: str, quality: int = 95) -> bool:
        """
        保存处理后的图片

        Args:
            output_path: 输出文件路径
            quality: JPEG质量 (1-100)

        Returns:
            bool: 保存成功返回True
        """
        if not self.current_image:
            return False

        try:
            # 根据输出格式转换图片模式
            ext = os.path.splitext(output_path)[1].lower()

            if ext in ['.jpg', '.jpeg']:
                # JPEG不支持透明度，转换为RGB
                if self.current_image.mode == 'RGBA':
                    # 创建白色背景
                    background = Image.new('RGB', self.current_image.size, (255, 255, 255))
                    background.paste(self.current_image, mask=self.current_image.split()[-1])
                    background.save(output_path, 'JPEG', quality=quality)
                else:
                    self.current_image.save(output_path, 'JPEG', quality=quality)
            else:
                # PNG支持透明度
                self.current_image.save(output_path, 'PNG')

            return True

        except Exception as e:
            print(f"保存图片失败: {e}")
            return False

    def reset_image(self):
        """重置图片到原始状态"""
        if self.original_image:
            self.current_image = self.original_image.copy()

    def get_current_image(self) -> Optional[Image.Image]:
        """获取当前处理中的图片"""
        return self.current_image

    def get_image_size(self) -> Optional[Tuple[int, int]]:
        """获取当前图片尺寸"""
        if self.current_image:
            return self.current_image.size
        return None