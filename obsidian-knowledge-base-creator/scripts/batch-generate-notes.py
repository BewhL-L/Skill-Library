#!/usr/bin/env python3
"""
批量生成标准化笔记脚本
从 JSON/YAML 列表文件批量生成多个标准化笔记

用法:
    python batch-generate-notes.py --list notes.json --kb-root ./my-kb
    python batch-generate-notes.py --list notes.yaml --kb-root ./my-kb --dry-run

列表文件格式（JSON）:
[
  {"title": "Vue3 响应式原理", "category": "前端开发", "difficulty": 3, "tags": ["Vue3", "前端"]},
  {"title": "Redis 缓存策略", "category": "数据库与缓存", "difficulty": 3, "tags": ["Redis", "缓存"]}
]

列表文件格式（YAML）:
- title: Vue3 响应式原理
  category: 前端开发
  difficulty: 3
  tags: [Vue3, 前端]
- title: Redis 缓存策略
  category: 数据库与缓存
  difficulty: 3
  tags: [Redis, 缓存]
"""

import os
import sys
import json
import argparse
from datetime import datetime

# 分类映射
CATEGORY_MAP = {
    "综合导航": "00-综合导航", "前端开发": "01-前端开发",
    "后端开发": "02-后端开发", "数据库与缓存": "03-数据库与缓存",
    "分布式与中间件": "04-分布式与中间件", "云原生与运维": "05-云原生与运维",
    "计算机基础": "06-计算机基础", "通用工具": "07-通用工具",
    "Python全栈": "08-Python全栈", "AI与效率工具": "09-AI与效率工具",
    "项目实战": "99-项目实战",
}

DIFFICULTY_STARS = {1: "⭐", 2: "⭐⭐", 3: "⭐⭐⭐", 4: "⭐⭐⭐⭐", 5: "⭐⭐⭐⭐⭐"}


def resolve_category_dir(category: str, kb_root: str) -> str:
    """解析分类对应的目录名。

    优先在知识库根目录下扫描形如 ``01-前端开发`` 的目录并匹配 ``-{category}``
    后缀（支持自定义分类/编号）；否则回退到内置 CATEGORY_MAP；仍未命中则直接用
    分类名作为目录名。
    """
    if os.path.isdir(kb_root):
        for d in os.listdir(kb_root):
            dp = os.path.join(kb_root, d)
            if os.path.isdir(dp) and '-' in d:
                prefix, suffix = d.split('-', 1)
                if suffix == category:
                    return d
    return CATEGORY_MAP.get(category, category)

def load_list_file(filepath: str) -> dict:
    """加载列表文件（支持JSON和YAML）"""
    if not os.path.exists(filepath):
        print(f"❌ 列表文件不存在: {filepath}")
        return []

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 尝试JSON
    try:
        data = json.loads(content)
        if isinstance(data, list):
            return data
    except json.JSONDecodeError:
        pass

    # 尝试YAML（简单解析，不依赖pyyaml）
    if filepath.endswith('.yaml') or filepath.endswith('.yml'):
        return parse_simple_yaml(content)

    print(f"❌ 无法解析列表文件，请使用 JSON 或 YAML 格式")
    return []

def parse_simple_yaml(content: str) -> dict:
    """简单的YAML解析（仅支持本脚本需要的格式）"""
    items = []
    current_item = None
    current_key = None

    for line in content.split('\n'):
        line = line.rstrip()
        if not line or line.startswith('#'):
            continue

        # 新条目
        if line.startswith('- '):
            if current_item:
                items.append(current_item)
            current_item = {}
            line = line[2:]
            if ':' in line:
                key, value = line.split(':', 1)
                current_item[key.strip()] = parse_value(value.strip())
                current_key = key.strip()
        # 键值对
        elif ':' in line and current_item is not None:
            key, value = line.split(':', 1)
            current_item[key.strip()] = parse_value(value.strip())
            current_key = key.strip()

    if current_item:
        items.append(current_item)

    return items

def parse_value(value: str) -> dict:
    """解析YAML值"""
    value = value.strip()
    # 列表
    if value.startswith('[') and value.endswith(']'):
        inner = value[1:-1]
        if inner:
            return [v.strip().strip('"\'') for v in inner.split(',')]
        return []
    # 数字
    try:
        return int(value)
    except ValueError:
        pass
    # 字符串
    return value.strip('"\'')

