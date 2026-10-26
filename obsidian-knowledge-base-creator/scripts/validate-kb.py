#!/usr/bin/env python3
"""
知识库质量校验脚本
验证五段式结构、排版规范、代码块语言标注、表格格式、MOC表格格式

用法:
    python validate-kb.py --path "知识库路径"
    python validate-kb.py --path "./my-kb" --strict
    python validate-kb.py --path "./my-kb/MOC-前端开发.md" --moc

v1.1.0: 新增表格格式深度检查（列数一致性/双链管道符未转义），支持MOC文件校验
"""

import os
import re
import argparse


def extract_frontmatter(filepath: str) -> str:
    """提取文件内容，返回完整内容字符串（无论是否有Frontmatter）"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        return content
    except:
        pass
    return ""


def _clean_table_pipes(line: str) -> str:
    """清理表格行中的管道符，排除转义的 \\| 和双链内的 |"""
    cleaned = line.replace('\\|', '')
    cleaned = re.sub(r'\[\[[^\]]*\]\]', '[[]]', cleaned)
    return cleaned


def validate_structure(content: str, filename: str) -> list:
    """验证五段式结构"""
    issues = []
    # 检查五大模块
    sections = ['概述', '原理', '实操', '问题', '拓展']
    for section in sections:
        if not re.search(rf'##.*{section}', content):
            issues.append(f"  ⚠️ 缺少模块: {section}")

    # 检查标题层级
    h1_count = len(re.findall(r'^# ', content, re.MULTILINE))
    if h1_count > 1:
        issues.append(f"  ⚠️ 一级标题过多 ({h1_count}个，应仅1个)")

    # 检查文档尾部
    if not re.search(r'\[\[Home', content):
        issues.append(f"  ⚠️ 缺少返回首页链接")

    return issues


def validate_formatting(content: str, filename: str) -> list:
    """验证排版规范"""
    issues = []

    # 检查代码块语言标注
    code_blocks = re.findall(r'```(\w*)', content)
    unnamed_blocks = [i for i, lang in enumerate(code_blocks) if not lang]
    if unnamed_blocks:
        issues.append(f"  ⚠️ {len(unnamed_blocks)} 个代码块未标注语言")

    # 检查引用块类型
    if '> 💡' not in content and '> ⚠️' not in content and '> ✅' not in content:
        issues.append(f"  ⚠️ 缺少引用块（提示/警告/最佳实践）")

    # 检查加粗使用
    bold_count = len(re.findall(r'\*\*[^*]+\*\*', content))
    if bold_count == 0:
        issues.append(f"  ⚠️ 没有使用加粗强调")

    return issues


def validate_table_format(content: str, filename: str) -> list:
    """验证表格格式（列数一致性、双链管道符未转义）"""
    issues = []
    lines = content.split('\n')
    in_table = False
    expected_cols = 0

    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        # 检测表头行
        if not in_table and stripped.startswith('|') and stripped.endswith('|'):
            if not re.match(r'^\|[\s\-:|]+\|$', stripped):
                in_table = True
                cleaned = _clean_table_pipes(stripped)
                expected_cols = cleaned.count('|') - 1
                continue

        # 分隔符行
        if in_table and re.match(r'^\|[\s\-:|]+\|$', stripped):
            continue

        # 数据行
        if in_table and stripped.startswith('|') and stripped.endswith('|'):
            # 1. 检查列数一致性
            cleaned = _clean_table_pipes(stripped)
            actual_cols = cleaned.count('|') - 1
            if actual_cols != expected_cols and expected_cols > 0:
                issues.append(f"  ⚠️ 行{i}: 表格列数不匹配 (实际{actual_cols}列≠表头{expected_cols}列) | {stripped[:60]}")

            # 2. 检查表格中双链管道符未转义
            wiki_links = re.findall(r'\[\[([^\]]+)\]\]', stripped)
            for link in wiki_links:
                if '|' in link and '\\|' not in link:
                    issues.append(f"  ⚠️ 行{i}: 表格双链管道符未转义 [[{link[:40]}]] 中的 | 应转义为 \\|")

            continue

        # 空行结束表格
        if in_table and not stripped:
            in_table = False

    # 3. 检查双链目标为空（[[|文字]] 格式错误）
    empty_target_links = re.findall(r'\[\[\s*\|[^\]]+\]\]', content)
    if empty_target_links:
        issues.append(f"  🔴 发现 {len(empty_target_links)} 个双链目标为空 ([[|文字]] 格式错误)")

    return issues


def validate_links(content: str, filename: str) -> list:
    """验证链接规范"""
    issues = []

    # 检查内部链接
    internal_links = re.findall(r'\[\[([^\]]+)\]\]', content)
    if len(internal_links) < 2:
        issues.append(f"  ⚠️ 内部链接过少 ({len(internal_links)}个，建议至少2个)")

    # 检查外部链接格式
    external_links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
    for text, url in external_links:
        if not url.startswith('http'):
            issues.append(f"  ⚠️ 外部链接格式错误: {url}")

    return issues


def main() -> None:
    """主函数"""
    parser = argparse.ArgumentParser(description="知识库质量校验")
    parser.add_argument("--path", required=True, help="知识库路径或单文件路径")
    parser.add_argument("--strict", action="store_true", help="严格模式（检查所有项）")
    parser.add_argument("--moc", action="store_true", help="MOC校验模式（重点检查表格格式）")
    args = parser.parse_args()

    path = os.path.abspath(args.path)

    # 判断是文件还是目录
    if os.path.isfile(path):
        files = [path]
    else:
        files = []
        for root, dirs, fs in os.walk(path):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for f in fs:
                if f.endswith('.md'):
                    # MOC模式只校验MOC文件，非MOC模式跳过MOC文件（MOC有专门的格式要求）
                    if args.moc:
                        if f.startswith('MOC-'):
                            files.append(os.path.join(root, f))
                    else:
                        if not f.startswith('MOC-'):
                            files.append(os.path.join(root, f))

    print(f"\n✅ 质量校验: {path}")
    if args.moc:
        print("📋 模式: MOC 表格格式校验")
    print(f"📝 待校验文件: {len(files)} 个")
    print("=" * 60)

    total_issues = 0
    perfect_files = 0

    for filepath in files:
        filename = os.path.basename(filepath)
        content = extract_frontmatter(filepath)
        if not content:
            print(f"\n❌ {filename}: 无法读取")
            continue

        issues = []

        if args.moc:
            # MOC模式：重点校验表格格式
            issues.extend(validate_table_format(content, filename))
        else:
            # 普通模式：校验结构、排版、表格格式
            issues.extend(validate_structure(content, filename))
            issues.extend(validate_formatting(content, filename))
            issues.extend(validate_table_format(content, filename))
            if args.strict:
                issues.extend(validate_links(content, filename))

        if issues:
            print(f"\n⚠️ {filename}: {len(issues)} 个问题")
            for issue in issues:
                print(issue)
            total_issues += len(issues)
        else:
            perfect_files += 1

    print("\n" + "=" * 60)
    print("📊 校验总结")
    print(f"  总文件数: {len(files)}")
    print(f"  完美文件: {perfect_files}")
    print(f"  有问题文件: {len(files) - perfect_files}")
    print(f"  总问题数: {total_issues}")
    if total_issues == 0:
        print("\n🎉 全部文件通过质量校验！")
    else:
        print(f"\n💡 平均每文件问题数: {total_issues/len(files):.1f}")
        if args.moc:
            print("💡 建议优先修复: 表格列数不匹配 > 双链管道符未转义 > 双链目标为空")
        else:
            print("💡 建议优先修复: 结构缺失 > 表格格式 > 代码块语言 > 引用块缺失")


if __name__ == "__main__":
    main()
