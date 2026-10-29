#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_docs.py 的单元测试：四类断言 + 退出码。"""

from __future__ import annotations

import sys
from pathlib import Path

import check_docs
import pytest


def _write_tests(tests_dir: Path, skipped: bool = False) -> None:
    tests_dir.mkdir(parents=True, exist_ok=True)
    body = "def test_one():\n    assert True\n"
    if skipped:
        body = 'import pytest\n\npytestmark = pytest.mark.skip(reason="todo")\n\n' + body
    (tests_dir / "test_sample.py").write_text(body, encoding="utf-8")


def test_count_tests_separates_skipped(tmp_path: Path) -> None:
    """被 skip 的用例计入总数，但不计入 passed。"""
    _write_tests(tmp_path / "tests")
    assert check_docs.count_tests(tmp_path / "tests") == (1, 0)

    _write_tests(tmp_path / "tests_skip", skipped=True)
    assert check_docs.count_tests(tmp_path / "tests_skip") == (1, 1)


def test_check_numbers_accepts_passed_or_total(tmp_path: Path) -> None:
    tests_dir = tmp_path / "tests"
    _write_tests(tests_dir)

    assert check_docs.check_numbers("# 1 passed", tests_dir) == []
    assert check_docs.check_numbers("目录里 1 个测试", tests_dir) == []

    errors = check_docs.check_numbers("# 9 passed", tests_dir)
    assert errors and "9" in errors[0]


def test_check_numbers_ignores_frontend_line(tmp_path: Path) -> None:
    """前端 `npm run test # 5 passed` 不应被当成后端数量。"""
    tests_dir = tmp_path / "tests"
    _write_tests(tests_dir)
    text = "```\npytest -q   # 1 passed\nnpm run test  # 5 passed（vitest）\n```"
    assert check_docs.check_numbers(text, tests_dir) == []


def test_check_paths_and_backend_fallback(tmp_path: Path) -> None:
    """`scripts/x.py` 允许落在 backend/scripts 下。"""
    (tmp_path / "backend" / "scripts").mkdir(parents=True)
    (tmp_path / "backend" / "scripts" / "x.py").write_text("", encoding="utf-8")

    assert check_docs.check_paths("`backend/scripts/x.py`", tmp_path) == []
    assert check_docs.check_paths("`scripts/x.py`", tmp_path) == []

    errors = check_docs.check_paths("`backend/app/nope.py`", tmp_path)
    assert errors and "nope.py" in errors[0]


def test_check_forbidden() -> None:
    errors = check_docs.check_forbidden("见 产品/backend", {"产品/": "旧路径"})
    assert errors and "产品/" in errors[0]


def test_check_endpoints_normalizes_braces() -> None:
    routes = {"/api/kb/{}", "/api/kb/{}/members", "/api/chat"}
    text = "`/api/kb/{id}/members`、`/api/chat`"
    assert check_docs.check_endpoints(text, routes) == []

    errors = check_docs.check_endpoints("`/api/not-exist`", routes)
    assert errors and "not-exist" in errors[0]


def test_check_private_detects_tracked_env(tmp_path: Path, monkeypatch) -> None:
    class _Result:
        returncode = 0
        stdout = "README.md\nbackend/.env\n"

    monkeypatch.setattr(check_docs.subprocess, "run", lambda *a, **k: _Result())
    errors = check_docs.check_private(tmp_path, {"backend/.env": "密钥"})
    assert errors and "backend/.env" in errors[0]


def test_main_exit_codes(tmp_path: Path, monkeypatch) -> None:
    """数量一致退出 0，不一致退出 1。"""
    tests_dir = tmp_path / "tests"
    _write_tests(tests_dir)
    (tmp_path / "README.md").write_text("```\npytest -q  # 1 passed\n```\n", encoding="utf-8")

    monkeypatch.setattr(
        sys, "argv", ["check_docs.py", "--root", str(tmp_path), "--tests", "tests", "--skip-git"]
    )
    assert check_docs.main() == 0

    (tmp_path / "README.md").write_text("```\npytest -q  # 7 passed\n```\n", encoding="utf-8")
    assert check_docs.main() == 1


def test_check_endpoints_accepts_method_prefix() -> None:
    """README 常写 `POST /api/kb`：方法前缀与 query 不该导致漏检（曾整类跳过）。"""
    routes = {"/api/kb", "/api/chat"}

    assert check_docs.check_endpoints("`POST /api/kb`、`GET /api/chat?top_k=5`", routes) == []

    errors = check_docs.check_endpoints("`POST /api/gone`", routes)
    assert errors and "gone" in errors[0]

