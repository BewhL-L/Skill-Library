# 贡献指南

感谢你愿意改进"项目流程化"Skill。

## 提交前检查

```bash
python -m py_compile scripts/*.py        # 语法
python -m pytest tests -v                # 全部测试通过
python -m pytest tests --cov=scripts     # 覆盖率
python -m ruff check scripts tests       # 风格（如已安装）
```

## 约定

- 脚本保持**纯标准库**、跨平台；新增第三方依赖需要在 PR 中说明必要性。
- 所有函数补全类型注解与 docstring；单文件控制在 500 行以内。
- 新增/修改脚本行为时，同步补充单元测试；修复 bug 先写复现测试。
- 改动方法论文档时，保持"五条铁律"不被削弱；示例数字必须可追溯。
- 若修改了脚本或 SKILL.md，在 `CHANGELOG.md` 记录变更并按需升级版本号。

## 提交信息

遵循 Conventional Commits：

- `feat:` 新功能
- `fix:` 缺陷修复
- `docs:` 文档
- `test:` 测试
- `refactor:` / `chore:` 重构 / 杂项

## 提交流程

1. Fork 并新建分支：`git checkout -b feat/your-change`。
2. 小步提交，保证每步测试通过。
3. 提交 PR，说明：解决的问题、实现方式、如何验证（附测试结果）。
4. 维护者评审通过后合并。

## 报告问题

提交 issue 时请附：操作系统与 Python 版本、复现命令、期望与实际结果、最小样例项目。
