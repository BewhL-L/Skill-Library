# 项目架构文档

## 📋 概述

本文档描述 Obsidian 知识库标准化生成器的整体架构设计、模块划分、数据流和关键设计决策。

---

## 🏗️ 整体架构

### 架构分层

```
┌─────────────────────────────────────────────────────────┐
│                    用户交互层 (CLI)                       │
│  kb.py / kb.bat / install.bat / install.sh              │
├─────────────────────────────────────────────────────────┤
│                    命令调度层                              │
│  argparse 命令解析 → 子命令分发 → 参数验证                 │
├─────────────────────────────────────────────────────────┤
│                    业务逻辑层                              │
│  init / note / batch-note / moc / audit / validate      │
│  fix-fm / fix-link / fix-tags / standardize / progress  │
├─────────────────────────────────────────────────────────┤
│                    核心工具层                              │
│  frontmatter 解析 / 标签处理 / 双链检测 / 文件扫描        │
│  模板渲染 / 日志记录 / 异常处理 / 类型检查                 │
├─────────────────────────────────────────────────────────┤
│                    数据存储层                              │
│  Markdown 文件 / YAML Frontmatter / 目录结构 / 模板文件   │
└─────────────────────────────────────────────────────────┘
```

---

## 📁 目录结构

```
obsidian-knowledge-base-creator/
├── kb.bat                   # 🪟 Windows 启动器（自动调用 scripts/kb.py）
├── Makefile                 # 🔧 构建工具
├── pyproject.toml           # 📦 项目配置
├── requirements.txt         # 📋 运行时依赖
├── requirements-dev.txt     # 📋 开发依赖
├── install.bat / install.sh # 📦 跨平台安装脚本
├── uninstall.bat / uninstall.sh # 🗑️ 跨平台卸载脚本
├── test-all.py              # 🧪 集成测试
├── unit-test.py             # 🧪 单元测试
├── lint.py                  # 🔍 代码质量检查
├── .coveragerc              # 📊 覆盖率配置
├── .pre-commit-config.yaml  # 🚀 pre-commit 配置
├── .markdownlint.json       # 📝 Markdown 规范
├── .editorconfig            # 🎨 编辑器配置
├── .gitignore               # 🚫 Git 忽略
├── .github/                 # 🐙 GitHub 配置
│   ├── workflows/ci.yml     # CI/CD 配置
│   ├── ISSUE_TEMPLATE/      # Issue 模板
│   ├── pull_request_template.md # PR 模板
│   ├── CODEOWNERS           # 代码所有者
│   └── FUNDING.yml          # 赞助配置
├── assets/                  # 📄 模板文件（6个）
├── references/              # 📚 参考文档（5个）
├── examples/sample-kb/      # 📝 示例知识库（5个文件）
├── scripts/                 # 🔧 核心脚本（10个）
└── docs/                    # 📖 用户文档（12个）
```

---

## 🔧 核心模块

### 1. CLI 入口模块（scripts/kb.py）

**职责**：统一命令行入口，解析参数，分发到对应子命令。

**关键函数**：
- `main()` - 主入口函数
- `create_parser()` - 创建参数解析器
- `cmd_init()` - 初始化知识库命令
- `cmd_note()` - 生成笔记命令
- `cmd_batch_note()` - 批量生成笔记命令
- `cmd_moc()` - 生成 MOC 命令
- `cmd_audit()` - 健康检查命令
- `cmd_validate()` - 质量校验命令
- `cmd_fix_fm()` - 补全 Frontmatter 命令
- `cmd_fix_link()` - 修复死链命令
- `cmd_fix_tags()` - 统一标签命令
- `cmd_standardize()` - 一键标准化命令
- `cmd_progress()` - 学习进度命令
- `cmd_info()` - 帮助信息命令

**设计决策**：
- 使用 argparse 而非 click/typer，减少依赖
- 所有子命令函数统一命名 `cmd_xxx`
- 每个命令独立处理异常，不影响其他命令
- 支持 `--dry-run` 预览模式，避免误操作

### 2. 初始化模块（scripts/init-kb.py）

**职责**：创建知识库目录结构、首页、MOC、学习路线等核心文件。

