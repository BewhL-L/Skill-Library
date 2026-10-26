#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pytest 公共夹具：把 scripts 目录加入导入路径，并提供临时样例项目。"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from _pytest.fixtures import FixtureRequest  # noqa: F401

SKILL_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = SKILL_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))


@pytest.fixture()
def sample_project(tmp_path: Path) -> Path:
    """构造一个最小样例项目：含后端 app/tests、前端、.env、docker-compose。"""
    # 后端业务代码
    (tmp_path / "backend" / "app" / "routers").mkdir(parents=True)
    (tmp_path / "backend" / "app" / "routers").joinpath("__init__.py").write_text("", encoding="utf-8")
    (tmp_path / "backend" / "app" / "routers").joinpath("user.py").write_text(
        "def get_user():\n    return 1\n", encoding="utf-8")
    (tmp_path / "backend" / "app").joinpath("config.py").write_text(
        "CHUNK_SIZE = 500\nTOP_K = 5\n", encoding="utf-8")
    # 测试代码
    (tmp_path / "backend" / "tests").mkdir(parents=True)
    (tmp_path / "backend" / "tests").joinpath("test_user.py").write_text(
        "def test_get_user():\n    assert True\n\n"
        "def test_other():\n    assert 1 == 1\n", encoding="utf-8")
    # 前端
    (tmp_path / "frontend" / "src" / "views").mkdir(parents=True)
    (tmp_path / "frontend" / "src" / "views").joinpath("Home.vue").write_text(
        "<template><div>home</div></template>\n", encoding="utf-8")
    # 配置
    (tmp_path / "backend").joinpath(".env").write_text(
        "LLM_API_KEY=sk-secret\nDATABASE_URL=postgres://x\n", encoding="utf-8")
    (tmp_path / "backend").joinpath("requirements.txt").write_text(
        "fastapi==0.1\nuvicorn>=0.1\n", encoding="utf-8")
    (tmp_path).joinpath("docker-compose.yml").write_text(
        "services:\n  postgres:\n    image: x\n  backend:\n    image: y\n",
        encoding="utf-8")
    return tmp_path
