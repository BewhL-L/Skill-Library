#!/usr/bin/env python3
"""
知识库初始化脚本
自动生成 12 分类目录结构、Home 首页、综合导航 MOC、学习路线总览

用法:
    python init-kb.py --name "知识库名称" --path "输出路径" --theme "全栈+AI"
"""

import os
import sys
import argparse
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import load_config, get_categories, validate_config, find_config_in_kb

# 默认 11 个顶级分类（配置文件未指定时使用）
DEFAULT_CATEGORIES = [
    ("00", "综合导航", "首页、学习路线、知识地图、索引"),
    ("01", "前端开发", "HTML/CSS/JS/Vue/React/工程化"),
    ("02", "后端开发", "Java/Spring/微服务/并发/JVM"),
    ("03", "数据库与缓存", "MySQL/Redis/向量数据库/ES"),
    ("04", "分布式与中间件", "MQ/分布式事务/分布式锁/限流熔断"),
    ("05", "云原生与运维", "Docker/K8s/DevOps/监控/Linux"),
    ("06", "计算机基础", "网络/操作系统/数据结构/算法"),
    ("07", "通用工具", "Git/IDE/效率工具/终端"),
    ("08", "Python全栈", "Python/FastAPI/异步/测试"),
    ("09", "AI与效率工具", "LLM/RAG/Agent/多模态/Prompt"),
    ("99", "项目实战", "综合项目/案例/实战"),
]

# 全局分类变量（运行时从配置加载）
CATEGORIES = DEFAULT_CATEGORIES

def create_directory_structure(base_path: str) -> dict:
    """创建 11 分类目录结构"""
    for num, name, desc in CATEGORIES:
        dir_path = os.path.join(base_path, f"{num}-{name}")
        os.makedirs(dir_path, exist_ok=True)
        print(f"  📁 创建目录: {num}-{name}")

def create_home_md(base_path: str, kb_name: str, theme: str) -> dict:
    """创建 Home 首页"""
    content = f"""---
title: Home
tags: [MOC, 知识管理, 学习路线]
category: 综合导航
created: {datetime.now().strftime('%Y-%m-%d')}
updated: {datetime.now().strftime('%Y-%m-%d')}
difficulty: ⭐
status: ✅ 内容已完善
priority: 核心
pre: []
template_version: v2.0
---

# 🏠 {kb_name}

> {theme}知识库，从零基础到资深专家的完整学习路径。
>
> **当前状态**：共 0 篇笔记 · 0 个标签 · {len(CATEGORIES)} 个分类
> **最后更新**：{datetime.now().strftime('%Y-%m-%d')}

---

## 🗺️ 快速导航

### 📚 知识领域

| 分类 | 说明 | 入口 |
|------|------|------|
"""
    for num, name, desc in CATEGORIES:
        if num != "00":
            content += f"| [[MOC-{name}\\|{num}-{name}]] | {desc} | 📖 |\n"

    content += f"""
---

## 🎯 学习路线

详见 [[学习路线总览]]

---

## 📖 使用指南

1. **确定方向**：根据兴趣选择主攻方向
2. **按路线学习**：遵循学习路线，从入门阶段开始
3. **配合项目**：每个阶段完成对应的项目实战
4. **定期复习**：使用间隔重复法复习核心概念

---

## 🏷️ 核心标签

`#前端` `#后端` `#Java` `#Python` `#MySQL` `#Redis` `#分布式` `#云原生` `#AI应用` `#RAG` `#LLM`

---

> 💡 **提示**：建议将本页设为 Obsidian 启动页。
"""
    file_path = os.path.join(base_path, "00-综合导航", "Home.md")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  📄 创建首页: Home.md")

