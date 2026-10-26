#!/usr/bin/env python3
"""
标题级别修复脚本（v5.1）
基于 171 篇文档实战验证，修复标题级别问题：
1. 将多余 H1 降级为 H2
2. 修复 H2→H4 级别跳跃（降级 H4 为 H3）
3. 识别并包裹暴露的代码注释（#开头且相邻代码行）
4. H2 数量异常检测与告警
5. 标题文本代码模式识别与代码内容自动包裹（H2/H3）
6. 装饰性分隔线识别与转换
7. MOC/枢纽文档例外处理
8. 子章节标题智能降级

用法：
    python repair-headers.py --path "知识库路径"
    python repair-headers.py --path "知识库路径" --dry-run
"""

import os
import re
import sys
import argparse

BT = '`' * 3

# 统一命令行工具前缀列表（looks_like_code / is_code_comment / is_code_pattern_heading / detect_code_language 共用）
COMMAND_PREFIXES = (
    r'pip|python|docker|kubectl|git|npm|curl|apt|sudo|cd|ls|echo|export|'
    r'chmod|mkdir|uvicorn|gunicorn|celery|pytest|ruff|black|mypy|pre-commit|'
    r'streamlit|gradio|alembic|poetry|node|conda|helm|aws|gcloud|terraform|'
    r'ansible|systemctl|ffmpeg|mpirun|vllm|trtllm|ollama|sglang|wget|tar|'
    r'gzip|ssh|scp|rsync|make|cmake|gcc|g\+\+|java|javac|mvn|gradle|go|rustc|cargo'
)


def looks_like_code(line):
    """判断一行是否像代码"""
    s = line.strip()
    if not s:
        return False
    if re.match(r'^#{1,6}\s+', s):
        return False
    if s.startswith(('- ', '* ', '+ ', '>', '|', '```', '~~~', '![')):
        return False
    if re.match(r'^(-{3,}|\*{3,}|_{3,})$', s):
        return False
    # 代码特征
    if re.search(r'^[a-zA-Z_][\w.]*\s*\(', s): return True
    if re.search(r'^[a-zA-Z_][\w.]*\s*=\s*', s): return True
    if re.search(r'^(def|class|import|from|return|if|elif|else|for|while|try|except|with|async|await|yield|raise|pass|break|continue|lambda)\b', s): return True
    if re.search(r'^@\w+', s): return True
    if re.search(r'^(const|let|var|function|console|require|module|exports|interface|type)\b', s): return True
    if re.search(r'^(SELECT|INSERT|UPDATE|DELETE|CREATE|DROP|ALTER|FROM|WHERE|JOIN)\b', s, re.I): return True
    if re.search(r'^(' + COMMAND_PREFIXES + r')\s', s, re.I): return True
    if re.search(r'^[A-Z_][A-Z0-9_]*\s*=', s): return True
    if re.search(r'\\$', s): return True
    if re.search(r'^\s+\S', s): return True
    if re.search(r'\\[dwsWSDbBAZ]|\(\?[=!]|\[\^?[^\]]*\]|\{\d+,?\d*\}', s): return True
    if re.search(r'[+\-*/%]=|==|!=|<=|>=|&&|\|\||->|=>|::', s): return True
    return False


def is_code_comment(line, prev_line, next_line):
    """判断 H1 行是否实际是代码注释"""
    s = line.strip()
    if not re.match(r'^#\s+', s):
        return False
    # 相邻代码行 → 是代码注释
    if prev_line and looks_like_code(prev_line):
        return True
    if next_line and looks_like_code(next_line):
        return True
    # 包含代码符号
    if any(c in s for c in ['--', '(', ')', '=', '{', '}', '[', ']', '|', '>', '<', ';', "'", '"']):
        return True
    if re.match(r'^#\s+\d+[\.、]', s):
        return True
    if re.search(r'\b(' + COMMAND_PREFIXES + r')\b', s, re.I):
        return True
    return False


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