**核心流程**：
1. 验证输入参数（名称、路径、主题）
2. 创建 12 个顶级分类目录
3. 生成 Home 首页
4. 生成综合导航 MOC
5. 生成学习路线总览
6. 为每个分类生成标准化 MOC
7. 输出创建结果统计

### 3. 笔记生成模块（scripts/generate-note.py）

**职责**：生成符合五段式结构的标准化笔记。

**核心流程**：
1. 验证输入参数（标题、分类、难度）
2. 加载笔记模板
3. 填充 Frontmatter 元数据
4. 生成五段式内容结构
5. 写入目标文件
6. 自动更新对应 MOC 索引

### 4. MOC 生成模块（scripts/generate-moc.py）

**职责**：扫描目录下所有笔记，生成标准化 MOC 内容地图。

**核心流程**：
1. 扫描目标目录下所有 Markdown 文件
2. 解析每篇笔记的 Frontmatter
3. 按难度/优先级/创建时间排序
4. 生成学习路线
5. 生成文档索引表
6. 生成知识关联图
7. 生成学习顺序建议
8. 写入 MOC 文件

### 5. 健康检查模块（scripts/audit-kb.py）

**职责**：检测知识库的健康状况，输出健康报告。

**检查维度**：
- Frontmatter 完整性（10 个标准字段）
- 标签规范性（是否来自核心标签集）
- 死链检测（引用但不存在的笔记）
- 孤立文档检测（无入链也无出链）
- MOC 覆盖率（每个分类是否有 MOC）
- 目录结构完整性（12 个顶级分类）

### 6. 质量校验模块（scripts/validate-kb.py）

**职责**：严格校验每篇笔记是否符合规范。

**校验项**：
- 五段式结构完整性（概述/原理/实操/问题/拓展）
- Frontmatter 字段标准
- 排版规范（标题层级、表格格式、代码块语言）
- 链接有效性
- 标签数量（3-8 个）
- 难度星级制

### 7. Frontmatter 修复模块（scripts/fix-frontmatter.py）

**职责**：批量补全 Frontmatter 缺失字段。

**修复策略**：
- 根据文件夹自动推断 category
- 根据文件名推断 difficulty/priority
- 自动填充 created/updated 时间
- 默认 status 为 📝 草稿
- 自动生成 aliases（文件名变体）

### 8. 死链修复模块（scripts/fix-links.py）

**职责**：自动修复高频死链。

**修复策略**：
- 统计所有死链的引用次数
- 高频死链（≥阈值）创建对应笔记
- 低频死链映射到已有文档或添加别名
- 支持 `--threshold` 参数控制修复范围
- 支持 `--dry-run` 预览模式

### 9. 标签统一模块（scripts/fix-tags.py）

**职责**：批量统一标签体系。

**修复策略**：
- 100+ 标签映射规则
- 合并重复标签（大小写、拼写变体）
- 删除无意义标签（一次性标签）
- 映射到核心标签集（77 个）
- 支持 `--dry-run` 预览模式

### 10. 一键标准化模块（scripts/standardize.py）

**职责**：整合所有修复功能，一键完成知识库标准化。

**执行流程**：
1. `fix-fm` - 补全 Frontmatter
2. `fix-link` - 修复高频死链
3. `fix-tags` - 统一标签体系
4. `generate-moc` - 生成所有 MOC
5. `audit` - 健康检查并输出报告

---

## 🔄 数据流

### 新建知识库数据流

```
用户输入（名称/路径/主题）
    ↓
参数验证
    ↓
目录结构创建（12个分类）
    ↓
模板加载（home/moc/learning-path）
    ↓
模板渲染（填充变量）
    ↓
文件写入（Home/MOC/学习路线）
    ↓
结果统计与输出
```

### 笔记生成数据流

```
用户输入（标题/分类/难度/标签）
    ↓
参数验证
    ↓
模板加载（note-template）
    ↓
Frontmatter 生成（10个字段）
    ↓
五段式内容生成（概述/原理/实操/问题/拓展）
    ↓
文件写入（目标目录）
    ↓
MOC 自动更新（添加索引）
```

### 健康检查数据流

```
知识库路径
    ↓
目录扫描（所有 .md 文件）
    ↓
逐文件解析（Frontmatter + 内容）
    ↓
多维度检查（Frontmatter/标签/死链/孤立/MOC）
    ↓
问题收集与分类
    ↓
健康报告生成（统计 + 详情 + 建议）
```

