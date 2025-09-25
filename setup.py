"""
Photo Watermark 2 安装脚本
"""

from setuptools import setup, find_packages
from pathlib import Path

# 读取README文件
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# 读取版本信息
version = {}
with open("photo_watermark/__init__.py") as fp:
    exec(fp.read(), version)

setup(
    name="photo-watermark-2",
    version=version['__version__'],
    description="图片水印处理应用程序",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="NJU SE Course",
    author_email="",
    url="https://github.com/your-username/NJU_SE_PhotoWaterMark2",

    packages=find_packages(),

    install_requires=[
        "Pillow>=9.0.0",
    ],

    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'black>=22.0.0',
            'flake8>=4.0.0',
        ],
        'pyqt5': ['PyQt5>=5.15.0'],
        'pyqt6': ['PyQt6>=6.2.0'],
    },

    python_requires='>=3.7',

    entry_points={
        'console_scripts': [
            'photo-watermark=photo_watermark.main:main',
        ],
    },

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],

    keywords="watermark image processing desktop application",

    package_data={
        'photo_watermark': [
            'resources/*',
        ],
    },

    include_package_data=True,
)