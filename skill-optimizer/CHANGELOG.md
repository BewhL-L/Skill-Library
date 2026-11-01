# 更新日志

## [1.9.0] - 2026-11-02

### ✨ 新功能

- **新增 `scripts/check-install-sync.py`**：检查同一个 Skill 在各 agent 安装位是否存在旧副本或错误链接。自动扫描 `~/.workbuddy/skills`、`~/.claude/skills`、`~/.codex/skills` 等已知根目录与 `~/<任意>/skills`，逐处给出 `LINKED` / `IN_SYNC` / `STALE` / `MISMATCH` / `ABSENT`，`STALE` 时列出差异文件。
  - 退出码语义化：`0` 正常、`1` 有 `STALE`/`MISMATCH`、`2` 路径无效，可直接接入 CI 或提交前钩子。
  - 只读诊断，不修改任何文件；`--json` 供流水线消费。

### 📄 文档

- SKILL.md 新增「5. 部署一致性检查」：状态表、修复建议，以及两个反直觉的坑——备份留在技能根目录会被当成第二个同名 Skill；安装位里的 `_user_meta.json` 改链接后会落进源码目录，需 `.gitignore`。
- CHECKLIST.md 新增 P1「部署一致性（4 项）」，检查项总数 101 → **105**。

### 🧭 背景

- 起因是 2026-11-02 的一次实战：Skill 源码改完、agent 加载的仍是旧副本，而**两边看起来都正常**——源码目录对、安装目录也在、文件都能读。根因是安装位为独立拷贝而非链接，审计维度里没有任何一项覆盖它。
- 同一批实战还沉淀了固化方案：Windows 用 junction（无需管理员权限），Linux/WSL 用 `ln -sfn`，并明确了备份位置与幂等语义（详见 `hermes-portability` 技能的 `scripts/link-skill.ps1`）。

---

## [1.8.1] - 2026-10-09

### 🏗️ 工程化

- **CHANGELOG 更新从"建议"升级为"强制约束"**：SKILL.md 三处修改——①每轮优化标准流程第5步标注【强制】并新增警告说明（未更新 CHANGELOG 的修改视为未完成，不得提交）；②优化检查清单文档部分从10项扩为11项，新增"【强制】本次修改已同步更新 CHANGELOG.md"检查项；③使用流程场景一第6步标注【强制】。修复了之前"流程里写了要更 CHANGELOG 但没有任何机制强制执行"的漏洞。

### 📄 文档

- SKILL.md 检查清单总数从 50 项更新为 51 项（文档部分 10→11）

---

## [1.8.0] - 2026-09-01

### ✨ 新功能
- **重构统一 CLI 入口 skill-opt.py**：修复致命导入 bug（之前根本无法运行），用 importlib.util 动态加载带连字符的模块
- **新增 type 命令**：Skill 类型检测，显示评估模式、维度权重、优化范围
- **新增 batch 命令**：批量优化目录下所有 Skill，生成批量对比报告（JSON）
- **新增 diff 命令**：优化前后对比报告，逐维度展示得分变化
- **类型感知改造 generate-tests.py**：纯文档型自动跳过测试生成，给出针对性建议
- **类型感知改造 generate-docs.py**：纯文档型自动跳过 API/架构文档，只生成适用的 FAQ 和使用示例

### 🔧 优化
- skill-opt.py 所有命令添加 try/except 错误处理，失败时打印 traceback
- skill-opt.py 采用懒加载模块，避免启动时加载所有模块
- cmd_all 一键全流程按类型自适应，纯文档型跳过测试生成步骤
- OPTIMIZATION-GUIDE.md 新增「按 Skill 类型适配」章节，纯文档型 15 轮专属优化路径

### 🐛 Bug 修复
- 修复 skill-opt.py 导入路径错误（`Path(__file__).parent / "scripts"` 多了一层目录）
- 修复 skill-opt.py 模块名错误（`audit_skill` 无法 import 连字符文件名 `audit-skill.py`）
- 修复 skill-opt.py 版本号停留在 v1.5.0 的问题
- 修复 SKILL.md 底部重复的 v1.0.0 旧版本信息

### 📄 文档
- SKILL.md 统一 CLI 入口部分新增 type/batch/diff 命令说明
- SKILL.md 版本记录新增 v1.7 和 v1.8
- OPTIMIZATION-GUIDE.md 新增纯文档型 Audit 4 个专属维度详解

---

## [1.7.0] - 2026-09-01

