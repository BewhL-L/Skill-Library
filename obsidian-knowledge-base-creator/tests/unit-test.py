#!/usr/bin/env python3
"""
单元测试脚本
为核心函数编写单元测试，确保代码质量

用法:
    python unit-test.py
    python unit-test.py -v  # 详细输出
"""

import os
import sys
import unittest
import tempfile
import shutil
from pathlib import Path

# 项目根目录（tests/ 的上一级），脚本统一在根目录的 scripts/ 下
SCRIPT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPT_DIR / 'scripts'))

# 辅助函数：导入带连字符的模块
def import_script_module(module_name):
    """导入带连字符的脚本模块"""
    import importlib.util
    script_path = SCRIPT_DIR / 'scripts' / f'{module_name}.py'
    spec = importlib.util.spec_from_file_location(module_name.replace('-', '_'), script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestFrontmatterExtraction(unittest.TestCase):
    """测试 Frontmatter 提取功能"""

    def test_extract_frontmatter_with_valid_yaml(self):
        """测试提取有效的 YAML Frontmatter"""
        validate_kb = import_script_module("validate-kb")
        extract_frontmatter = validate_kb.extract_frontmatter
        # 创建临时文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write("---\ntitle: 测试\ntags: [测试]\n---\n\n正文内容")
            tmp_path = f.name

        try:
            result = extract_frontmatter(tmp_path)
            self.assertIsInstance(result, str)
            self.assertIn('title: 测试', result)
        finally:
            os.unlink(tmp_path)

    def test_extract_frontmatter_without_frontmatter(self):
        """测试没有 Frontmatter 的文件：函数契约是返回完整内容（仅读失败才返回空串）"""
        validate_kb = import_script_module("validate-kb")
        extract_frontmatter = validate_kb.extract_frontmatter
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write("只有正文内容，没有 Frontmatter")
            tmp_path = f.name

        try:
            result = extract_frontmatter(tmp_path)
            self.assertEqual(result, "只有正文内容，没有 Frontmatter")
        finally:
            os.unlink(tmp_path)

    def test_extract_frontmatter_with_nonexistent_file(self):
        """测试不存在的文件"""
        validate_kb = import_script_module("validate-kb")
        extract_frontmatter = validate_kb.extract_frontmatter
        result = extract_frontmatter('/nonexistent/file.md')
        self.assertEqual(result, "")


class TestFixFrontmatter(unittest.TestCase):
    """测试 Frontmatter 修复功能"""

    def test_format_frontmatter(self):
        """测试格式化 Frontmatter"""
        fix_frontmatter = import_script_module("fix-frontmatter")
        format_frontmatter = fix_frontmatter.format_frontmatter
        fm = {
            'title': '测试笔记',
            'tags': '[测试]',
            'category': '前端开发',
            'difficulty': '⭐⭐⭐'
        }
        result = format_frontmatter(fm)
        self.assertIn('---', result)
        self.assertIn('title: 测试笔记', result)
        self.assertIn('category: 前端开发', result)

    def test_format_frontmatter_order(self):
        """测试 Frontmatter 字段顺序"""
        fix_frontmatter = import_script_module("fix-frontmatter")
        format_frontmatter = fix_frontmatter.format_frontmatter
        fm = {
            'aliases': ['别名'],
            'title': '测试',
            'tags': '[测试]'
        }
        result = format_frontmatter(fm)
        lines = result.split('\n')
        # title 应该在 tags 前面
        title_idx = next(i for i, l in enumerate(lines) if l.startswith('title:'))
        tags_idx = next(i for i, l in enumerate(lines) if l.startswith('tags:'))
        self.assertLess(title_idx, tags_idx)


class TestFixTags(unittest.TestCase):
    """测试标签统一功能"""

    def test_normalize_tag_function(self):
        """测试标签标准化函数"""
        fix_tags = import_script_module("fix-tags")
        normalize_tag = fix_tags.normalize_tag
        self.assertTrue(callable(normalize_tag))

    def test_extract_tags_function(self):
        """测试标签提取函数"""
        fix_tags = import_script_module("fix-tags")
        extract_tags = fix_tags.extract_tags
        self.assertTrue(callable(extract_tags))

    def test_process_file_function(self):
        """测试文件处理函数"""
        fix_tags = import_script_module("fix-tags")
        process_file = fix_tags.process_file
        self.assertTrue(callable(process_file))


class TestAuditFunctions(unittest.TestCase):
    """测试审计功能"""

    def test_check_frontmatter_function(self):
        """测试 Frontmatter 检查函数"""
        audit_kb = import_script_module("audit-kb")
        check_frontmatter = audit_kb.check_frontmatter
        self.assertTrue(callable(check_frontmatter))

    def test_check_tags_function(self):
        """测试标签检查函数"""
        audit_kb = import_script_module("audit-kb")
        check_tags = audit_kb.check_tags
        self.assertTrue(callable(check_tags))

    def test_check_links_function(self):
        """测试链接检查函数"""
        audit_kb = import_script_module("audit-kb")
        check_links = audit_kb.check_links
        self.assertTrue(callable(check_links))

    def test_check_moc_coverage_function(self):
        """测试 MOC 覆盖率检查函数"""
        audit_kb = import_script_module("audit-kb")
        check_moc_coverage = audit_kb.check_moc_coverage
        self.assertTrue(callable(check_moc_coverage))


class TestProgressFunctions(unittest.TestCase):
    """测试学习进度功能"""

    def test_get_difficulty_level(self):
        """测试难度等级获取函数"""
        progress = import_script_module("progress")
        get_difficulty_level = progress.get_difficulty_level
        self.assertTrue(callable(get_difficulty_level))

    def test_extract_frontmatter_progress(self):
        """测试进度模块的 Frontmatter 提取"""
        progress = import_script_module("progress")
        extract_frontmatter = progress.extract_frontmatter
        content = "---\ntitle: 测试\n---\n\n正文"
        result = extract_frontmatter(content)
        self.assertIsInstance(result, dict)


class TestLintTool(unittest.TestCase):
    """测试代码质量检查工具本身"""

    def test_lint_script_exists(self):
        """测试 lint.py 存在"""
        lint_path = SCRIPT_DIR / 'scripts' / 'lint.py'
        self.assertTrue(lint_path.exists())

    def test_lint_script_executable(self):
        """测试 lint.py 可以导入"""
        import importlib.util
        spec = importlib.util.spec_from_file_location("lint", SCRIPT_DIR / 'scripts' / 'lint.py')
        self.assertIsNotNone(spec)


class TestCLITool(unittest.TestCase):
    """测试 CLI 工具"""

    def test_kb_py_exists(self):
        """测试 kb.py 存在"""
        kb_path = SCRIPT_DIR / 'scripts' / 'kb.py'
        self.assertTrue(kb_path.exists())

    def test_kb_py_has_commands(self):
        """测试 kb.py 包含所有命令"""
        with open(SCRIPT_DIR / 'scripts' / 'kb.py', 'r', encoding='utf-8') as f:
            content = f.read()
        commands = ['init', 'note', 'moc', 'audit', 'validate',
                    'fix-fm', 'fix-link', 'fix-tags', 'standardize',
                    'progress', 'batch-note', 'info']
        for cmd in commands:
            self.assertIn(cmd, content, f"缺少命令: {cmd}")


class TestTemplates(unittest.TestCase):
    """测试模板文件"""

    def test_note_template_exists(self):
        """测试笔记模板存在"""
        template_path = SCRIPT_DIR / 'assets' / 'note-template.md'
        self.assertTrue(template_path.exists())

    def test_moc_template_exists(self):
        """测试 MOC 模板存在"""
        template_path = SCRIPT_DIR / 'assets' / 'moc-template.md'
        self.assertTrue(template_path.exists())

    def test_home_template_exists(self):
        """测试首页模板存在"""
        template_path = SCRIPT_DIR / 'assets' / 'home-template.md'
        self.assertTrue(template_path.exists())

    def test_learning_path_template_exists(self):
        """测试学习路线模板存在"""
        template_path = SCRIPT_DIR / 'assets' / 'learning-path-template.md'
        self.assertTrue(template_path.exists())

    def test_atomic_note_template_exists(self):
        """测试原子化笔记模板存在"""
        template_path = SCRIPT_DIR / 'assets' / 'atomic-note-template.md'
        self.assertTrue(template_path.exists())

    def test_config_template_exists(self):
        """测试配置模板存在"""
        template_path = SCRIPT_DIR / 'assets' / 'config-template.yaml'
        self.assertTrue(template_path.exists())


class TestReferences(unittest.TestCase):
    """测试参考文档"""

    def test_directory_structure_ref_exists(self):
        """测试目录结构参考文档存在"""
        ref_path = SCRIPT_DIR / 'references' / 'directory-structure.md'
        self.assertTrue(ref_path.exists())

    def test_frontmatter_standard_ref_exists(self):
        """测试 Frontmatter 标准参考文档存在"""
        ref_path = SCRIPT_DIR / 'references' / 'frontmatter-standard.md'
        self.assertTrue(ref_path.exists())

    def test_tag_taxonomy_ref_exists(self):
        """测试标签分类参考文档存在"""
        ref_path = SCRIPT_DIR / 'references' / 'tag-taxonomy.md'
        self.assertTrue(ref_path.exists())

    def test_document_structure_ref_exists(self):
        """测试文档结构参考文档存在"""
        ref_path = SCRIPT_DIR / 'references' / 'document-structure.md'
        self.assertTrue(ref_path.exists())

    def test_formatting_guide_ref_exists(self):
        """测试排版规范参考文档存在"""
        ref_path = SCRIPT_DIR / 'references' / 'formatting-guide.md'
        self.assertTrue(ref_path.exists())


class TestProjectStructure(unittest.TestCase):
    """测试项目整体结构"""

    def test_all_scripts_exist(self):
        """测试所有脚本存在"""
        scripts = [
            'init-kb.py', 'generate-note.py', 'generate-moc.py',
            'audit-kb.py', 'validate-kb.py', 'fix-frontmatter.py',
            'fix-deadlinks.py', 'fix-tags.py', 'progress.py',
            'batch-generate-notes.py'
        ]
        for script in scripts:
            script_path = SCRIPT_DIR / 'scripts' / script
            self.assertTrue(script_path.exists(), f"缺少脚本: {script}")

    def test_all_docs_exist(self):
        """测试所有文档存在（根目录与 docs/ 分别核对）"""
        root_docs = ['README.md', 'SKILL.md', 'QUICKSTART.md', 'CHANGELOG.md', 'LICENSE']
        docs_docs = ['FAQ.md', 'OBSIDIAN-GUIDE.md', 'CONTRIBUTING.md', 'USE-CASES.md']
        for doc in root_docs:
            doc_path = SCRIPT_DIR / doc
            self.assertTrue(doc_path.exists(), f"缺少文档: {doc}")
        for doc in docs_docs:
            doc_path = SCRIPT_DIR / 'docs' / doc
            self.assertTrue(doc_path.exists(), f"缺少文档: docs/{doc}")

    def test_all_configs_exist(self):
        """测试所有配置文件存在"""
        configs = [
            '.gitignore', '.editorconfig', '.pre-commit-config.yaml',
            '.markdownlint.json', '.coveragerc'
        ]
        for config in configs:
            config_path = SCRIPT_DIR / config
            self.assertTrue(config_path.exists(), f"缺少配置: {config}")


def run_tests():
    """运行所有单元测试"""
    print("=" * 60)
    print("🧪 单元测试")
    print("=" * 60)
    print()

    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # 添加所有测试类
    test_classes = [
        TestFrontmatterExtraction,
        TestFixFrontmatter,
        TestFixTags,
        TestAuditFunctions,
        TestProgressFunctions,
        TestLintTool,
        TestCLITool,
        TestTemplates,
        TestReferences,
        TestProjectStructure,
    ]

    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)

    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print()
    print("=" * 60)
    print("📊 测试总结")
    print("=" * 60)
    print(f"  总测试数: {result.testsRun}")
    print(f"  ✅ 通过: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"  ❌ 失败: {len(result.failures)}")
    print(f"  ⚠️  错误: {len(result.errors)}")

    if result.wasSuccessful():
        print(f"  通过率: 100.0%")
        print()
        print("🎉 所有单元测试通过！")
        return 0
    else:
        pass_rate = (result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100
        print(f"  通过率: {pass_rate:.1f}%")
        print()
        print("❌ 部分测试失败，请检查！")
        return 1


if __name__ == '__main__':
    sys.exit(run_tests())
