#!/usr/bin/env python3
"""
Obsidian 知识库标准化工具 - 统一 CLI 入口

用法:
    python scripts/kb.py init --name "我的知识库" --path "./my-kb"
    python scripts/kb.py note --title "Vue3 响应式" --category 前端开发 --kb-root "./my-kb"
    python scripts/kb.py moc --category 前端开发 --kb-root "./my-kb"
    python scripts/kb.py audit --kb-root "./my-kb"
    python scripts/kb.py validate --kb-root "./my-kb"
    python scripts/kb.py fix-frontmatter --kb-root "./my-kb"
    python scripts/kb.py fix-deadlinks --kb-root "./my-kb"
"""

import os
import sys
import argparse
import subprocess
from datetime import datetime

# 脚本目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def run_script(script_name: str, args: list) -> bool:
    """运行子脚本"""
    script_path = os.path.join(SCRIPT_DIR, script_name)
    if not os.path.exists(script_path):
        print(f"❌ 脚本不存在: {script_path}")
        return False

    cmd = [sys.executable, script_path] + args
    try:
        result = subprocess.run(cmd, capture_output=False)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ 运行失败: {e}")
        return False

def cmd_init(args: argparse.Namespace) -> bool:
    """初始化知识库"""
    print(f"🚀 初始化知识库: {args.name}")
    extra_args = ["--name", args.name, "--path", args.path]
    if args.theme:
        extra_args += ["--theme", args.theme]
    if args.config:
        extra_args += ["--config", args.config]
    if args.demo:
        extra_args.append("--demo")
    return run_script("init-kb.py", extra_args)

def cmd_note(args: argparse.Namespace) -> bool:
    """生成标准化笔记"""
    print(f"📝 生成笔记: {args.title}")
    extra_args = ["--title", args.title, "--category", args.category]
    if args.difficulty:
        extra_args += ["--difficulty", str(args.difficulty)]
    if args.tags:
        extra_args += ["--tags"] + args.tags
    if args.pre:
        extra_args += ["--pre"] + args.pre
    if args.kb_root:
        extra_args += ["--kb-root", args.kb_root]
    if args.output:
        extra_args += ["--output", args.output]
    success = run_script("generate-note.py", extra_args)

    # 自动更新对应分类的MOC
    if success and args.kb_root:
        print(f"\n🔄 自动更新 MOC: {args.category}...")
        # 动态扫描分类目录（支持自定义配置分类）
        cat_dir = None
        if os.path.isdir(args.kb_root):
            for d in os.listdir(args.kb_root):
                dp = os.path.join(args.kb_root, d)
                if os.path.isdir(dp) and '-' in d:
                    parts = d.split('-', 1)
                    if len(parts) == 2 and parts[1] == args.category:
                        cat_dir = d
                        break
        # 兜底：默认分类映射
        if not cat_dir:
            default_map = {
                "综合导航": "00-综合导航", "前端开发": "01-前端开发",
                "后端开发": "02-后端开发", "数据库与缓存": "03-数据库与缓存",
                "分布式与中间件": "04-分布式与中间件", "云原生与运维": "05-云原生与运维",
                "计算机基础": "06-计算机基础", "通用工具": "07-通用工具",
                "Python全栈": "08-Python全栈", "AI与效率工具": "09-AI与效率工具",
                "项目实战": "99-项目实战",
            }
            cat_dir = default_map.get(args.category)
        if cat_dir:
            moc_path = os.path.join(args.kb_root, cat_dir)
            run_script("generate-moc.py", ["--category", args.category, "--path", moc_path])
    return success

