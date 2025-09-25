"""
应用程序配置管理模块

处理应用设置的保存和加载
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List


class AppConfig:
    """应用程序配置管理器"""

    def __init__(self, config_dir: Optional[str] = None):
        """
        初始化配置管理器

        Args:
            config_dir: 配置目录路径，如果为None则使用默认路径
        """
        if config_dir is None:
            # 使用用户目录下的应用配置文件夹
            home_dir = Path.home()
            config_dir = home_dir / ".photo_watermark"

        self.config_dir = Path(config_dir)
        self.config_file = self.config_dir / "config.json"
        self.templates_dir = self.config_dir / "templates"

        # 确保配置目录存在
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.templates_dir.mkdir(parents=True, exist_ok=True)

        # 默认配置
        self.default_config = {
            'window': {
                'width': 1200,
                'height': 800,
                'x': 100,
                'y': 100
            },
            'last_import_dir': str(Path.home()),
            'last_export_dir': str(Path.home()),
            'watermark': {
                'last_text': 'Sample Watermark',
                'last_font_size': 36,
                'last_color': [255, 255, 255],
                'last_opacity': 128,
                'last_position': 'bottom_right'
            },
            'export': {
                'default_format': 'png',
                'jpeg_quality': 95,
                'naming_rule': {
                    'add_prefix': False,
                    'prefix': 'wm_',
                    'add_suffix': True,
                    'suffix': '_watermarked'
                }
            }
        }

    def load_settings(self) -> Dict[str, Any]:
        """
        加载应用设置

        Returns:
            Dict[str, Any]: 配置字典
        """
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                # 合并默认配置和用户配置
                return self._merge_config(self.default_config, config)
            else:
                return self.default_config.copy()
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            return self.default_config.copy()

    def save_settings(self, config: Dict[str, Any]):
        """
        保存应用设置

        Args:
            config: 要保存的配置字典
        """
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"保存配置文件失败: {e}")

    def get_templates_dir(self) -> Path:
        """
        获取模板目录路径

        Returns:
            Path: 模板目录路径
        """
        return self.templates_dir

    def save_template(self, name: str, template_data: Dict[str, Any]) -> bool:
        """
        保存水印模板

        Args:
            name: 模板名称
            template_data: 模板数据

        Returns:
            bool: 保存是否成功
        """
        try:
            template_file = self.templates_dir / f"{name}.json"
            with open(template_file, 'w', encoding='utf-8') as f:
                json.dump(template_data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"保存模板失败: {e}")
            return False

    def load_template(self, name: str) -> Optional[Dict[str, Any]]:
        """
        加载水印模板

        Args:
            name: 模板名称

        Returns:
            Optional[Dict[str, Any]]: 模板数据，如果加载失败返回None
        """
        try:
            template_file = self.templates_dir / f"{name}.json"
            if template_file.exists():
                with open(template_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"加载模板失败: {e}")
        return None

    def list_templates(self) -> List[str]:
        """
        列出所有可用模板

        Returns:
            List[str]: 模板名称列表
        """
        try:
            templates = []
            for file_path in self.templates_dir.glob("*.json"):
                templates.append(file_path.stem)
            return sorted(templates)
        except Exception as e:
            print(f"列出模板失败: {e}")
            return []

    def delete_template(self, name: str) -> bool:
        """
        删除模板

        Args:
            name: 模板名称

        Returns:
            bool: 删除是否成功
        """
        try:
            template_file = self.templates_dir / f"{name}.json"
            if template_file.exists():
                template_file.unlink()
                return True
        except Exception as e:
            print(f"删除模板失败: {e}")
        return False

    def _merge_config(self, default: Dict[str, Any], user: Dict[str, Any]) -> Dict[str, Any]:
        """
        合并默认配置和用户配置

        Args:
            default: 默认配置
            user: 用户配置

        Returns:
            Dict[str, Any]: 合并后的配置
        """
        result = default.copy()

        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_config(result[key], value)
            else:
                result[key] = value

        return result

    def get_recent_files(self) -> List[str]:
        """
        获取最近打开的文件列表

        Returns:
            List[str]: 最近文件路径列表
        """
        config = self.load_settings()
        return config.get('recent_files', [])

    def add_recent_file(self, file_path: str, max_recent: int = 10):
        """
        添加最近打开的文件

        Args:
            file_path: 文件路径
            max_recent: 最大保存数量
        """
        config = self.load_settings()
        recent_files = config.get('recent_files', [])

        # 移除重复项
        if file_path in recent_files:
            recent_files.remove(file_path)

        # 添加到开头
        recent_files.insert(0, file_path)

        # 限制数量
        recent_files = recent_files[:max_recent]

        # 保存配置
        config['recent_files'] = recent_files
        self.save_settings(config)

    def load_templates(self) -> Dict[str, Any]:
        """
        加载所有模板

        Returns:
            Dict[str, Any]: 模板字典，键为模板名称，值为模板数据
        """
        templates = {}
        for template_name in self.list_templates():
            template_data = self.load_template(template_name)
            if template_data:
                templates[template_name] = template_data
        return templates

    def save_templates(self, templates: Dict[str, Any]):
        """
        批量保存模板

        Args:
            templates: 模板字典
        """
        # 先删除所有现有模板文件
        for file_path in self.templates_dir.glob("*.json"):
            try:
                file_path.unlink()
            except Exception as e:
                print(f"删除旧模板文件失败: {e}")

        # 保存新的模板
        for name, template_data in templates.items():
            self.save_template(name, template_data)