def create_moc_overview(base_path: str, kb_name: str) -> dict:
    """创建综合导航 MOC（v2.0 丰富版）"""
    date_str = datetime.now().strftime('%Y-%m-%d')
    cat_count = len(CATEGORIES)
    content = f"""---
title: 综合导航 MOC
tags: [MOC, 知识管理, 导航, 综合]
category: 综合导航
created: {date_str}
updated: {date_str}
difficulty: ⭐
status: ✅ 内容已完善
priority: 核心
hub: true
pre: []
aliases: [综合导航, 全库导航, 中央枢纽]
template_version: v2.0
---

# 📚 综合导航 MOC

> **内容地图**：{kb_name}全库内容地图，链接所有 {cat_count} 个分类 MOC，是知识库的中央枢纽。从这里可以快速定位到任何知识领域。
>
> **核心理念**：用导航体系把分散的笔记串起来，让学习者知道"有什么→学什么→怎么学→如何检验"。
>
> **学习建议**：建议从 [[学习路线总览]] 开始，按阶段推进；遇到具体问题时通过分类索引快速定位。

---

## 📊 导航体系总览

```mermaid
mindmap
  root(({kb_name}))
    综合导航
      Home首页
      学习路线总览
      本MOC
    技术领域
      待补充分类1
      待补充分类2
      待补充分类3
    项目实战
      待补充项目
    面试与求职
      面试题汇总
      简历与面试技巧
```

<!-- 填充指引：根据实际分类填充 mindmap，每个分类下列出核心文档 -->

---

## 🗂️ 分类索引

| 分类 | 说明 | 文档数 | MOC入口 |
|------|------|--------|---------|
"""
    for num, name, desc in CATEGORIES:
        if num != "00":
            content += f"| {num}-{name} | {desc} | 0 | [[MOC-{name}\\|📖 进入]] |\n"

    content += f"""
---

## 🗺️ 快速导航

### 我是新手，从哪开始？
1. [[学习路线总览]] — 查看四阶段学习路径，明确学习方向
2. 选择一个入门级分类，从基础概念开始学习
3. 用 `generate-note.py` 创建自己的学习笔记
4. 定期复习，用间隔重复法巩固核心概念

### 我想找某个技术点？
1. 在上方分类索引表中找到对应领域
2. 点击 MOC入口 进入该分类的内容地图
3. 在分类 MOC 的文档索引中查找具体笔记

### 我准备面试？
1. 查看 [[学习路线总览]] 的面试准备阶段
2. 重点复习核心原理和常见面试题
3. 参考各分类 MOC 中的面试高频考点

### 我想做项目？
1. 查看 [[MOC-项目实战]] 分类（如有）
2. 选择一个适合当前水平的项目
3. 按项目实战文档的分步实操推进

---

## 📚 学习路线

| 阶段 | 周期 | 核心目标 | 详细路线 |
|------|------|---------|---------|
| 🌱 入门筑基 | 0-3月 | 掌握基础语法和工具，能完成简单项目 | [[学习路线总览#第一阶段]] |
| 🌿 进阶提升 | 3-6月 | 深入原理和最佳实践，能解决实际问题 | [[学习路线总览#第二阶段]] |
| 🌳 高级精通 | 6-12月 | 掌握架构设计和优化，能设计复杂方案 | [[学习路线总览#第三阶段]] |
| 🌲 专家精通 | 12月+ | 源码级理解和技术输出，能引领技术方向 | [[学习路线总览#第四阶段]] |

**完整学习路线**：[[学习路线总览]]

---

## 📖 学习方法与技巧

1. **费曼学习法**：学完一个概念后，用自己的话讲给别人听，讲不清楚的地方就是没掌握的地方
2. **间隔重复**：按 1天→3天→7天→15天→30天 的间隔复习核心概念
3. **项目驱动**：每个阶段完成一个对应难度的项目，将理论转化为实践
4. **输出倒逼输入**：写笔记、写博客、做分享，输出的过程会发现知识盲区
5. **源码阅读**：高级阶段阅读优秀开源项目的源码，理解设计思想

---

## 📊 知识库统计

| 统计项 | 数量 |
|--------|------|
| **总分类数** | {cat_count} 个 |
| **总文档数** | 0 篇（创建笔记后更新） |
| **MOC 数量** | {cat_count} 个 |
| **最后更新** | {date_str} |

---

## 🏷️ 核心标签

`#知识管理` `#学习路线` `#MOC` `#导航` `#综合`

---

[[Home|🏠 返回首页]] · [[学习路线总览|🗺️ 学习路线]] · [[MOC-综合导航|📚 本页]]

---

> 📝 **MOC 版本**：v2.0 · **最后更新**：{date_str}
>
> 💡 **提示**：创建新笔记后，请在对应分类 MOC 中添加文档索引。使用 `generate-moc.py` 可自动扫描并更新分类 MOC。
"""
    file_path = os.path.join(base_path, "00-综合导航", "MOC-综合导航.md")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  📄 创建综合导航: MOC-综合导航.md (v2.0 丰富版)")

