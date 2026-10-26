# 架构文档

> 本文档描述 html-page-creator Skill 的架构设计。由于本Skill为纯文档型（doc-only），架构以文档组织和资源引用为核心。

## 架构总览

```
html-page-creator/
│
├── 📄 核心文档层
│   ├── SKILL.md              # Skill入口，工作流程与输出规范
│   ├── README.md             # 项目首页，功能概览
│   └── QUICKSTART.md         # 快速上手指南
│
├── 📚 参考文档层
│   ├── references/
│   │   ├── design-system.md  # 设计系统规范（单一数据源）
│   │   └── module-library.md # 模块库（13种可复用模块）
│   ├── API.md                # 接口参考
│   ├── FAQ.md                # 常见问题
│   └── USE-CASES.md          # 使用案例
│
├── 🎨 模板资源层
│   └── assets/
│       └── template.html     # 基础网页模板（可复制）
│
├── 📝 工程化配置层
│   ├── .gitignore
│   ├── .editorconfig
│   └── LICENSE
│
└── 📖 治理文档层
    ├── CHANGELOG.md
    ├── CONTRIBUTING.md
    ├── SECURITY.md
    ├── CODE_OF_CONDUCT.md
    ├── INSTALLATION.md
    ├── SUPPORT.md
    ├── TESTING.md
    ├── DEBUGGING.md
    └── ARCHITECTURE.md       # 本文件
```

## 设计原则

### 1. 单一数据源（Single Source of Truth）

- 设计规范只存在于 `references/design-system.md`
- 模块代码只存在于 `references/module-library.md`
- 模板只存在于 `assets/template.html`
- 其他文档引用这些源，不重复定义

### 2. 渐进式披露（Progressive Disclosure）

| 层级 | 内容 | 加载时机 |
|------|------|---------|
| L1 | Skill元数据（name/description） | 始终在上下文 |
| L2 | SKILL.md正文 | Skill触发时加载 |
| L3 | references/文档 | 需要时按需读取 |
| L4 | assets/template.html | 创建网页时复制 |

### 3. 纯文档型架构

本Skill不包含可执行代码，所有功能通过：
- 标准化模板（复制+修改）
- 设计系统规范（遵循+应用）
- 模块库（选择+组合）

由AI Agent执行，无需运行时环境。

## 数据流

```
用户需求
    │
    ▼
SKILL.md（工作流程）
    │
    ├─→ 理解需求
    │
    ├─→ 复制 assets/template.html
    │
    ├─→ 读取 references/module-library.md（选择模块）
    │
    ├─→ 读取 references/design-system.md（设计检查）
    │
    ├─→ 定制内容（填充用户数据）
    │
    ├─→ 质量检查（12项清单）
    │
    ▼
交付 HTML 文件
```

## 模块依赖关系

```
template.html
    ├── 依赖 design-system.md（CSS变量定义）
    └── 可扩展 module-library.md（添加模块）

module-library.md
    └── 依赖 design-system.md（所有模块使用统一变量）

design-system.md
    └── 无外部依赖（最底层规范）
```

## 扩展点

### 添加新模块
1. 在 `references/module-library.md` 添加模块文档
2. 确保模块使用 `design-system.md` 定义的CSS变量
3. 在 `SKILL.md` 模块组合建议中更新

### 修改设计规范
1. 修改 `references/design-system.md`
2. 同步更新 `assets/template.html` 中的CSS变量
3. 检查 `module-library.md` 中是否有硬编码值需要更新

### 创建新模板
1. 复制 `assets/template.html`
2. 根据需求修改结构和样式
3. 保存到 `assets/` 目录，命名清晰

## 性能考量

- **单文件交付**：所有CSS/JS内联，无HTTP请求
- **无外部依赖**：不加载外部字体、图标、库
- **控制backdrop-filter**：建议页面中玻璃卡片数量≤20个
- **精简动画**：入场动画只应用于关键模块，非所有元素
- **图片优化**：背景图片建议≤500KB，使用WebP格式

## 兼容性

| 浏览器 | 最低版本 | 说明 |
|--------|---------|------|
| Chrome | 90+ | 完全支持 |
| Edge | 90+ | 完全支持 |
| Firefox | 88+ | backdrop-filter需开启 |
| Safari | 14+ | 完全支持 |
| 移动端Chrome | 90+ | 响应式适配 |
| 移动端Safari | 14+ | 响应式适配 |

---

**版本**：v1.0.0
**最后更新**：2026-09-13
