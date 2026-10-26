#!/usr/bin/env python3
"""
批量补全 Frontmatter 脚本
扫描知识库中所有笔记，自动补全缺失的 Frontmatter 字段

用法:
    python fix-frontmatter.py --path "知识库路径"
    python fix-frontmatter.py --path "./my-kb" --dry-run

v1.1.0: 补全aliases字段（标准10字段），与obsidian-knowledge-base-creator标准一致
"""

import os
import re
import argparse
from datetime import datetime

# 分类映射（从文件夹名推断）
CATEGORY_MAP = {
    "00-综合导航": "综合导航",
    "01-前端开发": "前端开发",
    "02-后端开发": "后端开发",
    "03-数据库与缓存": "数据库与缓存",
    "04-分布式与中间件": "分布式与中间件",
    "05-云原生与运维": "云原生与运维",
    "06-计算机基础": "计算机基础",
    "07-通用工具": "通用工具",
    "08-Python全栈": "Python全栈",
    "09-AI与效率工具": "AI与效率工具",
    "99-项目实战": "项目实战",
}

# 标准字段（10个，含aliases）
REQUIRED_FIELDS = ['title', 'tags', 'category', 'created', 'updated', 'difficulty', 'status', 'priority', 'pre', 'aliases']


def build_dynamic_category_map(kb_root: str) -> dict:
    """动态扫描知识库目录，构建 目录名→分类名 映射（支持自定义配置分类）

    优先级：动态扫描 > 默认 CATEGORY_MAP
    扫描规则：匹配 "编号-分类名" 格式的目录名，如 "01-前端开发" → "前端开发"
    """
    dynamic_map = {}
    try:
        if os.path.exists(kb_root):
            for name in os.listdir(kb_root):
                full_path = os.path.join(kb_root, name)
                if os.path.isdir(full_path) and re.match(r'^\d+-', name):
                    # 提取 "编号-分类名" 中的分类名
                    cat_name = name.split('-', 1)[1] if '-' in name else name
                    dynamic_map[name] = cat_name
    except Exception:
        pass
    # 合并：动态映射优先，默认映射兜底
    merged = dict(CATEGORY_MAP)
    merged.update(dynamic_map)
    return merged


def extract_frontmatter(content: str) -> tuple:
    """提取 Frontmatter，返回 (frontmatter_dict, 剩余内容, 是否有frontmatter)"""
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if match:
        fm_text = match.group(1)
        fm = {}
        for line in fm_text.split('\n'):
            if ':' in line and not line.strip().startswith('#'):
                key, value = line.split(':', 1)
                fm[key.strip()] = value.strip()
        rest = content[match.end():]
        return fm, rest, True
    return {}, content, False


def infer_category(filepath: str, kb_root: str) -> str:
    """从文件路径推断分类（支持自定义配置分类）"""
    rel_path = os.path.relpath(filepath, kb_root)
    parts = rel_path.split(os.sep)
    # 使用动态映射（支持自定义分类）
    cat_map = build_dynamic_category_map(kb_root)
    if parts:
        top_dir = parts[0]
        if top_dir in cat_map:
            return cat_map[top_dir]
        # 尝试模糊匹配
        for key, value in cat_map.items():
            if key in top_dir or value in top_dir:
                return value
    return "未分类"


def infer_difficulty(filename: str, category: str) -> str:
    """从文件名推断难度"""
    name_lower = filename.lower()
    if any(x in name_lower for x in ['入门', '基础', '快速上手', 'hello', 'tutorial']):
        return "⭐"
    elif any(x in name_lower for x in ['进阶', '实战', '指南', '核心']):
        return "⭐⭐"
    elif any(x in name_lower for x in ['高级', '深度', '原理', '架构', '优化']):
        return "⭐⭐⭐"
    elif any(x in name_lower for x in ['专家', '源码', '精通', '底层']):
        return "⭐⭐⭐⭐"
    elif any(x in name_lower for x in ['资深', '前沿', '研究']):
        return "⭐⭐⭐⭐⭐"
    return "⭐⭐⭐"  # 默认中级


def infer_priority(filename: str, tags: str) -> str:
    """推断优先级"""
    name_lower = filename.lower()
    if any(x in name_lower for x in ['核心', '基础', '入门', '总览', '大全']):
        return "核心"
    elif any(x in name_lower for x in ['实战', '进阶', '原理', '深度']):
        return "重要"
    return "一般"


