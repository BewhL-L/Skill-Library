# 架构文档

> 本文档描述 career-life-guidance Skill 的架构设计。由于本Skill为纯文档型（doc-only），架构以文档组织、工作流程和资源引用为核心。

## 架构总览

```
career-life-guidance/
│
├── 📄 核心文档层
│   ├── SKILL.md              # Skill入口，工作流程与校验清单
│   ├── README.md             # 项目首页，功能概览
│   └── QUICKSTART.md         # 快速上手指南
│
├── 📚 参考文档层（12个，按使用频率编号）
│   ├── references/
│   │   ├── 01-user-profiling.md      # 用户画像与身份校准
│   │   ├── 02-track-selection.md     # 赛道选择与行业取证
│   │   ├── 03-six-phase-structure.md # 六篇结构与章节规划
│   │   ├── 04-learning-roadmap.md    # 学习路线与时间管理
│   │   ├── 05-project-playbook.md    # 项目实战手册（最高频）
│   │   ├── 06-job-hunting.md         # 求职冲刺与面试
│   │   ├── 07-longterm-development.md# 中长期发展与35岁危机
│   │   ├── 08-support-dimensions.md  # 支撑维度（7大维度）
│   │   ├── 09-writing-style.md       # 写作风格与前辈语气
│   │   ├── 10-obsidian-output.md     # Obsidian标准化输出
│   │   ├── 11-iteration-protocol.md  # 多轮迭代协议
│   │   └── 12-document-anatomy.md    # 成品级文档解剖
│   ├── API.md                # 接口与资源参考
│   ├── FAQ.md                # 常见问题
│   └── USE-CASES.md          # 使用案例
│
├── 🎨 模板资源层
│   └── assets/
│       └── document-template.md  # 完整六篇文档骨架模板
│
├── 📝 工程化配置层
│   ├── .gitignore
│   ├── .editorconfig
│   └── LICENSE
│
└── 📖 治理文档层
    ├── CHANGELOG.md
    ├── CONTRIBUTING.md
    ├── SECURITY.md
    ├── CODE_OF_CONDUCT.md
    ├── INSTALLATION.md
    ├── SUPPORT.md
    ├── TESTING.md
    ├── DEBUGGING.md
    └── ARCHITECTURE.md       # 本文件
```

## 设计原则

### 1. 单一数据源（Single Source of Truth）

- 身份校准规范只存在于 `references/01-user-profiling.md`
- 项目实战方法只存在于 `references/05-project-playbook.md`
- 写作风格只存在于 `references/09-writing-style.md`
- 文档结构标准只存在于 `references/12-document-anatomy.md`
- 其他文档引用这些源，不重复定义

### 2. 渐进式披露（Progressive Disclosure）

| 层级 | 内容 | 加载时机 |
|------|------|---------|
| L1 | Skill元数据（name/description） | 始终在上下文 |
| L2 | SKILL.md正文 | Skill触发时加载 |
| L3 | references/文档（12个） | 需要时按需读取，勿一次性全读 |
| L4 | assets/document-template.md | 搭建全书骨架时复制 |

### 3. 按使用频率编号

references目录下的12个文档按使用频率从01到12编号：
- 01-04：基础层（身份、方向、结构、学习）
- 05：核心层（项目实战，最高频，单独突出）
- 06-08：应用层（求职、发展、支撑）
- 09-12：质量层（风格、输出、迭代、解剖）

### 4. 纯文档型架构

本Skill不包含可执行代码，所有功能通过：
- 标准化文档模板（复制+填充）
- 参考文档（遵循+应用）
- 工作流程（按8步执行）
- 校验清单（逐项检查）

由AI Agent执行，无需运行时环境。

## 数据流

```
用户需求（身份+目标+约束）
    │
    ▼
SKILL.md（8步工作流程）
    │
    ├─→ 第1步：身份校准
    │     └─→ 读取 references/01-user-profiling.md
    │
    ├─→ 第2步：赛道选择与取证
    │     └─→ 读取 references/02-track-selection.md
    │
    ├─→ 第3步：搭建全书骨架
    │     ├─→ 复制 assets/document-template.md
    │     └─→ 读取 references/03-six-phase-structure.md
    │           + references/12-document-anatomy.md
    │
    ├─→ 第4步：填充学习路线
    │     └─→ 读取 references/04-learning-roadmap.md
    │
    ├─→ 第5步：填充项目实战（重中之重）
    │     └─→ 读取 references/05-project-playbook.md
    │
    ├─→ 第6步：填充求职与长期发展
    │     ├─→ 读取 references/06-job-hunting.md
    │     └─→ 读取 references/07-longterm-development.md
    │
    ├─→ 第7步：补齐支撑维度与风险预案
    │     └─→ 读取 references/08-support-dimensions.md
    │
    ├─→ 第8步：标准化输出与校验
    │     ├─→ 读取 references/09-writing-style.md（风格核对）
    │     ├─→ 读取 references/10-obsidian-output.md（格式标准化）
    │     └─→ 按SKILL.md校验清单逐项检查
    │
    ▼
交付：书籍级人生指导手册（Markdown/Obsidian格式）
```

