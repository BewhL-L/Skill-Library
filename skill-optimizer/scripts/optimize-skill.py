#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skill 自动优化脚本
基于 25 轮优化经验，自动补全缺失文档、统一代码风格、生成工程化配置
v1.8.0: 统一版本号，新增路径存在性验证，完善错误处理
"""

import os
import re
import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

# 导入同目录下的类型检测器
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from skill_type_detector import SkillTypeDetector
except ImportError:
    SkillTypeDetector = None


class SkillOptimizer:
    """Skill 自动优化器"""

    def __init__(self, skill_path: str, dry_run: bool = False):
        self.skill_path = Path(skill_path)
        self.dry_run = dry_run
        self.changes = []
        self.errors = []
        # Skill 类型检测
        self.skill_type = "unknown"
        if SkillTypeDetector is not None:
            try:
                detector = SkillTypeDetector(str(self.skill_path))
                self.skill_type = detector.detect()["type"]
            except Exception:
                self.skill_type = "unknown"

    def optimize(self, only: Optional[List[str]] = None) -> Dict:
        """执行自动优化（按 Skill 类型自适应）"""
        print(f"🚀 开始优化 Skill: {self.skill_path}")
        if self.dry_run:
            print("  [预览模式] 不会实际修改文件")
        type_names = {"code-driven": "代码驱动型", "doc-only": "纯文档型", "hybrid": "混合型", "unknown": "未知类型"}
        print(f"📋 检测到 Skill 类型: {type_names.get(self.skill_type, self.skill_type)}")

        # 按类型决定默认优化范围
        if only is None:
            if self.skill_type == "doc-only":
                only = ["docs", "basic_config"]
                print("  ℹ️  纯文档型：自动跳过代码优化和高级工程化配置，只补全文档和基础配置")
            else:
                only = ["docs", "code", "config"]
        print("=" * 60)

        if "docs" in only:
            self._optimize_docs()
        if "code" in only and self.skill_type != "doc-only":
            self._optimize_code()
        if "config" in only:
            self._optimize_config()
        if "basic_config" in only:
            self._optimize_basic_config()

        return {
            "changes": self.changes,
            "errors": self.errors,
            "total_changes": len(self.changes),
            "total_errors": len(self.errors),
            "skill_type": self.skill_type,
        }

    def _write_file(self, filepath: Path, content: str, description: str):
        """写入文件（支持 dry-run）"""
        if self.dry_run:
            self.changes.append({"action": "preview", "file": str(filepath), "description": description})
            print(f"  [预览] 将创建: {filepath.name}")
        else:
            filepath.parent.mkdir(parents=True, exist_ok=True)
            filepath.write_text(content, encoding="utf-8")
            self.changes.append({"action": "create", "file": str(filepath), "description": description})
            print(f"  ✅ 创建: {filepath.name}")

    def _optimize_docs(self):
        """优化文档"""
        print("\n📚 优化文档...")

        docs_to_create = {
            "README.md": self._generate_readme(),
            "QUICKSTART.md": self._generate_quickstart(),
            "CHANGELOG.md": self._generate_changelog(),
            "FAQ.md": self._generate_faq(),
            "CONTRIBUTING.md": self._generate_contributing(),
            "SECURITY.md": self._generate_security(),
            "CODE_OF_CONDUCT.md": self._generate_code_of_conduct(),
            "INSTALLATION.md": self._generate_installation(),
            "USE-CASES.md": self._generate_use_cases(),
            "SUPPORT.md": self._generate_support(),
        }

        for filename, content in docs_to_create.items():
            filepath = self.skill_path / filename
            if not filepath.exists():
                self._write_file(filepath, content, f"创建 {filename}")
            else:
                print(f"  ⏭️  已存在，跳过: {filename}")

    def _optimize_code(self):
        """优化代码"""
        print("\n💻 优化代码...")

        # 检查并添加类型注解提示
        py_files = [f for f in self.skill_path.rglob("*.py")
                    if not any(part in [".venv", "venv", "__pycache__"] for part in f.parts)]

        for py_file in py_files:
            content = py_file.read_text(encoding="utf-8", errors="ignore")
            issues = []

            # 检查缺少返回类型注解的函数
            funcs = re.findall(r'def\s+(\w+)\s*\(([^)]*)\)\s*:', content)
            for func_name, params in funcs:
                if func_name.startswith("__"):
                    continue
                # 简单检查是否有返回类型
                pattern = rf'def\s+{func_name}\s*\([^)]*\)\s*->'
                if not re.search(pattern, content):
                    issues.append(f"函数 {func_name} 缺少返回类型注解")

            if issues:
                print(f"  ⚠️  {py_file.name}: {len(issues)} 个函数缺少类型注解")
                print(f"     建议手动添加，参考 OPTIMIZATION-GUIDE.md 第6轮")

    def _optimize_basic_config(self):
        """优化基础配置（纯文档型专用：只创建 .gitignore 和 .editorconfig）"""
        print("\n🔧 优化基础配置（纯文档型模式）...")

        basic_configs = {
            ".gitignore": self._generate_gitignore(),
            ".editorconfig": self._generate_editorconfig(),
        }

        for filename, content in basic_configs.items():
            filepath = self.skill_path / filename
            if not filepath.exists():
                self._write_file(filepath, content, f"创建 {filename}")
            else:
                print(f"  ⏭️  已存在，跳过: {filename}")

        print("  ℹ️  纯文档型跳过：pre-commit/pyproject/Makefile/requirements/CI-CD")

    def _optimize_config(self):
        """优化工程化配置（代码驱动型/混合型：创建完整工程化配置）"""
        print("\n🔧 优化工程化配置...")

        # 纯文档型使用基础配置
        if self.skill_type == "doc-only":
            self._optimize_basic_config()
            return

        configs = {
            ".gitignore": self._generate_gitignore(),
            ".editorconfig": self._generate_editorconfig(),
            ".pre-commit-config.yaml": self._generate_precommit(),
            "pyproject.toml": self._generate_pyproject(),
            "Makefile": self._generate_makefile(),
            "requirements.txt": self._generate_requirements(),
        }

        for filename, content in configs.items():
            filepath = self.skill_path / filename
            if not filepath.exists():
                self._write_file(filepath, content, f"创建 {filename}")
            else:
                print(f"  ⏭️  已存在，跳过: {filename}")

        # 创建 .github/workflows
        workflows_dir = self.skill_path / ".github" / "workflows"
        ci_file = workflows_dir / "ci.yml"
        if not ci_file.exists():
            self._write_file(ci_file, self._generate_ci(), "创建 CI/CD 配置")

    # ========== 文档生成模板 ==========

    def _get_skill_name(self) -> str:
        """从 SKILL.md 获取 Skill 名称"""
        skill_md = self.skill_path / "SKILL.md"
        if skill_md.exists():
            content = skill_md.read_text(encoding="utf-8", errors="ignore")
            match = re.search(r'name:\s*(\S+)', content)
            if match:
                return match.group(1)
        return "my-skill"

    def _generate_readme(self) -> str:
        name = self._get_skill_name()
        return f"""# {name}

