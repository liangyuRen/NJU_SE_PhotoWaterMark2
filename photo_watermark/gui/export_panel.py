"""
导出设置面板模块

提供文件命名规则和JPEG质量设置界面
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable


class ExportSettingsPanel:
    """导出设置面板类"""

    def __init__(self, parent: tk.Widget, on_settings_changed: Callable[[], None]):
        """
        初始化导出设置面板

        Args:
            parent: 父组件
            on_settings_changed: 设置改变回调函数
        """
        self.parent = parent
        self.on_settings_changed = on_settings_changed

        # 设置变量
        self.keep_original_name = tk.BooleanVar(value=True)
        self.add_prefix = tk.BooleanVar(value=False)
        self.prefix_text = tk.StringVar(value="wm_")
        self.add_suffix = tk.BooleanVar(value=True)
        self.suffix_text = tk.StringVar(value="_watermarked")
        self.jpeg_quality = tk.IntVar(value=95)
        self.output_format = tk.StringVar(value="保持原格式")

        self.create_widgets()
        self.setup_layout()
        self.bind_events()

    def create_widgets(self):
        """创建组件"""
        # 主框架
        self.main_frame = ttk.LabelFrame(self.parent, text="导出设置")

        # 文件命名规则框架
        self.naming_frame = ttk.LabelFrame(self.main_frame, text="文件命名规则")

        # 保留原文件名选项
        self.keep_name_cb = ttk.Checkbutton(
            self.naming_frame,
            text="保留原文件名",
            variable=self.keep_original_name,
            command=self.on_settings_changed
        )

        # 添加前缀选项
        self.prefix_cb = ttk.Checkbutton(
            self.naming_frame,
            text="添加前缀:",
            variable=self.add_prefix,
            command=self.on_settings_changed
        )
        self.prefix_entry = ttk.Entry(
            self.naming_frame,
            textvariable=self.prefix_text,
            width=10
        )

        # 添加后缀选项
        self.suffix_cb = ttk.Checkbutton(
            self.naming_frame,
            text="添加后缀:",
            variable=self.add_suffix,
            command=self.on_settings_changed
        )
        self.suffix_entry = ttk.Entry(
            self.naming_frame,
            textvariable=self.suffix_text,
            width=15
        )

        # 输出格式框架
        self.format_frame = ttk.LabelFrame(self.main_frame, text="输出格式")

        # 格式选择
        ttk.Label(self.format_frame, text="输出格式:").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.format_combo = ttk.Combobox(
            self.format_frame,
            textvariable=self.output_format,
            values=["保持原格式", "PNG", "JPEG", "BMP", "TIFF"],
            state="readonly",
            width=15
        )

        # JPEG质量设置框架
        self.quality_frame = ttk.LabelFrame(self.main_frame, text="JPEG质量设置")

        ttk.Label(self.quality_frame, text="质量:").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.quality_scale = ttk.Scale(
            self.quality_frame,
            from_=1, to=100,
            variable=self.jpeg_quality,
            orient=tk.HORIZONTAL,
            command=self.on_quality_changed
        )
        self.quality_label = ttk.Label(self.quality_frame, text=f"{self.jpeg_quality.get()}%")

    def setup_layout(self):
        """设置布局"""
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 命名规则布局
        self.naming_frame.pack(fill=tk.X, pady=(0, 5))
        self.keep_name_cb.grid(row=0, column=0, columnspan=3, sticky='w', padx=5, pady=2)

        self.prefix_cb.grid(row=1, column=0, sticky='w', padx=5, pady=2)
        self.prefix_entry.grid(row=1, column=1, sticky='w', padx=(0, 5), pady=2)

        self.suffix_cb.grid(row=2, column=0, sticky='w', padx=5, pady=2)
        self.suffix_entry.grid(row=2, column=1, sticky='w', padx=(0, 5), pady=2)

        # 输出格式布局
        self.format_frame.pack(fill=tk.X, pady=(0, 5))
        self.format_combo.grid(row=0, column=1, sticky='w', padx=5, pady=2)

        # JPEG质量布局
        self.quality_frame.pack(fill=tk.X)
        self.quality_scale.grid(row=0, column=1, sticky='ew', padx=5, pady=2)
        self.quality_label.grid(row=0, column=2, padx=5, pady=2)

        # 配置网格权重
        self.quality_frame.grid_columnconfigure(1, weight=1)

    def bind_events(self):
        """绑定事件"""
        # 文本改变事件
        self.prefix_text.trace('w', self.on_settings_changed_trace)
        self.suffix_text.trace('w', self.on_settings_changed_trace)

        # 格式改变事件
        self.format_combo.bind('<<ComboboxSelected>>', self.on_settings_changed_trace)

    def on_quality_changed(self, value=None):
        """质量改变事件处理"""
        self.quality_label.config(text=f"{self.jpeg_quality.get()}%")
        self.on_settings_changed()

    def on_settings_changed_trace(self, *args):
        """设置改变trace回调"""
        self.on_settings_changed()

    def get_export_settings(self) -> dict:
        """获取当前导出设置"""
        return {
            'naming': {
                'keep_original_name': self.keep_original_name.get(),
                'add_prefix': self.add_prefix.get(),
                'prefix': self.prefix_text.get(),
                'add_suffix': self.add_suffix.get(),
                'suffix': self.suffix_text.get()
            },
            'format': {
                'output_format': self.output_format.get(),
                'jpeg_quality': self.jpeg_quality.get()
            }
        }

    def generate_filename(self, original_path: str, target_format: str = None) -> str:
        """
        根据设置生成新文件名

        Args:
            original_path: 原始文件路径
            target_format: 目标格式（如果指定）

        Returns:
            str: 生成的文件名
        """
        import os

        # 获取原始文件名和扩展名
        dir_path = os.path.dirname(original_path)
        filename = os.path.basename(original_path)
        name, ext = os.path.splitext(filename)

        # 构建新文件名
        new_name = ""

        # 添加前缀
        if self.add_prefix.get():
            new_name += self.prefix_text.get()

        # 添加原文件名
        if self.keep_original_name.get():
            new_name += name

        # 添加后缀
        if self.add_suffix.get():
            new_name += self.suffix_text.get()

        # 确定输出格式
        if target_format:
            new_ext = target_format
        elif self.output_format.get() != "保持原格式":
            format_map = {
                "PNG": ".png",
                "JPEG": ".jpg",
                "BMP": ".bmp",
                "TIFF": ".tiff"
            }
            new_ext = format_map.get(self.output_format.get(), ext)
        else:
            new_ext = ext

        return new_name + new_ext