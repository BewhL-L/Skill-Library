# 测试指南

## 📋 概述

本文档描述项目的测试策略、测试框架、测试用例编写规范和测试覆盖率要求。

---

## 🧪 测试体系

### 测试分层

```
┌─────────────────────────────────────────┐
│         端到端测试 (E2E)                 │
│  完整用户场景，从命令输入到结果验证        │
│  数量：少而精，覆盖核心流程                │
├─────────────────────────────────────────┤
│         集成测试 (Integration)            │
│  多个模块协同工作，命令级别的功能验证       │
│  数量：12 个命令，每个命令至少 1 个用例    │
├─────────────────────────────────────────┤
│         单元测试 (Unit)                   │
│  单个函数/类的逻辑验证，隔离依赖           │
│  数量：36 个用例，覆盖核心工具函数          │
└─────────────────────────────────────────┘
```

### 测试文件

| 文件 | 类型 | 用例数 | 用途 |
|------|------|--------|------|
| `unit-test.py` | 单元测试 | 36 | 测试核心函数逻辑 |
| `test-all.py` | 集成测试 | 12 | 测试 12 个命令的端到端功能 |

---

## 🔧 测试框架

### 单元测试框架

**框架**：pytest（兼容 unittest）

**配置**：
- 测试文件命名：`test_*.py` 或 `*_test.py`
- 测试函数命名：`test_*`
- 测试类命名：`Test*`
- 使用 `assert` 语句进行断言

**常用插件**：
- `pytest-cov` - 代码覆盖率
- `pytest-xdist` - 并行测试
- `pytest-mock` - Mock 支持

### 集成测试框架

**框架**：自定义测试运行器（subprocess + 断言）

**特点**：
- 通过 subprocess 调用真实命令
- 验证命令退出码
- 验证输出文件存在性
- 验证输出内容正确性
- 自动清理测试临时文件

---

## 📝 单元测试详解

### 测试结构

```python
import unittest
import tempfile
import os
from pathlib import Path

class TestFrontmatterParser(unittest.TestCase):
    """Frontmatter 解析器测试"""

    def setUp(self):
        """每个测试前的准备工作"""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """每个测试后的清理工作"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_parse_valid_frontmatter(self):
        """测试解析有效的 Frontmatter"""
        # 准备
        content = """---
title: 测试笔记
tags: [测试, 示例]
category: 测试分类
difficulty: ⭐⭐⭐
---
# 测试内容
"""
        # 执行
        result = parse_frontmatter(content)

        # 断言
        self.assertEqual(result['title'], '测试笔记')
        self.assertEqual(len(result['tags']), 2)
        self.assertEqual(result['category'], '测试分类')
```

### 测试分类

#### 1. Frontmatter 解析测试（8 个用例）

| 用例 | 测试内容 |
|------|---------|
| test_parse_valid_frontmatter | 解析有效的 Frontmatter |
| test_parse_empty_frontmatter | 解析空 Frontmatter |
| test_parse_missing_fields | 解析缺失字段的 Frontmatter |
| test_parse_invalid_yaml | 解析无效的 YAML |
| test_parse_multiline_values | 解析多行值 |
| test_parse_list_values | 解析列表值 |
| test_parse_special_characters | 解析特殊字符 |
| test_parse_no_frontmatter | 解析无 Frontmatter 的文档 |

#### 2. 标签处理测试（6 个用例）

| 用例 | 测试内容 |
|------|---------|
| test_normalize_tag_case | 标签大小写归一化 |
| test_merge_duplicate_tags | 合并重复标签 |
| test_remove_empty_tags | 移除空标签 |
| test_tag_too_many | 标签数量过多检测 |
| test_tag_too_few | 标签数量过少检测 |
| test_tag_mapping | 标签映射规则 |

#### 3. 双链检测测试（6 个用例）

| 用例 | 测试内容 |
|------|---------|
| test_detect_wiki_link | 检测 Wiki 风格链接 |
| test_detect_markdown_link | 检测 Markdown 风格链接 |
| test_detect_dead_link | 检测死链 |
| test_detect_valid_link | 检测有效链接 |
| test_count_link_references | 统计链接引用次数 |
| test_detect_orphan_note | 检测孤立文档 |

#### 4. 文件扫描测试（5 个用例）

| 用例 | 测试内容 |
|------|---------|
| test_scan_markdown_files | 扫描 Markdown 文件 |
| test_scan_nested_directories | 扫描嵌套目录 |
| test_scan_ignore_hidden_files | 忽略隐藏文件 |
| test_scan_empty_directory | 扫描空目录 |
| test_scan_nonexistent_directory | 扫描不存在的目录 |

#### 5. 模板渲染测试（5 个用例）

