#!/usr/bin/env python3
"""
死链修复脚本
扫描知识库中的双链，自动修复高频死链（创建对应笔记或添加别名）

用法:
    python fix-deadlinks.py --path "知识库路径"
    python fix-deadlinks.py --path "./my-kb" --threshold 5
    python fix-deadlinks.py --path "./my-kb" --dry-run
"""

import os
import re
import argparse
from datetime import datetime
from collections import defaultdict

# 模板占位符关键词（这些不是真正的死链）
PLACEHOLDER_KEYWORDS = ['{{', '}}', '<', '>', '占位', '模板', '示例', '待填', 'TODO', 'FIXME']

def extract_links(content: str) -> dict:
    """提取所有双链"""
    pattern = r'\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]'
    return re.findall(pattern, content)

def is_placeholder(link_name: str) -> dict:
    """判断是否为模板占位符"""
    for keyword in PLACEHOLDER_KEYWORDS:
        if keyword in link_name:
            return True
    # 纯数字或单个字符
    if len(link_name.strip()) <= 1:
        return True
    return False

def scan_deadlinks(kb_root: str) -> dict:
    """扫描死链"""
    all_notes = set()
    link_counts = defaultdict(int)
    link_locations = defaultdict(list)

    # 第一遍：收集所有笔记名称
    for root, dirs, files in os.walk(kb_root):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if file.endswith('.md'):
                all_notes.add(file.replace('.md', ''))

    # 第二遍：收集所有链接
    for root, dirs, files in os.walk(kb_root):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if not file.endswith('.md'):
                continue
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                links = extract_links(content)
                for link in links:
                    link_name = link.strip()
                    if is_placeholder(link_name):
                        continue
                    link_counts[link_name] += 1
                    link_locations[link_name].append(file)
            except:
                pass

    # 找出死链（链接目标不存在）
    deadlinks = {}
    for link_name, count in link_counts.items():
        if link_name not in all_notes:
            deadlinks[link_name] = {
                'count': count,
                'locations': list(set(link_locations[link_name]))
            }

    return deadlinks, all_notes

def build_dynamic_maps(kb_root: str) -> tuple:
    """动态扫描知识库目录，构建双向分类映射（支持自定义配置分类）

    返回 (dir_to_cat, cat_to_dir)
    优先级：动态扫描 > 默认映射
    """
    default_dir_to_cat = {
        "00-综合导航": "综合导航", "01-前端开发": "前端开发",
        "02-后端开发": "后端开发", "03-数据库与缓存": "数据库与缓存",
        "04-分布式与中间件": "分布式与中间件", "05-云原生与运维": "云原生与运维",
        "06-计算机基础": "计算机基础", "07-通用工具": "通用工具",
        "08-Python全栈": "Python全栈", "09-AI与效率工具": "AI与效率工具",
        "99-项目实战": "项目实战",
    }
    dir_to_cat = dict(default_dir_to_cat)
    try:
        if os.path.exists(kb_root):
            for name in os.listdir(kb_root):
                full_path = os.path.join(kb_root, name)
                if os.path.isdir(full_path) and re.match(r'^\d+-', name):
                    cat_name = name.split('-', 1)[1] if '-' in name else name
                    dir_to_cat[name] = cat_name
    except Exception:
        pass
    cat_to_dir = {v: k for k, v in dir_to_cat.items()}
    return dir_to_cat, cat_to_dir


def infer_category(link_name: str, locations: str, kb_root: str) -> dict:
    """从引用位置推断分类（支持自定义配置分类）"""
    category_map, _ = build_dynamic_maps(kb_root)

    # 统计引用位置的分类
    category_counts = defaultdict(int)
    for loc in locations:
        for key, value in category_map.items():
            if key in loc:
                category_counts[value] += 1
                break

    if category_counts:
        return max(category_counts, key=category_counts.get)

    # 从名称推断
    name_lower = link_name.lower()
    if any(x in name_lower for x in ['vue', 'react', 'css', 'html', 'js', '前端', 'typescript']):
        return "前端开发"
    elif any(x in name_lower for x in ['java', 'spring', '后端', 'jvm', '微服务']):
        return "后端开发"
    elif any(x in name_lower for x in ['mysql', 'redis', '数据库', '缓存', 'sql']):
        return "数据库与缓存"
    elif any(x in name_lower for x in ['kafka', 'mq', '分布式', '消息队列', 'zookeeper']):
        return "分布式与中间件"
    elif any(x in name_lower for x in ['docker', 'k8s', 'kubernetes', '云原生', '运维', 'devops']):
        return "云原生与运维"
    elif any(x in name_lower for x in ['网络', '操作系统', '数据结构', '算法', '计算机']):
        return "计算机基础"
    elif any(x in name_lower for x in ['python', 'fastapi', 'django']):
        return "Python全栈"
    elif any(x in name_lower for x in ['ai', 'llm', 'rag', 'agent', '大模型', 'prompt']):
        return "AI与效率工具"
    return "通用工具"

