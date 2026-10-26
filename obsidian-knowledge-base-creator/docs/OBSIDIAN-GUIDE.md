# 📖 Obsidian 配置与使用指南

> 基于本知识库标准的 Obsidian 最佳实践配置，让你真正用好这个知识库

---

## 📋 目录

1. [基础配置](#基础配置)
2. [推荐插件](#推荐插件)
3. [关系图谱颜色配置](#关系图谱颜色配置)
4. [Dataview 查询示例](#dataview-查询示例)
5. [快捷键配置](#快捷键配置)
6. [日常使用工作流](#日常使用工作流)

---

## 基础配置

### 1. 设置启动页

将 `00-综合导航/Home.md` 设为启动页：

1. 打开 `设置 → 核心插件 → 工作区`
2. 启用"启动时恢复上次工作区"
3. 或使用 `Homepage` 社区插件，设置启动页为 `Home`

### 2. 外观配置

推荐设置：
- **主题**：默认主题或 Minimal 主题（简洁美观）
- **基础颜色方案**：深色（护眼）或浅色（清晰）
- **字体**：
  - 界面字体：系统默认
  - 正文字体：思源黑体 / Microsoft YaHei
  - 等宽字体：JetBrains Mono / Fira Code
- **行宽**：800px（适合阅读）
- **行高**：1.6（舒适阅读）

### 3. 编辑器配置

推荐设置：
- ✅ 启用"实时预览"（Live Preview）
- ✅ 启用"严格换行"（Strict Line Breaks）
- ✅ 启用"显示行号"
- ✅ 启用"高亮当前行"
- ✅ 启用"自动配对"（括号、引号）
- ✅ 启用"智能缩进列表"

### 4. 文件与链接配置

- ✅ 启用"使用 [[Wikilinks]]"
- ✅ 启用"新链接使用相对路径"
- ✅ 启用"自动更新内部链接"（重命名文件时自动更新链接）
- **附件默认路径**：`assets/`（统一管理图片等附件）

---

## 推荐插件

### 🔧 核心插件（默认启用）

| 插件 | 用途 | 本知识库用法 |
|------|------|-------------|
| 标签面板 | 查看所有标签 | 按标签筛选笔记 |
| 大纲 | 查看文档结构 | 快速跳转章节 |
| 关系图谱 | 可视化知识网络 | 查看笔记间关联 |
| 搜索 | 全文搜索 | 快速查找知识点 |
| 书签 | 收藏重要笔记 | 收藏高频使用的 MOC |
| 模板 | 快速插入模板 | 使用笔记模板 |

### 🚀 社区插件（强烈推荐）

#### 1. Dataview（必装）

**用途**：基于 Frontmatter 的动态查询，自动生成索引、清单、表格。

**安装**：设置 → 社区插件 → 浏览 → 搜索 "Dataview" → 安装并启用

**本知识库核心用法**：
- 自动生成学习进度表
- 按分类/难度/优先级筛选笔记
- 生成待学习清单
- 统计各分类笔记数量

详见 [Dataview 查询示例](#dataview-查询示例)

#### 2. Templater（推荐）

**用途**：高级模板引擎，支持变量、函数、动态内容。

**本知识库用法**：
- 快速创建标准化笔记（自动填写日期、分类等）
- 模板中使用 `<% tp.date.now() %>` 自动填写日期
- 根据分类自动选择不同模板

#### 3. Calendar（推荐）

**用途**：日历视图，快速查看和创建每日笔记。

**本知识库用法**：
- 记录每日学习进度
- 关联学习笔记到具体日期
- 查看学习历史

#### 4. Excalidraw（推荐）

**用途**：手绘风格图表，适合画架构图、流程图、思维导图。

**本知识库用法**：
- 为"原理"章节绘制架构图
- 绘制学习路线思维导图
- 可视化复杂概念

#### 5. Omnisearch（可选）

**用途**：更强大的全文搜索，支持模糊匹配、中文分词。

**本知识库用法**：
- 快速搜索技术概念
- 跨文档查找相关内容

#### 6. Style Settings（可选）

**用途**：可视化调整主题样式，无需写 CSS。

**本知识库用法**：
- 调整字体大小、行高
- 自定义颜色方案
- 优化阅读体验

---

## 关系图谱颜色配置

基于 Frontmatter 的 `category` 字段，为不同分类的笔记设置不同颜色，让图谱一目了然。

### 配置方法

1. 打开关系图谱视图（左侧边栏图标）
2. 点击"颜色组"（Color groups）
3. 按以下配置添加颜色组：

### 推荐颜色方案

| 分类 | 颜色 | 十六进制 | 匹配规则 |
|------|------|---------|---------|
| 综合导航 | 金色 | `#FFD700` | `tag:#综合导航` 或 `path:00-综合导航` |
| 前端开发 | 蓝色 | `#3B82F6` | `path:01-前端开发` |
| 后端开发 | 绿色 | `#10B981` | `path:02-后端开发` |
| 数据库与缓存 | 橙色 | `#F59E0B` | `path:03-数据库与缓存` |
| 分布式与中间件 | 紫色 | `#8B5CF6` | `path:04-分布式与中间件` |
| 云原生与运维 | 青色 | `#06B6D4` | `path:05-云原生与运维` |
| 计算机基础 | 红色 | `#EF4444` | `path:06-计算机基础` |
| 通用工具 | 灰色 | `#6B7280` | `path:07-通用工具` |
| Python全栈 | 黄色 | `#EAB308` | `path:08-Python全栈` |
| AI与效率工具 | 粉色 | `#EC4899` | `path:09-AI与效率工具` |
| 项目实战 | 靛蓝 | `#6366F1` | `path:99-项目实战` |
| MOC文件 | 白色 | `#FFFFFF` | `file:MOC-` |

### 图谱显示优化

- **节点大小**：按"入链数"（入链越多，节点越大）
- **连线**：显示，透明度 30%
- **中心节点**：将 `Home` 设为中心节点
- **显示标签**：启用，便于识别节点
- **动画**：启用，图谱更生动

---

## Dataview 查询示例

在任意笔记中插入以下代码块，即可动态生成查询结果。

### 1. 学习进度总览

```dataview
TABLE 
  category AS "分类",
  difficulty AS "难度",
  status AS "状态",
  priority AS "优先级"
FROM ""
WHERE !contains(file.name, "MOC-") AND file.name != "Home"
SORT category ASC, difficulty ASC
```

### 2. 待学习核心笔记

```dataview
TABLE 
  category AS "分类",
  difficulty AS "难度",
  priority AS "优先级"
FROM ""
WHERE priority = "核心" AND !contains(status, "已完善")
SORT category ASC, difficulty ASC
```

### 3. 按分类统计笔记数量

```dataview
TABLE length(rows) AS "笔记数"
FROM ""
WHERE !contains(file.name, "MOC-") AND file.name != "Home"
GROUP BY category AS "分类"
SORT length(rows) DESC
```

### 4. 入门级笔记清单

```dataview
LIST
FROM ""
WHERE difficulty = "⭐"
SORT category ASC
```

### 5. 最近更新的笔记

```dataview
TABLE 
  category AS "分类",
  updated AS "更新时间"
FROM ""
WHERE !contains(file.name, "MOC-")
SORT updated DESC
LIMIT 10
```

### 6. 某分类的所有笔记

```dataview
TABLE 
  difficulty AS "难度",
  status AS "状态",
  priority AS "优先级"
FROM "01-前端开发"
WHERE !contains(file.name, "MOC-")
SORT difficulty ASC
```

### 7. 带特定标签的笔记

```dataview
LIST
FROM #Vue3
SORT file.name ASC
```

### 8. 学习完成度统计

```dataview
TABLE 
  length(rows) AS "总数",
  length(filter(rows, (r) => contains(r.status, "已完善"))) AS "已完成"
FROM ""
WHERE !contains(file.name, "MOC-") AND file.name != "Home"
GROUP BY category AS "分类"
```

---

## 快捷键配置

推荐自定义以下快捷键，提升使用效率：

### 常用操作

| 操作 | 推荐快捷键 | 说明 |
|------|-----------|------|
| 快速切换器 | `Ctrl+O` | 快速打开笔记 |
| 命令面板 | `Ctrl+P` | 执行任意命令 |
| 新建笔记 | `Ctrl+N` | 创建新笔记 |
| 全局搜索 | `Ctrl+Shift+F` | 全文搜索 |
| 关系图谱 | `Ctrl+G` | 打开图谱视图 |
| 反向链接 | `Ctrl+Shift+L` | 查看当前笔记的反向链接 |
| 大纲 | `Ctrl+Shift+O` | 查看当前笔记大纲 |
| 标签面板 | `Ctrl+Shift+T` | 查看所有标签 |

### 编辑操作

| 操作 | 推荐快捷键 | 说明 |
|------|-----------|------|
| 插入模板 | `Ctrl+T` | 使用 Templater 插入模板 |
| 切换编辑/预览 | `Ctrl+E` | 切换编辑模式 |
| 加粗 | `Ctrl+B` | 选中文本加粗 |
| 斜体 | `Ctrl+I` | 选中文本斜体 |
| 插入链接 | `Ctrl+K` | 插入 `[[]]` 链接 |
| 插入代码块 | `Ctrl+Shift+C` | 插入代码块 |

---

## 日常使用工作流

### 📅 每日学习流程

1. **打开知识库**（启动页自动显示 Home）
2. **查看待学清单**（Home 页的 Dataview 查询）
3. **选择一篇笔记学习**
4. **学习过程中**：
   - 高亮重要内容
   - 添加自己的理解和注释
   - 关联相关笔记（`[[]]`）
   - 记录疑问和问题
5. **学习完成后**：
   - 将 status 改为 `✅ 内容已完善`
   - 更新 updated 日期
   - 在学习日志中记录今日所学
6. **查看学习进度**（运行 `kb.bat progress` 或 Dataview 查询）

### 📝 新增笔记流程

1. **确定主题和分类**
2. **使用模板创建笔记**：
   ```bash
   kb.bat note --title "新主题" --category "分类" --difficulty 3 --kb-root ./my-kb
   ```
3. **填充五段式内容**（概述/原理/实操/问题/拓展）
4. **建立关联**：
   - 添加相关笔记的双链
   - 设置 pre 前置知识
   - 添加 aliases 别名
5. **更新 MOC**（note 命令会自动更新）
6. **质量检查**：
   ```bash
   kb.bat validate --kb-root ./my-kb
   ```

### 🔄 每周维护流程

1. **运行健康检查**：
   ```bash
   kb.bat audit --kb-root ./my-kb
   ```
2. **修复发现的问题**（死链、孤立文档、标签不规范等）
3. **一键标准化**：
   ```bash
   kb.bat standardize --kb-root ./my-kb
   ```
4. **查看学习进度**：
   ```bash
   kb.bat progress --kb-root ./my-kb
   ```
5. **整理本周新增笔记**，确保分类正确、关联完整
6. **更新学习计划**，根据进度调整下周学习重点

### 🎯 项目实战流程

1. **在 `99-项目实战` 目录创建项目笔记**
2. **关联相关知识点**（项目中用到的技术概念）
3. **记录项目过程**：
   - 需求分析
   - 技术选型
   - 架构设计
   - 遇到的问题和解决方案
   - 总结和反思
4. **项目完成后**，更新相关技术笔记的"实操"章节
5. **在 MOC 中添加项目索引**

---

## 💡 高级技巧

### 1. 使用别名快速搜索

在 Frontmatter 中设置 `aliases`，可以通过别名搜索到笔记：
```yaml
aliases: [Vue3组合式API, Composition API, Vue组合式]
```

### 2. 利用反向链接发现知识关联

查看笔记的反向链接面板，可以发现哪些笔记引用了当前笔记，从而发现潜在的知识关联。

### 3. 使用标签进行跨分类组织

标签不受文件夹限制，可以跨分类组织相关内容。例如 `#性能优化` 标签可以关联前端、后端、数据库等多个分类的笔记。

### 4. 定期导出图谱截图

在学习的不同阶段导出关系图谱截图，可以直观看到知识网络的成长过程。

### 5. 使用 Canvas 组织学习路线

使用 Obsidian Canvas 功能，将相关笔记拖拽到画布中，可视化组织学习路线和知识关联。

---

## 📚 更多资源

- [Obsidian 官方文档](https://help.obsidian.md/)
- [Obsidian 社区论坛](https://forum.obsidian.md/)
- [Dataview 文档](https://blacksmithgu.github.io/obsidian-dataview/)
- [Awesome Obsidian](https://github.com/kmaasrud/awesome-obsidian)

---

> 💡 **提示**：配置完成后，建议导出配置备份（设置 → 关于 → 导出配置），方便在其他设备上同步配置。
