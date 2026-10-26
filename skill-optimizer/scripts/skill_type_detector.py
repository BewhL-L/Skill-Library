#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skill 类型自动检测模块
自动检测 Skill 是代码驱动型（code-driven）还是纯文档型（doc-only），
为 audit 和 optimize 提供类型信息，实现按类型适配的优化策略。

v1.8.0: 统一版本号，完善边界情况处理
"""

import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional


class SkillTypeDetector:
    """Skill 类型检测器"""

    def __init__(self, skill_path: str):
        self.skill_path = Path(skill_path)
        self._detection_result = None

    def detect(self) -> Dict:
        """
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
        """
        if self._detection_result is not None:
            return self._detection_result

        indicators = self._collect_indicators()
        code_score = self._calculate_code_score(indicators)
        doc_score = self._calculate_doc_score(indicators)
        skill_type, confidence = self._determine_type(code_score, doc_score)
        description = self._generate_description(skill_type, indicators)

        self._detection_result = {
            "type": skill_type,
            "confidence": round(confidence, 2),
            "indicators": indicators,
            "code_score": code_score,
            "doc_score": doc_score,
            "description": description,
        }
        return self._detection_result

    def _collect_indicators(self) -> Dict:
        """收集检测指标"""
        indicators = {
            "has_scripts_dir": False,
            "python_files": 0,
            "has_tests_dir": False,
            "test_files": 0,
            "has_pyproject": False,
            "has_requirements": False,
            "has_makefile": False,
            "has_ci_config": False,
            "has_main_py": False,
            "has_cli_entry": False,
            "md_files": 0,
            "has_references": False,
            "has_assets": False,
            "has_templates": False,
            "total_files": 0,
        }

        if not self.skill_path.exists():
            return indicators

        # 扫描所有文件
        all_files = list(self.skill_path.rglob("*"))
        indicators["total_files"] = len([f for f in all_files if f.is_file()])

        for f in all_files:
            if not f.is_file():
                continue
            rel = f.relative_to(self.skill_path)
            name = f.name
            parts = rel.parts

            # Python 文件
            if name.endswith(".py"):
                indicators["python_files"] += 1
                if name == "main.py":
                    indicators["has_main_py"] = True
                # 检测 CLI 入口（包含 argparse 或 click 或 if __name__ == "__main__"）
                try:
                    content = f.read_text(encoding="utf-8", errors="ignore")
                    if "argparse" in content or "click" in content or '__name__ == "__main__"' in content:
                        indicators["has_cli_entry"] = True
                except Exception:
                    pass

            # 测试文件
            if name.startswith("test_") or name.endswith("_test.py"):
                indicators["test_files"] += 1

            # Markdown 文件
            if name.endswith(".md"):
                indicators["md_files"] += 1

            # 目录检测
            if len(parts) > 0:
                top_dir = parts[0]
                if top_dir == "scripts":
                    indicators["has_scripts_dir"] = True
                if top_dir == "tests" or top_dir == "test":
                    indicators["has_tests_dir"] = True
                if top_dir == "references":
                    indicators["has_references"] = True
                if top_dir == "assets":
                    indicators["has_assets"] = True
                if top_dir == "templates":
                    indicators["has_templates"] = True

            # 配置文件
            if name == "pyproject.toml" or name == "setup.py" or name == "setup.cfg":
                indicators["has_pyproject"] = True
            if name == "requirements.txt" or name == "Pipfile":
                indicators["has_requirements"] = True
            if name == "Makefile":
                indicators["has_makefile"] = True
            # CI 配置
            if ".github" in parts and "workflows" in parts and name.endswith((".yml", ".yaml")):
                indicators["has_ci_config"] = True
            if name == ".gitlab-ci.yml" or name == "circle.yml":
                indicators["has_ci_config"] = True

        return indicators

    def _calculate_code_score(self, indicators: Dict) -> int:
        """计算代码型得分（0-100）"""
        score = 0

        # 强指标（每项 +20）
        if indicators["has_scripts_dir"]:
            score += 20
        if indicators["python_files"] >= 3:
            score += 20
        elif indicators["python_files"] >= 1:
            score += 10
        if indicators["has_main_py"] or indicators["has_cli_entry"]:
            score += 15
        if indicators["has_tests_dir"] or indicators["test_files"] > 0:
            score += 15

        # 中指标（每项 +10）
        if indicators["has_pyproject"]:
            score += 10
        if indicators["has_requirements"]:
            score += 5
        if indicators["has_makefile"]:
            score += 5
        if indicators["has_ci_config"]:
            score += 10

        return min(100, score)

    def _calculate_doc_score(self, indicators: Dict) -> int:
        """计算文档型得分（0-100）"""
        score = 0

        # 强指标
        if indicators["md_files"] >= 3:
            score += 25
        elif indicators["md_files"] >= 1:
            score += 10
        if indicators["has_references"]:
            score += 20
        if indicators["has_assets"]:
            score += 15
        if indicators["has_templates"]:
            score += 15

        # 没有代码特征加分
        if indicators["python_files"] == 0:
            score += 15
        if not indicators["has_scripts_dir"]:
            score += 10

        return min(100, score)

    def _determine_type(self, code_score: int, doc_score: int) -> Tuple[str, float]:
        """
        确定 Skill 类型

        Returns:
            (type, confidence)
        """
        diff = abs(code_score - doc_score)

        if code_score >= 60 and doc_score < 60:
            return "code-driven", min(0.95, 0.6 + code_score / 200)
        elif doc_score >= 60 and code_score < 40:
            return "doc-only", min(0.95, 0.6 + doc_score / 200)
        elif code_score >= 40 and doc_score >= 40:
            return "hybrid", min(0.85, 0.4 + diff / 100)
        elif code_score > doc_score:
            return "code-driven", 0.5 + (code_score - doc_score) / 200
        else:
            return "doc-only", 0.5 + (doc_score - code_score) / 200

    def _generate_description(self, skill_type: str, indicators: Dict) -> str:
        """生成类型描述"""
        type_names = {
            "code-driven": "代码驱动型",
            "doc-only": "纯文档型",
            "hybrid": "混合型",
        }
        desc = f"检测为【{type_names.get(skill_type, skill_type)}】"

        features = []
        if indicators["has_scripts_dir"]:
            features.append(f"scripts/目录({indicators['python_files']}个Python文件)")
        if indicators["has_tests_dir"] or indicators["test_files"] > 0:
            features.append(f"测试({indicators['test_files']}个测试文件)")
        if indicators["has_references"]:
            features.append("references/参考文档")
        if indicators["has_assets"]:
            features.append("assets/模板资源")
        if indicators["md_files"] > 0:
            features.append(f"{indicators['md_files']}个Markdown文档")

        if features:
            desc += f"，特征：{', '.join(features)}"

        return desc

    def is_doc_only(self) -> bool:
        """是否为纯文档型"""
        return self.detect()["type"] == "doc-only"

    def is_code_driven(self) -> bool:
        """是否为代码驱动型"""
        return self.detect()["type"] == "code-driven"

    def get_audit_weights(self) -> Dict[str, float]:
        """
        根据 Skill 类型获取 audit 权重

        Returns:
            维度权重字典，权重之和为 1.0
        """
        skill_type = self.detect()["type"]

        if skill_type == "doc-only":
            # 纯文档型：跳过代码/测试/工程化，新增文档结构/触发场景/输出规范/references深度
            return {
                "metadata": 0.15,
                "documentation": 0.25,
                "doc_structure": 0.15,      # 新增：SKILL.md 结构完整性
                "trigger_scenarios": 0.10,  # 新增：触发场景覆盖度
                "output_spec": 0.10,        # 新增：输出规范明确性
                "references_depth": 0.10,   # 新增：references 深度
                "templates": 0.10,
                "usability": 0.05,
            }
        elif skill_type == "hybrid":
            # 混合型：适度降低代码相关权重
            return {
                "metadata": 0.12,
                "documentation": 0.18,
                "code_quality": 0.12,
                "testing": 0.08,
                "engineering": 0.08,
                "doc_structure": 0.10,
                "trigger_scenarios": 0.08,
                "output_spec": 0.08,
                "templates": 0.08,
                "usability": 0.04,
                "maintainability": 0.04,
            }
        else:
            # 代码驱动型：保持原有权重
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

    def get_optimize_scopes(self) -> List[str]:
        """
        根据 Skill 类型获取 optimize 适用范围

        Returns:
            适用的优化范围列表 ["docs", "code", "config", "tests"]
        """
        skill_type = self.detect()["type"]

        if skill_type == "doc-only":
            # 纯文档型：只优化文档和基础配置，不优化代码/测试/工程化
            return ["docs", "basic_config"]
        elif skill_type == "hybrid":
            return ["docs", "code", "config", "tests"]
        else:
            return ["docs", "code", "config", "tests"]


def detect_skill_type(skill_path: str) -> Dict:
    """便捷函数：检测 Skill 类型"""
    detector = SkillTypeDetector(skill_path)
    return detector.detect()


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Skill 类型自动检测")
    parser.add_argument("--path", required=True, help="Skill 路径")
    parser.add_argument("--json", action="store_true", help="以 JSON 格式输出")
    args = parser.parse_args()

    result = detect_skill_type(args.path)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"🔍 Skill 类型检测结果")
        print("=" * 50)
        print(f"  类型: {result['type']} ({result['description']})")
        print(f"  置信度: {result['confidence']:.0%}")
        print(f"  代码型得分: {result['code_score']}/100")
        print(f"  文档型得分: {result['doc_score']}/100")
        print(f"  Audit 权重: {result['type']} 模式")
        print(f"  Optimize 范围: {', '.join(SkillTypeDetector(args.path).get_optimize_scopes())}")
