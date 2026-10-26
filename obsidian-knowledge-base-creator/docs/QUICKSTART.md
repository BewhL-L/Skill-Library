# 🚀 快速开始指南

> 5 分钟上手 Obsidian 知识库标准化工具

---

## 📋 目录

1. [环境准备](#环境准备)
2. [快速体验（3分钟）](#快速体验3分钟)
3. [完整工作流（10分钟）](#完整工作流10分钟)
4. [常用命令速查](#常用命令速查)
5. [下一步](#下一步)

---

## 环境准备

### 系统要求
- Windows / macOS / Linux
- Python 3.8+

### 验证 Python 安装

```bash
python --version
```

如果显示 `Python 3.x.x`，说明环境已准备好。

---

## 快速体验（3分钟）

### 第 1 步：初始化知识库

```bash
# Windows
kb.bat init --name "我的知识库" --path ./my-kb

# macOS / Linux
python scripts/kb.py init --name "我的知识库" --path ./my-kb
```

这会自动创建：
- ✅ 12 个分类目录
- ✅ Home 首页
- ✅ 综合导航 MOC
- ✅ 学习路线总览
- ✅ 11 个分类 MOC

### 第 2 步：生成一篇笔记

```bash
kb.bat note --title "Vue3 响应式原理" --category "前端开发" --difficulty 3 --kb-root ./my-kb
```

这会自动：
- ✅ 在 `01-前端开发` 目录下创建笔记
- ✅ 生成五段式结构（概述/原理/实操/问题/拓展）
- ✅ 填写完整 Frontmatter
- ✅ 自动更新 `MOC-前端开发.md` 索引

### 第 3 步：查看学习进度

```bash
kb.bat progress --kb-root ./my-kb
```

查看知识库的整体完成度、分类进度、待学清单等。

🎉 **恭喜！你已经完成了快速体验。**

---

## 完整工作流（10分钟）

### 场景：从零搭建一个「前端开发」知识库

#### 1. 初始化（1分钟）

```bash
kb.bat init --name "前端开发知识库" --path ./frontend-kb --theme "前端工程化"
```

#### 2. 准备核心笔记列表（2分钟）

创建 `notes.json` 文件：

```json
[
  {"title": "HTML 基础", "category": "前端开发", "difficulty": 1, "tags": ["HTML", "前端"]},
  {"title": "CSS 布局", "category": "前端开发", "difficulty": 2, "tags": ["CSS", "前端"]},
  {"title": "JavaScript 核心", "category": "前端开发", "difficulty": 2, "tags": ["JavaScript", "前端"]},
  {"title": "Vue3 组合式 API", "category": "前端开发", "difficulty": 3, "tags": ["Vue3", "前端"]},
  {"title": "TypeScript 进阶", "category": "前端开发", "difficulty": 3, "tags": ["TypeScript", "前端"]},
  {"title": "Vite 构建工具", "category": "前端开发", "difficulty": 3, "tags": ["Vite", "前端工程化"]},
  {"title": "前端性能优化", "category": "前端开发", "difficulty": 4, "tags": ["性能优化", "前端"]}
]
```

#### 3. 批量生成笔记（2分钟）

```bash
# 先预览
kb.bat batch-note --list notes.json --kb-root ./frontend-kb --dry-run

# 确认无误后执行
kb.bat batch-note --list notes.json --kb-root ./frontend-kb
```

#### 4. 一键标准化（2分钟）

```bash
kb.bat standardize --kb-root ./frontend-kb
```

自动完成：
- ✅ 补全所有笔记的 Frontmatter
- ✅ 修复死链（高频概念自动创建笔记）
- ✅ 为所有分类更新 MOC 索引
- ✅ 输出健康检查报告

#### 5. 查看进度并开始学习（3分钟）

```bash
kb.bat progress --kb-root ./frontend-kb
```

然后用 Obsidian 打开 `./frontend-kb` 文件夹，开始学习！

---

## 常用命令速查

### 🏗️ 建库相关

| 命令 | 用途 | 示例 |
|------|------|------|
| `init` | 初始化知识库 | `kb.bat init --name "我的库" --path ./my-kb` |
| `note` | 生成单篇笔记 | `kb.bat note --title "Vue3" --category 前端开发 --kb-root ./my-kb` |
| `batch-note` | 批量生成笔记 | `kb.bat batch-note --list notes.json --kb-root ./my-kb` |
| `moc` | 生成 MOC | `kb.bat moc --category 前端开发 --kb-root ./my-kb` |

### 🔧 维护相关

| 命令 | 用途 | 示例 |
|------|------|------|
| `standardize` | 一键标准化 | `kb.bat standardize --kb-root ./my-kb` |
| `fix-fm` | 补全 Frontmatter | `kb.bat fix-fm --kb-root ./my-kb` |
| `fix-tags` | 统一标签 | `kb.bat fix-tags --kb-root ./my-kb --dry-run` |
| `fix-link` | 修复死链 | `kb.bat fix-link --kb-root ./my-kb --threshold 3` |

### 📊 检查相关

| 命令 | 用途 | 示例 |
|------|------|------|
| `audit` | 健康检查 | `kb.bat audit --kb-root ./my-kb` |
| `validate` | 质量校验 | `kb.bat validate --kb-root ./my-kb --strict` |
| `progress` | 学习进度 | `kb.bat progress --kb-root ./my-kb` |
| `info` | 帮助信息 | `kb.bat info` |

---

## 下一步

### 📖 深入了解

- 阅读 `SKILL.md` 了解完整功能
- 阅读 `references/` 目录了解各项规范
- 阅读 `FAQ.md` 查看常见问题

### 💡 进阶技巧

1. **将 Skill 目录添加到系统 PATH**，即可在任意目录使用 `kb` 命令
2. **使用 `--dry-run` 预览**，确认无误后再执行
3. **定期运行 `standardize`**，保持知识库标准化
4. **使用 `progress` 跟踪学习进度**，调整学习计划
5. **使用 Makefile 简化操作**：
   ```bash
   make test          # 运行所有测试
   make lint          # 代码质量检查
   make check         # 完整质量检查（lint + test + type-check）
   make coverage      # 生成代码覆盖率报告
   make clean         # 清理临时文件
   ```
6. **运行自动化测试验证工具正常**：
   ```bash
   python test-all.py      # 集成测试（12个命令）
   python unit-test.py     # 单元测试（36个用例）
   ```
7. **代码质量检查**：
   ```bash
   python lint.py --path scripts  # 检查脚本代码质量
   ```

### 🤝 遇到问题？

- 查看 `FAQ.md` 常见问题解答
- 运行 `kb.bat info` 查看命令帮助
- 检查 `CHANGELOG.md` 了解版本变更

---

> 💡 **提示**：第一次使用建议先在测试目录体验，熟悉后再用于真实知识库。