def create_note(link_name: str, category: str, kb_root: str, count: str) -> dict:
    """创建缺失的笔记（支持自定义配置分类，v2.0 标准）"""
    _, category_dir_map = build_dynamic_maps(kb_root)

    cat_dir = category_dir_map.get(category, "07-通用工具")
    note_dir = os.path.join(kb_root, cat_dir)
    note_path = os.path.join(note_dir, f"{link_name}.md")
    date = datetime.now().strftime('%Y-%m-%d')

    content = f"""---
title: {link_name}
tags: [{category}]
category: {category}
created: {date}
updated: {date}
difficulty: ⭐⭐
status: 📝 草稿
priority: 重要
pre: []
aliases: []
template_version: v2.0
---

# {link_name}

> 自动创建的笔记，用于修复死链。被引用 {count} 次。请补充完整内容。

---

## 一、概述

### 1.1 什么是 {link_name}

{{请补充定义说明}}

### 1.2 为什么需要 {link_name}

| 痛点/问题 | 解决方案 |
|-----------|---------|
| {{问题1}} | {{解决方案1}} |

---

## 二、原理

{{请补充核心原理}}

---

## 三、实操

{{请补充实操示例}}

---

## 四、问题

{{请补充常见问题}}

---

## 五、拓展

{{请补充拓展内容}}

---

## 🔗 关联笔记

- {{请补充相关笔记}}

---

[[Home|🏠 返回首页]] · [[MOC-{category}|📚 返回分类]]
"""

    os.makedirs(note_dir, exist_ok=True)
    with open(note_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return note_path

def main() -> None:
    """主函数"""
    parser = argparse.ArgumentParser(description="修复死链")
    parser.add_argument("--path", required=True, help="知识库路径")
    parser.add_argument("--threshold", type=int, default=3, help="创建笔记的引用阈值（默认3次）")
    parser.add_argument("--dry-run", action="store_true", help="仅显示不执行")
    args = parser.parse_args()

    kb_root = os.path.abspath(args.path)
    if not os.path.exists(kb_root):
        print(f"❌ 路径不存在: {kb_root}")
        return

    print(f"🔗 死链修复: {kb_root}")
    print(f"   创建阈值: 引用 ≥ {args.threshold} 次")
    if args.dry_run:
        print("   (预览模式，不创建文件)")
    print("=" * 60)

    # 扫描死链
    print("\n🔍 扫描死链中...")
    deadlinks, all_notes = scan_deadlinks(kb_root)

    if not deadlinks:
        print("✅ 没有发现死链！")
        return

    print(f"📊 发现 {len(deadlinks)} 个死链\n")

    # 按引用次数排序
    sorted_deadlinks = sorted(deadlinks.items(), key=lambda x: x[1]['count'], reverse=True)

    # 分类处理
    high_freq = []  # 高频，创建笔记
    low_freq = []   # 低频，建议手动处理

    for link_name, info in sorted_deadlinks:
        if info['count'] >= args.threshold:
            high_freq.append((link_name, info))
        else:
            low_freq.append((link_name, info))

    # 显示高频死链
    if high_freq:
        print(f"🔥 高频死链（≥{args.threshold}次，将自动创建笔记）:")
        for link_name, info in high_freq[:20]:
            print(f"   [[{link_name}]] - {info['count']}次 (来自 {len(info['locations'])} 个文件)")
        if len(high_freq) > 20:
            print(f"   ... 还有 {len(high_freq)-20} 个")

    # 显示低频死链
    if low_freq:
        print(f"\n📌 低频死链（<{args.threshold}次，建议手动处理）:")
        for link_name, info in low_freq[:10]:
            print(f"   [[{link_name}]] - {info['count']}次")
        if len(low_freq) > 10:
            print(f"   ... 还有 {len(low_freq)-10} 个")

    if args.dry_run:
        print(f"\n💡 预览模式，将创建 {len(high_freq)} 个笔记")
        print("   去掉 --dry-run 参数以执行创建")
        return

    # 创建高频死链对应的笔记
    if high_freq:
        print(f"\n🔧 自动创建笔记...")
        created = 0
        for link_name, info in high_freq:
            category = infer_category(link_name, info['locations'], kb_root)
            try:
                note_path = create_note(link_name, category, kb_root, info['count'])
                created += 1
                print(f"   ✅ 创建: [[{link_name}]] -> {category} ({info['count']}次引用)")
            except Exception as e:
                print(f"   ❌ 失败: [[{link_name}]] - {e}")

        print(f"\n✅ 已创建 {created} 个笔记")

    print(f"\n📊 修复总结:")
    print(f"   总死链数: {len(deadlinks)}")
    print(f"   自动创建: {len(high_freq)}")
    print(f"   待手动处理: {len(low_freq)}")
    if low_freq:
        print(f"\n💡 建议:")
        print(f"   1. 对于低频死链，检查是否为拼写错误或别名")
        print(f"   2. 可以在已有笔记的 Frontmatter 中添加 aliases 字段")
        print(f"   3. 运行 audit-kb.py 再次检查死链情况")

if __name__ == "__main__":
    main()
