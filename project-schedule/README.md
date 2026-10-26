# Project-Schedule

一键生成暖色玻璃拟态风格的多阶段周计划 / 学习排期表单页 HTML。

## 特性

- 深色/浅色双主题，localStorage 记忆
- 可勾选任务清单，进度自动保存
- 右侧周导航快速跳转，今日自动高亮
- 滚动入场动画 + IntersectionObserver
- 顶部滚动进度条 + 总进度条
- 单文件、无外部依赖、双击即开

## 快速开始

```powershell
# 1. 复制模板
Copy-Item .\templates\schedule-template.html .\我的排期表.html

# 2. 打开我的排期表.html，替换 {{...}} 占位符（见 SKILL.md 第三节）

# 3. 双击浏览器打开
```

## 目录结构

```
Project-Schedule/
├── SKILL.md                  # 核心使用指南
├── README.md                 # 本文件
├── QUICKSTART.md             # 5 分钟上手
├── CHANGELOG.md              # 版本记录
├── FAQ.md                    # 常见问题
├── LICENSE                   # MIT
├── templates/
│   └── schedule-template.html # 完整 HTML 模板（带 {{占位符}}）
└── references/
    └── design-system.md       # 设计系统规范
```

## 什么时候用

- 学习路线排期表
- 项目里程碑看板
- 周计划 / 习惯打卡
- 任何需要「阶段 → 周 → 任务清单」三级结构的网页
