#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skill 测试生成脚本
自动解析 Python 脚本，生成单元测试和集成测试模板
v1.8.0: 统一版本号，新增路径存在性验证，完善错误处理
"""

import os
import re
import ast
import sys
import argparse
from pathlib import Path
from typing import List, Dict

# 导入同目录下的类型检测器
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from skill_type_detector import SkillTypeDetector
except ImportError:
    SkillTypeDetector = None


class TestGenerator:
    """测试生成器"""

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

    def generate(self, test_type: str = "all"):
        """生成测试（纯文档型自动跳过）"""
        print(f"🧪 开始生成测试: {self.skill_path}")

        # 纯文档型跳过
        if self.skill_type == "doc-only":
            print("=" * 60)
            print("⚠️  检测到纯文档型 Skill，无需生成测试（无 Python 代码）")
            print("   建议：专注于完善文档结构和 references 深度")
            print("   可运行 audit-skill.py 查看文档型专属维度得分")
            return self.generated

        print("=" * 60)
        print(f"📋 Skill 类型: {self.skill_type}")

        if test_type in ["all", "unit"]:
            self._generate_unit_tests()
        if test_type in ["all", "integration"]:
            self._generate_integration_tests()
        if test_type in ["all", "conftest"]:
            self._generate_conftest()
        if test_type in ["all", "coverage"]:
            self._generate_coverage_config()

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
                if isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
                    functions.append({
                        "name": node.name,
                        "args": [a.arg for a in node.args.args],
                        "line": node.lineno
                    })
        except Exception:
            pass
        return functions

    def _sanitize_module_name(self, raw_name: str) -> Dict[str, str]:
        """
        清理模块名，生成合法的 Python 标识符

        Args:
            raw_name: 原始模块名（可能包含连字符，如 "audit-kb"）

        Returns:
            {
                "snake": "audit_kb",      # 下划线版本，用于文件名和导入
                "pascal": "AuditKb",      # PascalCase 版本，用于类名
                "original": "audit-kb",    # 原始名称，用于显示
            }
        """
        # 连字符替换成下划线
        snake_name = raw_name.replace("-", "_").replace(" ", "_")
        # 生成 PascalCase 类名
        pascal_name = "".join(word.capitalize() for word in snake_name.split("_"))
        return {
            "snake": snake_name,
            "pascal": pascal_name,
            "original": raw_name,
        }

    def _generate_unit_tests(self):
        """生成单元测试"""
        print("\n🔬 生成单元测试...")

        tests_dir = self.skill_path / "tests" / "unit"
        tests_dir.mkdir(parents=True, exist_ok=True)

        py_files = self._get_python_files()
        total_tests = 0

        for py_file in py_files:
            funcs = self._parse_functions(py_file)
            if not funcs:
                continue

            # 清理模块名，避免连字符导致语法错误
            name_info = self._sanitize_module_name(py_file.stem)
            module_name = name_info["snake"]  # 下划线版本，用于文件名
            class_name = name_info["pascal"]   # PascalCase 版本，用于类名
            original_name = name_info["original"]  # 原始名称，用于显示

            test_file = tests_dir / f"test_{module_name}.py"

            if test_file.exists():
                print(f"  ⏭️  {test_file.name} 已存在，跳过")
                continue

            # 生成测试文件内容
            content = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
{original_name} 模块单元测试
自动生成于 {__import__('datetime').datetime.now().strftime('%Y-%m-%d')}
"""

import pytest
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class Test{class_name}:
    """{original_name} 模块测试类"""
'''

            for func in funcs:
                args_str = ", ".join(func["args"]) if func["args"] else ""
                content += f'''
    def test_{func["name"]}_basic(self):
        """测试 {func["name"]} 基本功能"""
        # TODO: 实现测试逻辑
        # result = {module_name}.{func["name"]}({args_str})
        # assert result is not None
        pass

    def test_{func["name"]}_edge_cases(self):
        """测试 {func["name"]} 边界情况"""
        # TODO: 实现边界情况测试
        # 空输入、超大输入、特殊字符等
        pass

    def test_{func["name"]}_error_handling(self):
        """测试 {func["name"]} 错误处理"""
        # TODO: 实现错误处理测试
        # with pytest.raises(Exception):
        #     {module_name}.{func["name"]}(invalid_args)
        pass
