"""
水印设置面板模块

提供文本和图片水印的设置界面
"""

import tkinter as tk
from tkinter import ttk, filedialog, colorchooser
from typing import Callable

from photo_watermark.core.watermark import (
    TextWatermark, ImageWatermark, WatermarkLayout,
    WatermarkPosition, WatermarkType
)


class WatermarkPanel:
    """水印设置面板类"""

    def __init__(self, parent: tk.Widget, on_watermark_changed: Callable[[], None]):
        """
        初始化水印面板

        Args:
            parent: 父组件
            on_watermark_changed: 水印设置改变回调函数
        """
        self.parent = parent
        self.on_watermark_changed = on_watermark_changed

        # 水印配置对象
        self.text_watermark = TextWatermark()
        self.image_watermark = ImageWatermark()
        self.watermark_layout = WatermarkLayout()

        # 界面变量
        self.watermark_type = tk.StringVar(value=WatermarkType.TEXT.value)
        self.text_content = tk.StringVar(value=self.text_watermark.text)
        self.font_size = tk.IntVar(value=self.text_watermark.font_size)
        self.opacity = tk.IntVar(value=self.text_watermark.opacity)
        self.position = tk.StringVar(value=self.watermark_layout.position.value)

        # 预览设置
        self.show_preview = tk.BooleanVar(value=True)
        self.show_position_indicator = tk.BooleanVar(value=True)

        self.create_widgets()
        self.setup_layout()
        self.bind_events()

    def create_widgets(self):
        """创建组件"""
        # 主框架
        self.main_frame = ttk.Frame(self.parent)

        # 水印类型选择
        self.type_frame = ttk.LabelFrame(self.main_frame, text="水印类型")
        self.text_radio = ttk.Radiobutton(
            self.type_frame,
            text="文本水印",
            variable=self.watermark_type,
            value=WatermarkType.TEXT.value,
            command=self.on_type_changed
        )
        self.image_radio = ttk.Radiobutton(
            self.type_frame,
            text="图片水印",
            variable=self.watermark_type,
            value=WatermarkType.IMAGE.value,
            command=self.on_type_changed
        )

        # 文本水印设置框架
        self.text_frame = ttk.LabelFrame(self.main_frame, text="文本水印设置")
        self.create_text_widgets()

        # 图片水印设置框架
        self.image_frame = ttk.LabelFrame(self.main_frame, text="图片水印设置")
        self.create_image_widgets()

        # 位置设置框架
        self.position_frame = ttk.LabelFrame(self.main_frame, text="位置设置")
        self.create_position_widgets()

        # 高级设置框架
        self.advanced_frame = ttk.LabelFrame(self.main_frame, text="高级设置")
        self.create_advanced_widgets()

        # 预览设置框架
        self.preview_frame = ttk.LabelFrame(self.main_frame, text="预览设置")
        self.create_preview_widgets()

    def create_text_widgets(self):
        """创建文本水印设置组件"""
        # 文本内容
        ttk.Label(self.text_frame, text="文本内容:").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.text_entry = ttk.Entry(self.text_frame, textvariable=self.text_content)
        self.text_entry.grid(row=0, column=1, sticky='ew', padx=5, pady=2)

        # 字体大小
        ttk.Label(self.text_frame, text="字体大小:").grid(row=1, column=0, sticky='w', padx=5, pady=2)
        self.font_size_scale = ttk.Scale(
            self.text_frame,
            from_=12, to=72,
            variable=self.font_size,
            orient=tk.HORIZONTAL,
            command=self.on_text_changed
        )
        self.font_size_scale.grid(row=1, column=1, sticky='ew', padx=5, pady=2)
        self.font_size_label = ttk.Label(self.text_frame, text=f"{self.font_size.get()}px")
        self.font_size_label.grid(row=1, column=2, padx=5, pady=2)

        # 文字颜色
        ttk.Label(self.text_frame, text="文字颜色:").grid(row=2, column=0, sticky='w', padx=5, pady=2)
        self.color_button = ttk.Button(
            self.text_frame,
            text="选择颜色",
            command=self.on_choose_color
        )
        self.color_button.grid(row=2, column=1, sticky='w', padx=5, pady=2)

        # 透明度
        ttk.Label(self.text_frame, text="透明度:").grid(row=3, column=0, sticky='w', padx=5, pady=2)
        self.opacity_scale = ttk.Scale(
            self.text_frame,
            from_=0, to=255,
            variable=self.opacity,
            orient=tk.HORIZONTAL,
            command=self.on_text_changed
        )
        self.opacity_scale.grid(row=3, column=1, sticky='ew', padx=5, pady=2)
        self.opacity_label = ttk.Label(self.text_frame, text=f"{self.opacity.get()}")
        self.opacity_label.grid(row=3, column=2, padx=5, pady=2)

        # 字体样式
        self.font_bold = tk.BooleanVar()
        self.font_italic = tk.BooleanVar()

        ttk.Checkbutton(
            self.text_frame,
            text="粗体",
            variable=self.font_bold,
            command=self.on_text_changed
        ).grid(row=4, column=0, sticky='w', padx=5, pady=2)

        ttk.Checkbutton(
            self.text_frame,
            text="斜体",
            variable=self.font_italic,
            command=self.on_text_changed
        ).grid(row=4, column=1, sticky='w', padx=5, pady=2)

        # 配置网格权重
        self.text_frame.grid_columnconfigure(1, weight=1)

    def create_image_widgets(self):
        """创建图片水印设置组件"""
        # 选择图片文件
        ttk.Label(self.image_frame, text="水印图片:").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.image_path_var = tk.StringVar()
        self.image_path_entry = ttk.Entry(
            self.image_frame,
            textvariable=self.image_path_var,
            state='readonly'
        )
        self.image_path_entry.grid(row=0, column=1, sticky='ew', padx=5, pady=2)

        self.browse_button = ttk.Button(
            self.image_frame,
            text="浏览...",
            command=self.on_browse_image
        )
        self.browse_button.grid(row=0, column=2, padx=5, pady=2)

        # 图片尺寸
        ttk.Label(self.image_frame, text="宽度:").grid(row=1, column=0, sticky='w', padx=5, pady=2)
        self.image_width = tk.IntVar(value=100)
        ttk.Entry(
            self.image_frame,
            textvariable=self.image_width,
            width=10
        ).grid(row=1, column=1, sticky='w', padx=5, pady=2)

        ttk.Label(self.image_frame, text="高度:").grid(row=2, column=0, sticky='w', padx=5, pady=2)
        self.image_height = tk.IntVar(value=100)
        ttk.Entry(
            self.image_frame,
            textvariable=self.image_height,
            width=10
        ).grid(row=2, column=1, sticky='w', padx=5, pady=2)

        # 保持纵横比
        self.keep_aspect = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            self.image_frame,
            text="保持纵横比",
            variable=self.keep_aspect,
            command=self.on_image_changed
        ).grid(row=3, column=0, columnspan=2, sticky='w', padx=5, pady=2)

        # 图片透明度
        ttk.Label(self.image_frame, text="透明度:").grid(row=4, column=0, sticky='w', padx=5, pady=2)
        self.image_opacity = tk.IntVar(value=128)
        ttk.Scale(
            self.image_frame,
            from_=0, to=255,
            variable=self.image_opacity,
            orient=tk.HORIZONTAL,
            command=self.on_image_changed
        ).grid(row=4, column=1, sticky='ew', padx=5, pady=2)

        # 配置网格权重
        self.image_frame.grid_columnconfigure(1, weight=1)

    def create_position_widgets(self):
        """创建位置设置组件"""
        # 预设位置（九宫格）
        ttk.Label(self.position_frame, text="预设位置:").grid(row=0, column=0, sticky='w', padx=5, pady=2)

        # 九宫格按钮
        positions = [
            ("↖", WatermarkPosition.TOP_LEFT),
            ("↑", WatermarkPosition.TOP_CENTER),
            ("↗", WatermarkPosition.TOP_RIGHT),
            ("←", WatermarkPosition.MIDDLE_LEFT),
            ("●", WatermarkPosition.CENTER),
            ("→", WatermarkPosition.MIDDLE_RIGHT),
            ("↙", WatermarkPosition.BOTTOM_LEFT),
            ("↓", WatermarkPosition.BOTTOM_CENTER),
            ("↘", WatermarkPosition.BOTTOM_RIGHT),
        ]

        self.position_buttons = {}
        for i, (symbol, pos) in enumerate(positions):
            row = i // 3 + 1
            col = i % 3
            btn = ttk.Button(
                self.position_frame,
                text=symbol,
                width=3,
                command=lambda p=pos: self.set_position(p)
            )
            btn.grid(row=row, column=col, padx=1, pady=1)
            self.position_buttons[pos] = btn

        # 自定义位置
        ttk.Label(self.position_frame, text="X偏移:").grid(row=4, column=0, sticky='w', padx=5, pady=2)
        self.x_offset = tk.IntVar(value=0)
        ttk.Entry(
            self.position_frame,
            textvariable=self.x_offset,
            width=10
        ).grid(row=4, column=1, sticky='w', padx=5, pady=2)

        ttk.Label(self.position_frame, text="Y偏移:").grid(row=5, column=0, sticky='w', padx=5, pady=2)
        self.y_offset = tk.IntVar(value=0)
        ttk.Entry(
            self.position_frame,
            textvariable=self.y_offset,
            width=10
        ).grid(row=5, column=1, sticky='w', padx=5, pady=2)

    def create_advanced_widgets(self):
        """创建高级设置组件"""
        # 旋转角度
        ttk.Label(self.advanced_frame, text="旋转角度:").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.rotation = tk.DoubleVar(value=0.0)
        ttk.Scale(
            self.advanced_frame,
            from_=0, to=360,
            variable=self.rotation,
            orient=tk.HORIZONTAL,
            command=self.on_layout_changed
        ).grid(row=0, column=1, sticky='ew', padx=5, pady=2)

        # 边距
        ttk.Label(self.advanced_frame, text="边距:").grid(row=1, column=0, sticky='w', padx=5, pady=2)
        self.margin = tk.IntVar(value=20)
        ttk.Entry(
            self.advanced_frame,
            textvariable=self.margin,
            width=10
        ).grid(row=1, column=1, sticky='w', padx=5, pady=2)

        # 配置网格权重
        self.advanced_frame.grid_columnconfigure(1, weight=1)

    def create_preview_widgets(self):
        """创建预览设置组件"""
        # 显示水印预览
        ttk.Checkbutton(
            self.preview_frame,
            text="显示水印预览",
            variable=self.show_preview,
            command=self.on_preview_changed
        ).grid(row=0, column=0, sticky='w', padx=5, pady=2)

        # 显示可拖拽水印
        ttk.Checkbutton(
            self.preview_frame,
            text="显示可拖拽水印叠加层",
            variable=self.show_position_indicator,
            command=self.on_preview_changed
        ).grid(row=1, column=0, sticky='w', padx=5, pady=2)

    def setup_layout(self):
        """设置布局"""
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 垂直排列各个框架
        self.type_frame.pack(fill=tk.X, pady=(0, 5))
        self.text_frame.pack(fill=tk.X, pady=(0, 5))
        self.image_frame.pack(fill=tk.X, pady=(0, 5))
        self.position_frame.pack(fill=tk.X, pady=(0, 5))
        self.advanced_frame.pack(fill=tk.X, pady=(0, 5))
        self.preview_frame.pack(fill=tk.X)

        # 类型选择布局
        self.text_radio.pack(anchor='w', padx=5, pady=2)
        self.image_radio.pack(anchor='w', padx=5, pady=2)

        # 初始显示文本水印面板
        self.on_type_changed()

    def bind_events(self):
        """绑定事件"""
        # 文本内容改变事件
        self.text_content.trace('w', self.on_text_changed_trace)

        # 位置和尺寸改变事件
        self.x_offset.trace('w', self.on_layout_changed_trace)
        self.y_offset.trace('w', self.on_layout_changed_trace)
        self.margin.trace('w', self.on_layout_changed_trace)

        # 图片设置改变事件
        self.image_width.trace('w', self.on_image_changed_trace)
        self.image_height.trace('w', self.on_image_changed_trace)
        self.image_opacity.trace('w', self.on_image_changed_trace)

    def on_type_changed(self):
        """水印类型改变事件处理"""
        watermark_type = WatermarkType(self.watermark_type.get())

        if watermark_type == WatermarkType.TEXT:
            self.text_frame.pack(fill=tk.X, pady=(0, 5), before=self.position_frame)
            self.image_frame.pack_forget()
        else:
            self.image_frame.pack(fill=tk.X, pady=(0, 5), before=self.position_frame)
            self.text_frame.pack_forget()

        self.on_watermark_changed()

    def on_text_changed(self, value=None):
        """文本水印设置改变事件处理"""
        # 更新标签显示
        self.font_size_label.config(text=f"{self.font_size.get()}px")
        self.opacity_label.config(text=f"{self.opacity.get()}")

        # 更新配置对象
        self.text_watermark.text = self.text_content.get()
        self.text_watermark.font_size = self.font_size.get()
        self.text_watermark.opacity = self.opacity.get()
        self.text_watermark.font_bold = self.font_bold.get()
        self.text_watermark.font_italic = self.font_italic.get()

        self.on_watermark_changed()

    def on_text_changed_trace(self, *args):
        """文本内容trace回调"""
        self.on_text_changed()

    def on_image_changed(self, value=None):
        """图片水印设置改变事件处理"""
        try:
            # 更新配置对象，添加错误处理
            self.image_watermark.image_path = self.image_path_var.get()
            width_val = self.image_width.get()
            height_val = self.image_height.get()
            self.image_watermark.width = width_val if width_val > 0 else None
            self.image_watermark.height = height_val if height_val > 0 else None
            self.image_watermark.opacity = self.image_opacity.get()
            self.image_watermark.keep_aspect_ratio = self.keep_aspect.get()

            self.on_watermark_changed()
        except (tk.TclError, ValueError):
            # 忽略输入框为空或无效值的错误
            pass

    def on_image_changed_trace(self, *args):
        """图片设置trace回调"""
        self.on_image_changed()

    def on_layout_changed(self, value=None):
        """布局设置改变事件处理"""
        try:
            # 更新配置对象，添加错误处理
            self.watermark_layout.x_offset = self.x_offset.get()
            self.watermark_layout.y_offset = self.y_offset.get()
            self.watermark_layout.rotation = self.rotation.get()
            self.watermark_layout.margin = self.margin.get()

            self.on_watermark_changed()
        except (tk.TclError, ValueError):
            # 忽略输入框为空或无效值的错误
            pass

    def on_layout_changed_trace(self, *args):
        """布局设置trace回调"""
        self.on_layout_changed()

    def on_preview_changed(self):
        """预览设置改变事件处理"""
        # 触发水印更新
        self.on_watermark_changed()

    def on_choose_color(self):
        """选择颜色事件处理"""
        color = colorchooser.askcolor(
            title="选择文字颜色",
            initialcolor=self.text_watermark.color
        )
        if color[0]:  # color[0] 是RGB元组
            self.text_watermark.color = tuple(int(c) for c in color[0])
            self.on_watermark_changed()

    def on_browse_image(self):
        """浏览图片事件处理"""
        filetypes = [
            ("图片文件", "*.png *.jpg *.jpeg *.bmp *.tiff"),
            ("PNG文件", "*.png"),
            ("所有文件", "*.*")
        ]

        file_path = filedialog.askopenfilename(
            title="选择水印图片",
            filetypes=filetypes
        )

        if file_path:
            self.image_path_var.set(file_path)
            self.on_image_changed()

    def set_position(self, position: WatermarkPosition):
        """设置预设位置"""
        self.watermark_layout.position = position
        self.position.set(position.value)

        # 重置偏移量为0，使用纯预设位置
        self.x_offset.set(0)
        self.y_offset.set(0)
        self.watermark_layout.x_offset = 0
        self.watermark_layout.y_offset = 0

        # 高亮选中的按钮
        for pos, btn in self.position_buttons.items():
            if pos == position:
                btn.state(['pressed'])
            else:
                btn.state(['!pressed'])

        self.on_watermark_changed()

    def get_watermark_config(self) -> dict:
        """获取当前水印配置"""
        watermark_type = WatermarkType(self.watermark_type.get())

        return {
            'type': watermark_type,
            'text_config': self.text_watermark.__dict__ if watermark_type == WatermarkType.TEXT else {},
            'image_config': self.image_watermark.__dict__ if watermark_type == WatermarkType.IMAGE else {},
            'layout': self.watermark_layout.__dict__
        }

    def load_watermark_config(self, config: dict):
        """加载水印配置"""
        try:
            # 加载水印类型
            watermark_type = config.get('type', WatermarkType.TEXT.value)
            if isinstance(watermark_type, str):
                self.watermark_type.set(watermark_type)
            else:
                self.watermark_type.set(watermark_type.value)

            # 加载文本配置
            text_config = config.get('text_config', {})
            if text_config:
                self.text_content.set(text_config.get('text', 'Sample Watermark'))
                self.font_size.set(text_config.get('font_size', 36))
                self.opacity.set(text_config.get('opacity', 128))

                # 设置颜色
                color = text_config.get('color', (255, 255, 255))
                if isinstance(color, (list, tuple)) and len(color) == 3:
                    self.text_watermark.color = tuple(color)

                # 设置字体样式
                self.font_bold.set(text_config.get('font_bold', False))
                self.font_italic.set(text_config.get('font_italic', False))

                # 更新文本水印对象
                self.text_watermark.text = self.text_content.get()
                self.text_watermark.font_size = self.font_size.get()
                self.text_watermark.opacity = self.opacity.get()
                self.text_watermark.font_bold = self.font_bold.get()
                self.text_watermark.font_italic = self.font_italic.get()

            # 加载图片配置
            image_config = config.get('image_config', {})
            if image_config:
                self.image_path_var.set(image_config.get('image_path', ''))
                width = image_config.get('width', 100)
                height = image_config.get('height', 100)
                if width is not None:
                    self.image_width.set(width)
                if height is not None:
                    self.image_height.set(height)
                self.image_opacity.set(image_config.get('opacity', 128))
                self.keep_aspect.set(image_config.get('keep_aspect_ratio', True))

                # 更新图片水印对象
                self.image_watermark.image_path = self.image_path_var.get()
                self.image_watermark.width = width
                self.image_watermark.height = height
                self.image_watermark.opacity = self.image_opacity.get()
                self.image_watermark.keep_aspect_ratio = self.keep_aspect.get()

            # 加载布局配置
            layout_config = config.get('layout', {})
            if layout_config:
                # 设置位置
                position = layout_config.get('position', WatermarkPosition.BOTTOM_RIGHT.value)
                if isinstance(position, str):
                    position_enum = WatermarkPosition(position)
                else:
                    position_enum = position

                self.watermark_layout.position = position_enum
                self.position.set(position_enum.value)

                # 设置偏移和其他布局属性
                self.x_offset.set(layout_config.get('x_offset', 0))
                self.y_offset.set(layout_config.get('y_offset', 0))
                self.rotation.set(layout_config.get('rotation', 0.0))
                self.margin.set(layout_config.get('margin', 20))

                # 更新布局对象
                self.watermark_layout.x_offset = self.x_offset.get()
                self.watermark_layout.y_offset = self.y_offset.get()
                self.watermark_layout.rotation = self.rotation.get()
                self.watermark_layout.margin = self.margin.get()

            # 更新界面显示
            self.font_size_label.config(text=f"{self.font_size.get()}px")
            self.opacity_label.config(text=f"{self.opacity.get()}")

            # 更新位置按钮状态
            for pos, btn in self.position_buttons.items():
                if pos == self.watermark_layout.position:
                    btn.state(['pressed'])
                else:
                    btn.state(['!pressed'])

            # 显示对应的设置面板
            self.on_type_changed()

            # 触发更新
            self.on_watermark_changed()

        except Exception as e:
            print(f"加载水印配置失败: {e}")

    def reset_to_defaults(self):
        """重置所有水印设置为默认值"""
        # 重置文本水印设置
        self.text_watermark = TextWatermark()
        self.image_watermark = ImageWatermark()
        self.watermark_layout = WatermarkLayout()

        # 重置界面变量
        self.watermark_type.set(WatermarkType.TEXT.value)
        self.text_content.set(self.text_watermark.text)
        self.font_size.set(self.text_watermark.font_size)
        self.opacity.set(self.text_watermark.opacity)
        self.position.set(self.watermark_layout.position.value)

        # 重置图片水印设置
        self.image_path_var.set('')
        self.image_width.set(100)
        self.image_height.set(100)
        self.keep_aspect.set(True)
        self.image_opacity.set(128)

        # 重置位置和高级设置
        self.x_offset.set(0)
        self.y_offset.set(0)
        self.rotation.set(0.0)
        self.margin.set(20)

        # 重置字体样式
        self.font_bold.set(False)
        self.font_italic.set(False)

        # 更新标签显示
        self.font_size_label.config(text=f"{self.font_size.get()}px")
        self.opacity_label.config(text=f"{self.opacity.get()}")

        # 重置位置按钮状态
        for pos, btn in self.position_buttons.items():
            if pos == self.watermark_layout.position:
                btn.state(['pressed'])
            else:
                btn.state(['!pressed'])

        # 重新显示对应的设置面板
        self.on_type_changed()

        # 触发回调
        self.on_watermark_changed()