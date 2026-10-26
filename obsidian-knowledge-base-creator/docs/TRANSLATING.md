# 翻译指南

## 📋 概述

本文档描述如何将 Obsidian 知识库标准化生成器翻译为其他语言，包括翻译流程、术语规范、质量检查和提交指南。

---

## 🌍 支持的语言

### 当前支持

| 语言 | 状态 | 翻译者 | 最后更新 |
|------|------|--------|---------|
| 中文（简体） | ✅ 完成 | 项目创建者 | 2026-08-30 |
| 英文 | ⬜ 待开始 | - | - |
| 日文 | ⬜ 待开始 | - | - |
| 韩文 | ⬜ 待开始 | - | - |

### 计划支持

- 中文（繁体）
- 法文
- 德文
- 西班牙文
- 葡萄牙文（巴西）
- 俄文
- 阿拉伯文

---

## 📝 翻译范围

### 需要翻译的文件

| 文件类型 | 文件 | 优先级 |
|---------|------|--------|
| 项目首页 | README.md | 高 |
| 快速上手 | QUICKSTART.md | 高 |
| 安装指南 | INSTALLATION.md | 高 |
| 完整文档 | SKILL.md | 高 |
| 常见问题 | FAQ.md | 中 |
| 使用案例 | USE-CASES.md | 中 |
| 贡献指南 | CONTRIBUTING.md | 中 |
| 行为准则 | CODE_OF_CONDUCT.md | 中 |
| 安全策略 | SECURITY.md | 中 |
| 支持指南 | SUPPORT.md | 低 |
| 模板指南 | TEMPLATES.md | 低 |
| 性能指南 | PERFORMANCE.md | 低 |
| 开发者文档 | ARCHITECTURE.md, TESTING.md, DEBUGGING.md | 低 |

### 不需要翻译的文件

- 代码文件（.py）
- 配置文件（.yaml, .json, .toml, .cfg）
- 模板文件（assets/ 目录下）
- 示例文件（examples/ 目录下）
- CHANGELOG.md（版本历史，保持英文）
- LICENSE（法律文件，保持英文）
- CITATION.cff（学术引用，保持英文）

---

## 🚀 开始翻译

### 1. 确认翻译意愿

在开始翻译前，请先：
1. 查看 [CONTRIBUTORS.md](CONTRIBUTORS.md) 确认是否已有该语言的翻译者
2. 在 GitHub Discussions 中发帖说明你想翻译的语言
3. 等待维护者确认并分配翻译任务

### 2. Fork 项目

```bash
# Fork 项目到你的 GitHub 账户
# 然后克隆你的 Fork
git clone https://github.com/your-username/obsidian-knowledge-base-creator.git
cd obsidian-knowledge-base-creator
```

### 3. 创建翻译分支

```bash
# 创建翻译分支，命名规范：translation/<语言代码>
git checkout -b translation/zh-TW
# 或
git checkout -b translation/ja
# 或
git checkout -b translation/ko
```

### 4. 创建翻译目录

```bash
# 在 docs/ 目录下创建语言子目录
mkdir -p docs/zh-TW
mkdir -p docs/ja
mkdir -p docs/ko

# 复制需要翻译的文件
cp README.md docs/zh-TW/README.md
cp QUICKSTART.md docs/zh-TW/QUICKSTART.md
# ... 其他文件
```

### 5. 开始翻译

使用你熟悉的 Markdown 编辑器开始翻译。推荐使用：
- **VS Code** + Markdown 插件
- **Obsidian**（本项目就是为 Obsidian 设计的）
- **Typora**
- **任何支持 Markdown 的文本编辑器**

---

## 📖 翻译规范

### 1. 术语一致性

#### 核心术语对照表

| 英文 | 中文（简体） | 日文 | 韩文 | 说明 |
|------|-------------|------|------|------|
| Knowledge Base | 知识库 | 知識ベース | 지식 베이스 | 核心概念 |
| MOC (Map of Content) | 内容地图 | コンテンツマップ | 콘텐츠 맵 | 保持缩写 MOC |
| Frontmatter | 元数据/Frontmatter | フロントマター | 프론트매터 | 可保留英文 |
| Wiki Link | Wiki 链接 | Wikiリンク | Wiki 링크 | `[[]]` 格式 |
| Backlink | 反向链接 | バックリンク | 백링크 | |
| Atomic Note | 原子化笔记 | アトミックノート | 원자 노트 | |
| Learning Path | 学习路线 | 学習パス | 학습 경로 | |
| Difficulty | 难度 | 難易度 | 난이도 | |
| Status | 状态 | ステータ스 | 상태 | |
| Priority | 优先级 | 優先度 | 우선순위 | |
| Tag | 标签 | タグ | 태그 | |
| Category | 分类 | カテゴリ | 카테고리 | |
| Template | 模板 | テンプレート | 템플릿 | |
| Plugin | 插件 | プラグイン | 플러그인 | |
| Vault | 仓库/Vault | ボールト | 볼트 | Obsidian 术语 |

#### 术语使用原则

1. **首次出现时标注原文**：如「内容地图（MOC, Map of Content）」
2. **后续使用统一术语**：保持全文一致
3. **技术术语可保留英文**：如 Frontmatter、Vault、YAML 等
4. **参考 Obsidian 官方翻译**：保持与 Obsidian 官方术语一致

### 2. 格式规范

#### Markdown 格式

