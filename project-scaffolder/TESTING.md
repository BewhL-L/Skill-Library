# 测试指南

> **注意**：本 Skill 为**纯文档型 Skill**，无可执行代码和自动化测试。本文档说明 Skill 的"质量验证"方法——即如何验证 Skill 生成的项目质量。

---

## Skill 自身质量验证

### 1. 健康检查（audit）

使用 skill-optimizer 工具运行健康检查：

```bash
cd skill-optimizer
python scripts/audit-skill.py --path /path/to/project-scaffolder
```

检查维度（纯文档型模式，8 维度）：
- metadata（元数据完整性）
- documentation（文档完整性）
- templates（模板资源）
- usability（易用性）
- doc_structure（SKILL.md 结构）
- trigger_scenarios（触发场景覆盖）
- output_spec（输出规范明确性）
- references_depth（references 深度）

### 2. 类型检测

```bash
python scripts/skill_type_detector.py --path /path/to/project-scaffolder
```

确认检测为 `doc-only`（纯文档型），置信度 ≥ 90%。

---

## Skill 生成项目的质量验证

Skill 生成项目后，通过第六步的 **12 维度自检**验证质量：

### 基础维度（1-5）

| 维度 | 验证方法 |
|------|----------|
| 产物自检 | 检查文件完整性、可打开性、入口明确性 |
| 文档自检 | 检查每章七要素、人机分工、可视化、格式规范 |
| 分工自检 | 检查每个产物标注 A/B/C、C 类有验证方法 |
| 通用性自检 | 检查流程适配不同项目类型 |
| 可执行性自检 | 检查用户能按文档启动、操作、验收 |

### 深度维度（6-11）

| 维度 | 验证方法 |
|------|----------|
| 前后端契约 | 列出前端所有 API 调用，逐条与后端路由比对 |
| 依赖完整性 | 扫描 import，与依赖清单比对 |
| 静态资源 | 扫描引用的资源路径，确认文件存在 |
| 框架语法 | 按框架特定规则逐条核对 |
| 运行时验证 | 实际执行导入/构建命令，确认无错误 |
| 内容完整性 | 对照标配功能清单，逐项检查 P0/P1 实现 |

---

## 手动验证清单

每次修改 Skill 后，手动验证以下内容：

### SKILL.md 验证

- [ ] Frontmatter 有 name 和 description
- [ ] description 包含触发词和适用场景
- [ ] 七步工作流程完整（第一步~第七步）
- [ ] 第三步有 13 条生成质量强制约束（含工程底座六件套、文档断言、私有边界、反假完备、测试可复现）
- [ ] 第六步有 12 个自检维度（第 12 维：工程底座与文档一致性）
- [ ] References 导航列出所有 references 文件（含 engineering-baseline.md）
- [ ] 末尾有版本号和最后更新日期

### 脚本单测

```bash
python -m pytest tests -q      # 8 例：schema/index/private/deadconfig/退出码
```

### 脚本单测

```bash
python -m pytest tests -q      # 8 例：schema/index/private/deadconfig/退出码
```

### references 验证

- [ ] 5 个 references 文件都存在
- [ ] 每个文件在 SKILL.md 中有对应引用
- [ ] content-completeness.md 覆盖 7 大项目类型
- [ ] Markdown 表格列数一致（无 1 列≠2 列的错误）

### 文档验证

- [ ] README.md 内容 ≥ 500 字，包含功能/安装/使用/文档导航
- [ ] QUICKSTART.md 提供 5 分钟快速上手
- [ ] CHANGELOG.md 记录版本变更
- [ ] FAQ.md 覆盖常见问题

---

## 回归测试

每次修改 Skill 后，用一个真实项目测试完整流程：

1. 说"我想做一个 XX 项目"
2. 观察是否正确识别项目类型
3. 检查第二步是否生成功能完整性矩阵
4. 检查第三步是否同步生成 P1 周边功能
5. 检查第六步是否执行 12 维度自检
6. 检查最终交付是否完整

**测试项目建议**：
- 社交类（验证收藏/搜索/通知等周边功能）
- 学习类（验证练习题/进度跟踪等）
- 商业类（验证财务模型/SOP 等）
- 混合型（验证类型组合处理）

---

*本 Skill 为纯文档型，无自动化测试框架，质量保证依赖健康检查工具和手动验证清单。*