def create_learning_path(base_path: str, kb_name: str, theme: str) -> dict:
    """创建学习路线总览"""
    content = f"""---
title: 学习路线总览
tags: [学习路线, 知识管理]
category: 综合导航
created: {datetime.now().strftime('%Y-%m-%d')}
updated: {datetime.now().strftime('%Y-%m-%d')}
difficulty: ⭐
status: ✅ 内容已完善
priority: 核心
pre: []
template_version: v2.0
---

# 🗺️ {kb_name}学习路线总览

> 从零基础到资深专家的完整学习路径，覆盖 {theme} 全栈知识体系。

---

## 📋 路线总览

```
🌱 入门阶段（0-3月）→ 🌿 进阶阶段（3-6月）→ 🌳 高级阶段（6-12月）→ 🌲 专家阶段（12月+）
```

---

## 🌱 第一阶段：入门筑基（0-3 个月）

### 🎯 目标
- 掌握基础语法和工具
- 能独立完成简单 CRUD 项目
- 理解计算机基础概念

### 📚 核心知识点
1. 计算机基础（网络/操作系统）
2. Git 版本控制
3. 主攻语言基础
4. 主流框架入门
5. 数据库基础

### ✅ 验收标准
- [ ] 能独立搭建开发环境
- [ ] 能使用 Git 进行版本控制
- [ ] 能编写基础的 CRUD 接口
- [ ] 能完成一个简单的全栈项目

---

## 🌿 第二阶段：进阶提升（3-6 个月）

### 🎯 目标
- 深入理解核心框架原理
- 掌握数据库优化和缓存
- 熟悉工程化实践

### 📚 核心知识点
1. 语言进阶特性
2. 设计模式
3. 数据库优化
4. Redis 缓存
5. 工程化实践
6. 消息队列基础

### ✅ 验收标准
- [ ] 理解核心框架的底层原理
- [ ] 能进行数据库性能优化
- [ ] 能搭建 CI/CD 流水线
- [ ] 能设计简单的分布式系统

---

## 🌳 第三阶段：高级精通（6-12 个月）

### 🎯 目标
- 掌握系统架构设计
- 能解决分布式复杂问题
- 熟悉云原生技术栈

### 📚 核心知识点
1. 系统架构设计
2. 分布式事务与一致性
3. Kubernetes 容器编排
4. 可观测性
5. 性能调优
6. 安全实战

### ✅ 验收标准
- [ ] 能独立设计中大型系统架构
- [ ] 能解决分布式系统的复杂问题
- [ ] 能使用 K8s 进行容器编排
- [ ] 能进行全链路性能调优

---

## 🌲 第四阶段：专家架构（12 个月+）

### 🎯 目标
- 深入理解核心技术源码
- 能预判技术趋势并做选型
- 具备技术管理能力

### 📚 核心知识点
1. 核心框架源码精读
2. AI 工程化
3. 云原生新特性
4. 技术管理
5. 开源贡献

### ✅ 验收标准
- [ ] 能深入理解核心技术的源码实现
- [ ] 能带领团队完成复杂项目
- [ ] 有公开的技术输出和影响力

---

## ⚠️ 常见误区

1. **只看不练**：编程是实践技能，必须动手写代码
2. **追求完美**：先完成再完美
3. **频繁切换**：选定一个方向深入
4. **忽视基础**：计算机基础决定技术上限
5. **不做项目**：项目是检验学习成果的最好方式

---

[[Home|🏠 返回首页]] · [[MOC-综合导航|📚 综合导航]]
"""
    file_path = os.path.join(base_path, "00-综合导航", "学习路线总览.md")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  📄 创建学习路线: 学习路线总览.md")