def build_frontmatter(fm: dict, filepath: str, kb_root: str, filename: str) -> dict:
    """构建完整的 Frontmatter（10个标准字段）"""
    date = datetime.now().strftime('%Y-%m-%d')
    title = filename.replace('.md', '')

    # 补全缺失字段
    if 'title' not in fm or not fm['title']:
        fm['title'] = title
    if 'category' not in fm or not fm['category'] or fm['category'] == '未分类':
        fm['category'] = infer_category(filepath, kb_root)
    if 'created' not in fm or not fm['created']:
        fm['created'] = date
    if 'updated' not in fm or not fm['updated']:
        fm['updated'] = date
    if 'difficulty' not in fm or not fm['difficulty'] or not fm['difficulty'].startswith('⭐'):
        fm['difficulty'] = infer_difficulty(filename, fm.get('category', ''))
    if 'status' not in fm or not fm['status']:
        fm['status'] = '✅ 内容已完善'
    if 'priority' not in fm or not fm['priority']:
        fm['priority'] = infer_priority(filename, fm.get('tags', ''))
    if 'pre' not in fm:
        fm['pre'] = '[]'
    if 'aliases' not in fm:
        fm['aliases'] = '[]'
    if 'tags' not in fm or not fm['tags'] or fm['tags'] == '[]':
        # 从分类推断默认标签
        cat = fm.get('category', '')
        fm['tags'] = f'[{cat}]'

    return fm


def format_frontmatter(fm: dict) -> str:
    """格式化 Frontmatter 为 YAML 字符串"""
    lines = ['---']
    # 按标准顺序输出（10个字段）
    field_order = [
        'title', 'tags', 'category', 'created', 'updated',
        'difficulty', 'status', 'priority', 'pre', 'aliases'
    ]
    for field in field_order:
        if field in fm:
            lines.append(f'{field}: {fm[field]}')
    # 输出其他字段
    for field in fm:
        if field not in field_order:
            lines.append(f'{field}: {fm[field]}')
    lines.append('---')
    return '\n'.join(lines)


def process_file(filepath: str, kb_root: str, dry_run: bool = False) -> tuple:
    """处理单个文件"""
    filename = os.path.basename(filepath)

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return filename, f'读取失败: {e}', False

    fm, rest, has_fm = extract_frontmatter(content)

    # 检查缺失字段
    missing = [f for f in REQUIRED_FIELDS if f not in fm or not fm[f]]
    # 检查 difficulty 是否为星级
    diff_issue = 'difficulty' in fm and not fm['difficulty'].startswith('⭐')

    if not missing and not diff_issue and has_fm:
        return filename, '已完整', False

    # 补全 Frontmatter
    new_fm = build_frontmatter(fm, filepath, kb_root, filename)
    new_fm_text = format_frontmatter(new_fm)
    new_content = new_fm_text + '\n\n' + rest

    if dry_run:
        changes = []
        if not has_fm:
            changes.append('新增Frontmatter')
        if missing:
            changes.append(f'补全字段: {", ".join(missing)}')
        if diff_issue:
            changes.append('difficulty转为星级')
        return filename, '; '.join(changes), True

    # 写入文件
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        changes = []
        if not has_fm:
            changes.append('新增Frontmatter')
        if missing:
            changes.append(f'补全: {", ".join(missing)}')
        if diff_issue:
            changes.append('difficulty星级化')
        return filename, '; '.join(changes), True
    except Exception as e:
        return filename, f'写入失败: {e}', False


def main() -> None:
    """主函数"""
    parser = argparse.ArgumentParser(description="批量补全 Frontmatter（10个标准字段）")
    parser.add_argument("--path", required=True, help="知识库路径")
    parser.add_argument("--dry-run", action="store_true", help="仅显示不执行")
    args = parser.parse_args()

    kb_root = os.path.abspath(args.path)
    if not os.path.exists(kb_root):
        print(f"❌ 路径不存在: {kb_root}")
        return

    print(f"🔧 批量补全 Frontmatter: {kb_root}")
    print(f"   标准字段: {', '.join(REQUIRED_FIELDS)}")
    if args.dry_run:
        print("  (预览模式，不修改文件)")
    print("=" * 60)

    # 扫描所有 markdown 文件
    md_files = []
    for root, dirs, files in os.walk(kb_root):
        # 跳过隐藏目录
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if file.endswith('.md'):
                md_files.append(os.path.join(root, file))

    print(f"📝 发现 {len(md_files)} 个 Markdown 文件\n")

    # 处理文件
    changed = 0
    for filepath in md_files:
        filename, msg, was_changed = process_file(filepath, kb_root, args.dry_run)
        if was_changed:
            changed += 1
            status = "🔧" if was_changed else "✅"
            print(f"  {status} {filename}: {msg}")

    print("\n" + "=" * 60)
    print(f"📊 处理完成")
    print(f"  总文件数: {len(md_files)}")
    print(f"  需修改: {changed}")
    print(f"  已完整: {len(md_files) - changed}")
    if args.dry_run:
        print(f"\n💡 这是预览模式，去掉 --dry-run 参数以执行修改")


if __name__ == "__main__":
    main()
