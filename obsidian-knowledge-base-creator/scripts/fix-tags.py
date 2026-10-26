#!/usr/bin/env python3
"""
标签统一工具
扫描知识库中所有标签，合并重复标签、统一大小写、映射到核心标签集

用法:
    python fix-tags.py --path "知识库路径"
    python fix-tags.py --path "./my-kb" --dry-run
"""

import os
import re
import argparse
from collections import defaultdict

# 核心标签映射表（将各种变体映射到标准标签）
TAG_MAPPING = {
    # 前端
    "vue": "Vue3", "vue3": "Vue3", "Vue": "Vue3", "vue.js": "Vue3",
    "react": "React", "React.js": "React",
    "js": "JavaScript", "Javascript": "JavaScript", "javascript": "JavaScript",
    "ts": "TypeScript", "Typescript": "TypeScript", "typescript": "TypeScript",
    "css": "CSS", "html": "HTML", "Html": "HTML",
    "前端": "前端", "frontend": "前端", "Frontend": "前端",

    # 后端
    "java": "Java", "Java": "Java",
    "spring": "SpringBoot", "springboot": "SpringBoot", "Spring Boot": "SpringBoot",
    "springcloud": "微服务", "Spring Cloud": "微服务",
    "后端": "后端", "backend": "后端",

    # 数据库
    "mysql": "MySQL", "Mysql": "MySQL",
    "redis": "Redis", "Redis": "Redis",
    "数据库": "数据库", "DataBase": "数据库",
    "缓存": "缓存", "cache": "缓存",

    # 分布式
    "kafka": "Kafka", "Kafka": "Kafka",
    "rabbitmq": "RabbitMQ", "RabbitMQ": "RabbitMQ",
    "mq": "消息队列", "MessageQueue": "消息队列",
    "分布式": "分布式", "Distributed": "分布式",
    "分布式事务": "分布式事务",
    "分布式锁": "分布式锁",

    # 云原生
    "docker": "Docker", "Docker": "Docker",
    "k8s": "Kubernetes", "kubernetes": "Kubernetes", "K8s": "Kubernetes",
    "云原生": "云原生", "CloudNative": "云原生",
    "devops": "DevOps", "DevOps": "DevOps",
    "运维": "运维", "Operations": "运维",

    # 计算机基础
    "网络": "计算机网络", "计算机网络": "计算机网络", "network": "计算机网络",
    "操作系统": "操作系统", "os": "操作系统", "OS": "操作系统",
    "数据结构": "数据结构", "DataStructure": "数据结构",
    "算法": "算法", "Algorithm": "算法",
    "http": "HTTP", "HTTP": "HTTP", "Http": "HTTP",

    # Python
    "python": "Python", "Python": "Python", "py": "Python",
    "fastapi": "FastAPI", "FastAPI": "FastAPI",
    "django": "Django", "Django": "Django",

    # AI
    "ai": "AI应用", "AI": "AI应用", "人工智能": "AI应用",
    "llm": "LLM", "大语言模型": "LLM", "大模型": "LLM",
    "rag": "RAG", "检索增强生成": "RAG",
    "agent": "Agent", "智能体": "Agent",
    "多模态": "多模态", "Multimodal": "多模态",
    "prompt": "Prompt工程", "提示词": "Prompt工程", "Prompt": "Prompt工程",
    "ai工程化": "AI工程化", "AI工程化": "AI工程化",

    # 通用
    "git": "Git", "Git": "Git",
    "效率工具": "效率工具", "工具": "效率工具",
    "面试": "面试", "Interview": "面试",
    "性能优化": "性能优化", "性能": "性能优化",
    "安全": "安全", "Security": "安全",
    "架构设计": "架构设计", "架构": "架构设计",
    "设计模式": "设计模式", "DesignPattern": "设计模式",
    "并发": "并发", "Concurrency": "并发",
    "jvm": "JVM", "JVM": "JVM",
    "异步": "异步", "Async": "异步",
    "测试": "测试", "Test": "测试",
    "工程化": "工程化",
    "可观测性": "可观测性",
    "限流熔断": "限流熔断",
    "nacos": "Nacos", "Nacos": "Nacos",
    "prometheus": "Prometheus", "Prometheus": "Prometheus",
    "linux": "Linux", "Linux": "Linux",
    "nginx": "Nginx", "Nginx": "Nginx",
    "elasticsearch": "Elasticsearch", "Elasticsearch": "Elasticsearch", "es": "Elasticsearch",
    "postgresql": "PostgreSQL", "PostgreSQL": "PostgreSQL", "pg": "PostgreSQL",
    "mongodb": "MongoDB", "MongoDB": "MongoDB", "mongo": "MongoDB",
    "zookeeper": "ZooKeeper", "ZooKeeper": "ZooKeeper", "zk": "ZooKeeper",
    "sentinel": "Sentinel", "Sentinel": "Sentinel",
    "istio": "Istio", "Istio": "Istio",
    "xxl-job": "任务调度", "XXL-Job": "任务调度",
    "skywalking": "可观测性", "SkyWalking": "可观测性",
}

