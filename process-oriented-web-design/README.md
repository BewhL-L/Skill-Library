# Process-oriented Web Design

把"已有的精美 HTML 看板"改造成"数据驱动的学习/项目进度看板"，完整保留 three.js WebGL 背景、GSAP 动画、玻璃拟态和所有交互，只替换数据层。

## 什么时候用

- 你有一个好看的 HTML 单页，但数据是别人的（旧排期/旧项目）
- 要换成自己的周数/截止日/每日任务
- 不要另起炉灶写简化版（会丢 3D 效果）
- 要把柱状图改成玻璃风 SVG 折线图

## 核心原则

1. 复制原文件再改，不碰 CSS/动画/交互
2. 只替换 START/END/PHASES/BASE_PLAN/todayPos 和 renderRhythm
3. 不加 CSS `!important` 兜底，用 JS setTimeout 智能兜底
4. SVG 不拉伸，保持比例居中
5. 换 localStorage key 隔离旧进度

## 快速开始

```bash
# 1. grep 原文件关键位置
Grep -n "const START|const PHASES|<h1>" 原文件.html

# 2. 复制副本
Copy-Item 原文件.html 新文件.html

# 3. 按 references/02 替换数据
# 4. 按 references/03 替换 renderRhythm
# 5. 按 references/04 加智能兜底
```

## 文档

- [SKILL.md](SKILL.md) — 完整工作流
- [references/](references/) — 5 份详细规范
- [templates/](templates/) — 最小骨架

## License

MIT
