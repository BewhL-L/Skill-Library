#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_toc.py — 学习指南折叠目录（TOC）生成器（"项目流程化" Skill 核心工具）

作用：为长篇学习指南生成"可点击跳转"的 Markdown 目录，锚点采用 GitHub 标准 slug
算法（与 GitHub / Obsidian 阅读视图一致）。用代码围栏状态机跳过 ``` 内的 # 注释，
避免把 bash 注释误识别为标题。

GitHub slug 规则（已在真实文档上与手写锚点交叉验证）：
  1) 转小写；2) 移除标点（保留字母/数字/中文/空白/连字符）；3) 每个空白转一个连字符
  （注意：连续空格不合并，会产生连续连字符，如 "a + b" -> "a--b"）。

用法：
  # 打印 H3-H4 的目录
  python make_toc.py --path README.md --levels 3-4
  # 限定从某个标题到某个标题之间（如只生成"学习指南"部分），并包成折叠块
  python make_toc.py --path README.md --start "🎓 从零到专家" --end "License" \
      --levels 3-4 --details --title "学习指南目录"
  # 直接写回（插入到 --insert-after 标题之后）
  python make_toc.py --path README.md --levels 3-4 --details --insert-after "学习指南（AI 协作版）" --write
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import List, Optional, Tuple


def github_slug(title: str) -> str:
    """按 GitHub 规则生成标题锚点 slug。"""
    s = title.strip().lower()
    # 移除标点，保留字母数字、下划线、中文、空白、连字符
    s = re.sub(r"[^\w\s\u4e00-\u9fff\-]", "", s)
    s = s.strip()
    # 每个空白 -> 一个连字符（不合并连续连字符）
    s = re.sub(r"\s", "-", s)
    return s


def collect_headings(text: str, start: Optional[str] = None,
                     end: Optional[str] = None) -> List[Tuple[int, str]]:
    """用围栏状态机收集指定区间内的标题，返回 [(层级, 标题文本)]。

    Args:
        text: 完整 Markdown 文本。
        start: 区间起始标题需包含的子串（含该标题）；None 表示从头。
        end: 区间结束标题需包含的子串（不含该标题）；None 表示到末尾。
    """
    lines = text.splitlines()
    begin_idx = 0
    end_idx = len(lines)
    if start:
        for i, line in enumerate(lines):
            if re.match(r"^#{1,6}\s", line) and start in line:
                begin_idx = i
                break
    if end:
        for i in range(begin_idx + 1, len(lines)):
            line = lines[i]
            if re.match(r"^#{1,6}\s", line) and end in line:
                end_idx = i
                break

    headings: List[Tuple[int, str]] = []
    in_code = False
    for i in range(begin_idx, end_idx):
        line = lines[i]
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_code = not in_code
            continue
        if in_code:
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            headings.append((len(m.group(1)), m.group(2).strip()))
    return headings


def parse_levels(spec: str) -> Tuple[int, int]:
    """解析 '3-4' 或 '2' 形式的层级范围。"""
    if "-" in spec:
        lo, hi = spec.split("-", 1)
        return int(lo), int(hi)
    n = int(spec)
    return n, n


def build_toc(headings: List[Tuple[int, str]], min_level: int, max_level: int,
              base_level: Optional[int] = None) -> str:
    """根据标题列表生成 Markdown 列表目录。

    Args:
        base_level: 用于缩进归零的基准层级；默认取区间内最小层级。
    """
    selected = [(lv, t) for lv, t in headings if min_level <= lv <= max_level]
    if not selected:
        return ""
    if base_level is None:
        base_level = min(lv for lv, _ in selected)
    out: List[str] = []
    for lv, title in selected:
        indent = "  " * (lv - base_level)
        out.append(f"{indent}- [{title}](#{github_slug(title)})")
    return "\n".join(out)


def wrap_details(toc: str, title: str) -> str:
    """把目录包进 <details> 折叠块。"""
    return f"<details>\n<summary>{title}</summary>\n\n{toc}\n\n</details>"


def main() -> int:
    """命令行入口。"""
    parser = argparse.ArgumentParser(description="学习指南折叠目录生成器（GitHub slug）")
    parser.add_argument("--path", required=True, help="Markdown 文件路径")
    parser.add_argument("--levels", default="3-4", help="标题层级范围，如 2-4 或 3")
    parser.add_argument("--start", help="区间起始标题包含的子串")
    parser.add_argument("--end", help="区间结束标题包含的子串（不含）")
    parser.add_argument("--details", action="store_true", help="用 <details> 折叠")
    parser.add_argument("--title", default="目录（点击展开）", help="折叠块标题")
    parser.add_argument("--insert-after", help="写回时插入到该标题之后（标题包含子串）")
    parser.add_argument("--write", action="store_true", help="直接写回原文件")
    parser.add_argument("--output", help="输出到指定文件")
    args = parser.parse_args()

    path = Path(args.path)
    if not path.exists():
        print(f"❌ 文件不存在: {path}", file=sys.stderr)
        return 2
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"❌ 读取失败: {exc}", file=sys.stderr)
        return 1

    min_level, max_level = parse_levels(args.levels)
    headings = collect_headings(text, args.start, args.end)
    toc = build_toc(headings, min_level, max_level)
    if not toc:
        print("⚠️ 指定区间/层级内没有标题", file=sys.stderr)
        return 1
    if args.details:
        toc = wrap_details(toc, args.title)

    if args.write:
        if not args.insert_after:
            print("❌ --write 需配合 --insert-after 使用", file=sys.stderr)
            return 2
        pattern = re.compile(r"(^#{1,6}.*" + re.escape(args.insert_after) + r".*$)", re.M)
        if not pattern.search(text):
            print(f"❌ 未找到插入锚点标题: {args.insert_after}", file=sys.stderr)
            return 2
        new_text = pattern.sub(lambda m: m.group(1) + "\n\n" + toc, text, count=1)
        path.write_text(new_text, encoding="utf-8")
        print(f"已将目录插入到「{args.insert_after}」之后并写回 {path}")
        return 0

    if args.output:
        Path(args.output).write_text(toc + "\n", encoding="utf-8")
        print(f"已写入 {args.output}")
    else:
        print(toc)
    return 0


if __name__ == "__main__":
    sys.exit(main())