def cmd_moc(args: argparse.Namespace) -> bool:
    """生成 MOC"""
    print(f"📚 生成 MOC: {args.category}")
    if args.kb_root:
        # 动态扫描分类目录（支持自定义配置分类）
        cat_dir = None
        if os.path.isdir(args.kb_root):
            for d in os.listdir(args.kb_root):
                dp = os.path.join(args.kb_root, d)
                if os.path.isdir(dp) and '-' in d:
                    parts = d.split('-', 1)
                    if len(parts) == 2 and parts[1] == args.category:
                        cat_dir = d
                        break
        # 兜底：默认映射或直接用分类名
        if not cat_dir:
            default_map = {
                "综合导航": "00-综合导航", "前端开发": "01-前端开发",
                "后端开发": "02-后端开发", "数据库与缓存": "03-数据库与缓存",
                "分布式与中间件": "04-分布式与中间件", "云原生与运维": "05-云原生与运维",
                "计算机基础": "06-计算机基础", "通用工具": "07-通用工具",
                "Python全栈": "08-Python全栈", "AI与效率工具": "09-AI与效率工具",
                "项目实战": "99-项目实战",
            }
            cat_dir = default_map.get(args.category, args.category)
        path = os.path.join(args.kb_root, cat_dir)
    else:
        path = args.path or args.category
    extra_args = ["--category", args.category, "--path", path]
    return run_script("generate-moc.py", extra_args)

def cmd_audit(args: argparse.Namespace) -> bool:
    """健康检查"""
    print(f"🔍 健康检查: {args.kb_root}")
    return run_script("audit-kb.py", ["--path", args.kb_root])

def cmd_validate(args: argparse.Namespace) -> bool:
    """质量校验"""
    print(f"✅ 质量校验: {args.kb_root}")
    extra_args = ["--path", args.kb_root]
    if args.strict:
        extra_args.append("--strict")
    return run_script("validate-kb.py", extra_args)

def cmd_fix_frontmatter(args: argparse.Namespace) -> bool:
    """批量补全 Frontmatter"""
    print(f"🔧 批量补全 Frontmatter: {args.kb_root}")
    return run_script("fix-frontmatter.py", ["--path", args.kb_root])

def cmd_fix_deadlinks(args: argparse.Namespace) -> bool:
    """修复死链"""
    print(f"🔗 修复死链: {args.kb_root}")
    extra_args = ["--path", args.kb_root]
    if args.threshold:
        extra_args += ["--threshold", str(args.threshold)]
    if args.dry_run:
        extra_args.append("--dry-run")
    return run_script("fix-deadlinks.py", extra_args)

def cmd_info(args: argparse.Namespace) -> bool:
    """显示工具信息"""
    print("""
╔══════════════════════════════════════════════╗
║  Obsidian 知识库标准化工具 v2.3              ║
║  基于全栈+AI工程知识库标准                    ║
╠══════════════════════════════════════════════╣
║                                              ║
║  可用命令:                                   ║
║    init        - 初始化知识库                ║
║    note        - 生成标准化笔记（自动更新MOC）║
║    batch-note  - 批量生成笔记 🆕             ║
║    moc         - 生成 MOC 内容地图           ║
║    audit       - 健康检查                    ║
║    validate    - 质量校验                    ║
║    fix-fm      - 批量补全 Frontmatter        ║
║    fix-link    - 修复死链                    ║
║    fix-tags    - 批量统一标签                ║
║    standardize - 一键标准化知识库            ║
║    progress    - 生成学习进度报告            ║
║    info        - 显示此帮助信息              ║
║                                              ║
║  使用示例:                                   ║
║    kb.bat init --name "我的库" --path ./kb  ║
║    kb.bat note --title "Vue3" --category 前端开发 --kb-root ./kb
║    kb.bat standardize --kb-root ./kb        ║
║    kb.bat progress --kb-root ./kb            ║
║                                              ║
╚══════════════════════════════════════════════╝
""")
    return True

