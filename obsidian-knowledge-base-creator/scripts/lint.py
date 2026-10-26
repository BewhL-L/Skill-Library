#!/usr/bin/env python3
"""
代码质量检查脚本
检查 Python 脚本的代码规范、类型注解、文档字符串等

用法:
    python lint.py
    python lint.py --fix
    python lint.py --path scripts/
"""

import os
import sys
import re
import ast
from pathlib import Path

# 获取脚本所在目录
SCRIPT_DIR = Path(__file__).parent.absolute()

# 检查结果
results = {
    'errors': [],
    'warnings': [],
    'info': []
}

def add_error(file, line, message):
    results['errors'].append((file, line, message))

def add_warning(file, line, message):
    results['warnings'].append((file, line, message))

def add_info(file, line, message):
    results['info'].append((file, line, message))

def check_file(filepath):
    """检查单个 Python 文件"""
    file_path = Path(filepath)
    rel_path = str(file_path.relative_to(SCRIPT_DIR)) if file_path.is_absolute() else str(file_path)

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
    except Exception as e:
        add_error(rel_path, 0, f"无法读取文件: {e}")
        return

    # 1. 检查文件编码声明
    if not content.startswith('#!/usr/bin/env python3') and not content.startswith('# -*- coding: utf-8 -*-'):
        if len(lines) > 0 and not lines[0].startswith('#!'):
            add_warning(rel_path, 1, "缺少 shebang 或编码声明")

    # 2. 检查模块文档字符串
    try:
        tree = ast.parse(content)
        if not (tree.body and isinstance(tree.body[0], ast.Expr) and isinstance(tree.body[0].value, ast.Constant) and isinstance(tree.body[0].value.value, str)):
            add_warning(rel_path, 1, "缺少模块文档字符串")
    except SyntaxError as e:
        add_error(rel_path, e.lineno, f"语法错误: {e.msg}")
        return

    # 3. 检查函数文档字符串和类型注解
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # 检查函数文档字符串
            if not (node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant) and isinstance(node.body[0].value.value, str)):
                if not node.name.startswith('_'):  # 私有函数可以没有文档字符串
                    add_warning(rel_path, node.lineno, f"函数 '{node.name}' 缺少文档字符串")

            # 检查参数类型注解
            for arg in node.args.args:
                if arg.arg == 'self' or arg.arg == 'cls':
                    continue
                if arg.annotation is None:
                    add_info(rel_path, node.lineno, f"函数 '{node.name}' 参数 '{arg.arg}' 缺少类型注解")

            # 检查返回值类型注解
            if node.returns is None and node.name != 'main':
                add_info(rel_path, node.lineno, f"函数 '{node.name}' 缺少返回值类型注解")

    # 4. 检查行宽
    for i, line in enumerate(lines, 1):
        if len(line) > 120:
            add_warning(rel_path, i, f"行宽超过 120 字符 ({len(line)})")

    # 5. 检查行尾空格
    for i, line in enumerate(lines, 1):
        if line != line.rstrip():
            add_warning(rel_path, i, "行尾有空格")

    # 6. 检查 Tab 缩进
    for i, line in enumerate(lines, 1):
        if '\t' in line and not line.strip().startswith('#'):
            add_error(rel_path, i, "使用 Tab 缩进，应使用空格")

    # 7. 检查 print 语句（应该使用 logging）
    # 注意：CLI 工具可以使用 print，这里只作为提示
    print_count = len(re.findall(r'\bprint\s*\(', content))
    if print_count > 10:
        add_info(rel_path, 0, f"使用了 {print_count} 次 print，考虑使用 logging 模块")

    # 8. 检查 TODO/FIXME
    for i, line in enumerate(lines, 1):
        if 'TODO' in line or 'FIXME' in line:
            add_info(rel_path, i, f"包含 TODO/FIXME: {line.strip()[:50]}")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="代码质量检查")
    parser.add_argument("--path", default=".", help="检查的路径（文件或目录）")
    parser.add_argument("--fix", action="store_true", help="自动修复可修复的问题")
    args = parser.parse_args()

    check_path = Path(args.path)
    if not check_path.is_absolute():
        check_path = SCRIPT_DIR / check_path

    # 收集所有 Python 文件
    python_files = []
    if check_path.is_file():
        if check_path.suffix == '.py':
            python_files.append(check_path)
    elif check_path.is_dir():
        for f in check_path.rglob('*.py'):
            # 排除测试文件和临时文件
            if 'test' not in f.name and 'lint' not in f.name:
                python_files.append(f)

    print("=" * 60)
    print("🔍 代码质量检查")
    print("=" * 60)
    print(f"📁 检查路径: {check_path}")
    print(f"📄 检查文件数: {len(python_files)}")
    print()

    # 检查每个文件
    for filepath in sorted(python_files):
        check_file(filepath)

    # 输出结果
    print("=" * 60)
    print("📊 检查结果")
    print("=" * 60)
    print(f"❌ 错误: {len(results['errors'])}")
    print(f"⚠️  警告: {len(results['warnings'])}")
    print(f"ℹ️  信息: {len(results['info'])}")
    print()

    if results['errors']:
        print("❌ 错误:")
        for file, line, msg in results['errors'][:20]:
            print(f"  {file}:{line}: {msg}")
        if len(results['errors']) > 20:
            print(f"  ... 还有 {len(results['errors'])-20} 个错误")
        print()

    if results['warnings']:
        print("⚠️  警告:")
        for file, line, msg in results['warnings'][:20]:
            print(f"  {file}:{line}: {msg}")
        if len(results['warnings']) > 20:
            print(f"  ... 还有 {len(results['warnings'])-20} 个警告")
        print()

    if results['info']:
        print("ℹ️  信息:")
        for file, line, msg in results['info'][:10]:
            print(f"  {file}:{line}: {msg}")
        if len(results['info']) > 10:
            print(f"  ... 还有 {len(results['info'])-10} 条信息")
        print()

    # 总结
    total_issues = len(results['errors']) + len(results['warnings'])
    if total_issues == 0:
        print("🎉 代码质量优秀，没有发现问题！")
        return 0
    elif len(results['errors']) == 0:
        print(f"✅ 没有错误，但有 {len(results['warnings'])} 个警告，建议修复")
        return 0
    else:
        print(f"❌ 发现 {len(results['errors'])} 个错误，需要修复")
        return 1

if __name__ == "__main__":
    sys.exit(main())
