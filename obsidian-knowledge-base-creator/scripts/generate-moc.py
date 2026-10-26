#!/usr/bin/env python3
"""
MOC 内容地图生成脚本
扫描指定目录下的所有笔记，自动生成标准化 MOC

用法:
    python generate-moc.py --category "前端开发" --path "01-前端开发"

v1.1.0: 修复表格中双链管道符未转义导致列数错位的问题，统一表格结构为 文档|说明|难度
"""

import os
import re
import argparse
from datetime import datetime


def extract_frontmatter(filepath: str) -> dict:
    """提取笔记的 Frontmatter"""
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
            return result
    except:
        pass
    return {}


def scan_notes(directory: str) -> list:
    """扫描目录下的所有笔记"""
    notes = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md') and not file.startswith('MOC-'):
                filepath = os.path.join(root, file)
                fm = extract_frontmatter(filepath)
                rel_path = os.path.relpath(filepath, directory)
                notes.append({
                    'title': fm.get('title', file.replace('.md', '')),
                    'filename': file.replace('.md', ''),
                    'difficulty': fm.get('difficulty', '⭐⭐⭐'),
                    'category': fm.get('category', ''),
                    'tags': fm.get('tags', ''),
                    'path': rel_path,
                    'filepath': filepath,
                })
    return notes


def escape_wiki_link(filename: str, title: str) -> str:
    """生成表格中安全的双链，将别名分隔符 | 转义为 \\|

    Markdown 表格中，[[filename|title]] 内的 | 会被误判为列分隔符，
    必须转义为 [[filename\\|title]] 才能保证表格列数正确。
    """
    if filename == title:
        return f"[[{filename}]]"
    return f"[[{filename}\\|{title}]]"


def extract_note_description(filepath: str, title: str) -> str:
    """从笔记内容提取简短说明（用于MOC文档索引表）"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        # 去除 frontmatter
        content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)
        # 查找第一个引用块 > 后面的内容
        quote_match = re.search(r'^>\s*(.+)$', content, re.MULTILINE)
        if quote_match:
            desc = quote_match.group(1).strip()
            if len(desc) > 50:
                desc = desc[:47] + '...'
            return desc
        # 查找第一个非标题、非空行的正文
        for line in content.split('\n'):
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('```') and not line.startswith('|') and not line.startswith('-') and not line.startswith('>'):
                if len(line) > 50:
                    line = line[:47] + '...'
                return line
    except:
        pass
    return title


def generate_moc(category: str, directory: str, notes: list) -> str:
    """生成 MOC 内容"""
    date = datetime.now().strftime('%Y-%m-%d')

    # 按难度分组
    by_difficulty = {}
    for note in notes:
        diff = note['difficulty']
        if diff not in by_difficulty:
            by_difficulty[diff] = []
        by_difficulty[diff].append(note)

    content = f"""---
title: {category} MOC
tags: [MOC, {category}]
category: {category}
created: {date}
updated: {date}
difficulty: ⭐⭐
status: ✅ 内容已完善
priority: 核心
pre: []
aliases: [{category}内容地图, {category}MOC]
hub: true
template_version: v2.0
---

# 📚 {category} MOC

> **内容地图**：{category}领域的内容地图，共 {len(notes)} 篇笔记，涵盖从入门到专家的完整知识体系。
>
> **核心理念**：用导航体系把分散的笔记串起来，让学习者知道"有什么→学什么→怎么学→如何检验"。
>
> **学习建议**：建议从入门级笔记开始，按学习路线循序渐进；遇到具体问题时通过文档索引快速定位。

---

## 📊 导航体系总览

```mermaid
mindmap
  root(({category}))
    入门基础
      基础概念
      核心用法
      快速上手
    进阶实战
      原理深入
      最佳实践
      性能优化
    高级架构
      架构设计
      分布式
      云原生
    专家精通
      源码分析
      前沿技术
      技术输出
```

<!-- 填充指引：根据实际笔记填充 mindmap，每个阶段下列出核心文档 -->

---

## 📚 学习路线

| 阶段 | 周期 | 核心目标 | 关键内容 |
|------|------|---------|---------|
| 🌱 入门筑基 | 0-3月 | 掌握基础概念和核心用法 | 基础概念、核心用法、快速上手 |
| 🌿 进阶提升 | 3-6月 | 深入原理和最佳实践 | 原理深入、最佳实践、性能优化 |
| 🌳 高级精通 | 6-12月 | 掌握架构设计和分布式 | 架构设计、分布式、云原生 |
| 🌲 专家精通 | 12月+ | 源码级理解和技术输出 | 源码分析、前沿技术、技术输出 |

---

## 🗺️ 快速导航

### 我是新手，从哪开始？
1. 先学习 ⭐ 入门级笔记，掌握基础概念
2. 按学习路线表的阶段推进
3. 配合实操部分动手练习

### 我想找某个知识点？
1. 在下方文档索引中按难度查找
2. 使用 Obsidian 全局搜索（Ctrl+O）
3. 查看关联笔记发现相关内容