def create_category_mocs(base_path: str) -> dict:
    """为每个分类创建 v2.0 标准化 MOC（丰富版结构）"""
    date_str = datetime.now().strftime('%Y-%m-%d')
    for num, name, desc in CATEGORIES:
        if num == "00":
            continue
        content = f"""---
title: {name} MOC
tags: [MOC, {name}, 导航]
category: {name}
created: {date_str}
updated: {date_str}
difficulty: ⭐⭐
status: ✅ 内容已完善
priority: 核心
hub: true
pre: []
aliases: [{name}导航, {name}MOC]
template_version: v2.0
---

# 📚 {name} MOC

> **内容地图**：{desc}。是{name}领域的"控制塔"，指引学习者从入门到精通。
>
> **学习建议**：建议先学基础概念，再深入原理，最后通过项目实战巩固。使用 `generate-note.py` 创建笔记后，在此处添加索引。

---

## 📊 导航体系总览

```mermaid
mindmap
  root(({name}))
    基础概念
      待补充核心文档
    核心原理
      待补充原理文档
    实战应用
      待补充实战文档
    进阶拓展
      待补充进阶文档
```

<!-- 填充指引：根据实际笔记填充 mindmap，4-5个子领域，每个子领域2-4个核心文档 -->

---

## 📚 学习路线

| 阶段 | 周期 | 核心目标 | 关键技能 | 验收标准 |
|------|------|---------|---------|---------|
| 🌱 入门筑基 | 2-4周 | 掌握基础概念和基本用法 | 基础语法、核心概念 | 能独立完成基础示例 |
| ⚡ 进阶实战 | 1-2月 | 深入原理和最佳实践 | 核心用法、常见场景 | 能解决实际问题 |
| 🏗️ 高级架构 | 2-3月 | 掌握架构设计和优化 | 原理深入、性能优化 | 能设计复杂方案 |
| 👑 专家精通 | 3月+ | 源码级理解和技术输出 | 源码分析、前沿技术 | 能输出技术文章 |

---

## 📂 文档索引

> **⚠️ 表格格式规范**：文档索引表统一为三列 `文档 | 说明 | 难度`。若双链使用别名格式，其中的竖线必须用反斜杠转义，否则会导致表格列数错位。

### 一、基础概念

| 文档 | 说明 | 难度 |
|------|------|------|
| （待补充） | 使用 `generate-note.py` 创建笔记后在此添加索引 | ⭐ |

### 二、核心原理

| 文档 | 说明 | 难度 |
|------|------|------|
| （待补充） | | ⭐⭐⭐ |

### 三、实战应用

| 文档 | 说明 | 难度 |
|------|------|------|
| （待补充） | | ⭐⭐ |

---

## 🗺️ 快速导航

### 我是新手，从哪开始？
1. 先学习基础概念类笔记，掌握核心定义
2. 参考学习路线表，按阶段推进
3. 用 `generate-note.py` 创建自己的学习笔记

### 我想深入原理？
1. 学习核心原理类笔记，理解底层机制
2. 结合实战应用，将理论转化为实践
3. 参考 [[MOC-综合导航]] 查看跨领域关联

---

## 🔗 知识关联

### 领域内知识体系

```
{name}体系
├── 基础概念 ← 入门必备
├── 核心原理 ← 深入理解
├── 实战应用 ← 能力提升
└── 进阶拓展 ← 专家之路
```

### 跨领域关联

- [[MOC-综合导航]] — 全库中央枢纽
- [[学习路线总览]] — 四阶段学习路径
- （根据实际领域添加跨领域关联）

---

## 📖 学习顺序

1. **入门筑基**：基础概念 → 核心定义 → 快速上手
2. **核心进阶**：原理深入 → 最佳实践 → 常见场景
3. **高级实战**：架构设计 → 性能优化 → 复杂方案
4. **专家精通**：源码分析 → 前沿技术 → 技术输出
5. **综合应用**：结合项目实战，将知识融会贯通

---

## 🌐 跨领域 MOC 导航

| 领域 | MOC入口 | 核心内容 |
|------|---------|---------|
| 📚 综合导航 | [[MOC-综合导航]] | 全库中央枢纽、学习路线 |
| 🗺️ 学习路线 | [[学习路线总览]] | 四阶段学习路径 |
| （添加其他相关领域） | | |

---

## 📊 本分类统计

| 统计项 | 数量 |
|--------|------|
| **总文档数** | 0 篇 |
| **子领域** | 4 个（基础/原理/实战/拓展） |
| **最后更新** | {date_str} |

---

## 🏷️ 标签体系

`#{name}` `#MOC` `#导航`

---

[[Home|🏠 返回首页]] · [[MOC-综合导航|📚 综合导航]] · [[学习路线总览|🗺️ 学习路线]]

---

> 📝 **MOC 版本**：v2.0 · **最后更新**：{date_str}
>
> 💡 **提示**：创建笔记后，请在此处添加文档索引。使用 `generate-moc.py --category {name} --path "{num}-{name}"` 可自动扫描并更新索引。
"""
        file_path = os.path.join(base_path, f"{num}-{name}", f"MOC-{name}.md")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  📄 创建MOC: MOC-{name}.md (v2.0 丰富版)")

