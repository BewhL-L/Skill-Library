#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skill 工程化优化器 - 统一 CLI 入口 v1.8.0
基于 25 轮优化经验，提供 Skill 健康检查、自动优化、文档生成、测试生成、批量优化、对比报告全流程工具
v1.7.0: 修复导入路径bug、集成 Skill 类型自动检测、新增批量优化/对比报告/类型检测命令、
        纯文档型自动跳过测试生成、完善错误处理
v1.8.0: 版本号统一，完善文档和批量优化报告
"""

import argparse
import sys
import os
import json
import importlib.util
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# 同目录脚本路径
SCRIPTS_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS_DIR))


def _load_module(module_name: str, filename: str):
    """
    动态加载带连字符的 Python 模块（如 audit-skill.py）
    因为 Python import 不支持连字符文件名
    """
    filepath = SCRIPTS_DIR / filename
    if not filepath.exists():
        print(f"❌ 错误: 找不到脚本文件 {filename}")
        sys.exit(1)
    spec = importlib.util.spec_from_file_location(module_name, str(filepath))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# 懒加载模块（避免启动时加载所有模块）
_modules = {}

def _get_auditor():
    if "auditor" not in _modules:
        _modules["auditor"] = _load_module("audit_skill", "audit-skill.py")
    return _modules["auditor"]

def _get_optimizer():
    if "optimizer" not in _modules:
        _modules["optimizer"] = _load_module("optimize_skill", "optimize-skill.py")
    return _modules["optimizer"]

def _get_doc_generator():
    if "docs" not in _modules:
        _modules["docs"] = _load_module("generate_docs", "generate-docs.py")
    return _modules["docs"]

def _get_test_generator():
    if "tests" not in _modules:
        _modules["tests"] = _load_module("generate_tests", "generate-tests.py")
    return _modules["tests"]

def _get_type_detector():
    if "detector" not in _modules:
        _modules["detector"] = _load_module("skill_type_detector", "skill_type_detector.py")
    return _modules["detector"]


def _detect_skill_type(skill_path: str) -> str:
    """检测 Skill 类型"""
    try:
        detector_cls = _get_type_detector().SkillTypeDetector
        detector = detector_cls(skill_path)
        return detector.detect()["type"]
    except Exception as e:
        print(f"⚠️  类型检测失败: {e}，默认按代码驱动型处理")
        return "code-driven"


def _validate_skill_path(skill_path: str, require_skill_md: bool = True) -> bool:
    """
    验证 Skill 路径是否有效

    Args:
        skill_path: Skill 目录路径
        require_skill_md: 是否要求存在 SKILL.md

    Returns:
        True 表示路径有效，False 表示无效
    """
    path = Path(skill_path)
    if not path.exists():
        print(f"❌ 错误: 路径不存在 - {skill_path}")
        print("   请检查路径是否正确，或使用绝对路径。")
        return False
    if not path.is_dir():
        print(f"❌ 错误: 路径不是目录 - {skill_path}")
        return False
    if require_skill_md and not (path / "SKILL.md").exists():
        print(f"⚠️  警告: 目录中未找到 SKILL.md - {skill_path}")
        print("   这可能不是一个有效的 Skill 目录。评估结果可能不准确。")
        print("   继续执行...（如需终止，请按 Ctrl+C）")
    return True


# ========== 命令实现 ==========

def cmd_type(args):
    """类型检测命令"""
    if not _validate_skill_path(args.path, require_skill_md=False):
        return 1
    print("🔍 Skill 类型检测")
    print("=" * 60)
    try:
        detector_cls = _get_type_detector().SkillTypeDetector
        detector = detector_cls(args.path)
        result = detector.detect()

        type_names = {
            "code-driven": "代码驱动型",
            "doc-only": "纯文档型",
            "hybrid": "混合型",
        }
        print(f"\n📋 Skill 路径: {args.path}")
        print(f"   类型: {type_names.get(result['type'], result['type'])}")
        print(f"   置信度: {result['confidence']:.0%}")
        print(f"   代码型得分: {result['code_score']}/100")
        print(f"   文档型得分: {result['doc_score']}/100")
        print(f"   描述: {result.get('description', '')}")

        weights = detector.get_audit_weights()
        print(f"\n📊 Audit 评估模式: {result['type']} 模式（{len(weights)}个维度）")
        for dim, w in sorted(weights.items(), key=lambda x: -x[1]):
            print(f"   {dim:25s} {w*100:5.1f}%")

        scopes = detector.get_optimize_scopes()
        print(f"\n🔧 Optimize 适用范围: {', '.join(scopes)}")
        return 0
    except Exception as e:
        print(f"❌ 类型检测失败: {e}")
        return 1


def cmd_audit(args):
    """健康检查命令"""
    if not _validate_skill_path(args.path):
        return 1
    try:
        auditor_cls = _get_auditor().SkillAuditor
        auditor = auditor_cls(args.path)
        results = auditor.audit()
        if args.format == "json":
            output = args.output or "audit-report.json"
            auditor.save_report(output)
        else:
            auditor.print_report()
        return 0 if results["score"] >= 70 else 1
    except Exception as e:
        print(f"❌ 健康检查失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


def cmd_optimize(args):
    """自动优化命令"""
    if not _validate_skill_path(args.path):
        return 1
    try:
        optimizer_cls = _get_optimizer().SkillOptimizer
        optimizer = optimizer_cls(args.path, dry_run=args.dry_run)
        only = args.only.split(",") if args.only else None
        result = optimizer.optimize(only=only)
        optimizer.print_summary()
        return 0 if not result["errors"] else 1
    except Exception as e:
        print(f"❌ 自动优化失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


def cmd_docs(args):
    """文档生成命令"""
    if not _validate_skill_path(args.path):
        return 1
    try:
        gen_cls = _get_doc_generator().DocGenerator
        generator = gen_cls(args.path)
        generator.generate(doc_type=args.type)
        generator.print_summary()
        return 0
    except Exception as e:
        print(f"❌ 文档生成失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


def cmd_tests(args):
    """测试生成命令（纯文档型自动跳过）"""
    if not _validate_skill_path(args.path):
        return 1
    skill_type = _detect_skill_type(args.path)
    if skill_type == "doc-only":
        print("⚠️  检测到纯文档型 Skill，无需生成测试（无 Python 代码）")
        print("   建议：专注于完善文档结构和 references 深度")
        return 0

    try:
        gen_cls = _get_test_generator().TestGenerator
        generator = gen_cls(args.path)
        generator.generate(test_type=args.type)
        generator.print_summary()
        return 0
    except Exception as e:
        print(f"❌ 测试生成失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


def cmd_all(args):
    """一键全流程命令（按 Skill 类型自适应）"""
    if not _validate_skill_path(args.path):
        return 1
    print("🚀 开始全流程优化（检查→优化→文档→[测试]→验证）")
    print("=" * 60)

    skill_type = _detect_skill_type(args.path)
    type_names = {"code-driven": "代码驱动型", "doc-only": "纯文档型", "hybrid": "混合型"}
    print(f"\n📋 检测到 Skill 类型: {type_names.get(skill_type, skill_type)}")

    # 1. 健康检查（优化前）
    print("\n📋 步骤 1/5: 健康检查（优化前）")
    auditor_cls = _get_auditor().SkillAuditor
    auditor = auditor_cls(args.path)
    before_results = auditor.audit()
    auditor.print_report()
    before_score = before_results["score"]

    # 2. 自动优化
    print("\n🔧 步骤 2/5: 自动优化")
    optimizer_cls = _get_optimizer().SkillOptimizer
    optimizer = optimizer_cls(args.path, dry_run=False)
    opt_result = optimizer.optimize()
    optimizer.print_summary()

    # 3. 生成文档
    print("\n📚 步骤 3/5: 生成文档")
    doc_gen_cls = _get_doc_generator().DocGenerator
    doc_gen = doc_gen_cls(args.path)
    doc_gen.generate(doc_type="all")
    doc_gen.print_summary()

    # 4. 生成测试（纯文档型跳过）
    if skill_type == "doc-only":
        print("\n🧪 步骤 4/5: 生成测试（跳过 - 纯文档型无需测试）")
        test_count = 0
    else:
        print("\n🧪 步骤 4/5: 生成测试")
        test_gen_cls = _get_test_generator().TestGenerator
        test_gen = test_gen_cls(args.path)
        test_gen.generate(test_type="all")
        test_gen.print_summary()
        test_count = len(test_gen.generated)

    # 5. 最终验证（优化后）
    print("\n📊 步骤 5/5: 最终验证（优化后）")
    auditor2 = auditor_cls(args.path)
    after_results = auditor2.audit()
    after_score = after_results["score"]
    score_diff = after_score - before_score

    # 最终报告
    print("\n" + "=" * 60)
    print("✅ 全流程优化完成！")
    print(f"\n📈 优化效果对比:")
    print(f"   优化前总分: {before_score}/100")
    print(f"   优化后总分: {after_score}/100")
    print(f"   分数变化: {'+' if score_diff >= 0 else ''}{score_diff:.1f} 分")
    print(f"\n📝 优化统计:")
    print(f"   自动优化更改: {opt_result['total_changes']} 项")
    print(f"   生成文档: {len(doc_gen.generated)} 个")
    if skill_type != "doc-only":
        print(f"   生成测试: {test_count} 个文件")
    print(f"\n💡 后续建议:")
    if skill_type != "doc-only":
        print("   1. 手动完善代码类型注解和异常处理")
        print("   2. 实现生成的测试用例中的 TODO")
        print("   3. 运行 python -m pytest tests/ -v 验证")
    else:
        print("   1. 深化 references/ 文档内容（每篇至少80行）")
        print("   2. 完善 SKILL.md 的输出规范和质量检查清单")
        print("   3. 增加具体使用场景和输入/输出示例")
    print("   4. 再次运行 audit 查看优化效果")
    return 0


def cmd_batch(args):
    """批量优化命令：一次优化目录下所有 Skill"""
    base_dir = Path(args.path)
    if not base_dir.exists():
        print(f"❌ 错误: 目录不存在 - {args.path}")
        return 1

    # 查找所有包含 SKILL.md 的子目录
    skill_dirs = []
    for item in base_dir.iterdir():
        if item.is_dir() and (item / "SKILL.md").exists():
            skill_dirs.append(item)

    if not skill_dirs:
        print(f"❌ 在 {args.path} 下未找到任何 Skill（包含 SKILL.md 的目录）")
        return 1

    print(f"📦 批量优化模式")
    print("=" * 60)
    print(f"   目标目录: {base_dir}")
    print(f"   发现 Skill: {len(skill_dirs)} 个")
    for i, d in enumerate(skill_dirs, 1):
        print(f"   {i}. {d.name}")
    print()

    # 逐个优化
    results = []
    for i, skill_dir in enumerate(skill_dirs, 1):
        print(f"\n{'='*60}")
        print(f"[{i}/{len(skill_dirs)}] 优化: {skill_dir.name}")
        print(f"{'='*60}")

        try:
            # 优化前 audit
            auditor_cls = _get_auditor().SkillAuditor
            auditor = auditor_cls(str(skill_dir))
            before = auditor.audit()
            before_score = before["score"]
            skill_type = before.get("skill_type", "unknown")

            # 自动优化
            optimizer_cls = _get_optimizer().SkillOptimizer
            optimizer = optimizer_cls(str(skill_dir), dry_run=args.dry_run)
            opt_result = optimizer.optimize()

            # 优化后 audit
            auditor2 = auditor_cls(str(skill_dir))
            after = auditor2.audit()
            after_score = after["score"]

            results.append({
                "name": skill_dir.name,
                "type": skill_type,
                "before": before_score,
                "after": after_score,
                "diff": round(after_score - before_score, 1),
                "changes": opt_result["total_changes"],
                "errors": len(opt_result["errors"]),
            })

            print(f"\n✅ {skill_dir.name}: {before_score} → {after_score} ({'+' if after_score >= before_score else ''}{after_score - before_score:.1f})")

        except Exception as e:
            print(f"❌ {skill_dir.name} 优化失败: {e}")
            results.append({
                "name": skill_dir.name,
                "type": "error",
                "before": 0,
                "after": 0,
                "diff": 0,
                "changes": 0,
                "errors": 1,
                "error_msg": str(e),
            })

    # 批量报告
    print(f"\n{'='*60}")
    print("📊 批量优化报告")
    print(f"{'='*60}")
    print(f"\n{'Skill名称':<30} {'类型':<10} {'优化前':>6} {'优化后':>6} {'变化':>7} {'更改':>5}")
    print("-" * 70)
    total_diff = 0
    success_count = 0
    for r in results:
        if r["errors"] == 0:
            success_count += 1
            total_diff += r["diff"]
        print(f"{r['name']:<30} {r['type']:<10} {r['before']:>6.1f} {r['after']:>6.1f} {r['diff']:>+7.1f} {r['changes']:>5}")

    print("-" * 70)
    avg_diff = total_diff / success_count if success_count > 0 else 0
    failed_count = len(results) - success_count
    if failed_count > 0:
        print(f"成功: {success_count}/{len(results)} | 失败: {failed_count} | 平均提升: {avg_diff:+.1f} 分 | 总提升: {total_diff:+.1f} 分")
    else:
        print(f"成功: {success_count}/{len(results)} | 平均提升: {avg_diff:+.1f} 分 | 总提升: {total_diff:+.1f} 分")

    # 保存报告
    if args.output:
        report = {
            "batch_time": datetime.now().isoformat(),
            "base_dir": str(base_dir),
            "total_skills": len(results),
            "success_count": success_count,
            "failed_count": failed_count,
            "total_score_diff": round(total_diff, 1),
            "avg_score_diff": round(avg_diff, 1),
            "results": results,
        }
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\n📄 批量报告已保存到: {args.output}")

    return 0 if success_count == len(results) else 1


def cmd_diff(args):
    """优化前后对比报告命令"""
    print("📊 Skill 优化前后对比报告")
    print("=" * 60)

    # 读取优化前报告
    before_file = Path(args.before)
    after_file = Path(args.after) if args.after else None

    if not before_file.exists():
        print(f"❌ 错误: 优化前报告不存在 - {args.before}")
        return 1

    try:
        with open(before_file, "r", encoding="utf-8") as f:
            before_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ 错误: 优化前报告不是有效的 JSON 文件 - {args.before}")
        print(f"   解析错误: {e}")
        print("   请确保使用 audit-skill.py --format json 生成的报告文件。")
        return 1
    except Exception as e:
        print(f"❌ 错误: 读取优化前报告失败 - {e}")
        return 1

    # 验证报告格式
    if "score" not in before_data or "dimensions" not in before_data:
        print(f"❌ 错误: 优化前报告格式不正确 - {args.before}")
        print("   报告应包含 'score' 和 'dimensions' 字段。")
        print("   请使用 audit-skill.py --format json 重新生成报告。")
        return 1

    # 如果没有提供优化后报告，则实时运行 audit
    if after_file is None:
        print("⚠️  未提供优化后报告，将实时运行 audit...")
        skill_path = before_data.get("metadata", {}).get("skill_path", args.path)
        if not skill_path or not Path(skill_path).exists():
            print(f"❌ 错误: 无法从报告中获取有效的 Skill 路径，且未提供 --path 参数")
            print("   请使用 --path 指定 Skill 目录，或提供 --after 报告文件。")
            return 1
        auditor_cls = _get_auditor().SkillAuditor
        auditor = auditor_cls(skill_path)
        after_data = auditor.audit()
    else:
        if not after_file.exists():
            print(f"❌ 错误: 优化后报告不存在 - {args.after}")
            return 1
        try:
            with open(after_file, "r", encoding="utf-8") as f:
                after_data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"❌ 错误: 优化后报告不是有效的 JSON 文件 - {args.after}")
            print(f"   解析错误: {e}")
            return 1
        except Exception as e:
            print(f"❌ 错误: 读取优化后报告失败 - {e}")
            return 1

    before_score = before_data.get("score", 0)
    after_score = after_data.get("score", 0)
    score_diff = after_score - before_score

    print(f"\n📈 总分对比:")
    print(f"   优化前: {before_score}/100")
    print(f"   优化后: {after_score}/100")
    print(f"   变化: {'+' if score_diff >= 0 else ''}{score_diff:.1f} 分")

    # 各维度对比
    before_dims = before_data.get("dimensions", {})
    after_dims = after_data.get("dimensions", {})
    all_dims = sorted(set(list(before_dims.keys()) + list(after_dims.keys())))

    print(f"\n📊 各维度对比:")
    print(f"   {'维度':<25} {'优化前':>6} {'优化后':>6} {'变化':>7} {'状态':<6}")
    print("   " + "-" * 55)
    for dim in all_dims:
        b = before_dims.get(dim, {}).get("score", 0)
        a = after_dims.get(dim, {}).get("score", 0)
        d = a - b
        if d > 0:
            status = "✅ 提升"
        elif d < 0:
            status = "⚠️ 下降"
        else:
            status = "➖ 持平"
        print(f"   {dim:<25} {b:>6.1f} {a:>6.1f} {d:>+7.1f} {status:<6}")

    # 问题数对比
    before_issues = len(before_data.get("issues", []))
    after_issues = len(after_data.get("issues", []))
    print(f"\n🔍 问题数对比:")
    print(f"   优化前: {before_issues} 个问题")
    print(f"   优化后: {after_issues} 个问题")
    print(f"   减少: {before_issues - after_issues} 个问题")

    # 保存对比报告
    if args.output:
        diff_report = {
            "diff_time": datetime.now().isoformat(),
            "before_score": before_score,
            "after_score": after_score,
            "score_diff": round(score_diff, 1),
            "dimensions": {
                dim: {
                    "before": before_dims.get(dim, {}).get("score", 0),
                    "after": after_dims.get(dim, {}).get("score", 0),
                    "diff": round(after_dims.get(dim, {}).get("score", 0) - before_dims.get(dim, {}).get("score", 0), 1),
                }
                for dim in all_dims
            },
            "before_issues": before_issues,
            "after_issues": after_issues,
            "issues_reduced": before_issues - after_issues,
        }
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(diff_report, f, ensure_ascii=False, indent=2)
        print(f"\n📄 对比报告已保存到: {args.output}")

    return 0


def cmd_info(args):
    """显示信息命令"""
    print("=" * 60)
    print("🛠️  Skill 工程化优化器 v1.8.0")
    print("=" * 60)
    print("\n基于 25 轮实战优化经验，提供 Skill 全流程优化工具链。")
    print("支持自动检测 Skill 类型（代码驱动型/纯文档型/混合型），按类型自适应优化。")
    print("\n📋 可用命令:")
    print("  type       - Skill 类型检测（查看评估模式和优化范围）")
    print("  audit      - 健康检查（按类型自适应维度评估）")
    print("  optimize   - 自动优化（按类型过滤操作）")
    print("  docs       - 文档生成（API/FAQ/示例/架构）")
    print("  tests      - 测试生成（纯文档型自动跳过）")
    print("  all        - 一键全流程（检查→优化→文档→[测试]→验证）")
    print("  batch      - 批量优化（一次优化目录下所有 Skill）")
    print("  diff       - 优化前后对比报告")
    print("  info       - 显示此帮助信息")
    print("\n📚 详细文档:")
    print("  SKILL.md              - 完整功能说明")
    print("  OPTIMIZATION-GUIDE.md - 25轮优化完整指南（含纯文档型适配）")
    print("  CHECKLIST.md          - 优化检查清单（100+项）")
    print("  QUALITY-STANDARDS.md  - 质量标准与验收规范")
    print("\n💡 使用示例:")
    print("  python skill-opt.py type --path ./my-skill")
    print("  python skill-opt.py audit --path ./my-skill")
    print("  python skill-opt.py optimize --path ./my-skill --auto")
    print("  python skill-opt.py all --path ./my-skill")
    print("  python skill-opt.py batch --path ./skills-dir --output batch-report.json")
    print("  python skill-opt.py diff --before before.json --after after.json")
    print("\n" + "=" * 60)
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Skill 工程化优化器 v1.8.0 - 基于25轮优化经验的全流程工具（支持多类型Skill自适应+批量优化）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python skill-opt.py type --path ./my-skill
  python skill-opt.py audit --path ./my-skill
  python skill-opt.py optimize --path ./my-skill --auto
  python skill-opt.py all --path ./my-skill
  python skill-opt.py batch --path ./skills-dir
  python skill-opt.py diff --before before.json
        """
    )
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # type 命令
    type_parser = subparsers.add_parser("type", help="Skill 类型检测")
    type_parser.add_argument("--path", required=True, help="Skill 目录路径")
    type_parser.set_defaults(func=cmd_type)

    # audit 命令
    audit_parser = subparsers.add_parser("audit", help="Skill 健康检查")
    audit_parser.add_argument("--path", required=True, help="Skill 目录路径")
    audit_parser.add_argument("--format", choices=["text", "json"], default="text", help="输出格式")
    audit_parser.add_argument("--output", help="输出文件路径（JSON格式时）")
    audit_parser.set_defaults(func=cmd_audit)

    # optimize 命令
    opt_parser = subparsers.add_parser("optimize", help="自动优化")
    opt_parser.add_argument("--path", required=True, help="Skill 目录路径")
    opt_parser.add_argument("--auto", action="store_true", help="自动执行所有优化")
    opt_parser.add_argument("--dry-run", action="store_true", help="预览模式")
    opt_parser.add_argument("--only", help="只优化指定部分（docs,code,config,basic_config），逗号分隔")
    opt_parser.set_defaults(func=cmd_optimize)

    # docs 命令
    docs_parser = subparsers.add_parser("docs", help="生成文档")
    docs_parser.add_argument("--path", required=True, help="Skill 目录路径")
    docs_parser.add_argument("--type", choices=["all", "api", "faq", "examples", "architecture"],
                             default="all", help="文档类型")
    docs_parser.set_defaults(func=cmd_docs)

    # tests 命令
    tests_parser = subparsers.add_parser("tests", help="生成测试（纯文档型自动跳过）")
    tests_parser.add_argument("--path", required=True, help="Skill 目录路径")
    tests_parser.add_argument("--type", choices=["all", "unit", "integration", "conftest", "coverage"],
                              default="all", help="测试类型")
    tests_parser.set_defaults(func=cmd_tests)

    # all 命令
    all_parser = subparsers.add_parser("all", help="一键全流程优化（按类型自适应）")
    all_parser.add_argument("--path", required=True, help="Skill 目录路径")
    all_parser.set_defaults(func=cmd_all)

    # batch 命令
    batch_parser = subparsers.add_parser("batch", help="批量优化目录下所有 Skill")
    batch_parser.add_argument("--path", required=True, help="包含多个 Skill 的目录路径")
    batch_parser.add_argument("--dry-run", action="store_true", help="预览模式")
    batch_parser.add_argument("--output", help="批量优化报告输出路径（JSON）")
    batch_parser.set_defaults(func=cmd_batch)

    # diff 命令
    diff_parser = subparsers.add_parser("diff", help="优化前后对比报告")
    diff_parser.add_argument("--before", required=True, help="优化前 audit 报告（JSON）")
    diff_parser.add_argument("--after", help="优化后 audit 报告（JSON），不提供则实时运行")
    diff_parser.add_argument("--path", help="Skill 路径（当 --after 不提供时使用）")
    diff_parser.add_argument("--output", help="对比报告输出路径（JSON）")
    diff_parser.set_defaults(func=cmd_diff)

    # info 命令
    info_parser = subparsers.add_parser("info", help="显示帮助信息")
    info_parser.set_defaults(func=cmd_info)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
