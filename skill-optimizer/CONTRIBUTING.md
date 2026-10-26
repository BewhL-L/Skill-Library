# 贡献指南

> 感谢你对 skill-optimizer 的贡献！本文档说明如何参与开发。

---

## 目录

- [开发环境搭建](#开发环境搭建)
- [项目结构](#项目结构)
- [代码规范](#代码规范)
- [提交规范](#提交规范)
- [测试流程](#测试流程)
- [发布流程](#发布流程)

---

## 开发环境搭建

### 前置要求

- Python 3.8+
- Git

### 克隆项目

```bash
git clone <repo-url>
cd skill-optimizer
```

### 安装依赖

```bash
# 核心依赖（标准库即可运行，无需额外安装）
python --version  # 确认 Python 3.8+

# 可选：开发依赖
pip install pytest pytest-cov black isort flake8
```

### 验证安装

```bash
# 运行健康检查（自检）
python scripts/skill-opt.py audit --path .

# 显示帮助信息
python scripts/skill-opt.py info
```

---

## 项目结构

```
skill-optimizer/
├── SKILL.md                    # 核心文档（必须）
├── README.md                   # 项目首页
├── API.md                      # API 参考
├── ARCHITECTURE.md             # 架构文档
├── QUICKSTART.md               # 快速上手
├── INSTALLATION.md             # 安装指南
├── CONTRIBUTING.md             # 本文档
├── CHANGELOG.md                # 版本记录
├── FAQ.md                      # 常见问题
├── CHECKLIST.md                # 检查清单
├── QUALITY-STANDARDS.md       # 质量标准
├── OPTIMIZATION-GUIDE.md      # 25轮优化指南
├── .gitignore                  # Git 忽略
├── .editorconfig               # 编辑器配置
└── scripts/                    # 脚本目录
    ├── skill-opt.py            # 统一 CLI 入口
    ├── skill_type_detector.py  # 类型检测（核心依赖）
    ├── audit-skill.py          # 健康检查
    ├── optimize-skill.py       # 自动优化
    ├── generate-docs.py        # 文档生成
    └── generate-tests.py       # 测试生成
```

---

## 代码规范

### Python 规范

- 遵循 [PEP 8](https://peps.python.org/pep-0008/) 风格指南
- 缩进：4 个空格
- 行宽：最大 120 字符
- 命名：
  - 类名：`PascalCase`（如 `SkillAuditor`）
  - 函数/方法：`snake_case`（如 `_check_metadata`）
  - 常量：`UPPER_SNAKE_CASE`
- 所有公共函数必须有 docstring
- 所有函数参数和返回值必须有类型注解

### 类型注解示例

```python
def calculate_score(self, dimensions: Dict[str, float]) -> float:
    """
    计算加权总分

    Args:
        dimensions: 维度得分字典，key为维度名，value为得分(0-100)

    Returns:
        加权总分(0-100)
    """
    total = 0.0
    for dim, weight in self.weights.items():
        total += dimensions.get(dim, 0) * weight
    return round(total, 1)
```

### 错误处理

- 所有可能失败的操作必须有 try/except
- 捕获异常后必须打印有意义的错误信息
- CLI 命令失败时返回非零退出码
- 不要用裸 `except:`，必须指定异常类型

### Markdown 规范

- 标题层级：`#` → `##` → `###` → `####`
- 表格必须有表头和分隔行
- 代码块必须指定语言
- 链接使用相对路径

---

## 提交规范

遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范。

### 提交格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

### 类型（type）

| 类型 | 说明 |
|------|------|
| `feat` | 新功能 |
| `fix` | Bug 修复 |
| `docs` | 文档变更 |
| `style` | 代码格式（不影响功能） |
| `refactor` | 重构（既不修复bug也不添加功能） |
| `perf` | 性能优化 |
| `test` | 测试相关 |
| `chore` | 构建/工具/依赖变更 |

### 示例

```
feat(audit): 新增纯文档型4个专属维度

- 新增 _check_doc_structure() 检查 SKILL.md 结构完整性
- 新增 _check_trigger_scenarios() 检查触发场景覆盖度
- 新增 _check_output_spec() 检查输出规范明确性
- 新增 _check_references_depth() 检查 references 深度
- 权重计算改为动态获取，按类型适配

Closes #123
```

---

## 测试流程

### 运行自检

```bash
# 对自身运行健康检查
python scripts/skill-opt.py audit --path .

# 预期：总分 >= 60，无 critical 级别问题
```

### 功能测试

```bash
# 测试类型检测
python scripts/skill-opt.py type --path ./test-skill

# 测试健康检查
python scripts/skill-opt.py audit --path ./test-skill

# 测试自动优化（预览模式）
python scripts/skill-opt.py optimize --path ./test-skill --dry-run

# 测试批量优化
python scripts/skill-opt.py batch --path ./skills-dir --dry-run

# 测试对比报告
python scripts/skill-opt.py diff --before before.json --after after.json
```

### 多类型测试

必须对三种类型的 Skill 分别测试：

```bash
# 代码驱动型
python scripts/skill-opt.py audit --path ./code-driven-skill

# 纯文档型
python scripts/skill-opt.py audit --path ./doc-only-skill

# 混合型
python scripts/skill-opt.py audit --path ./hybrid-skill
```

---

## 发布流程

### 发布前检查

- [ ] 所有功能测试通过
- [ ] 三种类型 Skill 都验证通过
- [ ] 自身 audit 总分 >= 60
- [ ] CHANGELOG.md 已更新
- [ ] SKILL.md 版本号已更新
- [ ] 所有脚本版本号已更新
- [ ] 文档无死链

### 版本号规范

遵循 [语义化版本](https://semver.org/)：`MAJOR.MINOR.PATCH`

- `MAJOR`：不兼容的 API 变更
- `MINOR`：向下兼容的功能新增
- `PATCH`：向下兼容的 Bug 修复

### 发布步骤

1. 更新 CHANGELOG.md，添加新版本记录
2. 更新 SKILL.md 版本号
3. 更新所有脚本头部的版本号
4. 运行完整测试
5. 提交代码：`git commit -m "chore: release vX.Y.Z"`
6. 打标签：`git tag vX.Y.Z`
7. 推送：`git push && git push --tags`

---

## 获得帮助

- 阅读 [FAQ.md](FAQ.md) 查看常见问题
- 阅读 [ARCHITECTURE.md](ARCHITECTURE.md) 了解架构设计
- 阅读 [API.md](API.md) 查看 API 参考
- 提交 Issue 报告 Bug 或提出功能建议

---

> **版本**：v1.8.0
>
> **最后更新**：2026-09-01
