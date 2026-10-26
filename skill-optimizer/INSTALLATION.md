# 安装指南

> skill-optimizer 的安装、配置和卸载说明。

---

## 目录

- [系统要求](#系统要求)
- [安装方式](#安装方式)
- [配置说明](#配置说明)
- [验证安装](#验证安装)
- [卸载](#卸载)
- [常见问题](#常见问题)

---

## 系统要求

| 要求 | 最低版本 | 推荐版本 |
|------|---------|---------|
| Python | 3.8 | 3.10+ |
| 操作系统 | Windows 10 / macOS 10.15 / Ubuntu 18.04 | 最新稳定版 |
| 磁盘空间 | 10 MB | 50 MB（含文档和模板） |

### Python 标准库依赖

skill-optimizer 仅使用 Python 标准库，无需安装额外依赖：

- `os`、`sys`、`re`、`json`、`ast`、`argparse`
- `pathlib`、`datetime`、`typing`、`importlib`
- `py_compile`（语法验证）
- `tempfile`（临时文件）

---

## 安装方式

### 方式一：安装到豆包 Skill 目录（推荐）

将 skill-optimizer 文件夹复制到豆包的用户 Skill 目录：

**Windows**：
```
C:\Users\<用户名>\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\.user_skills\
```

**macOS**：
```
~/Library/Application Support/Doubao/User Data/Default/.doubao/agent_mode/workspace/.user_skills/
```

**Linux**：
```
~/.config/Doubao/User Data/Default/.doubao/agent_mode/workspace/.user_skills/
```

安装后目录结构：
```
.user_skills/
└── skill-optimizer/
    ├── SKILL.md
    ├── scripts/
    │   ├── skill-opt.py
    │   ├── skill_type_detector.py
    │   ├── audit-skill.py
    │   ├── optimize-skill.py
    │   ├── generate-docs.py
    │   └── generate-tests.py
    └── ...（其他文档）
```

### 方式二：本地开发安装

```bash
# 克隆或下载项目
git clone <repo-url>
cd skill-optimizer

# 验证可运行
python scripts/skill-opt.py info
```

### 方式三：作为依赖使用

将 `scripts/` 目录添加到 Python 路径：

```python
import sys
sys.path.insert(0, "/path/to/skill-optimizer/scripts")

from skill_type_detector import SkillTypeDetector
from audit_skill import SkillAuditor  # 注意：需要用 importlib 动态加载

# 或直接用 CLI
import subprocess
subprocess.run(["python", "/path/to/skill-optimizer/scripts/skill-opt.py", "audit", "--path", "./my-skill"])
```

---

## 配置说明

skill-optimizer 无需额外配置即可使用。以下是可选的环境变量：

| 环境变量 | 说明 | 默认值 |
|---------|------|--------|
| `SKILL_OPTIMIZER_DEBUG` | 调试模式，打印详细错误信息 | `false` |
| `SKILL_OPTIMIZER_CONFIG` | 自定义配置文件路径 | 无 |

### 配置文件（可选）

可以创建 `skill-optimizer.config.json` 自定义默认行为：

```json
{
  "default_audit_format": "text",
  "default_dry_run": false,
  "score_thresholds": {
    "S": 95,
    "A": 85,
    "B": 70,
    "C": 50
  },
  "doc_only_skip_tests": true,
  "doc_only_skip_api_docs": true
}
```

---

## 验证安装

### 快速验证

```bash
# 显示版本和帮助信息
python scripts/skill-opt.py info

# 预期输出：
# ============================================================
# 🛠️  Skill 工程化优化器 v1.8.0
# ============================================================
# ...（可用命令列表）
```

### 功能验证

```bash
# 1. 类型检测
python scripts/skill-opt.py type --path .

# 2. 健康检查（自检）
python scripts/skill-opt.py audit --path .

# 3. 自动优化（预览模式，不修改文件）
python scripts/skill-opt.py optimize --path . --dry-run

# 4. 所有命令帮助
python scripts/skill-opt.py --help
```

### 预期结果

- `info`：显示 v1.8.0 和 9 个可用命令
- `type`：检测为 code-driven（skill-optimizer 自身是代码驱动型）
- `audit`：总分 >= 50，无 critical 级别错误
- `optimize --dry-run`：显示将执行的操作，不实际修改文件

---

## 卸载

### 方式一：从豆包 Skill 目录卸载

直接删除 skill-optimizer 文件夹：

**Windows**：
```powershell
Remove-Item -Recurse -Force "C:\Users\<用户名>\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\.user_skills\skill-optimizer"
```

**macOS/Linux**：
```bash
rm -rf ~/.config/Doubao/.../.user_skills/skill-optimizer
```

### 方式二：本地开发卸载

直接删除项目目录即可，skill-optimizer 不会在系统其他位置写入文件。

### 卸载后清理

skill-optimizer 运行时可能生成以下临时文件，可手动删除：

- `audit-report.json` — 健康检查报告
- `batch-report.json` — 批量优化报告
- `diff-report.json` — 对比报告
- `__pycache__/` — Python 缓存目录
- `*.pyc` — 编译的 Python 文件

---

## 常见问题

### Q: 运行时提示 `ModuleNotFoundError: No module named 'skill_type_detector'`

**A**：确保从 scripts/ 目录的父目录运行，或使用完整路径：

```bash
# 正确：从项目根目录运行
python scripts/skill-opt.py audit --path ./my-skill

# 错误：从 scripts/ 目录运行
cd scripts
python skill-opt.py audit --path ../my-skill  # 可能找不到模块
```

### Q: 中文显示乱码

**A**：Windows 下设置控制台编码：

```powershell
chcp 65001  # 切换到 UTF-8
```

或设置环境变量：
```powershell
$env:PYTHONIOENCODING = "utf-8"
```

### Q: audit 报告中纯文档型的代码维度显示 0 分

**A**：这是正常行为。v1.7+ 版本会自动检测 Skill 类型，纯文档型会跳过代码/测试/工程化维度，不参与计分。使用 `type` 命令确认检测结果：

```bash
python scripts/skill-opt.py type --path ./my-skill
```

### Q: 如何强制按代码驱动型评估？

**A**：当前版本自动检测类型，暂不支持手动指定。如果检测结果不准确，请检查：
- 是否有 scripts/ 目录
- 是否有 .py 文件
- 是否有 tests/ 目录

### Q: 批量优化时某些 Skill 失败怎么办？

**A**：batch 命令会跳过失败的 Skill 并继续处理其他 Skill。失败的 Skill 会在报告中标记。可以单独对失败的 Skill 运行 audit 查看具体错误：

```bash
python scripts/skill-opt.py audit --path ./failed-skill
```

---

> **版本**：v1.8.0
>
> **最后更新**：2026-09-01