> 基于工程化标准构建的专业级 Skill

## ✨ 功能特性

- 功能1
- 功能2
- 功能3

## 📦 安装

```bash
# 克隆或下载到 Skill 目录
git clone <repo-url>
```

## 🚀 快速开始

```bash
# 查看帮助
python main.py --help

# 基本使用
python main.py --input <输入> --output <输出>
```

## 📚 文档

- [快速上手](QUICKSTART.md)
- [安装指南](INSTALLATION.md)
- [常见问题](FAQ.md)
- [贡献指南](CONTRIBUTING.md)
- [更新日志](CHANGELOG.md)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License
"""

    def _generate_quickstart(self) -> str:
        return """# 快速上手

## 5 分钟快速开始

### 1. 环境准备

```bash
# 确保已安装 Python 3.8+
python --version
```

### 2. 基本使用

```bash
# 查看所有命令
python main.py --help

# 执行基本操作
python main.py --input example.txt
```

### 3. 进阶使用

参考 [完整文档](SKILL.md)

## 常见问题

见 [FAQ.md](FAQ.md)
"""

    def _generate_changelog(self) -> str:
        return f"""# 更新日志

## [1.0.0] - {datetime.now().strftime('%Y-%m-%d')}

### ✨ 新功能
- 初始版本发布
- 核心功能实现

