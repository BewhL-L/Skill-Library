#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skill 文档生成脚本
自动解析 Python 脚本，生成 API 参考文档、使用示例等
v1.8.0: 统一版本号，新增路径存在性验证，完善错误处理
"""

import os
import re
import ast
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Tuple, Optional

# 导入同目录下的类型检测器
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from skill_type_detector import SkillTypeDetector
except ImportError:
    SkillTypeDetector = None


class DocGenerator:
    """文档生成器"""

    def __init__(self, skill_path: str):
        self.skill_path = Path(skill_path)
        self.generated = []
        # Skill 类型检测
        self.skill_type = "unknown"
        if SkillTypeDetector is not None:
            try:
                detector = SkillTypeDetector(str(self.skill_path))
                self.skill_type = detector.detect()["type"]
            except Exception:
                self.skill_type = "unknown"

    def generate(self, doc_type: str = "all"):
        """生成文档（按 Skill 类型自适应）"""
        print(f"📝 开始生成文档: {self.skill_path}")
        print("=" * 60)
        print(f"📋 Skill 类型: {self.skill_type}")

        # 纯文档型跳过 API 和架构文档
        is_doc_only = self.skill_type == "doc-only"
        if is_doc_only:
            print("ℹ️  纯文档型：自动跳过 API 文档和架构文档（无代码）")

        if doc_type in ["all", "api"]:
            if is_doc_only:
                print("\n🔌 API 参考文档（跳过 - 纯文档型无代码）")
            else:
                self._generate_api_docs()
        if doc_type in ["all", "faq"]:
            self._generate_faq()
        if doc_type in ["all", "examples"]:
            self._generate_examples()
        if doc_type in ["all", "architecture"]:
            if is_doc_only:
                print("\n🏗️  架构文档（跳过 - 纯文档型无代码架构）")
            else:
                self._generate_architecture()

        return self.generated

    def _get_python_files(self) -> List[Path]:
        """获取所有 Python 文件"""
        return [f for f in self.skill_path.rglob("*.py")
                if not any(part in [".venv", "venv", "__pycache__", "tests"] for part in f.parts)]

    def _parse_functions(self, filepath: Path) -> List[Dict]:
        """解析 Python 文件中的函数"""
        functions = []
        try:
            content = filepath.read_text(encoding="utf-8", errors="ignore")
            tree = ast.parse(content)

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # 获取参数
                    args = []
                    for arg in node.args.args:
                        arg_info = arg.arg
                        if arg.annotation:
                            arg_info += f": {ast.unparse(arg.annotation)}"
                        args.append(arg_info)

                    # 获取返回类型
                    returns = ast.unparse(node.returns) if node.returns else "None"

                    # 获取 docstring
                    docstring = ast.get_docstring(node) or ""

                    functions.append({
                        "name": node.name,
                        "args": args,
                        "returns": returns,
                        "docstring": docstring,
                        "line": node.lineno,
                        "file": filepath.name
                    })
        except Exception as e:
            print(f"  ⚠️  解析 {filepath.name} 失败: {e}")

        return functions

    def _generate_api_docs(self):
        """生成 API 参考文档"""
        print("\n📚 生成 API 参考文档...")

        py_files = self._get_python_files()
        all_functions = []

        for py_file in py_files:
            funcs = self._parse_functions(py_file)
            all_functions.extend(funcs)

        if not all_functions:
            print("  ⚠️  未找到可解析的函数")
            return

        # 按文件分组
        by_file: Dict[str, List] = {}
        for func in all_functions:
            by_file.setdefault(func["file"], []).append(func)

        # 生成文档
        content = f"""# API 参考文档

> 自动生成于 {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}

## 📋 函数索引

共 {len(all_functions)} 个函数，分布在 {len(by_file)} 个文件中。

| 文件 | 函数数 |
|------|--------|
"""
        for filename, funcs in by_file.items():
            content += f"| [{filename}](#{filename.replace('.', '')}) | {len(funcs)} |\n"

        content += "\n---\n"

        # 详细函数文档
        for filename, funcs in by_file.items():
            content += f"\n## {filename}\n\n"
            for func in funcs:
                args_str = ", ".join(func["args"])
                content += f"### `{func['name']}({args_str}) -> {func['returns']}`\n\n"
                if func["docstring"]:
                    content += f"{func['docstring']}\n\n"
                else:
                    content += "*暂无文档说明*\n\n"
                content += "**参数:**\n"
                if func["args"]:
                    for arg in func["args"]:
                        content += f"- `{arg}`\n"
                else:
                    content += "- 无\n"
                content += f"\n**返回值:** `{func['returns']}`\n\n"
                content += "---\n"

        api_path = self.skill_path / "API.md"
        api_path.write_text(content, encoding="utf-8")
        self.generated.append({"type": "api", "file": "API.md", "functions": len(all_functions)})
        print(f"  ✅ 生成 API.md（{len(all_functions)} 个函数）")

    def _generate_faq(self):
        """生成常见问题文档"""
        print("\n❓ 生成常见问题文档...")

        faq_path = self.skill_path / "FAQ.md"
        if faq_path.exists():
            print("  ⏭️  FAQ.md 已存在，跳过")
            return

        content = """# 常见问题

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
"""

        faq_path.write_text(content, encoding="utf-8")
        self.generated.append({"type": "faq", "file": "FAQ.md"})
        print("  ✅ 生成 FAQ.md")

    def _generate_examples(self):
        """生成使用示例文档"""
        print("\n💡 生成使用示例文档...")

        examples_path = self.skill_path / "USE-CASES.md"
        if examples_path.exists():
            print("  ⏭️  USE-CASES.md 已存在，跳过")
            return

        content = """# 使用案例与最佳实践

