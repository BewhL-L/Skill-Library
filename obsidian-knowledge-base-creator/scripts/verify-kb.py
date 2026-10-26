#!/usr/bin/env python3
"""
知识库综合验证脚本（v5.1）
基于 171 篇文档实战验证，检查 Frontmatter YAML、代码块平衡、标题级别三大维度。
标题级别检查新增：H2 数量异常检测、标题文本代码模式检测、H2/H3/H4 数量统计、MOC 文档例外处理。

用法：
    python verify-kb.py --path "知识库路径" --all
    python verify-kb.py --path "知识库路径" --check frontmatter
    python verify-kb.py --path "知识库路径" --check codeblocks
    python verify-kb.py --path "知识库路径" --check headers
"""

import os
import re
import sys
import argparse

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

BT = '`' * 3

# 统一命令行工具前缀列表（looks_like_code / is_code_comment / is_code_pattern_heading 共用）
COMMAND_PREFIXES = (
    r'pip|python|docker|kubectl|git|npm|curl|apt|sudo|cd|ls|echo|export|'
    r'chmod|mkdir|uvicorn|gunicorn|celery|pytest|ruff|black|mypy|pre-commit|'
    r'streamlit|gradio|alembic|poetry|node|conda|helm|aws|gcloud|terraform|'
    r'ansible|systemctl|ffmpeg|mpirun|vllm|trtllm|ollama|sglang|wget|tar|'
    r'gzip|ssh|scp|rsync|make|cmake|gcc|g\+\+|java|javac|mvn|gradle|go|rustc|cargo'
)


def find_md_files(root):
    """递归查找所有 .md 文件"""
    files = []
    for dirpath, _, filenames in os.walk(root):
        for f in filenames:
            if f.endswith('.md'):
                files.append(os.path.join(dirpath, f))
    return sorted(files)


def is_code_pattern_heading(text):
    """判断标题文本是否匹配代码模式，返回 (是否匹配, 模式类型)"""
    # 注释模式：文本内容以#开头
    if re.match(r'^#\s', text):
        return True, '注释'
    # 文件名模式
    if re.match(r'^[\w.-]+\.(py|txt|conf|yaml|yml|json|md|sh|bat|cfg|ini|toml|env|gitignore|dockerignore)$', text, re.I):
        return True, '文件名'
    if re.match(r'^(Makefile|Dockerfile|Gemfile|Rakefile)$', text, re.I):
        return True, '文件名'
    # 命令行模式
    if re.match(r'^(' + COMMAND_PREFIXES + r')\b', text, re.I):
        return True, '命令行'
    # 参数模式
    if re.match(r'^--', text):
        return True, '参数'
    # ASCII树模式
    if re.search(r'[├──└│┌┐┘├┤┬┴┼]', text):
        return True, 'ASCII树'
    # 代码符号模式（含等号/括号/箭头等，且不是正常中文标题）
    if re.search(r'[=(){}\[\]>-]|::|=>', text) and not re.search(r'[\u4e00-\u9fff]{3,}', text):
        return True, '代码符号'
    return False, ''


def is_moc_document(filepath, content):
    """判断是否为 MOC/枢纽/系统梳理类文档"""
    fname = os.path.basename(filepath) if filepath else ''
    moc_keywords = ['MOC', 'moc', '枢纽', '索引', '导航', '系统梳理', '总览']
    # 文件名匹配
    for kw in moc_keywords:
        if kw in fname:
            return True
    # H1 标题匹配
    h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if h1_match:
        h1_text = h1_match.group(1)
        for kw in moc_keywords:
            if kw in h1_text:
                return True
    # Frontmatter category 匹配
    fm_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if fm_match:
        fm_text = fm_match.group(1)
        cat_match = re.search(r'^category:\s*(.+)$', fm_text, re.MULTILINE)
        if cat_match:
            cat_val = cat_match.group(1).strip().strip('"\'')
            if cat_val in moc_keywords:
                return True
    return False


