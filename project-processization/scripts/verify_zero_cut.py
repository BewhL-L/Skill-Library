#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_zero_cut.py — 原文零删减比对器（"项目流程化" Skill 核心工具）

作用：在把"AI 生成的原始 README"扩写为"零基础学习指南"后，强制保证原文一行不丢，
新增只能"插入/增强"，不能"删除/改写"。逐行核对原文的每个实质行是否仍存在于新文档：

匹配分三级：
  - exact   归一化空白后与新文档某行完全一致           → 已保留
  - loose   去除所有标点空白后与新文档某行高度相似       → 疑似修改（需人工确认是否有意修正）
  - missing 两级都不命中                                → 疑似删减（默认不允许）

有意修正（如修正测试用例数 47→79）应通过 --allow-note 记录说明，且仅允许极少处；
工具会把 loose 行与 note 一起列出，便于确认"差异是否全部是有意为之"。

用法：
  python verify_zero_cut.py --original README_orig.md --new README.md
  python verify_zero_cut.py --original a.md --new b.md --allow-note "tests 用例数 47→79"
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

# 视为"纯装饰"、不参与内容比对的行
_DECORATION = re.compile(r"^\s*(-{3,}|\*{3,}|_{3,})\s*$")


def normalize_ws(line: str) -> str:
    """去除所有空白字符，用于严格匹配。"""
    return re.sub(r"\s+", "", line)


def normalize_loose(line: str) -> str:
    """去除所有空白与中英文标点，仅保留字母数字与中文，用于宽松相似匹配。"""
    no_ws = normalize_ws(line)
    # 保留：中文、字母、数字；其余全部去掉
    return re.sub(r"[^\w\u4e00-\u9fff]", "", no_ws, flags=re.UNICODE)


def is_substantive(line: str) -> bool:
    """判断是否为需要比对的实质内容行（非空、非纯分隔线、非图片/链接噪声）。"""
    stripped = line.strip()
    if not stripped:
        return False
    if _DECORATION.match(stripped):
        return False
    return True


def compare(original: Path, new: Path) -> Dict[str, Any]:
    """执行逐行比对，返回分级结果。"""
    orig_lines = original.read_text(encoding="utf-8", errors="ignore").splitlines()
    new_lines = new.read_text(encoding="utf-8", errors="ignore").splitlines()

    new_ws = [normalize_ws(l) for l in new_lines]
    new_loose = [normalize_loose(l) for l in new_lines]
    new_ws_set = set(new_ws)
    new_loose_set = set(x for x in new_loose if len(x) >= 4)

    exact: List[str] = []
    loose: List[Dict[str, str]] = []
    missing: List[Dict[str, Any]] = []

    for idx, line in enumerate(orig_lines, 1):
        if not is_substantive(line):
            continue
        ws = normalize_ws(line)
        if ws in new_ws_set:
            exact.append(line)
            continue
        lo = normalize_loose(line)
        # 宽松命中：要求足够长，避免短行误判
        matched = False
        if len(lo) >= 4 and lo in new_loose_set:
            matched = True
            near = next((l for l, n in zip(new_lines, new_loose) if n == lo), "")
            loose.append({"orig_line": idx, "orig": line.strip(), "new": near.strip()})
        if not matched:
            # 再做一次"包含"兜底：原文行是某新行的一部分（常见于被加了前后缀）
            contained = any(len(lo) >= 8 and lo in n for n in new_loose)
            if contained:
                loose.append({"orig_line": idx, "orig": line.strip(),
                              "new": "(被包含于新文档某行，疑似增强)"})
            else:
                missing.append({"orig_line": idx, "text": line.strip()})

    return {
        "original": str(original),
        "new": str(new),
        "substantive_lines": len(exact) + len(loose) + len(missing),
        "exact_kept": len(exact),
        "loose_modified": len(loose),
        "missing": len(missing),
        "loose_details": loose,
        "missing_details": missing,
        "ok": len(missing) == 0,
    }


def print_report(result: Dict[str, Any], allow_note: str) -> int:
    """打印比对报告，返回退出码。"""
    print("=" * 60)
    print("原文零删减比对")
    print("=" * 60)
    total = result["substantive_lines"]
    print(f"原文实质行: {total}")
    print(f"  严格保留: {result['exact_kept']}")
    print(f"  疑似修改: {result['loose_modified']}（需确认是否为有意修正）")
    print(f"  疑似删减: {result['missing']}（默认不允许）")

    if result["loose_details"]:
        print("\n— 疑似修改（请逐行确认）—")
        for d in result["loose_details"]:
            print(f"  原文行{d['orig_line']}: {d['orig']}")
            print(f"      → 新文档: {d['new']}")
    if result["missing_details"]:
        print("\n— 疑似删减（必须处理）—")
        for d in result["missing_details"][:30]:
            print(f"  原文行{d['orig_line']}: {d['text']}")

    if allow_note:
        print(f"\n已声明的有意修正说明: {allow_note}")

    if result["ok"]:
        print("\n✅ 无删减：原文所有实质行均已保留（疑似修改项请人工确认）")
        return 0
    print("\n❌ 存在疑似删减，请补回或显式说明修改理由")
    return 1


def main() -> int:
    """命令行入口。"""
    parser = argparse.ArgumentParser(description="原文零删减比对器")
    parser.add_argument("--original", required=True, help="原始文档路径")
    parser.add_argument("--new", required=True, help="增补后的新文档路径")
    parser.add_argument("--allow-note", default="", help="本次有意修正的说明（一句话）")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    args = parser.parse_args()

    original = Path(args.original)
    new = Path(args.new)
    if not original.exists() or not new.exists():
        print("❌ 原始或新文档路径不存在", file=sys.stderr)
        return 2
    try:
        result = compare(original, new)
    except OSError as exc:
        print(f"❌ 比对失败: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["ok"] else 1
    return print_report(result, args.allow_note)


if __name__ == "__main__":
    sys.exit(main())
