#!/usr/bin/env python3
"""
知识库配置加载模块
支持从 YAML 配置文件加载知识库配置，实现分类、模板、标签等的可定制化

用法:
    from config import load_config, get_categories, get_category_map
    config = load_config("path/to/.kb-config.yaml")
    categories = get_categories(config)
"""

import os
import sys
import yaml
from typing import Optional


# 默认 12 个分类（当配置文件不存在或未指定分类时使用）
DEFAULT_CATEGORIES = [
    ("00", "综合导航", "首页、学习路线、知识地图、索引"),
    ("01", "前端开发", "HTML/CSS/JS/Vue/React/工程化"),
    ("02", "后端开发", "Java/Spring/微服务/并发/JVM"),
    ("03", "数据库与缓存", "MySQL/Redis/向量数据库/ES"),
    ("04", "分布式与中间件", "MQ/分布式事务/分布式锁/限流熔断"),
    ("05", "云原生与运维", "Docker/K8s/DevOps/监控/Linux"),
    ("06", "计算机基础", "网络/操作系统/数据结构/算法"),
    ("07", "通用工具", "Git/IDE/效率工具/终端"),
    ("08", "Python全栈", "Python/FastAPI/异步/测试"),
    ("09", "AI与效率工具", "LLM/RAG/Agent/多模态/Prompt"),
    ("99", "项目实战", "综合项目/案例/实战"),
]

# 默认 Frontmatter 配置
DEFAULT_FRONTSMATTER = {
    "defaults": {
        "status": "✅ 内容已完善",
        "priority": "重要",
        "difficulty": "⭐⭐⭐",
    },
    "required": ["title", "tags", "category", "created", "updated", "difficulty", "status", "priority", "pre"],
    "optional": ["aliases", "description", "author"],
}

# 默认难度配置
DEFAULT_DIFFICULTY = {
    "use_stars": True,
    "levels": {
        "⭐": "入门",
        "⭐⭐": "进阶",
        "⭐⭐⭐": "高级",
        "⭐⭐⭐⭐": "专家",
        "⭐⭐⭐⭐⭐": "资深",
    },
}

# 默认笔记生成配置
DEFAULT_NOTE_GEN = {
    "default_template": "note-template.md",
    "sections": [
        {"name": "概述", "weight": 15},
        {"name": "原理", "weight": 30},
        {"name": "实操", "weight": 30},
        {"name": "问题", "weight": 15},
        {"name": "拓展", "weight": 10},
    ],
    "auto_create_links": True,
    "auto_update_moc": True,
}

# 默认 MOC 配置
DEFAULT_MOC = {
    "auto_learning_path": True,
    "sort_by": "difficulty",
    "show_stats": True,
}


def load_config(config_path: Optional[str] = None) -> dict:
    """
    加载知识库配置文件

    Args:
        config_path: 配置文件路径，为 None 时返回默认配置

    Returns:
        配置字典，包含所有配置项
    """
    config = {
        "kb": {
            "name": "我的知识库",
            "theme": "全栈+AI工程",
            "version": "1.0.0",
            "description": "从零基础到资深专家的完整学习路径",
        },
        "structure": {
            "categories": [{"id": c[0], "name": c[1], "desc": c[2]} for c in DEFAULT_CATEGORIES],
        },
        "frontmatter": DEFAULT_FRONTSMATTER,
        "tags": {
            "min_count": 2,
            "max_count": 8,
            "allow_custom": True,
            "core_tags_file": "references/tag-taxonomy.md",
        },
        "difficulty": DEFAULT_DIFFICULTY,
        "note_generation": DEFAULT_NOTE_GEN,
        "moc": DEFAULT_MOC,
        "deadlink_fix": {
            "create_threshold": 3,
            "auto_infer_category": True,
            "default_status": "📝 草稿",
            "default_difficulty": "⭐⭐",
        },
        "audit": {
            "checks": ["frontmatter_complete", "tags_valid", "no_deadlinks", "no_isolated_notes", "moc_coverage", "structure_complete"],
            "isolated_threshold": 0,
            "report_format": "text",
        },
        "learning_path": {
            "stages": [
                {"name": "入门筑基", "duration": "0-3个月", "goal": "掌握基础语法和工具"},
                {"name": "进阶提升", "duration": "3-6个月", "goal": "深入理解核心原理"},
                {"name": "高级精通", "duration": "6-12个月", "goal": "掌握架构设计"},
                {"name": "专家架构", "duration": "12个月+", "goal": "技术引领和输出"},
            ],
            "require_project": True,
            "require_acceptance": True,
        },
        "obsidian": {
            "recommended_plugins": ["Dataview", "Templater", "Calendar", "Graph Analysis", "Excalidraw"],
            "graph_colors": {
                "00-综合导航": "#FF6B6B",
                "01-前端开发": "#4ECDC4",
                "02-后端开发": "#45B7D1",
                "03-数据库与缓存": "#96CEB4",
                "04-分布式与中间件": "#FFEAA7",
                "05-云原生与运维": "#DDA0DD",
                "06-计算机基础": "#98D8C8",
                "07-通用工具": "#F7DC6F",
                "08-Python全栈": "#BB8FCE",
                "09-AI与效率工具": "#85C1E9",
                "99-项目实战": "#F8B500",
            },
        },
        "templates": {
            "dir": None,  # 自定义模板目录，为 None 时使用默认 assets 目录
        },
    }

    if config_path and os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                user_config = yaml.safe_load(f)
            if user_config:
                _deep_merge(config, user_config)
                print(f"✅ 已加载配置文件: {config_path}")
        except yaml.YAMLError as e:
            print(f"⚠️  配置文件解析失败，使用默认配置: {e}")
        except Exception as e:
            print(f"⚠️  配置文件读取失败，使用默认配置: {e}")
    elif config_path:
        print(f"⚠️  配置文件不存在，使用默认配置: {config_path}")

    return config


