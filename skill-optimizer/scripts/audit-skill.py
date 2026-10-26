#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skill 健康检查脚本
基于 25 轮优化经验，检测 Skill 的 8 大维度健康状况
v1.8.0: 统一版本号，新增路径存在性验证和 SKILL.md 警告，完善错误处理
v1.8.0: 统一版本号，新增路径存在性验证和 SKILL.md 警告，完善错误处理
"""

import os
import re
import json
import py_compile
import argparse
import tempfile
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# 导入同目录下的类型检测器
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from skill_type_detector import SkillTypeDetector
except ImportError:
    SkillTypeDetector = None


class SkillAuditor:
    """Skill 健康检查器"""

    def __init__(self, skill_path: str):
        self.skill_path = Path(skill_path)
        # Skill 类型检测
        self.skill_type = "unknown"
        self.type_info = None
        if SkillTypeDetector is not None:
            try:
                detector = SkillTypeDetector(str(self.skill_path))
                self.type_info = detector.detect()
                self.skill_type = self.type_info["type"]
            except Exception:
                self.skill_type = "unknown"
        self.results = {
            "score": 0,
            "skill_type": self.skill_type,
            "type_info": self.type_info,
            "dimensions": {},
            "issues": [],
            "suggestions": [],
            "metadata": {
                "skill_path": str(self.skill_path),
                "audit_time": datetime.now().isoformat(),
                "version": "1.8.0",
                "skill_type": self.skill_type,
            }
        }

    def audit(self) -> Dict:
        """执行完整审计"""
        print(f"🔍 开始审计 Skill: {self.skill_path}")
        # 显示检测到的 Skill 类型
        type_names = {"code-driven": "代码驱动型", "doc-only": "纯文档型", "hybrid": "混合型", "unknown": "未知类型"}
        print(f"📋 检测到 Skill 类型: {type_names.get(self.skill_type, self.skill_type)}")
        if self.type_info:
            print(f"   {self.type_info.get('description', '')}")
        print("=" * 60)

        # 通用维度（所有类型都检查）
        self._check_metadata()        # 元数据完整性
        self._check_documentation()   # 文档完整性（含Markdown格式检查）
        self._check_templates()       # 模板资源
        self._check_usability()       # 易用性

        # 按类型决定检查哪些维度
        if self.skill_type in ("code-driven", "hybrid", "unknown"):
            self._check_code_quality()    # 代码质量
            self._check_testing()         # 测试覆盖
            self._check_engineering()     # 工程化配置
            self._check_maintainability() # 可维护性

        # 纯文档型和混合型：新增文档型专属维度
        if self.skill_type in ("doc-only", "hybrid"):
            self._check_doc_structure()      # SKILL.md 结构完整性
            self._check_trigger_scenarios()  # 触发场景覆盖度
            self._check_output_spec()        # 输出规范明确性
            self._check_references_depth()   # references 深度

        # 计算总分（使用动态权重）
        self._calculate_score()

        # 生成建议（按类型）
        self._generate_suggestions()

        return self.results

    def _check_metadata(self):
        """检查元数据完整性"""
        print("\n📋 检查元数据完整性...")
        score = 100
        issues = []

        # 检查 SKILL.md
        skill_md = self.skill_path / "SKILL.md"
        if not skill_md.exists():
            score -= 50
            issues.append({"severity": "critical", "message": "缺少 SKILL.md 核心文档"})
        else:
            content = skill_md.read_text(encoding="utf-8", errors="ignore")
            # 检查 frontmatter
            if not content.startswith("---"):
                score -= 20
                issues.append({"severity": "high", "message": "SKILL.md 缺少 frontmatter"})
            else:
                # 检查 name
                if not re.search(r'name:\s*\S+', content):
                    score -= 10
                    issues.append({"severity": "medium", "message": "frontmatter 缺少 name 字段"})
                # 检查 description
                if not re.search(r'description:\s*.+', content):
                    score -= 15
                    issues.append({"severity": "high", "message": "frontmatter 缺少 description 字段"})

        # 检查版本号
        has_version = False
        for f in ["SKILL.md", "README.md", "pyproject.toml", "package.json"]:
            fp = self.skill_path / f
            if fp.exists():
                content = fp.read_text(encoding="utf-8", errors="ignore")
                if re.search(r'v?\d+\.\d+\.\d+', content):
                    has_version = True
                    break
        if not has_version:
            score -= 10
            issues.append({"severity": "low", "message": "未找到版本号"})

        # 检查许可证
        has_license = (self.skill_path / "LICENSE").exists()
        if not has_license:
            score -= 5
            issues.append({"severity": "low", "message": "缺少 LICENSE 文件"})

        self.results["dimensions"]["metadata"] = {"score": max(0, score), "issues": issues}
        self.results["issues"].extend(issues)
        print(f"  得分: {max(0, score)}/100, 问题: {len(issues)} 个")

    def _check_documentation(self):
        """检查文档完整性（含Markdown格式检查）"""
        print("\n📚 检查文档完整性...")
        score = 100
        issues = []

        required_docs = {
            "README.md": 20,
            "QUICKSTART.md": 10,
            "CHANGELOG.md": 15,
            "FAQ.md": 10,
            "CONTRIBUTING.md": 8,
            "SECURITY.md": 5,
            "CODE_OF_CONDUCT.md": 5,
            "API.md": 8,
            "ARCHITECTURE.md": 5,
            "TESTING.md": 5,
            "DEBUGGING.md": 5,
            "INSTALLATION.md": 4,
        }

        for doc, weight in required_docs.items():
            if not (self.skill_path / doc).exists():
                score -= weight
                issues.append({"severity": "medium", "message": f"缺少文档: {doc}"})

        # 检查文档内容质量
        readme = self.skill_path / "README.md"
        if readme.exists():
            content = readme.read_text(encoding="utf-8", errors="ignore")
            if len(content) < 500:
                score -= 10
                issues.append({"severity": "low", "message": "README.md 内容过短（<500字）"})

        # === 新增：Markdown 文档格式检查 ===
        md_format_issues = self._check_markdown_format()
        if md_format_issues:
            # 格式问题按严重程度扣分，最多扣20分
            format_penalty = min(20, len(md_format_issues) * 2)
            score -= format_penalty
            issues.extend(md_format_issues)
            print(f"  📝 Markdown格式检查: 发现 {len(md_format_issues)} 个问题，扣 {format_penalty} 分")

        self.results["dimensions"]["documentation"] = {"score": max(0, score), "issues": issues}
        self.results["issues"].extend(issues)
        print(f"  得分: {max(0, score)}/100, 问题: {len(issues)} 个")

    def _check_markdown_format(self) -> List[Dict]:
        """检查 Markdown 文档格式（表格列数一致性、双链格式有效性）"""
        issues = []
        md_files = list(self.skill_path.rglob("*.md"))
        skip_dirs = {".venv", "venv", "__pycache__", "node_modules", ".git"}

        for md_file in md_files:
            if any(part in skip_dirs for part in md_file.parts):
                continue
            try:
                content = md_file.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue

            lines = content.split('\n')
            rel_path = str(md_file.relative_to(self.skill_path))

            # 1. 表格列数一致性检查
            in_table = False
            expected_cols = 0
            for i, line in enumerate(lines, 1):
                stripped = line.strip()
                # 检测表头行（包含 | 且不是分隔符行）
                if not in_table and stripped.startswith('|') and stripped.endswith('|'):
                    # 排除分隔符行
                    if not re.match(r'^\|[\s\-:|]+\|$', stripped):
                        in_table = True
                        # 计算列数（排除转义的 \| 和双链内的 |）
                        cleaned = self._clean_table_pipes(stripped)
                        expected_cols = cleaned.count('|') - 1
                        continue
                # 分隔符行
                if in_table and re.match(r'^\|[\s\-:|]+\|$', stripped):
                    continue
                # 数据行
                if in_table and stripped.startswith('|') and stripped.endswith('|'):
                    cleaned = self._clean_table_pipes(stripped)
                    actual_cols = cleaned.count('|') - 1
                    if actual_cols != expected_cols and expected_cols > 0:
                        issues.append({
                            "severity": "medium",
                            "message": f"表格列数不匹配: {rel_path} 行{i} (实际{actual_cols}列≠表头{expected_cols}列)"
                        })
                    continue
                # 空行结束表格
                if in_table and not stripped:
                    in_table = False

            # 2. 双链格式有效性检查
            # 检查 [[|文字]] 错误格式（目标为空）
            empty_target_links = re.findall(r'\[\[\s*\|[^\]]+\]\]', content)
            if empty_target_links:
                issues.append({
                    "severity": "high",
                    "message": f"双链目标为空: {rel_path} 发现 {len(empty_target_links)} 个 [[|文字]] 格式错误"
                })

            # 检查表格中双链内未转义的 |（可能导致列数错位）
            # 只在表格行中检查
            in_table = False
            for i, line in enumerate(lines, 1):
                stripped = line.strip()
                if not in_table and stripped.startswith('|') and stripped.endswith('|'):
                    if not re.match(r'^\|[\s\-:|]+\|$', stripped):
                        in_table = True
                        continue
                if in_table and re.match(r'^\|[\s\-:|]+\|$', stripped):
                    continue
                if in_table and stripped.startswith('|') and stripped.endswith('|'):
                    # 检查双链中是否有未转义的 |
                    wiki_links = re.findall(r'\[\[([^\]]+)\]\]', stripped)
                    for link in wiki_links:
                        if '|' in link and '\\|' not in link:
                            issues.append({
                                "severity": "medium",
                                "message": f"表格双链管道符未转义: {rel_path} 行{i} [[{link[:40]}...]] 中的 | 应转义为 \\|"
                            })
                    continue
                if in_table and not stripped:
                    in_table = False

        return issues

    @staticmethod
    def _clean_table_pipes(line: str) -> str:
        """清理表格行中的管道符，排除转义的 \\| 和双链内的 |"""
        # 先移除转义的 \|
        cleaned = line.replace('\\|', '')
        # 再移除双链 [[...]] 内的内容（包括其中的 |）
        cleaned = re.sub(r'\[\[[^\]]*\]\]', '[[]]', cleaned)
        return cleaned

    def _check_code_quality(self):
        """检查代码质量（含py_compile验证、修复类型注解检测）"""
        print("\n💻 检查代码质量...")
        score = 100
        issues = []

        py_files = list(self.skill_path.rglob("*.py"))
        if not py_files:
            score -= 50
            issues.append({"severity": "high", "message": "未找到 Python 脚本文件"})
        else:
            total_funcs = 0
            typed_funcs = 0
            funcs_with_docstring = 0
            has_try_except = False
            syntax_errors = []

            for py_file in py_files:
                if any(part in [".venv", "venv", "__pycache__", "node_modules"] for part in py_file.parts):
                    continue
                try:
                    content = py_file.read_text(encoding="utf-8", errors="ignore")

                    # === 新增：py_compile 语法验证 ===
                    try:
                        with tempfile.NamedTemporaryFile(suffix='.pyc', delete=False) as tmp:
                            tmp_path = tmp.name
                        py_compile.compile(str(py_file), cfile=tmp_path, doraise=True)
                        os.unlink(tmp_path)
                    except py_compile.PyCompileError as e:
                        syntax_errors.append(f"{py_file.name}: {str(e)[:100]}")
                    except Exception as e:
                        syntax_errors.append(f"{py_file.name}: {str(e)[:100]}")

                    # === 修复：使用 re.finditer 精确获取函数位置 ===
                    # 匹配 def 函数定义，捕获函数名和完整签名行
                    func_pattern = re.compile(r'^(\s*)def\s+(\w+)\s*\(([^)]*)\)(\s*->\s*[^:]+)?\s*:', re.MULTILINE)
                    for match in func_pattern.finditer(content):
                        total_funcs += 1
                        func_name = match.group(2)
                        return_annotation = match.group(4)

                        # 检查返回类型注解（精确匹配签名行）
                        if return_annotation and '->' in return_annotation:
                            typed_funcs += 1

                        # 检查 docstring（从函数体开始位置检查）
                        func_start = match.end()
                        func_body = content[func_start:func_start + 500]
                        # 去除前导空白后检查是否以 docstring 开头
                        body_stripped = func_body.lstrip()
                        if body_stripped.startswith('"""') or body_stripped.startswith("'''"):
                            funcs_with_docstring += 1

                    # 检查异常处理
                    if 'try:' in content and 'except' in content:
                        has_try_except = True
                except Exception:
                    pass

            # === 新增：语法错误扣分 ===
            if syntax_errors:
                score -= min(30, len(syntax_errors) * 10)
                for err in syntax_errors:
                    issues.append({"severity": "critical", "message": f"Python语法错误: {err}"})
                print(f"  ❌ py_compile验证: 发现 {len(syntax_errors)} 个语法错误")
            else:
                print(f"  ✅ py_compile验证: 所有脚本语法正确")

            if total_funcs > 0:
                type_coverage = typed_funcs / total_funcs * 100
                if type_coverage < 100:
                    score -= int((100 - type_coverage) * 0.3)
                    issues.append({"severity": "medium", "message": f"类型注解覆盖率: {type_coverage:.1f}% (目标 100%)"})

                docstring_coverage = funcs_with_docstring / total_funcs * 100
                if docstring_coverage < 80:
                    score -= int((80 - docstring_coverage) * 0.2)
                    issues.append({"severity": "low", "message": f"docstring 覆盖率: {docstring_coverage:.1f}% (目标 80%)"})

            if not has_try_except:
                score -= 10
                issues.append({"severity": "medium", "message": "未发现异常处理（try/except）"})

        self.results["dimensions"]["code_quality"] = {"score": max(0, score), "issues": issues}
        self.results["issues"].extend(issues)
        print(f"  得分: {max(0, score)}/100, 问题: {len(issues)} 个")

    def _check_testing(self):
        """检查测试覆盖"""
        print("\n🧪 检查测试覆盖...")
        score = 100
        issues = []

        test_dirs = ["tests", "test", "__tests__"]
        has_test_dir = any((self.skill_path / d).exists() for d in test_dirs)
        if not has_test_dir:
            score -= 60
            issues.append({"severity": "high", "message": "缺少测试目录"})
        else:
            test_files = list(self.skill_path.rglob("test_*.py")) + list(self.skill_path.rglob("*_test.py"))
            if not test_files:
                score -= 40
                issues.append({"severity": "high", "message": "未找到测试文件"})
            else:
                # 检查测试内容
                has_assert = False
                for tf in test_files[:5]:
                    content = tf.read_text(encoding="utf-8", errors="ignore")
                    if "assert" in content:
                        has_assert = True
                        break
                if not has_assert:
                    score -= 20
                    issues.append({"severity": "medium", "message": "测试文件中未找到 assert 断言"})

        # 检查覆盖率配置
        if not (self.skill_path / ".coveragerc").exists():
            score -= 10
            issues.append({"severity": "low", "message": "缺少 .coveragerc 覆盖率配置"})

        self.results["dimensions"]["testing"] = {"score": max(0, score), "issues": issues}
        self.results["issues"].extend(issues)
        print(f"  得分: {max(0, score)}/100, 问题: {len(issues)} 个")

    def _check_engineering(self):
        """检查工程化配置"""
        print("\n🔧 检查工程化配置...")
        score = 100
        issues = []

        configs = {
            ".gitignore": 15,
            ".editorconfig": 10,
            ".pre-commit-config.yaml": 15,
            "pyproject.toml": 10,
            "Makefile": 8,
            "requirements.txt": 8,
        }

        for config, weight in configs.items():
            if not (self.skill_path / config).exists():
                score -= weight
                issues.append({"severity": "low", "message": f"缺少配置文件: {config}"})

        # 检查 CI/CD
        github_dir = self.skill_path / ".github" / "workflows"
        if not github_dir.exists():
            score -= 15
            issues.append({"severity": "medium", "message": "缺少 GitHub Actions CI/CD 配置"})
        else:
            workflows = list(github_dir.glob("*.yml")) + list(github_dir.glob("*.yaml"))
            if not workflows:
                score -= 10
                issues.append({"severity": "low", "message": ".github/workflows 目录为空"})

        self.results["dimensions"]["engineering"] = {"score": max(0, score), "issues": issues}
        self.results["issues"].extend(issues)
        print(f"  得分: {max(0, score)}/100, 问题: {len(issues)} 个")

    def _check_templates(self):
        """检查模板资源"""
        print("\n📋 检查模板资源...")
        score = 100
        issues = []

        template_dirs = ["templates", "assets", "examples", "references"]
        has_template_dir = any((self.skill_path / d).exists() for d in template_dirs)
        if not has_template_dir:
            score -= 50
            issues.append({"severity": "medium", "message": "缺少模板/示例/参考文档目录"})

        # 检查示例
        examples_dir = self.skill_path / "examples"
        if not examples_dir.exists():
            score -= 20
            issues.append({"severity": "low", "message": "缺少 examples 示例目录"})

        self.results["dimensions"]["templates"] = {"score": max(0, score), "issues": issues}
        self.results["issues"].extend(issues)
        print(f"  得分: {max(0, score)}/100, 问题: {len(issues)} 个")

    def _check_usability(self):
        """检查易用性"""
        print("\n✨ 检查易用性...")
        score = 100
        issues = []

        # 检查帮助信息
        py_files = list(self.skill_path.rglob("*.py"))
        has_help = False
        has_argparse = False
        for py_file in py_files:
            if any(part in [".venv", "venv", "__pycache__"] for part in py_file.parts):
                continue
            content = py_file.read_text(encoding="utf-8", errors="ignore")
            if "--help" in content or "add_argument" in content:
                has_help = True
            if "argparse" in content:
                has_argparse = True
            break

        if not has_argparse:
            score -= 20
            issues.append({"severity": "medium", "message": "未使用 argparse 处理命令行参数"})

        # 检查 QUICKSTART
        if not (self.skill_path / "QUICKSTART.md").exists():
            score -= 30
            issues.append({"severity": "high", "message": "缺少 QUICKSTART.md 快速上手指南"})

        self.results["dimensions"]["usability"] = {"score": max(0, score), "issues": issues}
        self.results["issues"].extend(issues)
        print(f"  得分: {max(0, score)}/100, 问题: {len(issues)} 个")

    def _check_maintainability(self):
        """检查可维护性"""
        print("\n🔄 检查可维护性...")
        score = 100
        issues = []

        # 检查代码结构
        py_files = [f for f in self.skill_path.rglob("*.py")
                    if not any(part in [".venv", "venv", "__pycache__"] for part in f.parts)]

        if py_files:
            # 检查是否有主入口
            has_main = any("if __name__" in f.read_text(encoding="utf-8", errors="ignore") for f in py_files)
            if not has_main:
                score -= 15
                issues.append({"severity": "low", "message": "未找到主入口函数（if __name__ == '__main__'）"})

            # 检查单文件过大
            for py_file in py_files:
                lines = len(py_file.read_text(encoding="utf-8", errors="ignore").splitlines())
                if lines > 500:
                    score -= 10
                    issues.append({"severity": "low", "message": f"文件过大: {py_file.name} ({lines}行)，建议拆分"})
                    break

        self.results["dimensions"]["maintainability"] = {"score": max(0, score), "issues": issues}
        self.results["issues"].extend(issues)
        print(f"  得分: {max(0, score)}/100, 问题: {len(issues)} 个")

    def _check_doc_structure(self):
        """检查 SKILL.md 结构完整性（纯文档型专属）"""
        print("\n📐 检查 SKILL.md 结构完整性...")
        score = 100
        issues = []

        skill_md = self.skill_path / "SKILL.md"
        if not skill_md.exists():
            score = 0
            issues.append({"severity": "critical", "message": "缺少 SKILL.md"})
        else:
            content = skill_md.read_text(encoding="utf-8", errors="ignore")

            # 检查核心结构模块
            structure_checks = {
                "核心原则/设计理念": r"(核心原则|设计理念|设计原则)",
                "使用流程/工作流程": r"(使用流程|工作流程|使用场景|使用方法)",
                "输出规范/质量标准": r"(输出规范|质量标准|质量检查|检查清单)",
                "参考文档/references": r"(references|参考文档|参考资料)",
                "版本信息": r"(版本|version|v\d+\.\d+)",
            }

            for name, pattern in structure_checks.items():
                if not re.search(pattern, content):
                    score -= 15
                    issues.append({"severity": "medium", "message": f"SKILL.md 缺少模块: {name}"})

            # 检查标题层级
            h1_count = len(re.findall(r'(?m)^#\s+\S', content))
            h2_count = len(re.findall(r'(?m)^##\s+\S', content))
            if h1_count == 0:
                score -= 10
                issues.append({"severity": "medium", "message": "SKILL.md 缺少一级标题"})
            if h2_count < 3:
                score -= 10
                issues.append({"severity": "low", "message": f"SKILL.md 二级标题过少（{h2_count}个），建议至少3个"})

            # 检查 frontmatter
            if not content.startswith("---"):
                score -= 15
                issues.append({"severity": "high", "message": "SKILL.md 缺少 frontmatter"})

        self.results["dimensions"]["doc_structure"] = {"score": max(0, score), "issues": issues}
        self.results["issues"].extend(issues)
        print(f"  得分: {max(0, score)}/100, 问题: {len(issues)} 个")

    def _check_trigger_scenarios(self):
        """检查触发场景覆盖度（纯文档型专属）"""
        print("\n🎯 检查触发场景覆盖度...")
        score = 100
        issues = []

        skill_md = self.skill_path / "SKILL.md"
        if not skill_md.exists():
            score = 0
            issues.append({"severity": "critical", "message": "缺少 SKILL.md"})
        else:
            content = skill_md.read_text(encoding="utf-8", errors="ignore")

            # 从 description 提取触发场景
            desc_match = re.search(r'description:\s*(.+?)(?:\n---|\n$)', content, re.DOTALL)
            if desc_match:
                desc = desc_match.group(1)
                # 检查触发关键词
                trigger_keywords = ["当用户", "需要", "支持", "场景", "使用时"]
                found = sum(1 for kw in trigger_keywords if kw in desc)
                if found < 2:
                    score -= 20
                    issues.append({"severity": "medium", "message": "description 中触发场景描述不足，建议包含'当用户...时使用'和'支持...场景'"})
            else:
                score -= 25
                issues.append({"severity": "high", "message": "frontmatter 缺少 description 字段"})

            # 检查使用场景数量
            scene_sections = re.findall(r'(?m)^###\s+场景[一二三四五六七八九十\d]', content)
            if len(scene_sections) == 0:
                # 尝试其他格式
                scene_sections = re.findall(r'(?m)^###\s+(使用场景|场景)', content)
            if len(scene_sections) < 2:
                score -= 20
                issues.append({"severity": "medium", "message": f"使用场景过少（{len(scene_sections)}个），建议至少2个具体使用场景"})

            # 检查示例
            if not re.search(r'(示例|example|输入.*输出)', content, re.IGNORECASE):
                score -= 15
                issues.append({"severity": "low", "message": "缺少使用示例（输入/输出示例）"})

        self.results["dimensions"]["trigger_scenarios"] = {"score": max(0, score), "issues": issues}
        self.results["issues"].extend(issues)
        print(f"  得分: {max(0, score)}/100, 问题: {len(issues)} 个")

    def _check_output_spec(self):
        """检查输出规范明确性（纯文档型专属）"""
        print("\n📝 检查输出规范明确性...")
        score = 100
        issues = []

        skill_md = self.skill_path / "SKILL.md"
        if not skill_md.exists():
            score = 0
            issues.append({"severity": "critical", "message": "缺少 SKILL.md"})
        else:
            content = skill_md.read_text(encoding="utf-8", errors="ignore")

            # 检查输出规范模块
            if not re.search(r'(输出规范|输出要求|输出格式|质量标准|质量检查|检查清单|验收标准)', content):
                score -= 30
                issues.append({"severity": "high", "message": "缺少输出规范/质量标准模块，建议明确输出格式、质量要求和检查清单"})

            # 检查是否有具体的输出要求条目
            output_items = re.findall(r'(?m)^\d+\.\s+\*\*[^*]+\*\*', content)
            if len(output_items) < 3:
                score -= 15
                issues.append({"severity": "medium", "message": f"输出规范条目过少（{len(output_items)}条），建议至少3条具体的输出要求"})

            # 检查是否有质量检查清单
            if not re.search(r'(?m)^- \[ \]', content) and not re.search(r'(检查清单|checklist)', content, re.IGNORECASE):
                score -= 15
                issues.append({"severity": "low", "message": "缺少质量检查清单（checkbox 格式）"})

        self.results["dimensions"]["output_spec"] = {"score": max(0, score), "issues": issues}
        self.results["issues"].extend(issues)
        print(f"  得分: {max(0, score)}/100, 问题: {len(issues)} 个")

    def _check_references_depth(self):
        """检查 references 深度（纯文档型专属）"""
        print("\n📚 检查 references 深度...")
        score = 100
        issues = []

        refs_dir = self.skill_path / "references"
        if not refs_dir.exists():
            score -= 40
            issues.append({"severity": "high", "message": "缺少 references/ 目录，建议添加详细的参考文档"})
        else:
            ref_files = list(refs_dir.glob("*.md"))
            if len(ref_files) == 0:
                score -= 30
                issues.append({"severity": "high", "message": "references/ 目录为空，建议添加参考文档"})
            else:
                # 检查每个参考文档的深度
                total_lines = 0
                shallow_files = []
                for rf in ref_files:
                    try:
                        lines = len(rf.read_text(encoding="utf-8", errors="ignore").splitlines())
                        total_lines += lines
                        if lines < 50:
                            shallow_files.append(f"{rf.name}({lines}行)")
                    except Exception:
                        pass

                avg_lines = total_lines // len(ref_files) if ref_files else 0
                if avg_lines < 80:
                    score -= 20
                    issues.append({"severity": "medium", "message": f"参考文档平均深度不足（{avg_lines}行/篇），建议每篇至少80行"})
                if shallow_files:
                    score -= 10
                    issues.append({"severity": "low", "message": f"以下参考文档过浅: {', '.join(shallow_files[:3])}"})

                # 检查 SKILL.md 是否引用了 references
                skill_md = self.skill_path / "SKILL.md"
                if skill_md.exists():
                    content = skill_md.read_text(encoding="utf-8", errors="ignore")
                    if "references/" not in content and "参考文档" not in content:
                        score -= 15
                        issues.append({"severity": "medium", "message": "SKILL.md 未引用 references/ 目录中的文档，建议在相关章节添加引用链接"})

        self.results["dimensions"]["references_depth"] = {"score": max(0, score), "issues": issues}
        self.results["issues"].extend(issues)
        print(f"  得分: {max(0, score)}/100, 问题: {len(issues)} 个")

    def _calculate_score(self):
        """计算总分（按 Skill 类型使用动态权重）"""
        # 使用 SkillTypeDetector 获取动态权重
        if SkillTypeDetector is not None and self.skill_type != "unknown":
            try:
                detector = SkillTypeDetector(str(self.skill_path))
                weights = detector.get_audit_weights()
            except Exception:
                weights = self._get_default_weights()
        else:
            weights = self._get_default_weights()

        total = 0
        for dim, weight in weights.items():
            dim_score = self.results["dimensions"].get(dim, {}).get("score", 0)
            total += dim_score * weight

        self.results["score"] = round(total, 1)
        self.results["weights_used"] = weights

        # 计算等级（保存到 results，供 JSON 报告使用）
        score = self.results["score"]
        if score >= 95:
            self.results["grade"] = "S"
            self.results["grade_label"] = "专业级"
        elif score >= 85:
            self.results["grade"] = "A"
            self.results["grade_label"] = "优秀"
        elif score >= 70:
            self.results["grade"] = "B"
            self.results["grade_label"] = "良好"
        elif score >= 50:
            self.results["grade"] = "C"
            self.results["grade_label"] = "一般"
        else:
            self.results["grade"] = "D"
            self.results["grade_label"] = "较差"

    def _get_default_weights(self) -> Dict[str, float]:
        """获取默认权重（代码驱动型）"""
        return {
            "metadata": 0.15,
            "documentation": 0.20,
            "code_quality": 0.20,
            "testing": 0.15,
            "engineering": 0.10,
            "templates": 0.10,
            "usability": 0.05,
            "maintainability": 0.05,
        }

    def _generate_suggestions(self):
        """生成优化建议（按 Skill 类型）"""
        suggestions = []

        # 按类型使用不同的建议指南
        if self.skill_type == "doc-only":
            dim_guides = {
                "metadata": "完善 frontmatter（name/description），description 中明确触发场景",
                "documentation": "运行 optimize-skill.py --auto --only docs，补全 README/CHANGELOG 等文档",
                "doc_structure": "完善 SKILL.md 结构，添加核心原则、使用流程、输出规范、版本信息等模块",
                "trigger_scenarios": "增加具体使用场景（至少2个），每个场景包含输入/输出示例",
                "output_spec": "添加输出规范模块，明确输出格式、质量要求和检查清单（checkbox格式）",
                "references_depth": "深化 references/ 文档，每篇至少80行，在 SKILL.md 中添加引用链接",
                "templates": "创建 assets/ 或 templates/ 目录，添加模板文件",
                "usability": "编写 QUICKSTART.md，提供快速上手指南",
            }
        elif self.skill_type == "hybrid":
            dim_guides = {
                "metadata": "完善 frontmatter 和版本号",
                "documentation": "运行 optimize-skill.py --auto --only docs，补全缺失文档",
                "code_quality": "添加类型注解和异常处理，确保 py_compile 语法验证通过",
                "testing": "运行 generate-tests.py --type all，生成单元测试和集成测试",
                "engineering": "运行 optimize-skill.py --auto --only config，配置 CI/CD 和 pre-commit",
                "doc_structure": "完善 SKILL.md 结构，添加核心原则、使用流程、输出规范",
                "trigger_scenarios": "增加具体使用场景和输入/输出示例",
                "output_spec": "添加输出规范和质量检查清单",
                "templates": "创建 templates/ 和 examples/ 目录",
                "usability": "完善命令行帮助信息，编写 QUICKSTART.md",
                "maintainability": "重构过大的文件，添加架构文档",
            }
        else:
            # 代码驱动型（默认）
            dim_guides = {
                "metadata": "参考 OPTIMIZATION-GUIDE.md 第1轮，完善 frontmatter 和版本号",
                "documentation": "运行 optimize-skill.py --auto --only docs，自动补全缺失文档；修复Markdown表格列数和双链格式",
                "code_quality": "参考 OPTIMIZATION-GUIDE.md 第6轮，添加类型注解和异常处理；确保py_compile语法验证通过",
                "testing": "运行 generate-tests.py --type all，生成单元测试和集成测试",
                "engineering": "运行 optimize-skill.py --auto --only config，配置 CI/CD 和 pre-commit",
                "templates": "创建 templates/ 和 examples/ 目录，添加模板和示例",
                "usability": "完善命令行帮助信息，编写 QUICKSTART.md",
                "maintainability": "重构过大的文件，添加架构文档",
            }

        for dim, guide in dim_guides.items():
            dim_score = self.results["dimensions"].get(dim, {}).get("score", 100)
            if dim_score < 80:
                suggestions.append({
                    "dimension": dim,
                    "current_score": dim_score,
                    "suggestion": guide,
                    "priority": "high" if dim_score < 50 else "medium"
                })

        self.results["suggestions"] = suggestions

    def print_report(self):
        """打印审计报告"""
        print("\n" + "=" * 60)
        print("📊 审计报告")
        print("=" * 60)

        # 显示 Skill 类型
        type_names = {"code-driven": "代码驱动型", "doc-only": "纯文档型", "hybrid": "混合型", "unknown": "未知类型"}
        print(f"\n📋 Skill 类型: {type_names.get(self.skill_type, self.skill_type)}")
        if self.type_info:
            print(f"   置信度: {self.type_info.get('confidence', 0):.0%}")
            # 根据类型显示相关得分，避免纯文档型显示代码型0分造成误导
            if self.skill_type == "code-driven":
                print(f"   代码型得分: {self.type_info.get('code_score', 0)}/100")
            elif self.skill_type == "doc-only":
                print(f"   文档型得分: {self.type_info.get('doc_score', 0)}/100")
            else:  # hybrid 或 unknown
                print(f"   代码型得分: {self.type_info.get('code_score', 0)}/100 | 文档型得分: {self.type_info.get('doc_score', 0)}/100")
            if self.results.get("weights_used"):
                print(f"   评估模式: {self.skill_type} 模式（{len(self.results['weights_used'])}个维度）")

        score = self.results["score"]
        if score >= 95:
            grade = "🏆 S 级（专业级）"
        elif score >= 85:
            grade = "✅ A 级（优秀）"
        elif score >= 70:
            grade = "⚠️ B 级（良好）"
        elif score >= 50:
            grade = "❌ C 级（一般）"
        else:
            grade = "🔴 D 级（较差）"

        print(f"\n总分: {score}/100  {grade}")
        print(f"\n各维度得分:")
        for dim, data in self.results["dimensions"].items():
            bar = "█" * int(data["score"] / 5) + "░" * (20 - int(data["score"] / 5))
            print(f"  {dim:20s} {bar} {data['score']:3d}/100")

        # 问题统计
        critical = sum(1 for i in self.results["issues"] if i["severity"] == "critical")
        high = sum(1 for i in self.results["issues"] if i["severity"] == "high")
        medium = sum(1 for i in self.results["issues"] if i["severity"] == "medium")
        low = sum(1 for i in self.results["issues"] if i["severity"] == "low")

        print(f"\n问题统计: 🔴严重={critical} 🟠高={high} 🟡中={medium} 🟢低={low}")

        if self.results["issues"]:
            print(f"\n问题清单（前10个）:")
            for i, issue in enumerate(self.results["issues"][:10], 1):
                icon = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}.get(issue["severity"], "⚪")
                print(f"  {i}. {icon} {issue['message']}")

        if self.results["suggestions"]:
            print(f"\n💡 优化建议:")
            for i, sug in enumerate(self.results["suggestions"], 1):
                print(f"  {i}. [{sug['dimension']}] {sug['suggestion']}")

        print(f"\n{'=' * 60}")
        print(f"审计完成时间: {self.results['metadata']['audit_time']}")
        print(f"审计工具版本: v{self.results['metadata']['version']}")

    def save_report(self, output_path: str):
        """保存报告到文件"""
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        print(f"\n📄 报告已保存到: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Skill 健康检查工具 v1.8.0（支持多类型 Skill 自适应评估）")
    parser.add_argument("--path", required=True, help="Skill 目录路径")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="输出格式")
    parser.add_argument("--output", help="输出文件路径（JSON 格式时使用）")
    args = parser.parse_args()

    if not os.path.exists(args.path):
        print(f"❌ 错误: 路径不存在 - {args.path}")
        return

    auditor = SkillAuditor(args.path)
    results = auditor.audit()

    if args.format == "json":
        output = args.output or "audit-report.json"
        auditor.save_report(output)
    else:
        auditor.print_report()


if __name__ == "__main__":
    main()
