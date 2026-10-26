# 开发者技术英语训练手册（计划 · 材料 · 词汇句型 · 模板）

> 供 english-for-developers 制定训练计划与带练时参考。核心思想：在真实开发材料里、按场景学，每天 30 分钟长期持续，用真实任务做验收。

---

## 一、每日 30 分钟训练表（按阶段配比）

| 阶段 | 精读 | 泛读/听 | 词汇句型 | 写作/口语输出 | 重点 |
|------|------|--------|---------|--------------|------|
| E1（0–1 月） | 12' 报错/Getting Started | 8' 配字幕视频 | 7' 报错高频词 | 3' 写 1 条 Commit | 敢读、建立套路 |
| E2（1–3 月） | 12' 官方文档/SO | 8' 技术视频 | 5' 文档句型 | 5' 写 Issue 草稿 | 阅读流畅、会检索 |
| E3（3–6 月） | 10' 源码注释/Changelog | 8' 关字幕听 | 4' 协作句型 | 8' 写 PR/回答 + 站会口述 | 写作流畅、能开口 |
| E4（6–12 月） | 8' RFC/长文并总结 | 10' 无字幕 1.25x | 3' 查漏 | 9' 博客/会议/面试模拟 | 协作与面试流畅 |

> 时间是参考，可按个人调整，但**输出（写/说）占比要随阶段上升**——只输入永远不会写和说。宁可每天稳定 30 分钟，不要周末突击 5 小时后停一周。

### 每周节奏建议
- 周一到周五：按上表日练
- 周六：一次 45–60 分钟综合实战（读一篇 + 写一篇 Issue/PR 或一次模拟对话）
- 周日：复盘 + 把本周词汇句型用 `knowledge-review-spaced` 过一遍

---

## 二、"读"的训练法

### 2.1 报错堆栈四步阅读法
1. **看错误类型**：最底部/异常类名（如 `NullPointerException`、`TypeError`、`ECONNREFUSED`），它直接点名问题类别
2. **抓关键信息词**：`Caused by`（根因链）、`expected ... but found ...`、`cannot find / undefined / not defined`、`timeout`、`permission denied`
3. **定位位置**：`at xxx (File:line)` 找到**你自己代码**的第一帧（框架内部帧先跳过）
4. **先猜后查**：用异常名+关键词猜大意，再用英文检索验证，而不是整段丢翻译

**高频报错信号词速查**：
| 英文 | 含义 | 常见根因方向 |
|------|------|-------------|
| null / undefined / NoneType | 空值 | 用了未初始化/不存在的值 |
| cannot find / not found / unresolved | 找不到 | 依赖缺失、路径/导入错误、拼写 |
| permission denied / forbidden / unauthorized | 权限 | 文件权限、认证、越权 |
| timeout / timed out | 超时 | 网络、连接池、慢查询、死锁 |
| refused / reset / ECONNRESET | 连接被拒/重置 | 服务没起、端口、防火墙 |
| conflict / duplicate / already exists | 冲突/重复 | 唯一约束、并发、重复提交 |
| expected / mismatched / invalid | 不符合预期 | 类型、格式、参数校验 |
| out of memory / stack overflow | 内存/栈溢出 | 泄漏、死递归、数据量过大 |
| deprecated | 已废弃 | 版本升级，API 被移除/替换 |

### 2.2 文档精读三遍法
- **第一遍（不查词）**：抓结构和主干，这段在讲"是什么/怎么用/注意什么"
- **第二遍（查高频词）**：只查反复出现、影响理解的词，专业术语顺手记技术笔记
- **第三遍（复述）**：合起文档，用自己的话（中文也行）复述操作步骤或原理
- 进阶：边读边在知识库做"官方文档 → 我的理解"对照笔记

### 2.3 阅读材料从易到难
1. 入门：报错信息、库的 Getting Started / Quickstart、MDN/菜鸟对照
2. 中级：官方文档 Core Concepts、Stack Overflow 高票回答、GitHub Issue
3. 进阶：源码注释与 README、Changelog / Migration Guide、RFC / 设计文档、英文技术博客
4. 高阶：英文论文（转 `paper-reader`）、规范标准（RFC/W3C/JEP/PEP）

---

## 三、"检"的训练法：英文检索与提问

### 3.1 把中文问题转成英文检索式
- 公式：`框架/语言 + 确切错误名/关键信息 + 场景或版本`，去掉"为什么/怎么办/我的"这类口语
- 例：中文"Spring Boot 启动报连接数据库失败" → `spring boot datasource "Failed to configure a DataSource" url attribute`
- 技巧：
  - 用**双引号**锁完整报错：`"ECONNREFUSED 127.0.0.1:6379"`
  - 限定站点：`site:stackoverflow.com`、`site:github.com`
  - 带版本：`react 18 useEffect strict mode twice`
  - 先搜英文错误原文，命中率远高于中文翻译版

### 3.2 结果优先级
官方文档/官方 Issue > Stack Overflow 高票且被采纳答案 > 维护者博客 > 普通博客/论坛。注意答案时间与版本是否匹配。