## 模块依赖关系

```
document-template.md（骨架模板）
    ├── 依赖 03-six-phase-structure.md（六篇结构）
    └── 依赖 12-document-anatomy.md（成品标准）

05-project-playbook.md（项目实战）
    ├── 依赖 04-learning-roadmap.md（学习基础）
    └── 被 06-job-hunting.md 依赖（项目写进简历）

09-writing-style.md（写作风格）
    └── 被所有内容生成环节引用（全局质量标准）

10-obsidian-output.md（输出格式）
    └── 被第8步标准化输出引用

11-iteration-protocol.md（迭代协议）
    └── 被多轮迭代场景引用

12-document-anatomy.md（文档解剖）
    ├── 依赖 03-six-phase-structure.md
    └── 被第3步搭建骨架引用
```

## 六篇内容架构

```
人生指导手册
│
├── 第一篇：决策与方向（10%-15%篇幅）
│   ├── 我是谁（身份画像、能力盘点、优劣势分析）
│   ├── 我要去哪（目标设定、赛道选择、三情景推演）
│   └── 为什么是这条路（行业取证、趋势分析、个人匹配度）
│
├── 第二篇：学习与成长（15%-20%篇幅）
│   ├── 学习路线（时间线、阶段划分、里程碑）
│   ├── 学习方法（高效学习、刻意练习、费曼技巧）
│   ├── 时间管理（每日/每周/每月计划、番茄工作法）
│   └── 心态建设（焦虑应对、挫败处理、长期主义）
│
├── 第三篇：项目与实战（25%-35%篇幅，重中之重）
│   ├── 项目1（入门级，验证学习成果）
│   ├── 项目2（进阶级，展示工程能力）
│   ├── 项目3（高级级，体现深度和创新）
│   ├── 项目4-5（可选，拓展广度）
│   └── 每个项目包含：需求分析→技术选型→实现指南→工程化→部署→简历包装
│
├── 第四篇：求职与入职（15%-20%篇幅）
│   ├── 简历优化（STAR法则、项目描述、关键词匹配）
│   ├── 面试准备（技术题库、行为面试、项目讲解）
│   ├── 薪资谈判（市场行情、谈判策略、offer对比）
│   ├── 签约避坑（合同条款、试用期、五险一金）
│   └── 入职前100天（融入团队、建立信任、快速产出）
│
├── 第五篇：站稳与发展（10%-15%篇幅）
│   ├── 晋升路径（技术专家/管理/架构师）
│   ├── 跳槽策略（时机判断、简历更新、面试节奏）
│   ├── 地区选择（一线城市/新一线/二线/远程）
│   ├── 35岁危机应对（能力护城河、副业、转型）
│   └── 10年规划（5年/10年/15年里程碑）
│
└── 第六篇：支撑与风险（10%-15%篇幅）
    ├── 身体健康（作息、运动、饮食、体检）
    ├── 心理韧性（压力管理、情绪调节、社交支持）
    ├── 理财规划（预算、储蓄、投资、保险）
    ├── 社保公积金（缴纳、转移、使用、政策）
    ├── 个人品牌（博客、开源、演讲、社群）
    ├── 人脉建设（同事、同行、导师、社群）
    ├── 英语能力（学习方法、应用场景、提升路径）
    └── 风险预案（失业、生病、行业衰退、个人危机）
```

## 扩展点

### 添加新的参考文档
1. 在 `references/` 目录添加新文档，按主题编号
2. 在 `SKILL.md` 的"参考文件导航"中更新
3. 在 `README.md` 的文件结构中更新
4. 确保不与现有文档内容重复

### 修改工作流程
1. 修改 `SKILL.md` 的"标准工作流程"章节
2. 同步更新 `API.md` 的工作流接口
3. 同步更新 `README.md` 的快速开始
4. 在 `CHANGELOG.md` 记录变更

### 创建新模板
1. 复制 `assets/document-template.md`
2. 根据需求修改结构和内容
3. 保存到 `assets/` 目录，命名清晰

## 性能考量

- **按需加载**：12个参考文档不要一次性全读，按工作流程步骤按需读取
- **模板复用**：使用document-template.md作为骨架，避免从零开始
- **迭代深化**：先完成骨架和核心内容，再通过多轮迭代深化，不要追求一次完美
- **密度控制**：每1000字至少1个可执行动作，避免空泛的宏观分析

## 兼容性

| 环境 | 支持情况 | 说明 |
|------|---------|------|
| Obsidian | ✅ 完全支持 | 双链、Frontmatter、流程图 |
| Typora | ✅ 支持 | Markdown渲染 |
| VS Code | ✅ 支持 | Markdown预览 |
| 飞书文档 | ⚠️ 部分支持 | 需手动调整格式 |
| Notion | ⚠️ 部分支持 | 需手动调整格式 |

---

**版本**：v2.0.0
**最后更新**：2026-09-13
