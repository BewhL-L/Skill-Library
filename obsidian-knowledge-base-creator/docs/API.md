# API 参考文档

## 📋 概述

本文档提供 Obsidian 知识库标准化生成器所有脚本函数的 API 参考，包括函数签名、参数说明、返回值和使用示例。

---

## 📁 模块概览

| 模块 | 文件 | 主要功能 |
|------|------|---------|
| CLI 入口 | `scripts/kb.py` | 命令行接口，参数解析，命令分发 |
| 初始化 | `scripts/init-kb.py` | 知识库目录结构初始化 |
| 笔记生成 | `scripts/generate-note.py` | 标准化笔记生成 |
| MOC 生成 | `scripts/generate-moc.py` | MOC 内容地图生成 |
| 健康检查 | `scripts/audit-kb.py` | 知识库健康检查 |
| 质量校验 | `scripts/validate-kb.py` | 笔记质量校验 |
| Frontmatter 修复 | `scripts/fix-frontmatter.py` | Frontmatter 批量补全 |
| 死链修复 | `scripts/fix-links.py` | 死链自动修复 |
| 标签统一 | `scripts/fix-tags.py` | 标签批量统一 |
| 一键标准化 | `scripts/standardize.py` | 一键标准化流程 |

---

## 🎯 kb.py - CLI 入口模块

### main()

**函数签名**：
```python
def main() -> None:
```

**功能**：主入口函数，解析命令行参数并分发到对应子命令。

**参数**：无

**返回值**：无

**使用示例**：
```python
if __name__ == "__main__":
    main()
```

---

### create_parser()

**函数签名**：
```python
def create_parser() -> argparse.ArgumentParser:
```

**功能**：创建命令行参数解析器，定义所有子命令和参数。

**参数**：无

**返回值**：
- `argparse.ArgumentParser` - 配置好的参数解析器

**使用示例**：
```python
parser = create_parser()
args = parser.parse_args(["init", "--name", "测试", "--path", "./test"])
```

---

### cmd_init(args: argparse.Namespace) -> None

**函数签名**：
```python
def cmd_init(args: argparse.Namespace) -> None:
```

**功能**：初始化知识库命令处理。

**参数**：
- `args.name` (str) - 知识库名称
- `args.path` (str) - 输出路径
- `args.theme` (str) - 知识库主题

**返回值**：无

**使用示例**：
```python
args = parser.parse_args(["init", "--name", "我的知识库", "--path", "./my-kb", "--theme", "全栈+AI"])
cmd_init(args)
```

---

### cmd_note(args: argparse.Namespace) -> None

**函数签名**：
```python
def cmd_note(args: argparse.Namespace) -> None:
```

**功能**：生成单篇标准化笔记命令处理。

**参数**：
- `args.title` (str) - 笔记标题
- `args.category` (str) - 分类名称
- `args.difficulty` (int) - 难度等级（1-5）
- `args.tags` (list) - 标签列表
- `args.kb_root` (str) - 知识库根目录
- `args.pre` (list) - 前置知识列表

**返回值**：无

---

### cmd_batch_note(args: argparse.Namespace) -> None

**函数签名**：
```python
def cmd_batch_note(args: argparse.Namespace) -> None:
```

**功能**：批量生成笔记命令处理。

**参数**：
- `args.list` (str) - JSON/YAML 列表文件路径
- `args.kb_root` (str) - 知识库根目录

**返回值**：无

---

### cmd_moc(args: argparse.Namespace) -> None

**函数签名**：
```python
def cmd_moc(args: argparse.Namespace) -> None:
```

**功能**：生成/更新 MOC 内容地图命令处理。

**参数**：
- `args.category` (str) - 分类名称
- `args.path` (str) - 目标目录路径

**返回值**：无

---

### cmd_audit(args: argparse.Namespace) -> None

**函数签名**：
```python
def cmd_audit(args: argparse.Namespace) -> None:
```

**功能**：知识库健康检查命令处理。

**参数**：
- `args.path` (str) - 知识库路径
- `args.format` (str) - 输出格式（text/json/csv）
- `args.quiet` (bool) - 安静模式

**返回值**：无

---

### cmd_validate(args: argparse.Namespace) -> None