| 用例 | 测试内容 |
|------|---------|
| test_render_simple_template | 渲染简单模板 |
| test_render_with_variables | 带变量渲染 |
| test_render_missing_variables | 缺失变量处理 |
| test_render_conditional_blocks | 条件块渲染 |
| test_render_loop_blocks | 循环块渲染 |

#### 6. 异常处理测试（6 个用例）

| 用例 | 测试内容 |
|------|---------|
| test_handle_file_not_found | 文件不存在异常 |
| test_handle_permission_error | 权限异常 |
| test_handle_invalid_encoding | 编码异常 |
| test_handle_disk_full | 磁盘满异常 |
| test_handle_invalid_input | 无效输入异常 |
| test_handle_network_error | 网络异常（如适用） |

---

## 🔄 集成测试详解

### 测试流程

```python
def test_init_command():
    """测试 init 命令"""
    with tempfile.TemporaryDirectory() as temp_dir:
        # 1. 执行命令
        result = subprocess.run(
            ['python', 'scripts/kb.py', 'init', '--name', '测试知识库',
             '--path', temp_dir, '--theme', '测试'],
            capture_output=True, text=True
        )

        # 2. 验证退出码
        assert result.returncode == 0

        # 3. 验证输出
        assert '知识库创建成功' in result.stdout

        # 4. 验证文件存在
        assert os.path.exists(os.path.join(temp_dir, 'Home.md'))
        assert os.path.exists(os.path.join(temp_dir, '01-测试分类'))

        # 5. 验证文件内容
        with open(os.path.join(temp_dir, 'Home.md'), 'r', encoding='utf-8') as f:
            content = f.read()
            assert '测试知识库' in content
```

### 12 个命令测试

| 命令 | 测试内容 | 验证点 |
|------|---------|--------|
| `init` | 初始化知识库 | 目录结构、Home.md、MOC、学习路线 |
| `note` | 生成单篇笔记 | Frontmatter、五段式结构、MOC 更新 |
| `batch-note` | 批量生成笔记 | 多文件生成、顺序、MOC 更新 |
| `moc` | 生成 MOC | 文档索引、学习路线、知识关联 |
| `audit` | 健康检查 | 报告格式、统计数据、问题识别 |
| `validate` | 质量校验 | 校验项、问题清单、严格模式 |
| `fix-fm` | 补全 Frontmatter | 字段补全、推断逻辑、dry-run |
| `fix-link` | 修复死链 | 高频死链创建、阈值控制、dry-run |
| `fix-tags` | 统一标签 | 映射规则、合并重复、dry-run |
| `standardize` | 一键标准化 | 流程执行、报告输出、全库处理 |
| `progress` | 学习进度 | 统计维度、报告格式、数据准确 |
| `info` | 帮助信息 | 命令列表、用法说明、版本信息 |

---

## 📊 代码覆盖率

### 覆盖率目标

| 模块 | 目标覆盖率 | 当前覆盖率 |
|------|-----------|-----------|
| 核心工具函数 | ≥90% | 100% |
| CLI 入口 | ≥80% | 100% |
| 业务逻辑 | ≥85% | 100% |
| 整体项目 | ≥80% | 100% |

### 覆盖率配置（.coveragerc）

```ini
[run]
source = .
omit =
    */tests/*
    */test_*.py
    setup.py
    */__pycache__/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    if self.debug:
    if settings.DEBUG
    raise NotImplementedError
    if __name__ == .__main__.:

[html]
directory = coverage_html_report

[xml]
output = coverage.xml
```

### 覆盖率报告生成

```bash
# 运行测试并生成覆盖率报告
coverage run unit-test.py

# 查看文本报告
coverage report

# 查看详细报告（包含未覆盖的行）
coverage report -m

# 生成 HTML 报告（可在浏览器中查看）
coverage html

# 生成 XML 报告（用于 CI/CD 集成）
coverage xml
```

### 覆盖率报告解读

```
Name                      Stmts   Miss  Cover
---------------------------------------------
kb.py                       156      0   100%
scripts/init-kb.py           89      0   100%
scripts/generate-note.py    102      0   100%
scripts/generate-moc.py      78      0   100%
scripts/audit-kb.py          95      0   100%
scripts/validate-kb.py       87      0   100%
scripts/fix-frontmatter.py   65      0   100%
scripts/fix-links.py         72      0   100%
scripts/fix-tags.py          58      0   100%
scripts/standardize.py       45      0   100%
---------------------------------------------
TOTAL                       847      0   100%
```

---

## 🚀 运行测试

### 使用 Makefile（推荐）

