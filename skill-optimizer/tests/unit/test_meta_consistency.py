#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skill 自身元数据一致性测试

页脚版本/日期必须与 CHANGELOG 最新条目对齐：
- 改了 SKILL.md / references 忘更 CHANGELOG -> 页脚版本落后 -> 红
- 更了 CHANGELOG 忘更页脚 -> 同样红
（1.9.0/1.9.1 发布时页脚停在 v1.8.1 两个版本没人发现，正是缺这个测试）
"""

import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SKILL = (PROJECT_ROOT / "SKILL.md").read_text(encoding="utf-8")
CHANGELOG = (PROJECT_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")


def test_footer_version_matches_changelog() -> None:
    """页脚 `**版本**：vX.Y.Z` 必须等于 CHANGELOG 的第一条（最新）版本。"""
    footer = re.search(r"\*\*版本\*\*：v(\d+\.\d+\.\d+)", SKILL)
    latest = re.search(r"^## \[(\d+\.\d+\.\d+)\]", CHANGELOG, re.MULTILINE)
    assert footer, "SKILL.md 页脚缺少 `**版本**：vX.Y.Z`"
    assert latest, "CHANGELOG.md 缺少 `## [X.Y.Z]` 条目"
    assert footer.group(1) == latest.group(1), (
        f"页脚 v{footer.group(1)} 与 CHANGELOG 最新 v{latest.group(1)} 不一致"
        f"（改完内容忘了升页脚，或更了 CHANGELOG 忘了页脚）"
    )


def test_footer_date_not_older_than_changelog() -> None:
    """页脚"最后更新"日期不得早于 CHANGELOG 最新条目的日期。"""
    footer = re.search(r"\*\*最后更新\*\*：(\d{4}-\d{2}-\d{2})", SKILL)
    latest = re.search(
        r"^## \[\d+\.\d+\.\d+\] - (\d{4}-\d{2}-\d{2})", CHANGELOG, re.MULTILINE
    )
    assert footer, "SKILL.md 页脚缺少 `**最后更新**：YYYY-MM-DD`"
    assert latest, "CHANGELOG.md 最新条目缺少 `- YYYY-MM-DD` 日期"
    assert footer.group(1) >= latest.group(1), (
        f"页脚日期 {footer.group(1)} 早于 CHANGELOG 最新条目 {latest.group(1)}"
        f"（CHANGELOG 更了、页脚没跟着走）"
    )
