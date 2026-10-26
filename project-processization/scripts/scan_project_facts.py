#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scan_project_facts.py — 项目事实扫描器（"项目流程化" Skill 核心工具）

作用：在为"AI 已搭好骨架的项目"撰写学习指南前，自动扫描出可信、可追溯的事实
数字，杜绝凭印象编造行数 / 用例数 / 组件数 / 依赖 / 服务名。

能力：
  - 按扩展名与顶层目录统计代码文件数、物理行数（自动排除 venv/node_modules 等）
  - 统计测试文件数与测试函数数（Python 的 def test_*、JS/TS 的 test()/it()）
  - 列出指定组件目录（如 app/routers、src/views）下的文件数
  - 提取 docker-compose 服务名、.env 键名（脱敏，不打印值）、requirements 依赖、
    package.json 依赖
  - 输出人类可读报告，或 --json 结构化结果供后续步骤引用

用法：
  python scan_project_facts.py --path /path/to/project
  python scan_project_facts.py --path /path/to/project --json --output facts.json
  python scan_project_facts.py --path ./proj --components "app/routers,app/models,src/views"
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Set, Tuple

# 默认排除的目录名（依赖、构建产物、缓存）
DEFAULT_EXCLUDE: Set[str] = {
    ".git", ".venv", "venv", "env", "node_modules", "__pycache__",
    "dist", "build", ".next", ".nuxt", "coverage", ".idea", ".vscode",
    "egg-info", ".mypy_cache", ".pytest_cache", ".cache", "site-packages",
}

# 默认按技术栈归类的扩展名
DEFAULT_EXT_GROUPS: Dict[str, Set[str]] = {
    "python": {".py"},
    "frontend": {".vue", ".ts", ".tsx", ".js", ".jsx"},
}

CONFIG_FILE_NAMES = {".env", ".env.example", ".env.template"}


def iter_code_files(
    root: Path,
    exts: Set[str],
    exclude: Set[str],
) -> Iterator[Path]:
    """遍历 root 下所有匹配扩展名、且不在排除目录中的文件。

    Args:
        root: 项目根目录。
        exts: 需要收集的扩展名集合（小写，含点，如 ``{'.py'}``）。
        exclude: 需要排除的目录名集合。

    Yields:
        逐个匹配的文件 Path。
    """
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if any(part in exclude for part in path.parts):
            continue
        if path.suffix.lower() in exts:
            yield path


def count_physical_lines(path: Path) -> int:
    """统计文件物理行数（以换行切分，空行也计入），失败返回 0。"""
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return 0
    return len(text.splitlines())


def group_by_topdir(files: List[Path], root: Path, depth: int = 1) -> Dict[str, Dict[str, int]]:
    """把文件按相对 root 的前 ``depth`` 级目录分组，统计文件数与行数。

    直接位于根目录的文件归入 ``<root>`` 组。例如 depth=2 时 backend/app 与
    backend/tests 会分成两组，便于区分业务代码与测试代码。
    """
    groups: Dict[str, Dict[str, int]] = {}
    for f in files:
        rel = f.relative_to(root)
        if len(rel.parts) > 1:
            top = "/".join(rel.parts[:depth])
        else:
            top = "<root>"
        bucket = groups.setdefault(top, {"files": 0, "lines": 0})
        bucket["files"] += 1
        bucket["lines"] += count_physical_lines(f)
    return dict(sorted(groups.items(), key=lambda kv: kv[1]["lines"], reverse=True))


def count_test_functions(files: List[Path]) -> Dict[str, int]:
    """统计测试文件数与测试函数/用例数。

    Python 匹配 ``def test_``；JS/TS 匹配 ``test(`` / ``it(`` 调用。
    """
    py_test_pat = re.compile(r"^\s*(?:async\s+)?def\s+(test_\w+)\s*\(", re.M)
    js_test_pat = re.compile(r"\b(?:it|test)\s*\(", re.M)
    test_files = 0
    functions = 0
    per_file: List[Dict[str, Any]] = []
    for f in files:
        name = f.name
        is_test_file = name.startswith("test_") or name.endswith(("_test.py", ".test.ts",
                                                                   ".test.js", ".spec.ts",
                                                                   ".spec.js")) or "test_" in name
        if not is_test_file:
            continue
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        n = len(py_test_pat.findall(text)) if f.suffix == ".py" else len(js_test_pat.findall(text))
        test_files += 1
        functions += n
        per_file.append({"file": str(f), "cases": n})
    per_file.sort(key=lambda x: x["cases"], reverse=True)
    return {"files": test_files, "functions": functions, "per_file": per_file}