def cmd_standardize(args: argparse.Namespace) -> bool:
    """一键标准化知识库"""
    kb_root = os.path.abspath(args.kb_root)
    print(f"🚀 一键标准化知识库: {kb_root}")
    print("=" * 60)

    # 12个分类
    categories = ["综合导航", "前端开发", "后端开发", "数据库与缓存",
                  "分布式与中间件", "云原生与运维", "计算机基础", "通用工具",
                  "Python全栈", "AI与效率工具", "项目实战"]
    category_dirs = ["00-综合导航", "01-前端开发", "02-后端开发", "03-数据库与缓存",
                     "04-分布式与中间件", "05-云原生与运维", "06-计算机基础", "07-通用工具",
                     "08-Python全栈", "09-AI与效率工具", "99-项目实战"]

    results = {}

    # 步骤1：批量补全Frontmatter
    if not args.skip_fix_fm:
        print("\n📋 步骤 1/4: 批量补全 Frontmatter...")
        success = run_script("fix-frontmatter.py", ["--path", kb_root])
        results['fix_fm'] = success
    else:
        print("\n⏭️  步骤 1/4: 跳过 Frontmatter 补全")

    # 步骤2：修复死链
    if not args.skip_fix_link:
        print("\n🔗 步骤 2/4: 修复死链...")
        success = run_script("fix-deadlinks.py",
                           ["--path", kb_root, "--threshold", str(args.threshold)])
        results['fix_link'] = success
    else:
        print("\n⏭️  步骤 2/4: 跳过死链修复")

    # 步骤3：为所有分类生成MOC
    if not args.skip_moc:
        print("\n📚 步骤 3/4: 生成所有分类 MOC...")
        moc_success = True
        for cat, cat_dir in zip(categories, category_dirs):
            cat_path = os.path.join(kb_root, cat_dir)
            if os.path.exists(cat_path):
                print(f"  生成 MOC: {cat}...")
                success = run_script("generate-moc.py",
                                   ["--category", cat, "--path", cat_path])
                if not success:
                    moc_success = False
        results['moc'] = moc_success
    else:
        print("\n⏭️  步骤 3/4: 跳过 MOC 生成")

    # 步骤4：健康检查
    print("\n🔍 步骤 4/4: 健康检查...")
    success = run_script("audit-kb.py", ["--path", kb_root])
    results['audit'] = success

    # 总结
    print("\n" + "=" * 60)
    print("📊 标准化完成总结:")
    for step, success in results.items():
        status = "✅" if success else "❌"
        print(f"  {status} {step}")

    all_success = all(results.values())
    if all_success:
        print("\n🎉 知识库标准化全部完成！")
    else:
        print("\n⚠️  部分步骤失败，请检查上方日志")
    return all_success

def cmd_progress(args: argparse.Namespace) -> bool:
    """生成学习进度报告"""
    return run_script("progress.py", ["--path", args.kb_root])

def cmd_fix_tags(args: argparse.Namespace) -> bool:
    """批量统一标签"""
    extra_args = ["--path", args.kb_root]
    if args.dry_run:
        extra_args.append("--dry-run")
    return run_script("fix-tags.py", extra_args)