## 案例 1: 基本使用场景

### 场景描述
适用于初学者的基本使用流程。

### 操作步骤

```bash
# 1. 初始化
python main.py init --name "示例项目"

# 2. 执行操作
python main.py run --input data.txt

# 3. 查看结果
python main.py report
```

### 最佳实践
- 先使用 `--dry-run` 预览效果
- 定期备份重要数据
- 查看日志排查问题

---

## 案例 2: 批量处理场景

### 场景描述
需要处理大量文件或数据时。

### 操作步骤

```bash
# 准备输入列表
cat > list.json << EOF
["file1.txt", "file2.txt", "file3.txt"]
EOF

# 批量执行
python main.py batch --list list.json --output results/
```

### 最佳实践
- 分批处理，避免内存溢出
- 使用 `--parallel` 启用并行处理
- 处理完成后验证结果完整性

---

## 案例 3: 集成到工作流

### 场景描述
与 CI/CD 或其他工具集成。

### 操作步骤

```yaml
# GitHub Actions 示例
- name: Run Skill
  run: |
    python main.py run --input ${{ github.workspace }}/data
    python main.py report --format json
```

### 最佳实践
- 在 CI 中使用固定版本
- 添加失败重试机制
- 输出结构化日志便于分析

---

## 案例 4: 自定义扩展

### 场景描述
需要添加自定义功能或模板。

### 操作步骤

```python
# 自定义插件
from skill import BasePlugin

class MyPlugin(BasePlugin):
    def execute(self, data):
        # 自定义逻辑
        return processed_data
```

### 最佳实践
- 遵循现有代码风格
- 添加单元测试
- 更新文档说明
"""

        examples_path.write_text(content, encoding="utf-8")
        self.generated.append({"type": "examples", "file": "USE-CASES.md"})
        print("  ✅ 生成 USE-CASES.md")

    def _generate_architecture(self):
        """生成架构文档"""
        print("\n🏗️  生成架构文档...")

        arch_path = self.skill_path / "ARCHITECTURE.md"
        if arch_path.exists():
            print("  ⏭️  ARCHITECTURE.md 已存在，跳过")
            return

        py_files = self._get_python_files()

        content = f"""# 项目架构

## 概述

本项目采用模块化设计，遵循单一职责原则。

## 目录结构

```
project/
├── main.py              # 主入口
├── scripts/             # 核心脚本
"""
        for f in py_files:
            rel = f.relative_to(self.skill_path)
            content += f"│   ├── {rel.name}\n"

        content += """├── templates/           # 模板文件
├── tests/               # 测试
└── docs/                # 文档
```

## 核心模块

### 主入口模块
负责命令行参数解析和流程调度。

### 功能模块
每个脚本负责一个独立功能，遵循高内聚低耦合原则。

### 数据流向

```
输入 → 参数解析 → 核心处理 → 输出生成 → 结果返回
```

## 设计原则

1. **单一职责**: 每个模块只做一件事
2. **开闭原则**: 对扩展开放，对修改关闭
3. **依赖倒置**: 依赖抽象而非具体实现
4. **接口隔离**: 提供最小必要接口

## 扩展点

- 插件系统: 支持自定义插件
- 模板引擎: 支持自定义模板
- 钩子机制: 支持生命周期钩子
"""

        arch_path.write_text(content, encoding="utf-8")
        self.generated.append({"type": "architecture", "file": "ARCHITECTURE.md"})
        print("  ✅ 生成 ARCHITECTURE.md")

    def print_summary(self):
        """打印生成摘要"""
        print("\n" + "=" * 60)
        print("📊 文档生成摘要")
        print("=" * 60)
        for item in self.generated:
            print(f"  ✅ {item['file']} ({item['type']})")
        print(f"\n共生成 {len(self.generated)} 个文档")


def main():
    parser = argparse.ArgumentParser(description="Skill 文档生成工具 v1.8.0（纯文档型自动跳过API/架构文档）")
    parser.add_argument("--path", required=True, help="Skill 目录路径")
    parser.add_argument("--type", choices=["all", "api", "faq", "examples", "architecture"],
                        default="all", help="生成文档类型")
    args = parser.parse_args()

    if not os.path.exists(args.path):
        print(f"❌ 错误: 路径不存在 - {args.path}")
        return

    generator = DocGenerator(args.path)
    generator.generate(doc_type=args.type)
    generator.print_summary()


if __name__ == "__main__":
    main()