### 📝 文档
- 添加 README
- 添加 QUICKSTART
"""

    def _generate_faq(self) -> str:
        return """# 常见问题

## 安装相关

### Q: 如何安装？
A: 参考 [INSTALLATION.md](INSTALLATION.md)

### Q: 支持哪些平台？
A: Windows / macOS / Linux

## 使用相关

### Q: 如何查看帮助？
A: 运行 `python main.py --help`

### Q: 遇到错误怎么办？
A: 查看 [DEBUGGING.md](DEBUGGING.md) 或提交 Issue

## 其他

### Q: 如何贡献？
A: 参考 [CONTRIBUTING.md](CONTRIBUTING.md)
"""

    def _generate_contributing(self) -> str:
        return """# 贡献指南

感谢你对本项目的关注！

## 开发环境搭建

```bash
# 1. Fork 并克隆
git clone <your-fork>
cd <project>

# 2. 安装依赖
pip install -r requirements-dev.txt

# 3. 安装 pre-commit
pre-commit install
```

## 提交规范

使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

- `feat:` 新功能
- `fix:` Bug 修复
- `docs:` 文档更新
- `style:` 代码格式
- `refactor:` 重构
- `test:` 测试
- `chore:` 构建/工具

## 提交流程

1. 创建功能分支
2. 提交更改
3. 运行测试
4. 提交 Pull Request

## 代码规范

- Python: PEP 8
- 类型注解: 100% 覆盖
- 测试覆盖率: ≥80%
"""

    def _generate_security(self) -> str:
        return """# 安全策略

## 报告安全漏洞

如果你发现了安全漏洞，请**不要**公开提交 Issue，而是通过以下方式联系：

- 邮件: security@example.com
- 私密 Issue

## 响应时间

- 严重漏洞: 24 小时内响应
- 一般漏洞: 7 天内响应

## 支持的版本

| 版本 | 支持状态 |
|------|---------|
| 1.x | ✅ 完全支持 |
| 0.x | ⚠️ 仅安全修复 |
"""

    def _generate_code_of_conduct(self) -> str:
        return """# 行为准则

## 我们的承诺

我们致力于为每个人提供一个友好、安全和包容的环境。

## 我们的标准

✅ **积极的行为**包括：
- 使用友好和包容的语言
- 尊重不同的观点和经验
- 优雅地接受建设性批评

❌ **不可接受的行为**包括：
- 骚扰、侮辱或贬低性评论
- 公开或私下的骚扰
- 未经许可发布他人的私人信息

## 执行

违反行为准则的行为可能导致：
- 警告
- 临时禁止
- 永久禁止

## 联系

如有问题，请联系项目维护者。
"""

    def _generate_installation(self) -> str:
        return """# 安装指南

## 系统要求

- Python 3.8+
- pip

## 安装步骤

### Windows

```bash
# 下载或克隆项目
# 进入项目目录
cd project-name

# 安装依赖
pip install -r requirements.txt
```

### macOS / Linux

```bash
git clone <repo-url>
cd project-name
pip install -r requirements.txt
```

## 验证安装

```bash
python main.py --help
```
"""

    def _generate_use_cases(self) -> str:
        return """# 使用案例

## 案例 1: 基本使用

描述基本使用场景...

## 案例 2: 进阶使用

描述进阶使用场景...

## 案例 3: 集成使用

描述与其他工具集成的场景...
"""

    def _generate_support(self) -> str:
        return """# 支持指南

## 获取帮助

### 文档
- [快速上手](QUICKSTART.md)
- [常见问题](FAQ.md)
- [调试指南](DEBUGGING.md)

