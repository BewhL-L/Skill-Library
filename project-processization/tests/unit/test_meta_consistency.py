#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Skill 自身的一致性：版本号、引用链接、脚本数量。

这三项都曾靠人工同步而漏改（v1.0.0 没跟上、模板还指着旧文件），
所以用测试兜住：改了 CHANGELOG 忘改页脚、删了文件忘改引用，都会红。
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")
CHANGELOG = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")


def test_footer_version_matches_changelog() -> None:
    """页脚版本必须等于 CHANGELOG 的第一条（最新）版本。"""
    footer = re.search(r"版本：v(\d+\.\d+\.\d+)", SKILL)
    latest = re.search(r"^## v(\d+\.\d+\.\d+)", CHANGELOG, re.M)

    assert footer, "SKILL.md 页脚缺少 `版本：vX.Y.Z`"
    assert latest, "CHANGELOG.md 缺少 `## vX.Y.Z` 条目"
    assert footer.group(1) == latest.group(1), (
        f"页脚 v{footer.group(1)} 与 CHANGELOG 最新 v{latest.group(1)} 不一致"
    )


def test_referenced_files_exist() -> None:
    """SKILL.md 里反引号引用的 references/scripts/templates 路径必须存在。"""
    paths = set(re.findall(r"`((?:references|scripts|templates)/[^`\s]+)`", SKILL))
    assert paths, "没有解析到任何引用路径，检查正则是否失效"

    missing = [rel for rel in paths if not (ROOT / rel).exists()]
    assert not missing, f"引用了不存在的文件：{missing}"


def test_script_count_in_footer() -> None:
    """页脚声明的脚本数量必须等于 scripts/ 下的实际 CLI 数（排除 __init__.py）。"""
    match = re.search(r"scripts/ 下 (\d+) 个纯标准库 CLI", SKILL)
    assert match, "页脚缺少脚本数量声明"

    actual = len([
        p for p in (ROOT / "scripts").glob("*.py") if p.name != "__init__.py"
    ])
    assert int(match.group(1)) == actual, (
        f"页脚写 {match.group(1)} 个脚本，实际 {actual} 个"
    )