def generate_note_content(title: str, category: str, difficulty: str, tags: str = None, pre: str = None) -> dict:
    """生成单篇笔记内容（v2.0 丰富版，与 generate-note.py 一致）"""
    stars = DIFFICULTY_STARS.get(difficulty, "⭐⭐⭐")
    date = datetime.now().strftime('%Y-%m-%d')
    tags_list = tags if tags else [category]
    tags_str = ", ".join(tags_list)
    tags_display = "`#" + "` `#".join(tags_list) + "`"
    pre_str = ", ".join([f"[[{p}]]" for p in pre]) if pre else ""

    return f"""---
title: {title}
tags: [{tags_str}]
category: {category}
created: {date}
updated: {date}
difficulty: {stars}
status: 📝 草稿
priority: 重要
pre: [{pre_str}]
aliases: []
template_version: v2.0
---

# {title}

> 一句话定义：用最简洁的语言说明{title}是什么、解决什么问题、适用场景。

---

## 一、概述

<!-- 填充指引：概述部分占全文15%，用通俗语言解释核心概念，让零基础读者也能理解 -->

### 1.1 什么是 {title}

{{定义说明，用通俗语言解释核心概念}}

### 1.2 为什么需要 {title}

| 痛点/问题 | 解决方案 |
|-----------|---------|
| {{问题1}} | {{解决方案1}} |
| {{问题2}} | {{解决方案2}} |

### 1.3 核心概念

| 概念 | 说明 |
|------|------|
| {{概念1}} | {{说明1}} |
| {{概念2}} | {{说明2}} |

### 1.4 适用场景

- ✅ **适用**：{{适用场景1}}、{{适用场景2}}
- ❌ **不适用**：{{不适用场景1}}

---

## 二、原理

<!-- 填充指引：原理部分占全文30%，深入底层机制，配合架构图和流程图说明 -->

### 2.1 核心原理

{{核心机制、关键算法、工作原理的详细说明}}

```mermaid
graph TD
    A[输入层] --> B[核心处理层]
    B --> C[输出层]
    B --> D[存储层]
    <!-- 填充指引：根据实际技术替换为真实架构图/流程图，可使用 graph/flowchart/sequence 等类型 -->
```

### 2.2 架构设计

| 组件 | 职责 | 关键技术 |
|------|------|---------|
| {{组件1}} | {{职责1}} | {{技术1}} |
| {{组件2}} | {{职责2}} | {{技术2}} |

### 2.3 工作流程

1. **步骤1**：{{说明}}
2. **步骤2**：{{说明}}
3. **步骤3**：{{说明}}

### 2.4 与相关技术对比

| 维度 | {title} | {{对比技术1}} | {{对比技术2}} |
|------|---------|-------------|-------------|
| 性能 | | | |
| 易用性 | | | |
| 生态 | | | |
| 适用场景 | | | |

---

## 三、实操

<!-- 填充指引：实操部分占全文30%，提供可运行的代码示例，从环境搭建到完整项目 -->

### 3.1 环境搭建

```bash
# 安装命令
{{安装命令}}

# 版本要求
{{版本要求}}
```

### 3.2 快速上手

```javascript
// Hello World 示例
{{最小可运行代码}}
```

### 3.3 完整示例

{{完整的可运行代码示例，包含注释说明}}

---

## 四、问题

<!-- 填充指引：问题部分占全文15%，收集真实开发中遇到的错误，给出原因和解决方案 -->

### 4.1 常见错误

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| {{错误1}} | {{原因1}} | {{方案1}} |

### 4.2 踩坑记录

> ⚠️ **踩坑记录1**：{{问题描述}}
> **原因**：{{原因分析}}
> **解决方案**：{{解决方法}}

---

## 五、拓展

<!-- 填充指引：拓展部分占全文10%，介绍进阶用法、生态工具和学习资源 -->

### 5.1 进阶特性

- {{进阶特性1}}
- {{进阶特性2}}

### 5.2 生态工具

| 工具 | 用途 | 推荐度 |
|------|------|--------|
| {{工具1}} | {{用途1}} | ⭐⭐⭐⭐⭐ |
| {{工具2}} | {{用途2}} | ⭐⭐⭐⭐ |

### 5.3 学习资源

- 📖 **官方文档**：{{链接}}
- 📚 **推荐书籍**：{{书名}}
- 🎓 **优质教程**：{{链接}}
- 💬 **社区**：{{社区链接}}

---

## 🔗 关联笔记

- [[{{相关概念1}}]] — {{简要说明}}
- [[{{相关概念2}}]] — {{简要说明}}

## 📖 前置知识

- [[{{前置知识1}}]]
- [[{{前置知识2}}]]

## 🏷️ 相关标签

{tags_display}

---

[[Home|🏠 返回首页]] · [[MOC-{category}|📚 返回分类]] · [[学习路线总览|🗺️ 学习路线]]

---

> 🎯 **使用建议**：
> ① 按五段式结构填充内容，先完成概述和实操，再深入原理
> ② 关键概念可添加 HTML/CSS 动画卡片或 Mermaid 图，提升可读性（参考 advanced-visual-templates.md）
> ③ 完成后将 status 从 📝草稿 改为 ✅内容已完善，并更新对应 MOC 索引
> ④ 添加相关笔记的 `[[]]` 双链，构建知识网络
"""

