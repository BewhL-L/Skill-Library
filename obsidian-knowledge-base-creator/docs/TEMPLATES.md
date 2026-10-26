# 模板使用指南

## 📋 概述

本文档详细介绍项目中所有模板的使用方法、自定义技巧和最佳实践。

---

## 📁 模板文件清单

| 模板文件 | 用途 | 适用场景 |
|---------|------|---------|
| `assets/note-template.md` | 标准化笔记模板 | 生成技术笔记、概念文档 |
| `assets/moc-template.md` | MOC 内容地图模板 | 生成分类导航、知识索引 |
| `assets/home-template.md` | 知识库首页模板 | 生成知识库总入口 |
| `assets/learning-path-template.md` | 学习路线模板 | 生成渐进式学习路径 |
| `assets/atomic-note-template.md` | 原子化笔记模板 | 生成单一概念笔记 |
| `references/*.md` | 参考规范文档 | 查阅标准和规范 |

---

## 📝 note-template.md - 标准化笔记模板

### 模板结构

```markdown
---
title: {{title}}
tags: [{{tags}}]
category: {{category}}
created: {{created}}
updated: {{updated}}
difficulty: {{difficulty}}
status: 📝 草稿
priority: {{priority}}
pre: [{{pre}}]
aliases: [{{aliases}}]
---

# {{title}}

## 概述
<!-- 定义、作用、解决什么问题 -->

## 原理
<!-- 底层机制、核心逻辑、架构设计 -->

## 实操
<!-- 安装配置、代码示例、最佳实践 -->

## 问题
<!-- 常见错误、排查方案、性能调优 -->

## 拓展
<!-- 进阶用法、生态工具、相关概念 -->

## 参考资料
<!-- 学习资源、官方文档、相关链接 -->
```

### 变量说明

| 变量 | 说明 | 示例 |
|------|------|------|
| `{{title}}` | 笔记标题 | Vue3 响应式原理 |
| `{{tags}}` | 标签列表（逗号分隔） | Vue3,前端,响应式 |
| `{{category}}` | 分类名称 | 前端开发 |
| `{{created}}` | 创建日期 | 2026-08-30 |
| `{{updated}}` | 更新日期 | 2026-08-30 |
| `{{difficulty}}` | 难度星级 | ⭐⭐⭐ |
| `{{priority}}` | 优先级 | 核心/重要/一般 |
| `{{pre}}` | 前置知识 | [[Vue3基础]] |
| `{{aliases}}` | 别名 | 响应式原理,Reactivity |

### 使用方法

```bash
# 方法一：使用命令生成
python scripts/kb.py note --title "Vue3 响应式原理" --category "前端开发" --difficulty 3 --tags Vue3 前端 响应式

# 方法二：手动复制模板
cp assets/note-template.md "01-前端开发/Vue3响应式原理.md"
# 然后编辑文件，替换变量和填充内容
```

### 自定义技巧

1. **添加自定义字段**：在 Frontmatter 中添加需要的字段
   ```yaml
   ---
   title: Vue3 响应式原理
   author: 你的名字
   review_count: 3
   next_review: 2026-09-15
   ---
   ```

2. **修改五段式结构**：根据需要调整模块
   - 简单概念：概述 + 实操 + 拓展
   - 复杂概念：概述 + 原理 + 实操 + 问题 + 拓展 + 源码分析
   - 工具类：概述 + 安装 + 配置 + 使用 + 最佳实践

3. **添加代码块语言标注**：
   ```python
   # Python 代码
   def example():
       pass
   ```

   ```javascript
   // JavaScript 代码
   const example = () => {}
   ```

---

## 🗺️ moc-template.md - MOC 内容地图模板

### 模板结构