def is_decorative_separator(text):
    """判断是否为装饰性分隔线标题，返回 (是否匹配, 内部文本)"""
    m = re.match(r'^[=\-*]{3,}\s*(.+?)\s*[=\-*]{3,}$', text)
    if m:
        return True, m.group(1)
    return False, ''


def detect_code_language(code_lines):
    """根据代码块内容判断语言，返回语言标签（默认 text）"""
    text = '\n'.join(code_lines)
    # mermaid
    if re.search(r'^\s*(graph|flowchart|sequenceDiagram|classDiagram|stateDiagram|gantt|pie|erDiagram)\b', text, re.MULTILINE):
        return 'mermaid'
    # python
    if re.search(r'^\s*(def|class|import|from|print)\s+\w+', text, re.MULTILINE):
        return 'python'
    # bash / shell
    if re.search(r'^\s*(' + COMMAND_PREFIXES + r')\b', text, re.MULTILINE):
        return 'bash'
    # sql
    if re.search(r'^\s*(SELECT|INSERT|UPDATE|DELETE|CREATE|DROP|ALTER)\b', text, re.MULTILINE):
        return 'sql'
    # yaml / config（多行 key: value 格式，且不含代码块符号）
    yaml_lines = re.findall(r'^\s*[\w.-]+\s*:\s*\S+', text, re.MULTILINE)
    if len(yaml_lines) >= 2 and not re.search(r'[;{}]|\bdef \b|\bclass \b', text):
        return 'yaml'
    return 'text'


def looks_like_code_or_comment(line):
    """判断一行是否像代码或代码注释（用于代码块扩展）"""
    s = line.strip()
    if not s:
        return False
    # 标题行：检查标题文本是否匹配代码模式，或 H1 代码注释
    hm = re.match(r'^(#{1,6})\s+', s)
    if hm:
        text = s[len(hm.group(1)):].strip()
        is_code, _ = is_code_pattern_heading(text)
        if is_code:
            return True
        # 兼容现有 H1 代码注释逻辑
        if hm.group(1) == '#' and is_code_comment(line, '', ''):
            return True
        return False
    # 非标题行：用现有 looks_like_code
    if looks_like_code(line):
        return True
    # 非标题注释行（#后无空格，或 // 注释）
    if re.match(r'^#{1,6}\S', s):
        return True
    if re.match(r'^//', s):
        return True
    if re.match(r'^/\*', s) or re.match(r'^\s*\*', s) or s.endswith('*/'):
        return True
    return False


def expand_code_block(lines, start_idx, wrapped_ranges=None):
    """从 start_idx 向前向后扩展连续代码行块，返回 (group_start, group_end)

    wrapped_ranges: 已包裹的代码块范围列表 [(start, end), ...]，扩展时不越过这些范围
    """
    if wrapped_ranges is None:
        wrapped_ranges = []

    def in_wrapped(idx):
        return any(ws <= idx <= we for ws, we in wrapped_ranges)

    group_start = start_idx
    group_end = start_idx

    # 向前扩展
    j = start_idx - 1
    while j >= 0 and not in_wrapped(j):
        ps = lines[j].strip()
        if not ps:
            if j > 0 and looks_like_code_or_comment(lines[j - 1]):
                group_start = j
                j -= 1
                continue
            break
        if looks_like_code_or_comment(lines[j]):
            group_start = j
            j -= 1
        else:
            break

    # 向后扩展
    j = start_idx + 1
    while j < len(lines) and not in_wrapped(j):
        ns = lines[j].strip()
        if not ns:
            if j + 1 < len(lines) and looks_like_code_or_comment(lines[j + 1]):
                group_end = j
                j += 1
                continue
            break
        if looks_like_code_or_comment(lines[j]):
            group_end = j
            j += 1
        else:
            break

    return group_start, group_end


def find_md_files(root):
    """递归查找所有 .md 文件"""
    files = []
    for dirpath, _, filenames in os.walk(root):
        for f in filenames:
            if f.endswith('.md'):
                files.append(os.path.join(dirpath, f))
    return sorted(files)