**函数签名**：
```python
def cmd_validate(args: argparse.Namespace) -> None:
```

**功能**：笔记质量校验命令处理。

**参数**：
- `args.path` (str) - 知识库路径
- `args.strict` (bool) - 严格模式
- `args.check` (list) - 检查项列表

**返回值**：无

---

### cmd_fix_fm(args: argparse.Namespace) -> None

**函数签名**：
```python
def cmd_fix_fm(args: argparse.Namespace) -> None:
```

**功能**：批量补全 Frontmatter 命令处理。

**参数**：
- `args.kb_root` (str) - 知识库根目录
- `args.path` (str) - 目标目录路径
- `args.dry_run` (bool) - 预览模式
- `args.backup` (bool) - 备份原文件

**返回值**：无

---

### cmd_fix_link(args: argparse.Namespace) -> None

**函数签名**：
```python
def cmd_fix_link(args: argparse.Namespace) -> None:
```

**功能**：自动修复高频死链命令处理。

**参数**：
- `args.kb_root` (str) - 知识库根目录
- `args.threshold` (int) - 死链修复阈值（引用次数）
- `args.dry_run` (bool) - 预览模式

**返回值**：无

---

### cmd_fix_tags(args: argparse.Namespace) -> None

**函数签名**：
```python
def cmd_fix_tags(args: argparse.Namespace) -> None:
```

**功能**：批量统一标签命令处理。

**参数**：
- `args.kb_root` (str) - 知识库根目录
- `args.path` (str) - 目标目录路径
- `args.dry_run` (bool) - 预览模式
- `args.report` (bool) - 输出变更报告

**返回值**：无

---

### cmd_standardize(args: argparse.Namespace) -> None

**函数签名**：
```python
def cmd_standardize(args: argparse.Namespace) -> None:
```

**功能**：一键标准化命令处理（fix-fm → fix-link → 生成MOC → audit）。

**参数**：
- `args.kb_root` (str) - 知识库根目录
- `args.threshold` (int) - 死链修复阈值
- `args.dry_run` (bool) - 预览模式

**返回值**：无

---

### cmd_progress(args: argparse.Namespace) -> None

**函数签名**：
```python
def cmd_progress(args: argparse.Namespace) -> None:
```

**功能**：生成学习进度报告命令处理。

**参数**：
- `args.kb_root` (str) - 知识库根目录
- `args.format` (str) - 输出格式

**返回值**：无

---

### cmd_info(args: argparse.Namespace) -> None

**函数签名**：
```python
def cmd_info(args: argparse.Namespace) -> None:
```

**功能**：显示帮助信息命令处理。

**参数**：无

**返回值**：无

---

## 📝 scripts/init-kb.py - 初始化模块

### init_knowledge_base(name: str, path: str, theme: str) -> Dict[str, Any]

**函数签名**：
```python
def init_knowledge_base(name: str, path: str, theme: str) -> Dict[str, Any]:
```

**功能**：初始化知识库目录结构和核心文件。

**参数**：
- `name` (str) - 知识库名称
- `path` (str) - 输出路径
- `theme` (str) - 知识库主题

**返回值**：
- `Dict[str, Any]` - 初始化结果统计
  - `directories_created` (int) - 创建的目录数
  - `files_created` (int) - 创建的文件数
  - `home_path` (str) - Home 首页路径
  - `moc_paths` (List[str]) - MOC 文件路径列表

**使用示例**：
```python
from scripts.init_kb import init_knowledge_base

result = init_knowledge_base(
    name="我的知识库",
    path="./my-kb",
    theme="全栈+AI"
)
print(f"创建了 {result['directories_created']} 个目录")
print(f"创建了 {result['files_created']} 个文件")
```

---

### create_directory_structure(base_path: str) -> List[str]

**函数签名**：
```python
def create_directory_structure(base_path: str) -> List[str]:
```

**功能**：创建 12 个顶级分类目录结构。

**参数**：
- `base_path` (str) - 基础路径

**返回值**：
- `List[str]` - 创建的目录路径列表

---

## 📄 scripts/generate-note.py - 笔记生成模块

### generate_note(title: str, category: str, difficulty: int, tags: List[str] = None, pre: List[str] = None, output_path: str = None) -> str