def cmd_batch_note(args: argparse.Namespace) -> bool:
    """批量生成笔记"""
    extra_args = ["--list", args.list, "--kb-root", args.kb_root]
    if args.dry_run:
        extra_args.append("--dry-run")
    return run_script("batch-generate-notes.py", extra_args)

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Obsidian 知识库标准化工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python scripts/kb.py init --name "我的知识库" --path "./my-kb"
  python scripts/kb.py init --name "演示库" --path "./demo" --demo
  python scripts/kb.py init --name "AI库" --path "./ai" --config themes/ai-engineering.yaml
  python scripts/kb.py note --title "Vue3 响应式" --category 前端开发 --kb-root "./my-kb"
  python scripts/kb.py moc --category 前端开发 --kb-root "./my-kb"
  python scripts/kb.py audit --kb-root "./my-kb"
  python scripts/kb.py validate --kb-root "./my-kb" --strict
        """
    )
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # init 命令
    p_init = subparsers.add_parser("init", help="初始化知识库")
    p_init.add_argument("--name", required=True, help="知识库名称")
    p_init.add_argument("--path", required=True, help="输出路径")
    p_init.add_argument("--theme", default="全栈+AI", help="知识库主题")
    p_init.add_argument("--config", help="配置文件路径（YAML格式，自定义分类/模板/标签）")
    p_init.add_argument("--demo", action="store_true", help="生成包含示例笔记的演示知识库")

    # note 命令
    p_note = subparsers.add_parser("note", help="生成标准化笔记")
    p_note.add_argument("--title", required=True, help="笔记标题")
    p_note.add_argument("--category", required=True, help="所属分类")
    p_note.add_argument("--difficulty", type=int, default=3, choices=[1,2,3,4,5], help="难度等级")
    p_note.add_argument("--tags", nargs="*", help="标签列表")
    p_note.add_argument("--pre", nargs="*", help="前置知识列表")
    p_note.add_argument("--kb-root", help="知识库根目录")
    p_note.add_argument("--output", help="输出文件路径")

    # moc 命令
    p_moc = subparsers.add_parser("moc", help="生成 MOC 内容地图")
    p_moc.add_argument("--category", required=True, help="分类名称")
    p_moc.add_argument("--kb-root", help="知识库根目录")
    p_moc.add_argument("--path", help="笔记目录路径（优先于kb-root）")

    # audit 命令
    p_audit = subparsers.add_parser("audit", help="健康检查")
    p_audit.add_argument("--kb-root", required=True, help="知识库根目录")

    # validate 命令
    p_validate = subparsers.add_parser("validate", help="质量校验")
    p_validate.add_argument("--kb-root", required=True, help="知识库根目录")
    p_validate.add_argument("--strict", action="store_true", help="严格模式")

    # fix-frontmatter 命令
    p_fix_fm = subparsers.add_parser("fix-fm", help="批量补全 Frontmatter")
    p_fix_fm.add_argument("--kb-root", required=True, help="知识库根目录")

    # fix-deadlinks 命令
    p_fix_link = subparsers.add_parser("fix-link", help="修复死链")
    p_fix_link.add_argument("--kb-root", required=True, help="知识库根目录")
    p_fix_link.add_argument("--threshold", type=int, default=3, help="创建笔记的引用阈值")
    p_fix_link.add_argument("--dry-run", action="store_true", help="仅显示不执行")

    # standardize 命令（一键标准化）
    p_standardize = subparsers.add_parser("standardize", help="一键标准化知识库")
    p_standardize.add_argument("--kb-root", required=True, help="知识库根目录")
    p_standardize.add_argument("--skip-fix-fm", action="store_true", help="跳过Frontmatter补全")
    p_standardize.add_argument("--skip-fix-link", action="store_true", help="跳过死链修复")
    p_standardize.add_argument("--skip-moc", action="store_true", help="跳过MOC生成")
    p_standardize.add_argument("--threshold", type=int, default=3, help="死链修复阈值")

    # progress 命令（学习进度报告）
    p_progress = subparsers.add_parser("progress", help="生成学习进度报告")
    p_progress.add_argument("--kb-root", required=True, help="知识库根目录")

    # fix-tags 命令（标签统一）
    p_fix_tags = subparsers.add_parser("fix-tags", help="批量统一标签")
    p_fix_tags.add_argument("--kb-root", required=True, help="知识库根目录")
    p_fix_tags.add_argument("--dry-run", action="store_true", help="仅显示不执行")

    # batch-note 命令（批量生成笔记）
    p_batch_note = subparsers.add_parser("batch-note", help="批量生成标准化笔记")
    p_batch_note.add_argument("--list", required=True, help="笔记列表文件（JSON/YAML）")
    p_batch_note.add_argument("--kb-root", required=True, help="知识库根目录")
    p_batch_note.add_argument("--dry-run", action="store_true", help="仅显示不执行")

    # info 命令
    subparsers.add_parser("info", help="显示工具信息")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # 命令分发
    commands = {
        "init": cmd_init,
        "note": cmd_note,
        "batch-note": cmd_batch_note,
        "moc": cmd_moc,
        "audit": cmd_audit,
        "validate": cmd_validate,
        "fix-fm": cmd_fix_frontmatter,
        "fix-link": cmd_fix_deadlinks,
        "fix-tags": cmd_fix_tags,
        "standardize": cmd_standardize,
        "progress": cmd_progress,
        "info": cmd_info,
    }

    handler = commands.get(args.command)
    if handler:
        success = handler(args)
        sys.exit(0 if success else 1)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
