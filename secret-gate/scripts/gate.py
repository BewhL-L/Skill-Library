#!/usr/bin/env python3
"""gate —— 提交前的敏感内容闸门（stdlib，无第三方依赖）。

用途：
    在 `git commit` 之前检查即将入库的内容，拦住"不该进版本库"的东西：
    密钥、私钥、连接串、私密文档、依赖目录、超大文件。

三种模式：
    --staged  只检查暂存区（pre-commit 钩子用这个）
    --all     检查所有已跟踪文件（体检用）
    <path>    检查指定文件或目录（默认当前目录，递归）

退出码：
    0  通过
    1  发现违规（有输出）
    2  用法错误 / 不在 git 仓库

用法：
    python gate.py --staged
    python gate.py --all --json
    python gate.py ../some-repo --all
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import subprocess
import sys
from pathlib import Path

DEFAULT_RULES = Path(__file__).resolve().parent.parent / "rules.json"

BINARY_EXT = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".bmp", ".pdf", ".zip",
    ".gz", ".7z", ".rar", ".mp4", ".mp3", ".wav", ".woff", ".woff2", ".ttf",
    ".otf", ".glb", ".gltf", ".pkl", ".npy", ".so", ".dll", ".exe", ".pyc",
}


def git(args: list[str], cwd: Path) -> tuple[int, str]:
    """在仓库内执行 git，返回 (退出码, 合并后的输出)。"""
    proc = subprocess.run(["git", "-C", str(cwd), *args], capture_output=True, text=True,
                          encoding="utf-8", errors="replace")
    return proc.returncode, (proc.stdout or "").strip()


def load_rules(path: Path) -> dict:
    """读取规则文件，补齐缺失字段的默认值。"""
    with path.open(encoding="utf-8") as handle:
        rules = json.load(handle)
    rules.setdefault("deny_paths", [])
    rules.setdefault("content", [])
    rules.setdefault("allow", [])
    rules.setdefault("max_file_bytes", 5 * 1024 * 1024)
    return rules


def collect_files(mode: str, root: Path) -> list[Path]:
    """按模式收集待扫描文件：staged / all / 目录递归。"""
    if mode in ("staged", "all"):
        flag = ["diff", "--cached", "--name-only"] if mode == "staged" else ["ls-files"]
        code, out = git(flag, root)
        if code != 0:
            raise SystemExit(f"gate: 不是 git 仓库或 git 调用失败：{root}")
        return [root / line for line in out.splitlines() if line.strip()]
    target = Path(mode)
    if target.is_file():
        return [target]
    return [p for p in target.rglob("*") if p.is_file()]


def is_allowed(rel: str, allow: list[str]) -> bool:
    """路径是否命中 allow 白名单（glob）。"""
    return any(fnmatch.fnmatch(rel, pattern) for pattern in allow)


def scan(root: Path, files: list[Path], rules: dict) -> list[dict]:
    """按 路径规则 → 体积 → 内容规则 的顺序扫描，返回 findings 列表。"""
    findings: list[dict] = []
    path_rules = [(r["id"], re.compile(r["pattern"]), r.get("why", "")) for r in rules["deny_paths"]]
    content_rules = [(r["id"], re.compile(r["pattern"]), r.get("why", "")) for r in rules["content"]]

    for path in files:
        try:
            rel = str(path.relative_to(root)).replace("\\", "/")
        except ValueError:
            rel = path.name
        if is_allowed(rel, rules["allow"]):
            continue

        for rule_id, rx, why in path_rules:
            if rx.search(rel):
                findings.append({"file": rel, "line": 0, "rule": rule_id, "why": why})

        if path.suffix.lower() in BINARY_EXT:
            continue
        try:
            size = path.stat().st_size
        except OSError:
            continue
        if size > rules["max_file_bytes"]:
            findings.append({"file": rel, "line": 0, "rule": "file-too-large",
                             "why": f"{size // 1024} KB > {rules['max_file_bytes'] // 1024} KB"})
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue

        for lineno, line in enumerate(text.splitlines(), 1):
            for rule_id, rx, why in content_rules:
                if rx.search(line):
                    findings.append({"file": rel, "line": lineno, "rule": rule_id, "why": why})
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="提交前敏感内容闸门")
    parser.add_argument("path", nargs="?", default=".", help="仓库或目录（默认当前目录）")
    parser.add_argument("--staged", action="store_true", help="只检查暂存区")
    parser.add_argument("--all", action="store_true", help="检查所有已跟踪文件")
    parser.add_argument("--rules", default=str(DEFAULT_RULES), help="规则文件")
    parser.add_argument("--json", action="store_true", help="JSON 输出")
    args = parser.parse_args()

    if args.staged and args.all:
        print("gate: --staged 与 --all 只能二选一", file=sys.stderr)
        return 2

    root = Path(args.path).resolve()
    mode = "staged" if args.staged else ("all" if args.all else str(root))

    rules_path = Path(args.rules)
    if not rules_path.is_file():
        print(f"gate: 找不到规则文件 {rules_path}", file=sys.stderr)
        return 2
    rules = load_rules(rules_path)

    files = collect_files(mode, root)
    findings = scan(root, files, rules)

    if args.json:
        print(json.dumps({"checked": len(files), "findings": findings},
                         ensure_ascii=False, indent=2))
    else:
        if findings:
            print(f"gate: 拦截 {len(findings)} 处（检查 {len(files)} 个文件）", file=sys.stderr)
            for f in findings:
                loc = f"{f['file']}:{f['line']}" if f["line"] else f["file"]
                print(f"  {loc}  [{f['rule']}] {f['why']}", file=sys.stderr)
            print("\n处置：移除该内容，或确认无误后在 rules.json 的 allow 里加白名单。", file=sys.stderr)
        else:
            print(f"gate: 通过（检查 {len(files)} 个文件）")

    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