```bash
# 运行所有测试（单元+集成）
make test

# 只运行单元测试
make test-unit

# 只运行集成测试
make test-integration

# 生成代码覆盖率报告
make coverage

# 完整质量检查（lint + test + type-check）
make check
```

### 手动运行

```bash
# 运行单元测试
python unit-test.py

# 运行集成测试
python test-all.py

# 使用 pytest 运行
pytest unit-test.py -v

# 运行特定测试类
pytest unit-test.py::TestFrontmatterParser -v

# 运行特定测试方法
pytest unit-test.py::TestFrontmatterParser::test_parse_valid_frontmatter -v

# 并行运行测试
pytest unit-test.py -n auto

# 生成覆盖率报告
coverage run unit-test.py
coverage report -m
coverage html
```

### CI/CD 中运行

GitHub Actions 会自动运行测试：

```yaml
- name: Run tests
  run: |
    python -m pip install -r requirements-dev.txt
    coverage run unit-test.py
    coverage report -m
    coverage xml

- name: Upload coverage
  uses: actions/upload-artifact@v3
  with:
    name: coverage-report
    path: coverage.xml
```

---

## ✅ 测试最佳实践

### 1. 测试命名规范

- 测试文件：`test_*.py` 或 `*_test.py`
- 测试类：`Test*`（大驼峰）
- 测试函数：`test_*`（小写下划线）
- 测试名称应描述测试内容，而非测试方法

**好的命名**：
```python
def test_parse_valid_frontmatter_with_all_fields():
def test_init_creates_12_top_level_directories():
def test_fix_link_creates_note_for_high_frequency_dead_link():
```

**不好的命名**：
```python
def test1():
def test_parse():
def test_init_command():
```

### 2. 测试结构（AAA 模式）

每个测试应遵循 Arrange-Act-Assert 模式：

```python
def test_example():
    # Arrange - 准备测试数据和环境
    temp_dir = tempfile.mkdtemp()
    input_data = "test content"

    # Act - 执行被测试的代码
    result = process(input_data)

    # Assert - 验证结果
    assert result == expected_output
    assert os.path.exists(output_file)
```

### 3. 测试隔离

- 每个测试应独立运行，不依赖其他测试的结果
- 使用 `setUp()` 和 `tearDown()` 管理测试环境
- 使用临时目录避免污染真实文件系统
- Mock 外部依赖（网络、数据库等）

### 4. 测试数据

- 使用固定的测试数据，避免随机值
- 测试数据应覆盖边界情况
- 使用参数化测试减少重复代码

```python
import pytest

@pytest.mark.parametrize("input,expected", [
    ("⭐", 1),
    ("⭐⭐", 2),
    ("⭐⭐⭐", 3),
    ("⭐⭐⭐⭐", 4),
    ("⭐⭐⭐⭐⭐", 5),
])
def test_difficulty_star_count(input, expected):
    assert count_stars(input) == expected
```

### 5. 异常测试

```python
import pytest

def test_invalid_input_raises_error():
    with pytest.raises(ValueError) as exc_info:
        process(None)
    assert "输入不能为空" in str(exc_info.value)
```

### 6. 测试覆盖率

- 新功能必须添加对应的单元测试
- 修复 Bug 必须添加回归测试
- 核心工具函数覆盖率应达到 100%
- 整体覆盖率不应低于 80%
- 提交前运行 `make coverage` 检查覆盖率

---

## 🐛 调试测试

### 测试失败排查

1. **查看错误信息**：仔细阅读断言错误和异常堆栈
2. **单独运行失败测试**：`pytest unit-test.py::TestClass::test_method -v`
3. **添加调试输出**：使用 `print()` 或 `logging` 输出中间状态
4. **使用断点**：`import pdb; pdb.set_trace()`
5. **检查测试环境**：确认临时目录、依赖版本等

### 常见测试问题

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 测试在本地通过但 CI 失败 | 环境差异 | 使用相同的 Python 版本和依赖 |
| 测试随机失败 | 测试顺序依赖 | 确保测试隔离，使用独立的临时目录 |
| 覆盖率不达标 | 缺少测试 | 添加缺失的测试用例 |
| 测试运行慢 | 大量 IO 操作 | Mock 文件系统操作，使用内存文件系统 |
| 断言不清晰 | 断言信息不足 | 使用描述性的断言消息 |

---

## 📞 相关文档

- [ARCHITECTURE.md](ARCHITECTURE.md) - 项目架构
- [DEBUGGING.md](DEBUGGING.md) - 调试指南
- [CONTRIBUTING.md](CONTRIBUTING.md) - 贡献指南
- [.coveragerc](.coveragerc) - 覆盖率配置
- [Makefile](Makefile) - 构建工具

---

> **最后更新**：2026-08-30
>
> **版本**：v3.1
