# 如何创建 GitHub Release

## 自动化脚本
GitHub CLI 不可用时，请按照以下步骤手动创建 Release：

## 手动创建 Release 步骤：

1. **访问 GitHub 仓库页面**
   - 打开 https://github.com/liangyuRen/NJU_SE_PhotoWaterMark2

2. **创建新 Release**
   - 点击右侧的 "Releases" 或 "Create a new release"
   - 或直接访问：https://github.com/liangyuRen/NJU_SE_PhotoWaterMark2/releases/new

3. **填写 Release 信息**
   - **Tag version**: `v1.2.0`
   - **Release title**: `Photo Watermark 2 v1.2.0 - Windows 可执行版本`
   - **Description**: 复制 `RELEASE_NOTES.md` 的内容

4. **上传可执行文件**
   - 拖拽或点击上传 `dist/PhotoWatermark2.exe` 文件
   - 文件大小约 29MB

5. **发布**
   - 确认信息无误后点击 "Publish release"

## 文件信息
- **可执行文件位置**: `dist/PhotoWatermark2.exe`
- **文件大小**: 约 29MB
- **系统要求**: Windows 10/11 (64位)
- **发布说明**: 详见 `RELEASE_NOTES.md`

## 验证
发布成功后，用户可以通过以下链接下载：
https://github.com/liangyuRen/NJU_SE_PhotoWaterMark2/releases/latest

---
**重要提示**: 请确保在发布前测试可执行文件能够正常运行！