# Photo Watermark 2

南京大学大模型辅助软件工程课程作业2 - 图片水印处理应用

## 项目简介

Photo Watermark 2 是一款功能丰富的桌面图片水印处理工具，支持为单张或批量图片添加文本和图片水印。该应用提供直观的用户界面、实时预览功能和灵活的水印配置选项。

## 主要功能

### 🖼️ 文件处理
- **多格式支持**: JPEG、PNG、BMP、TIFF
- **灵活导入**: 单张导入、批量选择、文件夹导入、拖拽导入
- **智能导出**: 防覆盖机制、自定义命名规则、质量控制

### 🏷️ 水印功能
- **文本水印**: 自定义文字、字体、颜色、透明度、阴影效果
- **图片水印**: 支持PNG透明图片、自由缩放、透明度调节
- **实时预览**: 所有调整立即显示效果

### 📍 位置控制
- **九宫格布局**: 一键定位到预设位置
- **手动拖拽**: 鼠标直接调整水印位置
- **精确控制**: 数值输入、旋转角度、边距设置

### 💾 配置管理
- **模板系统**: 保存和加载水印配置模板
- **设置持久化**: 自动保存用户偏好设置
- **批量处理**: 多线程处理，进度显示

## 技术架构

### 核心技术栈
- **语言**: Python 3.7+
- **GUI框架**: Tkinter (内置)
- **图像处理**: Pillow (PIL)
- **配置管理**: JSON
- **打包工具**: PyInstaller

### 项目结构
```
photo_watermark/
├── core/                    # 核心功能模块
│   ├── image_processor.py   # 图像处理器
│   ├── watermark.py         # 水印配置和计算
│   └── batch_processor.py   # 批量处理器
├── gui/                     # 用户界面模块
│   ├── main_window.py       # 主窗口
│   ├── image_panel.py       # 图片面板
│   ├── watermark_panel.py   # 水印设置面板
│   └── control_panel.py     # 控制面板
├── utils/                   # 工具模块
│   └── app_config.py        # 配置管理
└── main.py                  # 程序入口
```

## 快速开始

### 环境要求
- Python 3.7 或更高版本
- 支持的操作系统: Windows 10+, macOS 10.14+

### 安装依赖
```bash
# 克隆项目
git clone https://github.com/your-username/NJU_SE_PhotoWaterMark2.git
cd NJU_SE_PhotoWaterMark2

# 安装依赖
pip install -r requirements.txt

# 或使用开发环境安装
make install-dev
```

### 运行应用
```bash
# 方式1: 直接运行
python -m photo_watermark.main

# 方式2: 使用Makefile
make run

# 方式3: 安装后运行
pip install -e .
photo-watermark
```

### 打包可执行文件
```bash
# 生成单文件可执行程序
make package

# Windows专用打包
make package-win

# 打包完成后在dist/目录找到可执行文件
```

## 使用指南

### 基本操作流程

1. **导入图片**
   - 点击"导入图片"按钮选择文件
   - 或直接将图片拖拽到应用窗口
   - 支持批量导入整个文件夹

2. **设置水印**
   - 选择水印类型（文本/图片）
   - 调整水印内容和样式
   - 使用九宫格或手动设置位置

3. **实时预览**
   - 在预览区域查看效果
   - 点击图片列表切换不同图片
   - 所有调整立即生效

4. **导出图片**
   - 单张导出：选择图片后点击"导出当前"
   - 批量导出：点击"批量导出"选择输出文件夹

### 高级功能

- **模板管理**: 水印菜单 → 保存/加载模板
- **批量处理**: 支持多线程并发处理
- **格式转换**: 导出时可转换图片格式
- **质量控制**: JPEG格式支持质量调节

## 开发指南

### 开发环境设置
```bash
# 创建虚拟环境
make venv

# 激活虚拟环境 (Windows)
venv\Scripts\activate

# 激活虚拟环境 (Linux/Mac)
source venv/bin/activate

# 安装开发依赖
make install-dev
```

### 代码规范
```bash
# 代码格式化
make format

# 代码检查
make lint

# 运行测试
make test

# 完整开发流程检查
make dev
```

### 项目构建
```bash
# 清理构建文件
make clean

# 构建项目
make build
```

## 系统要求

### 最低配置
- **操作系统**: Windows 10 / macOS 10.14 / Linux
- **内存**: 512MB RAM
- **存储**: 100MB 可用空间
- **Python**: 3.7+ (开发环境)

### 推荐配置
- **内存**: 2GB RAM 或更多
- **存储**: 1GB 可用空间
- **显示器**: 1024x768 或更高分辨率

## 软件需求规格

详细的功能需求和技术规格请参考 [软件需求规格说明书 (SRS.md)](./SRS.md)

## 许可证

本项目采用 MIT 许可证 - 详情请查看 [LICENSE](LICENSE) 文件

## 贡献指南

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 作者

- **课程**: 南京大学软件工程课程
- **项目**: 大模型辅助软件工程作业2

## 致谢

- [Pillow](https://pillow.readthedocs.io/) - Python图像处理库
- [PyInstaller](https://pyinstaller.readthedocs.io/) - Python打包工具
- [南京大学软件学院](https://software.nju.edu.cn/) - 课程支持

## 版本历史

- **v1.0.0** - 初始版本
  - 基础水印功能
  - 文本和图片水印支持
  - 批量处理功能
  - 模板管理系统

---

**注意**: 这是一个学术项目，仅用于学习和教育目的。