'''
                total_tests += 3

            test_file.write_text(content, encoding="utf-8")
            self.generated.append({"type": "unit", "file": str(test_file), "tests": len(funcs) * 3})
            print(f"  ✅ 生成 {test_file.name}（{len(funcs)} 个函数，{len(funcs)*3} 个测试用例）")

        print(f"  📊 单元测试总计: {total_tests} 个用例")

    def _generate_integration_tests(self):
        """生成集成测试"""
        print("\n🔗 生成集成测试...")

        tests_dir = self.skill_path / "tests" / "integration"
        tests_dir.mkdir(parents=True, exist_ok=True)

        # 主流程集成测试
        test_file = tests_dir / "test_workflow.py"
        if test_file.exists():
            print(f"  ⏭️  {test_file.name} 已存在，跳过")
        else:
            content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主流程集成测试
测试完整的端到端工作流
"""

import pytest
import subprocess
import sys
import tempfile
from pathlib import Path


class TestWorkflow:
    """端到端工作流测试"""

    def test_help_command(self):
        """测试帮助命令"""
        result = subprocess.run(
            [sys.executable, "main.py", "--help"],
            capture_output=True,
            text=True,
            cwd=str(Path(__file__).parent.parent.parent)
        )
        assert result.returncode == 0
        assert "usage" in result.stdout.lower() or "帮助" in result.stdout

    def test_basic_workflow(self, tmp_path):
        """测试基本工作流"""
        # TODO: 根据实际命令修改
        # result = subprocess.run(
        #     [sys.executable, "main.py", "init", "--name", "test", "--path", str(tmp_path)],
        #     capture_output=True,
        #     text=True
        # )
        # assert result.returncode == 0
        # assert (tmp_path / "output").exists()
        pass

    def test_error_handling_workflow(self):
        """测试错误处理工作流"""
        # TODO: 测试无效输入时的错误处理
        # result = subprocess.run(
        #     [sys.executable, "main.py", "invalid_command"],
        #     capture_output=True,
        #     text=True
        # )
        # assert result.returncode != 0
        pass

    def test_output_format(self, tmp_path):
        """测试输出格式"""
        # TODO: 验证输出文件格式正确
        pass
'''
            test_file.write_text(content, encoding="utf-8")
            self.generated.append({"type": "integration", "file": str(test_file), "tests": 4})
            print(f"  ✅ 生成 {test_file.name}（4 个测试用例）")

        # CLI 命令集成测试
        cli_test = tests_dir / "test_cli.py"
        if cli_test.exists():
            print(f"  ⏭️  {cli_test.name} 已存在，跳过")
        else:
            content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI 命令集成测试
测试所有命令行命令
"""

import pytest
import subprocess
import sys
from pathlib import Path


def run_command(*args):
    """运行命令并返回结果"""
    return subprocess.run(
        [sys.executable, "main.py", *args],
        capture_output=True,
        text=True,
        cwd=str(Path(__file__).parent.parent.parent)
    )


class TestCLI:
    """CLI 命令测试"""

    def test_help(self):
        """测试 --help"""
        result = run_command("--help")
        assert result.returncode == 0

    def test_version(self):
        """测试 --version"""
        result = run_command("--version")
        assert result.returncode == 0

    def test_invalid_command(self):
        """测试无效命令"""
        result = run_command("invalid_command_xyz")
        assert result.returncode != 0

    def test_missing_required_arg(self):
        """测试缺少必需参数"""
        # TODO: 根据实际命令修改
        pass
'''
            cli_test.write_text(content, encoding="utf-8")
            self.generated.append({"type": "integration", "file": str(cli_test), "tests": 4})
            print(f"  ✅ 生成 {cli_test.name}（4 个测试用例）")

    def _generate_conftest(self):
        """生成 conftest.py"""
        print("\n⚙️  生成 conftest.py...")

        tests_dir = self.skill_path / "tests"
        conftest = tests_dir / "conftest.py"

        if conftest.exists():
            print("  ⏭️  conftest.py 已存在，跳过")
            return

        content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pytest 配置文件
提供共享的 fixture 和配置
"""

import pytest
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture
def project_root():
    """返回项目根目录"""
    return PROJECT_ROOT


@pytest.fixture
def temp_dir(tmp_path):
    """创建临时目录"""
    return tmp_path


@pytest.fixture
def sample_data():
    """提供示例数据"""
    return {
        "name": "test",
        "version": "1.0.0",
        "items": [1, 2, 3]
    }


def pytest_configure(config):
    """pytest 配置钩子"""
    config.addinivalue_line("markers", "slow: 标记慢速测试")
    config.addinivalue_line("markers", "integration: 标记集成测试")
    config.addinivalue_line("markers", "unit: 标记单元测试")
'''
        conftest.write_text(content, encoding="utf-8")
        self.generated.append({"type": "conftest", "file": str(conftest)})
        print("  ✅ 生成 conftest.py")

    def _generate_coverage_config(self):
        """生成覆盖率配置"""
        print("\n📊 生成覆盖率配置...")

        coverage_file = self.skill_path / ".coveragerc"
        if coverage_file.exists():
            print("  ⏭️  .coveragerc 已存在，跳过")
            return

        content = '''[run]
source = .
omit =
    */tests/*
    */__pycache__/*
    */.venv/*
    setup.py
    conftest.py

[report]
show_missing = True
skip_covered = False
precision = 2

[html]
directory = htmlcov

[xml]
output = coverage.xml
'''
        coverage_file.write_text(content, encoding="utf-8")
        self.generated.append({"type": "coverage", "file": str(coverage_file)})
        print("  ✅ 生成 .coveragerc")

    def print_summary(self):
        """打印生成摘要"""
        print("\n" + "=" * 60)
        print("📊 测试生成摘要")
        print("=" * 60)
        total_tests = 0
        for item in self.generated:
            tests = item.get("tests", 0)
            total_tests += tests
            print(f"  ✅ {Path(item['file']).name} ({item['type']}, {tests} 个用例)")
        print(f"\n共生成 {len(self.generated)} 个文件，{total_tests} 个测试用例")
        print(f"\n💡 运行测试:")
        print(f"   python -m pytest tests/ -v")
        print(f"   python -m pytest tests/ --cov=. --cov-report=html")


def main():
    parser = argparse.ArgumentParser(description="Skill 测试生成工具 v1.8.0（纯文档型自动跳过）")
    parser.add_argument("--path", required=True, help="Skill 目录路径")
    parser.add_argument("--type", choices=["all", "unit", "integration", "conftest", "coverage"],
                        default="all", help="生成测试类型")
    args = parser.parse_args()

    if not os.path.exists(args.path):
        print(f"❌ 错误: 路径不存在 - {args.path}")
        return

    generator = TestGenerator(args.path)
    generator.generate(test_type=args.type)
    generator.print_summary()


if __name__ == "__main__":
    main()
