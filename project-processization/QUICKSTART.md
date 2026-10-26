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

## 第三步：套模板写指南

1. 复制 `templates/learning-guide-template.md` 到项目 `README.md` 末尾（`## License` 之前）。
2. 用 `facts.json` 与源码核对结果填充所有 `{{...}}` 占位。
3. 写法参照 `references/03-写作规范.md`；需要的 Prompt 从 `references/04-AI协作Prompt库.md` 复制。
4. 删除模板里的 `<!-- 使用说明 -->` 注释块。

## 第四步：三连校验

```bash
# 结构（H1 唯一、围栏闭合、层级不跳、表格列数）
python scripts/validate_md.py --path README.md --require-frontmatter

# 原文零删减（有意的事实修正请用 --allow-note 说明）
python scripts/verify_zero_cut.py --original README_orig.md --new README.md

# 生成并写回折叠目录
python scripts/make_toc.py --path README.md --start "学习指南" --end "License" \
  --levels 3-4 --details --title "学习指南目录（点击展开）" \
  --insert-after "学习指南（AI 协作版）" --write
```

## 验收标准

- 三条命令都通过（`validate` 无问题、`verify_zero_cut` 仅剩已声明的有意修正、TOC 锚点与标题一致）。
- 八章齐全；每阶段含周期 / 验收 / 练习 / 优先级；结尾有可勾选的终极 checklist。
- 每个数字都能在 `facts.json` 或源码中找到来源。

## 卡住了？

- 想了解每轮该做什么：见 `references/01-五轮迭代方法论.md`。
- 不确定某个事实怎么核对：见 `references/02-事实核查清单.md`。
- 命令参数不清楚：`python scripts/xxx.py --help`。
