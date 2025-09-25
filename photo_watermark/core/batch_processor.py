"""
批量处理模块

处理多张图片的批量水印添加和导出功能
"""

import os
from pathlib import Path
from typing import List, Dict, Callable, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

from .image_processor import ImageProcessor
from .watermark import TextWatermark, ImageWatermark, WatermarkLayout, WatermarkType


class BatchProcessor:
    """批量处理器"""

    def __init__(self, max_workers: int = 4):
        """
        初始化批量处理器

        Args:
            max_workers: 最大工作线程数
        """
        self.max_workers = max_workers
        self.is_processing = False
        self.cancel_flag = threading.Event()

    def process_images(
        self,
        image_paths: List[str],
        output_dir: str,
        watermark_config: Dict,
        layout: WatermarkLayout,
        naming_rule: Dict,
        progress_callback: Optional[Callable[[int, int, str], None]] = None
    ) -> Dict[str, bool]:
        """
        批量处理图片

        Args:
            image_paths: 图片路径列表
            output_dir: 输出目录
            watermark_config: 水印配置
            layout: 布局配置
            naming_rule: 命名规则配置
            progress_callback: 进度回调函数 (current, total, current_file)

        Returns:
            Dict[str, bool]: 处理结果，文件路径->是否成功
        """
        self.is_processing = True
        self.cancel_flag.clear()
        results = {}

        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)

        total_images = len(image_paths)
        completed = 0

        try:
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                # 提交所有任务
                future_to_path = {
                    executor.submit(
                        self._process_single_image,
                        image_path,
                        output_dir,
                        watermark_config,
                        layout,
                        naming_rule
                    ): image_path
                    for image_path in image_paths
                }

                # 处理完成的任务
                for future in as_completed(future_to_path):
                    if self.cancel_flag.is_set():
                        break

                    image_path = future_to_path[future]
                    completed += 1

                    try:
                        success = future.result()
                        results[image_path] = success
                    except Exception as e:
                        print(f"处理图片失败 {image_path}: {e}")
                        results[image_path] = False

                    # 调用进度回调
                    if progress_callback:
                        progress_callback(completed, total_images, os.path.basename(image_path))

        except Exception as e:
            print(f"批量处理出错: {e}")

        finally:
            self.is_processing = False

        return results

    def _process_single_image(
        self,
        image_path: str,
        output_dir: str,
        watermark_config: Dict,
        layout: WatermarkLayout,
        naming_rule: Dict
    ) -> bool:
        """
        处理单张图片

        Args:
            image_path: 图片路径
            output_dir: 输出目录
            watermark_config: 水印配置
            layout: 布局配置
            naming_rule: 命名规则

        Returns:
            bool: 处理是否成功
        """
        if self.cancel_flag.is_set():
            return False

        try:
            # 创建图像处理器
            processor = ImageProcessor()

            # 加载图片
            if not processor.load_image(image_path):
                return False

            # 添加水印
            success = self._add_watermark(processor, watermark_config, layout)
            if not success:
                return False

            # 生成输出文件名
            output_path = self._generate_output_path(
                image_path, output_dir, naming_rule
            )

            # 保存图片
            quality = watermark_config.get('quality', 95)
            return processor.save_image(output_path, quality)

        except Exception as e:
            print(f"处理单张图片失败 {image_path}: {e}")
            return False

    def _add_watermark(
        self,
        processor: ImageProcessor,
        watermark_config: Dict,
        layout: WatermarkLayout
    ) -> bool:
        """
        添加水印到图片

        Args:
            processor: 图像处理器
            watermark_config: 水印配置
            layout: 布局配置

        Returns:
            bool: 添加是否成功
        """
        watermark_type = watermark_config.get('type', WatermarkType.TEXT)

        if watermark_type == WatermarkType.TEXT:
            return self._add_text_watermark(processor, watermark_config, layout)
        elif watermark_type == WatermarkType.IMAGE:
            return self._add_image_watermark(processor, watermark_config, layout)

        return False

    def _add_text_watermark(
        self,
        processor: ImageProcessor,
        watermark_config: Dict,
        layout: WatermarkLayout
    ) -> bool:
        """添加文本水印"""
        text_config = watermark_config.get('text_config', {})

        # 计算位置
        from .watermark import WatermarkCalculator
        image_size = processor.get_image_size()
        text_size = WatermarkCalculator.get_text_size(
            text_config.get('text', 'Watermark'),
            text_config.get('font_size', 36)
        )
        position = WatermarkCalculator.calculate_position(image_size, text_size, layout)

        return processor.add_text_watermark(
            text=text_config.get('text', 'Watermark'),
            position=position,
            font_size=text_config.get('font_size', 36),
            color=text_config.get('color', (255, 255, 255)),
            opacity=text_config.get('opacity', 128)
        )

    def _add_image_watermark(
        self,
        processor: ImageProcessor,
        watermark_config: Dict,
        layout: WatermarkLayout
    ) -> bool:
        """添加图片水印"""
        image_config = watermark_config.get('image_config', {})
        watermark_path = image_config.get('image_path', '')

        if not watermark_path or not os.path.exists(watermark_path):
            return False

        # 计算位置和大小
        from .watermark import WatermarkCalculator
        image_size = processor.get_image_size()

        # 获取水印图片尺寸
        from PIL import Image
        with Image.open(watermark_path) as wm_img:
            wm_size = wm_img.size

        # 如果指定了新尺寸，使用新尺寸
        target_size = image_config.get('size')
        if target_size:
            wm_size = target_size

        position = WatermarkCalculator.calculate_position(image_size, wm_size, layout)

        return processor.add_image_watermark(
            watermark_path=watermark_path,
            position=position,
            size=target_size,
            opacity=image_config.get('opacity', 128)
        )

    def _generate_output_path(
        self,
        input_path: str,
        output_dir: str,
        naming_rule: Dict
    ) -> str:
        """
        根据命名规则生成输出文件路径

        Args:
            input_path: 输入文件路径
            output_dir: 输出目录
            naming_rule: 命名规则

        Returns:
            str: 输出文件路径
        """
        input_file = Path(input_path)
        name_stem = input_file.stem
        extension = naming_rule.get('format', input_file.suffix)

        # 应用命名规则
        if naming_rule.get('add_prefix'):
            name_stem = naming_rule['prefix'] + name_stem

        if naming_rule.get('add_suffix'):
            name_stem = name_stem + naming_rule['suffix']

        output_filename = name_stem + extension
        return os.path.join(output_dir, output_filename)

    def cancel_processing(self):
        """取消当前的批量处理"""
        self.cancel_flag.set()

    def is_busy(self) -> bool:
        """检查是否正在处理"""
        return self.is_processing