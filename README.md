# Skill Library

一套面向**工程化学习、项目交付与前端实现**的 Skill 合集，共 **34 个**，按 `SKILL.md` 规范组织，可直接用于支持该规范的 AI 客户端（Claude Code / WorkBuddy 等）。

- 每个 Skill 是一个独立目录，`SKILL.md` 为必需入口，`references/`、`scripts/`、`tests/` 按需提供。
- 体系结构、依赖方向与调用优先级见 **[Skill 依赖关系图谱](Skill依赖关系图谱.md)**。
- 全部内容为纯文本 + 少量纯标准库脚本，无外部依赖、无网络请求。

---

## 目录

| 分组 | 数量 | 说明 |
|---|---|---|
| [学习闭环](#一学习闭环19) | 19 | L0 职业统筹 → L6 求职输出 |
| [横向赋能](#二横向赋能2) | 2 | 贯穿全层的放大器 |
| [设计交付](#三设计交付5) | 5 | 把内容做成可交付的页面 |
| [前端底座](#四前端底座5) | 5 | 页面里的动画与组件实现 |
| [工程化元工具](#五工程化元工具3) | 3 | 生成与维护项目、维护 Skill 自身 |

---

## 一、学习闭环（19）

### L0 职业统筹

| Skill | 一句话 | 典型触发 |
|---|---|---|
| `career-life-guidance` | 人生/职业路线总纲：赛道选择、六篇时间线、风险控制 | "我该不该转行""未来三年怎么走" |

### L1 知识库基础

| Skill | 一句话 | 典型触发 |
|---|---|---|
| `obsidian-knowledge-base-creator` | 知识库结构标准化、笔记生成与校验；代码类知识点"底层逻辑四步" | "整理我的笔记""建一个知识库" |
| `note-quality-evaluator` | 笔记质量评估与改进建议 | "这篇笔记写得怎么样" |
| `multi-kb-sync` | 多知识库的标签/模板/样式同步 | "两个库的模板不一致" |

### L2 学习规划

| Skill | 一句话 | 典型触发 |
|---|---|---|
| `learning-path-planner` | 分阶段学习路线、知识点优先级、项目建议 | "三个月学会后端" |
| `algorithm-practice-trainer` | 算法题生成、复杂度分析、题解 | "练动态规划" |

### L3 内容深度

| Skill | 一句话 | 典型触发 |
|---|---|---|
| `tech-concept-deep-dive` | 技术概念三位一体拆解（作用 / 原理 / 用法） | "讲透 TCP 三次握手" |
| `source-code-reader` | 源码阅读路线、核心流程、设计模式定位 | "读懂这个框架的启动流程" |
| `system-design-planner` | 系统设计八步法、容量估算、架构方案 | "设计一个短链系统" |
| `paper-reader` | 论文精读八步法、AI 方向论文分类 | "帮我读这篇论文" |
| `bug-troubleshooter` | 排查五步法、根因分析、六域速查 | "这个报错怎么查" |

### L4 实践与质量

| Skill | 一句话 | 典型触发 |
|---|---|---|
| `project-based-learning` | 项目方案、分步实现、验收标准 | "用项目练手" |
| `code-practice-generator` | 可运行代码练习、梯度题目与答案 | "给我出几道练习题" |
| `code-review-refactor` | 五维评审、坏味道识别、测试保护下重构 | "审一下这段代码" |
| `devops-deployment-guide` | Docker/K8s、CI/CD、监控告警 | "怎么部署上线" |

### L5 复习巩固

| Skill | 一句话 | 典型触发 |
|---|---|---|
| `knowledge-review-spaced` | SM-2 间隔重复、今日清单、统计 | "今天该复习什么" |
| `cheatsheet-generator` | 5 类速查表、打印排版、高频考点 | "做一份速查表" |

### L6 求职输出

| Skill | 一句话 | 典型触发 |
|---|---|---|
| `interview-prep-coach` | 5 种题型框架、模拟面试、追问链 | "准备面试" |
| `tech-article-writer` | 6 种文章类型、平台适配、SEO | "把这段经历写成文章" |

---

## 二、横向赋能（2）

| Skill | 一句话 | 典型触发 |
|---|---|---|
| `ai-assisted-coding` | AI 辅助学/写/调/重构的工作流、Prompt 库、五条红线 | "怎么让 AI 帮我写代码又不失控" |
| `english-for-developers` | 读文档报错、英文检索、写 commit/PR、英文面试 | "英文文档看不懂" |

---

## 三、设计交付（5）

| Skill | 一句话 | 典型触发 |
|---|---|---|
| `design-taste-frontend` | 反"AI 味"的前端审美规范：字体、留白、动效节奏 | "这个页面为什么看起来廉价" |
| `process-oriented-web-design` | 流程导向的玻璃拟态学习/项目看板 | "做一个流程看板页" |
| `html-page-creator` | 通用单页 HTML 生成，自包含、可离线打开 | "把这份内容做成一页网页" |
| `frontend-audit-loop` | 网页改造的多轮自检收敛（改—看—再改） | "页面按设计稿改到位" |
| `project-schedule` | 排期表/周计划看板：可勾选、进度持久化、深浅色切换 | "做一张学习排期表" |

---

## 四、前端底座（5）

| Skill | 一句话 | 典型触发 |
|---|---|---|
| `gsap-core` | GSAP 核心 API 与时间线模型 | "写一段入场动画" |
| `gsap-scrolltrigger` | 滚动驱动动画与滚动叙事 | "滚动到某处再触发" |
| `gsap-plugins` | 插件体系（Flip / Draggable 等） | "做列表重排动画" |
| `gsap-performance` | 动画性能与掉帧排查 | "动画卡顿" |
| `react-bits` | React 交互动效组件实现 | "React 里做这个交互" |

---

## 五、工程化元工具（3）

| Skill | 一句话 | 典型触发 |
|---|---|---|
| `project-scaffolder` | 从需求到产物：WBS、生成、人机分工、12 维自检、工程底座 | "我想做一个 XX 项目" |
| `project-processization` | 把 AI 搭好的项目转成学习指南 + 公开 README；文档防漂移 | "给这个项目补一份学习路线" |
| `skill-optimizer` | Skill 健康检查、自动优化、文档/测试生成 | "优化我的 skill" |

> 这三个是仓库里**唯一带可执行脚本与测试**的部分：
> `project-processization`（`check_docs.py`，7 个测试文件）、`project-scaffolder`（`check_baseline.py` + 单测）、`skill-optimizer`（6 个脚本 + 8 个测试）。

---

## 安装

**用户级**（对所有项目生效）：

```bash
git clone https://github.com/BewhL-L/Skill-Library.git
cp -r Skill-Library/* ~/.claude/skills/          # Claude Code
# 或 WorkBuddy：~/.workbuddy/skills/
```

**项目级**（只对当前仓库生效）：

```bash
mkdir -p .workbuddy/skills && cp -r Skill-Library/project-scaffolder .workbuddy/skills/
```

> 客户端对 Skill 的加载方式不同：有的按需读取 `references/`，有的只加载 `SKILL.md`。
> 本仓库的 `SKILL.md` 都写成"可独立执行"的形式，`references/` 是深入材料，不读也能用。

## 自检脚本

三个脚本都是纯标准库、跨平台、无网络请求：

```bash
# 文档与代码一致性（测试数 / 路径 / 废弃表述 / 私有文件）
python project-processization/scripts/check_docs.py --root <你的项目>

# 工程底座七项自检（迁移 / 索引 / CI / 文档 / 私有边界 / 默认安全 / 假完备）
python project-scaffolder/scripts/check_baseline.py --root <你的项目>

# Markdown 结构校验（H1 唯一、围栏闭合、层级不跳）
python project-processization/scripts/validate_md.py --path README.md
```

## 设计原则

1. **可执行优先**：能写成命令的就不写成形容词；每份 `SKILL.md` 都给触发条件、步骤与验收。
2. **不重复造轮子**：跨 Skill 只做"引用"不做"复制"，唯一例外是必须随项目分发的脚本（并注明来源）。
3. **如实标注边界**：能力状态分"已接线 / 旁路可用 / 未生效"，不把没做的事写成做了。

## 许可

未指定开源许可证。如需在他人项目中复用，请先联系作者。
