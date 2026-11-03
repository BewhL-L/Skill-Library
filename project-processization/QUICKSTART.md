# 快速上手（5 分钟）

> 目标：对一个项目跑完"扫描事实 → 生成指南 → 三连校验"的最小闭环。

## 前置条件

- Python 3.8+（命令行运行 `python --version` 确认）。
- 脚本零第三方依赖，无需安装任何包。

## 第一步：备份原文

```bash
cp README.md README_orig.md      # Windows PowerShell: Copy-Item README.md README_orig.md
```

## 第二步：扫描事实

```bash
python scripts/scan_project_facts.py --path ./你的项目 --group-depth 2 \
  --components "backend/app/routers,backend/app/models,frontend/src/views" \
  --json --output facts.json
```

打开 `facts.json`，记录：分层行数、测试用例数、组件业务文件数、Docker 服务、依赖、`.env` 键名。

## 第三步：写两份文档（不要混）

1. **公开 README**：原 H2 一个不删，只插入"能力 / 快速开始 / 架构 / 已知限制"四块；**不写分工、不写 AI 协作比例**。
2. **私密指南**：复制 `templates/learning-guide-template.md` 到**仓库外**（如 `../private-notes/学习指南.md`），填充所有 `{{...}}` 占位。**不要把它放进 README**。
3. **零基础读者**：另起一份《零基础精讲版》（`references/06-零基础精讲版规范.md`），不要指望一份"专家版"同时满足两种读者。
4. 写法参照 `references/03-写作规范.md`；Prompt 从 `references/04-AI协作Prompt库.md` 复制；删除模板里的 `<!-- 使用说明 -->` 注释块。

## 第四步：分别校验

```bash
# 私密指南：结构（H1 唯一、围栏闭合、层级不跳、表格列数）
python scripts/validate_md.py --path ../private-notes/学习指南.md --require-frontmatter

# 公开 README：原文零删减（有意的事实修正请用 --allow-note 说明）
python scripts/verify_zero_cut.py --original README_orig.md --new README.md

# 私密指南：生成并写回折叠目录
python scripts/make_toc.py --path ../private-notes/学习指南.md --start "学习指南" --end "License" \
  --levels 3-4 --details --title "学习指南目录（点击展开）" \
  --insert-after "学习指南（AI 协作版）" --write

# 项目：文档与代码一致性
python scripts/check_docs.py --root . --tests backend/tests
```

## 验收标准

- 三类校验都通过（`validate` 无问题、`verify_zero_cut` 仅剩已声明的有意修正、TOC 锚点与标题一致）。
- 八章齐全；每阶段含周期 / 验收 / 练习 / 优先级；结尾有可勾选的终极 checklist。
- 每个数字都能在 `facts.json` 或源码中找到来源。
- **私密指南不在仓库内**，`git ls-files` 里没有它。

## 卡住了？

- 想了解每轮该做什么：见 `references/01-五轮迭代方法论.md`。
- 不确定某个事实怎么核对：见 `references/02-事实核查清单.md`。
- 命令参数不清楚：`python scripts/xxx.py --help`。