def fix_headers(content, filepath=''):
    """修复标题级别，返回 (新内容, 总修改数, 统计dict)

    统计dict包含: h1_downgraded, code_wrapped, jump_fixed,
    decorative_converted, subsection_downgraded, h2_count_before,
    h2_count_after, is_moc
    """
    lines = content.replace('\r\n', '\n').replace('\r', '\n').split('\n')

    stats = {
        'h1_downgraded': 0,
        'code_wrapped': 0,
        'jump_fixed': 0,
        'decorative_converted': 0,
        'subsection_downgraded': 0,
        'h2_count_before': 0,
        'h2_count_after': 0,
        'is_moc': False,
    }

    # MOC 检测
    stats['is_moc'] = is_moc_document(filepath, content)

    # 第一遍：收集所有非代码块内的标题，统计 H2 数量
    in_code = False
    cml = 0
    headers = []  # (index, level, text, raw_line)
    h2_count = 0

    for i, line in enumerate(lines):
        s = line.strip()
        m = re.match(r'^(`+)', s)
        if m and len(m.group(1)) >= 3:
            bt_count = len(m.group(1))
            if not in_code:
                in_code = True
                cml = bt_count
            elif bt_count >= cml:
                closing_lang = s[bt_count:].strip()
                if closing_lang:
                    print(f'  ⚠️ 代码块关闭标记带语言名 ```{closing_lang}（视为损坏但仍关闭）')
                in_code = False
                cml = 0
            continue
        if in_code:
            continue

        hm = re.match(r'^(#{1,6})\s+', s)
        if hm:
            level = len(hm.group(1))
            text = s[level:].strip()
            headers.append((i, level, text, s))
            if level == 2:
                h2_count += 1

    stats['h2_count_before'] = h2_count

    # H2 数量异常告警（非 MOC，修复前输出）
    if not stats['is_moc'] and h2_count > 25:
        severity = '严重' if h2_count > 40 else '警告'
        fname = os.path.basename(filepath) if filepath else '(unknown)'
        print(f'  ⚠️ [{severity}] {fname}: H2数量异常（{h2_count}个），可能存在代码内容暴露为标题的问题')

    # 第二遍：修复多余 H1（现有逻辑，保持不变）
    new_lines = list(lines)
    offset = 0  # H1 包裹导致的行偏移
    h1_wrapped_ranges = []  # 已包裹的代码块范围，防止重叠

    h1_count = 0
    for idx, level, text, raw in headers:
        if level == 1:
            h1_count += 1
            if h1_count > 1:
                adj_idx = idx + offset
                # 检查是否已落入某个已包裹范围
                if any(ws <= adj_idx <= we for ws, we in h1_wrapped_ranges):
                    continue
                line = new_lines[adj_idx]
                # 找上一个非空行（最多回溯2行，跳过空行）
                prev_line = ''
                for j in range(adj_idx - 1, max(adj_idx - 3, -1), -1):
                    if new_lines[j].strip():
                        prev_line = new_lines[j]
                        break
                # 找下一个非空行（最多看2行，跳过空行）
                next_line = ''
                for j in range(adj_idx + 1, min(adj_idx + 3, len(new_lines))):
                    if new_lines[j].strip():
                        next_line = new_lines[j]
                        break

                if is_code_comment(line, prev_line, next_line):
                    # 是代码注释，包裹进代码块（现有扩展逻辑）
                    group_start = adj_idx
                    group_end = adj_idx
                    # 向前扩展
                    j = adj_idx - 1
                    while j >= 0:
                        ps = new_lines[j].strip()
                        if not ps:
                            if j > 0 and (looks_like_code(new_lines[j-1]) or is_code_comment(new_lines[j-1], '', '')):
                                group_start = j
                                j -= 1
                                continue
                            break
                        if looks_like_code(new_lines[j]) or is_code_comment(new_lines[j], '', ''):
                            group_start = j
                            j -= 1
                        else:
                            break
                    # 向后扩展
                    j = adj_idx + 1
                    while j < len(new_lines):
                        ns = new_lines[j].strip()
                        if not ns:
                            if j + 1 < len(new_lines) and (looks_like_code(new_lines[j+1]) or is_code_comment(new_lines[j+1], '', '')):
                                group_end = j
                                j += 1
                                continue
                            break
                        if looks_like_code(new_lines[j]) or is_code_comment(new_lines[j], '', ''):
                            group_end = j
                            j += 1
                        else:
                            break
                    if group_end > group_start:
                        lang = detect_code_language(new_lines[group_start:group_end + 1])
                        open_tag = BT + lang if lang else BT
                        new_lines.insert(group_end + 1, BT)
                        new_lines.insert(group_start, open_tag)
                        h1_wrapped_ranges.append((group_start, group_end + 2))
                        offset += 2
                        stats['code_wrapped'] += 1
                else:
                    # 是实际标题，降级为 H2
                    indent = line[:len(line) - len(line.lstrip())]
                    new_lines[adj_idx] = indent + '## ' + line.lstrip('#').strip()
                    stats['h1_downgraded'] += 1

    # 第三遍：H2/H3 代码模式标题 → 自动包裹进代码块（非 MOC）
    if not stats['is_moc']:
        # 重新扫描标题（H1 修复后行号可能变化）
        in_code = False
        cml = 0
        code_headers = []  # (index, level, text)
        for i, line in enumerate(new_lines):
            s = line.strip()
            m = re.match(r'^(`+)', s)
            if m and len(m.group(1)) >= 3:
                bt_count = len(m.group(1))
                if not in_code:
                    in_code = True
                    cml = bt_count
                elif bt_count >= cml:
                    closing_lang = s[bt_count:].strip()
                    if closing_lang:
                        print(f'  ⚠️ 代码块关闭标记带语言名 ```{closing_lang}（视为损坏但仍关闭）')
                    in_code = False
                    cml = 0
                continue
            if in_code:
                continue
            hm = re.match(r'^(#{1,6})\s+', s)
            if hm:
                level = len(hm.group(1))
                text = s[level:].strip()
                if level in (2, 3):
                    is_cp, _ = is_code_pattern_heading(text)
                    if is_cp:
                        code_headers.append((i, level, text))

        # 倒序处理，避免插入导致行号偏移
        wrapped_ranges = []
        for idx, level, text in reversed(code_headers):
            # 检查是否已落入某个已包裹范围
            if any(ws <= idx <= we for ws, we in wrapped_ranges):
                continue
            # 再次确认该行仍是标题且匹配代码模式
            if idx >= len(new_lines):
                continue
            s = new_lines[idx].strip()
            hm = re.match(r'^(#{1,6})\s+', s)
            if not hm:
                continue
            heading_text = s[len(hm.group(1)):].strip()
            is_cp, _ = is_code_pattern_heading(heading_text)
            if not is_cp:
                continue

            # 扩展代码块并包裹
            group_start, group_end = expand_code_block(new_lines, idx, wrapped_ranges)
            if group_end >= group_start:
                lang = detect_code_language(new_lines[group_start:group_end + 1])
                open_tag = BT + lang if lang else BT
                new_lines.insert(group_end + 1, BT)
                new_lines.insert(group_start, open_tag)
                wrapped_ranges.append((group_start, group_end + 2))  # +2 因为插入了两行
                stats['code_wrapped'] += 1

    # 第四遍：装饰性分隔线转换（=== xxx === → **xxx**）
    in_code = False
    cml = 0
    for i, line in enumerate(new_lines):
        s = line.strip()
        m = re.match(r'^(`+)', s)
        if m and len(m.group(1)) >= 3:
            bt_count = len(m.group(1))
            if not in_code:
                in_code = True
                cml = bt_count
            elif bt_count >= cml:
                closing_lang = s[bt_count:].strip()
                if closing_lang:
                    print(f'  ⚠️ 代码块关闭标记带语言名 ```{closing_lang}（视为损坏但仍关闭）')
                in_code = False
                cml = 0
            continue
        if in_code:
            continue
        hm = re.match(r'^(#{1,6})\s+', s)
        if hm:
            text = s[len(hm.group(1)):].strip()
            is_dec, inner = is_decorative_separator(text)
            if is_dec:
                indent = line[:len(line) - len(line.lstrip())]
                new_lines[i] = indent + '**' + inner + '**'
                stats['decorative_converted'] += 1

    # 第五遍：子章节标题智能降级（非 MOC，H2 仍 > 25 时）
    if not stats['is_moc']:
        in_code = False
        cml = 0
        h2_indices = []
        for i, line in enumerate(new_lines):
            s = line.strip()
            m = re.match(r'^(`+)', s)
            if m and len(m.group(1)) >= 3:
                bt_count = len(m.group(1))
                if not in_code:
                    in_code = True
                    cml = bt_count
                elif bt_count >= cml:
                    closing_lang = s[bt_count:].strip()
                    if closing_lang:
                        print(f'  ⚠️ 代码块关闭标记带语言名 ```{closing_lang}（视为损坏但仍关闭）')
                    in_code = False
                    cml = 0
                continue
            if in_code:
                continue
            if re.match(r'^##\s+', s):
                h2_indices.append(i)

        downgraded = set()
        # 数字.数字格式（如"2.1 核心机制"）→ 始终判定为子章节并降级为 H3
        for curr_idx in h2_indices:
            line = new_lines[curr_idx]
            text = line.lstrip('#').strip()
            if re.match(r'^\d+\.\d+', text):
                indent = line[:len(line) - len(line.lstrip())]
                new_lines[curr_idx] = indent + '### ' + text
                stats['subsection_downgraded'] += 1
                downgraded.add(curr_idx)

        # 连续 H2（中间只有空行）→ 第二个及以后降级为 H3（仅 H2>25 时）
        if len(h2_indices) > 25:
            for k in range(1, len(h2_indices)):
                prev_idx = h2_indices[k - 1]
                curr_idx = h2_indices[k]
                if curr_idx in downgraded or prev_idx in downgraded:
                    continue
                has_content = False
                for j in range(prev_idx + 1, curr_idx):
                    if new_lines[j].strip():
                        has_content = True
                        break
                if not has_content:
                    line = new_lines[curr_idx]
                    indent = line[:len(line) - len(line.lstrip())]
                    text = line.lstrip('#').strip()
                    new_lines[curr_idx] = indent + '### ' + text
                    stats['subsection_downgraded'] += 1
                    downgraded.add(curr_idx)

    # 第六遍：修复 H2→H4 级别跳跃（现有逻辑）
    in_code = False
    cml = 0
    prev_level = None
    for i, line in enumerate(new_lines):
        s = line.strip()
        m = re.match(r'^(`+)', s)
        if m and len(m.group(1)) >= 3:
            bt_count = len(m.group(1))
            if not in_code:
                in_code = True
                cml = bt_count
            elif bt_count >= cml:
                closing_lang = s[bt_count:].strip()
                if closing_lang:
                    print(f'  ⚠️ 代码块关闭标记带语言名 ```{closing_lang}（视为损坏但仍关闭）')
                in_code = False
                cml = 0
            continue
        if in_code:
            continue

        hm = re.match(r'^(#{1,6})\s+', s)
        if hm:
            level = len(hm.group(1))
            if prev_level == 2 and level == 4:
                # H2→H4 跳跃，降级 H4 为 H3
                indent = line[:len(line) - len(line.lstrip())]
                new_lines[i] = indent + '### ' + line.lstrip('#').strip()
                stats['jump_fixed'] += 1
                level = 3
            prev_level = level

    # 统计修复后 H2 数量
    in_code = False
    cml = 0
    h2_after = 0
    for line in new_lines:
        s = line.strip()
        m = re.match(r'^(`+)', s)
        if m and len(m.group(1)) >= 3:
            bt_count = len(m.group(1))
            if not in_code:
                in_code = True
                cml = bt_count
            elif bt_count >= cml:
                closing_lang = s[bt_count:].strip()
                if closing_lang:
                    print(f'  ⚠️ 代码块关闭标记带语言名 ```{closing_lang}（视为损坏但仍关闭）')
                in_code = False
                cml = 0
            continue
        if in_code:
            continue
        if re.match(r'^##\s+', s):
            h2_after += 1
    stats['h2_count_after'] = h2_after

    total_changes = (stats['h1_downgraded'] + stats['code_wrapped'] +
                      stats['jump_fixed'] + stats['decorative_converted'] +
                      stats['subsection_downgraded'])

    return '\n'.join(new_lines), total_changes, stats