- **保持原始 Markdown 格式**：标题层级、列表、表格、代码块等
- **不修改链接目标**：`[链接文字](URL)` 中的 URL 保持不变
- **不修改图片路径**：图片路径保持不变
- **代码块不翻译**：代码块中的代码保持原样，只翻译注释

#### 代码块处理

```markdown
**翻译前**：
```bash
# This is a comment
python scripts/kb.py init --name "My KB"
```

**翻译后**：
```bash
# 这是一条注释
python scripts/kb.py init --name "我的知识库"
```
```

**注意**：
- 命令和参数不翻译
- 注释可以翻译
- 输出示例可以翻译（如果是用户可见的输出）

#### Frontmatter 处理

Frontmatter 中的值可以翻译，但键名保持英文：

```yaml
---
title: 翻译后的标题
tags: [标签1, 标签2]
category: 翻译后的分类
created: 2026-08-30
updated: 2026-08-30
difficulty: ⭐⭐⭐
status: ✅ 内容已完善
priority: 核心
---
```

### 3. 文化适配

- **日期格式**：根据目标语言地区习惯调整（如中文用 2026年8月30日，英文用 August 30, 2026）
- **数字格式**：千位分隔符、小数点等根据地区习惯调整
- **示例内容**：可以使用目标语言地区更熟悉的示例
- **引用资源**：优先引用目标语言的资源

---

## ✅ 质量检查

### 翻译完成后检查清单

- [ ] 所有需要翻译的文件都已翻译
- [ ] 术语使用一致（参考术语对照表）
- [ ] Markdown 格式保持完整
- [ ] 链接目标未修改
- [ ] 代码块中的命令和参数未翻译
- [ ] Frontmatter 键名保持英文
- [ ] 图片路径未修改
- [ ] 没有遗漏的英文文本（除技术术语外）
- [ ] 翻译符合目标语言的表达习惯
- [ ] 没有错别字和语法错误

### 自动检查工具

```bash
# 检查 Markdown 格式
npx markdownlint docs/zh-TW/

# 检查链接有效性
# 使用 markdown-link-check 或类似工具

# 检查未翻译的文本（简单检查）
grep -r "TODO\|FIXME\|TBD" docs/zh-TW/
```

### 人工审核

翻译完成后，需要：
1. **自我审核**：通读全文，检查准确性和流畅性
2. **母语者审核**：如果可能，请目标语言的母语者审核
3. **技术审核**：请熟悉项目的技术人员审核技术术语
4. **维护者审核**：提交 PR 后，项目维护者会进行最终审核

---

## 📤 提交翻译

### 1. 提交更改

```bash
# 添加更改
git add docs/zh-TW/

# 提交，提交信息遵循 Conventional Commits
git commit -m "docs: add Traditional Chinese translation"

# 推送到你的 Fork
git push origin translation/zh-TW
```

### 2. 创建 Pull Request

在 GitHub 上创建 Pull Request：
- **标题**：`docs: add <语言> translation`
- **描述**：
  - 翻译的语言
  - 翻译的文件列表
  - 翻译完成度（百分比）
  - 翻译者信息
  - 任何需要注意的问题

### 3. 等待审核

- 维护者会在 7 个工作日内审核
- 可能会要求修改某些部分
- 审核通过后会合并到主分支

---

## 🔄 维护翻译

### 同步更新

当原始文档更新时，翻译也需要同步更新：

1. **监控变更**：Watch 项目，接收更新通知
2. **定期检查**：每月检查一次原始文档的变更
3. **及时更新**：发现变更后及时更新翻译
4. **标注版本**：在翻译文档末尾标注对应的原始文档版本

### 翻译版本标注

在每个翻译文档的末尾添加：

```markdown
---

> **翻译信息**
> - 语言：中文（繁体）
> - 翻译者：[翻译者名称](GitHub链接)
> - 最后更新：2026-08-30
> - 对应原文版本：v3.1.0
> - 原文链接：[README.md](../README.md)
```

---

## 🎁 翻译者权益

- 名字会被列入 [CONTRIBUTORS.md](CONTRIBUTORS.md) 的翻译贡献者名单
- 获得项目贡献者徽章
- 优先参与项目决策
- 翻译质量优秀者可成为该语言的维护者
- 在项目发布说明中被致谢

---

## ❓ 常见问题

### Q1: 我可以只翻译部分文件吗？

A: 可以。建议从高优先级文件开始（README、QUICKSTART、INSTALLATION、SKILL），逐步完成其他文件。

### Q2: 翻译过程中遇到不确定的术语怎么办？

A: 
1. 参考 Obsidian 官方文档的翻译
2. 在翻译文档中用注释标注不确定的术语
3. 在 PR 描述中说明需要讨论的术语
4. 与维护者讨论确定统一译法

### Q3: 翻译完成后发现错误怎么办？

A: 随时可以提交新的 PR 修正错误。小的错别字修正会快速合并。

### Q4: 可以机翻后人工校对吗？

A: 可以使用机器翻译作为辅助，但必须经过人工校对，确保翻译质量和表达自然。纯机翻未经校对的 PR 会被拒绝。

### Q5: 如何成为某语言的维护者？

A: 
1. 完成该语言至少 80% 的翻译
2. 持续维护翻译 3 个月以上
3. 翻译质量优秀，获得社区认可
4. 获得现有维护者推荐

---

## 📞 联系翻译团队

- **翻译讨论**：[GitHub Discussions](https://github.com/your-username/obsidian-knowledge-base-creator/discussions)
- **翻译协调者**：项目创建者
- **邮件**：translation@example.com

---

> **最后更新**：2026-08-30
>
> **版本**：v1.0
