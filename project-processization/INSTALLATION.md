# 安装指南

## 运行时（仅使用脚本）

脚本只用 Python 标准库，**无需 pip 安装**：

1. 安装 Python 3.8 或更高版本，命令行确认：
   ```bash
   python --version
   ```
2. 让本 Skill 位于工作区的 `.user_skills/项目流程化/` 目录下（随 Skill 加载机制自动识别）。
3. 直接运行脚本：
   ```bash
   python scripts/scan_project_facts.py --help
   ```

## 开发 / 测试环境（可选）

如需运行测试或参与开发：

```bash
# 建议使用虚拟环境
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# Linux / macOS
source .venv/bin/activate

# 安装开发依赖
pip install -e ".[dev]"
# 或仅安装测试依赖
pip install pytest pytest-cov ruff
```

## 验证安装

```bash
python -m py_compile scripts/*.py     # 语法编译
python -m pytest tests -v             # 运行 32 个测试
```

## 平台说明

- **Windows**：在 PowerShell 7 中运行；若控制台中文显示乱码，是 GBK 控制台编码问题，
  脚本写出的文件本身为 UTF-8，不受影响。建议执行 `chcp 65001` 或用 Python 读取结果文件。
- **Linux / macOS**：直接运行；Makefile 提供 `make test / cov / lint / audit`。

## 卸载

直接删除 Skill 目录即可；脚本不会写入系统或修改项目外的文件（仅在你指定的项目内生成报告）。
