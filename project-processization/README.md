# 项目流程化（Project Flow Skill）

> 把 AI 已经生成 / 搭好骨架的软件项目，转化成一份**零基础可学、可动手、可验收**的
> 《从零到专家 · AI 协作学习指南》。核心方法论来自一次真实的五轮迭代：
> 为一个 74KB 的企业级 RAG + Agent 项目 README 做事实校准、可执行性增强、全面性补全与
> 导航校验，最终产出可直接用于学习与面试的指南，并把全过程固化为可复用脚本与模板。

## 它解决什么问题

AI 现在能一键生成"能跑、功能齐全"的全栈项目，但学习者直接拿到会陷入两个陷阱：

- **抄完就交**：项目能跑，却一行没写、一问就露馅；
- **无从下手**：上万行代码、几十个模块，不知先读什么、什么必须自己重写、怎么验收。

本 Skill 让 AI 按一条固定流水线工作：先**扫描可信事实**，再**零删减增补**一份学习指南，
明确"AI 已完成的部分如何利用"与"学习者必须亲手做的部分怎么完成"，最后用脚本做
**结构校验、原文零删减比对、目录生成**三道回归检查。

## 五条铁律

1. **零删减（仅指公开 README）**：原 README 一个字不删，只允许插入 / 增强；事实修正必须显式声明并经脚本比对。私密指南独立成文，不受此约束。
2. **事实可追溯**：行数、测试数、组件数、依赖、服务、脚本参数都来自脚本扫描或源码，禁止编造。
3. **分工显式**：每个模块标注"AI 已完成 / 需验证 / 必须亲手写"，并配套"让 AI 讲代码"的 Prompt。
4. **循序渐进**：分阶段路线，每阶段给周期、验收、练习、优先级、学习技巧。
5. **可执行可验收**：命令可照抄、报错有排查、每步有 checklist。

## 目录结构

```text
项目流程化/
├── SKILL.md                          # 核心方法论（AI 触发后首先加载）
├── scripts/                          # 5 个纯标准库 CLI
│   ├── scan_project_facts.py         # 扫描规模/测试/组件/服务/依赖/.env
│   ├── validate_md.py                # Markdown 结构校验（围栏状态机）
│   ├── verify_zero_cut.py            # 原文零删减比对
│   ├── make_toc.py                   # 生成 GitHub 风格折叠目录
│   └── check_docs.py                 # 文档与代码一致性（测试数/路径/接口/私有文件）
├── references/                       # 深入参考（按需加载）
│   ├── 01-五轮迭代方法论.md
│   ├── 02-事实核查清单.md
│   ├── 03-写作规范.md
│   ├── 04-AI协作Prompt库.md
│   └── 05-文档一致性与防漂移.md
├── templates/
│   └── learning-guide-template.md    # 八章学习指南主骨架
├── examples/
│   └── 企业知识库项目-章节映射.md      # 真实样例：事实 → 八章
├── tests/                            # 单元 + 集成测试（32 用例）
├── .github/workflows/ci.yml          # CI
└── pyproject.toml / Makefile / .coveragerc / ...
```

## 快速上手

```bash
# 1. 扫描事实（数字全部来自这里）
python scripts/scan_project_facts.py --path ./你的项目 --group-depth 2 \
  --components "app/routers,app/models,src/views" --json --output facts.json

# 2. 复制 templates/learning-guide-template.md，按 references 填充八章

# 3. 三连校验
python scripts/validate_md.py --path README.md --require-frontmatter
python scripts/verify_zero_cut.py --original README_orig.md --new README.md
python scripts/make_toc.py --path README.md --start "学习指南" --end "License" \
  --levels 3-4 --details --write
```

详见 [QUICKSTART.md](QUICKSTART.md)；每个脚本都支持 `--help`。

## 运行要求

- Python 3.8+，**脚本仅使用标准库，零第三方依赖**。
- 开发测试可选：`pip install pytest pytest-cov ruff`（见 `pyproject.toml` 的 `[dev]`）。

## 验证

```bash
python -m pytest tests -v          # 32 个用例
python -m py_compile scripts/*.py  # 语法检查
```

## 文档导航

- [安装指南](INSTALLATION.md) · [快速上手](QUICKSTART.md) · [脚本 API](API.md)
- [架构设计](ARCHITECTURE.md) · [测试说明](TESTING.md) · [调试指南](DEBUGGING.md)
- [常见问题](FAQ.md) · [变更记录](CHANGELOG.md) · [贡献指南](CONTRIBUTING.md)
- [安全策略](SECURITY.md) · [行为准则](CODE_OF_CONDUCT.md)

## 许可证

[MIT](LICENSE)
