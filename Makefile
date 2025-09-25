# Photo Watermark 2 Makefile

.PHONY: help install install-dev run test clean build package format lint

# 默认目标
help:
	@echo "Photo Watermark 2 - 可用命令:"
	@echo "  install      - 安装基本依赖"
	@echo "  install-dev  - 安装开发依赖"
	@echo "  run          - 运行应用程序"
	@echo "  test         - 运行测试"
	@echo "  clean        - 清理构建文件"
	@echo "  build        - 构建项目"
	@echo "  package      - 打包为可执行文件"
	@echo "  format       - 格式化代码"
	@echo "  lint         - 代码检查"

# 安装基本依赖
install:
	pip install -r requirements.txt

# 安装开发依赖
install-dev:
	pip install -r requirements.txt
	pip install -e .[dev]

# 运行应用程序
run:
	python -m photo_watermark.main

# 运行测试
test:
	pytest tests/ -v

# 清理构建文件
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

# 构建项目
build: clean
	python setup.py sdist bdist_wheel

# 打包为可执行文件
package: clean
	pyinstaller --onefile --windowed --name PhotoWatermark2 photo_watermark/main.py
	@echo "可执行文件已生成到 dist/ 目录"

# Windows 打包 (如果在Windows上运行)
package-win: clean
	pyinstaller --onefile --windowed --name PhotoWatermark2.exe photo_watermark/main.py
	@echo "Windows可执行文件已生成到 dist/ 目录"

# 格式化代码
format:
	black photo_watermark/ tests/

# 代码检查
lint:
	flake8 photo_watermark/ tests/

# 创建虚拟环境
venv:
	python -m venv venv
	@echo "虚拟环境已创建，请运行以下命令激活:"
	@echo "Windows: venv\\Scripts\\activate"
	@echo "Linux/Mac: source venv/bin/activate"

# 开发模式安装
dev-setup: venv install-dev
	@echo "开发环境设置完成"

# 完整的开发流程
dev: format lint test
	@echo "开发流程检查完成"