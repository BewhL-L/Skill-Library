#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_zero_cut.py 的单元测试。"""

from __future__ import annotations

from pathlib import Path

import verify_zero_cut


def _write(tmp_path: Path, name: str, text: str) -> Path:
    p = tmp_path / name
    p.write_text(text, encoding="utf-8")
    return p


def test_exact_kept(tmp_path: Path) -> None:
    """新文档完整保留原文时通过。"""
    orig = _write(tmp_path, "o.md", "# 标题\n\n这是一段需要保留的内容。\n")
    new = _write(tmp_path, "n.md", "# 标题\n\n新增指南\n\n这是一段需要保留的内容。\n")
    result = verify_zero_cut.compare(orig, new)
    assert result["ok"] is True
    assert result["exact_kept"] >= 1
    assert result["missing"] == 0


def test_missing_detected(tmp_path: Path) -> None:
    """删除原文一行应被识别为疑似删减。"""
    orig = _write(tmp_path, "o.md", "# 标题\n\n重要的一行内容必须保留。\n\n另一行。\n")
    new = _write(tmp_path, "n.md", "# 标题\n\n另一行。\n")
    result = verify_zero_cut.compare(orig, new)
    assert result["missing"] >= 1
    assert result["ok"] is False


def test_changed_number_not_exact(tmp_path: Path) -> None:
    """数字被改写时不应算作严格保留。"""
    orig = _write(tmp_path, "o.md", "tests 目录下有 pytest 47 个用例需要核对。\n")
    new = _write(tmp_path, "n.md", "tests 目录下有 pytest 79 个用例需要核对。\n")
    result = verify_zero_cut.compare(orig, new)
    assert result["exact_kept"] == 0
