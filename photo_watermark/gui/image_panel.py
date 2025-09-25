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

    def __init__(self, parent: tk.Widget, on_image_selected: Callable[[str, int], None]):
        """
        初始化图片面板

        Args:
            parent: 父组件
            on_image_selected: 图片选择回调函数
        """
        self.parent = parent
        self.on_image_selected = on_image_selected
        self.image_list: List[str] = []
        self.current_preview_image: Optional[ImageTk.PhotoImage] = None

        self.create_widgets()
        self.setup_layout()

    def create_widgets(self):
        """创建组件"""
        # 图片列表框架
        self.list_frame = ttk.LabelFrame(self.parent, text="图片列表")

        # 图片列表
        self.image_listbox = tk.Listbox(
            self.list_frame,
            height=8,
            selectmode=tk.SINGLE
        )

        # 列表滚动条
        self.list_scrollbar = ttk.Scrollbar(
            self.list_frame,
            orient=tk.VERTICAL,
            command=self.image_listbox.yview
        )
        self.image_listbox.config(yscrollcommand=self.list_scrollbar.set)

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
        self.image_listbox.bind('<<ListboxSelect>>', self.on_listbox_select)
        self.preview_canvas.bind('<Button-1>', self.on_canvas_click)
        self.preview_canvas.bind('<B1-Motion>', self.on_canvas_drag)

    def setup_layout(self):
        """设置布局"""
        # 图片列表区域
        self.list_frame.pack(fill=tk.BOTH, expand=False, pady=(0, 5))
        self.image_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
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

        # 清空列表框
        self.image_listbox.delete(0, tk.END)

        # 添加图片文件名到列表框
        for path in image_paths:
            filename = os.path.basename(path)
            self.image_listbox.insert(tk.END, filename)

    def update_preview(self, image: Optional[Image.Image]):
        """
        更新预览图片

        Args:
            image: PIL图片对象
        """
        # 清空画布
        self.preview_canvas.delete("all")

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

        self.preview_canvas.create_image(
            x, y,
            anchor=tk.NW,
            image=self.current_preview_image
        )

        # 设置滚动区域
        self.preview_canvas.config(scrollregion=self.preview_canvas.bbox("all"))

    def get_selected_image(self) -> Optional[str]:
        """
        获取当前选中的图片路径

        Returns:
            str: 图片路径，如果未选中则返回None
        """
        selection = self.image_listbox.curselection()
        if selection and self.image_list:
            index = selection[0]
            if 0 <= index < len(self.image_list):
                return self.image_list[index]
        return None

    def get_selected_index(self) -> int:
        """
        获取当前选中的图片索引

        Returns:
            int: 图片索引，如果未选中则返回-1
        """
        selection = self.image_listbox.curselection()
        if selection:
            return selection[0]
        return -1

    def select_image(self, index: int):
        """
        选中指定索引的图片

        Args:
            index: 图片索引
        """
        if 0 <= index < self.image_listbox.size():
            self.image_listbox.selection_clear(0, tk.END)
            self.image_listbox.selection_set(index)
            self.image_listbox.see(index)

    def clear_list(self):
        """清空图片列表"""
        self.image_list.clear()
        self.image_listbox.delete(0, tk.END)
        self.preview_canvas.delete("all")
        self.current_preview_image = None

    def on_listbox_select(self, event):
        """列表框选择事件处理"""
        selection = self.image_listbox.curselection()
        if selection and self.image_list:
            index = selection[0]
            if 0 <= index < len(self.image_list):
                image_path = self.image_list[index]
                self.on_image_selected(image_path, index)

    def on_canvas_click(self, event):
        """画布点击事件处理"""
        # TODO: 实现水印位置拖拽功能
        pass

    def on_canvas_drag(self, event):
        """画布拖拽事件处理"""
        # TODO: 实现水印位置拖拽功能
        pass