### 3.3 英文追问/提问骨架
```
标题：[工具/版本] 一句话问题（用名词短语，少用完整句子）
Environment: OS / language version / framework version
Steps to reproduce: 1.. 2.. 3..
Expected behavior:
Actual behavior:（贴完整报错）
What I've tried: …（已尝试，避免让对方重复）
```

---

## 四、"写"的模板库（可直接填空）

### 4.1 Commit Message（Conventional Commits）
```
<type>(<scope>): <subject 祈使句、小写开头、不加句号>

type = feat | fix | docs | style | refactor | perf | test | chore | build | ci
```
例：`fix(order): prevent duplicate submit when user clicks twice`
常用动词：add / fix / remove / update / refactor / extract / rename / bump / handle / validate。

### 4.2 Bug Issue
```
**Bug**: <short symptom>
**Environment**: <os, runtime and framework versions>
**Steps to reproduce**
1. ...
**Expected**: ...
**Actual**: ... (error log below)
**Workaround tried**: ...
```

### 4.3 Pull Request 描述
```
## What
- what this PR changes (bullet)
## Why
- problem / linked issue: #123
## How to test
- steps / commands to verify
## Risk / Notes
- breaking change? migration? screenshots?
```

### 4.4 常用写作句型
- 说明问题：`This causes ... when ...` / `It fails with ... because ...`
- 给方案：`I suggest ... so that ...` / `An alternative would be ...`
- 求确认：`Could you confirm whether ...?` / `Please let me know if ...`
- 礼貌追问：`Any update on this? Happy to provide more details.`
- 回复评审：`Good point, fixed in ...` / `I've updated ... to address this.`

> 用 AI 改写时，要求"保留我的技术含义、改成地道简洁的技术英文、并解释改了哪几处"，对照学习而非直接粘贴。

---

## 五、"说听"的训练法

### 5.1 Daily Standup 三句话（最先练）
```
Yesterday I worked on ... and finished ...
Today I plan to ... / I'll focus on ...
I'm blocked on ... (or: No blockers.)
```

### 5.2 会议高频句型
- 没听清：`Sorry, could you repeat that?` / `Do you mean ...?`
- 确认理解：`Just to make sure, we're going to ..., right?`
- 表达意见：`I think ... because ...` / `I see your point, but ...`
- 求助/接话：`I can take this.` / `Let me follow up offline and get back to you.`
- 总结：`To summarize, action items are ...`

### 5.3 听力进阶
配英文字幕（不看中文字幕）→ 关字幕 → 1.25 倍速；精听一段 1–2 分钟反复到能复述，泛听保语感。技术大会演讲、官方发布视频、技术 Podcast 都是材料。

### 5.4 英文技术面试
把 `interview-prep-coach` 的 STAR 项目、自我介绍、技术概念转成英文，固定可复用句式：
- 开场：`I'm a ... engineer with experience in ...`
- 项目：`In this project, I was responsible for ...; I built ... which improved ... by ...`
- 不会时：`I haven't used it in production, but I understand the core idea is ...`

---

## 六、AI 陪练 Prompt（与 ai-assisted-coding 配合）

- 精读对照：`把这段英文文档逐句翻译并讲解关键语法和技术词，最后用简单英文复述：【贴文本】`
- 报错讲解：`解释这个英文报错每部分的含义，教我怎么用英文关键词去搜：【贴报错】`
- 写作改写：`把下面这段中式技术英文改成地道简洁的表达，逐条说明改动原因：【文本】`
- 模拟站会：`你是我海外团队的 tech lead，我们用英文开 standup，你先问我 yesterday/today/blocker，再纠正我的表达`
- 模拟面试：`用英文对我做一场 15 分钟后端技术面试，逐题进行，我答完给语法和内容反馈`
- 词汇卡：`基于这段材料，挑出 10 个开发者最高频的词/短语，给英文释义+技术例句，不要生僻词`

---

## 七、阶段验收清单（真实任务，不看感觉）

| 阶段 | 验收任务（能独立完成即达标） |
|------|------------------------------|
| E1 | 不靠整段翻译，说出任意报错的类型与大致方向；写出规范 Commit Message |
| E2 | 裸读一篇官方 Getting Started 并复述步骤；用英文检索式独立搜到一个报错的解；写出结构完整的 Bug Issue 草稿 |
| E3 | 读懂 Changelog/Migration 并判断对项目影响；独立写一篇 PR 描述；用英文做 1 分钟站会汇报 |
| E4 | 读完一篇英文技术文章/RFC 并写英文总结；参与一次英文 Issue 讨论；完成一轮模拟英文技术面试并自评达标 |

---

## 八、沉淀进知识库

- **词汇笔记**：按"报错 / 文档 / commit / PR / issue / 会议"六个场景建 MOC，词带例句与出处，不做孤立单词表
- **报错对照本**：`英文报错关键词 → 根因 → 解决方案 → 知识库双链`，与 `bug-troubleshooter` 踩坑笔记互通
- **模板库**：Commit/Issue/PR/Standup 模板存为可复用笔记
- 全部用 `knowledge-review-spaced` 间隔复习；技术内容本身用 `tech-concept-deep-dive` 深化，英语只是承载它的工具