```markdown
---
title: {{category}} MOC
tags: [MOC, {{category}}]
category: {{category}}
created: {{created}}
updated: {{updated}}
difficulty: ⭐⭐
status: ✅ 内容已完善
priority: 核心
---

# {{category}} 知识地图

## 📚 学习路线
<!-- 入门 → 进阶 → 高级 → 专家 -->

### 入门阶段
- [ ] 基础概念
- [ ] 环境搭建
- [ ] Hello World

### 进阶阶段
...

## 📋 文档索引
| 文档 | 难度 | 优先级 | 状态 | 标签 |
|------|------|--------|------|------|
| [[文档1]] | ⭐⭐ | 核心 | ✅ | 标签1,标签2 |

## 🔗 知识关联
<!-- 相关概念、依赖关系、知识网络 -->

## 📖 学习顺序建议
<!-- 推荐的学习顺序和时间安排 -->

## 🎯 核心概念
<!-- 该分类下最重要的概念列表 -->

## 📝 待补充
<!-- 需要创建或完善的笔记清单 -->
```

### 使用方法

```bash
# 自动生成 MOC（扫描目录下所有笔记）
python scripts/kb.py moc --category "前端开发" --path "01-前端开发"

# 手动创建
cp assets/moc-template.md "01-前端开发/MOC.md"
```

### 自定义技巧

1. **添加进度统计**：
   ```markdown
   ## 📊 学习进度
   - 总笔记数：25
   - 已完成：18 (72%)
   - 进行中：5 (20%)
   - 待开始：2 (8%)
   ```

2. **添加思维导图**：使用 Mermaid 语法
   ```mermaid
   graph TD
     A[前端开发] --> B[HTML/CSS]
     A --> C[JavaScript]
     A --> D[框架]
     D --> E[Vue3]
     D --> F[React]
   ```

3. **按子分类组织**：
   ```markdown
   ## 📂 子分类
   ### 基础技术
   - [[HTML5]]
   - [[CSS3]]
   - [[JavaScript]]

   ### 前端框架
   - [[Vue3]]
   - [[React]]
   ```

---

## 🏠 home-template.md - 知识库首页模板

### 模板结构

```markdown
---
title: Home
tags: [首页,导航,MOC]
category: 首页
created: {{created}}
updated: {{updated}}
difficulty: ⭐
status: ✅ 内容已完善
priority: 核心
---

# {{kb_name}}

> {{description}}

## 🚀 快速开始
<!-- 新手入门指南 -->

## 📚 知识分类
<!-- 12 个顶级分类的导航 -->

### 01-前端开发
- [[前端开发 MOC]]
- 核心概念：[[Vue3]]、[[React]]、[[TypeScript]]

### 02-后端开发
...

## 🗺️ 学习路线
<!-- 整体学习路径 -->

## 📊 学习统计
<!-- 笔记数量、完成度、最近更新 -->

## 🔥 最近更新
<!-- 最近创建或修改的笔记 -->

## 📌 重点学习
<!-- 当前重点学习的内容 -->

## 🔗 有用链接
<!-- 外部资源、工具、社区 -->
```

### 使用方法

```bash
# init 命令会自动生成 Home 首页
python scripts/kb.py init --name "我的知识库" --path "./my-kb"

# 手动更新
python scripts/kb.py moc --category "首页" --path "."
```

---

## 🎓 learning-path-template.md - 学习路线模板

### 模板结构

