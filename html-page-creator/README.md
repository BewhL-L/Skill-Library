# HTML Page Creator

> 专业网页创建与设计Skill，基于玻璃拟态（Glassmorphism）设计系统，快速生成美观、响应式、带深色/浅色主题切换的单页HTML网站。

## ✨ 功能特性

- 🎨 **玻璃拟态设计** - 统一的Glassmorphism风格，backdrop-filter模糊+半透明背景+内阴影高光
- 🌓 **深色/浅色主题** - 一键切换，颜色系统自动适配，用户偏好本地存储
- 📱 **响应式布局** - 自动适配桌面（>1024px）、平板（768-1024px）、手机（<768px）
- ✨ **滚动入场动画** - IntersectionObserver驱动，支持`prefers-reduced-motion`减少动画偏好
- 📊 **滚动进度条** - 顶部实时显示阅读进度
- 🧩 **模块化组合** - 13种可复用模块（导航栏、Hero、统计卡片、功能卡片、时间线、进度条、表格、代码块、提示框、标签、按钮、表单、页脚）
- 🎯 **设计系统规范** - 统一的颜色、排版、间距、圆角、阴影、动效标准
- ⚡ **性能优化** - 单文件交付，无外部依赖，内联CSS/JS，控制backdrop-filter数量

## 📦 适用场景

- 学习路线图 / 知识总结页
- 个人作品集 / 项目展示页
- 产品介绍页 / 营销落地页
- 简历 / 个人主页
- 任何需要精美单页HTML的场景

## 🚀 快速开始

### 使用方式

本Skill为AI Agent设计，无需手动运行命令。在对话中描述需求即可：

```
"帮我创建一个关于Python学习路线的网页"
"设计一个个人作品集展示页"
"做一个产品介绍的HTML页面"
```

### 工作流程

1. **理解需求** - 明确网页主题、核心内容、页面结构
2. **复制模板** - 基于`assets/template.html`创建基础结构
3. **定制内容** - 填充用户提供的内容到各个模块
4. **模块组合** - 从模块库选择合适的模块组合
5. **设计检查** - 确保符合设计系统规范
6. **验证交付** - 浏览器验证后交付HTML文件

## 📁 文件结构

```
html-page-creator/
├── SKILL.md                    # 核心文档（使用指南、工作流程、输出规范）
├── README.md                   # 项目首页（本文件）
├── QUICKSTART.md               # 5分钟快速上手指南
├── CHANGELOG.md                # 版本变更记录
├── FAQ.md                      # 常见问题解答
├── INSTALLATION.md             # 安装与配置指南
├── USE-CASES.md                # 使用案例与最佳实践
├── CONTRIBUTING.md             # 贡献指南
├── SECURITY.md                 # 安全策略
├── CODE_OF_CONDUCT.md          # 行为准则
├── SUPPORT.md                  # 支持与帮助
├── .gitignore                  # Git忽略配置
├── .editorconfig               # 编辑器配置
├── assets/
│   └── template.html           # 基础网页模板（复制后修改）
└── references/
    ├── design-system.md        # 设计系统规范（颜色、排版、间距、动效）
    └── module-library.md       # 模块库（13种可复用模块的HTML+CSS代码）
```

## 📚 核心文档

| 文档 | 用途 |
|------|------|
| [SKILL.md](SKILL.md) | 完整使用指南、工作流程、输出规范、质量检查清单 |
| [QUICKSTART.md](QUICKSTART.md) | 5分钟快速上手，从零创建第一个网页 |
| [design-system.md](references/design-system.md) | 设计系统规范：颜色、排版、间距、圆角、阴影、动效 |
| [module-library.md](references/module-library.md) | 13种可复用模块的完整HTML+CSS代码 |
| [FAQ.md](FAQ.md) | 常见问题解答 |
| [CHANGELOG.md](CHANGELOG.md) | 版本变更记录 |

## 🎨 设计系统预览

### 主色调
- 主色（橙色）：`#ff9a2e`（深色）/ `#c46a10`（浅色）
- 次色（青色）：`#4fc4b4` / `#2a9d8f`
- 第三色（紫色）：`#9b8cf0` / `#6c5ce7`
- 第四色（粉色）：`#e879a0` / `#d63384`

### 玻璃效果
```css
background: var(--bg-glass);           /* 半透明背景 */
backdrop-filter: blur(24px) saturate(160%);  /* 模糊+饱和度 */
border: 1px solid var(--line);         /* 细边框 */
box-shadow: var(--shadow-md), var(--shadow-inset);  /* 外阴影+内高光 */
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 贡献方式
1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

**版本**：v1.0.0
**最后更新**：2026-09-13
**类型**：纯文档型 Skill（doc-only）