def extract_tags(content: str) -> dict:
    """从Frontmatter提取标签"""
    match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return [], None
    fm_text = match.group(1)
    tags_match = re.search(r'^tags:\s*\[(.*?)\]', fm_text, re.MULTILINE)
    if not tags_match:
        return [], fm_text
    tags_str = tags_match.group(1)
    tags = [t.strip() for t in tags_str.split(',') if t.strip()]
    return tags, fm_text

def normalize_tag(tag: str) -> dict:
    """标准化单个标签"""
    # 先查映射表
    if tag in TAG_MAPPING:
        return TAG_MAPPING[tag]
    # 去掉首尾空格
    tag = tag.strip()
    # 统一常见格式
    tag_lower = tag.lower()
    if tag_lower in TAG_MAPPING:
        return TAG_MAPPING[tag_lower]
    return tag

def process_file(filepath: str, dry_run: str = False) -> tuple:
    """处理单个文件的标签"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return None, []

    tags, fm_text = extract_tags(content)
    if not tags:
        return None, []

    # 标准化标签
    normalized_tags = []
    changes = []
    for tag in tags:
        new_tag = normalize_tag(tag)
        if new_tag != tag:
            changes.append((tag, new_tag))
        if new_tag not in normalized_tags:
            normalized_tags.append(new_tag)

    if not changes and len(normalized_tags) == len(tags):
        return None, []

    # 替换Frontmatter中的标签
    old_tags_str = ', '.join(tags)
    new_tags_str = ', '.join(normalized_tags)
    new_content = content.replace(f'tags: [{old_tags_str}]', f'tags: [{new_tags_str}]')

    # 也处理可能的空格差异
    if new_content == content:
        # 尝试其他格式
        old_pattern = r'tags:\s*\[' + re.escape(old_tags_str) + r'\]'
        new_content = re.sub(old_pattern, f'tags: [{new_tags_str}]', content)

    if dry_run:
        return normalized_tags, changes

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return normalized_tags, changes

    return None, []

def main() -> None:
    """主函数"""
    parser = argparse.ArgumentParser(description="批量统一标签")
    parser.add_argument("--path", required=True, help="知识库路径")
    parser.add_argument("--dry-run", action="store_true", help="仅显示不执行")
    args = parser.parse_args()

    kb_root = os.path.abspath(args.path)
    if not os.path.exists(kb_root):
        print(f"❌ 路径不存在: {kb_root}")
        return

    print(f"🏷️  标签统一工具: {kb_root}")
    if args.dry_run:
        print("  (预览模式，不修改文件)")
    print("=" * 60)

    # 扫描所有文件
    all_tags = defaultdict(int)
    tag_files = defaultdict(list)
    md_files = []

    for root, dirs, files in os.walk(kb_root):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                md_files.append(filepath)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    tags, _ = extract_tags(content)
                    for tag in tags:
                        all_tags[tag] += 1
                        tag_files[tag].append(file)
                except:
                    pass

    print(f"\n📝 发现 {len(md_files)} 个 Markdown 文件")
    print(f"🏷️  发现 {len(all_tags)} 个不同标签\n")

    # 显示需要统一的标签
    print("🔄 需要统一的标签:")
    need_fix = []
    for tag, count in sorted(all_tags.items(), key=lambda x: x[1], reverse=True):
        normalized = normalize_tag(tag)
        if normalized != tag:
            need_fix.append((tag, normalized, count))
            print(f"  {tag} ({count}次) → {normalized}")

    if not need_fix:
        print("  ✅ 所有标签已统一，无需修改")
        return

    print(f"\n📊 共 {len(need_fix)} 个标签需要统一")

    # 处理文件
    print(f"\n🔧 处理文件中...")
    changed_files = 0
    total_changes = 0

    for filepath in md_files:
        filename = os.path.basename(filepath)
        new_tags, changes = process_file(filepath, args.dry_run)
        if changes:
            changed_files += 1
            total_changes += len(changes)
            if args.dry_run:
                print(f"  📄 {filename}: {len(changes)} 处修改")
                for old, new in changes:
                    print(f"     {old} → {new}")

    print(f"\n" + "=" * 60)
    print(f"📊 处理完成:")
    print(f"  修改文件数: {changed_files}")
    print(f"  总修改数: {total_changes}")
    if args.dry_run:
        print(f"\n💡 这是预览模式，去掉 --dry-run 参数以执行修改")

if __name__ == "__main__":
    main()
