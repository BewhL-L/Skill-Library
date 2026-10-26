# API 参考文档

> 自动生成于 2026-09-01 21:48

## 📋 函数索引

共 100 个函数，分布在 6 个文件中。

| 文件 | 函数数 |
|------|--------|
| [audit-skill.py](#audit-skillpy) | 22 |
| [generate-docs.py](#generate-docspy) | 10 |
| [generate-tests.py](#generate-testspy) | 11 |
| [optimize-skill.py](#optimize-skillpy) | 27 |
| [skill-opt.py](#skill-optpy) | 18 |
| [skill_type_detector.py](#skill_type_detectorpy) | 12 |

---

## audit-skill.py

### `main() -> None`

*暂无文档说明*

**参数:**
- 无

**返回值:** `None`

---
### `__init__(self, skill_path: str) -> None`

*暂无文档说明*

**参数:**
- `self`
- `skill_path: str`

**返回值:** `None`

---
### `audit(self) -> Dict`

执行完整审计

**参数:**
- `self`

**返回值:** `Dict`

---
### `_check_metadata(self) -> None`

检查元数据完整性

**参数:**
- `self`

**返回值:** `None`

---
### `_check_documentation(self) -> None`

检查文档完整性（含Markdown格式检查）

**参数:**
- `self`

**返回值:** `None`

---
### `_check_markdown_format(self) -> List[Dict]`

检查 Markdown 文档格式（表格列数一致性、双链格式有效性）

**参数:**
- `self`

**返回值:** `List[Dict]`

---
### `_clean_table_pipes(line: str) -> str`

清理表格行中的管道符，排除转义的 \| 和双链内的 |

**参数:**
- `line: str`

**返回值:** `str`

---
### `_check_code_quality(self) -> None`

检查代码质量（含py_compile验证、修复类型注解检测）

**参数:**
- `self`

**返回值:** `None`

---
### `_check_testing(self) -> None`

检查测试覆盖

**参数:**
- `self`

**返回值:** `None`

---
### `_check_engineering(self) -> None`

检查工程化配置

**参数:**
- `self`

**返回值:** `None`

---
### `_check_templates(self) -> None`

检查模板资源

**参数:**
- `self`

**返回值:** `None`

---
### `_check_usability(self) -> None`

检查易用性

**参数:**
- `self`

**返回值:** `None`

---
### `_check_maintainability(self) -> None`

检查可维护性

**参数:**
- `self`

**返回值:** `None`

---
### `_check_doc_structure(self) -> None`

检查 SKILL.md 结构完整性（纯文档型专属）

**参数:**
- `self`

**返回值:** `None`

---
### `_check_trigger_scenarios(self) -> None`

检查触发场景覆盖度（纯文档型专属）

**参数:**
- `self`

**返回值:** `None`

---
### `_check_output_spec(self) -> None`

检查输出规范明确性（纯文档型专属）

**参数:**
- `self`

**返回值:** `None`

---
### `_check_references_depth(self) -> None`

检查 references 深度（纯文档型专属）

**参数:**
- `self`

**返回值:** `None`

---
### `_calculate_score(self) -> None`

计算总分（按 Skill 类型使用动态权重）

**参数:**
- `self`

**返回值:** `None`

---
### `_get_default_weights(self) -> Dict[str, float]`

获取默认权重（代码驱动型）

**参数:**
- `self`

**返回值:** `Dict[str, float]`

---
### `_generate_suggestions(self) -> None`

生成优化建议（按 Skill 类型）

**参数:**
- `self`

**返回值:** `None`

---
### `print_report(self) -> None`

打印审计报告

**参数:**
- `self`

**返回值:** `None`

---
### `save_report(self, output_path: str) -> None`

保存报告到文件

**参数:**
- `self`
- `output_path: str`

**返回值:** `None`

---

## generate-docs.py

### `main() -> None`

*暂无文档说明*

**参数:**
- 无

**返回值:** `None`

---
### `__init__(self, skill_path: str) -> None`

*暂无文档说明*

**参数:**
- `self`
- `skill_path: str`

**返回值:** `None`

---
### `generate(self, doc_type: str) -> None`

生成文档（按 Skill 类型自适应）

**参数:**
- `self`
- `doc_type: str`

**返回值:** `None`

---
### `_get_python_files(self) -> List[Path]`

获取所有 Python 文件

**参数:**
- `self`

**返回值:** `List[Path]`

---
### `_parse_functions(self, filepath: Path) -> List[Dict]`

解析 Python 文件中的函数

**参数:**
- `self`
- `filepath: Path`

**返回值:** `List[Dict]`

---
### `_generate_api_docs(self) -> None`

生成 API 参考文档

**参数:**
- `self`

**返回值:** `None`

---
### `_generate_faq(self) -> None`

生成常见问题文档

**参数:**
- `self`

**返回值:** `None`

---
### `_generate_examples(self) -> None`

生成使用示例文档

**参数:**
- `self`

**返回值:** `None`

---
### `_generate_architecture(self) -> None`

生成架构文档

**参数:**
- `self`

**返回值:** `None`

---
### `print_summary(self) -> None`

打印生成摘要

**参数:**
- `self`

**返回值:** `None`

---

## generate-tests.py

### `main() -> None`

*暂无文档说明*

**参数:**
- 无

**返回值:** `None`

---
### `__init__(self, skill_path: str) -> None`

*暂无文档说明*

**参数:**
- `self`
- `skill_path: str`

**返回值:** `None`

---
### `generate(self, test_type: str) -> None`

生成测试（纯文档型自动跳过）

**参数:**
- `self`
- `test_type: str`

**返回值:** `None`

---
### `_get_python_files(self) -> List[Path]`

获取所有 Python 文件

**参数:**
- `self`

**返回值:** `List[Path]`

---
### `_parse_functions(self, filepath: Path) -> List[Dict]`

解析 Python 文件中的函数

**参数:**
- `self`
- `filepath: Path`

**返回值:** `List[Dict]`

---
### `_sanitize_module_name(self, raw_name: str) -> Dict[str, str]`

清理模块名，生成合法的 Python 标识符

Args:
    raw_name: 原始模块名（可能包含连字符，如 "audit-kb"）

Returns:
    {
        "snake": "audit_kb",      # 下划线版本，用于文件名和导入
        "pascal": "AuditKb",      # PascalCase 版本，用于类名
        "original": "audit-kb",    # 原始名称，用于显示
    }

**参数:**
- `self`
- `raw_name: str`

**返回值:** `Dict[str, str]`

---
### `_generate_unit_tests(self) -> None`

生成单元测试

**参数:**
- `self`

**返回值:** `None`

---
### `_generate_integration_tests(self) -> None`

生成集成测试

**参数:**
- `self`

**返回值:** `None`

---
### `_generate_conftest(self) -> None`

生成 conftest.py

**参数:**
- `self`

**返回值:** `None`

---
### `_generate_coverage_config(self) -> None`

生成覆盖率配置

**参数:**
- `self`

**返回值:** `None`

---
### `print_summary(self) -> None`

打印生成摘要

**参数:**
- `self`

**返回值:** `None`

---

## optimize-skill.py

### `main() -> None`

*暂无文档说明*

**参数:**
- 无

**返回值:** `None`

---
### `__init__(self, skill_path: str, dry_run: bool) -> None`

*暂无文档说明*

**参数:**
- `self`
- `skill_path: str`
- `dry_run: bool`

**返回值:** `None`

---
### `optimize(self, only: Optional[List[str]]) -> Dict`

执行自动优化（按 Skill 类型自适应）

**参数:**
- `self`
- `only: Optional[List[str]]`

**返回值:** `Dict`

---
### `_write_file(self, filepath: Path, content: str, description: str) -> None`

写入文件（支持 dry-run）

**参数:**
- `self`
- `filepath: Path`
- `content: str`
- `description: str`

**返回值:** `None`

---
### `_optimize_docs(self) -> None`

优化文档

**参数:**
- `self`

**返回值:** `None`

---
### `_optimize_code(self) -> None`

优化代码

**参数:**
- `self`

**返回值:** `None`

---
### `_optimize_basic_config(self) -> None`

优化基础配置（纯文档型专用：只创建 .gitignore 和 .editorconfig）

**参数:**
- `self`

**返回值:** `None`

---
### `_optimize_config(self) -> None`

优化工程化配置（代码驱动型/混合型：创建完整工程化配置）

**参数:**
- `self`

**返回值:** `None`

---
### `_get_skill_name(self) -> str`

从 SKILL.md 获取 Skill 名称

**参数:**
- `self`

**返回值:** `str`

---
### `_generate_readme(self) -> str`

*暂无文档说明*

**参数:**
- `self`

**返回值:** `str`

---
### `_generate_quickstart(self) -> str`

*暂无文档说明*

**参数:**
- `self`

**返回值:** `str`

---
### `_generate_changelog(self) -> str`

*暂无文档说明*

**参数:**
- `self`

**返回值:** `str`

---
### `_generate_faq(self) -> str`

*暂无文档说明*

**参数:**
- `self`

**返回值:** `str`

---
### `_generate_contributing(self) -> str`

*暂无文档说明*

**参数:**
- `self`

**返回值:** `str`

---
### `_generate_security(self) -> str`

*暂无文档说明*

**参数:**
- `self`

**返回值:** `str`

---
### `_generate_code_of_conduct(self) -> str`

*暂无文档说明*

**参数:**
- `self`

**返回值:** `str`

---
### `_generate_installation(self) -> str`

*暂无文档说明*

**参数:**
- `self`

**返回值:** `str`

---
### `_generate_use_cases(self) -> str`

*暂无文档说明*

**参数:**
- `self`

**返回值:** `str`

---
### `_generate_support(self) -> str`

*暂无文档说明*

**参数:**
- `self`

**返回值:** `str`

---
### `_generate_gitignore(self) -> str`

*暂无文档说明*

**参数:**
- `self`

**返回值:** `str`

---
### `_generate_editorconfig(self) -> str`

*暂无文档说明*

**参数:**
- `self`

**返回值:** `str`

---
### `_generate_precommit(self) -> str`

*暂无文档说明*

**参数:**
- `self`

**返回值:** `str`

---
### `_generate_pyproject(self) -> str`

*暂无文档说明*

**参数:**
- `self`

**返回值:** `str`

---
### `_generate_makefile(self) -> str`

*暂无文档说明*

**参数:**
- `self`

**返回值:** `str`

---
### `_generate_requirements(self) -> str`

*暂无文档说明*

**参数:**
- `self`

**返回值:** `str`

---
### `_generate_ci(self) -> str`

*暂无文档说明*

**参数:**
- `self`

**返回值:** `str`

---
### `print_summary(self) -> None`

打印优化摘要

**参数:**
- `self`

**返回值:** `None`

---

## skill-opt.py

### `_load_module(module_name: str, filename: str) -> None`

动态加载带连字符的 Python 模块（如 audit-skill.py）
因为 Python import 不支持连字符文件名

**参数:**
- `module_name: str`
- `filename: str`

**返回值:** `None`

---
### `_get_auditor() -> None`

*暂无文档说明*

**参数:**
- 无

**返回值:** `None`

---
### `_get_optimizer() -> None`

*暂无文档说明*

**参数:**
- 无

**返回值:** `None`

---
### `_get_doc_generator() -> None`

*暂无文档说明*

**参数:**
- 无

**返回值:** `None`

---
### `_get_test_generator() -> None`

*暂无文档说明*

**参数:**
- 无

**返回值:** `None`

---
### `_get_type_detector() -> None`

*暂无文档说明*

**参数:**
- 无

**返回值:** `None`

---
### `_detect_skill_type(skill_path: str) -> str`

检测 Skill 类型

**参数:**
- `skill_path: str`

**返回值:** `str`

---
### `_validate_skill_path(skill_path: str, require_skill_md: bool) -> bool`

验证 Skill 路径是否有效

Args:
    skill_path: Skill 目录路径
    require_skill_md: 是否要求存在 SKILL.md

Returns:
    True 表示路径有效，False 表示无效

**参数:**
- `skill_path: str`
- `require_skill_md: bool`

**返回值:** `bool`

---
### `cmd_type(args) -> None`

类型检测命令

**参数:**
- `args`

**返回值:** `None`

---
### `cmd_audit(args) -> None`

健康检查命令

**参数:**
- `args`

**返回值:** `None`

---
### `cmd_optimize(args) -> None`

自动优化命令

**参数:**
- `args`

**返回值:** `None`

---
### `cmd_docs(args) -> None`

文档生成命令

**参数:**
- `args`

**返回值:** `None`

---
### `cmd_tests(args) -> None`

测试生成命令（纯文档型自动跳过）

**参数:**
- `args`

**返回值:** `None`

---
### `cmd_all(args) -> None`

一键全流程命令（按 Skill 类型自适应）

**参数:**
- `args`

**返回值:** `None`

---
### `cmd_batch(args) -> None`

批量优化命令：一次优化目录下所有 Skill

**参数:**
- `args`

**返回值:** `None`

---
### `cmd_diff(args) -> None`

优化前后对比报告命令

**参数:**
- `args`

**返回值:** `None`

---
### `cmd_info(args) -> None`

显示信息命令

**参数:**
- `args`

**返回值:** `None`

---
### `main() -> None`

*暂无文档说明*

**参数:**
- 无

**返回值:** `None`

---

## skill_type_detector.py

### `detect_skill_type(skill_path: str) -> Dict`

便捷函数：检测 Skill 类型

**参数:**
- `skill_path: str`

**返回值:** `Dict`

---
### `__init__(self, skill_path: str) -> None`

*暂无文档说明*

**参数:**
- `self`
- `skill_path: str`

**返回值:** `None`

---
### `detect(self) -> Dict`

执行 Skill 类型检测

Returns:
    {
        "type": "code-driven" | "doc-only" | "hybrid",
        "confidence": float,  # 0.0 - 1.0
        "indicators": {
            "has_scripts_dir": bool,
            "python_files": int,
            "has_tests_dir": bool,
            "test_files": int,
            "has_pyproject": bool,
            "has_requirements": bool,
            "has_makefile": bool,
            "has_ci_config": bool,
            "has_main_py": bool,
            "has_cli_entry": bool,
            "md_files": int,
            "has_references": bool,
            "has_assets": bool,
            "has_templates": bool,
        },
        "code_score": int,  # 0-100, 越高越像代码型
        "doc_score": int,   # 0-100, 越高越像文档型
        "description": str,
    }

**参数:**
- `self`

**返回值:** `Dict`

---
### `_collect_indicators(self) -> Dict`

收集检测指标

**参数:**
- `self`

**返回值:** `Dict`

---
### `_calculate_code_score(self, indicators: Dict) -> int`

计算代码型得分（0-100）

**参数:**
- `self`
- `indicators: Dict`

**返回值:** `int`

---
### `_calculate_doc_score(self, indicators: Dict) -> int`

计算文档型得分（0-100）

**参数:**
- `self`
- `indicators: Dict`

**返回值:** `int`

---
### `_determine_type(self, code_score: int, doc_score: int) -> Tuple[str, float]`

确定 Skill 类型

Returns:
    (type, confidence)

**参数:**
- `self`
- `code_score: int`
- `doc_score: int`

**返回值:** `Tuple[str, float]`

---
### `_generate_description(self, skill_type: str, indicators: Dict) -> str`

生成类型描述

**参数:**
- `self`
- `skill_type: str`
- `indicators: Dict`

**返回值:** `str`

---
### `is_doc_only(self) -> bool`

是否为纯文档型

**参数:**
- `self`

**返回值:** `bool`

---
### `is_code_driven(self) -> bool`

是否为代码驱动型

**参数:**
- `self`

**返回值:** `bool`

---
### `get_audit_weights(self) -> Dict[str, float]`

根据 Skill 类型获取 audit 权重

Returns:
    维度权重字典，权重之和为 1.0

**参数:**
- `self`

**返回值:** `Dict[str, float]`

---
### `get_optimize_scopes(self) -> List[str]`

根据 Skill 类型获取 optimize 适用范围

Returns:
    适用的优化范围列表 ["docs", "code", "config", "tests"]

**参数:**
- `self`

**返回值:** `List[str]`

---
