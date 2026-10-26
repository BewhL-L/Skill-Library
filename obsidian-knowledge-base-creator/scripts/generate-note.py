#!/usr/bin/env python3
"""
标准化笔记生成脚本
基于五段式模板生成符合知识库标准的笔记

用法:
    python generate-note.py --title "Vue3 组合式 API" --category "前端开发" --kb-root "./my-kb"
    python generate-note.py --title "Redis 缓存" --category "数据库与缓存" --difficulty 3 --kb-root "C:/my-kb"
"""

import os
import argparse
from datetime import datetime

# 分类映射
CATEGORY_MAP = {
    "综合导航": "00-综合导航",
    "前端开发": "01-前端开发",
    "后端开发": "02-后端开发",
    "数据库与缓存": "03-数据库与缓存",
    "分布式与中间件": "04-分布式与中间件",
    "云原生与运维": "05-云原生与运维",
    "计算机基础": "06-计算机基础",
    "通用工具": "07-通用工具",
    "Python全栈": "08-Python全栈",
    "AI与效率工具": "09-AI与效率工具",
    "项目实战": "99-项目实战",
}

def resolve_category_dir(category, kb_root=None):
    """解析分类目录，支持自定义配置分类"""
    if category in CATEGORY_MAP:
        return CATEGORY_MAP[category]
    if kb_root and os.path.isdir(kb_root):
        for d in os.listdir(kb_root):
            dp = os.path.join(kb_root, d)
            if os.path.isdir(dp) and '-' in d:
                parts = d.split('-', 1)
                if len(parts) == 2 and parts[1] == category:
                    return d
    return category

# 难度星级
DIFFICULTY_STARS = {
    1: "⭐",
    2: "⭐⭐",
    3: "⭐⭐⭐",
    4: "⭐⭐⭐⭐",
    5: "⭐⭐⭐⭐⭐",
}

def generate_note(title: str, category: str, difficulty: str, tags: str = None, pre: str = None) -> dict:
    """生成标准化笔记内容"""
    stars = DIFFICULTY_STARS.get(difficulty, "⭐⭐⭐")
    date = datetime.now().strftime('%Y-%m-%d')
    tags_list = tags if tags else [category]
    tags_str = ", ".join(tags_list)
    tags_display = "`#" + "` `#".join(tags_list) + "`"
    pre_str = ", ".join([f"[[{p}]]" for p in pre]) if pre else ""

    content = f"""---
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

<!-- 填充指引：原理部分占全文30%，深入底层机制，配合架构图和流程图说明。代码/框架类进阶知识点走『底层逻辑四步』：运行链路(Mermaid图)→源码定位(包名.类名#方法+关键片段)→可自证实验(断点/日志/dis·javap/timeit)→设计权衡，不要只写"底层做了优化"。 -->

### 2.1 核心原理

{{核心机制、关键算法、工作原理的详细说明（代码类进阶知识点须含运行链路图+源码定位+可复现实验）}}

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

> 💡 **提示**：{{关键注意事项}}

### 3.3 核心用法

#### 用法1：{{名称}}

```javascript
{{代码示例}}
```

**说明**：{{用法解释}}

#### 用法2：{{名称}}

```javascript
{{代码示例}}
```

### 3.4 最佳实践

✅ **推荐做法**
- {{最佳实践1}}
- {{最佳实践2}}

❌ **避免做法**
- {{避免做法1}}

### 3.5 完整示例

```
项目结构
├── src/
│   ├── index.js
│   └── config.js
└── package.json
```

```javascript
// 完整项目代码
{{完整代码}}
```

---

## 四、问题

<!-- 填充指引：问题部分占全文15%，收集真实开发中遇到的错误，给出原因和解决方案 -->

### 4.1 常见错误

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| {{错误1}} | {{原因1}} | {{方案1}} |
| {{错误2}} | {{原因2}} | {{方案2}} |

### 4.2 性能优化

| 优化点 | 优化前 | 优化后 | 提升 |
|--------|--------|--------|------|
| {{优化点1}} | | | |

**优化策略**：
1. {{策略1}}
2. {{策略2}}

### 4.3 安全风险

| 风险 | 攻击方式 | 防护措施 |
|------|---------|---------|
| {{风险1}} | {{攻击方式1}} | {{防护措施1}} |

### 4.4 生产环境踩坑

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
    return content

def main() -> None:
    """主函数"""
    parser = argparse.ArgumentParser(description="生成标准化笔记")
    parser.add_argument("--title", required=True, help="笔记标题")
    parser.add_argument("--category", required=True, help="所属分类（支持默认11分类及自定义配置分类）")
    parser.add_argument("--difficulty", type=int, default=3, choices=[1,2,3,4,5], help="难度等级 1-5")
    parser.add_argument("--tags", nargs="*", help="标签列表")
    parser.add_argument("--pre", nargs="*", help="前置知识列表")
    parser.add_argument("--kb-root", help="知识库根目录（用于自动推断输出路径）")
    parser.add_argument("--output", help="输出文件路径（优先于自动推断）")
    args = parser.parse_args()

    # 推断输出路径（支持自定义分类）
    kb_root_resolve = os.path.abspath(args.kb_root) if args.kb_root else None
    category_dir = resolve_category_dir(args.category, kb_root_resolve)
    if args.output:
        output_path = os.path.abspath(args.output)
    elif args.kb_root:
        kb_root = os.path.abspath(args.kb_root)
        filename = f"{args.title}.md"
        output_path = os.path.join(kb_root, category_dir, filename)
    else:
        filename = f"{args.title}.md"
        output_path = os.path.join(os.getcwd(), category_dir, filename)
        print(f"⚠️  警告：未指定 --kb-root，将使用当前目录作为知识库根目录")
        print(f"   建议使用 --kb-root 指定知识库根目录以确保路径正确")

    # 检查文件是否已存在
    if os.path.exists(output_path):
        print(f"⚠️  警告：文件已存在，将被覆盖: {output_path}")
        response = input("是否继续？(y/N): ").strip().lower()
        if response != 'y':
            print("已取消")
            return

    # 生成笔记内容
    content = generate_note(args.title, args.category, args.difficulty, args.tags, args.pre)

    # 确保目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # 写入文件
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"\n✅ 笔记已生成")
    print(f"📝 标题: {args.title}")
    print(f"📂 分类: {args.category}")
    print(f"⭐ 难度: {DIFFICULTY_STARS[args.difficulty]}")
    print(f"📁 路径: {output_path}")
    print(f"\n💡 下一步:")
    print(f"  1. 填充 {{}} 占位符中的内容")
    print(f"  2. 将 status 从 📝草稿 改为 ✅内容已完善")
    print(f"  3. 运行 generate-moc.py 更新对应 MOC 索引")
    print(f"  4. 添加相关笔记的双链")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️  操作已取消")
    except Exception as e:
        print(f"\n❌ 运行出错: {type(e).__name__}: {e}")
        print("\n💡 排查建议:")
        print("  1. 检查路径是否正确，目录是否有写入权限")
        print("  2. 检查 Python 版本是否为 3.7+")
        print("  3. 查看 FAQ.md 了解常见问题")
        print("  4. 使用 --dry-run 先预览操作")
        import traceback
        traceback.print_exc()