def main():
    parser = argparse.ArgumentParser(description='标题级别修复脚本')
    parser.add_argument('--path', required=True, help='知识库根目录路径')
    parser.add_argument('--dry-run', action='store_true', help='预览模式')
    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f'错误：路径不存在 - {args.path}')
        sys.exit(1)

    files = find_md_files(args.path)
    print(f'总文件数: {len(files)}')
    print()

    total_changes = 0
    files_modified = 0
    h2_anomaly_files = []  # (filename, before, after)

    # 汇总统计
    sum_h1_downgraded = 0
    sum_code_wrapped = 0
    sum_jump_fixed = 0
    sum_decorative_converted = 0
    sum_subsection_downgraded = 0

    for fp in files:
        with open(fp, 'r', encoding='utf-8-sig') as f:
            content = f.read()

        new_content, changes, stats = fix_headers(content, fp)

        if stats['h2_count_before'] > 25 and not stats['is_moc']:
            h2_anomaly_files.append((
                os.path.basename(fp),
                stats['h2_count_before'],
                stats['h2_count_after']
            ))

        if changes > 0:
            files_modified += 1
            total_changes += changes
            fname = os.path.basename(fp)
            detail_parts = []
            if stats['h1_downgraded']:
                detail_parts.append(f"H1降级{stats['h1_downgraded']}")
            if stats['code_wrapped']:
                detail_parts.append(f"代码包裹{stats['code_wrapped']}")
            if stats['jump_fixed']:
                detail_parts.append(f"跳跃修复{stats['jump_fixed']}")
            if stats['decorative_converted']:
                detail_parts.append(f"装饰线转换{stats['decorative_converted']}")
            if stats['subsection_downgraded']:
                detail_parts.append(f"子章节降级{stats['subsection_downgraded']}")
            detail = ', '.join(detail_parts) if detail_parts else f'{changes}处'
            print(f'{fname}: 修复 {changes} 处（{detail}）')

            sum_h1_downgraded += stats['h1_downgraded']
            sum_code_wrapped += stats['code_wrapped']
            sum_jump_fixed += stats['jump_fixed']
            sum_decorative_converted += stats['decorative_converted']
            sum_subsection_downgraded += stats['subsection_downgraded']

            if not args.dry_run:
                with open(fp, 'w', encoding='utf-8', newline='\n') as f:
                    f.write(new_content)

    # 汇总输出
    print(f'\n{"=" * 60}')
    print(f'总计: 修复 {total_changes} 处，涉及 {files_modified} 个文件')
    print(f'  H1降级: {sum_h1_downgraded}, 代码包裹: {sum_code_wrapped}, '
          f'跳跃修复: {sum_jump_fixed}, 装饰线转换: {sum_decorative_converted}, '
          f'子章节降级: {sum_subsection_downgraded}')

    if h2_anomaly_files:
        print(f'\nH2数量异常文件（修复前后对比）:')
        for fname, before, after in h2_anomaly_files:
            delta = before - after
            print(f'  {fname}: {before} → {after} (减少{delta})')

    if args.dry_run:
        print('\n（预览模式，未写入文件）')


if __name__ == '__main__':
    main()
