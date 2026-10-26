#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""make_toc.py 的单元测试。"""

from __future__ import annotations

import make_toc


def test_slug_basic() -> None:
    """普通标题转小写、空格转连字符。"""
    assert make_toc.github_slug("Hello World") == "hello-world"


def test_slug_removes_punctuation_keeps_chinese() -> None:
    """中文保留，标点移除。"""
    assert make_toc.github_slug("5.1 启动项目（推荐 Docker）") == "51-启动项目推荐-docker"


def test_slug_double_space_keeps_double_hyphen() -> None:
    """含 ' + ' 的标题删除加号后产生连续空格，按 GitHub 规则保留双连字符。"""
    assert make_toc.github_slug("阶段 3：编排 + 生产化") == "阶段-3编排--生产化"


def test_collect_headings_skips_code_fence() -> None:
    """代码围栏内的 # 注释不应被当作标题。"""
    text = "# 真标题\n\n```bash\n# 这是注释\n```\n\n## 二级\n"
    headings = make_toc.collect_headings(text)
    titles = [t for _, t in headings]
    assert titles == ["真标题", "二级"]


def test_build_toc_indent_and_anchor() -> None:
    """生成的目录包含层级缩进与正确锚点。"""
    headings = [(3, "一、概述"), (4, "1.1 细节")]
    toc = make_toc.build_toc(headings, 3, 4)
    assert "- [一、概述](#一概述)" in toc
    assert "  - [1.1 细节](#11-细节)" in toc
