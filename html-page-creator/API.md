# API 参考

> 本文档描述 html-page-creator Skill 的接口规范。由于本Skill为纯文档型（doc-only），不包含可执行代码，本文档描述的是Skill的概念性接口和资源引用方式。

## 概述

html-page-creator 是一个纯文档型 Skill，通过提供标准化的模板、设计系统规范和模块库，帮助 AI Agent 快速创建高质量单页HTML网站。

## 资源接口

### 模板资源

| 资源 | 路径 | 用途 |
|------|------|------|
| 基础网页模板 | `assets/template.html` | 复制后修改，创建新网页的起点 |

### 参考文档接口

| 文档 | 路径 | 用途 | 读取时机 |
|------|------|------|---------|
| 设计系统规范 | `references/design-system.md` | 颜色、排版、间距、圆角、阴影、动效标准 | 需要调整设计风格、查询变量值时 |
| 模块库 | `references/module-library.md` | 13种可复用模块的完整HTML+CSS代码 | 需要添加特定模块、组合页面结构时 |

## 模板接口规范

### template.html 结构

```
template.html
├── <head>
│   ├── <meta charset>          # UTF-8编码
│   ├── <meta viewport>         # 响应式视口
│   ├── <title>                 # 页面标题（需替换）
│   ├── <meta description>      # 页面描述（需替换）
│   └── <style>                 # 内联CSS（含CSS变量、主题系统、组件样式）
├── <body>
│   ├── .scroll-progress        # 滚动进度条
│   ├── .nav                    # 导航栏（含主题切换按钮）
│   ├── .hero                   # Hero区域（标题+副标题+统计卡片）
│   ├── .section#section1       # 示例章节1（卡片网格）
│   ├── .section#section2       # 示例章节2（卡片网格）
│   └── .footer                 # 页脚
└── <script>                    # 内联JS（主题切换、滚动进度、入场动画）
```

### CSS变量接口

模板定义了以下CSS变量，创建网页时应使用变量而非硬编码值：

```css
:root {
  /* 颜色系统 */
  --bg: #100d0a;                    /* 页面背景 */
  --bg-secondary: #1a1510;          /* 次级背景 */
  --bg-glass: rgba(30,24,18,.62);  /* 玻璃卡片背景 */
  --text: #f6efe3;                   /* 主文字 */
  --text-secondary: #a89880;        /* 次级文字 */
  --line: rgba(246,239,227,.1);    /* 边框线 */
  --accent: #ff9a2e;                 /* 主强调色（橙色） */
  --accent-secondary: #4fc4b4;       /* 次强调色（青色） */
  --accent-third: #9b8cf0;           /* 第三强调色（紫色） */
  --accent-fourth: #e879a0;          /* 第四强调色（粉色） */

  /* 效果系统 */
  --glass: blur(24px) saturate(160%);  /* 玻璃模糊效果 */
  --shadow-sm: 0 2px 8px rgba(0,0,0,.2);
  --shadow-md: 0 8px 24px rgba(0,0,0,.3);
  --shadow-lg: 0 16px 48px rgba(0,0,0,.4);
  --shadow-inset: inset 0 1px 0 rgba(255,255,255,.06);

  /* 尺寸系统 */
  --radius-sm: 8px;
  --radius-md: 14px;
  --radius-lg: 20px;

  /* 动效系统 */
  --ease: cubic-bezier(.16,1,.3,1);
}
```

### JavaScript接口

模板包含以下JavaScript功能：

| 功能 | 触发方式 | 说明 |
|------|---------|------|
| 主题切换 | 点击`.theme-toggle`按钮 | 切换深色/浅色主题，保存到localStorage |
| 滚动进度 | window.scroll事件 | 更新`.scroll-progress`宽度 |
| 入场动画 | IntersectionObserver | 元素进入视口时添加`.visible`类 |
| 导航栏阴影 | window.scroll事件 | 滚动>50px时添加阴影 |

## 模块接口

模块库（`references/module-library.md`）提供13种可复用模块，每个模块包含：

- **HTML结构** - 可直接复制的标记
- **CSS样式** - 配套的样式定义
- **使用说明** - 适用场景和定制建议

模块列表：
1. 导航栏模块
2. Hero区域模块
3. 统计卡片模块
4. 功能卡片网格模块
5. 时间线模块
6. 进度条模块
7. 表格模块
8. 代码块模块
9. 引用/提示框模块
10. 标签/徽章模块
11. 按钮模块
12. 表单模块
13. 页脚模块

## 输出接口

### 交付格式

- **文件类型**：单个 `.html` 文件
- **编码**：UTF-8
- **依赖**：无外部依赖，所有CSS/JS内联
- **交付方式**：通过 `present_files` 工具交付

### 质量标准

交付前必须通过12项质量检查（详见SKILL.md"输出规范"章节）。

---

**版本**：v1.0.0
**最后更新**：2026-09-13