### 社区
- GitHub Discussions
- Issue 追踪

## 提交 Issue

提交 Issue 时请包含：
1. 问题描述
2. 复现步骤
3. 预期行为
4. 实际行为
5. 环境信息（OS/Python版本）
"""

    # ========== 配置文件生成模板 ==========

    def _generate_gitignore(self) -> str:
        return """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
*.egg-info/
dist/
build/
*.egg

# 虚拟环境
.venv/
venv/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo

# 操作系统
.DS_Store
Thumbs.db

# 测试
.coverage
htmlcov/
.pytest_cache/

# 临时文件
*.tmp
*.log
"""

    def _generate_editorconfig(self) -> str:
        return """root = true

[*]
charset = utf-8
end_of_line = lf
indent_style = space
indent_size = 4
insert_final_newline = true
trim_trailing_whitespace = true

[*.md]
trim_trailing_whitespace = false

[*.{yml,yaml}]
indent_size = 2

[*.json]
indent_size = 2
"""

    def _generate_precommit(self) -> str:
        return """repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-added-large-files

  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        language_version: python3

  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
        args: [--max-line-length=120]
"""

    def _generate_pyproject(self) -> str:
        name = self._get_skill_name()
        return f"""[tool.black]
line-length = 120
target-version = ['py38']

[tool.isort]
profile = "black"
line_length = 120

[tool.flake8]
max-line-length = 120
extend-ignore = ['E203', 'W503']

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = "-v --tb=short"
"""

    def _generate_makefile(self) -> str:
        return """.PHONY: help install test lint format clean

help: ## 显示帮助
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\\033[36m%-20s\\033[0m %s\\n", $$1, $$2}'

install: ## 安装依赖
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

test: ## 运行测试
	python -m pytest tests/ -v

lint: ## 代码检查
	flake8 scripts/
	mypy scripts/

format: ## 代码格式化
	black scripts/
	isort scripts/

clean: ## 清理临时文件
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .coverage htmlcov
"""

    def _generate_requirements(self) -> str:
        return """# 运行时依赖
# 在此添加项目依赖
"""

    def _generate_ci(self) -> str:
        return """name: CI

on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.8', '3.9', '3.10', '3.11', '3.12']

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Lint
        run: |
          flake8 scripts/ --max-line-length=120
          mypy scripts/

      - name: Test
        run: |
          python -m pytest tests/ -v --cov=. --cov-report=xml
"""

    def print_summary(self):
        """打印优化摘要"""
        print("\n" + "=" * 60)
        print("📊 优化摘要")
        print("=" * 60)
        print(f"  总更改数: {len(self.changes)}")
        print(f"  错误数: {len(self.errors)}")

        if self.changes:
            print(f"\n更改详情:")
            for change in self.changes:
                icon = "📝" if change["action"] == "create" else "👁️"
                print(f"  {icon} [{change['action']}] {change['description']}")

        if self.errors:
            print(f"\n错误:")
            for error in self.errors:
                print(f"  ❌ {error}")

        print(f"\n{'=' * 60}")


def main():
    parser = argparse.ArgumentParser(description="Skill 自动优化工具 v1.8.0（支持多类型 Skill 自适应优化）")
    parser.add_argument("--path", required=True, help="Skill 目录路径")
    parser.add_argument("--auto", action="store_true", help="自动执行所有优化")
    parser.add_argument("--dry-run", action="store_true", help="预览模式，不实际修改")
    parser.add_argument("--only", nargs="+", choices=["docs", "code", "config", "basic_config"],
                        help="只优化指定部分（纯文档型推荐 docs+basic_config）")
    args = parser.parse_args()

    if not os.path.exists(args.path):
        print(f"❌ 错误: 路径不存在 - {args.path}")
        return

    optimizer = SkillOptimizer(args.path, dry_run=args.dry_run)
    result = optimizer.optimize(only=args.only)
    optimizer.print_summary()


if __name__ == "__main__":
    main()
