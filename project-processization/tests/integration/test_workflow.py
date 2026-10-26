#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""端到端：模拟"原始 README + 增补学习指南"的完整校验流程。"""

from __future__ import annotations

from pathlib import Path

import make_toc
import validate_md
import verify_zero_cut


def test_full_workflow(tmp_path: Path) -> None:
    """零删减增补后的文档：结构校验通过、零删减通过、目录可生成。"""
    original = tmp_path / "README_orig.md"
    original.write_text(
        "# 示例项目\n\n## 项目简介\n\n这是原始内容，必须保留。\n\n## License\n\nMIT\n",
        encoding="utf-8")

    guide = tmp_path / "README.md"
    guide.write_text(
        "---\ntitle: 示例项目\n---\n\n"
        "# 示例项目\n\n"
        "## 项目简介\n\n这是原始内容，必须保留。\n\n"
        "## 🎓 学习指南\n\n"
        "### 一、概述\n\n#### 1.1 背景\n\n背景说明。\n\n"
        "### 二、步骤\n\n#### 2.1 启动\n\n```bash\ndocker compose up\n```\n\n"
        "## License\n\nMIT\n",
        encoding="utf-8")

    # 1) 结构校验
    result = validate_md.validate(guide, require_frontmatter=True)
    assert result["ok"] is True, result["issues"]
    assert result["heading_counts"]["H1"] == 1

    # 2) 零删减
    cut = verify_zero_cut.compare(original, guide)
    assert cut["ok"] is True, cut["missing_details"]

    # 3) 目录生成（学习指南区间，H3-H4）
    headings = make_toc.collect_headings(
        guide.read_text(encoding="utf-8"), start="学习指南", end="License")
    toc = make_toc.build_toc(headings, 3, 4)
    assert "(#一概述)" in toc
    assert "(#11-背景)" in toc


def test_fence_hash_not_false_heading(tmp_path: Path) -> None:
    """bash 注释不影响 H1 计数（状态机）。"""
    doc = tmp_path / "d.md"
    doc.write_text(
        "# 唯一标题\n\n```bash\n# 注释一\n# 注释二\n```\n\n## 二级\n",
        encoding="utf-8")
    result = validate_md.validate(doc, require_frontmatter=False)
    assert result["heading_counts"]["H1"] == 1
    assert result["ok"] is True
