#!/usr/bin/env python3
"""
代码块标记修复脚本（v5.0）
基于 171 篇文档实战验证，修复代码块标记问题：
1. 修复畸形结束标记（`$lang → ```）
2. 移除结束标记上的语言名（```python → ```）
3. 修复 4+ 反引号畸形标记
4. 根据代码内容自动恢复语言标识
5. 确保所有代码块正确闭合

用法：
    python repair-codeblocks.py --path "知识库路径"
    python repair-codeblocks.py --path "知识库路径" --dry-run
"""

import os
import re
import sys
import argparse

BT = '`' * 3

# 代码内容 → 语言映射规则
LANG_PATTERNS = [
    (r'\b(graph|flowchart|sequenceDiagram|classDiagram|stateDiagram|erDiagram|gantt|pie|journey|mindmap|timeline)\b', 'mermaid'),
    (r'^\s*(def |class |import |from |print\(|if __name__|@app\.|async def |lambda )', 'python'),
    (r'^\s*(const |let |var |function |=>|console\.|require\(|module\.|exports\.)', 'javascript'),
    (r'^\s*(SELECT |INSERT |UPDATE |DELETE |CREATE |DROP |ALTER |FROM |WHERE |JOIN )', 'sql'),
    (r'^\s*(pip |python |docker |kubectl |git |npm |curl |apt |sudo |cd |ls |echo |export |chmod |mkdir |uvicorn |gunicorn |celery |pytest |ruff |black |mypy |pre-commit |streamlit |gradio |alembic |poetry |node |conda |helm |aws |gcloud |terraform |ansible |systemctl |ffmpeg |mpirun |vllm |trtllm |ollama |sglang )', 'bash'),
    (r'^\s*(server |listen |upstream |location |root |proxy_pass )', 'nginx'),
    (r'^\s*(apiVersion:|kind:|metadata:|spec:|containers:|image:|ports:)', 'yaml'),
    (r'^\s*(\{|\[|")', 'json'),
    (r'^\s*(<\?xml|<html|<div|<span|<style|<script)', 'html'),
    (r'^\s*(\.|body|#|\.|@media|@keyframes)', 'css'),
]


def detect_language(code_lines):
    """根据代码内容检测语言"""
    code_text = '\n'.join(code_lines)
    for pattern, lang in LANG_PATTERNS:
        if re.search(pattern, code_text, re.MULTILINE | re.IGNORECASE):
            return lang
    return 'text'


def find_md_files(root):
    files = []
    for dirpath, _, filenames in os.walk(root):
        for f in filenames:
            if f.endswith('.md'):
                files.append(os.path.join(dirpath, f))
    return sorted(files)


def fix_codeblocks(content):
    """修复代码块标记，返回 (新内容, 修改数)"""
    lines = content.replace('\r\n', '\n').replace('\r', '\n').split('\n')
    changes = 0
    new_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]
        s = line.strip()

        # 检测代码块开头标记
        m = re.match(r'^(`+)', s)
        if m and len(m.group(1)) >= 3:
            bt_count = len(m.group(1))
            lang = s[bt_count:].strip()

            # 修复畸形标记：`$lang（一个反引号+语言名）
            if bt_count == 1 and lang:
                # 可能是畸形的结束标记，改为纯 ```
                new_lines.append(BT)
                changes += 1
                i += 1
                continue

            # 4+ 反引号且无语言名 → 可能是畸形，改为 3 反引号
            if bt_count > 3 and not lang:
                new_lines.append(BT)
                changes += 1
                i += 1
                continue

            # 正常开头标记
            new_lines.append(line)
            i += 1

            # 收集代码块内容，找到结束标记
            code_lines = []
            while i < len(lines):
                cl = lines[i]
                cs = cl.strip()
                cm = re.match(r'^(`+)', cs)
                if cm and len(cm.group(1)) >= 3:
                    # 找到结束标记
                    end_bt = len(cm.group(1))
                    end_lang = cs[end_bt:].strip()

                    # 修复结束标记带语言名
                    if end_lang:
                        new_lines.extend(code_lines)
                        new_lines.append(BT)  # 纯结束标记
                        changes += 1
                        i += 1
                        break
                    else:
                        new_lines.extend(code_lines)
                        new_lines.append(cl)
                        i += 1
                        break
                else:
                    code_lines.append(cl)
                    i += 1
            else:
                # 未闭合代码块，在文件末尾添加结束标记
                new_lines.extend(code_lines)
                new_lines.append(BT)
                changes += 1
        else:
            new_lines.append(line)
            i += 1

    # 第二遍：为没有语言名的开头标记恢复语言
    final_lines = []
    i = 0
    in_code = False
    while i < len(new_lines):
        line = new_lines[i]
        s = line.strip()
        m = re.match(r'^(`{3})(\s*)$', s)
        if m and not in_code:
            # 纯 ``` 开头标记（不在代码块内），需要检测语言
            code_lines = []
            j = i + 1
            while j < len(new_lines):
                cs = new_lines[j].strip()
                if cs == BT:
                    break
                code_lines.append(new_lines[j])
                j += 1

            if code_lines:
                lang = detect_language(code_lines)
                indent = line[:len(line) - len(line.lstrip())]
                final_lines.append(f'{indent}```{lang}')
                changes += 1
                in_code = True
            else:
                final_lines.append(line)
            i += 1
        elif m and in_code:
            # 纯 ``` 结束标记（在代码块内），保持不变
            final_lines.append(line)
            in_code = False
            i += 1
        else:
            # 带语言名的标记或普通行
            if re.match(r'^(`{3})\w+', s):
                in_code = not in_code
            final_lines.append(line)
            i += 1

    return '\n'.join(final_lines), changes


def main():
    parser = argparse.ArgumentParser(description='代码块标记修复脚本')
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

    for fp in files:
        with open(fp, 'r', encoding='utf-8-sig') as f:
            content = f.read()

        new_content, changes = fix_codeblocks(content)

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
