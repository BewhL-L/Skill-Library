# 版本发布指南

## 📋 概述

本文档描述 Obsidian 知识库标准化生成器的版本发布流程，包括发布前检查、版本号规范、发布步骤和发布后维护。

---

## 🎯 版本号规范

### 语义化版本

遵循 [语义化版本 2.0.0](https://semver.org/lang/zh-CN/)：

```
主版本号.次版本号.修订号
  │       │       │
  │       │       └─ 修订号：向后兼容的问题修正
  │       └───────── 次版本号：向下兼容的功能性新增
  └────────────────── 主版本号：不兼容的 API 变更
```

### 版本类型

| 类型 | 示例 | 说明 | 发布频率 |
|------|------|------|---------|
| 主版本（Major） | 3.0.0 → 4.0.0 | 不兼容的 API 变更 | 每年 1-2 次 |
| 次版本（Minor） | 3.1.0 → 3.2.0 | 向下兼容的新功能 | 每月 1 次 |
| 修订版（Patch） | 3.1.0 → 3.1.1 | 向下兼容的 Bug 修复 | 随时 |

### 预发布版本

| 类型 | 示例 | 说明 |
|------|------|------|
| Alpha | 3.2.0-alpha.1 | 内部测试，功能可能不完整 |
| Beta | 3.2.0-beta.1 | 公开测试，功能基本完整 |
| RC | 3.2.0-rc.1 | 发布候选，仅修复 Bug |

---

## 📅 发布计划

### 常规发布周期

| 版本类型 | 计划时间 | 内容 |
|---------|---------|------|
| Patch | 随时 | 紧急 Bug 修复 |
| Minor | 每月最后一个周五 | 新功能汇总 |
| Major | 每年 1 月和 7 月 | 重大变更 |

### 发布冻结期

- **Minor 版本**：发布前 3 天冻结新功能，只修复 Bug
- **Major 版本**：发布前 7 天冻结新功能，进入 RC 阶段
- **Patch 版本**：无冻结期，随时发布

---

## ✅ 发布前检查清单

### 代码质量检查

- [ ] 所有测试通过（单元测试 + 集成测试）
- [ ] 代码覆盖率不低于 90%
- [ ] 代码质量检查 0 错误 0 警告
- [ ] 类型检查通过（mypy）
- [ ] pre-commit 钩子全部通过
- [ ] CI/CD 所有 Job 通过

### 文档检查

- [ ] README.md 已更新
- [ ] CHANGELOG.md 已更新
- [ ] 新增功能有对应的文档
- [ ] API 文档已更新（API.md）
- [ ] 安装指南已更新（INSTALLATION.md）
- [ ] 所有示例代码可正常运行

### 功能检查

- [ ] 所有新功能已完成并测试
- [ ] 所有已知 Bug 已修复或记录
- [ ] 向后兼容性已验证
- [ ] 破坏性变更有迁移指南
- [ ] 性能没有明显下降

### 发布准备

- [ ] 版本号已更新（pyproject.toml, scripts/kb.py, 文档）
- [ ] 发布说明已撰写
- [ ] 发布标签已准备
- [ ] 发布公告已准备

---

## 🚀 发布步骤

### Patch 版本发布（Bug 修复）

#### 1. 确认 Bug 修复

```bash
# 确保在主分支
git checkout main
git pull origin main

# 运行所有测试
make test

# 运行代码质量检查
make check
```

#### 2. 更新版本号

```bash
# 编辑 pyproject.toml
# version = "3.1.0" → version = "3.1.1"

# 编辑 scripts/kb.py 中的版本号
# __version__ = "3.1.0" → __version__ = "3.1.1"
```

#### 3. 更新 CHANGELOG.md

```markdown
## [3.1.1] - 2026-08-30

### 修复
- 修复 XXX 功能在 Windows 下的兼容性问题
- 修复 XXX 命令在大知识库下的性能问题
- 修复文档中的错别字和链接错误
```

#### 4. 提交并打标签

```bash
git add pyproject.toml scripts/kb.py CHANGELOG.md
git commit -m "chore: release v3.1.1"

git tag -a v3.1.1 -m "Release v3.1.1

Bug fixes:
- Fix Windows compatibility issue
- Fix performance issue with large knowledge bases
- Fix typos and broken links in documentation"

git push origin main --tags
```

#### 5. 发布到 GitHub

1. 前往 GitHub Releases 页面
2. 点击 "Draft a new release"
3. 选择标签 v3.1.1
4. 填写发布标题和说明
5. 点击 "Publish release"

---

### Minor 版本发布（新功能）

#### 1. 功能冻结

发布前 3 天：
- 停止合并新功能 PR
- 只接受 Bug 修复 PR
- 开始全面测试

#### 2. 全面测试

```bash
# 运行所有测试
make test

# 运行代码质量检查
make check

# 运行性能基准测试
# 对比上一版本的性能

# 在不同平台测试
# Windows / macOS / Linux
# Python 3.8 / 3.9 / 3.10 / 3.11 / 3.12
```

#### 3. 更新版本号和文档

```bash
# 更新版本号
# 3.1.0 → 3.2.0

# 更新所有文档中的版本引用
# README.md, SKILL.md, FAQ.md, etc.

# 更新 API.md（如有新函数）

# 更新 CHANGELOG.md
```

#### 4. CHANGELOG.md 格式

```markdown
## [3.2.0] - 2026-08-30

### ✨ 新功能
- 新增 XXX 命令，支持 XXX 功能
- 新增 XXX 配置选项
- 支持 XXX 平台

### 🚀 性能优化
- 优化 XXX 功能，性能提升 50%
- 减少内存占用 30%

### 🐛 Bug 修复
- 修复 XXX 问题
- 修复 XXX 兼容性问题

### 📝 文档更新
- 更新 XXX 文档
- 新增 XXX 指南

### ⚠️ 破坏性变更
- XXX API 已变更，请参考迁移指南

### 🔧 维护
- 更新依赖到最新版本
- 重构 XXX 模块
```

#### 5. 发布候选（RC）阶段（可选）

对于重大功能更新：

```bash
# 创建 RC 版本
git tag -a v3.2.0-rc.1 -m "Release Candidate 1 for v3.2.0"
git push origin v3.2.0-rc.1

# 发布 RC 版本到 GitHub
# 邀请社区测试
# 收集反馈并修复 Bug

# 一周后发布正式版
git tag -a v3.2.0 -m "Release v3.2.0"
git push origin v3.2.0
```

---

### Major 版本发布（重大变更）

#### 1. 长期准备（3-6 个月）

- 制定详细的发布计划
- 分阶段实现重大变更
- 保持向后兼容（尽可能）
- 提供迁移工具和指南
- 多次 Alpha/Beta 测试

#### 2. Beta 测试阶段（1-2 个月）

```bash
# 发布 Alpha 版本
git tag -a v4.0.0-alpha.1 -m "Alpha 1 for v4.0.0"

# 收集反馈，迭代开发
# 发布多个 Alpha 版本

# 发布 Beta 版本
git tag -a v4.0.0-beta.1 -m "Beta 1 for v4.0.0"

# 公开测试，收集更多反馈

# 发布 RC 版本
git tag -a v4.0.0-rc.1 -m "Release Candidate 1 for v4.0.0"

# 最终测试和 Bug 修复

# 发布正式版
git tag -a v4.0.0 -m "Release v4.0.0"
```

#### 3. 迁移指南

Major 版本必须提供详细的迁移指南：

```markdown
# 从 v3.x 迁移到 v4.0

## 概述
v4.0 包含以下重大变更：
- XXX API 重构
- XXX 配置格式变更
- 移除 XXX 废弃功能

## 迁移步骤

### 1. 备份
备份你的知识库和配置文件。

### 2. 更新配置
旧格式：
```yaml
old_config: value
```

新格式：
```yaml
new_config: value
```

### 3. 更新代码
旧 API：
```python
old_function()
```

新 API：
```python
new_function()
```

### 4. 运行迁移工具
```bash
python scripts/migrate-v3-to-v4.py --path ./my-kb
```

### 5. 验证
运行测试确保一切正常。

## 常见问题
...
```

---

## 📢 发布后维护

### 发布公告

发布后需要在以下渠道发布公告：

1. **GitHub Releases** - 官方发布说明
2. **GitHub Discussions** - 社区公告
3. **社交媒体** - Twitter、微博等
4. **邮件列表** - 订阅用户通知
5. **CHANGELOG.md** - 版本变更记录

### 公告模板

```markdown
# 🎉 Obsidian 知识库标准化生成器 v3.2.0 发布！

我们很高兴地宣布 v3.2.0 版本正式发布！

## ✨ 主要新功能

### 1. XXX 功能
描述...

### 2. XXX 功能
描述...

## 🚀 性能优化
- XXX 性能提升 50%

## 🐛 Bug 修复
- 修复了 XXX 问题

## 📥 升级方式

```bash
# 使用 Git
git pull origin main

# 或下载最新版本
# https://github.com/your-username/obsidian-knowledge-base-creator/releases
```

## 🙏 致谢
感谢所有贡献者和反馈者！

完整变更日志请查看 [CHANGELOG.md](../CHANGELOG.md)。
```

### 发布后监控

发布后需要密切监控：

- **Issue 监控**：关注新发布的 Bug 报告
- **CI/CD 监控**：确保所有检查通过
- **性能监控**：关注性能反馈
- **社区反馈**：关注讨论区的反馈

### 紧急修复（Hotfix）

如果发布后发现严重 Bug：

1. **评估严重程度**：
   - 🔴 严重：影响所有用户，数据丢失风险 → 立即发布 Hotfix
   - 🟠 高：影响主要功能 → 24 小时内发布 Hotfix
   - 🟡 中：影响次要功能 → 包含在下个 Patch 版本
   - 🟢 低：轻微问题 → 包含在下个 Minor 版本

2. **创建 Hotfix 分支**：
```bash
git checkout -b hotfix/3.2.1 v3.2.0
# 修复 Bug
git commit -m "fix: critical bug in XXX"
git tag -a v3.2.1 -m "Hotfix v3.2.1"
git push origin hotfix/3.2.1 --tags
```

3. **合并到主分支**：
```bash
git checkout main
git merge hotfix/3.2.1
git push origin main
```

4. **发布紧急修复版本**

---

## 📊 版本统计

### 版本历史统计

| 版本 | 发布日期 | 新增功能 | Bug 修复 | 贡献者数 |
|------|---------|---------|---------|---------|
| v1.0 | 2026-08 | 5 | 0 | 1 |
| v2.0 | 2026-08 | 3 | 2 | 1 |
| v2.1 | 2026-08 | 3 | 1 | 1 |
| v2.2 | 2026-08 | 2 | 1 | 1 |
| v2.3 | 2026-08 | 3 | 2 | 1 |
| v2.4 | 2026-08 | 2 | 1 | 1 |
| v2.5 | 2026-08 | 4 | 2 | 1 |
| v2.6 | 2026-08 | 1 | 0 | 1 |
| v3.0 | 2026-08 | 2 | 1 | 1 |
| v3.1 | 2026-08 | 5 | 2 | 1 |

### 发布频率统计

- **平均发布间隔**：X 天
- **最长发布间隔**：X 天
- **最短发布间隔**：X 天
- **总发布次数**：10 次

---

## 🔗 相关文档

- [CHANGELOG.md](../CHANGELOG.md) - 版本变更记录
- [GOVERNANCE.md](GOVERNANCE.md) - 项目治理
- [CONTRIBUTING.md](CONTRIBUTING.md) - 贡献指南
- [ROADMAP.md](ROADMAP.md) - 发展路线图

---

> **最后更新**：2026-08-30
>
> **版本**：v1.0
