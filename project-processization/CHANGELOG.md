# Changelog

## v1.1.2 — 2026-10-27

### 变更
- `references/05-文档一致性与防漂移.md` 第 4 节补充跨 Skill 指引：完整四道门片段见 `project-scaffolder/references/ci-snippets.md`（仅在已安装该 Skill 时可用；未安装则按本节做法逐项补）。

## v1.1.1 — 2026-10-27

### 新增
- `tests/unit/test_check_docs.py`：8 条用例覆盖四类断言与退出码（含"前端 passed 行不应混算"的回归）。
- `tests/unit/test_meta_consistency.py`：3 条元一致性用例——页脚版本 == CHANGELOG 最新版本、SKILL.md 引用的文件都存在、页脚脚本数 == scripts/ 实际数。

### 修复
- `ARCHITECTURE.md` 流程图仍画成"单文档增补"，改为双产物（公开 README / 私密指南）两条链路。
- `DEBUGGING.md` 的 H1 指引按合并模型写成"沿用 README 的 H1"，改为"独立文档有且仅有 1 个 H1"。
- `README.md` 的零删减原则未限定范围，补"仅指公开 README"。
- 测试数 24 → 32（README / INSTALLATION）。
- 五、输出规范第 2 条把 README 与指南的要求混写在一条，拆成两条子项。
- SKILL.md 里 `references/01` 这类简写展开为完整文件名（元一致性测试抓到的失效引用）。
- SKILL.md frontmatter 补 `title` 字段，消除 `validate_md.py` 的 low 级提示。

## v1.1.0 — 2026-10-27

### 新增
- `references/05-文档一致性与防漂移.md`：单一事实源、四类断言、CI 接入、架构图规范、假完备清单、公开/私密分离。
- `scripts/check_docs.py`：文档与代码一致性校验（测试数 / 路径 / 废弃表述 / 私有文件 / 可选接口清单），可接 CI。
- 核心原则新增第 6 条「公开/私密分离」：README 只放可公开内容，学习指南放仓库外并写入 `.gitignore`。

### 变更
- **产物从"一份"改为"两份"**：公开 README 增强（能力/用法/架构/限制）+ 仓库外私密指南（分工/路线/验收）。
- 第 0 步增加"确认公开边界"；第 5 轮增加 `check_docs.py` 与 CI 接入。
- 脚本数 4 → 5；交付自检新增 3 项（反向验证、私有文件、架构图可追溯）。
- 模板 frontmatter 增加 `visibility: private`，使用说明改为"私密指南，不要并入 README"。
- 模板正文改为**独立文档**：移除"原 README 零删减"占位块与末尾 License 段（那是合并模型的遗留）。
- `references/01` 第 2 轮目标同步为"双产物"；场景三的回归校验补齐 `check_docs.py`。

# 变更记录

本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/) 与 Keep a Changelog 规范。

## [1.0.0] - 2026-10-14

### 新增

- `SKILL.md`：五条核心原则、五轮迭代工作流程、4 个脚本说明、输出规范与 3 个使用场景。
- `scripts/scan_project_facts.py`：扫描代码规模、分层行数、测试用例、组件业务文件数、
  Docker 服务、依赖、`.env` 键名（脱敏），支持 `--group-depth` 与 `--components`。
- `scripts/validate_md.py`：Markdown 结构校验（代码围栏状态机、H1 唯一、层级跳跃、
  表格列数、空目标双链）。
- `scripts/verify_zero_cut.py`：原文零删减三级比对（精确 / 宽松 / 疑似删减）。
- `scripts/make_toc.py`：GitHub 风格 slug 折叠目录生成，支持区间、层级与写回。
- `references/` 四篇深入参考：五轮方法论、事实核查清单、写作规范、AI 协作 Prompt 库。
- `templates/learning-guide-template.md`：八章学习指南主骨架（Frontmatter + 折叠 TOC +
  快速入口 + callout + 表格 + 验收清单）。
- `examples/企业知识库项目-章节映射.md`：真实企业级 RAG+Agent 项目样例。
- `tests/`：4 个单元测试文件 + 1 个集成测试文件，共 24 个用例，全部通过。
- 工程化配置：`pyproject.toml`、`Makefile`、`.coveragerc`、`.editorconfig`、
  `.gitignore`、`.pre-commit-config.yaml`、`.github/workflows/ci.yml`。

### 验证

- 4 个脚本在真实企业级项目上实测：
  - 组件数精确为 routers 12 / models 11 / schemas 7 / views 13（自动排除 `__init__.py`）；
  - 测试用例 79 个 / 9 文件并给出每文件分布；
  - 零删减比对 126 个实质行、125 行严格保留，唯一差异为已声明的用例数修正；
  - 目录生成 48 个锚点，与人工目录逐行一致。
- `pytest`：24 passed。