```markdown
---
title: {{topic}} 学习路线
tags: [学习路线,{{topic}}]
category: {{category}}
created: {{created}}
updated: {{updated}}
difficulty: ⭐⭐
status: ✅ 内容已完善
priority: 核心
---

# {{topic}} 学习路线

## 🎯 学习目标
<!-- 学完后能达到的水平 -->

## 📅 学习周期
<!-- 预计学习时间 -->

## 📚 四阶段学习路径

### 阶段一：入门（{{duration1}}）
**目标**：掌握基础概念，能完成简单项目

**核心技能**：
- [ ] 技能1
- [ ] 技能2

**项目实践**：
- 项目1：描述

**验收标准**：
- 能独立完成 XXX
- 理解 XXX 原理

**推荐资源**：
- [[相关笔记1]]
- 官方文档链接

### 阶段二：进阶（{{duration2}}）
...

### 阶段三：高级（{{duration3}}）
...

### 阶段四：专家（{{duration4}}）
...

## 📊 进度追踪
| 阶段 | 开始时间 | 完成时间 | 状态 | 笔记数 |
|------|---------|---------|------|--------|

## 🎯 能力矩阵
| 能力 | 入门 | 进阶 | 高级 | 专家 |
|------|------|------|------|------|
| 能力1 | ⬜ | ⬜ | ⬜ | ⬜ |

## 📝 学习笔记
<!-- 按阶段组织的笔记索引 -->

## 💡 学习技巧
<!-- 高效学习方法和建议 -->

## 🔗 相关资源
<!-- 书籍、课程、社区、工具 -->
```

### 使用方法

```bash
# init 命令会自动生成学习路线总览
# 为特定主题创建学习路线
cp assets/learning-path-template.md "学习路线/Vue3学习路线.md"
```

---

## ⚛️ atomic-note-template.md - 原子化笔记模板

### 模板结构

```markdown
---
title: {{concept}}
tags: [{{tags}}]
category: {{category}}
created: {{created}}
updated: {{updated}}
difficulty: {{difficulty}}
status: 📝 草稿
priority: {{priority}}
pre: [{{pre}}]
next: [{{next}}]
aliases: [{{aliases}}]
---

# {{concept}}

## 一句话定义
<!-- 用一句话精确描述这个概念 -->

## 核心要点
<!-- 3-5 个最重要的要点 -->
- 要点1
- 要点2

## 详细说明
<!-- 概念的详细解释 -->

## 示例
<!-- 代码示例或使用示例 -->

## 常见误区
<!-- 容易混淆或错误理解的地方 -->

## 相关概念
<!-- 相关概念的双向链接 -->
- [[相关概念1]]
- [[相关概念2]]

## 参考资料
<!-- 来源和延伸阅读 -->
```

### 原子化笔记原则

1. **单一概念**：每篇笔记只讲一个概念
2. **自包含**：不依赖其他笔记就能理解
3. **可复用**：可以在多个上下文中引用
4. **可链接**：与其他概念建立关联
5. **可演化**：随着理解深入不断完善

---

## 🎨 自定义模板指南

### 创建自定义模板

1. **复制现有模板**：
   ```bash
   cp assets/note-template.md assets/my-custom-template.md
   ```

2. **修改模板结构**：根据需要添加或删除模块

3. **使用自定义模板**：
   ```bash
   # 手动复制使用
   cp assets/my-custom-template.md "目标目录/笔记名.md"
   ```

### 模板变量语法

项目使用简单的变量替换语法：

| 语法 | 说明 | 示例 |
|------|------|------|
| `{{variable}}` | 简单变量替换 | `{{title}}` → Vue3 |
| `{{#if variable}}...{{/if}}` | 条件块 | 可选内容 |
| `{{#each items}}...{{/each}}` | 循环块 | 列表生成 |

### 最佳实践

1. **保持模板简洁**：不要在模板中放太多内容，留出填充空间
2. **使用注释标记**：用 `<!-- -->` 标记每个部分应该写什么
3. **统一命名规范**：模板文件名使用小写和连字符
4. **版本控制模板**：模板变更也要提交到 Git
5. **定期 review 模板**：根据使用反馈优化模板

---

## 📞 相关文档

- [SKILL.md](../SKILL.md) - 完整功能说明
- [OBSIDIAN-GUIDE.md](OBSIDIAN-GUIDE.md) - Obsidian 使用指南
- [references/](references/) - 详细规范文档
- [FAQ.md](FAQ.md) - 常见问题

---

> **最后更新**：2026-08-30
>
> **适用版本**：v3.1.0
