#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""scan_project_facts.py 的单元测试（基于 conftest 的样例项目）。"""

from __future__ import annotations

from pathlib import Path

import scan_project_facts as scan


def test_counts_files_and_lines(sample_project: Path) -> None:
    """样例项目：4 个 Python 文件、1 个前端文件。"""
    data = scan.scan(sample_project, [])
    assert data["code"]["python"]["files"] == 4
    assert data["code"]["frontend"]["files"] == 1


def test_test_functions_count(sample_project: Path) -> None:
    """测试函数识别：2 个 def test_。"""
    all_files = list(scan.iter_code_files(
        sample_project, {".py"}, scan.DEFAULT_EXCLUDE))
    result = scan.count_test_functions(all_files)
    assert result["files"] == 1
    assert result["functions"] == 2


def test_component_dir_excludes_init(sample_project: Path) -> None:
    """routers 业务文件数应排除 __init__.py，得 1。"""
    comps = scan.list_component_dirs(sample_project, ["backend/app/routers"])
    assert comps["backend/app/routers"]["exists"] is True
    assert comps["backend/app/routers"]["file_count"] == 1
    assert comps["backend/app/routers"]["init_files"] == 1


def test_docker_services(sample_project: Path) -> None:
    """提取 docker-compose 服务名。"""
    services = scan.parse_docker_services(sample_project)
    assert set(services) == {"postgres", "backend"}


def test_env_keys_without_values(sample_project: Path) -> None:
    """只提取键名，不泄露密钥值。"""
    keys = scan.parse_env_keys(sample_project / "backend")
    assert "LLM_API_KEY" in keys
    assert "DATABASE_URL" in keys


def test_requirements(sample_project: Path) -> None:
    """requirements 包名去掉版本约束。"""
    pkgs = scan.parse_requirements(sample_project)
    assert "fastapi" in pkgs
    assert "uvicorn" in pkgs


def test_group_depth_two(sample_project: Path) -> None:
    """二级分组应区分 app 与 tests。"""
    py_files = list(scan.iter_code_files(sample_project, {".py"}, scan.DEFAULT_EXCLUDE))
    groups = scan.group_by_topdir(py_files, sample_project, depth=2)
    assert "backend/app" in groups
    assert "backend/tests" in groups
