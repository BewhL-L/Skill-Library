# 快速上手

> 5 分钟学会使用 Skill 工程化优化器

---

## 🎯 第一步：环境准备

### 系统要求
- Python 3.8+
- 任意操作系统（Windows/macOS/Linux）

### 验证 Python
```bash
python --version
# 输出: Python 3.8.x 或更高
```

> 💡 本工具仅使用 Python 标准库，**无需安装任何第三方依赖**。

---

## 🚀 第二步：运行健康检查

### 基本用法
```bash
python skill-opt.py audit --path ./your-skill
```

### 查看报告
运行后会显示：
- 总分（0-100）
- 8 大维度得分
- 问题清单（按严重程度排序）
- 优化建议

### 导出 JSON 报告
```bash
python skill-opt.py audit --path ./your-skill --format json --output report.json
```

---

## 🔧 第三步：自动优化

### 预览模式（推荐先运行）
```bash
python skill-opt.py optimize --path ./your-skill --dry-run
```
只显示将执行的操作，不实际修改文件。

### 执行优化
```bash
python skill-opt.py optimize --path ./your-skill --auto
```

自动完成：
- ✅ 补全缺失文档（README/CHANGELOG/FAQ 等 10 种）
- ✅ 生成工程化配置（.gitignore/.editorconfig/pre-commit/CI/CD）
- ✅ 统一项目配置（pyproject.toml/Makefile/requirements）

### 只优化指定部分
```bash
# 只优化文档
python skill-opt.py optimize --path ./your-skill --only docs

# 只优化配置
python skill-opt.py optimize --path ./your-skill --only config

# 优化文档和配置
python skill-opt.py optimize --path ./your-skill --only docs,config
```

---

## 📚 第四步：生成文档

### 生成所有文档
```bash
python skill-opt.py docs --path ./your-skill --type all
```

### 生成指定类型
```bash
# API 参考文档（自动解析函数签名）
python skill-opt.py docs --path ./your-skill --type api

# 常见问题
python skill-opt.py docs --path ./your-skill --type faq

# 使用案例
python skill-opt.py docs --path ./your-skill --type examples

# 架构文档
python skill-opt.py docs --path ./your-skill --type architecture
```

---

## 🧪 第五步：生成测试

### 生成所有测试
```bash
python skill-opt.py tests --path ./your-skill --type all
```

### 生成指定类型
```bash
# 单元测试（每个函数 3 个用例）
python skill-opt.py tests --path ./your-skill --type unit

# 集成测试（CLI 命令/工作流）
python skill-opt.py tests --path ./your-skill --type integration

# 覆盖率配置
python skill-opt.py tests --path ./your-skill --type coverage
```

### 运行生成的测试
```bash
cd your-skill
python -m pytest tests/ -v
```

---

## ⚡ 一键全流程（推荐）

```bash
python skill-opt.py all --path ./your-skill
```

自动执行：
1. 📋 健康检查
2. 🔧 自动优化
3. 📚 生成文档
4. 🧪 生成测试
5. 📊 输出优化报告

---

## 📊 典型优化流程

```bash
# 1. 评估现状
python skill-opt.py audit --path ./my-skill

# 2. 预览优化
python skill-opt.py optimize --path ./my-skill --dry-run

# 3. 执行优化
python skill-opt.py optimize --path ./my-skill --auto

# 4. 生成文档和测试
python skill-opt.py docs --path ./my-skill --type all
python skill-opt.py tests --path ./my-skill --type all

# 5. 手动完善（类型注解/测试用例/文档内容）
# 参考 OPTIMIZATION-GUIDE.md 第6-10轮

# 6. 再次评估
python skill-opt.py audit --path ./my-skill
```

---

## 🎓 深入学习

完成快速上手后，建议阅读：

1. **[OPTIMIZATION-GUIDE.md](OPTIMIZATION-GUIDE.md)** - 25 轮优化完整指南
   - 每轮优化的具体内容和操作步骤
   - 代码示例和最佳实践
   - 验收标准

2. **[CHECKLIST.md](CHECKLIST.md)** - 100+ 项检查清单
   - 按优先级分类（P0/P1/P2/P3）
   - 评分标准
   - 发布前验收清单

3. **[QUALITY-STANDARDS.md](QUALITY-STANDARDS.md)** - 质量标准
   - S/A/B/C/D 五级质量定义
   - 8 大维度详细标准
   - 验收流程

---

## ❓ 遇到问题？

- 查看 [FAQ.md](FAQ.md) - 常见问题解答
- 运行 `python skill-opt.py info` - 查看帮助信息
- 提交 Issue - 报告 Bug 或请求功能

---

> **5 分钟后，你应该已经：**
> - ✅ 运行了健康检查，了解 Skill 现状
> - ✅ 执行了自动优化，补全了文档和配置
> - ✅ 生成了 API 文档和测试模板
> - ✅ 知道下一步该做什么（参考 25 轮优化指南）