def check_frontmatter(filepath):
    """检查 Frontmatter YAML 可解析性和 ``` 混入"""
    issues = []
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        content = f.read()

    if not content.startswith('---'):
        issues.append('缺少 Frontmatter')
        return issues

    end = content.find('\n---', 3)
    if end == -1:
        issues.append('Frontmatter 未闭合（缺少第二个 ---）')
        return issues

    fm_text = content[3:end].strip()

    # 检查 ``` 混入
    if BT in fm_text:
        count = fm_text.count(BT)
        issues.append(f'Frontmatter 中混入 {count} 个 ``` 标记')

    # 检查 pre 字段格式
    pre_match = re.search(r'^pre:\s*(.+)$', fm_text, re.MULTILINE)
    if pre_match:
        pre_val = pre_match.group(1).strip()
        if pre_val != '[]' and not pre_val.startswith('['):
            issues.append(f'pre 字段格式错误: {pre_val[:50]}')
        elif '[[' in pre_val and '"[[' not in pre_val:
            issues.append('pre 字段双链未用双引号包裹')

    # YAML 解析验证
    if HAS_YAML:
        try:
            data = yaml.safe_load(fm_text)
            if not isinstance(data, dict):
                issues.append(f'YAML 解析结果不是 dict: {type(data)}')
            else:
                required = ['title', 'tags', 'category', 'created', 'updated',
                           'difficulty', 'status', 'priority', 'pre', 'aliases']
                missing = [k for k in required if k not in data]
                if missing:
                    issues.append(f'缺少字段: {", ".join(missing)}')
        except Exception as e:
            issues.append(f'YAML 解析错误: {str(e)[:80]}')

    return issues


def check_codeblocks(filepath):
    """检查代码块开闭平衡和结束标记纯净度"""
    issues = []
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        lines = f.read().replace('\r\n', '\n').replace('\r', '\n').split('\n')

    in_code = False
    cml = 0
    open_line = 0
    mermaid_count = 0
    total_blocks = 0
    bad_closing = 0

    for i, line in enumerate(lines):
        s = line.strip()
        m = re.match(r'^(`+)', s)
        if m and len(m.group(1)) >= 3:
            bt_count = len(m.group(1))
            if not in_code:
                in_code = True
                cml = bt_count
                open_line = i + 1
                total_blocks += 1
                lang = s[bt_count:].strip()
                if lang == 'mermaid':
                    mermaid_count += 1
            elif bt_count >= cml:
                # 检查结束标记是否带语言名
                closing_lang = s[bt_count:].strip()
                if closing_lang:
                    bad_closing += 1
                    issues.append(f'L{i+1}: 结束标记带语言名 ```{closing_lang}')
                in_code = False
                cml = 0
            # else: 内部的短反引号，忽略

    if in_code:
        issues.append(f'未闭合代码块（起始行 L{open_line}）')

    if bad_closing > 0:
        issues.append(f'共 {bad_closing} 个结束标记带语言名')

    return issues, total_blocks, mermaid_count


def check_headers(filepath):
    """检查标题级别（H1数量、级别跳跃、H2数量异常、代码模式检测）

    返回 (issues列表, 统计dict)
    统计dict包含: h1_count, h2_count, h3_count, h4_count, is_moc
    """
    issues = []
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        content = f.read()
    lines = content.replace('\r\n', '\n').replace('\r', '\n').split('\n')

    # MOC 检测
    is_moc = is_moc_document(filepath, content)

    in_code = False
    cml = 0
    h1_count = 0
    h2_count = 0
    h3_count = 0
    h4_count = 0
    headers = []  # (line_num, level, text)

    for i, line in enumerate(lines):
        s = line.strip()
        m = re.match(r'^(`+)', s)
        if m and len(m.group(1)) >= 3:
            bt_count = len(m.group(1))
            if not in_code:
                in_code = True
                cml = bt_count
            elif bt_count >= cml:
                in_code = False
                cml = 0
            continue

        if in_code:
            continue

        hm = re.match(r'^(#{1,6})\s+', s)
        if hm:
            level = len(hm.group(1))
            text = s[level:].strip()
            headers.append((i + 1, level, text))
            if level == 1:
                h1_count += 1
            elif level == 2:
                h2_count += 1
            elif level == 3:
                h3_count += 1
            elif level == 4:
                h4_count += 1

    if h1_count > 1:
        issues.append(f'多个 H1 标题（{h1_count}个）')
    elif h1_count == 0:
        issues.append('缺少 H1 主标题')

    # 检查级别跳跃
    for idx in range(1, len(headers)):
        prev_level = headers[idx - 1][1]
        curr_level = headers[idx][1]
        if curr_level > prev_level + 1:
            issues.append(
                f'L{headers[idx][0]}: 级别跳跃 H{prev_level}->H{curr_level} '
                f'"{headers[idx][2][:50]}"'
            )

    # H2 数量异常检测（非 MOC）
    if not is_moc:
        if h2_count > 40:
            issues.append(
                f'[严重] H2数量异常（{h2_count}个，正常范围8-15），可能存在代码内容暴露'
            )
        elif h2_count > 25:
            issues.append(
                f'H2数量异常（{h2_count}个，正常范围8-15），可能存在代码内容暴露'
            )

        # 标题文本代码模式检测（H2/H3，非 MOC）
        for line_num, level, text in headers:
            if level in (2, 3):
                is_cp, pattern_type = is_code_pattern_heading(text)
                if is_cp:
                    issues.append(
                        f'L{line_num}: H{level}标题匹配代码模式（{pattern_type}）: '
                        f'"{text[:50]}"'
                    )

    stats = {
        'h1_count': h1_count,
        'h2_count': h2_count,
        'h3_count': h3_count,
        'h4_count': h4_count,
        'is_moc': is_moc,
    }

    return issues, stats


