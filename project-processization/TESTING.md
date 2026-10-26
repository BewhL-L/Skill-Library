# 测试说明

## 运行测试

```bash
# 全部测试（需先安装 pytest）
python -m pytest tests -v

# 仅单元测试 / 集成测试
python -m pytest tests/unit -v
python -m pytest tests/integration -v

# 覆盖率
python -m pytest tests --cov=scripts --cov-report=term-missing
```

## 测试结构

```text
tests/
├── conftest.py                    # 注入 scripts 路径 + sample_project 夹具
├── unit/
│   ├── test_scan_project_facts.py # 事实扫描：计数/测试数/组件/服务/依赖/.env
│   ├── test_validate_md.py        # 结构校验：围栏状态机/层级/表格/双链
│   ├── test_verify_zero_cut.py    # 零删减：保留/删除/数字改写
│   └── test_make_toc.py           # slug 与目录生成
└── integration/
    └── test_workflow.py           # 端到端：增补指南 → 三连校验
```

## 夹具（fixture）

`conftest.py` 提供 `sample_project`：在临时目录构造一个最小项目
（后端 `app` + `tests`、前端 `views`、`.env`、`requirements.txt`、`docker-compose.yml`），
让统计类测试隔离、可重复，不依赖任何真实项目路径。

## 覆盖的关键行为

- 组件目录排除 `__init__.py`；测试函数统计准确。
- 代码围栏内 `#` 不被误判为标题（状态机）。
- H1 唯一、层级跳跃、表格列数、空目标双链均能检出。
- 原文删除 / 数字改写不会被当作"严格保留"。
- 中文 slug 与连续空格双连字符符合 GitHub 规则。
- 端到端：一份合法增补指南能通过结构校验与零删减比对并生成目录。

## 新增测试的约定

- 测试文件命名 `test_*.py`，函数命名 `test_<行为>`。
- 用 `tmp_path` 或 `sample_project` 构造输入，不依赖外部环境。
- 每个测试函数都要有 `-> None` 注解与 docstring，且必须包含 `assert`。
- 修复 bug 时先补一个能复现问题的失败测试，再修复。
