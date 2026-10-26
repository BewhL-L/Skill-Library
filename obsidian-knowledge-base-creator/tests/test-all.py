#!/usr/bin/env python3
"""
自动化测试脚本 - 一键测试所有 12 个命令

用法:
    python test-all.py
    python test-all.py --keep  # 保留测试文件，不清理
"""

import os
import sys
import subprocess
import shutil
import tempfile
import time

# 项目根目录（tests/ 的上一级），kb.py 在根目录的 scripts/ 下
SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KB_PY = os.path.join(SCRIPT_DIR, "scripts", "kb.py")

# 测试结果
results = []
passed = 0
failed = 0

def run_command(cmd, description, timeout=60):
    """运行命令并返回结果"""
    global passed, failed
    print(f"\n{'='*60}")
    print(f"🧪 测试: {description}")
    print(f"   命令: {' '.join(cmd)}")
    print(f"{'='*60}")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=timeout,
            cwd=SCRIPT_DIR
        )

        # 检查是否有明显的错误（排除正常文档中的关键词）
        output = result.stdout + result.stderr
        output_lower = output.lower()
        # 只检测真正的错误，排除正常文档中的"错误"、"问题"等词
        has_error = (
            'traceback' in output_lower or
            'exception' in output_lower or
            '❌' in output or
            '失败' in output and '测试' not in output and '通过率' not in output
        )

        if result.returncode == 0 and not has_error:
            print(f"✅ 通过 (返回码: {result.returncode})")
            if result.stdout:
                # 只显示最后5行
                lines = result.stdout.strip().split('\n')
                for line in lines[-5:]:
                    print(f"   {line}")
            results.append((description, True, ""))
            passed += 1
            return True
        else:
            print(f"❌ 失败 (返回码: {result.returncode})")
            if result.stderr:
                print(f"   错误: {result.stderr[:500]}")
            elif result.stdout:
                print(f"   输出: {result.stdout[:500]}")
            results.append((description, False, result.stderr[:200]))
            failed += 1
            return False

    except subprocess.TimeoutExpired:
        print(f"❌ 超时 ({timeout}秒)")
        results.append((description, False, "超时"))
        failed += 1
        return False
    except Exception as e:
        print(f"❌ 异常: {e}")
        results.append((description, False, str(e)))
        failed += 1
        return False

def main():
    global passed, failed

    print("=" * 60)
    print("🧪 Obsidian 知识库工具 - 自动化测试")
    print(f"📁 脚本目录: {SCRIPT_DIR}")
    print(f"🐍 Python: {sys.version.split()[0]}")
    print("=" * 60)

    # 检查 kb.py 是否存在
    if not os.path.exists(KB_PY):
        print(f"❌ 找不到 kb.py: {KB_PY}")
        sys.exit(1)

    # 创建临时测试目录
    test_dir = os.path.join(tempfile.gettempdir(), f"kb-test-{int(time.time())}")
    print(f"\n📁 测试目录: {test_dir}")

    # 是否保留测试文件
    keep_files = "--keep" in sys.argv

    try:
        # 1. 测试 info 命令
        run_command(
            [sys.executable, KB_PY, "info"],
            "info - 显示帮助信息"
        )

        # 2. 测试 init 命令
        run_command(
            [sys.executable, KB_PY, "init", "--name", "测试知识库",
             "--path", test_dir, "--theme", "测试"],
            "init - 初始化知识库"
        )

        # 3. 测试 note 命令
        run_command(
            [sys.executable, KB_PY, "note", "--title", "测试笔记",
             "--category", "前端开发", "--difficulty", "2",
             "--kb-root", test_dir],
            "note - 生成标准化笔记"
        )

        # 4. 测试 moc 命令
        run_command(
            [sys.executable, KB_PY, "moc", "--category", "前端开发",
             "--kb-root", test_dir],
            "moc - 生成 MOC 内容地图"
        )

        # 5. 测试 audit 命令
        run_command(
            [sys.executable, KB_PY, "audit", "--kb-root", test_dir],
            "audit - 健康检查"
        )

        # 6. 测试 validate 命令
        run_command(
            [sys.executable, KB_PY, "validate", "--kb-root", test_dir],
            "validate - 质量校验"
        )

        # 7. 测试 fix-fm 命令
        run_command(
            [sys.executable, KB_PY, "fix-fm", "--kb-root", test_dir],
            "fix-fm - 批量补全 Frontmatter"
        )

        # 8. 测试 fix-tags 命令（预览模式）
        run_command(
            [sys.executable, KB_PY, "fix-tags", "--kb-root", test_dir,
             "--dry-run"],
            "fix-tags - 批量统一标签（预览）"
        )

        # 9. 测试 progress 命令
        run_command(
            [sys.executable, KB_PY, "progress", "--kb-root", test_dir],
            "progress - 学习进度报告"
        )

        # 10. 测试 standardize 命令（跳过死链修复，避免创建过多文件）
        run_command(
            [sys.executable, KB_PY, "standardize", "--kb-root", test_dir,
             "--skip-fix-link"],
            "standardize - 一键标准化知识库"
        )

        # 11. 测试 batch-note 命令（预览模式）
        # 创建测试 JSON 文件
        test_json = os.path.join(test_dir, "test-notes.json")
        import json
        with open(test_json, 'w', encoding='utf-8') as f:
            json.dump([
                {"title": "批量测试1", "category": "后端开发", "difficulty": 2},
                {"title": "批量测试2", "category": "数据库与缓存", "difficulty": 3}
            ], f, ensure_ascii=False)

        run_command(
            [sys.executable, KB_PY, "batch-note", "--list", test_json,
             "--kb-root", test_dir, "--dry-run"],
            "batch-note - 批量生成笔记（预览）"
        )

        # 12. 测试 fix-link 命令（预览模式，阈值设高避免创建）
        run_command(
            [sys.executable, KB_PY, "fix-link", "--kb-root", test_dir,
             "--threshold", "100"],
            "fix-link - 修复死链（高阈值）"
        )

    finally:
        # 清理测试文件
        if not keep_files and os.path.exists(test_dir):
            print(f"\n🧹 清理测试目录: {test_dir}")
            try:
                shutil.rmtree(test_dir)
                print("✅ 清理完成")
            except Exception as e:
                print(f"⚠️  清理失败: {e}")
        elif keep_files:
            print(f"\n📁 测试文件已保留: {test_dir}")

    # 输出测试总结
    print("\n" + "=" * 60)
    print("📊 测试总结")
    print("=" * 60)
    print(f"  总测试数: {len(results)}")
    print(f"  ✅ 通过: {passed}")
    print(f"  ❌ 失败: {failed}")
    print(f"  通过率: {passed/len(results)*100:.1f}%")
    print()

    if failed > 0:
        print("❌ 失败的测试:")
        for desc, success, error in results:
            if not success:
                print(f"  - {desc}: {error}")
        print()
        sys.exit(1)
    else:
        print("🎉 所有测试通过！")
        sys.exit(0)

if __name__ == "__main__":
    main()
