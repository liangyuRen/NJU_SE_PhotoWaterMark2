"""
控制面板模块

提供导入、导出和其他操作按钮
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable


class ControlPanel:
    """控制面板类"""

    def __init__(
        self,
        parent: tk.Widget,
        on_import_images: Callable[[], None],
        on_export_current: Callable[[], None],
        on_batch_export: Callable[[], None],
        on_clear_list: Callable[[], None],
        on_reset_watermark: Callable[[], None]
    ):
        """
        初始化控制面板

        Args:
            parent: 父组件
            on_import_images: 导入图片回调
            on_export_current: 导出当前图片回调
            on_batch_export: 批量导出回调
            on_clear_list: 清空列表回调
            on_reset_watermark: 重置水印回调
        """
        self.parent = parent
        self.on_import_images = on_import_images
        self.on_export_current = on_export_current
        self.on_batch_export = on_batch_export
        self.on_clear_list_callback = on_clear_list
        self.on_reset_watermark_callback = on_reset_watermark

        self.create_widgets()
        self.setup_layout()

    def create_widgets(self):
        """创建组件"""
        # 主框架
        self.main_frame = ttk.Frame(self.parent)

        # 导入按钮
        self.import_button = ttk.Button(
            self.main_frame,
            text="导入图片",
            command=self.on_import_images
        )

        # 导出当前图片按钮
        self.export_button = ttk.Button(
            self.main_frame,
            text="导出当前",
            command=self.on_export_current
        )

        # 批量导出按钮
        self.batch_export_button = ttk.Button(
            self.main_frame,
            text="批量导出",
            command=self.on_batch_export
        )

        # 清空列表按钮
        self.clear_button = ttk.Button(
            self.main_frame,
            text="清空列表",
            command=self.on_clear_list_callback
        )

        # 分隔符
        self.separator = ttk.Separator(self.main_frame, orient=tk.VERTICAL)

        # 重置按钮
        self.reset_button = ttk.Button(
            self.main_frame,
            text="重置水印",
            command=self.on_reset_watermark_callback
        )

    def setup_layout(self):
        """设置布局"""
        self.main_frame.pack(fill=tk.X, padx=5, pady=5)

        # 水平排列按钮
        self.import_button.pack(side=tk.LEFT, padx=(0, 5))
        self.export_button.pack(side=tk.LEFT, padx=(0, 5))
        self.batch_export_button.pack(side=tk.LEFT, padx=(0, 10))

        self.separator.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        self.clear_button.pack(side=tk.LEFT, padx=(0, 5))
        self.reset_button.pack(side=tk.LEFT)


    def set_button_state(self, button_name: str, enabled: bool):
        """
        设置按钮启用状态

        Args:
            button_name: 按钮名称
            enabled: 是否启用
        """
        button_map = {
            'import': self.import_button,
            'export': self.export_button,
            'batch_export': self.batch_export_button,
            'clear': self.clear_button,
            'reset': self.reset_button
        }

        if button_name in button_map:
            button = button_map[button_name]
            if enabled:
                button.state(['!disabled'])
            else:
                button.state(['disabled'])