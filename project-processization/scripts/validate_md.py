#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate_md.py — 学习指南 Markdown 结构校验器（"项目流程化" Skill 核心工具）

作用：在生成/增补学习指南后，用"代码围栏状态机"做可靠的结构校验，避免朴素正则
把代码块里的 ``#`` 注释误判成标题。检查：
  1. Frontmatter 是否以 --- 开始并正确闭合（可选，--require-frontmatter 时强制）
  2. 代码围栏 ``` 是否成对闭合（偶数，且不跨文档悬空）
  3. 标题层级：恰好 1 个 H1；不允许跳级（如 H1 后直接 H3）
  4. 表格列数是否一致（表头/分隔行/数据行；自动忽略转义 \\| 与双链 [[...]]）
  5. 双链格式：禁止 [[|文字]]（目标为空）
  6. 输出 H1-H6 计数与问题清单；有问题时退出码为 1

用法：
  python validate_md.py --path README.md
  python validate_md.py --path README.md --require-frontmatter --json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def split_frontmatter(text: str) -> Tuple[Optional[str], str]:
    """拆分 YAML frontmatter 与正文。

    Returns:
        (frontmatter, body)。文档不以 ``---`` 开头时返回 (None, 全文)。
    """
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            fm = text[3:end]
            body = text[end + 4:]
            return fm, body
    return None, text


def collect_headings(body: str) -> List[Tuple[int, int, str]]:
    """用代码围栏状态机收集围栏外的标题。

    Returns:
        [(行号, 层级, 标题文本), ...]，层级为 # 的数量。
    """
    headings: List[Tuple[int, int, str]] = []
    in_code = False
    for idx, line in enumerate(body.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_code = not in_code
            continue
        if in_code:
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            headings.append((idx, len(m.group(1)), m.group(2).strip()))
    return headings


def check_fences(body: str) -> List[Dict[str, Any]]:
    """检查代码围栏是否成对闭合，返回问题列表。"""
    issues: List[Dict[str, Any]] = []
    fence_count = 0
    in_code = False
    for idx, line in enumerate(body.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            fence_count += 1
            in_code = not in_code
    if fence_count % 2 != 0:
        issues.append({"severity": "high", "line": 0,
                       "message": f"代码围栏数量为奇数（{fence_count}），存在未闭合的 ``` 块"})
    if in_code:
        issues.append({"severity": "high", "line": 0,
                       "message": "文档结束时仍处于代码块内，最后一个围栏未闭合"})
    return issues


def check_heading_hierarchy(headings: List[Tuple[int, int, str]]) -> List[Dict[str, Any]]:
    """检查 H1 唯一性与层级跳跃。"""
    issues: List[Dict[str, Any]] = []
    h1 = [h for h in headings if h[1] == 1]
    if len(h1) != 1:
        issues.append({"severity": "high", "line": h1[0][0] if h1 else 0,
                       "message": f"应恰好有 1 个 H1，实际 {len(h1)} 个"})
    prev = 0
    for line_no, level, title in headings:
        if prev and level > prev + 1:
            issues.append({"severity": "medium", "line": line_no,
                           "message": f"标题层级跳跃：H{prev} 后直接出现 H{level}（{title}）"})
        prev = level
    return issues


def _clean_table_pipes(line: str) -> str:
    """移除转义 \\| 与双链 [[...]] 内部，避免干扰列数统计。"""
    cleaned = line.replace("\\|", "")
    cleaned = re.sub(r"\[\[[^\]]*\]\]", "[[]]", cleaned)
    return cleaned


def check_tables(body: str) -> List[Dict[str, Any]]:
    """检查每个表格的数据行列数是否与表头一致（含分隔行校验）。"""
    issues: List[Dict[str, Any]] = []
    in_code = False
    in_table = False
    expected_cols = 0
    for idx, line in enumerate(body.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_code = not in_code
            in_table = False
            continue
        if in_code:
            continue
        is_table_row = stripped.startswith("|") and stripped.endswith("|")
        is_separator = bool(re.match(r"^\|[\s\-:|]+\|$", stripped))
        if not in_table:
            if is_table_row and not is_separator:
                in_table = True
                expected_cols = _clean_table_pipes(stripped).count("|") - 1
        else:
            if is_separator:
                if expected_cols and stripped.count("|") - 1 != expected_cols:
                    issues.append({"severity": "medium", "line": idx,
                                   "message": "表格分隔行列数与表头不一致"})
                continue
            if is_table_row:
                actual = _clean_table_pipes(stripped).count("|") - 1
                if expected_cols and actual != expected_cols:
                    issues.append({"severity": "medium", "line": idx,
                                   "message": f"表格列数不匹配：该行 {actual} 列，表头 {expected_cols} 列"})
            elif stripped == "":
                in_table = False
    return issues


def check_wikilinks(body: str) -> List[Dict[str, Any]]:
    """检查空目标双链 [[|文字]]。"""
    issues: List[Dict[str, Any]] = []
    for m in re.finditer(r"\[\[\s*\|[^\]]+\]\]", body):
        line_no = body[:m.start()].count("\n") + 1
        issues.append({"severity": "high", "line": line_no,
                       "message": "存在空目标双链 [[|文字]]，请补全目标页"})
    return issues


def validate(path: Path, require_frontmatter: bool) -> Dict[str, Any]:
    """执行全部校验，返回结构化结果。"""
    text = path.read_text(encoding="utf-8", errors="ignore")
    frontmatter, body = split_frontmatter(text)
    headings = collect_headings(body)
    issues: List[Dict[str, Any]] = []

    if require_frontmatter and frontmatter is None:
        issues.append({"severity": "high", "line": 0, "message": "缺少 YAML frontmatter（应以 --- 开头）"})
    if frontmatter is not None:
        if not re.search(r"^title\s*:", frontmatter, re.M):
            issues.append({"severity": "low", "line": 0, "message": "frontmatter 建议包含 title 字段"})

    issues.extend(check_fences(body))
    issues.extend(check_heading_hierarchy(headings))
    issues.extend(check_tables(body))
    issues.extend(check_wikilinks(body))

    counts = {f"H{i}": sum(1 for h in headings if h[1] == i) for i in range(1, 7)}
    fences = sum(1 for line in body.splitlines() if line.strip().startswith("```"))
    return {
        "path": str(path),
        "ok": not issues,
        "heading_counts": counts,
        "fence_count": fences,
        "issues": issues,
    }


def print_report(result: Dict[str, Any]) -> None:
    """打印人类可读校验报告。"""
    print("=" * 60)
    print(f"校验文件: {result['path']}")
    print(f"标题计数: {result['heading_counts']}；围栏数: {result['fence_count']}")
    if result["ok"]:
        print("✅ 结构校验全部通过")
    else:
        print(f"❌ 发现 {len(result['issues'])} 个问题：")
        for i, issue in enumerate(result["issues"], 1):
            loc = f"行{issue['line']} " if issue.get("line") else ""
            print(f"  {i}. [{issue['severity']}] {loc}{issue['message']}")


def main() -> int:
    """命令行入口。"""
    parser = argparse.ArgumentParser(description="学习指南 Markdown 结构校验器")
    parser.add_argument("--path", required=True, help="待校验的 Markdown 文件")
    parser.add_argument("--require-frontmatter", action="store_true",
                        help="强制要求 YAML frontmatter")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    args = parser.parse_args()

    path = Path(args.path)
    if not path.exists():
        print(f"❌ 文件不存在: {path}", file=sys.stderr)
        return 2
    try:
        result = validate(path, args.require_frontmatter)
    except OSError as exc:
        print(f"❌ 读取失败: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_report(result)
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