def copy_obsidian_config(base_path: str) -> None:
    """复制预置的 .obsidian 配置到知识库（外观/插件/快捷键）"""
    import shutil
    script_dir = os.path.dirname(os.path.abspath(__file__))
    skill_root = os.path.dirname(script_dir)
    config_src = os.path.join(skill_root, "assets", "obsidian-config")
    obsidian_dst = os.path.join(base_path, ".obsidian")

    if not os.path.exists(config_src):
        print(f"  ⚠️  未找到 .obsidian 配置源: {config_src}")
        return

    os.makedirs(obsidian_dst, exist_ok=True)
    copied = 0
    for filename in os.listdir(config_src):
        src_file = os.path.join(config_src, filename)
        dst_file = os.path.join(obsidian_dst, filename)
        if os.path.isfile(src_file):
            shutil.copy2(src_file, dst_file)
            copied += 1
    print(f"  ⚙️  已复制 .obsidian 配置: {copied} 个文件（外观/插件/快捷键）")

def copy_demo_notes(base_path: str, only_existing_dirs: bool = False) -> None:
    """复制示例笔记到知识库（--demo 模式）

    Args:
        base_path: 知识库根目录
        only_existing_dirs: 仅复制目标目录已存在的文件（自定义配置时使用，
            避免创建不在配置中的额外分类目录）
    """
    import shutil
    script_dir = os.path.dirname(os.path.abspath(__file__))
    skill_root = os.path.dirname(script_dir)
    demo_src = os.path.join(skill_root, "examples", "sample-kb")

    if not os.path.exists(demo_src):
        print(f"  ⚠️  未找到示例知识库: {demo_src}")
        return

    copied = 0
    skipped = 0
    for root, dirs, files in os.walk(demo_src):
        for filename in files:
            if filename == "README.md":
                continue
            src_file = os.path.join(root, filename)
            rel_path = os.path.relpath(src_file, demo_src)
            dst_file = os.path.join(base_path, rel_path)
            dst_dir = os.path.dirname(dst_file)

            # 自定义配置模式：仅复制目标目录已存在的文件
            if only_existing_dirs and not os.path.isdir(dst_dir):
                skipped += 1
                continue

            os.makedirs(dst_dir, exist_ok=True)
            shutil.copy2(src_file, dst_file)
            copied += 1

    if skipped > 0:
        print(f"  📝 已复制示例笔记: {copied} 个文件（跳过 {skipped} 个不匹配自定义分类的文件）")
    else:
        print(f"  📝 已复制示例笔记: {copied} 个文件（8篇高质量示例笔记 + MOC + 学习路线）")

