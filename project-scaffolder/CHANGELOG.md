# Changelog

## v2.2.3 — 2026-10-27

### 新增
- `references/ci-snippets.md`：CI 片段库（Python / Node / 镜像构建 / 私有文件守卫 + 六个常见坑 + 三次反向验证）。原则是"给片段不给整文件"，避免覆盖用户既有 workflow。

### 变更
- **文档断言的脚本来源改为显式优先级**：已装 `project-processization` 则复制其 `scripts/check_docs.py`（同源不改逻辑）；未装则按 `references/engineering-baseline.md` 3.4 节自实现最小版。明确禁止两处各维护一份。
- 配套脚本章节补充**栈适用范围**：`schema/ci/docs/private` 通用，`index/defaults/deadconfig` 仅 Python；**"跳过"不等于"通过"**。
- `check_baseline.py` 的 docstring 与 `--help` 同步适用范围说明。
- README 参考表补 `ci-snippets.md` 与 `engineering-baseline.md` 两行。

## v2.2.2 — 2026-10-27

### 新增
- `tests/`（conftest + 8 例）：覆盖 schema / index / private / deadconfig 判定与退出码，脚本从此有回归保护。

### 变更
- 第六步自检新增「工程维度」分组：12 项从两组变三组（基础 1-5 / 深度 6-11 / 工程 12）。
- 全仓口径同步 11 → 12 维：README、API、ARCHITECTURE、TESTING、USE-CASES。
- SKILL.md frontmatter 补 `title` 字段，消除 `validate_md.py` 的 low 级提示。

### 修复
- `check_baseline.py` 在非 SQLAlchemy 项目上会静默返回空结果（看起来是 OK），改为输出"跳过：未发现模型目录"的信息项，避免误读为全绿。

## v2.2.1 — 2026-10-27

### 新增
- `scripts/check_baseline.py`：把第 12 维自检脚本化，覆盖 7 项——schema / index / ci / docs / private / defaults / deadconfig，error 非零退出，支持 `--strict` / `--json` / `--skip`。
- SKILL.md 新增「配套脚本」章节与 CLI 说明；增量迭代自检清单从 3 项扩到 4 项。

### 变更
- README 的"11 维度"统一为"12 维度（含工程底座）"。
- API.md 从"纯文档型 Skill"更正为"文档为主 + 一个自检脚本"，并补充 CLI 约定。

## v2.2.0 — 2026-10-27

### 新增
- `references/engineering-baseline.md`：工程底座六件套（版本化 schema / 索引 / 质量门 / 文档断言 / 私有边界 / 默认安全）+ 五种"假完备"反模式。
- 第三步新增 5 条生成约束：工程底座、文档断言、私有/公开边界、禁止假完备、测试可复现。
- 第六步新增第 12 维自检「工程底座与文档一致性」。

### 变更
- 第七步 Git 初始化：`.gitignore` 必须包含私有文档；明确禁止不检查就 `git add -A`。
- 自检维度 11 → 12；生成质量约束 8 → 13。

# 更新日志

本文件记录 project-scaffolder 的所有版本变更。格式遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

---

## [2.1.1] - 2026-10-09

### 🏗️ 工程化

- **迭代流程加入 CHANGELOG 强制更新约束**：references/iteration-guide.md 的"同步更新"部分新增"Skill 自身修改的特殊要求"，明确每次修改 SKILL.md 或 references/ 时必须同步更新 CHANGELOG.md（含版本号升级），迭代质量检查清单新增对应检查项。修复了之前"修改 Skill 但 CHANGELOG 不更新"的流程漏洞。

---

## [2.1.0] - 2026-10-09

### ✨ 新功能

- **技术选型决策框架**：第二步资源选型加入"技术选型必须有决策依据"约束，新增 `references/tech-selection.md`，包含四步决策流程（需求约束→候选方案→多维度对比→最终选型）、6维度加权打分表、常见项目类型推荐技术栈、5个选型反模式
- **增量更新与多轮迭代流程**：将原"执行阶段的动态调整"（5行简述）扩展为完整章节，新增 `references/iteration-guide.md`，包含6种迭代场景分类、五步标准迭代流程（现状探查→影响评估→执行修改→同步更新→验证交付）、每种场景的具体处理示例、回滚策略、迭代质量检查清单（11项）

### 🐛 Bug 修复

- 修复第二步编号重复（资源选型和项目结构规划都是"3."），修正为 3/4/5 连续编号
- 修复第六步标题写"十个维度"但实际有 11 个维度，修正为"十一个维度"

### 📝 文档

- References 导航新增 tech-selection.md 和 iteration-guide.md
- 版本号更新为 v2.1.0，更新"基于"说明

---

## [2.0.0] - 2026-10-09

### ✨ 新功能

