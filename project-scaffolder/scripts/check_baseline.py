#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_baseline.py — 工程底座自检（"项目脚手架" Skill 核心工具）

作用：把 SKILL.md 第六步第 12 维「工程底座与文档一致性」从清单变成可执行断言。
七项检查，出错即非零退出，可接 CI；警告项默认不阻断（--strict 时阻断）。

  1. schema      版本化迁移：有 alembic/prisma/rails 迁移体系、版本文件非空、
                 应用代码不再依赖 create_all
  2. index       索引：SQLAlchemy 外键列是否带 index=True、是否有复合索引声明
  3. ci          质量门：workflow 存在且覆盖 lint/test/build；测试命令是否误用 console script
  4. docs        文档断言：check_docs.py 是否存在、是否接进 CI
  5. private     私有边界：git 是否跟踪 .env / 私有文档 / 数据库文件；.gitignore 是否覆盖
  6. defaults    默认安全：AUTO_CREATE_TABLES / A2A_ENABLED 默认值、令牌是否常量时间比较
  7. deadconfig  假完备：只定义不读取的配置项、未实现的 TODO/NotImplemented

适用范围：schema / ci / docs / private 与语言无关；
          index / defaults / deadconfig 依赖 Python 特征（SQLAlchemy 模型、config.py），
          非 Python 项目会输出"跳过：未发现 …"——"跳过"不等于"通过"。

用法：
  python scripts/check_baseline.py --root .
  python scripts/check_baseline.py --root . --strict --json
  python scripts/check_baseline.py --root . --skip index,deadconfig
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

SKIP_DIRS = {
    ".git", "node_modules", ".venv", "venv", "dist", "build", "__pycache__",
    ".mypy_cache", ".pytest_cache", ".next", ".nuxt", "coverage",
}
MIGRATION_HINTS = ("alembic.ini", "migrations", "prisma/schema.prisma", "db/migrate")
FK_COLUMN = re.compile(r"Column\s*\(")
CONFIG_ASSIGN = re.compile(r"^([A-Z][A-Z0-9_]{2,})\s*[:=]", re.M)


def walk_files(root: Path, suffixes=(".py",)):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            if name.endswith(suffixes):
                yield Path(dirpath) / name


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


# ---------------- 1. schema ----------------

def _migration_base(root: Path):
    """迁移体系可能在仓库根，也可能在 backend/ server/ 这类子目录下"""
    candidates = [root] + [
        p for p in root.iterdir() if p.is_dir() and p.name not in SKIP_DIRS
    ]
    for base in candidates:
        if any((base / hint).exists() for hint in MIGRATION_HINTS):
            return base
    return None


def check_schema(root: Path) -> list:
    problems = []
    base = _migration_base(root)
    if base is None:
        problems.append(("error", "未发现迁移体系（alembic.ini / migrations / prisma / db/migrate）"))
        return problems

    version_dirs = [base / "migrations" / "versions", base / "alembic" / "versions"]
    versions = []
    for d in version_dirs:
        if d.exists():
            versions.extend(p for p in d.glob("*.py") if not p.name.startswith("__"))
    if version_dirs and not versions:
        problems.append(("error", "migrations/versions 为空：只有目录没有迁移脚本"))

    for path in walk_files(root):
        parts = set(path.parts)
        # 测试、迁移脚本、一次性数据修复脚本里用 create_all 是合理的
        if parts & {"tests", "test", "migrations", "scripts"}:
            continue
        text = read(path)
        for match in re.finditer(r"create_all\(", text):
            window = text[max(0, match.start() - 200):match.start()]
            if "AUTO_CREATE_TABLES" in window:
                problems.append(("info", f"{path.relative_to(root)} 的 create_all 受开关保护（可接受）"))
            else:
                problems.append(("warn", f"{path.relative_to(root)} 直接调用 create_all（应仅用于测试）"))
    return problems


# ---------------- 2. index ----------------

def _column_blocks(text: str):
    """按括号平衡切出 Column(...) 块，避免跨行正则误判"""
    for match in FK_COLUMN.finditer(text):
        depth, i = 0, match.end() - 1
        while i < len(text):
            if text[i] == "(":
                depth += 1
            elif text[i] == ")":
                depth -= 1
                if depth == 0:
                    yield text[match.end():i]
                    break
            i += 1


