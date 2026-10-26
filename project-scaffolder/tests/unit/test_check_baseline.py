#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_baseline.py 的单元测试：七项检查的判定与退出码。"""

from __future__ import annotations

from pathlib import Path

import check_baseline


def _make_migration(root: Path) -> None:
    (root / "backend" / "migrations" / "versions").mkdir(parents=True, exist_ok=True)
    (root / "backend" / "alembic.ini").write_text("[alembic]\n", encoding="utf-8")
    (root / "backend" / "migrations" / "versions" / "0001_init.py").write_text("", encoding="utf-8")


def test_missing_migration_is_error(tmp_path: Path) -> None:
    problems = check_baseline.check_schema(tmp_path)
    assert any(level == "error" for level, _ in problems)


def test_alembic_project_passes_schema(tmp_path: Path) -> None:
    _make_migration(tmp_path)
    assert check_baseline.check_schema(tmp_path) == []


def test_create_all_guarded_by_switch_is_info(tmp_path: Path) -> None:
    _make_migration(tmp_path)
    (tmp_path / "backend" / "app").mkdir(parents=True)
    (tmp_path / "backend" / "app" / "main.py").write_text(
        "if settings.AUTO_CREATE_TABLES:\n    Base.metadata.create_all(bind=engine)\n",
        encoding="utf-8",
    )
    levels = [level for level, _ in check_baseline.check_schema(tmp_path)]
    assert "warn" not in levels


def test_index_warns_on_foreign_key_without_index(tmp_path: Path) -> None:
    models = tmp_path / "app" / "models"
    models.mkdir(parents=True)
    (models / "doc.py").write_text(
        'id = Column(Integer, primary_key=True)\n'
        'kb_id = Column(Integer, ForeignKey("kbs.id"), nullable=False, comment="知识库")\n',
        encoding="utf-8",
    )
    problems = check_baseline.check_index(tmp_path)
    assert any(level == "warn" for level, _ in problems)


def test_index_ok_when_indexed(tmp_path: Path) -> None:
    models = tmp_path / "app" / "models"
    models.mkdir(parents=True)
    (models / "doc.py").write_text(
        'kb_id = Column(Integer, ForeignKey("kbs.id"), nullable=False, index=True)\n'
        'Index("ix_kb_created", "kb_id", "created_at")\n',
        encoding="utf-8",
    )
    levels = [level for level, _ in check_baseline.check_index(tmp_path)]
    assert "warn" not in levels


def test_private_detects_tracked_env(tmp_path: Path, monkeypatch) -> None:
    class _Result:
        returncode = 0
        stdout = "README.md\nbackend/.env\n"

    monkeypatch.setattr(check_baseline.subprocess, "run", lambda *a, **k: _Result())
    problems = check_baseline.check_private(tmp_path)
    assert any(level == "error" for level, _ in problems)


def test_dead_config_is_reported(tmp_path: Path) -> None:
    (tmp_path / "app").mkdir()
    (tmp_path / "app" / "config.py").write_text("UNUSED_FLAG: bool = True\n", encoding="utf-8")
    (tmp_path / "app" / "main.py").write_text("print('hi')\n", encoding="utf-8")

    problems = check_baseline.check_deadconfig(tmp_path)
    assert any("UNUSED_FLAG" in message for _, message in problems)


def test_main_returns_error_on_empty_project(tmp_path: Path, monkeypatch) -> None:
    import sys

    monkeypatch.setattr(sys, "argv", ["check_baseline.py", "--root", str(tmp_path)])
    assert check_baseline.main() == 1
