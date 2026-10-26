# Project Scaffolder — 项目全周期生成器

> 你说"我想做一个 XX 项目"，本 Skill 自动完成：需求分析 → 资源选型 → 生成全部产物 → 人机分工 → 指导文档 → 多轮自检。
>
> **不限代码项目**：软件、学习、内容、商业、研究、活动、个人生活，以及混合型项目都能处理。

---

## ✨ 核心能力

### 1. 七步工作流程

| 步骤 | 内容 | 产出 |
|------|------|------|
| 第一步 | 项目识别与需求分析 | 项目定位、类型标注、成功标准、约束风险 |
| 第二步 | 产物规划与资源选型 | WBS、功能完整性矩阵、目录结构、依赖关系 |
| 第三步 | 产物生成（AI 直接完成） | 全部 A 类产物（代码/文档/计划/模板/清单） |
| 第四步 | 人机分工判断 | A/B/C 分工表、B 类填空指引、C 类验证方法 |
| 第五步 | 生成《项目全景总结与行动指南》 | 三篇递进教程，每章七要素，含梯度验证任务 |
| 第六步 | 多轮自检与交付 | 12 维度自检报告（含工程底座），可用 `check_baseline.py` 跑其中 7 项 |
| 第七步 | Git 初始化与交付 | .gitignore、Git 提交、README、交付清单 |

### 2. 功能完整性矩阵（v2.0 新增）

生成项目时自动对照 7 大项目类型的"标配功能清单"，确保 P0（核心）和 P1（周边标配）功能首次交付就完整，不再出现"只做核心功能、遗漏收藏/搜索/通知"的问题。

- 社交类：自动包含收藏、搜索、通知、评论点赞、个人主页、关注体系
- 电商类：自动包含搜索筛选、订单列表、收货地址、评价
- 工具类：自动包含数据管理、搜索筛选、分类标签、导出分享
- 学习类：自动包含练习题、进度跟踪、复习计划、测评
- 商业类：自动包含市场分析、财务模型、营销方案、SOP
- 活动类：自动包含预算、物料清单、人员分工、应急预案
- 个人生活类：自动包含预算、清单、时间表、记录模板

### 3. 12 维度自检体系（含工程底座）

| 维度 | 检查内容 |
|------|----------|
| 1-5 | 产物/文档/分工/通用性/可执行性（基础维度） |
| 6 | 前后端契约检查（含功能完整性反向检查） |
| 7 | 依赖完整性检查 |
| 8 | 静态资源检查 |
| 9 | 框架语法检查（14 个框架） |
| 10 | 运行时验证（含文档与代码一致性） |
| 11 | 内容完整性检查（v2.0 新增） |

### 4. 人机分工 A/B/C 模型

- **A 类（AI 直接完成）**：信息整合、模板化、标准化工作
- **B 类（AI 生成框架 + 用户填充）**：需要个人信息或最终确认
- **C 类（必须用户自己完成）**：物理行动、真实社交、资金法律操作、个人体验

### 5. 七要素指导文档

每章必须包含：概念解释 → 原理说明 → 操作指引 → 🤝分工 → 💡深度讲解 → 📝精简总结 → 🎯梯度验证任务。

---

## 📦 安装

本 Skill 为纯文档型，无需安装依赖。将 `project-scaffolder/` 目录放入 Skill 根目录即可：

```
.skills/ 或 .user_skills/
└── project-scaffolder/
    ├── SKILL.md
    ├── README.md
    └── references/
        ├── project-types.md
        ├── division-rules.md
        ├── doc-template.md
        ├── verification-patterns.md
        └── content-completeness.md
```

---

## 🚀 快速开始

### 触发方式

直接对 AI 说以下任意一句话即可触发：

- "我想做一个 XX 项目"
- "帮我规划/搭建一个 XX"
- "从零开始做 XX"
- "帮我生成 XX"
- "我要完成 XX，帮我"

### 使用示例

```
用户：我想做一个宠物爱好者社交平台，爱好者注册账号，互相交流关注，发布宠物日常照片，最终做出小程序或可上线的app。

AI：[自动执行七步流程]
  1. 识别为"软件/技术 + 社交"混合型项目
  2. 规划 WBS + 功能完整性矩阵（对照社交类标配清单）
  3. 生成后端（FastAPI）+ 前端（微信小程序）全部代码
  4. 输出人机分工表（AI 已完成 vs 你需要做）
  5. 生成《项目全景总结与行动指南》（三篇递进教程）
  6. 12 维度自检（含工程底座），修复问题
  7. Git 初始化，交付
```

---

## 📚 文档导航

| 文档 | 用途 |
|------|------|
| [SKILL.md](SKILL.md) | 核心文档：七步工作流程、生成质量约束、12 维自检 |
| [QUICKSTART.md](QUICKSTART.md) | 5 分钟快速上手 |
| [references/project-types.md](references/project-types.md) | 7 大项目类型详解 |
| [references/division-rules.md](references/division-rules.md) | 人机分工 A/B/C 标准 |
| [references/doc-template.md](references/doc-template.md) | 指导文档模板 |
| [references/verification-patterns.md](references/verification-patterns.md) | 验证任务与面试题模式 |
| [references/content-completeness.md](references/content-completeness.md) | 功能完整性检查清单 |
| [references/ci-snippets.md](references/ci-snippets.md) | CI 片段库：Python/Node/镜像/私有文件守卫 |
| [references/engineering-baseline.md](references/engineering-baseline.md) | 工程底座六件套与反模式 |
| [FAQ.md](FAQ.md) | 常见问题 |
| [CHANGELOG.md](CHANGELOG.md) | 版本变更记录 |

---

## 📁 目录结构

```
project-scaffolder/
├── SKILL.md                    # 核心文档（七步流程 + 11维自检）
├── README.md                   # 本文件
├── QUICKSTART.md               # 快速上手
├── CHANGELOG.md                # 版本记录
├── FAQ.md                      # 常见问题
├── CONTRIBUTING.md             # 贡献指南
├── SECURITY.md                 # 安全策略
├── CODE_OF_CONDUCT.md          # 行为准则
├── INSTALLATION.md             # 安装指南
├── USE-CASES.md                # 使用案例
├── SUPPORT.md                  # 支持指南
├── .gitignore                  # Git 忽略
├── .editorconfig               # 编辑器配置
└── references/                 # 参考文档（按需加载）
    ├── project-types.md        # 7 大项目类型详解
    ├── division-rules.md       # 人机分工标准
    ├── doc-template.md         # 指导文档模板
    ├── verification-patterns.md # 验证任务模式
    └── content-completeness.md # 功能完整性清单
```

---

## 🤝 贡献

欢迎提交 Issue 和改进建议。本 Skill 基于实战经验持续迭代，每次优化都来自真实项目的反馈。

---

## 📄 许可证

MIT License