**函数签名**：
```python
def generate_note(
    title: str,
    category: str,
    difficulty: int,
    tags: List[str] = None,
    pre: List[str] = None,
    output_path: str = None
) -> str:
```

**功能**：生成符合五段式结构的标准化笔记。

**参数**：
- `title` (str) - 笔记标题
- `category` (str) - 分类名称
- `difficulty` (int) - 难度等级（1-5）
- `tags` (List[str], optional) - 标签列表，默认为 None
- `pre` (List[str], optional) - 前置知识列表，默认为 None
- `output_path` (str, optional) - 输出文件路径，默认为 None（自动生成）

**返回值**：
- `str` - 生成的笔记文件路径

**使用示例**：
```python
from scripts.generate_note import generate_note

note_path = generate_note(
    title="Vue3 响应式原理",
    category="前端开发",
    difficulty=3,
    tags=["Vue3", "前端", "响应式"],
    pre=["Vue3基础"],
    output_path="./my-kb/01-前端开发/Vue3响应式原理.md"
)
print(f"笔记已生成: {note_path}")
```

---

### generate_frontmatter(title: str, category: str, difficulty: int, tags: List[str], pre: List[str]) -> str

**函数签名**：
```python
def generate_frontmatter(
    title: str,
    category: str,
    difficulty: int,
    tags: List[str],
    pre: List[str]
) -> str:
```

**功能**：生成标准化的 YAML Frontmatter。

**参数**：
- `title` (str) - 笔记标题
- `category` (str) - 分类名称
- `difficulty` (int) - 难度等级（1-5）
- `tags` (List[str]) - 标签列表
- `pre` (List[str]) - 前置知识列表

**返回值**：
- `str` - YAML Frontmatter 字符串

---

## 🗺️ scripts/generate-moc.py - MOC 生成模块

### generate_moc(category: str, directory_path: str) -> str

**函数签名**：
```python
def generate_moc(category: str, directory_path: str) -> str:
```

**功能**：扫描目录下所有笔记，生成标准化 MOC 内容地图。

**参数**：
- `category` (str) - 分类名称
- `directory_path` (str) - 目标目录路径

**返回值**：
- `str` - 生成的 MOC 文件路径

**使用示例**：
```python
from scripts.generate_moc import generate_moc

moc_path = generate_moc(
    category="前端开发",
    directory_path="./my-kb/01-前端开发"
)
print(f"MOC 已生成: {moc_path}")
```

---

### scan_notes(directory_path: str) -> List[Dict[str, Any]]

**函数签名**：
```python
def scan_notes(directory_path: str) -> List[Dict[str, Any]]:
```

**功能**：扫描目录下所有 Markdown 笔记，解析 Frontmatter。

**参数**：
- `directory_path` (str) - 目录路径

**返回值**：
- `List[Dict[str, Any]]` - 笔记信息列表
  - `path` (str) - 文件路径
  - `title` (str) - 笔记标题
  - `difficulty` (str) - 难度星级
  - `status` (str) - 状态
  - `priority` (str) - 优先级
  - `tags` (List[str]) - 标签列表

---

## 🔍 scripts/audit-kb.py - 健康检查模块

### audit_knowledge_base(kb_path: str, format: str = "text") -> Dict[str, Any]

**函数签名**：
```python
def audit_knowledge_base(kb_path: str, format: str = "text") -> Dict[str, Any]:
```

**功能**：对知识库进行全面健康检查。

**参数**：
- `kb_path` (str) - 知识库路径
- `format` (str) - 输出格式（text/json/csv），默认为 "text"

**返回值**：
- `Dict[str, Any]` - 健康检查结果
  - `total_notes` (int) - 总笔记数
  - `frontmatter_issues` (List[Dict]) - Frontmatter 问题列表
  - `tag_issues` (List[Dict]) - 标签问题列表
  - `dead_links` (List[Dict]) - 死链列表
  - `orphan_notes` (List[Dict]) - 孤立文档列表
  - `moc_coverage` (Dict) - MOC 覆盖率统计
  - `health_score` (float) - 健康评分（0-100）

**使用示例**：
```python
from scripts.audit_kb import audit_knowledge_base

result = audit_knowledge_base("./my-kb", format="json")
print(f"总笔记数: {result['total_notes']}")
print(f"健康评分: {result['health_score']}")
print(f"死链数: {len(result['dead_links'])}")
```

