"""
主窗口界面模块

应用程序的主界面，整合所有功能面板
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import glob
from typing import List, Optional

from photo_watermark.core.image_processor import ImageProcessor
from photo_watermark.core.batch_processor import BatchProcessor
from photo_watermark.core.watermark import (
    TextWatermark, ImageWatermark, WatermarkLayout,
    WatermarkPosition, WatermarkType
)
from photo_watermark.utils.app_config import AppConfig

from .image_panel import ImagePanel
from .watermark_panel import WatermarkPanel
from .control_panel import ControlPanel


class MainWindow:
    """主窗口类"""

    def __init__(self, config: AppConfig):
        """
        初始化主窗口

        Args:
            config: 应用配置对象
        """
        self.config = config
        self.root = tk.Tk()
        self.setup_window()

        # 初始化处理器
        self.image_processor = ImageProcessor()
        self.batch_processor = BatchProcessor()

        # 当前加载的图片列表
        self.image_list: List[str] = []
        self.current_image_index = -1

        # 水印配置
        self.text_watermark = TextWatermark()
        self.image_watermark = ImageWatermark()
        self.watermark_layout = WatermarkLayout()
        self.current_watermark_type = WatermarkType.TEXT

        # 创建界面
        self.create_widgets()
        self.setup_layout()
        self.bind_events()

        # 加载配置
        self.load_settings()

    def setup_window(self):
        """设置窗口属性"""
        self.root.title("Photo Watermark 2 - 图片水印处理工具")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)

        # 设置窗口图标（如果有的话）
        # self.root.iconbitmap("icon.ico")

        # 设置关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        """创建界面组件"""
        # 创建主框架
        self.main_frame = ttk.Frame(self.root)

        # 创建菜单栏
        self.create_menubar()

        # 创建左侧面板（图片列表和预览）
        self.left_panel = ttk.Frame(self.main_frame)
        self.image_panel = ImagePanel(self.left_panel, self.on_image_selected)

        # 创建右侧面板（水印设置）
        self.right_panel = ttk.Frame(self.main_frame)
        self.watermark_panel = WatermarkPanel(
            self.right_panel,
            self.on_watermark_changed
        )

        # 创建底部控制面板
        self.bottom_panel = ttk.Frame(self.main_frame)
        self.control_panel = ControlPanel(
            self.bottom_panel,
            self.on_import_images,
            self.on_export_current,
            self.on_batch_export
        )

        # 创建状态栏
        self.status_bar = ttk.Label(
            self.main_frame,
            text="就绪",
            relief=tk.SUNKEN,
            anchor=tk.W
        )

    def create_menubar(self):
        """创建菜单栏"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="导入图片...", command=self.on_import_images)
        file_menu.add_command(label="导入文件夹...", command=self.on_import_folder)
        file_menu.add_separator()
        file_menu.add_command(label="导出当前图片...", command=self.on_export_current)
        file_menu.add_command(label="批量导出...", command=self.on_batch_export)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.on_closing)

        # 水印菜单
        watermark_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="水印", menu=watermark_menu)
        watermark_menu.add_command(label="保存模板...", command=self.on_save_template)
        watermark_menu.add_command(label="加载模板...", command=self.on_load_template)
        watermark_menu.add_command(label="管理模板...", command=self.on_manage_templates)

        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="帮助", menu=help_menu)
        help_menu.add_command(label="关于...", command=self.on_about)

    def setup_layout(self):
        """设置布局"""
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 左右面板水平分布
        self.left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))

        # 底部面板和状态栏
        self.bottom_panel.pack(side=tk.BOTTOM, fill=tk.X, pady=(5, 0))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, pady=(2, 0))

        # 设置面板尺寸
        self.right_panel.configure(width=300)

    def bind_events(self):
        """绑定事件"""
        # 拖拽支持 - 暂时注释掉，因为需要额外的拖拽库
        # self.root.drop_target_register(tk.DND_FILES)
        # self.root.dnd_bind('<<Drop>>', self.on_drop_files)
        pass

    def load_settings(self):
        """加载应用设置"""
        try:
            settings = self.config.load_settings()
            # 应用设置到界面
            # TODO: 实现设置加载逻辑
        except Exception as e:
            print(f"加载设置失败: {e}")

    def save_settings(self):
        """保存应用设置"""
        try:
            settings = {
                'window_geometry': self.root.geometry(),
                'last_watermark_config': self.get_current_watermark_config(),
                # 其他设置...
            }
            self.config.save_settings(settings)
        except Exception as e:
            print(f"保存设置失败: {e}")

    def update_status(self, message: str):
        """更新状态栏"""
        self.status_bar.config(text=message)
        self.root.update_idletasks()

    def get_current_watermark_config(self) -> dict:
        """获取当前水印配置"""
        return {
            'type': self.current_watermark_type.value if hasattr(self.current_watermark_type, 'value') else str(self.current_watermark_type),
            'text_config': self.text_watermark.__dict__,
            'image_config': self.image_watermark.__dict__,
            'layout': {k: (v.value if hasattr(v, 'value') else v) for k, v in self.watermark_layout.__dict__.items()}
        }

    # 事件处理方法
    def on_image_selected(self, image_path: str, index: int):
        """图片选择事件处理"""
        self.current_image_index = index
        if self.image_processor.load_image(image_path):
            self.update_preview()
            self.update_status(f"已加载图片: {os.path.basename(image_path)}")

    def on_watermark_changed(self):
        """水印设置改变事件处理"""
        if self.current_image_index >= 0:
            self.update_preview()

    def on_import_images(self):
        """导入图片事件处理"""
        filetypes = [
            ("图片文件", "*.jpg *.jpeg *.png *.bmp *.tiff"),
            ("JPEG文件", "*.jpg *.jpeg"),
            ("PNG文件", "*.png"),
            ("所有文件", "*.*")
        ]

        files = filedialog.askopenfilenames(
            title="选择图片文件",
            filetypes=filetypes
        )

        if files:
            self.add_images(files)

    def on_import_folder(self):
        """导入文件夹事件处理"""
        folder = filedialog.askdirectory(title="选择图片文件夹")
        if folder:
            image_files = []
            for ext in ImageProcessor.SUPPORTED_FORMATS['input']:
                pattern = os.path.join(folder, f"*{ext}")
                image_files.extend(glob.glob(pattern, recursive=True))

            if image_files:
                self.add_images(image_files)
            else:
                messagebox.showinfo("提示", "所选文件夹中未找到支持的图片文件")

    def on_export_current(self):
        """导出当前图片事件处理"""
        if self.current_image_index < 0:
            messagebox.showwarning("警告", "请先选择要导出的图片")
            return

        filetypes = [
            ("PNG文件", "*.png"),
            ("JPEG文件", "*.jpg"),
            ("所有文件", "*.*")
        ]

        file_path = filedialog.asksaveasfilename(
            title="保存图片",
            filetypes=filetypes,
            defaultextension=".png"
        )

        if file_path:
            self.export_single_image(file_path)

    def on_batch_export(self):
        """批量导出事件处理"""
        if not self.image_list:
            messagebox.showwarning("警告", "请先导入要处理的图片")
            return

        folder = filedialog.askdirectory(title="选择输出文件夹")
        if folder:
            self.batch_export_images(folder)

    def on_drop_files(self, event):
        """拖拽文件事件处理"""
        # 暂时禁用拖拽功能
        pass

    def on_save_template(self):
        """保存模板事件处理"""
        # TODO: 实现模板保存对话框
        pass

    def on_load_template(self):
        """加载模板事件处理"""
        # TODO: 实现模板加载对话框
        pass

    def on_manage_templates(self):
        """管理模板事件处理"""
        # TODO: 实现模板管理对话框
        pass

    def on_about(self):
        """关于对话框"""
        messagebox.showinfo(
            "关于",
            "Photo Watermark 2\n"
            "版本: 1.0.0\n"
            "南京大学软件工程课程作业"
        )

    def on_closing(self):
        """窗口关闭事件处理"""
        self.save_settings()
        self.root.quit()

    # 辅助方法
    def add_images(self, image_paths: List[str]):
        """添加图片到列表"""
        valid_images = [path for path in image_paths if self.is_supported_image(path)]
        self.image_list.extend(valid_images)
        self.image_panel.update_image_list(self.image_list)

        if valid_images and self.current_image_index < 0:
            self.on_image_selected(valid_images[0], 0)

    def is_supported_image(self, file_path: str) -> bool:
        """检查文件是否为支持的图片格式"""
        ext = os.path.splitext(file_path)[1].lower()
        return ext in ImageProcessor.SUPPORTED_FORMATS['input']

    def update_preview(self):
        """更新预览"""
        if self.current_image_index >= 0 and self.image_processor.current_image:
            # 重置图片
            self.image_processor.reset_image()

            # 应用水印
            self.apply_current_watermark()

            # 更新预览显示
            self.image_panel.update_preview(self.image_processor.get_current_image())

    def apply_current_watermark(self):
        """应用当前水印设置到图片"""
        if not self.image_processor.current_image:
            return

        try:
            # 获取水印配置
            watermark_config = self.watermark_panel.get_watermark_config()
            watermark_type = watermark_config.get('type', WatermarkType.TEXT)

            if watermark_type == WatermarkType.TEXT:
                self.apply_text_watermark(watermark_config)
            elif watermark_type == WatermarkType.IMAGE:
                self.apply_image_watermark(watermark_config)

        except Exception as e:
            print(f"应用水印失败: {e}")

    def apply_text_watermark(self, config: dict):
        """应用文本水印"""
        text_config = config.get('text_config', {})
        layout_config = config.get('layout', {})

        # 获取文本内容
        text = text_config.get('text', 'Sample Watermark')
        if not text:
            return

        # 计算水印位置
        from photo_watermark.core.watermark import WatermarkCalculator, WatermarkPosition
        image_size = self.image_processor.get_image_size()
        if not image_size:
            return

        # 估算文本尺寸
        font_size = text_config.get('font_size', 36)
        text_size = WatermarkCalculator.get_text_size(text, font_size)

        # 创建布局对象
        layout = WatermarkLayout()
        layout.position = WatermarkPosition(layout_config.get('position', 'bottom_right'))
        layout.x_offset = layout_config.get('x_offset', 50)
        layout.y_offset = layout_config.get('y_offset', 50)
        layout.margin = layout_config.get('margin', 20)

        # 计算位置
        position = WatermarkCalculator.calculate_position(image_size, text_size, layout)

        # 应用文本水印
        self.image_processor.add_text_watermark(
            text=text,
            position=position,
            font_size=font_size,
            color=text_config.get('color', (255, 255, 255)),
            opacity=text_config.get('opacity', 128),
            rotation=layout_config.get('rotation', 0.0)
        )

    def apply_image_watermark(self, config: dict):
        """应用图片水印"""
        image_config = config.get('image_config', {})
        layout_config = config.get('layout', {})

        watermark_path = image_config.get('image_path', '')
        if not watermark_path or not os.path.exists(watermark_path):
            return

        # 获取水印尺寸
        width = image_config.get('width')
        height = image_config.get('height')
        size = (width, height) if width and height else None

        # 计算位置
        from photo_watermark.core.watermark import WatermarkCalculator, WatermarkPosition
        image_size = self.image_processor.get_image_size()
        if not image_size:
            return

        # 获取水印图片实际尺寸
        try:
            from PIL import Image
            with Image.open(watermark_path) as wm_img:
                wm_size = size if size else wm_img.size
        except:
            return

        # 创建布局对象
        layout = WatermarkLayout()
        layout.position = WatermarkPosition(layout_config.get('position', 'bottom_right'))
        layout.x_offset = layout_config.get('x_offset', 50)
        layout.y_offset = layout_config.get('y_offset', 50)
        layout.margin = layout_config.get('margin', 20)

        position = WatermarkCalculator.calculate_position(image_size, wm_size, layout)

        # 应用图片水印
        self.image_processor.add_image_watermark(
            watermark_path=watermark_path,
            position=position,
            size=size,
            opacity=image_config.get('opacity', 128)
        )

    def export_single_image(self, output_path: str):
        """导出单张图片"""
        if self.image_processor.save_image(output_path):
            self.update_status(f"图片已保存: {os.path.basename(output_path)}")
            messagebox.showinfo("成功", "图片导出成功！")
        else:
            messagebox.showerror("错误", "图片导出失败！")

    def batch_export_images(self, output_dir: str):
        """批量导出图片"""
        if not self.image_list:
            messagebox.showwarning("警告", "没有图片需要导出")
            return

        # 获取当前水印配置
        watermark_config = self.get_current_watermark_config()

        # 获取命名规则
        naming_rule = {
            'format': '.png',  # 默认输出PNG格式
            'add_prefix': False,
            'prefix': 'wm_',
            'add_suffix': True,
            'suffix': '_watermarked'
        }

        # 简单的批量处理
        success_count = 0
        total_count = len(self.image_list)

        for i, image_path in enumerate(self.image_list):
            try:
                # 更新状态
                filename = os.path.basename(image_path)
                self.update_status(f"正在处理 {filename} ({i+1}/{total_count})")
                self.root.update()

                # 处理单张图片
                processor = ImageProcessor()
                if processor.load_image(image_path):
                    # 应用水印
                    if watermark_config['type'] == 'text':
                        self.apply_text_watermark_to_processor(processor, watermark_config)

                    # 生成输出文件名
                    input_file = Path(image_path)
                    output_filename = input_file.stem + naming_rule['suffix'] + naming_rule['format']
                    output_path = os.path.join(output_dir, output_filename)

                    # 保存图片
                    if processor.save_image(output_path):
                        success_count += 1

            except Exception as e:
                print(f"处理图片 {image_path} 失败: {e}")

        # 完成
        self.update_status("批量处理完成")
        messagebox.showinfo("完成", f"批量处理完成！\n成功: {success_count}/{total_count}")

    def apply_text_watermark_to_processor(self, processor: ImageProcessor, config: dict):
        """为指定的处理器应用文本水印"""
        text_config = config.get('text_config', {})
        layout_config = config.get('layout', {})

        text = text_config.get('text', 'Sample Watermark')
        if not text:
            return

        # 计算位置
        from photo_watermark.core.watermark import WatermarkCalculator, WatermarkPosition
        image_size = processor.get_image_size()
        if not image_size:
            return

        font_size = text_config.get('font_size', 36)
        text_size = WatermarkCalculator.get_text_size(text, font_size)

        layout = WatermarkLayout()
        layout.position = WatermarkPosition(layout_config.get('position', 'bottom_right'))
        layout.x_offset = layout_config.get('x_offset', 50)
        layout.y_offset = layout_config.get('y_offset', 50)
        layout.margin = layout_config.get('margin', 20)

        position = WatermarkCalculator.calculate_position(image_size, text_size, layout)

        processor.add_text_watermark(
            text=text,
            position=position,
            font_size=font_size,
            color=text_config.get('color', (255, 255, 255)),
            opacity=text_config.get('opacity', 128),
            rotation=layout_config.get('rotation', 0.0)
        )

    def run(self):
        """启动应用程序"""
        self.root.mainloop()