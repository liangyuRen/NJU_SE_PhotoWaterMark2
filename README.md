# 📸 Photo Watermark 2

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%2010%2B-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Release](https://img.shields.io/github/v/release/liangyuRen/NJU_SE_PhotoWaterMark2)

**功能强大的桌面图片水印处理工具**

南京大学软件工程课程 - 大模型辅助开发作业

[📥 下载可执行文件](https://github.com/liangyuRen/NJU_SE_PhotoWaterMark2/releases/latest) | [📖 使用指南](#-使用指南) | [🔧 开发文档](#-开发指南)

</div>

---

## 🌟 项目亮点

### ✨ 核心功能
- **🎨 双重水印支持** - 文本水印和图片水印，满足不同需求
- **🖱️ 拖拽式定位** - 鼠标直接拖拽调整水印位置，所见即所得
- **👁️ 实时预览** - 所有调整立即显示效果，无需等待
- **📦 批量处理** - 一键处理多张图片，提升工作效率
- **💾 模板系统** - 保存和重用水印配置，快速应用到新项目

### 🔧 技术特色
- **🚀 无需安装** - 单文件可执行程序，双击即用
- **🎯 多格式支持** - JPG、PNG、BMP、TIFF 全格式兼容
- **⚡ 高性能处理** - 多线程优化，处理速度快
- **🎨 用户友好** - 直观的图形界面，零学习成本

---

## 🎯 功能演示

### 主界面概览
```
┌─────────────────────────────────────────────────────────────────┐
│ 📁 文件  🎨 水印  📤 导出  🔧 工具  ❓ 帮助                      │
├─────────────┬───────────────────────────┬─────────────────────────┤
│   图片列表   │       预览区域              │      水印设置面板        │
│             │                           │                        │
│ 📂 image1.jpg │  ┌─────────────────────┐  │ 🏷️ 水印类型: [文本▼]    │
│ 📂 image2.png │  │                     │  │ 📝 文本内容: [        ] │
│ 📂 image3.bmp │  │     图片预览区域      │  │ 🎨 颜色: [⚫] 透明度: 50% │
│               │  │                     │  │ 📍 位置: [右下角▼]      │
│ [+ 导入图片]   │  │   [水印拖拽指示器]   │  │ 📐 偏移: X:20 Y:20     │
│ [🗑️ 清空列表] │  │                     │  │ ✅ [显示预览]           │
│               │  └─────────────────────┘  │ 🎯 [显示位置指示器]     │
│               │                           │ 💾 [保存模板] [加载]    │
└─────────────┴───────────────────────────┴─────────────────────────┤
│ 🔄 处理状态: 就绪 | 📊 已处理: 0/0 | ⏱️ 用时: 0s | 💾 内存: 45MB   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 快速开始

### 方式一：下载可执行文件（推荐）

1. **下载程序**
   ```
   访问: https://github.com/liangyuRen/NJU_SE_PhotoWaterMark2/releases/latest
   下载: PhotoWatermark2.exe (约29MB)
   ```

2. **运行程序**
   ```
   无需安装，双击 PhotoWatermark2.exe 即可运行
   首次启动可能需要3-5秒加载时间
   ```

3. **系统要求**
   - Windows 10/11 (64位)
   - 内存: 至少 512MB RAM
   - 存储: 100MB 可用空间

### 方式二：从源码运行

1. **环境准备**
   ```bash
   # 确保安装了Python 3.8+
   python --version

   # 克隆仓库
   git clone https://github.com/liangyuRen/NJU_SE_PhotoWaterMark2.git
   cd NJU_SE_PhotoWaterMark2
   ```

2. **安装依赖**
   ```bash
   # 安装核心依赖
   pip install -r requirements.txt

   # 或者只安装运行必需的包
   pip install Pillow>=9.0.0
   ```

3. **启动应用**
   ```bash
   # 方式1: 直接运行
   python run.py

   # 方式2: 模块化运行
   python -m photo_watermark.main
   ```

---

## 📖 使用指南

### 🎯 基础操作流程

#### 1️⃣ 导入图片
- **单张导入**: 点击 `文件 → 导入图片` 或按 `Ctrl+O`
- **批量导入**: 在文件选择器中按住 `Ctrl` 多选图片
- **文件夹导入**: 点击 `文件 → 导入文件夹`
- **拖拽导入**: 直接将图片拖拽到程序窗口（暂不支持）

#### 2️⃣ 配置水印

**文本水印设置:**
```
📝 文本内容: "© 2024 我的版权"
🎨 字体样式: Arial, 36号, 加粗
🌈 颜色透明度: 白色, 透明度 70%
📐 位置设置: 右下角, X偏移 20px, Y偏移 20px
🔄 旋转角度: -15度 (可选)
```

**图片水印设置:**
```
🖼️ 水印图片: 选择 PNG 透明图片文件
📏 尺寸调整: 宽度 200px, 等比缩放
📍 位置设置: 右下角, 边距 30px
👻 透明度: 80% (与背景融合)
```

#### 3️⃣ 实时预览与调整

- **预览开关**: 勾选 `✅ 显示水印预览` 查看效果
- **位置指示器**: 勾选 `🎯 显示位置指示器` 启用拖拽模式
- **拖拽调整**: 鼠标直接拖动水印到理想位置
- **实时反馈**: 所有调整立即在预览中显示

#### 4️⃣ 导出图片

**单张导出:**
```
1. 在图片列表中选择要导出的图片
2. 点击 "导出当前图片" 或按 Ctrl+S
3. 选择保存位置和文件名
4. 程序自动添加水印并保存
```

**批量导出:**
```
1. 点击 "批量导出" 或按 Ctrl+B
2. 选择输出文件夹
3. 程序自动处理所有图片
4. 显示处理进度和完成状态
```

### 🎨 高级功能详解

#### 💾 模板管理系统

**保存模板:**
1. 配置好所有水印参数
2. 点击 `水印 → 保存模板`
3. 输入模板名称，如 "公司标准水印"
4. 模板自动保存到配置文件

**加载模板:**
1. 点击 `水印 → 加载模板`
2. 从列表中选择已保存的模板
3. 所有参数自动应用
4. 注意：加载模板后需手动开启预览

**管理模板:**
- 删除模板: `水印 → 管理模板 → 选择 → 删除`
- 重命名模板: 删除旧模板后重新保存新名称

#### 🎯 精确位置控制

**九宫格定位:**
```
┌─────┬─────┬─────┐
│ 左上  │ 上中  │ 右上  │
├─────┼─────┼─────┤
│ 左中  │ 正中  │ 右中  │
├─────┼─────┼─────┤
│ 左下  │ 下中  │ 右下  │
└─────┴─────┴─────┘
```

**自定义偏移:**
- X偏移: 正值向右，负值向左
- Y偏移: 正值向下，负值向上
- 边距: 与图片边缘的距离

**鼠标拖拽:**
1. 启用 "显示位置指示器"
2. 鼠标指向水印区域
3. 按住左键拖动到目标位置
4. 释放鼠标完成调整

#### 📊 导出设置详解

**格式转换:**
- 原格式保持: 与输入图片格式相同
- PNG: 支持透明度，适合网络使用
- JPEG: 文件较小，适合打印
- BMP: Windows标准格式
- TIFF: 高质量，适合专业用途

**质量控制:**
- JPEG质量: 1-100，推荐85-95
- PNG压缩: 自动优化
- 文件命名: 自定义前缀/后缀

---

## ⚙️ 功能特色

### 🎨 水印类型对比

| 功能特性 | 文本水印 | 图片水印 |
|---------|---------|---------|
| **内容自定义** | ✅ 任意文字内容 | ✅ 任意图片文件 |
| **透明度控制** | ✅ 0-100% 可调 | ✅ 0-100% 可调 |
| **位置调整** | ✅ 九宫格+偏移 | ✅ 九宫格+偏移 |
| **拖拽定位** | ✅ 鼠标直接拖拽 | ✅ 鼠标直接拖拽 |
| **旋转角度** | ✅ -180° ~ +180° | ❌ 暂不支持 |
| **颜色设置** | ✅ RGB颜色选择 | ➖ 使用原图颜色 |
| **字体选择** | ✅ 系统字体 | ➖ 不适用 |
| **阴影效果** | ✅ 可选阴影 | ➖ 不适用 |

### 📁 支持格式详情

| 格式 | 输入支持 | 输出支持 | 透明度 | 推荐用途 |
|------|---------|---------|--------|----------|
| **JPEG** | ✅ | ✅ | ❌ | 照片、网页图片 |
| **PNG** | ✅ | ✅ | ✅ | 网页图标、透明图片 |
| **BMP** | ✅ | ✅ | ❌ | Windows系统图片 |
| **TIFF** | ✅ | ✅ | ✅ | 印刷、专业摄影 |

### 🚀 性能优化特性

- **内存管理**: 大图片自动压缩预览，节省内存
- **多线程处理**: 批量操作使用并行处理
- **智能缓存**: 频繁操作的图片自动缓存
- **进度显示**: 实时显示处理进度和剩余时间

---

## 🎮 快捷键参考

| 功能 | Windows快捷键 | 描述 |
|------|---------------|------|
| **导入图片** | `Ctrl + O` | 打开文件选择器导入图片 |
| **导出当前** | `Ctrl + S` | 导出当前选中的图片 |
| **批量导出** | `Ctrl + B` | 批量导出所有图片 |
| **重置水印** | `Ctrl + R` | 重置所有水印设置为默认值 |
| **清空列表** | `Delete` | 清空图片列表 |
| **保存模板** | `Ctrl + T` | 快速保存当前水印配置 |
| **程序帮助** | `F1` | 显示帮助信息 |
| **退出程序** | `Alt + F4` | 安全退出程序 |

---

## 🔧 开发指南

### 🏗️ 项目架构

```
photo_watermark/
├── 📁 core/                    # 🎯 核心业务逻辑
│   ├── image_processor.py      #   📸 图像处理引擎
│   ├── watermark.py           #   🏷️ 水印配置和算法
│   └── batch_processor.py     #   ⚡ 批量处理器
├── 📁 gui/                     # 🖥️ 用户界面模块
│   ├── main_window.py         #   🏠 主窗口和布局
│   ├── image_panel.py         #   🖼️ 图片列表和预览面板
│   ├── watermark_panel.py     #   ⚙️ 水印设置面板
│   ├── control_panel.py       #   🎛️ 控制按钮面板
│   └── export_panel.py        #   📤 导出设置面板
├── 📁 utils/                   # 🔧 工具和配置
│   └── app_config.py          #   ⚙️ 配置文件管理
└── 📄 main.py                  # 🚀 程序主入口
```

### 🛠️ 开发环境设置

**1. 环境要求:**
```bash
Python 3.8+
pip 21.0+
Git 2.25+
```

**2. 克隆和依赖:**
```bash
# 克隆仓库
git clone https://github.com/liangyuRen/NJU_SE_PhotoWaterMark2.git
cd NJU_SE_PhotoWaterMark2

# 创建虚拟环境 (推荐)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt
```

**3. 开发工具配置:**
```bash
# 安装开发工具
pip install black flake8 pytest

# 代码格式化
black photo_watermark/

# 代码检查
flake8 photo_watermark/

# 运行测试
pytest tests/
```

### 📦 构建可执行文件

**使用构建脚本:**
```bash
# Windows 批处理脚本
.\build.bat

# 或 Python 脚本
python build.py
```

**手动构建:**
```bash
# 安装 PyInstaller
pip install pyinstaller

# 构建命令
pyinstaller --onefile --windowed \
    --name "PhotoWatermark2" \
    --add-data "photo_watermark;photo_watermark" \
    --hidden-import "PIL._tkinter_finder" \
    run.py

# 输出文件位置: dist/PhotoWatermark2.exe
```

### 🐛 调试指南

**常见问题解决:**

1. **程序启动失败**
   ```
   检查 Python 版本 >= 3.8
   确认依赖包已安装: pip install Pillow
   ```

2. **图片加载失败**
   ```
   检查图片格式是否支持
   确认文件路径不包含特殊字符
   ```

3. **水印显示异常**
   ```
   检查字体文件是否存在
   确认水印图片路径正确
   ```

4. **导出文件损坏**
   ```
   检查目标文件夹写权限
   确认磁盘空间足够
   ```

---

## 🔍 技术实现详解

### 🖼️ 图像处理流程

```python
# 伪代码示例
def process_image_with_watermark(image_path, watermark_config):
    # 1. 加载原始图片
    original_image = Image.open(image_path)

    # 2. 创建水印图层
    watermark_layer = create_watermark(watermark_config)

    # 3. 计算水印位置
    position = calculate_position(original_image.size, watermark_config)

    # 4. 合成图片
    result = composite_images(original_image, watermark_layer, position)

    # 5. 导出最终图片
    return result
```

### 🎨 水印算法核心

**位置计算算法:**
```python
def calculate_watermark_position(image_size, watermark_size, layout):
    img_w, img_h = image_size
    wm_w, wm_h = watermark_size

    # 九宫格基础位置
    positions = {
        'top_left': (0, 0),
        'top_center': ((img_w - wm_w) // 2, 0),
        'top_right': (img_w - wm_w, 0),
        'center_left': (0, (img_h - wm_h) // 2),
        'center': ((img_w - wm_w) // 2, (img_h - wm_h) // 2),
        'center_right': (img_w - wm_w, (img_h - wm_h) // 2),
        'bottom_left': (0, img_h - wm_h),
        'bottom_center': ((img_w - wm_w) // 2, img_h - wm_h),
        'bottom_right': (img_w - wm_w, img_h - wm_h)
    }

    # 应用偏移和边距
    base_x, base_y = positions[layout.position]
    final_x = base_x + layout.x_offset
    final_y = base_y + layout.y_offset

    return (final_x, final_y)
```

---

## 📋 系统需求

### 💻 运行环境

| 项目 | 最低要求 | 推荐配置 |
|------|---------|----------|
| **操作系统** | Windows 10 (64位) | Windows 11 |
| **处理器** | Intel Core i3 / AMD Ryzen 3 | Intel Core i5 或更高 |
| **内存** | 4GB RAM | 8GB RAM 或更多 |
| **存储** | 500MB 可用空间 | 2GB 可用空间 |
| **显示器** | 1024×768 分辨率 | 1920×1080 或更高 |
| **网络** | 无需网络连接 | - |

### 📊 性能指标

| 操作类型 | 处理速度 | 内存占用 |
|---------|---------|----------|
| **单张图片预览** | < 1秒 | ~50MB |
| **批量处理 (100张)** | 2-5分钟 | ~200MB |
| **大尺寸图片 (4K)** | 2-3秒 | ~100MB |
| **程序启动时间** | 3-5秒 | - |

---

## 🐛 问题排查

### ❓ 常见问题

<details>
<summary><strong>Q: 程序无法启动，显示缺少 DLL 文件？</strong></summary>

**A:** 这通常是因为系统缺少 Visual C++ 运行库：
1. 下载并安装 [Microsoft Visual C++ 2019 Redistributable](https://support.microsoft.com/zh-cn/topic/the-latest-supported-visual-c-downloads-2647da03-1eea-4433-9aff-95f26a218cc0)
2. 重启计算机后再次运行程序
3. 如果问题仍然存在，尝试以管理员身份运行
</details>

<details>
<summary><strong>Q: 水印拖拽后又回到原来位置了？</strong></summary>

**A:** 这个问题在 v1.2.0 版本已修复：
1. 确保使用最新版本的程序
2. 拖拽水印后，确保松开鼠标
3. 拖拽完成后，程序会自动保存新位置
</details>

<details>
<summary><strong>Q: 保存的模板为什么会自动应用到所有图片？</strong></summary>

**A:** 这个问题在 v1.2.0 版本已修复：
1. 加载模板后，需要手动开启"显示水印预览"
2. 模板只保存设置，不会自动启用预览
3. 用户可以自主选择是否应用水印
</details>

<details>
<summary><strong>Q: 导出的图片质量很差？</strong></summary>

**A:** 检查以下设置：
1. JPEG 质量设置是否过低（推荐85-95）
2. 是否选择了合适的输出格式
3. 原图片分辨率是否足够高
4. 水印透明度设置是否合适
</details>

<details>
<summary><strong>Q: 批量处理时程序卡住不动？</strong></summary>

**A:** 处理大量图片时请耐心等待：
1. 查看状态栏的处理进度
2. 大图片或大量图片需要更多时间
3. 确保系统内存足够
4. 避免同时运行其他大型程序
</details>

### 🔧 故障诊断

**性能问题:**
- 关闭不必要的预览功能
- 减少同时处理的图片数量
- 关闭其他占用内存的程序

**兼容性问题:**
- 确保 Windows 版本为 10 或更高
- 更新显卡驱动程序
- 检查是否有安全软件阻止运行

---

## 🎯 版本历史

### 🔄 更新记录

#### 📅 v1.2.0 (2025-01-25) - 当前版本
**🐛 重要修复:**
- 修复水印拖拽完成后位置重置的问题
- 修复模板加载后自动应用到所有图片的问题
- 改进导出时的格式处理逻辑

**✨ 新增功能:**
- 增强图片格式支持 (BMP, TIFF)
- 添加导出设置面板
- 改进用户界面布局

**⚡ 性能优化:**
- 优化水印拖拽响应速度
- 改进内存使用效率
- 增强错误处理机制

#### 📅 v1.1.0 (2025-01-20)
**✨ 主要功能:**
- 实现清空列表和重置水印功能
- 优化位置设置逻辑
- 修复GUI输入验证问题

#### 📅 v1.0.0 (2025-01-15) - 初始版本
**🚀 核心功能:**
- 基础水印功能实现
- 文本和图片水印支持
- 批量处理功能
- 模板管理系统

---

## 📜 许可证

本项目采用 [MIT License](LICENSE) 开源许可证。

```
MIT License

Copyright (c) 2025 南京大学软件工程课程

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 🤝 贡献与支持

### 💡 贡献代码
1. **Fork** 本仓库到你的账户
2. **创建** 功能分支 (`git checkout -b feature/AmazingFeature`)
3. **提交** 你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. **推送** 到分支 (`git push origin feature/AmazingFeature`)
5. **创建** Pull Request

### 🐛 报告问题
- 在 [Issues](https://github.com/liangyuRen/NJU_SE_PhotoWaterMark2/issues) 页面报告 Bug
- 详细描述问题现象和重现步骤
- 附上系统环境信息和错误截图

### 💭 功能建议
- 在 Issues 中提出新功能建议
- 描述功能用途和预期效果
- 欢迎讨论实现方案

---

## 👥 作者与致谢

### 👨‍💻 开发团队
- **课程**: 南京大学软件工程
- **项目**: 大模型辅助软件工程作业2
- **技术支持**: Claude AI 辅助开发

### 🙏 特别致谢
- [**Pillow (PIL)**](https://pillow.readthedocs.io/) - 强大的Python图像处理库
- [**PyInstaller**](https://pyinstaller.readthedocs.io/) - Python应用打包工具
- [**Tkinter**](https://docs.python.org/3/library/tkinter.html) - Python标准GUI库
- [**南京大学软件学院**](https://software.nju.edu.cn/) - 课程指导与支持

---

## 📞 联系方式

- **项目仓库**: https://github.com/liangyuRen/NJU_SE_PhotoWaterMark2
- **问题反馈**: [GitHub Issues](https://github.com/liangyuRen/NJU_SE_PhotoWaterMark2/issues)
- **最新发布**: [GitHub Releases](https://github.com/liangyuRen/NJU_SE_PhotoWaterMark2/releases)

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给个星标支持！ ⭐**

</div>