---

### check_frontmatter(file_path: str) -> List[Dict[str, str]]

**函数签名**：
```python
def check_frontmatter(file_path: str) -> List[Dict[str, str]]:
```

**功能**：检查单个文件的 Frontmatter 完整性。

**参数**：
- `file_path` (str) - 文件路径

**返回值**：
- `List[Dict[str, str]]` - 问题列表
  - `field` (str) - 缺失的字段名
  - `severity` (str) - 严重程度（error/warning）
  - `message` (str) - 问题描述

---

## ✅ scripts/validate-kb.py - 质量校验模块

### validate_note(file_path: str, strict: bool = False) -> Dict[str, Any]

**函数签名**：
```python
def validate_note(file_path: str, strict: bool = False) -> Dict[str, Any]:
```

**功能**：校验单篇笔记是否符合规范。

**参数**：
- `file_path` (str) - 文件路径
- `strict` (bool) - 严格模式，默认为 False

**返回值**：
- `Dict[str, Any]` - 校验结果
  - `valid` (bool) - 是否通过校验
  - `errors` (List[Dict]) - 错误列表
  - `warnings` (List[Dict]) - 警告列表
  - `structure_check` (Dict) - 结构检查结果
  - `formatting_check` (Dict) - 排版检查结果

---

## 🔧 scripts/fix-frontmatter.py - Frontmatter 修复模块

### fix_frontmatter_batch(kb_path: str, dry_run: bool = False, backup: bool = False) -> Dict[str, Any]

**函数签名**：
```python
def fix_frontmatter_batch(
    kb_path: str,
    dry_run: bool = False,
    backup: bool = False
) -> Dict[str, Any]:
```

**功能**：批量补全知识库中所有笔记的 Frontmatter 缺失字段。

**参数**：
- `kb_path` (str) - 知识库根目录
- `dry_run` (bool) - 预览模式，不实际修改文件，默认为 False
- `backup` (bool) - 备份原文件，默认为 False

**返回值**：
- `Dict[str, Any]` - 修复结果统计
  - `total_files` (int) - 总文件数
  - `files_fixed` (int) - 修复的文件数
  - `fields_added` (int) - 添加的字段数
  - `changes` (List[Dict]) - 变更详情列表

---

## 🔗 scripts/fix-links.py - 死链修复模块

### fix_dead_links(kb_path: str, threshold: int = 5, dry_run: bool = False) -> Dict[str, Any]

**函数签名**：
```python
def fix_dead_links(
    kb_path: str,
    threshold: int = 5,
    dry_run: bool = False
) -> Dict[str, Any]:
```

**功能**：自动修复高频死链，为高频死链创建对应笔记。

**参数**：
- `kb_path` (str) - 知识库根目录
- `threshold` (int) - 死链修复阈值（引用次数），默认为 5
- `dry_run` (bool) - 预览模式，默认为 False

**返回值**：
- `Dict[str, Any]` - 修复结果
  - `total_dead_links` (int) - 总死链数
  - `high_frequency_dead_links` (int) - 高频死链数
  - `notes_created` (int) - 创建的笔记数
  - `created_notes` (List[Dict]) - 创建的笔记详情

---

## 🏷️ scripts/fix-tags.py - 标签统一模块

### fix_tags_batch(kb_path: str, dry_run: bool = False, report: bool = False) -> Dict[str, Any]

**函数签名**：
```python
def fix_tags_batch(
    kb_path: str,
    dry_run: bool = False,
    report: bool = False
) -> Dict[str, Any]:
```

**功能**：批量统一知识库中的标签体系。

**参数**：
- `kb_path` (str) - 知识库根目录
- `dry_run` (bool) - 预览模式，默认为 False
- `report` (bool) - 输出变更报告，默认为 False

**返回值**：
- `Dict[str, Any]` - 修复结果
  - `total_files` (int) - 总文件数
  - `files_modified` (int) - 修改的文件数
  - `tags_renamed` (int) - 重命名的标签数
  - `tags_removed` (int) - 删除的标签数
  - `tag_mapping` (Dict) - 标签映射详情

