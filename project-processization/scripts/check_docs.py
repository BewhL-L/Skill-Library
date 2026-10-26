#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_docs.py — 文档与代码一致性校验器（"项目流程化" Skill 核心工具）

作用：生成学习指南时的事实核查只解决"写的时候对不对"；本项目解决"写完以后还对不对"。
把四类可机械校验的一致性变成断言，接入 CI 后文档漂移会直接变红。

检查项：
  1. 数量一致：README/指南声明的"N passed""N 个测试" == tests 目录实际测试函数数
     （skip 的用例会被收集但不计入 passed，两个数字分开校验）
  2. 路径一致：反引号里以 backend/ frontend/ docker/ .github/ 开头的路径必须真实存在
  3. 表述一致：禁止出现已废弃的路径/数字/字段名（默认列表 + --forbid 追加）
  4. 私有文件：私有文档、.env 等绝不能出现在 git 跟踪列表里（--skip-git 可关）
  5. 接口一致（可选）：README 里的 `/api/...` 必须能在 --openapi 或 --routes 中找到

用法：
  python check_docs.py --root 项目根
  python check_docs.py --root . --tests backend/tests --openapi openapi.json
  python check_docs.py --root . --forbid "旧路径/" --json
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import subprocess
import sys
from pathlib import Path

# 默认禁止表述：值说明原因，便于报错时直接告诉用户改什么
DEFAULT_FORBIDDEN = {
    "产品/": "旧目录名，仓库已拆分",
    "hit_at_k": "字段名应为 hit@k",
}

# 私有文件：只检查"是否被 git 跟踪"，本地存在但被忽略的不算问题
DEFAULT_PRIVATE = {
    "项目学习指导书.md": "含 AI 协作说明的私有文档，不能进公开仓库",
    "backend/.env": "含真实密钥，只允许提交 .env.example",
    ".env": "含真实密钥，只允许提交 .env.example",
}

ROOTED_PREFIXES = ("backend/", "frontend/", "docker/", ".github/", "scripts/")
BACKTICK = re.compile(r"`([^`\n]+)`")
BRACES = re.compile(r"\{[^}]+\}")


def _is_skip_decorator(node: ast.AST) -> bool:
    target = node.func if isinstance(node, ast.Call) else node
    return (
        isinstance(target, ast.Attribute)
        and target.attr == "skip"
        and isinstance(target.value, ast.Attribute)
        and target.value.attr == "mark"
    )


def count_tests(tests_dir: Path) -> tuple:
    """返回 (测试函数总数, 被 skip 的数量)"""
    total = skipped = 0
    for path in sorted(tests_dir.glob("test_*.py")):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except (OSError, SyntaxError):
            continue
        module_skipped = any(
            isinstance(node, ast.Assign)
            and any(getattr(t, "id", "") == "pytestmark" for t in node.targets)
            and any(_is_skip_decorator(n) for n in ast.walk(node.value))
            for node in tree.body
        )
        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
                total += 1
                if module_skipped or any(_is_skip_decorator(d) for d in node.decorator_list):
                    skipped += 1
    return total, skipped


def check_numbers(text: str, tests_dir: Path) -> list:
    errors = []
    total, skipped = count_tests(tests_dir)
    if total == 0:
        return [f"未在 {tests_dir} 找到测试（用 --tests 指定目录）"]

    passed = total - skipped
    claimed = set()
    for line in text.splitlines():
        low = line.lower()
        if "passed" in low and not any(k in low for k in ("npm", "vitest", "frontend")):
            claimed.update(re.findall(r"(\d+)\s*passed", line))
    claimed.update(re.findall(r"(\d+)\s*个测试", text))

    if not claimed:
        errors.append("文档未声明测试数量（建议写 `pytest -q  # N passed`），无法校验")
    for number in sorted(claimed):
        if int(number) not in (passed, total):
            errors.append(
                f"测试数量不一致：文档写 {number}，实际 {passed} passed / {total} 个测试函数"
            )
    return errors


def check_paths(text: str, root: Path) -> list:
    errors, seen = [], set()
    for token in BACKTICK.findall(text):
        token = token.strip().rstrip("/")
        if not token.startswith(ROOTED_PREFIXES) or token in seen:
            continue
        if any(ch in token for ch in "{}* ") or "<" in token:
            continue
        seen.add(token)
        # 文档里常把 backend/scripts/xx.py 简写成 scripts/xx.py，这里做一次兼容
        candidates = [root / token, root / "backend" / token]
        if not any(c.exists() for c in candidates):
            errors.append(f"路径不存在：`{token}`")
    return errors


