# 全局标签集标准与同步报告模板

> 供 multi-kb-sync 执行多知识库同步时参考，按标签集标准和报告模板执行。

---

## 全局标签集标准

### 一级标签（技术领域）

| 标签 | 说明 | 包含范围 |
|------|------|---------|
| `#java` | Java 技术栈 | Java 基础、JVM、Spring、微服务 |
| `#frontend` | 前端技术栈 | Vue3、TypeScript、Vite、CSS |
| `#python` | Python 技术栈 | Python 基础、FastAPI、Django |
| `#ai-engineering` | AI 工程化 | LLM、RAG、Agent、LangChain |
| `#database` | 数据库与缓存 | MySQL、Redis、MongoDB、向量数据库 |
| `#devops` | 运维与部署 | Docker、K8s、CI/CD、Linux |
| `#algorithm` | 算法与数据结构 | 算法题、数据结构、复杂度分析 |
| `#system-design` | 系统设计 | 架构设计、高并发、分布式 |
| `#soft-skills` | 软技能 | 面试、简历、职业规划 |

### 二级标签（技术细分）

| 一级标签 | 二级标签示例 |
|---------|------------|
| `#java` | `#java/jvm`、`#java/spring-boot`、`#java/spring-cloud`、`#java/mybatis`、`#java/concurrency` |
| `#frontend` | `#frontend/vue3`、`#frontend/typescript`、`#frontend/vite`、`#frontend/css`、`#frontend/performance` |
| `#python` | `#python/fastapi`、`#python/async`、`#python/django`、`#python/pandas` |
| `#ai-engineering` | `#ai/llm`、`#ai/rag`、`#ai/agent`、`#ai/langchain`、`#ai/embedding`、`#ai/prompt` |
| `#database` | `#database/mysql`、`#database/redis`、`#database/mongodb`、`#database/vector-db` |
| `#devops` | `#devops/docker`、`#devops/k8s`、`#devops/cicd`、`#devops/linux`、`#devops/nginx` |

### 三级标签（状态/类型）

| 标签 | 说明 |
|------|------|
| `#status/learning` | 正在学习 |
| `#status/reviewing` | 需要复习 |
| `#status/mastered` | 已掌握 |
| `#type/concept` | 概念笔记 |
| `#type/tutorial` | 教程笔记 |
| `#type/cheatsheet` | 速查表 |
| `#type/project` | 项目笔记 |
| `#type/interview` | 面试题 |
| `#priority/high` | 高优先级 |
| `#priority/medium` | 中优先级 |
| `#priority/low` | 低优先级 |

---

## 同步操作规范

### 1. 标签同步

- 所有知识库使用统一的全局标签集
- 新增标签必须先在全局标签集中登记，再同步到各知识库
- 废弃标签标记为 `#deprecated`，保留 3 个月后清理
- 标签命名规范：小写字母、连字符分隔、不超过 3 级

### 2. 模板同步

- 笔记模板（Frontmatter、五段式结构）全局统一
- 模板更新后，同步到所有知识库的 `templates/` 目录
- 各知识库可在全局模板基础上扩展，但不得修改核心字段

### 3. 样式同步

- CSS 片段（callout、代码块、表格样式）全局统一
- 样式更新后，同步到所有知识库的 `snippets/` 目录
- 各知识库可添加自定义样式，但不得与全局样式冲突

### 4. 配置同步

- Dataview 查询、Templater 脚本、快捷键配置全局统一
- 配置更新后，同步到所有知识库的 `.obsidian/` 目录
- 各知识库可保留本地配置，但核心配置必须一致

---

## 同步报告模板

```markdown
## 📊 多知识库同步报告

**同步时间**：YYYY-MM-DD HH:mm
**同步范围**：知识库A、知识库B、知识库C（共 N 个）
**同步类型**：全量同步 / 增量同步
**操作人**：AI 助手

### 同步内容概览
| 同步项 | 同步前 | 同步后 | 变更数 | 状态 |
|--------|--------|--------|--------|------|
| 全局标签集 | N 个 | N 个 | +N/-N | ✅ 完成 |
| 笔记模板 | N 个 | N 个 | +N/-N | ✅ 完成 |
| CSS 样式 | N 个 | N 个 | +N/-N | ✅ 完成 |
| 配置文件 | N 个 | N 个 | +N/-N | ✅ 完成 |

### 各知识库同步详情
#### 知识库A
- 标签：新增 N 个，更新 N 个，删除 N 个
- 模板：更新 N 个
- 样式：更新 N 个
- 配置：更新 N 个
- 问题：无 / 列出问题

#### 知识库B
...

### 冲突处理
| 冲突项 | 知识库A | 知识库B | 处理方式 | 结果 |
|--------|---------|---------|---------|------|
| 标签定义 | 定义A | 定义B | 以全局标准为准 | 已统一 |
| ... | ... | ... | ... | ... |

### 未同步项（需人工确认）
- [ ] 项1：原因说明
- [ ] 项2：原因说明

### 同步质量检查
- [ ] 所有知识库标签集一致
- [ ] 所有知识库模板一致
- [ ] 所有知识库样式一致
- [ ] 所有知识库核心配置一致
- [ ] 无未处理的冲突
- [ ] 同步后各知识库可正常打开

### 下次同步建议
- 建议同步时间：YYYY-MM-DD
- 需要重点同步的内容：XXX
- 需要人工处理的遗留问题：XXX
```

---

## 标签冲突处理规则

| 冲突类型 | 处理规则 |
|---------|---------|
| 同名不同义 | 以全局标签集定义为准，修改各知识库的使用 |
| 同义不同名 | 合并为一个标签，更新所有引用 |
| 层级冲突 | 以全局标签集的层级为准，调整各知识库的标签层级 |
| 废弃标签 | 标记 `#deprecated`，3 个月后批量替换并删除 |
| 新增标签 | 先在全局标签集登记，再同步到各知识库 |
