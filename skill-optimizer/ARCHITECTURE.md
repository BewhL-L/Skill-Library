# 架构文档

> skill-optimizer 的模块架构、数据流和设计决策。

---

## 整体架构

```
┌─────────────────────────────────────────────────────────┐
│                    skill-opt.py (CLI 入口)                │
│  type │ audit │ optimize │ docs │ tests │ all │ batch │ diff │
└──────────────┬──────────────────────────────────────────┘
               │ 调用
┌──────────────▼──────────────────────────────────────────┐
│                    核心业务层                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ SkillAuditor │  │SkillOptimizer│  │ DocGenerator │ │
│  │ (audit)      │  │ (optimize)   │  │ (docs)       │ │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘ │
│         │                  │                  │          │
│  ┌──────▼───────┐  ┌──────▼───────┐         │          │
│  │TestGenerator │  │  类型检测层    │◄────────┘          │
│  │ (tests)      │  │              │                    │
│  └──────────────┘  └──────┬───────┘                    │
└─────────────────────────────┼────────────────────────────┘
                              │
                    ┌─────────▼─────────┐
                    │ skill_type_detector │
                    │  (类型自动检测)      │
                    └───────────────────┘
```

---

## 模块职责

### 1. skill_type_detector.py — 类型检测层

**职责**：自动检测 Skill 类型，为其他模块提供类型信息。

**核心逻辑**：
- 扫描 15 项指标（scripts/目录、Python文件数、tests/、references/、Markdown文件数等）
- 计算代码型得分（0-100）和文档型得分（0-100）
- 根据得分判定类型：code-driven / doc-only / hybrid
- 提供按类型适配的 audit 权重和 optimize 范围

**被依赖**：audit-skill.py、optimize-skill.py、generate-docs.py、generate-tests.py

### 2. audit-skill.py — 健康检查层

**职责**：按类型自适应评估 Skill 健康状况。

**核心逻辑**：
- 初始化时自动检测 Skill 类型
- 按类型决定检查哪些维度（代码型8维度 / 文档型8维度 / 混合型11维度）
- 纯文档型新增 4 个专属维度：doc_structure / trigger_scenarios / output_spec / references_depth
- 使用动态权重计算总分
- 按类型生成针对性优化建议

**依赖**：skill_type_detector.py

### 3. optimize-skill.py — 自动优化层

**职责**：按类型自适应执行优化操作。

**核心逻辑**：
- 初始化时自动检测 Skill 类型
- 纯文档型只执行 docs + basic_config（.gitignore/.editorconfig）
- 代码型/混合型执行 docs + code + config（完整工程化配置）
- 支持 dry-run 预览模式

**依赖**：skill_type_detector.py

### 4. generate-docs.py — 文档生成层

**职责**：自动生成 API/FAQ/示例/架构文档。

**核心逻辑**：
- 初始化时自动检测 Skill 类型
- 纯文档型跳过 API 和架构文档（无代码可解析）
- 用 AST 解析 Python 函数签名和 docstring

**依赖**：skill_type_detector.py

### 5. generate-tests.py — 测试生成层

**职责**：自动生成单元测试和集成测试。

**核心逻辑**：
- 初始化时自动检测 Skill 类型
- 纯文档型自动跳过（无代码可测试）
- 用 AST 解析函数，生成测试模板

**依赖**：skill_type_detector.py

### 6. skill-opt.py — CLI 入口层

**职责**：统一命令行入口，编排所有子命令。

**核心逻辑**：
- 用 importlib.util 动态加载带连字符的模块（audit-skill.py 等）
- 懒加载模块，提升启动速度
- 9 个子命令：type / audit / optimize / docs / tests / all / batch / diff / info
- batch 命令：批量优化目录下所有 Skill，生成对比报告
- diff 命令：优化前后对比，逐维度展示得分变化
- 所有命令都有 try/except 错误处理

**依赖**：所有其他脚本

---

## 数据流

### 单次 audit 流程

```
用户输入 --path
    │
    ▼
SkillAuditor.__init__()
    │ 调用 SkillTypeDetector.detect()
    ▼
获取 skill_type（code-driven/doc-only/hybrid）
    │
    ▼
SkillAuditor.audit()
    │ 按类型决定检查维度
    ▼
执行各维度检查方法
    │
    ▼
SkillAuditor._calculate_score()
    │ 调用 SkillTypeDetector.get_audit_weights()
    ▼
使用动态权重计算总分
    │
    ▼
SkillAuditor._generate_suggestions()
    │ 按类型生成针对性建议
    ▼
输出报告（print_report / save_report）
```

### batch 批量优化流程

```
用户输入 --path（包含多个Skill的目录）
    │
    ▼
扫描所有包含 SKILL.md 的子目录
    │
    ▼
对每个 Skill：
    ├── 优化前 audit（保存得分）
    ├── optimize（dry-run或实际执行）
    └── 优化后 audit（保存得分）
    │
    ▼
生成批量对比报告（表格 + JSON）
    │
    ├── 每个 Skill 的优化前后得分
    ├── 平均提升分数
    └── 总提升分数
```

---

## 设计决策

### 1. 为什么用 importlib.util 动态加载模块？

**问题**：脚本文件名带连字符（audit-skill.py），Python `import` 语句不支持连字符。

**方案**：用 `importlib.util.spec_from_file_location()` 动态加载，模块名用下划线（audit_skill）。

**替代方案**：重命名文件为下划线（audit_skill.py），但会破坏已有用户的调用习惯。

### 2. 为什么类型检测放在独立模块？

**原因**：
- 5 个脚本都需要类型信息（audit/optimize/docs/tests/skill-opt）
- 独立模块避免重复代码
- 类型检测逻辑变化时只需修改一处
- 可以独立测试和验证

### 3. 为什么纯文档型不直接给代码维度 0 分，而是跳过？

**原因**：
- 给 0 分会不合理地拉低总分（代码维度权重 20%+15%+10%+5% = 50%）
- 跳过不参与计分，用文档型专属维度替代，总分更合理
- 实际效果：纯文档型从 55.6 分（C级）提升到 78.5+ 分（B级）

### 4. 为什么 batch 命令要运行两次 audit？

**原因**：
- 第一次 audit 获取优化前得分
- 第二次 audit 获取优化后得分
- 两次对比才能计算实际提升分数
- dry-run 模式下两次得分相同（+0.0），但更改数显示将执行的操作

---

## 扩展点

### 新增 Skill 类型

1. 在 `skill_type_detector.py` 的 `_determine_type()` 中添加新类型判定逻辑
2. 在 `get_audit_weights()` 中添加新类型的权重
3. 在 `get_optimize_scopes()` 中添加新类型的优化范围
4. 在 `audit-skill.py` 的 `audit()` 中添加新类型的维度检查
5. 在 `optimize-skill.py` 的 `optimize()` 中添加新类型的优化操作

### 新增 audit 维度

1. 在 `audit-skill.py` 中添加 `_check_<dim_name>()` 方法
2. 在 `audit()` 中按类型决定是否调用该方法
3. 在 `skill_type_detector.py` 的 `get_audit_weights()` 中添加权重
4. 在 `_generate_suggestions()` 中添加该维度的建议指南

---

> **版本**：v1.8.0
>
> **最后更新**：2026-09-01
