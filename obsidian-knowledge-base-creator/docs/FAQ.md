# ❓ 常见问题解答（FAQ）

> 使用过程中遇到的常见问题及解决方案

---

## 📋 目录

1. [安装与环境](#安装与环境)
2. [初始化与建库](#初始化与建库)
3. [笔记生成](#笔记生成)
4. [标准化与维护](#标准化与维护)
5. [错误排查](#错误排查)
6. [进阶使用](#进阶使用)

---

## 安装与环境

### Q1: 提示 "python 不是内部或外部命令" 怎么办？

**A**: Python 未安装或未添加到系统 PATH。

**解决方案**：
1. 下载并安装 Python 3.8+（https://www.python.org/downloads/）
2. 安装时勾选 "Add Python to PATH"
3. 重启终端，运行 `python --version` 验证

### Q2: 可以在 macOS / Linux 上使用吗？

**A**: 可以。所有脚本都是跨平台的 Python 脚本。

**使用方式**：
```bash
# macOS / Linux 使用 python scripts/kb.py 代替 kb.bat
python scripts/kb.py init --name "我的知识库" --path ./my-kb
```

### Q3: 需要安装额外的 Python 库吗？

**A**: 不需要。所有脚本只使用 Python 标准库，无需安装第三方依赖。

---

## 初始化与建库

### Q4: init 命令会覆盖已有的文件吗？

**A**: 不会。init 命令只会创建不存在的目录和文件，如果文件已存在会跳过。

**建议**：在空目录中初始化新知识库，避免与现有文件混淆。

### Q5: 可以自定义分类目录吗？

**A**: 目前版本使用固定的 12 个分类。如果需要自定义，可以：
1. 初始化后手动重命名或删除不需要的目录
2. 修改 `assets/config-template.yaml` 中的分类配置
3. 手动创建新的分类目录和 MOC

### Q6: 初始化后如何在 Obsidian 中打开？

**A**: 
1. 打开 Obsidian
2. 点击 "打开文件夹作为库"
3. 选择初始化的知识库目录
4. 建议将 `00-综合导航/Home.md` 设为启动页

---

## 笔记生成

### Q7: note 命令生成的笔记内容是空的吗？

**A**: 不是完全空的。生成的笔记包含：
- 完整的五段式结构（概述/原理/实操/问题/拓展）
- 标准的表格模板
- 代码块占位符
- 完整的 Frontmatter

你需要填充 `{{占位符}}` 中的具体内容。

### Q8: 可以一次生成多篇笔记吗？

**A**: 可以。使用 `batch-note` 命令：

```bash
# 准备 notes.json 文件
kb.bat batch-note --list notes.json --kb-root ./my-kb
```

详见 `QUICKSTART.md` 中的完整示例。

### Q9: 生成笔记时提示 "文件已存在" 怎么办？

**A**: 脚本会询问是否覆盖。如果选择不覆盖，会跳过该笔记。

**建议**：
- 使用 `--dry-run` 先预览
- 确认标题不重复后再执行
- 如需覆盖，先备份原文件

### Q10: 生成的笔记分类不对怎么办？

**A**: 检查 `--category` 参数是否正确。支持的分类有：
- 综合导航、前端开发、后端开发、数据库与缓存
- 分布式与中间件、云原生与运维、计算机基础
- 通用工具、Python全栈、AI与效率工具、项目实战

如果分类不存在，脚本会自动使用"通用工具"分类。

---

## 标准化与维护

### Q11: standardize 命令会修改我的笔记内容吗？

**A**: 不会修改正文内容。standardize 只会：
1. 补全 Frontmatter 缺失字段（不修改已有字段）
2. 修复高频死链（创建新笔记，不修改现有笔记）
3. 更新 MOC 索引（重新生成 MOC 文件）
4. 输出健康检查报告

**建议**：首次运行前备份知识库，或使用 `--skip-*` 参数跳过特定步骤。

### Q12: fix-tags 会删除我的标签吗？

**A**: 不会删除，只会合并和统一。例如：
- `vue`、`Vue`、`vue.js` 会统一为 `Vue3`
- 重复的标签会自动去重

**建议**：先使用 `--dry-run` 预览修改，确认无误后再执行。

### Q13: fix-link 会创建很多空笔记吗？

**A**: 只会创建被引用 ≥3 次的高频死链对应的笔记。可以通过 `--threshold` 参数调整阈值。

```bash
# 只创建被引用 ≥5 次的死链
kb.bat fix-link --kb-root ./my-kb --threshold 5
```

创建的笔记状态为"📝 草稿"，需要后续填充内容。

### Q14: 多久运行一次 standardize 比较合适？

**A**: 建议：
- 新建知识库后：立即运行一次
- 批量添加笔记后：运行一次
- 日常维护：每周或每月运行一次
- 重大调整后：运行一次

---

## 错误排查

### Q15: 提示 "No module named 'yaml'" 怎么办？

**A**: 本工具不依赖 PyYAML。如果遇到这个错误，可能是运行了其他脚本。

本工具的 YAML 解析使用内置的简单解析器，无需安装第三方库。

### Q16: 中文显示乱码怎么办？

**A**: Windows 系统可能遇到编码问题。

**解决方案**：
1. 使用 `kb.bat` 而不是直接运行 Python 脚本（kb.bat 已设置 UTF-8 编码）
2. 确保终端使用 UTF-8 编码：`chcp 65001`
3. 使用 Windows Terminal 或 PowerShell 7+

### Q17: 提示 "权限被拒绝" 怎么办？

**A**: 可能是目标目录没有写入权限。

**解决方案**：
1. 确保目标目录不在系统保护目录（如 `C:\Program Files`）
2. 以管理员身份运行终端
3. 检查目录是否被其他程序占用（如 Obsidian 正在编辑）

### Q18: 脚本运行一半卡住了怎么办？

**A**: 可能是处理大量文件时需要时间，或遇到了异常。

**解决方案**：
1. 耐心等待（大知识库可能需要几分钟）
2. 按 `Ctrl+C` 中断，检查输出日志
3. 使用 `--dry-run` 预览，确认没有问题后再执行
4. 分批处理（先处理一个分类）

---

## 进阶使用

### Q19: 如何将 kb 命令添加到系统 PATH？

**A**: Windows 系统：
1. 将 Skill 目录路径添加到系统环境变量 PATH
2. 重启终端
3. 在任意目录使用 `kb.bat` 命令

macOS / Linux：
```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
export PATH="$PATH:/path/to/obsidian-knowledge-base-creator"
alias kb="python scripts/kb.py"
```

### Q20: 可以同时管理多个知识库吗？

**A**: 可以。每个知识库使用独立的目录，通过 `--kb-root` 或 `--path` 参数指定。

```bash
# 管理前端知识库
kb.bat progress --kb-root ./frontend-kb

# 管理 AI 知识库
kb.bat progress --kb-root ./ai-kb
```

### Q21: 如何备份知识库？

**A**: 直接复制整个知识库目录即可。建议：
1. 定期备份到云盘或 Git 仓库
2. 运行 `standardize` 后备份（此时知识库最规范）
3. 使用 Git 版本管理：`git init && git add . && git commit -m "init"`

### Q22: 可以从其他笔记工具导入吗？

**A**: 当前版本不支持直接导入。可以：
1. 将其他工具的笔记导出为 Markdown
2. 放入对应的分类目录
3. 运行 `standardize` 自动补全 Frontmatter 和 MOC

### Q23: 如何运行自动化测试？

**A**: 项目提供完整的测试体系，可以运行以下命令：

```bash
# 集成测试（测试12个命令的端到端功能）
python test-all.py

# 单元测试（测试核心函数逻辑，36个用例）
python unit-test.py

# 使用 Makefile
make test          # 运行所有测试
make test-unit     # 只运行单元测试
make test-integration  # 只运行集成测试
```

**测试结果**：48/48 全部通过，100% 通过率。

### Q24: 如何使用 Makefile？

**A**: 项目提供 Makefile 简化常用操作，运行 `make help` 查看所有命令：

```bash
make help           # 显示帮助信息
make install        # 安装运行时依赖
make install-dev    # 安装开发依赖
make test           # 运行所有测试
make lint           # 代码质量检查
make format-check   # 检查代码格式
make format         # 自动格式化代码
make type-check     # 类型检查
make coverage       # 生成代码覆盖率报告
make check          # 完整质量检查（lint + test + type-check）
make clean          # 清理临时文件
make info           # 显示项目信息
```

### Q25: 如何进行代码质量检查？

**A**: 项目提供多种代码质量检查方式：

```bash
# 项目专属 lint 工具
python lint.py --path scripts

# 使用 Makefile
make lint

# 完整质量检查（lint + test + type-check）
make check
```

**质量指标**：
- 代码质量：0 错误，0 警告
- 类型注解覆盖率：100%（63/63 函数）
- 测试通过率：100%（48/48）

### Q26: 项目的 CI/CD 是如何配置的？

**A**: 项目使用 GitHub Actions 进行 CI/CD 自动化，包含 7 个 Job：

1. **lint**：代码质量检查
2. **type-check**：类型检查
3. **test**：单元测试和集成测试
4. **cross-platform**：跨平台测试（Ubuntu/Windows/macOS）
5. **markdown-lint**：Markdown 规范检查
6. **shell-check**：Shell 脚本检查
7. **security**：安全扫描（bandit + safety）

支持 Python 3.8-3.12 多版本测试。

### Q27: 如何贡献代码？

**A**: 欢迎贡献代码！详细流程请查看 `CONTRIBUTING.md`：

1. Fork 项目并创建分支
2. 安装开发依赖：`pip install -r requirements-dev.txt`
3. 安装 pre-commit 钩子：`pre-commit install`
4. 编写代码和测试
5. 运行质量检查：`make check`
6. 提交 Pull Request

### Q28: 项目的代码覆盖率是多少？

**A**: 项目配置了完整的代码覆盖率体系，可以生成覆盖率报告：

```bash
# 生成覆盖率报告
coverage run unit-test.py
coverage report          # 文本报告
coverage html            # HTML 报告（在 coverage_html_report/ 目录）
coverage xml             # XML 报告（用于 CI/CD）

# 使用 Makefile
make coverage
```

覆盖率配置文件为 `.coveragerc`，支持分支覆盖率测量。

---

## 📞 还有其他问题？

如果以上 FAQ 没有解决你的问题：
1. 运行 `kb.bat info` 查看命令帮助
2. 阅读 `SKILL.md` 了解完整功能
3. 阅读 `QUICKSTART.md` 快速上手
4. 检查 `CHANGELOG.md` 了解版本变更