---

## 🎯 关键设计决策

### 1. 为什么使用 Python？

- 跨平台支持（Windows/macOS/Linux）
- 丰富的标准库（argparse/pathlib/re/json/yaml）
- 易于学习和贡献
- 与数据科学/AI 生态契合

### 2. 为什么使用 argparse 而非 click/typer？

- 零外部依赖，降低安装复杂度
- Python 标准库，无需额外安装
- 功能足够满足当前需求
- 减少供应链攻击风险

### 3. 为什么使用 YAML Frontmatter？

- Obsidian 原生支持
- 人类可读，易于编辑
- 支持复杂数据结构（列表、嵌套对象）
- 与 Dataview 等插件无缝集成

### 4. 为什么使用五段式结构？

- 符合技术学习的认知规律
- 概述→原理→实操→问题→拓展，层层递进
- 确保内容完整性，避免遗漏
- 便于自动化校验和质量控制

### 5. 为什么使用星级制难度？

- 直观清晰，一眼可辨
- 符合用户偏好（比等级制更直白）
- 五级划分，粒度适中
- 与学习路线四阶段对应

---

## 📊 依赖关系

### 运行时依赖

| 依赖 | 版本 | 用途 |
|------|------|------|
| Python | ≥3.8 | 运行环境 |
| PyYAML | ≥6.0 | YAML 解析（可选，标准库 fallback） |

### 开发依赖

| 依赖 | 版本 | 用途 |
|------|------|------|
| pytest | ≥7.0 | 单元测试框架 |
| coverage | ≥7.0 | 代码覆盖率 |
| flake8 | ≥6.0 | 代码风格检查 |
| black | ≥23.0 | 代码格式化 |
| isort | ≥5.0 | 导入排序 |
| mypy | ≥1.0 | 类型检查 |
| pre-commit | ≥3.0 | 提交前钩子 |
| bandit | ≥1.7 | 安全扫描 |
| safety | ≥2.0 | 依赖漏洞检查 |

---

## 🔌 扩展点

### 1. 新增命令

在 `scripts/kb.py` 中添加新的子命令：
1. 在 `create_parser()` 中添加子命令解析器
2. 创建 `cmd_xxx()` 函数处理命令
3. 在 `main()` 中添加命令分发
4. 添加对应的单元测试和集成测试

### 2. 新增模板

在 `assets/` 目录中添加新的模板文件：
1. 创建模板文件（支持 `{{变量}}` 占位符）
2. 在对应脚本中加载模板
3. 实现模板渲染逻辑
4. 添加模板使用文档

### 3. 新增检查项

在 `scripts/audit-kb.py` 或 `scripts/validate-kb.py` 中添加新的检查项：
1. 实现检查函数
2. 在主流程中调用
3. 在报告中添加输出
4. 添加对应的测试用例

### 4. 新增标签映射规则

在 `scripts/fix-tags.py` 中添加新的标签映射规则：
1. 在 `TAG_MAPPINGS` 字典中添加映射
2. 运行测试确保不影响现有规则
3. 更新标签分类体系文档

---

## 📝 版本演进

| 版本 | 主要架构变更 |
|------|-------------|
| v1.0 | 初始架构，5 个独立脚本 |
| v2.0 | 统一 CLI 入口（scripts/kb.py），脚本模块化 |
| v2.1 | 一键标准化（standardize），流程编排 |
| v2.3 | 自动化测试体系，质量保障 |
| v2.5 | CI/CD + pre-commit，工程化完善 |
| v2.6 | 全项目类型注解，类型安全 |
| v3.0 | 单元测试体系，测试覆盖率 |
| v3.1 | 现代化项目配置（Makefile/pyproject） |

---

## 📞 相关文档

- [README.md](../README.md) - 项目首页
- [CONTRIBUTING.md](CONTRIBUTING.md) - 贡献指南
- [TESTING.md](TESTING.md) - 测试指南
- [DEBUGGING.md](DEBUGGING.md) - 调试指南
- [SECURITY.md](SECURITY.md) - 安全策略
- [CHANGELOG.md](../CHANGELOG.md) - 版本变更记录

---

> **最后更新**：2026-08-30
>
> **版本**：v3.1
