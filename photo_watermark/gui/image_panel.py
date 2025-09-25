"""
图片面板模块

显示图片列表和预览功能
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from typing import List, Callable, Optional
import os


class ImagePanel:
    """图片面板类"""

    def __init__(self, parent: tk.Widget, on_image_selected: Callable[[str, int], None], on_watermark_position_changed: Callable[[int, int], None] = None):
        """
        初始化图片面板

        Args:
            parent: 父组件
            on_image_selected: 图片选择回调函数
            on_watermark_position_changed: 水印位置改变回调函数
        """
        self.parent = parent
        self.on_image_selected = on_image_selected
        self.on_watermark_position_changed = on_watermark_position_changed
        self.image_list: List[str] = []
        self.current_preview_image: Optional[ImageTk.PhotoImage] = None

        # 水印拖拽相关
        self.is_dragging = False
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.watermark_start_x = 0
        self.watermark_start_y = 0
        self.watermark_overlay_id = None
        self.watermark_text_id = None
        self.current_image_scale = 1.0
        self.current_image_offset = (0, 0)
        self.show_watermark_indicator = True

        self.create_widgets()
        self.setup_layout()

    def create_widgets(self):
        """创建组件"""
        # 图片列表框架
        self.list_frame = ttk.LabelFrame(self.parent, text="图片列表")

        # 图片列表框架
        self.list_container = ttk.Frame(self.list_frame)

        # 使用Treeview来显示缩略图和文件名
        self.image_treeview = ttk.Treeview(
            self.list_container,
            columns=('filename',),
            show='tree headings',
            height=8,
            selectmode='browse'
        )

        # 设置列标题
        self.image_treeview.heading('#0', text='缩略图')
        self.image_treeview.heading('filename', text='文件名')
        self.image_treeview.column('#0', width=80, minwidth=80)
        self.image_treeview.column('filename', width=200, minwidth=150)

        # 存储缩略图
        self.thumbnails = {}

        # 列表滚动条
        self.list_scrollbar = ttk.Scrollbar(
            self.list_container,
            orient=tk.VERTICAL,
            command=self.image_treeview.yview
        )
        self.image_treeview.config(yscrollcommand=self.list_scrollbar.set)

        # 预览框架
        self.preview_frame = ttk.LabelFrame(self.parent, text="预览")

        # 预览画布
        self.preview_canvas = tk.Canvas(
            self.preview_frame,
            width=400,
            height=300,
            bg='white'
        )

        # 预览滚动条
        self.h_scrollbar = ttk.Scrollbar(
            self.preview_frame,
            orient=tk.HORIZONTAL,
            command=self.preview_canvas.xview
        )
        self.v_scrollbar = ttk.Scrollbar(
            self.preview_frame,
            orient=tk.VERTICAL,
            command=self.preview_canvas.yview
        )

        self.preview_canvas.config(
            xscrollcommand=self.h_scrollbar.set,
            yscrollcommand=self.v_scrollbar.set
        )

        # 绑定事件
        self.image_treeview.bind('<<TreeviewSelect>>', self.on_treeview_select)
        self.preview_canvas.bind('<Button-1>', self.on_canvas_click)
        self.preview_canvas.bind('<B1-Motion>', self.on_canvas_drag)
        self.preview_canvas.bind('<ButtonRelease-1>', self.on_canvas_release)

        # 绑定鼠标移动事件到整个画布，以便更好地跟踪拖拽
        self.preview_canvas.bind('<Motion>', self.on_canvas_motion)

    def setup_layout(self):
        """设置布局"""
        # 图片列表区域
        self.list_frame.pack(fill=tk.BOTH, expand=False, pady=(0, 5))
        self.list_container.pack(fill=tk.BOTH, expand=True)
        self.image_treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 预览区域
        self.preview_frame.pack(fill=tk.BOTH, expand=True)

        # 预览画布和滚动条
        self.preview_canvas.grid(row=0, column=0, sticky='nsew')
        self.h_scrollbar.grid(row=1, column=0, sticky='ew')
        self.v_scrollbar.grid(row=0, column=1, sticky='ns')

        # 设置网格权重
        self.preview_frame.grid_rowconfigure(0, weight=1)
        self.preview_frame.grid_columnconfigure(0, weight=1)

    def update_image_list(self, image_paths: List[str]):
        """
        更新图片列表

        Args:
            image_paths: 图片路径列表
        """
        self.image_list = image_paths

        # 清空列表
        for item in self.image_treeview.get_children():
            self.image_treeview.delete(item)
        self.thumbnails.clear()

        # 添加图片到列表，生成缩略图
        for i, path in enumerate(image_paths):
            filename = os.path.basename(path)

            try:
                # 生成缩略图
                with Image.open(path) as img:
                    # 创建64x64的缩略图
                    thumbnail = img.copy()
                    thumbnail.thumbnail((64, 64), Image.Resampling.LANCZOS)

                    # 转换为Tkinter格式
                    thumbnail_tk = ImageTk.PhotoImage(thumbnail)
                    self.thumbnails[f'item_{i}'] = thumbnail_tk

                    # 添加到Treeview
                    item_id = self.image_treeview.insert(
                        '', 'end',
                        iid=f'item_{i}',
                        image=thumbnail_tk,
                        values=(filename,)
                    )
            except Exception as e:
                # 如果无法生成缩略图，只显示文件名
                print(f"无法生成缩略图: {path}, 错误: {e}")
                item_id = self.image_treeview.insert(
                    '', 'end',
                    iid=f'item_{i}',
                    text=filename,
                    values=(filename,)
                )

    def update_preview(self, image: Optional[Image.Image]):
        """
        更新预览图片

        Args:
            image: PIL图片对象
        """
        # 清空画布
        self.preview_canvas.delete("all")
        self.watermark_overlay_id = None
        self.watermark_text_id = None

        if image is None:
            return

        # 计算显示尺寸
        canvas_width = self.preview_canvas.winfo_width()
        canvas_height = self.preview_canvas.winfo_height()

        if canvas_width <= 1 or canvas_height <= 1:
            canvas_width, canvas_height = 400, 300

        # 计算缩放比例以适应画布
        img_width, img_height = image.size
        scale_x = canvas_width / img_width
        scale_y = canvas_height / img_height
        scale = min(scale_x, scale_y, 1.0)  # 不放大，只缩小

        # 保存缩放信息供拖拽使用
        self.current_image_scale = scale

        # 调整图片尺寸
        if scale < 1.0:
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            display_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        else:
            display_image = image

        # 转换为Tkinter可显示的格式
        self.current_preview_image = ImageTk.PhotoImage(display_image)

        # 在画布中心显示图片
        display_width, display_height = display_image.size
        x = (canvas_width - display_width) // 2
        y = (canvas_height - display_height) // 2

        # 保存图片偏移信息
        self.current_image_offset = (x, y)

        self.preview_canvas.create_image(
            x, y,
            anchor=tk.NW,
            image=self.current_preview_image
        )

        # 添加水印叠加层（可拖拽的水印预览）
        # 这个方法需要从主窗口调用，传入水印配置
        pass

        # 设置滚动区域
        self.preview_canvas.config(scrollregion=self.preview_canvas.bbox("all"))

    def get_selected_image(self) -> Optional[str]:
        """
        获取当前选中的图片路径

        Returns:
            str: 图片路径，如果未选中则返回None
        """
        selection = self.image_treeview.selection()
        if selection and self.image_list:
            # 从item_id提取索引
            try:
                item_id = selection[0]
                index = int(item_id.split('_')[1])
                if 0 <= index < len(self.image_list):
                    return self.image_list[index]
            except (ValueError, IndexError):
                pass
        return None

    def get_selected_index(self) -> int:
        """
        获取当前选中的图片索引

        Returns:
            int: 图片索引，如果未选中则返回-1
        """
        selection = self.image_treeview.selection()
        if selection:
            try:
                item_id = selection[0]
                return int(item_id.split('_')[1])
            except (ValueError, IndexError):
                pass
        return -1

    def select_image(self, index: int):
        """
        选中指定索引的图片

        Args:
            index: 图片索引
        """
        item_id = f'item_{index}'
        if self.image_treeview.exists(item_id):
            # 清除之前的选择
            for item in self.image_treeview.selection():
                self.image_treeview.selection_remove(item)
            # 选中新项目
            self.image_treeview.selection_set(item_id)
            self.image_treeview.see(item_id)

    def clear_list(self):
        """清空图片列表"""
        self.image_list.clear()
        for item in self.image_treeview.get_children():
            self.image_treeview.delete(item)
        self.thumbnails.clear()
        self.preview_canvas.delete("all")
        self.current_preview_image = None

    def on_treeview_select(self, event):
        """Treeview选择事件处理"""
        selection = self.image_treeview.selection()
        if selection and self.image_list:
            try:
                item_id = selection[0]
                index = int(item_id.split('_')[1])
                if 0 <= index < len(self.image_list):
                    image_path = self.image_list[index]
                    self.on_image_selected(image_path, index)
            except (ValueError, IndexError):
                pass

    def add_watermark_overlay(self, watermark_config: dict):
        """添加可拖拽的水印叠加层"""
        if not self.current_preview_image or self.current_image_scale <= 0 or not self.show_watermark_indicator:
            return

        # 获取图片显示信息
        img_offset_x, img_offset_y = self.current_image_offset

        # 根据水印类型创建不同的叠加层
        from photo_watermark.core.watermark import WatermarkType
        watermark_type = watermark_config.get('type', WatermarkType.TEXT)

        if watermark_type == WatermarkType.TEXT:
            self.create_text_watermark_overlay(watermark_config)
        elif watermark_type == WatermarkType.IMAGE:
            self.create_image_watermark_overlay(watermark_config)

    def create_text_watermark_overlay(self, config: dict):
        """创建文本水印叠加层"""
        text_config = config.get('text_config', {})
        layout_config = config.get('layout', {})

        # 获取文本内容
        text = text_config.get('text', 'Sample Watermark')
        font_size = text_config.get('font_size', 36)
        opacity = text_config.get('opacity', 128)
        color = text_config.get('color', (255, 255, 255))

        # 计算水印在预览中的位置
        watermark_pos = self.calculate_preview_watermark_position(config, text_size=(len(text) * font_size * 0.6, font_size))

        if watermark_pos:
            x, y = watermark_pos

            # 创建半透明的文本水印叠加层
            alpha_value = int(opacity / 255 * 0.7 * 255)  # 预览中稍微透明一些

            # 创建背景框
            text_width = len(text) * int(font_size * self.current_image_scale * 0.6)
            text_height = int(font_size * self.current_image_scale)

            self.watermark_overlay_id = self.preview_canvas.create_rectangle(
                x - 5, y - 5,
                x + text_width + 5, y + text_height + 5,
                fill='', outline='red', width=2, dash=(5, 5),
                tags="watermark_overlay"
            )

            # 创建文本
            self.watermark_text_id = self.preview_canvas.create_text(
                x, y,
                text=text,
                anchor='nw',
                fill=f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}",
                font=('Arial', int(font_size * self.current_image_scale), 'bold'),
                tags="watermark_overlay"
            )

            # 绑定拖拽事件
            self.preview_canvas.tag_bind("watermark_overlay", "<Button-1>", self.on_watermark_click)
            self.preview_canvas.tag_bind("watermark_overlay", "<B1-Motion>", self.on_watermark_drag)
            self.preview_canvas.tag_bind("watermark_overlay", "<ButtonRelease-1>", self.on_watermark_release)

    def create_image_watermark_overlay(self, config: dict):
        """创建图片水印叠加层"""
        image_config = config.get('image_config', {})

        watermark_path = image_config.get('image_path', '')
        if not watermark_path or not os.path.exists(watermark_path):
            return

        try:
            from PIL import Image

            # 加载水印图片
            with Image.open(watermark_path) as wm_img:
                # 获取尺寸
                width = image_config.get('width', wm_img.width)
                height = image_config.get('height', wm_img.height)

                # 计算预览中的位置
                watermark_pos = self.calculate_preview_watermark_position(config, text_size=(width, height))

                if watermark_pos:
                    x, y = watermark_pos

                    # 调整到预览尺寸
                    preview_width = int(width * self.current_image_scale)
                    preview_height = int(height * self.current_image_scale)

                    # 创建边框指示器
                    self.watermark_overlay_id = self.preview_canvas.create_rectangle(
                        x, y,
                        x + preview_width, y + preview_height,
                        fill='', outline='blue', width=2, dash=(3, 3),
                        tags="watermark_overlay"
                    )

                    # 添加标签
                    self.watermark_text_id = self.preview_canvas.create_text(
                        x + preview_width // 2, y + preview_height // 2,
                        text="图片水印",
                        fill='blue',
                        font=('Arial', 10, 'bold'),
                        tags="watermark_overlay"
                    )

                    # 绑定拖拽事件
                    self.preview_canvas.tag_bind("watermark_overlay", "<Button-1>", self.on_watermark_click)
                    self.preview_canvas.tag_bind("watermark_overlay", "<B1-Motion>", self.on_watermark_drag)
                    self.preview_canvas.tag_bind("watermark_overlay", "<ButtonRelease-1>", self.on_watermark_release)

        except Exception as e:
            print(f"创建图片水印叠加层失败: {e}")

    def calculate_preview_watermark_position(self, config: dict, text_size: tuple) -> tuple:
        """计算水印在预览中的显示位置"""
        layout_config = config.get('layout', {})

        # 获取原始图片尺寸
        if not self.current_preview_image:
            return None

        img_offset_x, img_offset_y = self.current_image_offset
        preview_width = int(self.current_preview_image.width())
        preview_height = int(self.current_preview_image.height())

        # 获取水印配置
        from photo_watermark.core.watermark import WatermarkPosition, WatermarkCalculator, WatermarkLayout

        position = layout_config.get('position', 'bottom_right')
        if isinstance(position, str):
            try:
                position = WatermarkPosition(position)
            except:
                position = WatermarkPosition.BOTTOM_RIGHT

        x_offset = layout_config.get('x_offset', 0)
        y_offset = layout_config.get('y_offset', 0)
        margin = layout_config.get('margin', 20)

        # 创建布局对象
        layout = WatermarkLayout()
        layout.position = position
        layout.x_offset = x_offset
        layout.y_offset = y_offset
        layout.margin = margin

        # 计算在原始图片中的位置
        original_size = (int(preview_width / self.current_image_scale), int(preview_height / self.current_image_scale))
        watermark_size = text_size

        original_pos = WatermarkCalculator.calculate_position(original_size, watermark_size, layout)

        # 转换到预览坐标
        preview_x = int(original_pos[0] * self.current_image_scale) + img_offset_x
        preview_y = int(original_pos[1] * self.current_image_scale) + img_offset_y

        return (preview_x, preview_y)

    def on_watermark_click(self, event):
        """水印点击事件处理"""
        if self.watermark_overlay_id:
            # 记录拖拽开始时的鼠标位置
            self.is_dragging = True
            self.drag_start_x = event.x
            self.drag_start_y = event.y

            # 记录水印的初始位置
            bbox = self.preview_canvas.bbox(self.watermark_overlay_id)
            if bbox:
                self.watermark_start_x = bbox[0]
                self.watermark_start_y = bbox[1]
            else:
                self.watermark_start_x = event.x
                self.watermark_start_y = event.y

            # 清除缓存的尺寸数据，强制重新计算
            if hasattr(self, '_watermark_width'):
                delattr(self, '_watermark_width')
            if hasattr(self, '_watermark_height'):
                delattr(self, '_watermark_height')
            if hasattr(self, '_text_offset_x'):
                delattr(self, '_text_offset_x')
            if hasattr(self, '_text_offset_y'):
                delattr(self, '_text_offset_y')
            if hasattr(self, '_update_counter'):
                delattr(self, '_update_counter')

            self.preview_canvas.config(cursor="fleur")  # 更改鼠标样式
            print(f"开始拖拽水印: 鼠标({event.x}, {event.y}), 水印({self.watermark_start_x}, {self.watermark_start_y})")

    def on_watermark_drag(self, event):
        """水印拖拽事件处理 - 超级优化版本"""
        if not self.is_dragging or not self.watermark_overlay_id:
            return

        # 直接计算目标位置
        target_x = self.watermark_start_x + (event.x - self.drag_start_x)
        target_y = self.watermark_start_y + (event.y - self.drag_start_y)

        # 获取当前水印的尺寸（只获取一次）
        if not hasattr(self, '_watermark_width') or not hasattr(self, '_watermark_height'):
            coords = self.preview_canvas.coords(self.watermark_overlay_id)
            if len(coords) >= 4:
                self._watermark_width = coords[2] - coords[0]
                self._watermark_height = coords[3] - coords[1]
            else:
                return

        # 直接设置矩形坐标 - 最高效的方法
        self.preview_canvas.coords(
            self.watermark_overlay_id,
            target_x, target_y,
            target_x + self._watermark_width,
            target_y + self._watermark_height
        )

        # 如果有文本，同步移动
        if self.watermark_text_id:
            if not hasattr(self, '_text_offset_x') or not hasattr(self, '_text_offset_y'):
                text_coords = self.preview_canvas.coords(self.watermark_text_id)
                if len(text_coords) >= 2:
                    self._text_offset_x = text_coords[0] - self.watermark_start_x
                    self._text_offset_y = text_coords[1] - self.watermark_start_y
                else:
                    self._text_offset_x = self._watermark_width / 2
                    self._text_offset_y = self._watermark_height / 2

            self.preview_canvas.coords(
                self.watermark_text_id,
                target_x + self._text_offset_x,
                target_y + self._text_offset_y
            )

        # 降低更新频率 - 每10个像素更新一次位置到主窗口
        if not hasattr(self, '_update_counter'):
            self._update_counter = 0

        self._update_counter += 1
        if self._update_counter % 3 == 0:  # 每3次拖拽事件更新一次
            self._update_position_to_main_window(target_x, target_y)

    def _update_position_to_main_window(self, x: float, y: float):
        """更新位置到主窗口"""
        if self.current_image_scale > 0 and self.on_watermark_position_changed:
            img_offset_x, img_offset_y = self.current_image_offset

            # 计算水印在原始图像中的位置（考虑缩放）
            watermark_x = int((x - img_offset_x) / self.current_image_scale)
            watermark_y = int((y - img_offset_y) / self.current_image_scale)

            # 通知主窗口水印位置已改变
            self.on_watermark_position_changed(watermark_x, watermark_y)

    def on_watermark_release(self, event):
        """水印释放事件处理"""
        if self.is_dragging:
            # 最后一次更新位置到主窗口
            target_x = self.watermark_start_x + (event.x - self.drag_start_x)
            target_y = self.watermark_start_y + (event.y - self.drag_start_y)
            self._update_position_to_main_window(target_x, target_y)

            self.is_dragging = False
            self.preview_canvas.config(cursor="")  # 恢复鼠标样式

            # 通知主窗口拖拽已结束，需要更新预览中的实际水印位置
            if hasattr(self, 'on_watermark_drag_finished'):
                self.on_watermark_drag_finished()

            print("结束拖拽水印")

    def on_canvas_click(self, event):
        """画布点击事件处理"""
        print(f"画布点击: ({event.x}, {event.y})")

    def on_canvas_drag(self, event):
        """画布拖拽事件处理"""
        # 如果正在拖拽水印，调用水印拖拽处理
        if self.is_dragging:
            self.on_watermark_drag(event)

    def on_canvas_motion(self, event):
        """画布鼠标移动事件处理"""
        # 如果正在拖拽水印，实时更新位置
        if self.is_dragging:
            self.on_watermark_drag(event)

    def on_canvas_release(self, event):
        """画布释放事件处理"""
        # 如果正在拖拽水印，结束拖拽
        if self.is_dragging:
            self.on_watermark_release(event)

    def update_preview_image_only(self, image: Optional[Image.Image]):
        """
        只更新预览图片，不重新创建水印叠加层

        Args:
            image: PIL图片对象
        """
        if image is None:
            return

        # 保存当前水印叠加层的状态
        overlay_coords = None
        text_coords = None

        if self.watermark_overlay_id:
            overlay_coords = self.preview_canvas.coords(self.watermark_overlay_id)
        if self.watermark_text_id:
            text_coords = self.preview_canvas.coords(self.watermark_text_id)

        # 删除所有非水印对象，保留水印叠加层
        all_items = self.preview_canvas.find_all()
        for item in all_items:
            tags = self.preview_canvas.gettags(item)
            if "watermark_overlay" not in tags:
                self.preview_canvas.delete(item)

        # 计算显示尺寸（复用现有逻辑）
        canvas_width = self.preview_canvas.winfo_width()
        canvas_height = self.preview_canvas.winfo_height()

        if canvas_width <= 1 or canvas_height <= 1:
            canvas_width, canvas_height = 400, 300

        # 计算缩放比例以适应画布
        img_width, img_height = image.size
        scale_x = canvas_width / img_width
        scale_y = canvas_height / img_height
        scale = min(scale_x, scale_y, 1.0)

        # 保存缩放信息
        self.current_image_scale = scale

        # 调整图片尺寸
        if scale < 1.0:
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            display_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        else:
            display_image = image

        # 转换为Tkinter可显示的格式
        self.current_preview_image = ImageTk.PhotoImage(display_image)

        # 在画布中心显示图片
        display_width, display_height = display_image.size
        x = (canvas_width - display_width) // 2
        y = (canvas_height - display_height) // 2

        # 保存图片偏移信息
        self.current_image_offset = (x, y)

        # 创建图片，确保它在最底层
        image_id = self.preview_canvas.create_image(
            x, y,
            anchor=tk.NW,
            image=self.current_preview_image
        )

        # 将图片移到最底层，确保水印叠加层在上方
        self.preview_canvas.tag_lower(image_id)

        # 设置滚动区域
        self.preview_canvas.config(scrollregion=self.preview_canvas.bbox("all"))