### ✨ 新功能
- **新增 Skill 类型自动检测**（skill_type_detector.py）：自动识别 code-driven / doc-only / hybrid 三种类型
- **audit 按类型动态调整维度和权重**：纯文档型跳过代码质量/测试覆盖/工程化配置/可维护性 4 个维度，新增 doc_structure/trigger_scenarios/output_spec/references_depth 4 个文档型专属维度
- **optimize 按类型过滤操作**：纯文档型自动跳过代码优化和高级工程化配置（pre-commit/pyproject/Makefile/CI-CD），只补全文档和基础配置（.gitignore/.editorconfig）

### 🔧 优化
- audit-skill.py 新增 4 个文档型专属检查方法
- audit-skill.py 权重计算改为动态获取，按类型适配
- audit-skill.py 建议生成按类型区分，纯文档型给出文档优化建议
- optimize-skill.py 新增 _optimize_basic_config 方法，纯文档型专用

### 📄 文档
- SKILL.md 核心能力新增「Skill 类型自动检测」章节
- SKILL.md audit 维度表格改为按类型区分（代码型权重 vs 文档型权重）

---

## [1.6.0] - 2026-09-01

### 🐛 Bug 修复
- **修复类型注解检测逻辑**：原 `content.find(f'def {func_name}')` 可能匹配到错误位置（函数名子串问题，如 `foo` 先匹配到 `foobar`），且只检查前 200 字符可能漏检长签名函数。改用 `re.finditer` 精确获取每个函数的位置和完整签名行，通过捕获组 `(\s*->\s*[^:]+)?` 直接判断返回类型注解。
- **修复 docstring 检测逻辑**：原检测从 `def` 关键字位置开始检查前 500 字符，可能把函数签名行后的注释误判为 docstring。改为从函数体开始位置（`match.end()`）检查，且要求去除前导空白后以 `"""` 或 `'''` 开头。

### ✨ 新功能
- **新增 Markdown 文档格式检查**（集成到文档完整性维度）：
  - 表格列数一致性检查：检测数据行列数与表头列数不匹配的问题，自动排除转义的 `\|` 和双链 `[[...]]` 内的 `|`
  - 双链格式有效性检查：检测双链目标为空的错误格式（左括号后直接跟管道符，无目标笔记名）
  - 表格双链管道符检查：检测表格中双链内未转义的 `|`（会导致列数错位），提示应转义为 `\|`
- **新增 py_compile 语法验证**（集成到代码质量维度）：对每个 Python 脚本执行 `py_compile.compile()` 实际编译验证，语法错误标记为 critical 级别，最多扣 30 分。

### 📝 文档
- SKILL.md 更新版本号至 v1.6.0，补充新增检查项说明
- audit-skill.py 版本号更新至 1.6.0，报告输出新增审计工具版本显示

### 🔧 优化
- 新增 `_clean_table_pipes()` 静态方法，统一处理表格行中管道符的清理逻辑（排除转义符和双链）
- 新增 `_check_markdown_format()` 方法，独立封装 Markdown 格式检查逻辑
- 优化建议文本更新，文档维度建议包含"修复Markdown表格列数和双链格式"，代码质量维度建议包含"确保py_compile语法验证通过"

---

## [1.5.0] - 2026-08-31

### ✨ 新功能
- 初始版本发布
- 基于 25 轮优化经验的完整方法论
- 4 个核心脚本（audit/optimize/docs/tests）
- 统一 CLI 入口（skill-opt.py）
- 25 轮优化完整指南
- 100+ 项检查清单
- 专业级质量标准

### 📚 文档
- README.md - 项目首页
- SKILL.md - 核心文档
- QUICKSTART.md - 快速上手
- OPTIMIZATION-GUIDE.md - 25 轮优化指南
- CHECKLIST.md - 检查清单
- QUALITY-STANDARDS.md - 质量标准
- FAQ.md - 常见问题
- CHANGELOG.md - 版本记录

### 🔧 工具
- audit-skill.py - 8 维度健康检查
- optimize-skill.py - 自动优化（文档/代码/配置）
- generate-docs.py - 文档生成（API/FAQ/示例/架构）
- generate-tests.py - 测试生成（单元/集成/覆盖率）
- skill-opt.py - 统一 CLI 入口

---

## 版本说明

本项目采用 [语义化版本](https://semver.org/lang/zh-CN/)：

- **主版本号**：不兼容的 API 变更
- **次版本号**：向下兼容的功能性新增
- **修订号**：向下兼容的问题修正
