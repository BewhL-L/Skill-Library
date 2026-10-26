#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""validate_md.py 的单元测试。"""

from __future__ import annotations

import validate_md


def test_split_frontmatter() -> None:
    """能正确拆分 frontmatter 与正文。"""
    fm, body = validate_md.split_frontmatter("---\ntitle: x\n---\n# H1\n")
    assert fm is not None
    assert "title: x" in fm
    assert "# H1" in body


def test_collect_headings_ignores_fence_hash() -> None:
    """围栏内 bash 注释不计入标题。"""
    body = "# 标题\n```bash\n# 注释\n```\n## 二级\n"
    headings = validate_md.collect_headings(body)
    assert len(headings) == 2


def test_unclosed_fence_detected() -> None:
    """奇数个围栏应报错。"""
    issues = validate_md.check_fences("```bash\nprint(1)\n")
    assert any("未闭合" in i["message"] for i in issues)


def test_heading_hierarchy_single_h1_ok() -> None:
    """恰好一个 H1 且不跳级时无问题。"""
    headings = [(1, 1, "A"), (2, 2, "B"), (2, 2, "C")]
    assert validate_md.check_heading_hierarchy(headings) == []


def test_heading_hierarchy_skip_level() -> None:
    """H2 后直接 H4 应报层级跳跃。"""
    headings = [(1, 1, "A"), (2, 2, "B"), (4, 4, "D")]
    issues = validate_md.check_heading_hierarchy(headings)
    assert any("跳跃" in i["message"] for i in issues)


def test_table_column_mismatch() -> None:
    """数据行列数与表头不一致应报错。"""
    table = "| A | B |\n|---|---|\n| 1 | 2 |\n| 3 |\n"
    issues = validate_md.check_tables(table)
    assert any("列数不匹配" in i["message"] for i in issues)


def test_empty_wikilink_detected() -> None:
    """空目标双链应被识别。"""
    issues = validate_md.check_wikilinks("见 [[|某页]]")
    assert any("空目标双链" in i["message"] for i in issues)