def main() -> None:
    """主函数"""
    parser = argparse.ArgumentParser(description="批量生成标准化笔记")
    parser.add_argument("--list", required=True, help="笔记列表文件（JSON/YAML）")
    parser.add_argument("--kb-root", required=True, help="知识库根目录")
    parser.add_argument("--dry-run", action="store_true", help="仅显示不执行")
    args = parser.parse_args()

    kb_root = os.path.abspath(args.kb_root)
    if not os.path.exists(kb_root):
        print(f"❌ 知识库根目录不存在: {kb_root}")
        return

    # 加载列表
    notes = load_list_file(args.list)
    if not notes:
        print("❌ 列表文件为空或格式错误")
        return

    print(f"📝 批量生成笔记: {len(notes)} 篇")
    print(f"📂 知识库: {kb_root}")
    if args.dry_run:
        print("  (预览模式，不创建文件)")
    print("=" * 60)

    success_count = 0
    skip_count = 0
    fail_count = 0

    for i, note in enumerate(notes, 1):
        title = note.get('title', '').strip()
        category = note.get('category', '通用工具').strip()
        difficulty = note.get('difficulty', 3)
        tags = note.get('tags', [])
        pre = note.get('pre', [])

        if not title:
            print(f"  ⚠️  第 {i} 篇: 缺少标题，跳过")
            skip_count += 1
            continue

        # 解析分类目录（支持自定义配置分类）
        cat_dir = resolve_category_dir(category, kb_root)
        if category not in CATEGORY_MAP:
            print(f"  ℹ️  第 {i} 篇 [{title}]: 自定义分类 [{category}] -> 目录 [{cat_dir}]")

        # 构造输出路径
        output_path = os.path.join(kb_root, cat_dir, f"{title}.md")

        # 检查是否已存在
        if os.path.exists(output_path):
            print(f"  ⏭️  第 {i} 篇 [{title}]: 已存在，跳过")
            skip_count += 1
            continue

        if args.dry_run:
            stars = DIFFICULTY_STARS.get(difficulty, "⭐⭐⭐")
            print(f"  📋 第 {i} 篇: [{stars}] {title} -> {category}")
            success_count += 1
            continue

        # 生成笔记
        try:
            content = generate_note_content(title, category, difficulty, tags, pre)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            stars = DIFFICULTY_STARS.get(difficulty, "⭐⭐⭐")
            print(f"  ✅ 第 {i} 篇: [{stars}] {title} -> {category}")
            success_count += 1
        except Exception as e:
            print(f"  ❌ 第 {i} 篇 [{title}]: 生成失败 - {e}")
            fail_count += 1

    print("\n" + "=" * 60)
    print(f"📊 批量生成完成:")
    print(f"  总数: {len(notes)}")
    print(f"  成功: {success_count}")
    print(f"  跳过: {skip_count}")
    print(f"  失败: {fail_count}")

    if not args.dry_run and success_count > 0:
        print(f"\n💡 建议运行以下命令更新 MOC:")
        print(f"  python scripts/kb.py standardize --kb-root \"{kb_root}\"")

if __name__ == "__main__":
    main()