def check_index(root: Path) -> list:
    model_dirs = [root / "app" / "models", root / "models", root / "backend" / "app" / "models"]
    files = [p for d in model_dirs if d.exists() for p in d.rglob("*.py")]
    if not files:
        return [("info", "跳过：未发现 SQLAlchemy 模型目录（非 Python 栈属正常）")]

    problems, columns, indexed_columns, index_decls = [], 0, 0, 0
    for path in files:
        text = read(path)
        index_decls += text.count("Index(")
        for block in _column_blocks(text):
            if "ForeignKey(" not in block:
                continue
            columns += 1
            if "index=True" in block:
                indexed_columns += 1
            else:
                name = re.search(r"comment=\"([^\"]+)\"", block)
                problems.append((
                    "warn",
                    f"{path.relative_to(root)} 有外键列未建索引{('（' + name.group(1) + '）') if name else ''}",
                ))
    if columns and index_decls == 0:
        problems.append(("warn", f"{columns} 个外键列、0 个复合索引声明：高频查询可能全表扫"))
    elif indexed_columns:
        problems.append(("info", f"{indexed_columns}/{columns} 个外键列已建索引，复合索引 {index_decls} 个"))
    return problems


# ---------------- 3. ci ----------------

def check_ci(root: Path) -> list:
    wf_dir = root / ".github" / "workflows"
    workflows = list(wf_dir.glob("*.yml")) + list(wf_dir.glob("*.yaml")) if wf_dir.exists() else []
    if not workflows:
        return [("error", "没有 .github/workflows：没有质量门")]

    text = "\n".join(read(p) for p in workflows)
    problems = []
    for keyword, label in (("ruff", "lint"), ("pytest", "test"), ("build", "build")):
        if keyword not in text.lower():
            problems.append(("warn", f"workflow 未覆盖 {label}（找不到 `{keyword}`）"))
    if re.search(r"run:\s*(python\s+-m\s+)?pytest", text):
        for line in text.splitlines():
            if "pytest" in line and "python -m pytest" not in line and "run:" in line:
                problems.append(("warn", "测试命令未用 `python -m pytest`：console script 不会把 CWD 加进 sys.path"))
                break
    return problems


# ---------------- 4. docs ----------------

def check_docs(root: Path) -> list:
    candidates = list(root.rglob("check_docs.py"))
    if not candidates:
        return [("warn", "未找到 check_docs.py：文档漂移没有断言")]
    problems = [("info", f"找到 {candidates[0].relative_to(root)}")]
    wf_text = ""
    wf_dir = root / ".github" / "workflows"
    if wf_dir.exists():
        wf_text = "\n".join(read(p) for p in list(wf_dir.glob("*.yml")) + list(wf_dir.glob("*.yaml")))
    if "check_docs" not in wf_text:
        problems.append(("warn", "check_docs.py 未接进 CI：只在本地跑等于没有"))
    return problems


# ---------------- 5. private ----------------

def check_private(root: Path) -> list:
    problems = []
    try:
        result = subprocess.run(
            ["git", "ls-files"], cwd=root, capture_output=True, text=True, timeout=20
        )
    except (OSError, subprocess.SubprocessError):
        return [("info", "跳过：不在 git 仓库中")]
    if result.returncode != 0:
        return [("info", "跳过：不在 git 仓库中")]

    risky = []
    for name in result.stdout.splitlines():
        base = name.rsplit("/", 1)[-1]
        if base in (".env", ".env.local") or base.endswith((".db", ".sqlite3")):
            risky.append(name)
        elif "指导书" in base or "内部复盘" in base:
            risky.append(name)
    for name in risky:
        problems.append(("error", f"版本库跟踪了私有/敏感文件：{name}"))

    gitignore = root / ".gitignore"
    if gitignore.exists() and ".env" not in read(gitignore):
        problems.append(("warn", ".gitignore 未忽略 .env"))
    return problems


# ---------------- 6. defaults ----------------

