# 常见问题

## 安装相关

### Q: 如何安装本 Skill？
A: 将本文件夹复制到豆包用户技能目录，重启豆包即可。

### Q: 支持哪些操作系统？
A: Windows / macOS / Linux 均支持。

### Q: 需要安装 Python 吗？
A: 如果只在豆包中使用，不需要。如果使用命令行脚本，需要 Python 3.8+。

## 使用相关

### Q: 如何查看所有命令？
A: 运行 `python main.py --help` 或 `python kb.py info`。

### Q: 命令执行失败怎么办？
A: 1. 检查参数是否正确 2. 查看错误信息 3. 参考 DEBUGGING.md 4. 提交 Issue

### Q: 如何批量处理？
A: 使用 `--list` 参数传入 JSON/YAML 文件，或编写批处理脚本。

## 配置相关

### Q: 如何自定义模板？
A: 修改 templates/ 目录下的模板文件，或使用 `--template` 参数指定自定义模板。

### Q: 配置文件在哪里？
A: 项目根目录下的 config.yaml 或 pyproject.toml。

## 常见错误

### Q: 提示 "ModuleNotFoundError"
A: 运行 `pip install -r requirements.txt` 安装依赖。

### Q: 提示 "Permission denied"
A: 检查文件权限，或使用管理员权限运行。

### Q: 中文乱码怎么办？
A: 确保文件编码为 UTF-8，Windows 用户可设置环境变量 `PYTHONIOENCODING=utf-8`。

## 其他

### Q: 如何贡献代码？
A: 参考 CONTRIBUTING.md。

### Q: 如何报告 Bug？
A: 在 GitHub 提交 Issue，包含复现步骤和环境信息。

### Q: 有商业支持吗？
A: 联系项目维护者获取商业支持选项。