def main():
    parser = argparse.ArgumentParser(description='知识库综合验证脚本')
    parser.add_argument('--path', required=True, help='知识库根目录路径')
    parser.add_argument('--check', choices=['frontmatter', 'codeblocks', 'headers', 'all'],
                       default='all', help='检查项')
    parser.add_argument('--all', action='store_true', help='执行全部检查（等同于 --check all）')
    parser.add_argument('--verbose', '-v', action='store_true', help='显示详细信息')
    args = parser.parse_args()

    if args.all:
        args.check = 'all'

    if not os.path.isdir(args.path):
        print(f'错误：路径不存在 - {args.path}')
        sys.exit(1)

    files = find_md_files(args.path)
    print(f'总文件数: {len(files)}')
    print()

    total_issues = 0

    if args.check in ('frontmatter', 'all'):
        print('=' * 60)
        print('=== Frontmatter 检查 ===')
        print('=' * 60)
        fm_errors = 0
        for fp in files:
            issues = check_frontmatter(fp)
            if issues:
                fm_errors += 1
                fname = os.path.basename(fp)
                print(f'\n{fname}:')
                for issue in issues:
                    print(f'  - {issue}')
        print(f'\nFrontmatter 有问题的文件: {fm_errors}/{len(files)}')
        total_issues += fm_errors

    if args.check in ('codeblocks', 'all'):
        print('\n' + '=' * 60)
        print('=== 代码块检查 ===')
        print('=' * 60)
        cb_errors = 0
        total_blocks = 0
        total_mermaid = 0
        for fp in files:
            issues, blocks, mermaid = check_codeblocks(fp)
            total_blocks += blocks
            total_mermaid += mermaid
            if issues:
                cb_errors += 1
                fname = os.path.basename(fp)
                print(f'\n{fname}:')
                for issue in issues:
                    print(f'  - {issue}')
        print(f'\n代码块有问题的文件: {cb_errors}/{len(files)}')
        print(f'代码块总数: {total_blocks}, Mermaid图总数: {total_mermaid}')
        total_issues += cb_errors

    if args.check in ('headers', 'all'):
        print('\n' + '=' * 60)
        print('=== 标题级别检查 ===')
        print('=' * 60)
        hd_errors = 0
        total_h1 = 0
        total_h2 = 0
        total_h3 = 0
        total_h4 = 0
        max_h2 = 0
        max_h2_file = ''
        moc_count = 0

        for fp in files:
            issues, stats = check_headers(fp)
            total_h1 += stats['h1_count']
            total_h2 += stats['h2_count']
            total_h3 += stats['h3_count']
            total_h4 += stats['h4_count']
            if stats['is_moc']:
                moc_count += 1
            if stats['h2_count'] > max_h2:
                max_h2 = stats['h2_count']
                max_h2_file = os.path.basename(fp)
            if issues:
                hd_errors += 1
                fname = os.path.basename(fp)
                moc_tag = ' [MOC]' if stats['is_moc'] else ''
                print(f'\n{fname}{moc_tag}:')
                for issue in issues:
                    print(f'  - {issue}')

        avg_h1 = total_h1 / len(files) if files else 0
        avg_h2 = total_h2 / len(files) if files else 0
        avg_h3 = total_h3 / len(files) if files else 0
        avg_h4 = total_h4 / len(files) if files else 0

        print(f'\n标题有问题的文件: {hd_errors}/{len(files)}')
        print(f'平均标题数: H1={avg_h1:.1f}, H2={avg_h2:.1f}, H3={avg_h3:.1f}, H4={avg_h4:.1f}')
        if max_h2_file:
            warning = ' ⚠️' if max_h2 > 25 else ''
            print(f'H2最多: {max_h2_file} ({max_h2}个){warning}')
        if moc_count > 0:
            print(f'MOC类文档: {moc_count}个（跳过H2数量检查和代码模式检测）')
        total_issues += hd_errors

    print('\n' + '=' * 60)
    if total_issues == 0:
        print('✅ 全部检查通过！')
    else:
        print(f'⚠️  共 {total_issues} 个文件存在问题，请运行对应修复脚本')
    print('=' * 60)

    return 0 if total_issues == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