- **功能完整性矩阵**（核心能力）：第二步新增"功能完整性矩阵"环节，生成项目时自动对照 7 大项目类型的标配功能清单，确保 P0（核心）和 P1（周边标配）功能首次交付就完整，不再出现"只做核心功能、遗漏收藏/搜索/通知"的问题
- **第 11 维自检**：第六步新增"内容完整性检查"维度，对照标配功能清单逐项检查 P0/P1 实现状态，含功能完整性反向检查（后端有 API 但前端没入口）和常见缺失模式
- **第 8 条生成质量约束**：第三步新增"周边标配功能同步生成"约束，生成核心功能时必须同步生成 P1 周边功能，不允许"留空"或"TODO"
- **新增 references/content-completeness.md**：7 大项目类型（社交/电商/工具/管理后台/学习/商业/活动/个人生活）的标配功能清单，每个功能标注 P0/P1/P2 优先级，含完整性检查执行规则

### 📝 文档

- README.md 从通用模板重写为 1000+ 字实质内容（核心能力/七步流程/功能完整性矩阵/11维自检/使用示例/目录结构）
- 新增 10 个辅助文档：QUICKSTART/FAQ/CONTRIBUTING/SECURITY/CODE_OF_CONDUCT/INSTALLATION/USE-CASES/SUPPORT/API/ARCHITECTURE/TESTING/DEBUGGING
- 新增 LICENSE（MIT）、.gitignore、.editorconfig
- 新增 examples/ 示例目录（含 PetShare 真实案例摘要）
- USE-CASES.md 填充 7 个真实使用案例（求职项目/学习计划/电商创业/旅行计划/行业调研/技术沙龙/自媒体运营）

### 🏗️ 工程化

- 通过 skill-optimizer 健康检查，总分从 66.2（C级）提升到 97.0（S级专业级）
- 修复 doc-template.md 表格列数不匹配（行333，1列→2列）

---

## [1.2.0] - 2026-10-08

### ✨ 新功能

- **第 10 维运行时验证**：第六步新增"运行时验证"维度，防止"静态全过但跑不起来"，含后端导入验证/前端编译验证/数据库模型验证/配置文件解析验证/文档与代码一致性检查
- **Git 初始化步骤**：新增第七步"Git 初始化与交付"，含 .gitignore 生成（按项目类型）、Git 仓库初始化、README 创建、交付清单确认
- **框架语法检查扩展**：框架语法从 5 个扩展到 14 个（微信小程序/React/Vue/Next.js/Nuxt/Angular/FastAPI/Flask/Django/Spring Boot/Express/Flutter/uni-app）

### 📝 文档

- 第六步自检维度从 9 维扩展到 10 维
- 新增第七步完整流程说明

---

## [1.1.0] - 2026-10-08

### ✨ 新功能

- **自检维度扩展**：从 5 维基础检查扩展到 9 维深度检查，新增：
  - 前后端契约检查（含功能完整性反向检查）
  - 依赖完整性检查（扫描 import 与依赖清单比对）
  - 静态资源检查（扫描引用的资源路径确认文件存在）
  - 框架语法检查（5 个框架的特定语法约束）

### 🐛 Bug 修复

- 修复生成项目时前后端接口不一致的问题（通过前后端契约检查）
- 修复静态资源引用缺失的问题（通过静态资源检查）

---

## [1.0.0] - 2026-10-08

### ✨ 新功能

- **初始版本发布**：项目全周期生成器 Skill 首次发布
- **七步工作流程**：需求分析→产物规划→产物生成→人机分工→指导文档→多轮自检→交付
- **7 大项目类型支持**：软件/技术、学习/成长、内容/创作、商业/创业、研究/调研、活动/组织、个人/生活，以及混合型
- **人机分工 A/B/C 模型**：AI 直接完成 / AI 生成框架+用户填充 / 必须用户自己完成
- **七要素指导文档**：每章包含概念解释→原理说明→操作指引→🤝分工→💡深度讲解→📝精简总结→🎯梯度验证任务
- **5 维自检**：产物自检/文档自检/分工自检/通用性自检/可执行性自检
- **5 个 references 文件**：project-types.md / division-rules.md / doc-template.md / verification-patterns.md / content-completeness.md（初始版）

### 📝 文档

- SKILL.md 核心文档（七步流程 + 输出规范）
- 初始 references 知识库

---

## 版本说明

### 版本号规则

- **主版本号（MAJOR）**：不兼容的架构变更或核心流程重写
- **次版本号（MINOR）**：向下兼容的功能性新增（如新增自检维度、新增 references）
- **修订号（PATCH）**：向下兼容的问题修正（如 Bug 修复、文档修正）

### 已验证的实战项目

- **PetShare 宠物社交平台**（v1.0→v2.0 全程验证）：FastAPI 后端 + 微信小程序前端，9模型/8路由/12页面/16测试全通过，经历 5 轮自检和 P0-P3 内容设计优化

---

*最后更新：2026-10-09*