def _deep_merge(base: dict, override: dict) -> None:
    """深度合并两个字典，override 覆盖 base 中的值"""
    for key, value in override.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            _deep_merge(base[key], value)
        else:
            base[key] = value


def get_categories(config: dict) -> list:
    """
    从配置中获取分类列表

    Returns:
        [(id, name, desc), ...] 格式的分类列表
    """
    categories = []
    for cat in config.get("structure", {}).get("categories", []):
        categories.append((cat["id"], cat["name"], cat.get("desc", "")))
    return categories


def get_category_map(config: dict) -> dict:
    """
    从配置中获取分类映射（分类名 -> 目录名）

    Returns:
        {"前端开发": "01-前端开发", ...} 格式的映射
    """
    category_map = {}
    for cat in config.get("structure", {}).get("categories", []):
        category_map[cat["name"]] = f"{cat['id']}-{cat['name']}"
    return category_map


def get_template_dir(config: dict, skill_root: str) -> str:
    """
    获取模板目录路径

    Args:
        config: 配置字典
        skill_root: Skill 根目录（用于定位默认 assets 目录）

    Returns:
        模板目录路径
    """
    custom_dir = config.get("templates", {}).get("dir")
    if custom_dir:
        if os.path.isabs(custom_dir):
            return custom_dir
        return os.path.abspath(custom_dir)
    return os.path.join(skill_root, "assets")


def get_difficulty_stars(config: dict, level: int) -> str:
    """
    根据难度等级获取星级

    Args:
        config: 配置字典
        level: 难度等级 1-5

    Returns:
        星级字符串
    """
    levels = config.get("difficulty", {}).get("levels", {})
    stars_list = list(levels.keys())
    if 1 <= level <= len(stars_list):
        return stars_list[level - 1]
    return "⭐⭐⭐"


def validate_config(config: dict) -> list:
    """
    验证配置文件的完整性和合法性

    Returns:
        警告信息列表（空列表表示无问题）
    """
    warnings = []

    # 检查分类
    categories = config.get("structure", {}).get("categories", [])
    if not categories:
        warnings.append("未配置分类，将使用默认 12 分类")
    else:
        ids = [c["id"] for c in categories]
        if len(ids) != len(set(ids)):
            warnings.append("分类 ID 存在重复")
        if "00" not in ids:
            warnings.append("缺少 ID 为 00 的综合导航分类")

    # 检查 Frontmatter 必填字段
    required = config.get("frontmatter", {}).get("required", [])
    essential = ["title", "tags", "category", "difficulty"]
    for field in essential:
        if field not in required:
            warnings.append(f"Frontmatter 必填字段缺少: {field}")

    # 检查难度等级
    levels = config.get("difficulty", {}).get("levels", {})
    if len(levels) < 3:
        warnings.append(f"难度等级过少（当前 {len(levels)} 个），建议至少 3 个")

    return warnings


def find_config_in_kb(kb_root: str) -> Optional[str]:
    """
    在知识库根目录中查找配置文件

    Args:
        kb_root: 知识库根目录

    Returns:
        配置文件路径，未找到返回 None
    """
    candidates = [
        os.path.join(kb_root, ".kb-config.yaml"),
        os.path.join(kb_root, ".kb-config.yml"),
        os.path.join(kb_root, "kb-config.yaml"),
        os.path.join(kb_root, "kb-config.yml"),
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return None


def export_default_config(output_path: str) -> None:
    """
    导出默认配置文件模板

    Args:
        output_path: 输出路径
    """
    config = load_config()
    # 转换为 YAML 友好的格式
    output = {
        "kb": config["kb"],
        "structure": config["structure"],
        "frontmatter": config["frontmatter"],
        "tags": config["tags"],
        "difficulty": config["difficulty"],
        "note_generation": config["note_generation"],
        "moc": config["moc"],
        "deadlink_fix": config["deadlink_fix"],
        "audit": config["audit"],
        "learning_path": config["learning_path"],
        "obsidian": config["obsidian"],
        "templates": {"dir": None, "_comment": "自定义模板目录路径，为 null 时使用默认 assets 目录"},
    }

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        yaml.dump(output, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    print(f"✅ 默认配置已导出: {output_path}")


if __name__ == "__main__":
    # 测试配置加载
    if len(sys.argv) > 1 and sys.argv[1] == "export":
        output = sys.argv[2] if len(sys.argv) > 2 else ".kb-config.yaml"
        export_default_config(output)
    else:
        config = load_config()
        print("默认配置加载成功")
        print(f"分类数量: {len(get_categories(config))}")
        print(f"分类映射: {list(get_category_map(config).keys())}")
        warnings = validate_config(config)
        if warnings:
            print("警告:")
            for w in warnings:
                print(f"  - {w}")
        else:
            print("配置验证通过")