---

## 🚀 scripts/standardize.py - 一键标准化模块

### standardize_knowledge_base(kb_path: str, threshold: int = 5, dry_run: bool = False) -> Dict[str, Any]

**函数签名**：
```python
def standardize_knowledge_base(
    kb_path: str,
    threshold: int = 5,
    dry_run: bool = False
) -> Dict[str, Any]:
```

**功能**：一键完成知识库标准化全流程。

**执行流程**：
1. `fix_frontmatter_batch()` - 补全 Frontmatter
2. `fix_dead_links()` - 修复高频死链
3. `fix_tags_batch()` - 统一标签体系
4. `generate_moc()` - 生成所有 MOC
5. `audit_knowledge_base()` - 健康检查并输出报告

**参数**：
- `kb_path` (str) - 知识库根目录
- `threshold` (int) - 死链修复阈值，默认为 5
- `dry_run` (bool) - 预览模式，默认为 False

**返回值**：
- `Dict[str, Any]` - 标准化结果
  - `frontmatter_result` (Dict) - Frontmatter 修复结果
  - `dead_links_result` (Dict) - 死链修复结果
  - `tags_result` (Dict) - 标签统一结果
  - `moc_result` (Dict) - MOC 生成结果
  - `audit_result` (Dict) - 健康检查结果
  - `total_time` (float) - 总耗时（秒）

**使用示例**：
```python
from scripts.standardize import standardize_knowledge_base

result = standardize_knowledge_base(
    kb_path="./my-kb",
    threshold=5,
    dry_run=False
)
print(f"标准化完成，总耗时: {result['total_time']:.2f}秒")
print(f"健康评分: {result['audit_result']['health_score']}")
```

---

## 📊 通用工具函数

### parse_frontmatter(content: str) -> Tuple[Dict[str, Any], str]

**函数签名**：
```python
def parse_frontmatter(content: str) -> Tuple[Dict[str, Any], str]:
```

**功能**：解析 Markdown 内容中的 YAML Frontmatter。

**参数**：
- `content` (str) - Markdown 文件内容

**返回值**：
- `Tuple[Dict[str, Any], str]` - (Frontmatter 字典, 正文内容)

**使用示例**：
```python
from scripts.utils import parse_frontmatter

with open("note.md", "r", encoding="utf-8") as f:
    content = f.read()

frontmatter, body = parse_frontmatter(content)
print(f"标题: {frontmatter.get('title')}")
print(f"标签: {frontmatter.get('tags')}")
```

---

### find_markdown_files(directory: str) -> List[str]

**函数签名**：
```python
def find_markdown_files(directory: str) -> List[str]:
```

**功能**：递归查找目录下所有 Markdown 文件。

**参数**：
- `directory` (str) - 目录路径

**返回值**：
- `List[str]` - Markdown 文件路径列表

---

### extract_wiki_links(content: str) -> List[str]

**函数签名**：
```python
def extract_wiki_links(content: str) -> List[str]:
```

**功能**：从 Markdown 内容中提取所有 Wiki 风格链接 `[[链接]]`。

**参数**：
- `content` (str) - Markdown 内容

**返回值**：
- `List[str]` - 链接目标列表

---

## 📝 数据类型定义

### NoteInfo

```python
class NoteInfo(TypedDict):
    path: str
    title: str
    category: str
    difficulty: str
    status: str
    priority: str
    tags: List[str]
    created: str
    updated: str
    pre: List[str]
    aliases: List[str]
```

### AuditResult

```python
class AuditResult(TypedDict):
    total_notes: int
    frontmatter_issues: List[Dict[str, str]]
    tag_issues: List[Dict[str, str]]
    dead_links: List[Dict[str, Any]]
    orphan_notes: List[str]
    moc_coverage: Dict[str, Any]
    health_score: float
```

---

## 📞 相关文档

- [ARCHITECTURE.md](ARCHITECTURE.md) - 项目架构设计
- [TESTING.md](TESTING.md) - 测试策略与指南
- [DEBUGGING.md](DEBUGGING.md) - 调试与问题排查
- [TEMPLATES.md](TEMPLATES.md) - 模板使用指南

---

> **最后更新**：2026-08-30
>
> **适用版本**：v3.1.0
