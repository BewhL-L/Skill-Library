# 贡献指南

感谢你对 Obsidian 知识库标准化生成器的关注！欢迎提交 Issue 和 Pull Request。

---

## 📋 目录

- [行为准则](#行为准则)
- [如何贡献](#如何贡献)
- [开发环境搭建](#开发环境搭建)
- [代码规范](#代码规范)
- [提交规范](#提交规范)
- [Pull Request 流程](#pull-request-流程)
- [报告 Issue](#报告-issue)

---

## 行为准则

本项目采用 [Contributor Covenant](https://www.contributor-covenant.org/) 行为准则。参与本项目即表示你同意遵守其条款。

---

## 如何贡献

你可以通过以下方式贡献：

1. **报告 Bug**：发现问题请提交 Issue
2. **提出新功能**：有好的想法请提交 Issue 讨论
3. **提交代码**：修复 Bug 或实现新功能
4. **完善文档**：改进 README、SKILL.md、FAQ 等文档
5. **分享示例**：分享使用本工具创建的知识库示例

---

## 开发环境搭建

### 1. 克隆仓库

```bash
git clone https://github.com/your-username/obsidian-knowledge-base-creator.git
cd obsidian-knowledge-base-creator
```

### 2. 安装 Python

需要 Python 3.8+，下载地址：https://www.python.org/downloads/

### 3. 安装开发依赖

```bash
pip install -r requirements-dev.txt
```

开发依赖包含：pytest、coverage、flake8、black、isort、mypy、pre-commit、bandit、safety 等。

### 4. 安装 pre-commit 钩子

```bash
pre-commit install
```

pre-commit 会在每次提交前自动运行代码质量检查、格式检查等，确保提交的代码符合规范。

### 5. 验证安装

```bash
python --version
python scripts/kb.py info
make help    # 查看 Makefile 可用命令
```

### 6. 使用 Makefile 简化开发流程

项目提供 Makefile 统一常用命令：

```bash
make help           # 显示所有命令帮助
make install        # 安装运行时依赖
make install-dev    # 安装开发依赖
make test           # 运行所有测试（单元+集成）
make test-unit      # 只运行单元测试
make test-integration  # 只运行集成测试
make lint           # 代码质量检查
make format-check   # 检查代码格式
make format         # 自动格式化代码
make type-check     # 类型检查
make coverage       # 生成代码覆盖率报告
make check          # 完整质量检查（lint + test + type-check）
make clean          # 清理临时文件
make info           # 显示项目信息
```

### 7. 运行测试

```bash
# 集成测试（测试12个命令的端到端功能）
python test-all.py

# 单元测试（测试核心函数逻辑，36个用例）
python unit-test.py

# 使用 Makefile
make test
```

### 8. 代码质量检查

```bash
# 项目专属 lint 工具
python lint.py --path scripts

# 使用 Makefile
make lint

# 完整质量检查（lint + test + type-check）
make check
```

### 9. 代码覆盖率检查

```bash
# 生成覆盖率报告
coverage run unit-test.py
coverage report          # 文本报告
coverage html            # HTML 报告（在 coverage_html_report/ 目录）
coverage xml             # XML 报告（用于 CI/CD）

# 使用 Makefile
make coverage
```

---

## 代码规范

### Python 代码规范

- 遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 风格指南
- 使用 4 空格缩进
- 行宽不超过 120 字符
- 使用有意义的变量名和函数名
- 添加必要的注释和文档字符串

### 示例

```python
def generate_note(title, category, difficulty=3):
    """生成标准化笔记

    Args:
        title: 笔记标题
        category: 所属分类
        difficulty: 难度等级 (1-5)

    Returns:
        生成的笔记内容字符串
    """
    # 实现逻辑
    pass
```

### Markdown 文档规范

- 使用标准 Markdown 语法
- 标题层级清晰（# → ## → ###）
- 代码块标注语言类型
- 表格格式规范
- 中文与英文/数字之间加空格

### Shell 脚本规范

- 使用 `#!/bin/bash` 或 `#!/bin/sh` 开头
- 添加必要的注释
- 使用 `set -e` 确保出错时退出
- 跨平台兼容（Windows/macOS/Linux）

---

## 提交规范

### 提交信息格式

遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type 类型

| 类型 | 说明 |
|------|------|
| `feat` | 新功能 |
| `fix` | 修复 Bug |
| `docs` | 文档更新 |
| `style` | 代码格式（不影响功能） |
| `refactor` | 重构（既不是新功能也不是修复 Bug） |
| `perf` | 性能优化 |
| `test` | 添加测试 |
| `chore` | 构建过程或辅助工具的变动 |
| `ci` | CI/CD 相关 |

### 示例

```
feat(init): 支持自定义分类目录结构

- 新增 --categories 参数，允许用户自定义分类
- 更新 init-kb.py 支持动态目录生成
- 更新文档说明自定义分类的用法

Closes #123
```

```
fix(audit): 修复 MOC 检测只在根目录查找的问题

- 修改 check_moc_coverage 函数，使用 os.walk 递归查找
- 添加测试用例验证修复
- 更新 CHANGELOG

Closes #456
```

---

## Pull Request 流程

### 1. Fork 并创建分支

```bash
# Fork 仓库后克隆
git clone https://github.com/your-username/obsidian-knowledge-base-creator.git
cd obsidian-knowledge-base-creator

# 创建功能分支
git checkout -b feature/your-feature-name
```

### 2. 提交更改

```bash
git add .
git commit -m "feat: 描述你的更改"
```

### 3. 推送并创建 PR

```bash
git push origin feature/your-feature-name
```

然后在 GitHub 上创建 Pull Request。

### 4. PR 检查清单

提交 PR 前请确认：

- [ ] 代码遵循项目的代码规范（PEP 8，行宽 120）
- [ ] 所有函数都添加了类型注解
- [ ] 已添加必要的注释和文档字符串
- [ ] 已运行 `make lint`，代码质量检查通过（0 错误 0 警告）
- [ ] 已运行 `make type-check`，类型检查通过
- [ ] 已运行 `make test`，所有测试通过（单元测试 36/36 + 集成测试 12/12）
- [ ] 新增功能已添加对应的单元测试
- [ ] 修复 Bug 已添加回归测试
- [ ] 已运行 `pre-commit run --all-files`，所有钩子通过
- [ ] 已更新 CHANGELOG.md（如有必要）
- [ ] 已更新相关文档（如有必要）
- [ ] 提交信息遵循 Conventional Commits 规范
- [ ] PR 描述清晰，说明更改的目的和内容
- [ ] CI/CD 所有检查通过（7 个 Job）

---

## 报告 Issue

### Bug 报告

报告 Bug 时请包含以下信息：

1. **描述**：清晰简洁地描述 Bug
2. **复现步骤**：
   ```
   1. 运行命令 '...'
   2. 看到错误 '...'
   ```
3. **预期行为**：描述你期望发生什么
4. **实际行为**：描述实际发生了什么
5. **环境信息**：
   - 操作系统：Windows 11 / macOS 14 / Ubuntu 22.04
   - Python 版本：3.x.x
   - 工具版本：v2.x
6. **截图/日志**：如有，请附上截图或错误日志

### 功能请求

提出新功能时请包含以下信息：

1. **描述**：清晰简洁地描述你想要的功能
2. **动机**：为什么需要这个功能？解决什么问题？
3. **方案**：你有什么实现思路？
4. **替代方案**：有没有考虑过其他方案？
5. **附加信息**：任何其他相关信息

---

## 📞 联系方式

- 提交 Issue：[GitHub Issues](https://github.com/your-username/obsidian-knowledge-base-creator/issues)
- 讨论：[GitHub Discussions](https://github.com/your-username/obsidian-knowledge-base-creator/discussions)

---

## 🙏 致谢

感谢所有为本项目做出贡献的人！

---

> 💡 **提示**：如果你是第一次贡献开源项目，可以阅读 [First Contributions](https://github.com/firstcontributions/first-contributions) 了解基本流程。
