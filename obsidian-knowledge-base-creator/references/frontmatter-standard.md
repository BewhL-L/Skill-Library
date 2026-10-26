# Frontmatter 标准规范

> 每篇笔记必须包含完整的 Frontmatter，这是 Obsidian 高级功能（Dataview 查询、图谱着色、筛选排序）的基础。
>
> **v5.0 更新**：基于 171 篇文档实战验证，新增 YAML 严格可解析规范，确保 Frontmatter 不被 ``` 标记污染，pre 字段格式统一。

---

## 标准字段（10 个）

```yaml
---
title: 笔记标题
tags: [标签1, 标签2, 标签3]
category: 所属分类
created: 2026-08-29
updated: 2026-08-29
difficulty: ⭐⭐⭐
status: ✅ 内容已完善
priority: 核心
pre: ["[[前置知识1]]", "[[前置知识2]]"]
aliases: [别名1, 别名2]
---
```

---

## 字段详解

### 1. title（必填）
笔记的显示标题，与文件名一致或更简洁。

### 2. tags（必填，3-8 个）
来自核心标签集的标签，涵盖：领域分类、技术栈、难度类型、应用场景。
- 禁止使用一次性标签
- 禁止使用与 category 重复的标签
- 参考 `tag-taxonomy.md` 选择标签

### 3. category（必填）
笔记所属的顶级分类，与所在文件夹对应：
- 综合导航、前端开发、后端开发、数据库与缓存、分布式与中间件
- 云原生与运维、计算机基础、通用工具、Python全栈、AI与效率工具、项目实战

### 4. created（必填）
创建日期，格式 `YYYY-MM-DD`。

### 5. updated（必填）
最后更新日期，格式 `YYYY-MM-DD`。每次内容更新后必须更新此字段。

### 6. difficulty（必填，星级制）
使用 ⭐ 到 ⭐⭐⭐⭐⭐ 五级难度：

| 星级 | 级别 | 说明 | 适用读者 |
|------|------|------|---------|
| ⭐ | 入门 | 基础概念、安装配置、快速上手 | 零基础新手 |
| ⭐⭐ | 进阶 | 核心用法、常见场景、最佳实践 | 有基础的开发者 |
| ⭐⭐⭐ | 高级 | 底层原理、架构设计、生产实践 | 资深开发者 |
| ⭐⭐⭐⭐ | 专家 | 源码分析、性能调优、复杂方案 | 技术专家 |
| ⭐⭐⭐⭐⭐ | 资深 | 前沿研究、跨领域融合、体系设计 | 技术架构师 |

### 7. status（必填）
内容状态：
- `✅ 内容已完善` — 内容完整，结构规范
- `📝 草稿` — 初步创建，内容待完善
- `🔄 更新中` — 正在更新内容
- `⚠️ 待审核` — 内容待审核验证

### 8. priority（必填）
学习优先级：
- `核心` — 必须掌握的核心概念，高频引用
- `重要` — 重要知识点，建议掌握
- `一般` — 了解即可，按需学习
- `可选` — 拓展内容，可选学习

### 9. pre（必填）
前置知识依赖，使用 `[[]]` 双链格式，**必须用双引号包裹在流序列中**：
```yaml
pre: ["[[Vue3基础]]", "[[TypeScript基础]]"]
```
无前置知识时填 `pre: []`。

**⚠️ 禁止**：`pre: [[Vue3基础]], [[TypeScript基础]]`（未加引号会导致 YAML 解析错误，因为 `[[` 在 YAML 中是嵌套序列开始符号）

### 10. aliases（可选）
笔记别名，用于解决死链和同义词问题：
```yaml
aliases: [Docker入门, Docker基础]
```
当其他笔记引用了别名时，Obsidian 会自动解析到本笔记。

---

## 示例

### 入门级笔记
```yaml
---
title: Docker 快速上手
tags: [Docker, 容器化, 云原生]
category: 云原生与运维
created: 2026-08-29
updated: 2026-08-29
difficulty: ⭐
status: ✅ 内容已完善
priority: 核心
pre: []
aliases: [Docker入门]
---
```

### 高级笔记
```yaml
---
title: Kubernetes 网络原理
tags: [Kubernetes, 云原生, 网络, 架构设计]
category: 云原生与运维
created: 2026-08-29
updated: 2026-08-29
difficulty: ⭐⭐⭐⭐
status: ✅ 内容已完善
priority: 重要
pre: ["[[Kubernetes基础]]", "[[Docker容器化]]", "[[计算机网络]]"]
aliases: [K8s网络, K8s网络原理]
---
```

---

## 常见错误

| 错误 | 正确做法 |
|------|---------|
| difficulty 使用 emoji 等级（🟢入门） | 使用星级制（⭐） |
| tags 使用一次性标签 | 只使用核心标签集 |
| 缺少 pre 字段 | 无前置知识时填 `pre: []` |
| status 使用随意文本 | 使用标准状态值 |
| category 与所在文件夹不一致 | category 必须与顶级文件夹对应 |
| 缺少 updated 字段 | 每次更新内容后必须更新 updated 日期 |
| **Frontmatter 内混入 ``` 标记** | **Frontmatter 内绝对不能出现 ```** |
| **pre 字段双链未加引号** | **必须使用 `pre: ["[[link]]"]` 格式** |
| **出现 `[[[[link]]]` 畸形多括号** | **必须修正为 `[[link]]`** |

---

## ⚠️ YAML 严格可解析规范（v5.0 新增）

基于 171 篇文档实战验证，Frontmatter 必须能被 YAML 解析器严格解析。以下是必须遵守的铁律：

### 铁律1：Frontmatter 内禁止出现 ``` 标记

**错误**（批量脚本最容易引入的问题，曾导致 170/171 个文件同时报错）：
```yaml
---
```
title: 笔记标题
tags: [标签1]
```
difficulty: ⭐⭐⭐
---
```

**正确**：
```yaml
---
title: 笔记标题
tags: [标签1]
difficulty: ⭐⭐⭐
---
```

**原因**：``` 标记会将 YAML 分割成多个代码块，导致 Obsidian 无法解析 Frontmatter，文档开头报错。

### 铁律2：pre 字段双链必须用双引号包裹

**错误**：
```yaml
pre: [[链接1]], [[链接2]]
```

**正确**：
```yaml
pre: ["[[链接1]]", "[[链接2]]"]
```

**原因**：`[[` 在 YAML 中是嵌套序列的开始符号，与 wiki-link 语法冲突，必须用双引号包裹为字符串。

### 铁律3：禁止畸形多括号

**错误**：
```yaml
pre: ["[[[[链接]]]"]
```

**正确**：
```yaml
pre: ["[[链接]]"]
```

### 验证方法

每次批量处理后，必须运行 YAML 解析验证：

```python
import yaml
with open('file.md', 'r', encoding='utf-8') as f:
    content = f.read()
fm_text = content.split('---')[1]
data = yaml.safe_load(fm_text)
assert isinstance(data, dict)
```

或使用 skill 提供的验证脚本：
```bash
python scripts/verify-kb.py --path "知识库路径" --check frontmatter
```

### 批量写入安全准则

1. 使用 YAML 库（PyYAML）序列化 Frontmatter，不要手动拼接字符串
2. 写入后立即用 `yaml.safe_load()` 验证
3. Frontmatter 模板中不要包含任何 ``` 标记
4. 处理前备份原文件
5. 小批量测试后再全量执行

---

## 相关文档

- `references/quality-assurance-and-repair.md` — 质量保障与修复指南（Frontmatter 修复章节）
- `references/obsidian-rendering-pitfalls.md` — Obsidian 渲染陷阱手册（陷阱1-3）
