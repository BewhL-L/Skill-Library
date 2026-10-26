# 贡献指南

感谢你对本项目的关注！

## 开发环境搭建

```bash
# 1. Fork 并克隆
git clone <your-fork>
cd <project>

# 2. 安装依赖
pip install -r requirements-dev.txt

# 3. 安装 pre-commit
pre-commit install
```

## 提交规范

使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

- `feat:` 新功能
- `fix:` Bug 修复
- `docs:` 文档更新
- `style:` 代码格式
- `refactor:` 重构
- `test:` 测试
- `chore:` 构建/工具

## 提交流程

1. 创建功能分支
2. 提交更改
3. 运行测试
4. 提交 Pull Request

## 代码规范

- Python: PEP 8
- 类型注解: 100% 覆盖
- 测试覆盖率: ≥80%
