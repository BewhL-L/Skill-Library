# 设计系统 · 暖色玻璃拟态

本文档固化「学习排期表」的全部视觉规范。改样式只准改 CSS 变量，不要在组件里硬编码颜色。

## 1. 色板

### 深色主题（默认）
| 变量 | 值 | 用途 |
|------|-----|------|
| `--accent` | `#ff9a2e` | 橙：主强调、今日周、本周标签 |
| `--accent-2` | `#4fc4b4` | 青：统计卡第 2 格数字 |
| `--accent-3` | `#9b8cf0` | 紫：badge 渐变、进度条中段 |
| `--accent-4` | `#e879a0` | 粉：进度条尾段、标题渐变 |
| `--bg` | `#0f0c09` | 页面底（暖黑，不是冷黑） |
| `--bg-2` | `#1a1510` | 次级底 |
| `--glass` | `rgba(32,26,20,.28)` | 卡片底 |
| `--glass-soft` | `rgba(32,26,20,.16)` | 内嵌周卡底 |
| `--glass-deep` | `rgba(32,26,20,.42)` | 验收条底 |
| `--text` | `#f6efe3` | 主文字（暖白） |
| `--text-2` | `#b8a88c` | 次文字（米褐） |
| `--line` | `rgba(246,239,227,.10)` | 边框 |

### 浅色主题（`[data-theme="light"]`）
- `--bg:#faf6f0`（米白），`--bg-2:#f0e8dc`
- glass 换成白色半透明 `rgba(255,255,255,.48/.30/.62)`
- 文字 `#2a2218` / `#6b5d4a`
- 阴影偏暖色 `rgba(80,50,20,...)`

### 状态色
- `--good:#4ade80` 绿
- `--warn:#fbbf24` 黄
- `--bad:#f87171` 红（重置按钮）
- `--today:rgba(251,191,36,.14)` 今日周卡背景

## 2. 字号阶梯（全站 7 档，不准新增）

| 变量 | 值 | 用途 |
|------|-----|------|
| `--fs-display` | `clamp(26px,3.2vw,34px)` | Hero 大标题 |
| `--fs-title` | 17px | 阶段名 h2 |
| `--fs-subtitle` | 15px | 周标题 h4 |
| `--fs-body` | 14px | 任务项正文 |
| `--fs-sm` | 13px | 按钮/阶段目标/验收 |
| `--fs-xs` | 12px | 日期/标签/计数 |
| `--fs-metric` | 28px | 统计数字 |

行高：`--lh-body:1.65`、`--lh-title:1.4`、`--lh-tight:1.2`。

## 3. 间距阶梯（4 的倍数）

`--sp-1:4 / --sp-2:8 / --sp-3:12 / --sp-4:16 / --sp-5:20 / --sp-6:24 / --sp-8:32 / --sp-10:40`

## 4. 圆角 / 阴影

- 圆角：`sm:8 / md:12 / lg:16 / xl:20 / pill:999`
- 阴影：`sm:0 2px 12px rgba(0,0,0,.18)`、`md:0 8px 32px .25`、`lg:0 20px 60px .35`
- 顶部内高光：`--inset: inset 0 1px 0 rgba(255,255,255,.08)`
- 动效：`--ease:cubic-bezier(.22,1,.36,1)`，`--dur:.28s`
- 玻璃模糊：`--blur:24px`，配合 `saturate(180%)`

## 5. 布局常量

- 内容最大宽：`1160px`（`.wrap`）
- 右侧导航占位：`--rail-w:52px`（≥1101px 才显示，wrap 自动让出 padding-right）
- 按钮统一高：`--control-h:34px`

## 6. 动效清单

| 元素 | 效果 |
|------|------|
| `.reveal` | 入场 `opacity 0→1, translateY(24px→0)`，.7s |
| `.week.reveal` | 位移更短（16px），.55s |
| `.week li` | 逐条错峰 40ms 渐入（1–14 条） |
| `.deliver` | 延迟 .4s 后渐入 |
| `.stage.open .stage-body` | `fadeInDown .5s` |
| `.stage .arrow` | 折叠时 `rotate(90deg)` |
| `.stat:hover` | `translateY(-3px)` + 阴影加深 |
| `.chip:hover` | `translateY(-2px)` + 边框变橙 |
| `.weeknav-item.current` | 橙底白字加粗 |
| `body::after` | 全局 `backdrop-filter:blur(6px)` 覆层 |

`prefers-reduced-motion: reduce` 时全部动画关闭。

## 7. 响应式断点

- `≤768px`：统计卡变 2 列，左右 padding 收紧
- `≤520px`：统计数字降到 24px，阶段标题降为 body 字号
- `≤1100px`：右侧周导航隐藏

## 8. 不要做的事

- ❌ 不要用冷黑/冷灰背景（这是暖色主题）
- ❌ 不要在组件里硬编码 `#fff` / `#000`，走变量
- ❌ 不要加新的动画曲线，统一 `--ease`
- ❌ 不要在 `.week li` 里加超过 14 条子项的错峰 delay（模板只写了 14 档，更多就统一 0.52s）
- ❌ 不要删 `body::after` 的模糊层，否则玻璃卡片会透出背景图
