# 架构

本 Skill 是纯文档型，无代码。结构：

```
Process-oriented-Web-Design/
├── SKILL.md              # 核心工作流（五轮）
├── README.md             # 项目首页
├── QUICKSTART.md         # 5 分钟上手
├── FAQ.md                # 常见问题
├── CHANGELOG.md          # 版本记录
├── INSTALLATION.md       # 安装（纯文档型无需安装）
├── CONTRIBUTING.md       # 贡献
├── SECURITY.md           # 安全
├── LICENSE               # MIT
├── examples/
│   └── use-cases.md      # 三个真实示例
├── templates/
│   └── dashboard-skeleton.html  # 最小骨架
└── references/
    ├── 01-玻璃拟态设计系统.md
    ├── 02-数据驱动替换清单.md
    ├── 03-SVG玻璃风图表规范.md
    ├── 04-动画兜底与CDN容错.md
    └── 05-字体与渲染优化.md
```

设计理念：视觉是资产，数据是内容。原文件 CSS/JS/动画不动，只替换数据层和图表函数。
