"""
水印配置和管理模块

定义水印的属性、位置计算等功能
"""

from dataclasses import dataclass
from typing import Tuple, Optional
from enum import Enum


class WatermarkType(Enum):
    """水印类型枚举"""
    TEXT = "text"
    IMAGE = "image"


class WatermarkPosition(Enum):
    """水印预设位置枚举（九宫格）"""
    TOP_LEFT = "top_left"
    TOP_CENTER = "top_center"
    TOP_RIGHT = "top_right"
    MIDDLE_LEFT = "middle_left"
    CENTER = "center"
    MIDDLE_RIGHT = "middle_right"
    BOTTOM_LEFT = "bottom_left"
    BOTTOM_CENTER = "bottom_center"
    BOTTOM_RIGHT = "bottom_right"
    CUSTOM = "custom"


@dataclass
class TextWatermark:
    """文本水印配置类"""
    text: str = "Sample Watermark"
    font_family: str = "Arial"
    font_size: int = 36
    font_bold: bool = False
    font_italic: bool = False
    color: Tuple[int, int, int] = (255, 255, 255)  # RGB
    opacity: int = 128  # 0-255
    shadow: bool = False
    shadow_color: Tuple[int, int, int] = (0, 0, 0)
    stroke: bool = False
    stroke_color: Tuple[int, int, int] = (0, 0, 0)
    stroke_width: int = 1


@dataclass
class ImageWatermark:
    """图片水印配置类"""
    image_path: str = ""
    width: Optional[int] = None
    height: Optional[int] = None
    opacity: int = 128  # 0-255
    keep_aspect_ratio: bool = True


@dataclass
class WatermarkLayout:
    """水印布局配置类"""
    position: WatermarkPosition = WatermarkPosition.BOTTOM_RIGHT
    x_offset: int = 50  # 相对于预设位置的偏移
    y_offset: int = 50
    rotation: float = 0.0  # 旋转角度 0-360
    margin: int = 20  # 距离边缘的边距


class WatermarkCalculator:
    """水印位置计算器"""

    @staticmethod
    def calculate_position(
        image_size: Tuple[int, int],
        watermark_size: Tuple[int, int],
        layout: WatermarkLayout
    ) -> Tuple[int, int]:
        """
        根据布局配置计算水印的实际位置

        Args:
            image_size: 图片尺寸 (width, height)
            watermark_size: 水印尺寸 (width, height)
            layout: 布局配置

        Returns:
            Tuple[int, int]: 水印左上角坐标 (x, y)
        """
        img_width, img_height = image_size
        wm_width, wm_height = watermark_size
        margin = layout.margin

        # 计算九宫格基础位置
        positions = {
            WatermarkPosition.TOP_LEFT: (margin, margin),
            WatermarkPosition.TOP_CENTER: (
                (img_width - wm_width) // 2, margin
            ),
            WatermarkPosition.TOP_RIGHT: (
                img_width - wm_width - margin, margin
            ),
            WatermarkPosition.MIDDLE_LEFT: (
                margin, (img_height - wm_height) // 2
            ),
            WatermarkPosition.CENTER: (
                (img_width - wm_width) // 2,
                (img_height - wm_height) // 2
            ),
            WatermarkPosition.MIDDLE_RIGHT: (
                img_width - wm_width - margin,
                (img_height - wm_height) // 2
            ),
            WatermarkPosition.BOTTOM_LEFT: (
                margin, img_height - wm_height - margin
            ),
            WatermarkPosition.BOTTOM_CENTER: (
                (img_width - wm_width) // 2,
                img_height - wm_height - margin
            ),
            WatermarkPosition.BOTTOM_RIGHT: (
                img_width - wm_width - margin,
                img_height - wm_height - margin
            ),
        }

        # 获取基础位置
        base_x, base_y = positions.get(layout.position, positions[WatermarkPosition.BOTTOM_RIGHT])

        # 应用偏移
        final_x = max(0, min(img_width - wm_width, base_x + layout.x_offset))
        final_y = max(0, min(img_height - wm_height, base_y + layout.y_offset))

        return (final_x, final_y)

    @staticmethod
    def get_text_size(
        text: str,
        font_size: int,
        font_family: str = "Arial"
    ) -> Tuple[int, int]:
        """
        估算文本尺寸

        Args:
            text: 文本内容
            font_size: 字体大小
            font_family: 字体族

        Returns:
            Tuple[int, int]: 估算的文本尺寸 (width, height)
        """
        # 简单估算，实际应用中可能需要更精确的计算
        char_width = font_size * 0.6  # 平均字符宽度
        line_height = font_size * 1.2  # 行高

        lines = text.split('\n')
        max_width = max(len(line) for line in lines) * char_width
        total_height = len(lines) * line_height

        return (int(max_width), int(total_height))