---
name: Process-oriented-Web-Design
description: 从零生成一个设计完整的"流程导向学习/项目看板"单文件 HTML。设计系统固化在 templates/dashboard-skeleton.html 里：深色玻璃拟态 + 三团 CSS 极光背景 + 入场动画 + SVG 玻璃风折线图 + 三态打卡 + localStorage 持久化。当用户需要：(1) 做一个学习/项目进度看板网页，要好看、有动效、能打卡、能看本周学时曲线；(2) 不要用脚手架/React/Vue，要单文件直接双击打开；(3) 内容根据用户具体项目填充（项目名、起止日期、周数、每日学时、阶段任务）；(4) 要玻璃拟态深色主题、不要白底普通仪表盘时使用。纯文档型 Skill，输出 .html 文件。
---

# 流程导向网页设计：从零生成玻璃拟态学习/项目看板

## 一、这个 Skill 做什么

输入：用户的项目信息（项目名、开始日期、截止日期、每日学时、分阶段任务）。
输出：一个**设计完整、可直接双击打开**的单文件 HTML 看板，包含：

- 深色背景 + 玻璃拟态卡片（backdrop-filter blur + 边缘高光 + 圆角 20px）
- 六套美学主题（右上角色板切换：光之展厅/紫夜回廊/琴弦夜曲/织波锦缎/幽灵纤维/酸性方格）
- 顶部栏（brand logo + 项目名 + 主题切换）
- hero 卡（标题 + 总进度条）
- 3 个统计卡（连续打卡天数 / 累计投入小时 / 任务 x/y）
- 阶段进度条（7 列，当前阶段高亮）
- SVG 玻璃风折线图（实际学时粉色发光曲线 + 计划虚线 + 2/4/6/8h 网格 + 今天光晕点）
- 周切换器（上一周/下一周翻页看历史）
- 今日任务三态打卡（完成 / 跳过 / 未做，localStorage 持久化）
- N 周全景网格（每周一个方块，点击跳周，已完成填充色）
- 落后提示条（dev-strip：计划 x 项/实际 y 项/落后 z 项，落后时才显示）
- 周视图（点"查看详情"进入：7 天任务展开 + 本周统计 + 复盘笔记自动保存）
- 底部总进度条（fixed 悬浮，显示整体进度）
- 大卡片 3D tilt（鼠标跟随倾斜）+ 小卡片微抬升
- 入场 3D 翻入（perspective 900px rotateX）
- 字体渲染优化（antialiased + grayscale + optimizeLegibility）
- 响应式 + prefers-reduced-motion 降级

> 核心理念：**设计是资产，内容是变量**。所有视觉固化在模板里，Agent 只填数据层 `{{...}}` 占位符。

## 二、六条铁律

1. **用模板**：复制 `templates/dashboard-skeleton.html`，只替换 `{{...}}` 占位符，不要重写 CSS/JS。
2. **数据层集中**：所有用户数据都在 `<script>` 开头的 `const CFG = {...}` 里，不要散落到 HTML。
3. **不改设计系统**：CSS 变量（--bg/--accent/--glass-*）、极光 animation、玻璃卡片样式一行不动。
4. **800ms 兜底**：模板已内置 `setTimeout(()=>document.querySelectorAll('.rv').forEach(e=>e.classList.add('in')),800)`，不要删。
5. **SVG 不拉伸**：模板已用 `height:auto`，不要加 `preserveAspectRatio="none"`。
6. **存储隔离**：每个用户用不同 `storageKey`（如 `ragstudy-v1`、`jobhunt-v1`），避免进度串。
7. **动态模块同步入场**：dev-strip 等运行时才显示的模块，必须加入统一入场队列（GSAP timeline 或 pendReveal），初始化时只设 `hidden=false`，不要手动 `add("in")`，否则会和其他模块不同步。
8. **性能红线**：动态模块（如 dev-strip）不要加 `backdrop-filter: blur()`，它叠在动态极光背景上会导致 GPU 卡顿；用 `var(--glass-tint)` 纯色半透明背景即可。