### 我准备面试？
1. 重点复习 ⭐⭐⭐ 高级和 ⭐⭐⭐⭐ 专家级笔记
2. 关注原理部分和常见错误
3. 参考面试题汇总（如有）

---

## 📂 文档索引

<!-- 填充指引：按难度分组展示所有笔记，表格结构统一为 文档|说明|难度 -->

"""

    # 按难度输出，表格结构统一为：文档 | 说明 | 难度
    difficulty_order = ['⭐', '⭐⭐', '⭐⭐⭐', '⭐⭐⭐⭐', '⭐⭐⭐⭐⭐']
    difficulty_names = {
        '⭐': '🌱 入门级',
        '⭐⭐': '🌿 进阶级',
        '⭐⭐⭐': '🌳 高级',
        '⭐⭐⭐⭐': '🌲 专家级',
        '⭐⭐⭐⭐⭐': '🏔️ 资深级',
    }

    for diff in difficulty_order:
        if diff in by_difficulty:
            content += f"### {difficulty_names[diff]}（{len(by_difficulty[diff])} 篇）\n\n"
            content += "| 文档 | 说明 | 难度 |\n"
            content += "|------|------|------|\n"
            for note in sorted(by_difficulty[diff], key=lambda x: x['title']):
                wiki_link = escape_wiki_link(note['filename'], note['title'])
                desc = extract_note_description(note['filepath'], note['title'])
                content += f"| {wiki_link} | {desc} | {note['difficulty']} |\n"
            content += "\n"

    content += f"""---

## 🔗 知识关联

```
{category}体系
├── 基础概念 ← 入门必备
│   ├── 核心原理 → 深入理解
│   └── 基础用法 → 快速上手
├── 进阶实战 ← 能力提升
│   ├── 最佳实践 → 工程化
│   └── 性能优化 → 调优技巧
└── 高级架构 ← 专家之路
    ├── 架构设计 → 系统设计
    └── 源码分析 → 底层原理
```

---

## 🔗 跨领域 MOC 导航

| 相关领域 | MOC入口 | 关联度 |
|---------|---------|--------|
| 综合导航 | [[MOC-综合导航]] | 中央枢纽 |
| 学习路线 | [[学习路线总览]] | 全局路线 |
| 项目实战 | [[MOC-项目实战]] | 实践应用 |
<!-- 填充指引：根据实际分类添加相关领域 MOC 链接 -->

---

## 📖 学习顺序

1. **入门筑基**：先学习 ⭐ 入门级笔记，掌握基础概念
2. **核心进阶**：学习 ⭐⭐ 进阶级笔记，深入原理和用法
3. **高级实战**：学习 ⭐⭐⭐ 高级笔记，掌握架构和优化
4. **专家精通**：学习 ⭐⭐⭐⭐ 专家级笔记，源码级理解
5. **综合应用**：结合项目实战，将知识融会贯通

---

## 📊 统计信息

| 统计项 | 数量 |
|--------|------|
| **总文档数** | {len(notes)} 篇 |
"""

    for diff in difficulty_order:
        if diff in by_difficulty:
            content += f"| **{diff} {difficulty_names[diff].split(' ')[1]}** | {len(by_difficulty[diff])} 篇 |\n"

    content += f"""
---

## 🏷️ 标签体系

`#{category}` `#MOC` `#内容地图`

---

[[Home|🏠 返回首页]] · [[MOC-综合导航|📚 综合导航]] · [[学习路线总览|🗺️ 学习路线]]

---

> 📝 **MOC 版本**：v2.0 · **自动生成**：generate-moc.py
>
> 💡 **提示**：新增笔记后重新运行本脚本可自动更新文档索引。
"""
    return content


def main() -> None:
    """主函数"""
    parser = argparse.ArgumentParser(description="生成 MOC 内容地图")
    parser.add_argument("--category", required=True, help="分类名称")
    parser.add_argument("--path", required=True, help="笔记目录路径")
    parser.add_argument("--output", help="输出文件路径（默认目录下 MOC-{分类}.md）")
    args = parser.parse_args()

    directory = os.path.abspath(args.path)
    if not os.path.exists(directory):
        print(f"❌ 目录不存在: {directory}")
        return

    # 扫描笔记
    print(f"📂 扫描目录: {directory}")
    notes = scan_notes(directory)
    print(f"📝 发现 {len(notes)} 篇笔记")

    # 生成 MOC
    content = generate_moc(args.category, directory, notes)

    # 输出路径
    if args.output:
        output_path = args.output
    else:
        output_path = os.path.join(directory, f"MOC-{args.category}.md")

    # 写入文件
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ MOC 已生成: {output_path}")
    print(f"📊 索引了 {len(notes)} 篇笔记")
    print(f"📝 表格结构: 文档 | 说明 | 难度（双链管道符已转义）")


if __name__ == "__main__":
    main()
