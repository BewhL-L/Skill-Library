#!/usr/bin/env python3
"""检查一个 Skill 在各 agent 安装位上是否存在"另一份副本"，以及它是否已经过期。

背景：
    Skill 通常存在两份——你编辑的源码目录，和 agent 实际加载的安装目录
    （如 ~/.workbuddy/skills/<name>）。改源码不会影响副本，于是出现
    "改了却没生效"。本脚本只做诊断，不修改任何文件。

判定：
    LINKED   安装位是指向源码的链接（junction / symlink），且目标正确
    MISMATCH 是链接，但指向别处
    IN_SYNC  是实体目录，内容与源码逐文件一致
    STALE    是实体目录，内容与源码不同（列出差异文件）
    ABSENT   该 root 下没有这个 skill

用法：
    python check-install-sync.py                  # 检查当前目录
    python check-install-sync.py ../hermes-portability
    python check-install-sync.py --json
    python check-install-sync.py --roots ~/some-agent/skills

退出码：0 全部正常（LINKED/IN_SYNC/无安装）；1 存在 MISMATCH 或 STALE。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

SKIP_DIRS = {"__pycache__", ".git", "node_modules", ".venv", "venv"}

# 由 agent / 安装器写入、不属于 Skill 内容的元数据，比较时忽略。
IGNORE_FILES = {"_user_meta.json", ".install-metadata.json", ".install-metadata.json.lock"}

# 已知的 agent 技能根目录（相对用户主目录）；不存在则跳过。
KNOWN_ROOTS = [
    ".workbuddy/skills",
    ".claude/skills",
    ".codex/skills",
    ".agents/skills",
    ".cc-switch/skills",
    ".cursor/skills",
]


def is_link(path: Path) -> bool:
    if path.is_symlink():
        return True
    checker = getattr(os.path, "isjunction", None)
    if checker is not None:
        try:
            return bool(checker(path))
        except OSError:
            return False
    return False


def link_target(path: Path) -> str:
    try:
        return os.path.realpath(path)
    except OSError:
        return ""


def fingerprint(root: Path) -> dict[str, str]:
    """相对路径 -> 内容摘要；跳过缓存与 VCS 目录。"""
    result: dict[str, str] = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            if name.endswith(".pyc") or name in IGNORE_FILES:
                continue
            full = Path(dirpath) / name
            rel = str(full.relative_to(root)).replace("\\", "/")
            try:
                digest = hashlib.sha256(full.read_bytes()).hexdigest()
            except OSError:
                digest = "unreadable"
            result[rel] = digest
    return result


def diff_summary(a: dict[str, str], b: dict[str, str], limit: int = 5) -> list[str]:
    only_a = sorted(set(a) - set(b))
    only_b = sorted(set(b) - set(a))
    changed = sorted(k for k in set(a) & set(b) if a[k] != b[k])
    lines = []
    for label, items in (("源码独有", only_a), ("副本独有", only_b), ("内容不同", changed)):
        if items:
            shown = ", ".join(items[:limit])
            more = "" if len(items) <= limit else f" …共 {len(items)} 个"
            lines.append(f"{label}: {shown}{more}")
    return lines


def discover_roots(extra: list[str]) -> list[Path]:
    home = Path.home()
    roots: list[Path] = []
    for rel in KNOWN_ROOTS:
        p = home / rel
        if p.is_dir():
            roots.append(p)
    # 自动发现：~/<任意目录>/skills
    try:
        for child in home.iterdir():
            if not child.is_dir():
                continue
            cand = child / "skills"
            if cand.is_dir():
                roots.append(cand)
    except OSError:
        pass
    for item in extra:
        p = Path(item).expanduser()
        if p.is_dir():
            roots.append(p)
    # 去重并保持稳定顺序
    seen: set[str] = set()
    unique: list[Path] = []
    for r in roots:
        key = os.path.realpath(r)
        if key not in seen:
            seen.add(key)
            unique.append(r)
    return unique


def check(skill_dir: Path, roots: list[Path]) -> list[dict]:
    name = skill_dir.name
    src_real = os.path.realpath(skill_dir)
    src_fp = None
    rows: list[dict] = []

    for root in roots:
        target = root / name
        if not target.exists() and not is_link(target):
            rows.append({"root": str(root), "status": "ABSENT", "detail": ""})
            continue
        if is_link(target):
            tgt = link_target(target)
            if tgt and os.path.normcase(tgt) == os.path.normcase(src_real):
                rows.append({"root": str(root), "status": "LINKED", "detail": tgt})
            else:
                rows.append({"root": str(root), "status": "MISMATCH", "detail": f"指向 {tgt or '<未知>'}"})
            continue
        if src_fp is None:
            src_fp = fingerprint(skill_dir)
        dst_fp = fingerprint(target)
        if dst_fp == src_fp:
            rows.append({"root": str(root), "status": "IN_SYNC", "detail": f"{len(dst_fp)} 个文件一致"})
        else:
            rows.append({"root": str(root), "status": "STALE", "detail": "; ".join(diff_summary(src_fp, dst_fp))})
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description="检查 Skill 安装副本是否与源码一致")
    parser.add_argument("path", nargs="?", default=".", help="Skill 目录（含 SKILL.md）")
    parser.add_argument("--roots", nargs="*", default=[], help="额外的 skills 根目录")
    parser.add_argument("--json", action="store_true", help="以 JSON 输出")
    args = parser.parse_args()

    skill_dir = Path(args.path).expanduser().resolve()
    if not (skill_dir / "SKILL.md").is_file():
        print(f"跳过：{skill_dir} 下没有 SKILL.md")
        return 2

    roots = discover_roots(args.roots)
    rows = check(skill_dir, roots)

    problems = [r for r in rows if r["status"] in {"STALE", "MISMATCH"}]
    installed = [r for r in rows if r["status"] != "ABSENT"]

    if args.json:
        print(json.dumps({"skill": str(skill_dir), "rows": rows, "problems": len(problems)},
                         ensure_ascii=False, indent=2))
    else:
        print(f"Skill: {skill_dir.name}   ({skill_dir})")
        print(f"扫描 {len(roots)} 个 skills 根目录，命中 {len(installed)} 处安装\n")
        for r in rows:
            if r["status"] == "ABSENT":
                continue
            print(f"  [{r['status']:<8}] {r['root']}")
            if r["detail"]:
                print(f"             {r['detail']}")
        if not installed:
            print("  未在任何 agent 目录发现该 Skill（无需处理）")
        if problems:
            print("\n修复建议：")
            print("  Windows : powershell -NoProfile -File <skill>/scripts/link-skill.ps1")
            print("  Linux   : ln -sfn <源码目录> <安装位>")
            print("  （link-skill.ps1 会把实体副本移到 %LOCALAPPDATA%\\SkillLinkBackups 后建 junction）")

    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