## 三、生成流程（五步）

### 第 1 步：收集用户需求

必须拿到：
- 项目名（如"RAG+Agent 学习"）
- 开始日期（年月日）
- 截止日期（年月日）
- 每日学时（如 8h）
- 阶段划分（几阶段，每阶段标题）
- 每周任务清单（每天学什么、对应学时）

缺任务清单时，按阶段和周数自动分配（见 references/02）。

### 第 2 步：复制模板

```powershell
Copy-Item "templates/dashboard-skeleton.html" "输出目录\项目看板.html"
```

### 第 3 步：替换占位符

模板里的 `{{...}}` 全部替换：

| 占位符 | 替换为 |
|--------|--------|
| `{{TITLE}}` | `<title>` 标签 |
| `{{PROJECT_NAME}}` | H1 大标题 |
| `{{START_STR}}` | 如 "2026·10·12" |
| `{{END_STR}}` | 如 "2027·04·30" |
| `{{WEEKS}}` | 周数整数 |
| `{{DAILY_H}}` | 每日学时整数 |
| `{{START_Y}}` `{{START_M_MINUS_1}}` `{{START_D}}` | new Date 参数（月从 0 开始） |
| `{{END_Y}}` `{{END_M_MINUS_1}}` `{{END_D}}` | 同上 |
| `{{STORAGE_KEY}}` | 如 "ragstudy-v1" |
| `{{BASE_PLAN_JSON}}` | JSON 数组，见 references/02 |

### 第 4 步：验证

```powershell
python -c "import re,io; s=io.open('输出.html',encoding='utf-8').read(); b=max(re.findall(r'<script(?![^>]*src)[^>]*>(.*?)</script>',s,re.S),key=len); io.open('_m.js','w',encoding='utf-8').write(b)"
node --check _m.js
```

浏览器打开，确认极光背景、玻璃卡片、折线图、打卡交互正常。

### 第 5 步：交付

通过 `present_files` 交付 .html 文件。

## 四、参考文档

| 文件 | 内容 |
|------|------|
| `references/01-玻璃拟态设计系统.md` | CSS 变量、极光、玻璃卡片、三态按钮规范 |
| `references/02-数据层生成规范.md` | CFG/BASE_PLAN JSON 结构、自动排周算法 |
| `references/03-SVG玻璃风图表规范.md` | 折线图参数、平滑曲线、发光滤镜 |
| `references/04-动画兜底与降级.md` | 800ms 兜底、prefers-reduced-motion |
| `references/05-字体与渲染优化.md` | font-smoothing、高分屏 |

## 五、输出规范

- 单文件 .html，UTF-8，内联 CSS/JS，无外部依赖
- 双击即可打开，不需要服务器
- 响应式：桌面 900px 居中，移动端全宽
- 深色主题，主色玫瑰粉 #e06391

### 交付前自检

- [ ] 所有 `{{...}}` 占位符已替换（grep 无残留）
- [ ] `node --check` 通过
- [ ] START/END 月参数正确（月从 0 开始）
- [ ] storageKey 唯一
- [ ] BASE_PLAN 每周 7 天，每天任务学时和 = 每日学时
- [ ] 无 API Key/密码

## 六、使用场景

### 场景一：学习计划看板
用户："我要从 10 月到明年 4 月学 RAG+Agent，每天 8h，做个看板。"
→ 收集阶段 → 复制模板 → 填 CFG → 交付。

### 场景二：项目进度看板
用户："我在做一个全栈项目，3 个月，分 4 阶段，做个进度页。"
→ 同上，任务换成项目里程碑。

### 场景三：求职冲刺看板
用户："我要 35 周内找到工作，每天 6h，做个打卡页。"
→ 同上。

## 七、边界

- 不做白底浅色主题（本 Skill 只做深色玻璃拟态）
- 不加 three.js WebGL（模板用纯 CSS 极光，性能更好）
- 不做后端/数据库（localStorage 足够）
- 不做多用户协作

---
> 版本：v2.0.0
> 模板：templates/dashboard-skeleton.html
