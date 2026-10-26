#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI 命令集成测试
测试所有命令行命令
"""

import pytest
import subprocess
import sys
from pathlib import Path


def run_command(*args):
    """运行命令并返回结果"""
    return subprocess.run(
        [sys.executable, "main.py", *args],
        capture_output=True,
        text=True,
        cwd=str(Path(__file__).parent.parent.parent)
    )


class TestCLI:
    """CLI 命令测试"""

    def test_help(self):
        """测试 --help"""
        result = run_command("--help")
        assert result.returncode == 0

    def test_version(self):
        """测试 --version"""
        result = run_command("--version")
        assert result.returncode == 0

    def test_invalid_command(self):
        """测试无效命令"""
        result = run_command("invalid_command_xyz")
        assert result.returncode != 0

    def test_missing_required_arg(self):
        """测试缺少必需参数"""
        # TODO: 根据实际命令修改
        pass
