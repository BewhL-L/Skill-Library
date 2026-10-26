#!/usr/bin/env python3
"""
知识库健康检查脚本
检测 Frontmatter 完整性、标签规范性、死链、孤立文档、MOC 覆盖率、MOC 表格格式

用法:
    python audit-kb.py --path "知识库路径"

v1.1.0: 新增 MOC 表格格式检查（列数一致性、双链管道符未转义、[[|文字]]错误格式）
"""

import os
import re
import argparse
from collections import defaultdict


def extract_frontmatter(filepath: str) -> tuple:
    """提取 Frontmatter"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        if match:
            fm = match.group(1)
            result = {}
            for line in fm.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    result[key.strip()] = value.strip()
            return result, content
    except:
        pass
    return {}, ""


def check_frontmatter(notes: list) -> list:
    """检查 Frontmatter 完整性"""
    required_fields = ['title', 'tags', 'category', 'created', 'updated', 'difficulty', 'status', 'priority', 'pre', 'aliases']
    issues = []
    for note in notes:
        fm = note['fm']
        missing = [f for f in required_fields if f not in fm or not fm[f]]
        if missing:
            issues.append(f"  ⚠️ {note['name']}: 缺少字段 {', '.join(missing)}")

        # 检查 difficulty 是否为星级
        if 'difficulty' in fm and not fm['difficulty'].startswith('⭐'):
            issues.append(f"  ⚠️ {note['name']}: difficulty 不是星级格式 - {fm['difficulty']}")

        # 检查 status 是否标准
        standard_status = ['✅ 内容已完善', '📝 草稿', '🔄 更新中', '⚠️ 待审核']
        if 'status' in fm and fm['status'] not in standard_status:
            issues.append(f"  ⚠️ {note['name']}: status 不标准 - {fm['status']}")

    return issues


def check_tags(notes: list) -> tuple:
    """检查标签规范性"""
    all_tags = defaultdict(int)
    issues = []
    for note in notes:
        fm = note['fm']
        if 'tags' in fm:
            tags_str = fm['tags'].strip('[]')
            tags = [t.strip() for t in tags_str.split(',') if t.strip()]
            for tag in tags:
                all_tags[tag] += 1
            if len(tags) > 8:
                issues.append(f"  ⚠️ {note['name']}: 标签过多 ({len(tags)}个)")
            if len(tags) < 2:
                issues.append(f"  ⚠️ {note['name']}: 标签过少 ({len(tags)}个)")

    # 一次性标签
    one_time_tags = {tag: count for tag, count in all_tags.items() if count == 1}
    return issues, all_tags, one_time_tags


def check_links(notes: list, all_note_names: set) -> tuple:
    """检查死链和孤立文档"""
    link_pattern = r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]'
    all_links = defaultdict(int)
    linked_notes = set()
    issues = []

    for note in notes:
        content = note['content']
        links = re.findall(link_pattern, content)
        for link in links:
            link_name = link.strip()
            all_links[link_name] += 1
            if link_name in all_note_names:
                linked_notes.add(link_name)
            else:
                # 排除模板占位符
                if not any(x in link_name for x in ['{{', '<', '占位', '模板']):
                    issues.append(f"  🔗 死链: [[{link_name}]] (引用 {all_links[link_name]} 次)")

    # 孤立文档（没有入链也没有出链）
    isolated = []
    for note in notes:
        name = note['name'].replace('.md', '')
        has_outlink = bool(re.search(link_pattern, note['content']))
        has_inlink = name in linked_notes
        if not has_outlink and not has_inlink:
            isolated.append(name)

    return issues, all_links, isolated


def check_moc_coverage(notes: list, directory: str) -> tuple:
    """检查 MOC 覆盖率"""
    categories = defaultdict(list)
    for note in notes:
        fm = note['fm']
        cat = fm.get('category', '未分类')
        categories[cat].append(note['name'])

    # 递归查找所有 MOC 文件（包括子目录）
    moc_files = []
    for root, dirs, files in os.walk(directory):
        for f in files:
            if f.startswith('MOC-') and f.endswith('.md'):
                moc_files.append(f)
    issues = []
    for cat, note_list in categories.items():
        moc_exists = any(cat in moc for moc in moc_files)
        if not moc_exists and cat != '未分类':
            issues.append(f"  📚 {cat}: 缺少 MOC ({len(note_list)} 篇笔记)")

    return issues, categories


def _clean_table_pipes(line: str) -> str:
    """清理表格行中的管道符，排除转义的 \\| 和双链内的 |"""
    # 先移除转义的 \|
    cleaned = line.replace('\\|', '')
    # 再移除双链 [[...]] 内的内容（包括其中的 |）
    cleaned = re.sub(r'\[\[[^\]]*\]\]', '[[]]', cleaned)
    return cleaned


def check_moc_format(directory: str) -> list:
    """检查 MOC 文件中的表格格式问题

    检测三类问题：
    1. 表格列数不匹配（数据行列数与表头不一致）
    2. 表格中双链管道符未转义（[[filename|title]] 中的 | 应转义为 \\|）
    3. 双链目标为空（[[|文字]] 格式错误）
    """
    issues = []
    moc_files = []

    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for f in files:
            if f.startswith('MOC-') and f.endswith('.md'):
                moc_files.append(os.path.join(root, f))

    for moc_path in moc_files:
        try:
            with open(moc_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            continue

        moc_name = os.path.basename(moc_path)
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
                    issues.append(f"  ⚠️ {moc_name} 行{i}: 表格列数不匹配 (实际{actual_cols}列≠表头{expected_cols}列)")

                # 2. 检查表格中双链管道符未转义
                wiki_links = re.findall(r'\[\[([^\]]+)\]\]', stripped)
                for link in wiki_links:
                    if '|' in link and '\\|' not in link:
                        issues.append(f"  ⚠️ {moc_name} 行{i}: 表格双链管道符未转义 [[{link[:40]}]] 中的 | 应转义为 \\|")

                continue

            # 空行结束表格
            if in_table and not stripped:
                in_table = False

        # 3. 检查双链目标为空（[[|文字]] 格式错误）
        empty_target_links = re.findall(r'\[\[\s*\|[^\]]+\]\]', content)
        if empty_target_links:
            issues.append(f"  🔴 {moc_name}: 发现 {len(empty_target_links)} 个双链目标为空 ([[|文字]] 格式错误)")

    return issues


def main() -> None:
    """主函数"""
    parser = argparse.ArgumentParser(description="知识库健康检查")
    parser.add_argument("--path", required=True, help="知识库路径")
    args = parser.parse_args()

    directory = os.path.abspath(args.path)
    if not os.path.exists(directory):
        print(f"❌ 目录不存在: {directory}")
        return

    print(f"\n🔍 知识库健康检查: {directory}")
    print("=" * 60)

    # 扫描所有笔记
    notes = []
    all_note_names = set()
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                fm, content = extract_frontmatter(filepath)
                notes.append({'name': file, 'path': filepath, 'fm': fm, 'content': content})
                all_note_names.add(file.replace('.md', ''))

    print(f"\n📝 总笔记数: {len(notes)}")

    # 1. Frontmatter 检查
    print("\n📋 1. Frontmatter 完整性检查")
    fm_issues = check_frontmatter(notes)
    if fm_issues:
        print(f"  发现 {len(fm_issues)} 个问题:")
        for issue in fm_issues[:20]:
            print(issue)
        if len(fm_issues) > 20:
            print(f"  ... 还有 {len(fm_issues)-20} 个问题")
    else:
        print("  ✅ 全部通过")

    # 2. 标签检查
    print("\n🏷️ 2. 标签规范性检查")
    tag_issues, all_tags, one_time_tags = check_tags(notes)
    print(f"  总标签数: {len(all_tags)}")
    print(f"  一次性标签: {len(one_time_tags)}")
    if one_time_tags:
        print("  一次性标签示例:", ", ".join(list(one_time_tags.keys())[:10]))
    if tag_issues:
        print(f"  发现 {len(tag_issues)} 个问题:")
        for issue in tag_issues[:10]:
            print(issue)

    # 3. 死链和孤立文档检查
    print("\n🔗 3. 死链和孤立文档检查")
    link_issues, all_links, isolated = check_links(notes, all_note_names)
    print(f"  死链数: {len(link_issues)}")
    print(f"  孤立文档数: {len(isolated)}")
    if isolated:
        print("  孤立文档:", ", ".join(isolated[:10]))
    if link_issues:
        print("  高频死链 TOP 10:")
        sorted_links = sorted(all_links.items(), key=lambda x: x[1], reverse=True)
        for link, count in sorted_links[:10]:
            if link not in all_note_names:
                print(f"    [[{link}]]: {count} 次")

    # 4. MOC 覆盖率
    print("\n📚 4. MOC 覆盖率检查")
    moc_issues, categories = check_moc_coverage(notes, directory)
    print(f"  分类数: {len(categories)}")
    if moc_issues:
        print(f"  发现 {len(moc_issues)} 个问题:")
        for issue in moc_issues:
            print(issue)
    else:
        print("  ✅ 全部通过")

    # 5. MOC 表格格式检查（新增）
    print("\n📊 5. MOC 表格格式检查")
    moc_format_issues = check_moc_format(directory)
    if moc_format_issues:
        print(f"  发现 {len(moc_format_issues)} 个问题:")
        for issue in moc_format_issues[:30]:
            print(issue)
        if len(moc_format_issues) > 30:
            print(f"  ... 还有 {len(moc_format_issues)-30} 个问题")
    else:
        print("  ✅ 全部 MOC 表格格式正确")

    # 总结
    print("\n" + "=" * 60)
    print("📊 健康检查总结")
    total_issues = len(fm_issues) + len(tag_issues) + len(link_issues) + len(moc_issues) + len(isolated) + len(moc_format_issues)
    print(f"  总问题数: {total_issues}")
    print(f"  - Frontmatter 问题: {len(fm_issues)}")
    print(f"  - 标签问题: {len(tag_issues)}")
    print(f"  - 死链: {len(link_issues)}")
    print(f"  - 孤立文档: {len(isolated)}")
    print(f"  - MOC 缺失: {len(moc_issues)}")
    print(f"  - MOC 表格格式: {len(moc_format_issues)}")
    if total_issues == 0:
        print("\n🎉 知识库非常健康！")
    else:
        print(f"\n💡 建议优先修复: MOC表格格式 > 高频死链 > Frontmatter缺失 > 孤立文档 > 标签问题")


if __name__ == "__main__":
    main()
