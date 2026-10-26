# 获取支持

感谢你使用 Obsidian 知识库标准化生成器！本文档列出了获取支持的各种渠道和方式。

---

## 📚 自助资源

在寻求支持之前，请先查阅以下自助资源，可能已经有你需要的答案：

### 1. 文档

| 文档 | 用途 |
|------|------|
| [README.md](../README.md) | 项目首页，功能概览 |
| [QUICKSTART.md](../QUICKSTART.md) | 5 分钟快速上手 |
| [SKILL.md](../SKILL.md) | 完整功能和规范说明 |
| [OBSIDIAN-GUIDE.md](OBSIDIAN-GUIDE.md) | Obsidian 配置与使用指南 |
| [FAQ.md](FAQ.md) | 常见问题解答（28 个问题） |
| [USE-CASES.md](USE-CASES.md) | 使用案例与最佳实践（6 个场景） |
| [CHANGELOG.md](../CHANGELOG.md) | 版本变更记录 |

### 2. 示例

查看 [examples/sample-kb/](examples/sample-kb/) 目录中的示例知识库，了解标准化知识库的实际效果。

### 3. 命令帮助

```bash
# 查看所有命令帮助
kb info

# 查看特定命令帮助
python scripts/kb.py init --help
python scripts/kb.py note --help
python scripts/kb.py standardize --help
```

---

## ❓ 常见问题

### 安装问题

**Q: 提示 "python 不是内部或外部命令"**
A: Python 未安装或未添加到系统 PATH。请安装 Python 3.8+ 并勾选 "Add Python to PATH"。

**Q: 安装后 kb 命令不可用**
A: 请确保 Skill 目录已添加到系统 PATH，或使用完整路径运行。

### 使用问题

**Q: 生成的笔记内容是空的**
A: 生成的是标准化模板，需要手动填充内容。参考 [USE-CASES.md](USE-CASES.md) 中的示例。

**Q: 死链太多，修复不过来**
A: 使用 `--threshold` 参数只修复高频死链，例如 `kb fix-link --threshold 5`。

**Q: 大知识库运行慢**
A: 参考 [USE-CASES.md](USE-CASES.md) 中的性能优化建议，分批次处理。

更多问题请查看 [FAQ.md](FAQ.md)。

---

## 💬 社区支持

### GitHub Discussions

在 [GitHub Discussions](https://github.com/your-username/obsidian-knowledge-base-creator/discussions) 中提问和讨论：

- **💡 想法与建议**：分享你的想法和功能建议
- **🙋 提问与求助**：提出使用问题，寻求社区帮助
- **📖 展示与分享**：分享你创建的知识库和使用经验
- **🛠️ 开发讨论**：讨论开发相关的技术问题

### 搜索已有讨论

在创建新讨论之前，请先搜索是否已有类似的讨论：

1. 前往 GitHub Discussions
2. 使用搜索框搜索关键词
3. 查看是否已有解决方案

---

## 🐛 报告 Bug

如果你发现了 Bug，请通过 [GitHub Issues](https://github.com/your-username/obsidian-knowledge-base-creator/issues) 报告：

### 报告前检查

1. 搜索现有 Issue，确认不是重复报告
2. 确认使用的是最新版本
3. 查看 [FAQ.md](FAQ.md) 是否有解决方案

### 报告内容

请使用 Bug 报告模板，包含：
- 清晰的 Bug 描述
- 详细的复现步骤
- 预期行为和实际行为
- 环境信息（操作系统、Python 版本、工具版本）
- 错误日志和截图

---

## ✨ 功能请求

如果你有新功能的想法，请通过 [GitHub Issues](https://github.com/your-username/obsidian-knowledge-base-creator/issues) 提交功能请求：

### 请求内容

请使用功能请求模板，包含：
- 功能描述
- 解决的问题
- 提议的解决方案
- 替代方案
- 预期效果

---

## 🔒 安全问题

如果你发现了安全漏洞，请**不要**在公开的 Issue 中报告，而是参考 [SECURITY.md](SECURITY.md) 中的安全漏洞报告流程，私下报告。

---

## 📧 联系维护者

如果以上渠道都无法解决你的问题，可以通过以下方式联系维护者：

- **GitHub**：[@your-username](https://github.com/your-username)
- **邮件**：support@example.com（仅用于一般咨询，不用于 Bug 报告）

**注意**：
- 请优先使用 GitHub Issues 和 Discussions，这样其他用户也能从回答中受益
- 邮件响应时间可能较长，请耐心等待
- 不要在邮件中包含敏感信息（如密码、密钥等）

---

## 🤝 贡献代码

如果你想为项目贡献代码，请参考 [CONTRIBUTING.md](CONTRIBUTING.md) 中的贡献指南：

1. Fork 项目并创建分支
2. 安装开发依赖
3. 编写代码和测试
4. 运行质量检查
5. 提交 Pull Request

---

## ⭐ 支持项目

如果你觉得这个项目对你有帮助，可以通过以下方式支持：

1. **给项目点 Star** ⭐
2. **分享给更多人**
3. **贡献代码或文档**
4. **赞助项目**（参考 [.github/FUNDING.yml](.github/FUNDING.yml)）

---

## 📝 响应时间

| 渠道 | 预期响应时间 |
|------|-------------|
| GitHub Issues | 3-5 个工作日 |
| GitHub Discussions | 1-3 个工作日（社区响应可能更快） |
| 安全报告 | 24 小时内初步确认 |
| 邮件 | 5-7 个工作日 |

**注意**：响应时间仅供参考，实际可能因工作量和问题复杂度而有所不同。

---

## 🙏 致谢

感谢所有使用、反馈、贡献和支持这个项目的人！是你们让这个项目不断完善。

---

> **提示**：在寻求支持之前，请先查阅文档和搜索已有讨论，这样可以更快地解决问题，也能减少维护者的工作量。
