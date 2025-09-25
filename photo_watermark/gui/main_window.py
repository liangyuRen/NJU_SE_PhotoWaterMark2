"""
主窗口界面模块

应用程序的主界面，整合所有功能面板
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import os
import glob
from typing import List, Optional
from pathlib import Path

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
from .export_panel import ExportSettingsPanel


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

        # 预览设置
        self.show_watermark_preview = tk.BooleanVar(value=True)

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
        self.image_panel = ImagePanel(self.left_panel, self.on_image_selected, self.on_watermark_position_changed)

        # 设置拖拽完成回调
        self.image_panel.on_watermark_drag_finished = self.on_watermark_drag_finished

        # 创建右侧面板（水印设置和导出设置）
        self.right_panel = ttk.Frame(self.main_frame)

        # 创建右侧滚动容器
        self.right_canvas = tk.Canvas(self.right_panel)
        self.right_scrollbar = ttk.Scrollbar(self.right_panel, orient="vertical", command=self.right_canvas.yview)
        self.right_scrollable_frame = ttk.Frame(self.right_canvas)

        self.right_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.right_canvas.configure(scrollregion=self.right_canvas.bbox("all"))
        )

        self.right_canvas.create_window((0, 0), window=self.right_scrollable_frame, anchor="nw")
        self.right_canvas.configure(yscrollcommand=self.right_scrollbar.set)

        # 创建水印设置面板
        self.watermark_panel = WatermarkPanel(
            self.right_scrollable_frame,
            self.on_watermark_changed
        )

        # 创建导出设置面板
        self.export_panel = ExportSettingsPanel(
            self.right_scrollable_frame,
            self.on_export_settings_changed
        )

        # 创建底部控制面板
        self.bottom_panel = ttk.Frame(self.main_frame)
        self.control_panel = ControlPanel(
            self.bottom_panel,
            self.on_import_images,
            self.on_export_current,
            self.on_batch_export,
            self.on_clear_list,
            self.on_reset_watermark
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

        # 配置右侧滚动面板
        self.right_canvas.pack(side="left", fill="both", expand=True)
        self.right_scrollbar.pack(side="right", fill="y")

        # 设置面板尺寸
        self.right_panel.configure(width=350)  # 增加宽度以容纳更多内容

    def bind_events(self):
        """绑定事件"""
        # 简化的拖拽支持：监听窗口事件
        self.root.bind('<Button-1>', self.on_window_click)

        # 尝试实现Windows拖拽功能
        try:
            # Windows特定的拖拽功能
            self.setup_drag_drop()
        except:
            # 如果拖拽功能不可用，只显示提示
            pass

        # 设置初始状态提示
        self.update_status("就绪 - 使用菜单、按钮或快捷键操作")

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
            # 获取可序列化的水印配置
            watermark_config = self.get_serializable_watermark_config()

            settings = {
                'window_geometry': self.root.geometry(),
                'last_watermark_config': watermark_config,
                # 其他设置...
            }
            self.config.save_settings(settings)
        except Exception as e:
            print(f"保存设置失败: {e}")

    def get_serializable_watermark_config(self) -> dict:
        """获取可序列化的水印配置"""
        config = self.get_current_watermark_config()

        # 转换枚举类型为字符串
        serializable_config = {}
        for key, value in config.items():
            if hasattr(value, 'value'):  # 枚举类型
                serializable_config[key] = value.value
            elif isinstance(value, dict):
                # 递归处理字典中的枚举
                serializable_dict = {}
                for k, v in value.items():
                    if hasattr(v, 'value'):
                        serializable_dict[k] = v.value
                    else:
                        serializable_dict[k] = v
                serializable_config[key] = serializable_dict
            else:
                serializable_config[key] = value

        return serializable_config

    def update_status(self, message: str):
        """更新状态栏"""
        self.status_bar.config(text=message)
        self.root.update_idletasks()

    def get_current_watermark_config(self) -> dict:
        """获取当前水印配置"""
        # 从水印面板获取最新配置
        return self.watermark_panel.get_watermark_config()

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

    def on_export_settings_changed(self):
        """导出设置改变事件处理"""
        # 导出设置改变时可以在这里添加逻辑
        pass

    def on_watermark_position_changed(self, x: int, y: int):
        """水印位置改变事件处理"""
        # 更新水印面板中的偏移设置
        if hasattr(self, 'watermark_panel'):
            self.watermark_panel.x_offset.set(x)
            self.watermark_panel.y_offset.set(y)
            self.watermark_panel.watermark_layout.x_offset = x
            self.watermark_panel.watermark_layout.y_offset = y

            # 设置为自定义位置
            from photo_watermark.core.watermark import WatermarkPosition
            self.watermark_panel.watermark_layout.position = WatermarkPosition.CUSTOM

            # ⚠️ 不要在拖拽时更新预览！这会导致水印重置到原位置
            # 只在拖拽结束时才需要更新预览中的实际水印
            # self.update_preview()

            # 更新状态栏
            self.update_status(f"水印位置: ({x}, {y})")

    def on_watermark_drag_finished(self):
        """水印拖拽完成事件处理"""
        # 拖拽结束时，只更新实际水印，不重新创建叠加层
        if self.current_image_index >= 0 and self.image_processor.current_image:
            show_watermark = self.watermark_panel.show_preview.get()
            if show_watermark:
                # 重置图片并重新应用水印到新位置
                self.image_processor.reset_image()
                self.apply_current_watermark()

                # 只更新预览图片，保持叠加层位置
                result_image = self.image_processor.get_current_image()
                if result_image and self.image_panel:
                    self.image_panel.update_preview_image_only(result_image)

    def on_import_images(self):
        """导入图片事件处理"""
        filetypes = [
            ("图片文件", "*.jpg *.jpeg *.png *.bmp *.tiff *.tif"),
            ("JPEG文件", "*.jpg *.jpeg"),
            ("PNG文件", "*.png"),
            ("BMP文件", "*.bmp"),
            ("TIFF文件", "*.tiff *.tif"),
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

        # 获取当前图片路径
        current_image_path = self.image_list[self.current_image_index]

        # 为防止覆盖原图，默认禁止导出到原文件夹
        # 使用桌面或文档文件夹作为默认导出位置
        import os
        from pathlib import Path

        try:
            # 优先使用桌面
            desktop_path = os.path.join(Path.home(), 'Desktop')
            if not os.path.exists(desktop_path):
                # 如果桌面不存在，使用文档文件夹
                desktop_path = os.path.join(Path.home(), 'Documents')
                if not os.path.exists(desktop_path):
                    # 最后使用用户主目录
                    desktop_path = str(Path.home())
        except:
            desktop_path = str(Path.home())

        # 使用导出设置生成文件名
        export_settings = self.export_panel.get_export_settings()
        default_filename = self.export_panel.generate_filename(current_image_path)

        filetypes = [
            ("PNG文件", "*.png"),
            ("JPEG文件", "*.jpg"),
            ("BMP文件", "*.bmp"),
            ("TIFF文件", "*.tiff"),
            ("所有文件", "*.*")
        ]

        # 根据导出设置确定默认扩展名
        export_settings = self.export_panel.get_export_settings()
        output_format = export_settings['format']['output_format']
        if output_format != "保持原格式":
            format_map = {
                "PNG": ".png",
                "JPEG": ".jpg",
                "BMP": ".bmp",
                "TIFF": ".tiff"
            }
            default_ext = format_map.get(output_format, ".png")
        else:
            default_ext = os.path.splitext(current_image_path)[1]

        file_path = filedialog.asksaveasfilename(
            title="保存图片",
            filetypes=filetypes,
            defaultextension=default_ext,
            initialdir=desktop_path,
            initialfile=default_filename
        )

        if file_path:
            self.export_single_image(file_path)

    def on_batch_export(self):
        """批量导出事件处理"""
        if not self.image_list:
            messagebox.showwarning("警告", "请先导入要处理的图片")
            return

        # 为防止覆盖原图，默认导出到桌面而非原文件夹
        try:
            desktop_path = os.path.join(Path.home(), 'Desktop')
            if not os.path.exists(desktop_path):
                desktop_path = os.path.join(Path.home(), 'Documents')
                if not os.path.exists(desktop_path):
                    desktop_path = str(Path.home())
        except:
            desktop_path = str(Path.home())

        folder = filedialog.askdirectory(
            title="选择输出文件夹",
            initialdir=desktop_path
        )
        if folder:
            self.batch_export_images(folder)

    def on_clear_list(self):
        """清空图片列表事件处理"""
        if self.image_list:
            # 确认对话框
            result = messagebox.askyesno(
                "确认清空",
                f"确定要清空所有图片吗？\n当前有 {len(self.image_list)} 张图片。"
            )
            if result:
                # 清空列表
                self.image_list.clear()
                self.current_image_index = -1

                # 清空界面
                self.image_panel.clear_list()
                self.image_processor.current_image = None
                self.image_processor.original_image = None

                # 更新状态
                self.update_status("图片列表已清空")
                messagebox.showinfo("完成", "图片列表已清空")
        else:
            messagebox.showinfo("提示", "图片列表已经是空的")

    def on_reset_watermark(self):
        """重置水印设置事件处理"""
        result = messagebox.askyesno(
            "确认重置",
            "确定要重置所有水印设置为默认值吗？"
        )
        if result:
            # 重置水印面板设置
            self.watermark_panel.reset_to_defaults()

            # 如果有当前图片，重新加载原始图片
            if self.current_image_index >= 0 and self.current_image_index < len(self.image_list):
                current_path = self.image_list[self.current_image_index]
                self.image_processor.load_image(current_path)
                self.image_panel.update_preview(self.image_processor.get_current_image())

            self.update_status("水印设置已重置")
            messagebox.showinfo("完成", "水印设置已重置为默认值")

    def setup_drag_drop(self):
        """设置拖拽功能和键盘快捷键"""
        # 添加键盘快捷键支持
        self.root.bind('<Control-o>', lambda e: self.on_import_images())
        self.root.bind('<Control-s>', lambda e: self.on_export_current())
        self.root.bind('<Control-b>', lambda e: self.on_batch_export())
        self.root.bind('<Control-r>', lambda e: self.on_reset_watermark())
        self.root.bind('<Delete>', lambda e: self.on_clear_list())

        # 设置窗口为可聚焦以接收键盘事件
        self.root.focus_set()

        # 在状态栏显示快捷键提示
        self.update_status("快捷键: Ctrl+O导入, Ctrl+S导出当前, Ctrl+B批量导出, Ctrl+R重置, Del清空列表")

    def on_window_click(self, event):
        """窗口点击事件处理"""
        # 这里可以添加更多的窗口交互逻辑
        pass

    def on_drop_files(self, event):
        """拖拽文件事件处理"""
        try:
            # 处理拖拽的文件路径
            files = event.data.split()
            image_files = []

            for file_path in files:
                # 清理路径格式
                file_path = file_path.strip('{}').strip()
                if os.path.exists(file_path):
                    ext = os.path.splitext(file_path)[1].lower()
                    if ext in ImageProcessor.SUPPORTED_FORMATS['input']:
                        image_files.append(file_path)

            if image_files:
                self.add_images(image_files)
                self.update_status(f"已通过拖拽导入 {len(image_files)} 张图片")
            else:
                messagebox.showwarning("警告", "拖拽的文件中没有支持的图片格式")

        except Exception as e:
            print(f"拖拽文件处理失败: {e}")
            messagebox.showerror("错误", "拖拽文件处理失败")

    def on_save_template(self):
        """保存模板事件处理"""
        # 获取当前水印配置
        watermark_config = self.get_current_watermark_config()

        # 创建简单的输入对话框
        template_name = tk.simpledialog.askstring(
            "保存水印模板",
            "请输入模板名称:",
            initialvalue="我的水印模板"
        )

        if template_name:
            try:
                # 获取可序列化的配置
                serializable_config = self.get_serializable_watermark_config()

                # 保存模板到配置文件
                templates = self.config.load_templates()
                templates[template_name] = serializable_config
                self.config.save_templates(templates)

                messagebox.showinfo("成功", f"模板 '{template_name}' 已保存")
                self.update_status(f"已保存水印模板: {template_name}")

            except Exception as e:
                print(f"保存模板失败: {e}")
                messagebox.showerror("错误", f"保存模板失败: {e}")

    def on_load_template(self):
        """加载模板事件处理"""
        try:
            # 获取所有模板
            templates = self.config.load_templates()

            if not templates:
                messagebox.showinfo("提示", "暂无保存的模板")
                return

            # 创建模板选择对话框
            template_names = list(templates.keys())
            selected_template = self.show_template_selection_dialog(template_names, "加载水印模板")

            if selected_template:
                # 加载选中的模板
                template_config = templates[selected_template]
                self.load_watermark_config(template_config)

                messagebox.showinfo("成功", f"模板 '{selected_template}' 已加载")
                self.update_status(f"已加载水印模板: {selected_template}")

        except Exception as e:
            print(f"加载模板失败: {e}")
            messagebox.showerror("错误", f"加载模板失败: {e}")

    def on_manage_templates(self):
        """管理模板事件处理"""
        try:
            # 获取所有模板
            templates = self.config.load_templates()

            if not templates:
                messagebox.showinfo("提示", "暂无保存的模板")
                return

            # 创建模板管理对话框
            self.show_template_management_dialog(templates)

        except Exception as e:
            print(f"管理模板失败: {e}")
            messagebox.showerror("错误", f"管理模板失败: {e}")

    def show_template_selection_dialog(self, template_names: List[str], title: str) -> Optional[str]:
        """显示模板选择对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("300x200")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        # 居中显示
        dialog.geometry(f"+{self.root.winfo_x() + 50}+{self.root.winfo_y() + 50}")

        selected_template = None

        # 创建列表框
        frame = ttk.Frame(dialog)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Label(frame, text="请选择要加载的模板:").pack(anchor='w', pady=(0, 5))

        listbox = tk.Listbox(frame, height=8)
        listbox.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        for name in template_names:
            listbox.insert(tk.END, name)

        # 按钮框架
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X)

        def on_load():
            selection = listbox.curselection()
            if selection:
                nonlocal selected_template
                selected_template = template_names[selection[0]]
                dialog.destroy()

        def on_cancel():
            dialog.destroy()

        ttk.Button(button_frame, text="加载", command=on_load).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="取消", command=on_cancel).pack(side=tk.RIGHT)

        # 双击加载
        listbox.bind('<Double-Button-1>', lambda e: on_load())

        dialog.wait_window()
        return selected_template

    def show_template_management_dialog(self, templates: dict):
        """显示模板管理对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("管理水印模板")
        dialog.geometry("400x300")
        dialog.resizable(True, True)
        dialog.transient(self.root)
        dialog.grab_set()

        # 居中显示
        dialog.geometry(f"+{self.root.winfo_x() + 50}+{self.root.winfo_y() + 50}")

        # 创建界面
        frame = ttk.Frame(dialog)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Label(frame, text="已保存的模板:").pack(anchor='w', pady=(0, 5))

        # 列表框和滚动条
        list_frame = ttk.Frame(frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        listbox = tk.Listbox(list_frame)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=listbox.yview)
        listbox.config(yscrollcommand=scrollbar.set)

        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        template_names = list(templates.keys())
        for name in template_names:
            listbox.insert(tk.END, name)

        # 按钮框架
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X)

        def on_load():
            selection = listbox.curselection()
            if selection:
                selected_name = template_names[selection[0]]
                template_config = templates[selected_name]
                self.load_watermark_config(template_config)
                messagebox.showinfo("成功", f"模板 '{selected_name}' 已加载")
                self.update_status(f"已加载水印模板: {selected_name}")

        def on_delete():
            selection = listbox.curselection()
            if selection:
                selected_name = template_names[selection[0]]
                result = messagebox.askyesno("确认删除", f"确定要删除模板 '{selected_name}' 吗？")
                if result:
                    del templates[selected_name]
                    self.config.save_templates(templates)
                    listbox.delete(selection[0])
                    template_names.pop(selection[0])
                    messagebox.showinfo("成功", f"模板 '{selected_name}' 已删除")

        def on_close():
            dialog.destroy()

        ttk.Button(button_frame, text="加载", command=on_load).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="删除", command=on_delete).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="关闭", command=on_close).pack(side=tk.RIGHT)

        dialog.wait_window()

    def load_watermark_config(self, config: dict):
        """加载水印配置到界面"""
        try:
            # 使用水印面板的加载方法
            self.watermark_panel.load_watermark_config(config)

            # 模板加载后，关闭水印预览以避免自动应用到所有图片
            self.watermark_panel.show_preview.set(False)

            # 更新预览（但不应用水印，因为预览已关闭）
            if self.current_image_index >= 0:
                self.update_preview()

        except Exception as e:
            print(f"加载配置失败: {e}")

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

            # 检查是否显示水印预览
            show_watermark = self.watermark_panel.show_preview.get()

            # 如果启用预览，应用水印到图片上
            if show_watermark:
                self.apply_current_watermark()

            # 更新预览显示（显示带或不带水印的图片）
            preview_image = self.image_processor.get_current_image()
            self.image_panel.update_preview(preview_image)

            # 检查是否显示可拖拽的水印叠加层
            show_indicator = self.watermark_panel.show_position_indicator.get()
            self.image_panel.show_watermark_indicator = show_indicator

            # 如果启用了拖拽指示器，添加水印叠加层
            if show_indicator:
                watermark_config = self.get_current_watermark_config()
                self.image_panel.add_watermark_overlay(watermark_config)

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
        # 获取JPEG质量设置
        export_settings = self.export_panel.get_export_settings()
        jpeg_quality = export_settings['format']['jpeg_quality']

        if self.image_processor.save_image(output_path, quality=jpeg_quality):
            self.update_status(f"图片已保存: {os.path.basename(output_path)}")
            messagebox.showinfo("成功", "图片导出成功！")
        else:
            messagebox.showerror("错误", "图片导出失败！")

    def batch_export_images(self, output_dir: str):
        """批量导出图片"""
        if not self.image_list:
            messagebox.showwarning("警告", "没有图片需要导出")
            return

        # 获取当前水印配置和导出设置
        watermark_config = self.get_current_watermark_config()
        export_settings = self.export_panel.get_export_settings()
        jpeg_quality = export_settings['format']['jpeg_quality']

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
                    print(f"成功加载图片: {image_path}")  # 调试信息

                    # 应用水印
                    print(f"水印配置类型: {watermark_config['type']}")  # 调试信息
                    if watermark_config['type'] == WatermarkType.TEXT:
                        print("应用文本水印...")  # 调试信息
                        self.apply_text_watermark_to_processor(processor, watermark_config)
                    elif watermark_config['type'] == WatermarkType.IMAGE:
                        print("应用图片水印...")  # 调试信息
                        # TODO: 实现图片水印批量处理
                        pass
                    else:
                        print(f"未知水印类型: {watermark_config['type']}")  # 调试信息

                    # 使用导出设置生成输出文件名
                    output_filename = self.export_panel.generate_filename(image_path)
                    output_path = os.path.join(output_dir, output_filename)
                    print(f"保存到: {output_path}")  # 调试信息

                    # 保存图片（使用JPEG质量设置）
                    if processor.save_image(output_path, quality=jpeg_quality):
                        print(f"保存成功: {output_path}")  # 调试信息
                        success_count += 1
                    else:
                        print(f"保存失败: {output_path}")  # 调试信息
                else:
                    print(f"加载图片失败: {image_path}")  # 调试信息

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