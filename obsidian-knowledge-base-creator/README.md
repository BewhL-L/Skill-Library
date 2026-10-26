# 📚 Obsidian 知识库标准化生成器

> 基于经过 50+ 轮优化验证的「全栈工程 + AI 工程」知识库标准，自动生成结构完整、排版统一、元数据规范的新知识库。

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()
[![Version](https://img.shields.io/badge/Version-6.1-green.svg)]()
[![Tests](https://img.shields.io/badge/Tests-48%2F48%20passing-brightgreen.svg)]()
[![Coverage](https://img.shields.io/badge/Coverage-configured-brightgreen.svg)]()
[![Type Hints](https://img.shields.io/badge/Type%20Hints-100%25-brightgreen.svg)]()
[![Lint](https://img.shields.io/badge/Lint-0%20errors-brightgreen.svg)]()
[![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-blue.svg)]()
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)]()

---

## ✨ 核心特性

- 🎯 **12 个命令**：初始化、生成笔记、批量生成、MOC、健康检查、质量校验、标准化等
- 📁 **12 个分类**：全栈开发 + AI 工程的完整知识体系
- 📝 **五段式结构**：概述 → 原理 → 实操 → 问题 → 拓展
- 🏷️ **标准化元数据**：10 个 Frontmatter 字段，难度星级制
- 🔗 **双链网络**：自动建立笔记间关联，无孤立文档
- 📊 **学习进度**：基于元数据的可视化学习进度报告（6 大统计维度）
- 🧪 **完整测试体系**：单元测试 36 个 + 集成测试 12 个，48/48 全部通过
- 📈 **代码覆盖率**：完整的覆盖率配置，支持文本/HTML/XML/JSON 报告
- 📋 **类型注解 100% 覆盖**：全项目 63 个函数全部添加类型注解
- 🔍 **代码质量检查**：项目专属 lint 工具，0 错误 0 警告
- 🚀 **CI/CD 自动化**：GitHub Actions 7 个 Job，多平台多版本测试
- 🔒 **pre-commit 钩子**：提交前自动检查代码质量
- 🛠️ **现代化项目配置**：Makefile + pyproject.toml + requirements，符合 PEP 621 标准
- 🪟 **跨平台支持**：Windows / macOS / Linux
- 📚 **完整文档体系**：26 个文档，涵盖入门、核心、开发者、社区四大类

### 🆕 v6.1 新增：单文档深度重写能力增强

- ⚡ **明确触发条件**：9类关键词自动触发深度重写（"深度重写"/"内容不够"/"写成学习文档"等），与普通格式优化明确区分
- 📊 **量化质量门槛**：11项指标（最低≥100KB/≥100代码示例，推荐≥200KB/≥200代码示例），参考Python三文档平均250KB/240示例标杆
- 🔄 **四步执行流程**：每步明确产出物（详细大纲→完整内容→总结练习题→最终文档），含编写铁律和面试考点标注
- ✅ **深度重写验收清单**：17项检查（格式质量5项+内容质量8项+学习路径质量4项）
- 🔧 **pre字段bug修复**：repair-frontmatter.py的pre字段回归bug已修复（影响252个文件），8测试用例全部通过

### 🆕 v6.0 新增：递进学习文档生成体系

- 🎓 **零基础到实战老手**：四阶段学习模型（入门筑基→进阶提升→高级精通→专家架构）
- 📖 **三篇递进体系**：入门篇（零基础）→进阶篇（有基础）→实战篇（老手），内容不重复，难度递增
- ✅ **知识点五要素标准**：概念解释（通俗）+原理说明（深入）+可运行代码+使用场景/最佳实践+常见坑点
- 📝 **章节总结与梯度练习题**：每章末尾💡深度讲解+📝精简总结+🎯梯度练习题（基础⭐+进阶⭐⭐+实战⭐⭐⭐）
- 🌱 **零基础友好写作指引**：语言风格、代码示例、结构安排、禁止事项，确保新手也能看懂
- 🔄 **多轮复查优化流程**：第一轮内容深化→深度内容复查→第二轮优化补充→第三轮最终验证
- 🔍 **内容深度复查体系**：五大维度（学习路径/逻辑顺序/结构完整性/内容深度/内容缺失）+问题清单优先级分类
- 🛡️ **质量保障与修复体系**：4类渲染问题诊断+修复+验证闭环（Frontmatter/代码块/标题级别/综合问题）

### 🆕 v5.0 新增：质量保障与修复体系

- 🔧 **4类修复脚本**：Frontmatter修复/代码块修复/标题级别修复/综合验证
- 📋 **3大验证维度**：Frontmatter YAML可解析性/代码块开闭平衡/标题级别规范性
- 📖 **2本实战手册**：质量保障与修复指南 + Obsidian渲染陷阱手册（14种踩坑记录）

---

## 🚀 快速开始

### 1. 安装

**Windows**：
```bash
install.bat
```

**macOS / Linux**：
```bash
chmod +x install.sh
./install.sh
```

### 2. 初始化知识库

```bash
kb init --name "我的知识库" --path ./my-kb
```

### 3. 生成笔记

```bash
kb note --title "Vue3 响应式原理" --category "前端开发" --difficulty 3 --kb-root ./my-kb
```

### 4. 一键标准化

```bash
kb standardize --kb-root ./my-kb
```

### 5. 查看学习进度

```bash
kb progress --kb-root ./my-kb
```

---

## 📖 文档

### 入门文档

| 文档 | 说明 | 适合人群 |
|------|------|---------|
| [QUICKSTART.md](QUICKSTART.md) | 5 分钟快速上手 | 初学者 |
| [INSTALLATION.md](docs/INSTALLATION.md) | 详细安装指南（跨平台） | 所有用户 |
| [OBSIDIAN-GUIDE.md](docs/OBSIDIAN-GUIDE.md) | Obsidian 配置与使用指南 | 所有用户 |

### 核心文档

| 文档 | 说明 | 适合人群 |
|------|------|---------|
| [SKILL.md](SKILL.md) | 完整使用文档与规范 | 深入了解 |
| [TEMPLATES.md](docs/TEMPLATES.md) | 模板使用与自定义指南 | 进阶用户 |
| [PERFORMANCE.md](docs/PERFORMANCE.md) | 性能优化指南 | 大知识库用户 |
| [FAQ.md](docs/FAQ.md) | 常见问题解答（28 个问题） | 遇到问题时 |
| [USE-CASES.md](docs/USE-CASES.md) | 使用案例与最佳实践（6 个场景） | 所有用户 |
| [SUPPORT.md](docs/SUPPORT.md) | 获取支持的渠道 | 需要帮助时 |

### 开发者文档

| 文档 | 说明 | 适合人群 |
|------|------|---------|
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | 项目架构设计 | 开发者 |
| [TESTING.md](docs/TESTING.md) | 测试策略与指南 | 开发者 |
| [DEBUGGING.md](docs/DEBUGGING.md) | 调试与问题排查 | 开发者 |
| [CONTRIBUTING.md](docs/CONTRIBUTING.md) | 贡献指南 | 开发者 |
| [ROADMAP.md](docs/ROADMAP.md) | 未来发展路线图 | 所有人 |

### 社区与法律

| 文档 | 说明 |
|------|------|
| [CHANGELOG.md](CHANGELOG.md) | 版本变更记录（14 个版本） |
| [SECURITY.md](docs/SECURITY.md) | 安全策略 |
| [CODE_OF_CONDUCT.md](docs/CODE_OF_CONDUCT.md) | 社区行为准则 |
| [CONTRIBUTORS.md](docs/CONTRIBUTORS.md) | 贡献者名单 |
| [ACKNOWLEDGMENTS.md](docs/ACKNOWLEDGMENTS.md) | 致谢 |
| [CITATION.cff](CITATION.cff) | 学术引用 |
| [LICENSE](LICENSE) | MIT 许可证 |

---

## 🛠️ 命令一览

| 命令 | 功能 | 版本 |
|------|------|------|
| `init` | 初始化知识库（12分类目录 + Home + MOC + 学习路线） | v1.0 |
| `note` | 生成单篇标准化笔记（自动更新对应MOC） | v2.0 |
| `batch-note` | 从 JSON/YAML 列表批量生成笔记 | v2.2 |
| `moc` | 生成/更新 MOC 内容地图 | v1.0 |
| `audit` | 健康检查（Frontmatter/标签/死链/孤立文档/MOC） | v1.0 |
| `validate` | 质量校验（五段式结构/排版/代码块/链接） | v1.0 |
| `fix-fm` | 批量补全 Frontmatter 缺失字段 | v2.0 |
| `fix-link` | 自动修复高频死链（创建对应笔记） | v2.0 |
| `fix-tags` | 批量统一标签（100+ 映射规则） | v2.1 |
| `standardize` | 一键标准化（fix-fm → fix-link → 生成MOC → audit） | v2.1 |
| `progress` | 生成学习进度报告（6 大统计维度） | v2.1 |
| `info` | 显示帮助信息 | v1.0 |

查看完整帮助：
```bash
kb info
```

---

## 📁 项目结构

```
obsidian-knowledge-base-creator/
├── kb.bat                   # 🪟 Windows 启动器（自动调用 scripts/kb.py）
├── Makefile                 # 🔧 构建工具（20+命令）
├── pyproject.toml           # 📦 现代Python项目配置（PEP 621）
├── requirements.txt         # 📋 运行时依赖
├── requirements-dev.txt     # 📋 开发依赖
├── install.bat              # Windows 安装脚本
├── install.sh               # macOS/Linux 安装脚本
├── uninstall.bat            # Windows 卸载脚本
├── uninstall.sh             # macOS/Linux 卸载脚本
├── test-all.py              # 🧪 集成测试脚本（12个命令）
├── unit-test.py             # 🧪 单元测试脚本（36个用例）
├── lint.py                  # 🔍 代码质量检查脚本
├── .coveragerc              # 📊 代码覆盖率配置
├── .pre-commit-config.yaml  # 🚀 pre-commit 配置
├── .markdownlint.json       # 📝 Markdown 规范配置
├── .editorconfig            # 🎨 代码风格配置
├── .gitignore               # 版本控制忽略配置
├── CITATION.cff             # 📚 学术引用文件
├── .github/                 # 🐙 GitHub 配置（7个文件）
│   ├── workflows/ci.yml     # CI/CD 配置（7个Job）
│   ├── ISSUE_TEMPLATE/      # Issue 模板（3个）
│   ├── pull_request_template.md # PR 模板
│   ├── CODEOWNERS           # 代码所有者
│   └── FUNDING.yml          # 赞助配置
├── README.md                # 项目首页
├── QUICKSTART.md            # 快速开始
├── INSTALLATION.md          # 详细安装指南 🆕
├── SKILL.md                 # 完整文档
├── OBSIDIAN-GUIDE.md       # Obsidian 配置指南
├── TEMPLATES.md             # 模板使用指南 🆕
├── PERFORMANCE.md           # 性能优化指南 🆕
├── FAQ.md                   # 常见问题
├── USE-CASES.md             # 使用案例
├── SUPPORT.md               # 支持指南
├── CHANGELOG.md             # 变更日志（10个版本）
├── CONTRIBUTING.md          # 贡献指南
├── ARCHITECTURE.md          # 项目架构 🆕
├── TESTING.md               # 测试指南 🆕
├── DEBUGGING.md             # 调试指南 🆕
├── ROADMAP.md               # 发展路线图 🆕
├── SECURITY.md              # 安全策略
├── CODE_OF_CONDUCT.md       # 行为准则
├── CONTRIBUTORS.md          # 贡献者名单 🆕
├── ACKNOWLEDGMENTS.md       # 致谢 🆕
├── LICENSE                  # MIT 许可证
├── assets/                  # 模板文件（6个模板）
├── references/              # 参考文档（13个文档，含v6.0新增2个）
├── examples/sample-kb/      # 示例知识库（5个文件）
└── scripts/                 # 功能脚本（10个脚本，类型注解100%覆盖）
```

---

## 🧪 测试

### 运行所有测试

```bash
# 集成测试（12个命令）
python test-all.py

# 单元测试（36个用例）
python unit-test.py

# 使用 Makefile
make test
```

### 测试结果

```
集成测试:
  总测试数: 12
  ✅ 通过: 12
  ❌ 失败: 0
  通过率: 100.0%

单元测试:
  总测试数: 36
  ✅ 通过: 36
  ❌ 失败: 0
  通过率: 100.0%

总计: 48/48 全部通过
```

### 代码覆盖率

```bash
# 生成覆盖率报告
coverage run unit-test.py
coverage report          # 文本报告
coverage html            # HTML 报告
coverage xml             # XML 报告（用于 CI/CD）
```

---

## 🔍 代码质量

### 运行代码质量检查

```bash
# 项目专属 lint 工具
python lint.py --path scripts

# 使用 Makefile
make lint

# 完整质量检查（lint + test + type-check）
make check
```

### 质量指标

| 指标 | 数值 |
|------|------|
| 代码质量 | 0 错误，0 警告 |
| 类型注解覆盖率 | 100%（63/63 函数） |
| 测试通过率 | 100%（48/48） |
| CI/CD Job 数 | 7 个 |
| 支持 Python 版本 | 3.8 / 3.9 / 3.10 / 3.11 / 3.12 |
| 支持平台 | Windows / macOS / Linux |

---

## 📝 示例

查看示例知识库：
```
examples/sample-kb/
```

用 Obsidian 打开该目录，即可查看标准化知识库的实际效果，包含：
- 完整的五段式笔记示例（Vue3 响应式原理）
- 标准化 MOC 内容地图
- 知识库首页（含 Dataview 查询）
- 完整的 Frontmatter 和双链关联

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

详细贡献指南请查看 [CONTRIBUTING.md](docs/CONTRIBUTING.md)。

### 开发环境设置

```bash
# 安装开发依赖
pip install -r requirements-dev.txt

# 安装 pre-commit 钩子
pre-commit install

# 运行测试
make test

# 运行代码质量检查
make check
```

---

## 📄 许可证

MIT License

---

## 🙏 致谢

感谢所有使用和反馈的用户，是你们让这个工具不断完善！

---

## 📊 版本历史

| 版本 | 核心变更 |
|------|---------|
| v6.1 | **单文档深度重写能力增强 + pre字段bug修复**（9类触发关键词/11项量化质量门槛/四步执行流程/17项验收清单/pre字段回归bug修复） |
| v6.0 | **递进学习文档生成体系 + 多轮复查优化流程**（知识点五要素/三篇递进体系/梯度练习题/内容深度复查） |
| v5.1 | 标题级别深度修复体系（14文档实战验证，H2数量从最高87降至正常范围） |
| v5.0 | 质量保障与修复体系（171篇文档实战验证，4类渲染问题诊断+修复+验证） |
| v3.5 | MOC表格格式修复 + aliases字段补全 + 表格格式深度检查 |
| v3.1 | 现代化项目配置（Makefile + pyproject.toml + requirements） |
| v3.0 | 单元测试体系（36 个用例）+ 代码覆盖率配置 |
| v2.6 | 全项目类型注解 100% 覆盖（63/63 函数） |
| v2.5 | 代码质量检查 + pre-commit + CI/CD + Markdown 规范 |
| v2.4 | 跨平台支持（macOS/Linux）+ 安全扫描 |
| v2.3 | Obsidian 使用指南 + 示例知识库 + 自动化测试 |
| v2.2 | 批量生成笔记（batch-note）+ 快速上手指南 |
| v2.1 | 一键标准化 + 学习进度 + 标签统一 |
| v2.0 | 统一 CLI 入口 + Frontmatter/死链自动修复 |
| v1.0 | 初始版本，5 个核心脚本 + 5 个模板 + 5 个参考文档 |

详细变更请查看 [CHANGELOG.md](CHANGELOG.md)。