def list_component_dirs(root: Path, relative_dirs: List[str]) -> Dict[str, Any]:
    """统计指定组件目录下各子目录/文件的规模。

    对每个相对路径：若为目录，列出其下直接包含的源文件数与文件名；若为文件，记录其行数。
    """
    result: Dict[str, Any] = {}
    source_exts = {".py", ".ts", ".tsx", ".vue", ".js", ".jsx"}
    for rel in relative_dirs:
        target = root / rel
        if not target.exists():
            result[rel] = {"exists": False}
            continue
        if target.is_dir():
            files = [p for p in sorted(target.rglob("*"))
                     if p.is_file() and p.suffix.lower() in source_exts
                     and not any(x in DEFAULT_EXCLUDE for x in p.parts)]
            # __init__.py 是包标记而非业务组件，单独统计，使 file_count 等于"业务组件数"
            init_files = [p for p in files if p.name == "__init__.py"]
            business = [p for p in files if p.name != "__init__.py"]
            result[rel] = {
                "exists": True,
                "file_count": len(business),
                "init_files": len(init_files),
                "files": [str(p.relative_to(root)).replace("\\", "/") for p in business],
            }
        else:
            result[rel] = {"exists": True, "lines": count_physical_lines(target)}
    return result


def parse_docker_services(root: Path) -> List[str]:
    """从 docker-compose*.yml 中提取顶层服务名（仅做轻量正则，不依赖 PyYAML）。"""
    services: Set[str] = set()
    in_services = False
    for compose in list(root.glob("docker-compose*.yml")) + list(root.glob("docker-compose*.yaml")):
        try:
            lines = compose.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError:
            continue
        for line in lines:
            stripped = line.strip()
            if re.match(r"^services\s*:\s*$", line.strip()):
                in_services = True
                continue
            if in_services:
                # services 顶层结束：遇到新的顶层键（无缩进且冒号结尾）
                if line and not line[0].isspace() and stripped.endswith(":"):
                    in_services = False
                    continue
                m = re.match(r"^ {2}([A-Za-z0-9_\-.]+)\s*:\s*$", line)
                if m:
                    services.add(m.group(1))
    return sorted(services)


def parse_env_keys(root: Path) -> List[str]:
    """提取 .env 类文件中的键名（不返回值，避免泄露密钥）。"""
    keys: Set[str] = set()
    for name in CONFIG_FILE_NAMES:
        env = root / name
        if not env.exists():
            continue
        try:
            for line in env.read_text(encoding="utf-8", errors="ignore").splitlines():
                m = re.match(r"^\s*([A-Z0-9_]+)\s*=", line)
                if m:
                    keys.add(m.group(1))
        except OSError:
            continue
    return sorted(keys)


def parse_requirements(root: Path) -> List[str]:
    """提取 requirements*.txt 中的包名（去掉版本约束）。"""
    pkgs: Set[str] = set()
    for req in root.rglob("requirements*.txt"):
        if any(part in DEFAULT_EXCLUDE for part in req.parts):
            continue
        try:
            for line in req.read_text(encoding="utf-8", errors="ignore").splitlines():
                line = line.strip()
                if not line or line.startswith("#") or line.startswith("-"):
                    continue
                name = re.split(r"[<>=!~;\[ ]", line, maxsplit=1)[0]
                if name:
                    pkgs.add(name)
        except OSError:
            continue
    return sorted(pkgs)


def parse_package_json(root: Path) -> Dict[str, List[str]]:
    """提取所有 package.json 的 dependencies/devDependencies 键名（排除 node_modules）。"""
    deps: Set[str] = set()
    dev_deps: Set[str] = set()
    for pkg in root.rglob("package.json"):
        if any(part in DEFAULT_EXCLUDE for part in pkg.parts):
            continue
        try:
            data = json.loads(pkg.read_text(encoding="utf-8", errors="ignore"))
        except (OSError, json.JSONDecodeError):
            continue
        deps.update(data.get("dependencies", {}).keys())
        dev_deps.update(data.get("devDependencies", {}).keys())
    return {"dependencies": sorted(deps), "devDependencies": sorted(dev_deps)}


