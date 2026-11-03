# TESTING

本文件说明 `skill-optimizer` 自身怎么测、测到什么程度、改完之后该回归什么。

## 1. 测试规模

| 项 | 数量 |
|---|---|
| 测试文件 | 9（6 单元 + 2 集成 + 1 conftest） |
| 测试用例 | **97** |
| 组织方式 | 按模块分文件，类内聚（`class TestXxx`），pytest 自动发现 |

## 2. 分层与职责

| 文件 | 用例 | 覆盖对象 |
|---|---|---|
| `tests/unit/test_audit_skill.py` | 12 | 八大维度的评分规则：元数据、文档清单、模板、可用性、代码质量 |
| `tests/unit/test_skill_type_detector.py` | 18 | 类型检测（代码驱动 / 纯文档 / 混合）与权重切换 |
| `tests/unit/test_skill_opt.py` | 30 | `skill-opt.py` 命令行入口与子命令分发 |
| `tests/unit/test_optimize_skill.py` | 9 | 自动补文档/配置的写盘行为 |
| `tests/unit/test_generate_docs.py` | 9 | 文档生成模板与占位替换 |
| `tests/unit/test_generate_tests.py` | 9 | 测试脚手架生成 |
| `tests/unit/test_meta_consistency.py` | 2 | 版本号、SKILL.md 与 CHANGELOG 的一致性 |
| `tests/integration/test_cli.py` | 4 | 真实子进程跑 CLI，验证退出码与输出 |
| `tests/integration/test_workflow.py` | 4 | "建临时 skill → 审计 → 优化 → 复审"的完整链路 |

## 3. 怎么跑

```bash
pip install -r requirements.txt      # pytest / ruff 等开发依赖
python -m pytest                     # 全量（pyproject 已配 testpaths=tests、-v --tb=short）
python -m pytest tests/unit/test_audit_skill.py -q
python -m pytest -k "metadata" -vv   # 只跑某类用例
```

覆盖率（`.coveragerc` 已把 `source` 设为项目根、排除 `tests/` 与缓存）：

```bash
python -m pytest --cov --cov-report=term-missing
```

> **环境限制**：本机当前 Python（3.13）未安装 pytest，直接 `python -m pytest` 会报
> `No module named pytest`。需先按上面第一条装依赖；审计脚本本身只依赖标准库，不受影响。

## 4. 无法自动化、需要手工验证的部分

1. **对真实 Skill 的端到端审计**：规则改动后，至少对三个真实技能各跑一次，确认分数变化可解释：

   | 目标 | 预期 |
   |---|---|
   | `hermes-portability` | 99（唯一遗留：argparse 不适用于 bash） |
   | `project-processization` | 100 |
   | `project-scaffolder` | 100 |

2. **BOM 场景**：Windows 上编辑过的文件常带 UTF-8 BOM。用带 BOM 的 `SKILL.md` 建临时技能，确认不再误报「缺少 frontmatter」（已在 v1.8.1 修复）。
3. **中文/空格路径**：在 `C:\Users\...\AI文档\...` 这类路径下跑，确认没有编码异常。
4. **UNC 路径**：`\\wsl.localhost\...` 下审计，确认 `Path` 与 `read_text` 不抛异常。

## 5. 回归清单（改动评分规则后必做）

- [ ] `python -m pytest` 全绿（若环境无 pytest，至少手工跑第 4 节四项）
- [ ] 三个真实技能的分数变化能用"规则变化"解释，而不是"某处读不到文件"
- [ ] 无新增 🔴/🟠 级问题
- [ ] `CHANGELOG.md` 记录了规则变更与受影响维度
- [ ] 类型检测未误判（纯文档型技能不该被套用代码权重）

## 6. 已知盲区

- **只测规则，不测真实文件系统边界**：权限拒绝、符号链接环、超大目录（>10 万文件）未覆盖。
- **性能无基线**：899 行脚本对单个技能约 1–3 秒，仓库级批量审计的耗时未测。
- **可用性维度按源码文件集合判断**：1.9.4 起扫描全部非测试源文件，不再受文件顺序影响。
- **docstring 与注解覆盖率只统计非测试源码**：`tests/` 下的简洁写法不再拖低该项（1.9.4 起）。