def check_forbidden(text: str, forbidden: dict) -> list:
    return [
        f"出现已废弃表述 `{needle}`：{reason}"
        for needle, reason in forbidden.items()
        if needle in text
    ]


def check_private(root: Path, private: dict) -> list:
    try:
        result = subprocess.run(
            ["git", "ls-files"], cwd=root, capture_output=True, text=True, timeout=20
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return [f"跳过私有文件检查：{type(exc).__name__}"]
    if result.returncode != 0:
        return ["跳过私有文件检查：不在 git 仓库中"]
    tracked = set(result.stdout.splitlines())
    return [
        f"版本库里出现 `{name}`：{reason}"
        for name, reason in private.items()
        if name in tracked
    ]


def load_routes(openapi: Path = None, routes_file: Path = None) -> set:
    paths = set()
    if openapi and openapi.exists():
        data = json.loads(openapi.read_text(encoding="utf-8"))
        paths.update(data.get("paths", {}).keys())
    if routes_file and routes_file.exists():
        paths.update(
            line.strip() for line in routes_file.read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
    return {BRACES.sub("{}", p).rstrip("/") for p in paths}


def check_endpoints(text: str, routes: set) -> list:
    if not routes:
        return []
    errors, seen = [], set()
    for token in BACKTICK.findall(text):
        if not token.startswith(("/api/", "/a2a/", "/embed/")):
            continue
        doc_path = BRACES.sub("{}", token.strip().rstrip("/"))
        if doc_path in seen:
            continue
        seen.add(doc_path)
        if not any(r == doc_path or r.startswith(doc_path + "/") for r in routes):
            errors.append(f"接口不存在：`{token}`（路由表中无匹配项）")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="文档与代码一致性校验")
    parser.add_argument("--root", default=".", help="项目根目录")
    parser.add_argument("--doc", default="README.md", help="待校验文档（相对 root）")
    parser.add_argument("--tests", default="backend/tests", help="测试目录（相对 root）")
    parser.add_argument("--openapi", default="", help="openapi.json 路径（可选）")
    parser.add_argument("--routes", default="", help="每行一个路由路径的文本文件（可选）")
    parser.add_argument("--forbid", action="append", default=[], help="追加禁止表述，可多次")
    parser.add_argument("--private", action="append", default=[], help="追加私有文件，可多次")
    parser.add_argument("--skip-git", action="store_true", help="跳过 git 私有文件检查")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    doc = root / args.doc
    if not doc.exists():
        print(f"找不到文档：{doc}")
        return 1

    text = doc.read_text(encoding="utf-8")
    forbidden = dict(DEFAULT_FORBIDDEN)
    forbidden.update({item: "由 --forbid 指定" for item in args.forbid})
    private = dict(DEFAULT_PRIVATE)
    private.update({item: "由 --private 指定" for item in args.private})

    routes = load_routes(
        Path(args.openapi) if args.openapi else None,
        Path(args.routes) if args.routes else None,
    )

    checks = [
        ("测试数量", lambda: check_numbers(text, root / args.tests)),
        ("文档路径", lambda: check_paths(text, root)),
        ("废弃表述", lambda: check_forbidden(text, forbidden)),
    ]
    if not args.skip_git:
        checks.append(("私有文件", lambda: check_private(root, private)))
    if routes:
        checks.append(("接口路径", lambda: check_endpoints(text, routes)))

    results, all_errors = [], []
    for name, func in checks:
        errors = func()
        results.append({"name": name, "ok": not errors, "errors": errors})
        all_errors.extend(errors)

    if args.json:
        print(json.dumps({"doc": str(doc), "results": results}, ensure_ascii=False, indent=2))
    else:
        for item in results:
            print(f"[{item['name']}] {'OK' if item['ok'] else str(len(item['errors'])) + ' 处不一致'}")
        if all_errors:
            print("\n发现文档与代码不一致：")
            for error in all_errors:
                print(f"  - {error}")
            print("\n修完再跑一次。")
    return 0 if not all_errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
