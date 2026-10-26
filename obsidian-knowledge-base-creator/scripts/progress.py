#!/usr/bin/env python3
"""
学习进度报告工具
基于 Frontmatter 的 status/difficulty/category 字段，生成学习进度统计报告

用法:
    python progress.py --path "知识库路径"
    python progress.py --path "./my-kb"
"""

import os
import re
import argparse
from collections import defaultdict
from datetime import datetime

def extract_frontmatter(filepath: str) -> dict:
    """提取Frontmatter"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        if match:
            fm_text = match.group(1)
            fm = {}
            for line in fm_text.split('\n'):
                if ':' in line and not line.strip().startswith('#'):
                    key, value = line.split(':', 1)
                    fm[key.strip()] = value.strip()
            return fm
    except:
        pass
    return {}

def get_difficulty_level(difficulty: str) -> dict:
    """将星级转换为数字等级"""
    if not difficulty:
        return 0
    return difficulty.count('⭐')

def main() -> None:
    """主函数"""
    parser = argparse.ArgumentParser(description="生成学习进度报告")
    parser.add_argument("--path", required=True, help="知识库路径")
    args = parser.parse_args()

    kb_root = os.path.abspath(args.path)
    if not os.path.exists(kb_root):
        print(f"❌ 路径不存在: {kb_root}")
        return

    print(f"📊 学习进度报告: {kb_root}")
    print(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # 扫描所有文件
    notes = []
    for root, dirs, files in os.walk(kb_root):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if file.endswith('.md') and not file.startswith('MOC-') and file != 'Home.md':
                filepath = os.path.join(root, file)
                fm = extract_frontmatter(filepath)
                if fm:
                    notes.append({
                        'title': fm.get('title', file.replace('.md', '')),
                        'category': fm.get('category', '未分类'),
                        'difficulty': fm.get('difficulty', '⭐⭐⭐'),
                        'status': fm.get('status', '📝 草稿'),
                        'priority': fm.get('priority', '一般'),
                        'tags': fm.get('tags', ''),
                        'filepath': filepath,
                    })

    total = len(notes)
    print(f"\n📝 总笔记数: {total}")

    if total == 0:
        print("⚠️  没有找到带 Frontmatter 的笔记")
        return

    # 1. 按状态统计
    print("\n" + "=" * 60)
    print("📌 一、学习状态统计")
    print("-" * 40)
    status_counts = defaultdict(int)
    for note in notes:
        status = note['status']
        # 简化状态
        if '已完善' in status or '完成' in status:
            status_counts['✅ 已完成'] += 1
        elif '草稿' in status or '待完善' in status:
            status_counts['📝 待完善'] += 1
        elif '更新中' in status:
            status_counts['🔄 更新中'] += 1
        else:
            status_counts['❓ 其他'] += 1

    for status, count in sorted(status_counts.items()):
        percent = count / total * 100
        bar = '█' * int(percent / 5) + '░' * (20 - int(percent / 5))
        print(f"  {status}: {count:4d} ({percent:5.1f}%) {bar}")

    completed = status_counts.get('✅ 已完成', 0)
    print(f"\n  📈 整体完成度: {completed/total*100:.1f}%")

    # 2. 按难度统计
    print("\n" + "=" * 60)
    print("⭐ 二、难度分布统计")
    print("-" * 40)
    diff_counts = defaultdict(int)
    for note in notes:
        level = get_difficulty_level(note['difficulty'])
        diff_names = {0: '未标注', 1: '⭐ 入门', 2: '⭐⭐ 进阶', 3: '⭐⭐⭐ 高级', 4: '⭐⭐⭐⭐ 专家', 5: '⭐⭐⭐⭐⭐ 资深'}
        diff_counts[diff_names.get(level, '未知')] += 1

    for level in ['未标注', '⭐ 入门', '⭐⭐ 进阶', '⭐⭐⭐ 高级', '⭐⭐⭐⭐ 专家', '⭐⭐⭐⭐⭐ 资深']:
        if level in diff_counts:
            count = diff_counts[level]
            percent = count / total * 100
            bar = '█' * int(percent / 5) + '░' * (20 - int(percent / 5))
            print(f"  {level:12s}: {count:4d} ({percent:5.1f}%) {bar}")

    # 3. 按分类统计
    print("\n" + "=" * 60)
    print("📂 三、分类学习进度")
    print("-" * 40)
    cat_stats = defaultdict(lambda: {'total': 0, 'completed': 0})
    for note in notes:
        cat = note['category']
        cat_stats[cat]['total'] += 1
        if '已完善' in note['status'] or '完成' in note['status']:
            cat_stats[cat]['completed'] += 1

    print(f"  {'分类':<15s} {'总数':>5s} {'已完成':>6s} {'完成度':>8s}")
    print("  " + "-" * 40)
    for cat, stats in sorted(cat_stats.items(), key=lambda x: x[1]['total'], reverse=True):
        percent = stats['completed'] / stats['total'] * 100 if stats['total'] > 0 else 0
        print(f"  {cat:<15s} {stats['total']:5d} {stats['completed']:6d} {percent:7.1f}%")

    # 4. 按优先级统计
    print("\n" + "=" * 60)
    print("🎯 四、优先级分布")
    print("-" * 40)
    priority_counts = defaultdict(int)
    for note in notes:
        priority = note['priority']
        priority_counts[priority] += 1

    for priority in ['核心', '重要', '一般', '可选']:
        if priority in priority_counts:
            count = priority_counts[priority]
            percent = count / total * 100
            print(f"  {priority}: {count:4d} ({percent:5.1f}%)")

    # 5. 待学习清单（核心+未完成）
    print("\n" + "=" * 60)
    print("📋 五、待学习核心笔记（核心优先级 + 未完成）")
    print("-" * 40)
    todo_notes = []
    for note in notes:
        if note['priority'] == '核心' and ('已完善' not in note['status']):
            todo_notes.append(note)

    if todo_notes:
        for i, note in enumerate(todo_notes[:20], 1):
            print(f"  {i:2d}. [{note['difficulty']}] {note['title']} ({note['category']})")
        if len(todo_notes) > 20:
            print(f"  ... 还有 {len(todo_notes)-20} 个")
    else:
        print("  ✅ 所有核心笔记已完成！")

    # 6. 学习建议
    print("\n" + "=" * 60)
    print("💡 六、学习建议")
    print("-" * 40)

    # 根据完成度给出建议
    if completed / total < 0.3:
        print("  📌 当前处于起步阶段，建议:")
        print("     1. 先从 ⭐ 入门级 笔记开始，打好基础")
        print("     2. 优先学习标记为「核心」优先级的笔记")
        print("     3. 每学完一篇，将 status 改为「✅ 内容已完善」")
        print("     4. 配合项目实战，巩固所学知识")
    elif completed / total < 0.6:
        print("  📌 当前处于进阶阶段，建议:")
        print("     1. 继续学习 ⭐⭐ 进阶级 和 ⭐⭐⭐ 高级 笔记")
        print("     2. 关注各分类的完成度，补齐薄弱环节")
        print("     3. 开始进行综合项目实战")
        print("     4. 建立笔记间的双链关联，形成知识网络")
    elif completed / total < 0.9:
        print("  📌 当前处于高级阶段，建议:")
        print("     1. 攻克 ⭐⭐⭐⭐ 专家级 和 ⭐⭐⭐⭐⭐ 资深级 笔记")
        print("     2. 深入研究源码和底层原理")
        print("     3. 参与开源项目或技术分享")
        print("     4. 整理自己的知识体系，输出技术文章")
    else:
        print("  🎉 恭喜！知识库学习完成度很高！")
        print("     建议: 持续关注技术前沿，更新知识库内容")

    print("\n" + "=" * 60)
    print(f"📊 报告生成完成！共分析 {total} 篇笔记")
    print(f"   整体完成度: {completed/total*100:.1f}%")
    print(f"   待学习核心笔记: {len(todo_notes)} 篇")

if __name__ == "__main__":
    main()