def main() -> None:
    """主函数"""
    global CATEGORIES
    parser = argparse.ArgumentParser(description="初始化 Obsidian 知识库")
    parser.add_argument("--name", required=True, help="知识库名称")
    parser.add_argument("--path", required=True, help="输出路径")
    parser.add_argument("--theme", default="全栈+AI", help="知识库主题")
    parser.add_argument("--config", help="配置文件路径（YAML格式，可自定义分类/模板/标签等）")
    parser.add_argument("--demo", action="store_true", help="生成包含示例笔记的演示知识库")
    args = parser.parse_args()

    # 加载配置文件
    config_path = args.config
    if not config_path:
        config_path = find_config_in_kb(os.path.abspath(args.path))
    config = load_config(config_path)

    # 验证配置
    warnings = validate_config(config)
    for w in warnings:
        print(f"  ⚠️  {w}")

    # 从配置加载分类
    config_categories = get_categories(config)
    if config_categories:
        CATEGORIES = config_categories
        print(f"  📋 从配置加载了 {len(CATEGORIES)} 个分类")

    base_path = os.path.abspath(args.path)
    print(f"\n🚀 初始化知识库: {args.name}")
    print(f"📁 输出路径: {base_path}")
    print(f"🎯 主题: {args.theme}")
    print()

    # 创建目录结构
    print("📁 创建目录结构...")
    create_directory_structure(base_path)

    # 创建核心文件
    print("\n📄 创建核心文件...")
    create_home_md(base_path, args.name, args.theme)
    create_moc_overview(base_path, args.name)
    create_learning_path(base_path, args.name, args.theme)

    # 创建分类 MOC
    print("\n📄 创建分类 MOC...")
    create_category_mocs(base_path)

    # 复制 .obsidian 配置（开箱即用）
    print("\n⚙️  复制 Obsidian 配置...")
    copy_obsidian_config(base_path)

    # --demo 模式：复制示例笔记
    if args.demo:
        print("\n📝 复制示例笔记（--demo 模式）...")
        # 自定义配置时仅复制匹配的目录，避免创建额外分类
        use_custom_config = bool(args.config) or bool(find_config_in_kb(base_path))
        if use_custom_config:
            print("  ⚠️  检测到自定义配置，仅复制匹配分类的示例文件")
        copy_demo_notes(base_path, only_existing_dirs=use_custom_config)

    # 创建 attachments 目录（含 .gitkeep 确保 Git 跟踪空目录）
    attachments_dir = os.path.join(base_path, "attachments")
    os.makedirs(attachments_dir, exist_ok=True)
    gitkeep_path = os.path.join(attachments_dir, ".gitkeep")
    if not os.path.exists(gitkeep_path):
        with open(gitkeep_path, "w", encoding="utf-8") as f:
            f.write("# 附件目录\n# 存放图片、PDF等附件文件\n")

    file_count = sum(len(files) for _, _, files in os.walk(base_path))
    print(f"\n✅ 知识库初始化完成！")
    print(f"📁 位置: {base_path}")
    print(f"📄 已创建: {len(CATEGORIES)} 个目录 + {file_count} 个文件")
    if args.demo:
        print(f"🎯 演示模式: 包含 8 篇高质量示例笔记，开箱即用")
    print(f"\n💡 下一步:")
    print(f"  1. 用 Obsidian 打开该文件夹")
    print(f"  2. 设置 Home.md 为启动页")
    print(f"  3. 使用 generate-note.py 创建标准化笔记")
    print(f"  4. 使用 generate-moc.py 更新 MOC 索引")

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