def scan(root: Path, component_dirs: List[str], group_depth: int = 1) -> Dict[str, Any]:
    """执行完整扫描，返回结构化事实字典。"""
    all_exts: Set[str] = set().union(*DEFAULT_EXT_GROUPS.values())
    all_files = list(iter_code_files(root, all_exts, DEFAULT_EXCLUDE))
    py_files = [f for f in all_files if f.suffix == ".py"]
    fe_files = [f for f in all_files if f.suffix in DEFAULT_EXT_GROUPS["frontend"]]

    def totals(files: List[Path]) -> Dict[str, int]:
        return {"files": len(files), "lines": sum(count_physical_lines(f) for f in files)}

    data: Dict[str, Any] = {
        "root": str(root),
        "group_depth": group_depth,
        "code": {
            "python": totals(py_files),
            "frontend": totals(fe_files),
            "total": totals(all_files),
        },
        "python_by_topdir": group_by_topdir(py_files, root, group_depth),
        "frontend_by_topdir": group_by_topdir(fe_files, root, group_depth),
        "tests": count_test_functions(all_files),
        "components": list_component_dirs(root, component_dirs),
        "docker_services": parse_docker_services(root),
        "env_keys": parse_env_keys(root),
        "requirements": parse_requirements(root),
        "package_json": parse_package_json(root),
    }
    return data


def format_report(data: Dict[str, Any]) -> str:
    """把扫描结果渲染为人类可读文本报告。"""
    lines: List[str] = []
    lines.append("=" * 60)
    lines.append("项目事实扫描报告")
    lines.append("=" * 60)
    code = data["code"]
    lines.append(f"代码总量: {code['total']['files']} 文件 / {code['total']['lines']} 行")
    lines.append(f"  Python: {code['python']['files']} 文件 / {code['python']['lines']} 行")
    lines.append(f"  前端:   {code['frontend']['files']} 文件 / {code['frontend']['lines']} 行")
    tests = data["tests"]
    lines.append(f"测试: {tests['files']} 个测试文件 / {tests['functions']} 个测试用例")
    for item in tests["per_file"]:
        rel = item["file"]
        lines.append(f"    - {Path(rel).name}: {item['cases']}")
    depth = data.get("group_depth", 1)
    lines.append(f"\nPython 按 {depth} 级目录:")
    for k, v in data["python_by_topdir"].items():
        lines.append(f"  {k:28s} {v['files']:4d} 文件 / {v['lines']:6d} 行")
    if data["components"]:
        lines.append("\n组件目录:")
        for rel, info in data["components"].items():
            if info.get("exists"):
                if "file_count" in info:
                    lines.append(f"  {rel}: {info['file_count']} 个文件")
                else:
                    lines.append(f"  {rel}: {info.get('lines', 0)} 行")
            else:
                lines.append(f"  {rel}: 不存在")
    if data["docker_services"]:
        lines.append(f"\nDocker 服务: {', '.join(data['docker_services'])}")
    if data["env_keys"]:
        lines.append(f"\n.env 键名（已脱敏）: {', '.join(data['env_keys'])}")
    if data["requirements"]:
        lines.append(f"\nPython 依赖: {', '.join(data['requirements'])}")
    pj = data["package_json"]
    if pj["dependencies"] or pj["devDependencies"]:
        lines.append(f"\n前端依赖: {', '.join(pj['dependencies'])}")
        lines.append(f"开发依赖: {', '.join(pj['devDependencies'])}")
    return "\n".join(lines)


def main() -> int:
    """命令行入口，返回进程退出码。"""
    parser = argparse.ArgumentParser(
        description="项目事实扫描器：统计行数/测试数/组件数/依赖/服务，输出可信事实")
    parser.add_argument("--path", required=True, help="项目根目录路径")
    parser.add_argument("--components", default="",
                        help="逗号分隔的组件目录相对路径，如 app/routers,app/models,src/views")
    parser.add_argument("--group-depth", type=int, default=1,
                        help="代码行数按前几级目录分组（默认1；设2可区分 app/ 与 tests/）")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    parser.add_argument("--output", help="将结果写入文件（JSON 或文本）")
    args = parser.parse_args()

    root = Path(args.path).resolve()
    if not root.exists() or not root.is_dir():
        print(f"❌ 路径不存在或不是目录: {root}", file=sys.stderr)
        return 2

    component_dirs = [c.strip() for c in args.components.split(",") if c.strip()]
    try:
        data = scan(root, component_dirs, group_depth=args.group_depth)
    except OSError as exc:
        print(f"❌ 扫描失败: {exc}", file=sys.stderr)
        return 1

    if args.json:
        payload = json.dumps(data, ensure_ascii=False, indent=2)
        if args.output:
            Path(args.output).write_text(payload, encoding="utf-8")
            print(f"已写入 {args.output}")
        else:
            print(payload)
    else:
        report = format_report(data)
        if args.output:
            Path(args.output).write_text(report, encoding="utf-8")
            print(f"已写入 {args.output}")
        else:
            print(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