def check_defaults(root: Path) -> list:
    config_files = [
        p for p in (
            root / "app" / "config.py", root / "backend" / "app" / "config.py",
            root / "config.py", root / "app" / "settings.py",
        ) if p.exists()
    ]
    if not config_files:
        return [("info", "跳过：未找到 config.py")]

    text = read(config_files[0])
    env_example = ""
    for candidate in (root / ".env.example", root / "backend" / ".env.example"):
        if candidate.exists():
            env_example = read(candidate)
            break

    problems = []
    for name, expect_false in (("AUTO_CREATE_TABLES", True), ("A2A_ENABLED", True)):
        match = re.search(rf"{name}\s*:\s*bool\s*=\s*(True|False)", text)
        if not (match and expect_false and match.group(1) == "True"):
            continue
        # 代码默认 True 但 .env.example 明确置 false，视为可接受（开发便利 + 部署收紧）
        if re.search(rf"{name}\s*=\s*false", env_example, re.IGNORECASE):
            problems.append(("info", f"{name} 代码默认 True，.env.example 已置 false（可接受）"))
        else:
            problems.append(("warn", f"{name} 默认 True：生产环境应默认关闭/走迁移"))

    for path in walk_files(root):
        src = read(path)
        if "A2A_TOKEN" in src and re.search(r"A2A_TOKEN\s*==", src):
            problems.append(("warn", f"{path.relative_to(root)} 用 == 比较令牌，建议 compare_digest"))
            break
    return problems


# ---------------- 7. deadconfig ----------------

def check_deadconfig(root: Path) -> list:
    config_files = [
        p for p in (
            root / "app" / "config.py", root / "backend" / "app" / "config.py",
            root / "config.py",
        ) if p.exists()
    ]
    if not config_files:
        return [("info", "跳过：未发现 config.py")]

    config_text = read(config_files[0])
    names = sorted(set(CONFIG_ASSIGN.findall(config_text)))
    if not names:
        return []

    corpus = []
    for path in walk_files(root):
        if path in config_files:
            continue
        corpus.append(read(path))
    haystack = "\n".join(corpus)

    dead = [name for name in names if haystack.count(name) == 0]
    problems = []
    if dead:
        preview = "、".join(dead[:8]) + ("…" if len(dead) > 8 else "")
        problems.append(("warn", f"{len(dead)} 个配置项只定义未使用：{preview}"))

    todo = sum(
        read(p).count("NotImplementedError") + len(re.findall(r"TODO", read(p)))
        for p in walk_files(root)
        if "test" not in p.parts
    )
    if todo:
        problems.append(("warn", f"代码中有 {todo} 处 TODO/NotImplementedError：确认不是留空实现"))
    return problems


CHECKS = {
    "schema": check_schema,
    "index": check_index,
    "ci": check_ci,
    "docs": check_docs,
    "private": check_private,
    "defaults": check_defaults,
    "deadconfig": check_deadconfig,
}

LEVEL_TAG = {"error": "ERROR", "warn": "WARN ", "info": "OK   "}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="工程底座自检（七项）",
        epilog="适用范围：schema/ci/docs/private 通用；index/defaults/deadconfig 仅 Python 栈，"
               "其他栈会显示“跳过”，不等于通过。",
    )
    parser.add_argument("--root", default=".", help="项目根目录")
    parser.add_argument("--skip", default="", help="跳过检查，逗号分隔")
    parser.add_argument("--strict", action="store_true", help="警告也视为失败")
    parser.add_argument("--json", action="store_true", help="JSON 输出")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    skip = {s.strip() for s in args.skip.split(",") if s.strip()}

    report, errors, warns = [], 0, 0
    for name, func in CHECKS.items():
        if name in skip:
            continue
        problems = func(root)
        level = "error" if any(p[0] == "error" for p in problems) else (
            "warn" if any(p[0] == "warn" for p in problems) else "info"
        )
        errors += sum(1 for p in problems if p[0] == "error")
        warns += sum(1 for p in problems if p[0] == "warn")
        report.append({"check": name, "level": level, "problems": problems})

    if args.json:
        print(json.dumps({"root": str(root), "checks": report,
                          "errors": errors, "warns": warns}, ensure_ascii=False, indent=2))
    else:
        for item in report:
            tag = LEVEL_TAG[item["level"]]
            print(f"[{item['check']:<10}] {tag}")
            for level, message in item["problems"]:
                print(f"    {LEVEL_TAG[level]} {message}")
        print(f"\n汇总：{errors} 个错误 / {warns} 个警告")

    if errors:
        return 1
    if args.strict and warns:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
