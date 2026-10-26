# Skill 工程化优化器

> 基于 25 轮实战优化经验，提供 Skill 健康检查、自动优化、文档生成、测试生成全流程工具链。

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()
[![Version](https://img.shields.io/badge/version-1.5.0-green.svg)]()
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)]()

---

## ✨ 功能特性

### 🔍 Skill 健康检查
- 8 大维度全面评估（元数据/文档/代码/测试/工程化/模板/易用性/可维护性）
- 自动生成健康报告和优化建议
- 支持 JSON 格式输出，便于集成

### 🚀 自动优化
- 自动补全缺失文档（README/CHANGELOG/FAQ 等 10+ 种）
- 自动生成工程化配置（.gitignore/.editorconfig/pre-commit/CI/CD）
- 支持预览模式（--dry-run）
- 支持按部分优化（docs/code/config）

### 📚 文档生成
- 自动解析 Python 脚本，生成 API 参考文档
- 生成 FAQ、使用案例、架构文档
- 函数签名、参数、返回值、docstring 自动提取

### 🧪 测试生成
- 自动生成单元测试模板（每个函数 3 个用例）
- 生成集成测试模板（CLI 命令/工作流）
- 生成 conftest.py 和覆盖率配置

### 🎯 25 轮优化方法论
- 完整的 5 阶段 25 轮优化指南
- 100+ 项检查清单
- 专业级质量标准

---

## 📦 安装

### 方式一：直接使用

```bash
# 克隆或下载到任意目录
git clone <repo-url>
cd skill-optimizer

# 无需安装依赖（仅使用 Python 标准库）
```

### 方式二：作为豆包 Skill

将整个文件夹复制到豆包用户技能目录：
```
Windows: C:\Users\{用户名}\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\.user_skills\
macOS: ~/Library/Application Support/Doubao/User Data/Default/.doubao/agent_mode/workspace/.user_skills/
```

重启豆包即可使用。

---

## 🚀 快速开始

### 1. 健康检查

```bash
python skill-opt.py audit --path ./my-skill
```

输出示例：
```
🔍 开始审计 Skill: ./my-skill
============================================================

📋 检查元数据完整性...
  得分: 80/100, 问题: 2 个

📚 检查文档完整性...
  得分: 50/100, 问题: 8 个
...

📊 审计报告
============================================================
总分: 62.5/100  ⚠️ B 级（良好）
```

### 2. 自动优化

```bash
# 预览模式（不实际修改）
python skill-opt.py optimize --path ./my-skill --dry-run

# 执行优化
python skill-opt.py optimize --path ./my-skill --auto

# 只优化文档
python skill-opt.py optimize --path ./my-skill --only docs
```

### 3. 生成文档

```bash
# 生成所有文档
python skill-opt.py docs --path ./my-skill --type all

# 只生成 API 文档
python skill-opt.py docs --path ./my-skill --type api
```

### 4. 生成测试

```bash
# 生成所有测试
python skill-opt.py tests --path ./my-skill --type all

# 只生成单元测试
python skill-opt.py tests --path ./my-skill --type unit
```

### 5. 一键全流程

```bash
python skill-opt.py all --path ./my-skill
```

自动执行：健康检查 → 自动优化 → 生成文档 → 生成测试 → 验证报告

---

## 📚 文档

| 文档 | 说明 |
|------|------|
| [SKILL.md](SKILL.md) | 完整功能说明 |
| [QUICKSTART.md](QUICKSTART.md) | 5 分钟快速上手 |
| [OPTIMIZATION-GUIDE.md](OPTIMIZATION-GUIDE.md) | 25 轮优化完整指南 |
| [CHECKLIST.md](CHECKLIST.md) | 优化检查清单（100+ 项） |
| [QUALITY-STANDARDS.md](QUALITY-STANDARDS.md) | 质量标准与验收规范 |
| [FAQ.md](FAQ.md) | 常见问题 |
| [CHANGELOG.md](CHANGELOG.md) | 版本变更记录 |

---

## 🛠️ 命令一览

```bash
# 健康检查
python skill-opt.py audit --path <skill路径> [--format text|json] [--output 文件]

# 自动优化
python skill-opt.py optimize --path <skill路径> [--auto] [--dry-run] [--only docs,code,config]

# 生成文档
python skill-opt.py docs --path <skill路径> [--type all|api|faq|examples|architecture]

# 生成测试
python skill-opt.py tests --path <skill路径> [--type all|unit|integration|conftest|coverage]

# 一键全流程
python skill-opt.py all --path <skill路径>

# 帮助信息
python skill-opt.py info
```

---

## 📊 优化效果

| 指标 | 优化前（典型） | 优化后（目标） |
|------|--------------|--------------|
| audit 总分 | 40-60 | 90+ |
| 文档数量 | 2-3 | 15+ |
| 测试覆盖率 | 0% | 80%+ |
| 类型注解覆盖 | 0% | 100% |
| 代码质量问题 | 10+ | 0 |
| 用户上手时间 | 30 分钟+ | 5 分钟 |

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 运行测试
5. 提交 Pull Request

详细贡献指南请参考 [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📄 许可证

MIT License

---

## 🙏 致谢

本项目基于对 `obsidian-knowledge-base-creator` Skill 进行 25 轮深度优化的实战经验提炼而成。
