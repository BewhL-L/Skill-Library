#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pytest 配置文件
提供共享的 fixture 和配置
"""

import pytest
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture
def project_root():
    """返回项目根目录"""
    return PROJECT_ROOT


@pytest.fixture
def temp_dir(tmp_path):
    """创建临时目录"""
    return tmp_path


@pytest.fixture
def sample_data():
    """提供示例数据"""
    return {
        "name": "test",
        "version": "1.0.0",
        "items": [1, 2, 3]
    }


def pytest_configure(config):
    """pytest 配置钩子"""
    config.addinivalue_line("markers", "slow: 标记慢速测试")
    config.addinivalue_line("markers", "integration: 标记集成测试")
    config.addinivalue_line("markers", "unit: 标记单元测试")
