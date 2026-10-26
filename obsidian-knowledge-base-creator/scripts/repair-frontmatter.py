#!/usr/bin/env python3
"""
Frontmatter YAML 修复脚本（v5.0）
基于 171 篇文档实战验证，修复 Frontmatter 中的常见问题：
1. 移除 Frontmatter 内混入的 ``` 标记
2. 统一 pre 字段为 ["[[link]]"] 格式
3. 修复畸形多括号 [[[[link]]]

用法：
    python repair-frontmatter.py --path "知识库路径"
    python repair-frontmatter.py --path "知识库路径" --dry-run
"""

import os
import re
import sys
import argparse

BT = '`' * 3


def find_md_files(root):
    files = []
    for dirpath, _, filenames in os.walk(root):
        for f in filenames:
            if f.endswith('.md'):
                files.append(os.path.join(dirpath, f))
    return sorted(files)


def fix_frontmatter(content):
    """修复单个文件的 Frontmatter，返回 (新内容, 修改数)"""
    if not content.startswith('---'):
        return content, 0

    end = content.find('\n---', 3)
    if end == -1:
        return content, 0

    fm_text = content[3:end]
    changes = 0

    # 1. 移除 Frontmatter 内的 ``` 标记
    if BT in fm_text:
        fm_lines = fm_text.split('\n')
        clean_lines = [line for line in fm_lines if line.strip() != BT]
        new_fm = '\n'.join(clean_lines)
        changes += fm_text.count(BT)
        fm_text = new_fm

    # 2. 修复 pre 字段格式
    def fix_pre(match):
        nonlocal changes
        pre_val = match.group(1).strip()
        if pre_val == '[]':
            return match.group(0)

        # 保存原始值，用于最后比较
        original_pre_val = pre_val

        # 修复已被旧bug污染的畸形格式：["[["link"]]"] → ["[[link]]"]
        # 特征：link周围多了一层引号，形如 [["link"]]
        pre_val = re.sub(r'\[\["([^"]+)"\]\]', r'[[\1]]', pre_val)

        links = []

        # 方法1：匹配 [[link]] 格式（已正确的双链）
        double_bracket_links = re.findall(r'\[\[([^\]]+)\]\]', pre_val)
        if double_bracket_links:
            links = double_bracket_links
        else:
            # 方法2：解析 YAML 数组格式 ["link1", "link2"] 或 ['link1', 'link2']
            # 匹配引号包裹的字符串（修复前bug：原正则 \[([^\]]+)\] 会把整个数组内容当作一个link）
            quoted_strings = re.findall(r'["\']([^"\']+)["\']', pre_val)
            if quoted_strings:
                links = quoted_strings
            else:
                # 方法3：逗号分隔的纯文本 link1, link2
                inner = pre_val.strip('[]').strip()
                if inner:
                    links = [s.strip() for s in inner.split(',') if s.strip()]

        if links:
            # 构造标准格式
            expected = 'pre: [' + ', '.join(f'"[[{l}]]"' for l in links) + ']'
            # 用原始值比较，确保畸形格式也能被检测到需要修改
            actual = 'pre: ' + original_pre_val
            if expected != actual:
                changes += 1
                return expected
        return match.group(0)

    fm_text = re.sub(r'^pre:\s*(.+)$', fix_pre, fm_text, flags=re.MULTILINE)

    # 3. 修复畸形多括号 [[[[link]]]
    fm_text = re.sub(r'\[{3,}([^\]]+)\]{3,}', r'[[\1]]', fm_text)

    new_content = '---' + fm_text + content[end:]
    return new_content, changes


def main():
    parser = argparse.ArgumentParser(description='Frontmatter YAML 修复脚本')
    parser.add_argument('--path', required=True, help='知识库根目录路径')
    parser.add_argument('--dry-run', action='store_true', help='预览模式，不写入文件')
    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f'错误：路径不存在 - {args.path}')
        sys.exit(1)

    files = find_md_files(args.path)
    print(f'总文件数: {len(files)}')
    print()

    total_changes = 0
    files_modified = 0

    for fp in files:
        with open(fp, 'r', encoding='utf-8-sig') as f:
            content = f.read()

        new_content, changes = fix_frontmatter(content)

        if changes > 0:
            files_modified += 1
            total_changes += changes
            fname = os.path.basename(fp)
            print(f'{fname}: 修复 {changes} 处')

            if not args.dry_run:
                with open(fp, 'w', encoding='utf-8', newline='\n') as f:
                    f.write(new_content)

    print(f'\n总计: 修复 {total_changes} 处，涉及 {files_modified} 个文件')
    if args.dry_run:
        print('（预览模式，未写入文件）')


if __name__ == '__main__':
    main()
