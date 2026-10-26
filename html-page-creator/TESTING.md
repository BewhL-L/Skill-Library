# 测试指南

> 本文档描述 html-page-creator Skill 的测试方法。由于本Skill为纯文档型（doc-only），测试以验证输出质量和文档完整性为主。

## 测试概述

本Skill不包含可执行代码，测试分为以下几个层面：

1. **文档完整性测试** - 验证所有必需文档存在且内容完整
2. **模板功能测试** - 验证template.html在浏览器中正常渲染
3. **输出质量测试** - 验证生成的网页符合质量标准
4. **设计一致性测试** - 验证输出遵循设计系统规范

## 文档完整性测试

### 必需文档清单

使用以下命令检查文档完整性：

```bash
# 检查所有必需文档是否存在
ls -la SKILL.md README.md QUICKSTART.md CHANGELOG.md FAQ.md \
  CONTRIBUTING.md SECURITY.md CODE_OF_CONDUCT.md INSTALLATION.md \
  USE-CASES.md SUPPORT.md API.md ARCHITECTURE.md TESTING.md DEBUGGING.md \
  LICENSE .gitignore .editorconfig
```

### 文档内容检查

| 文档 | 检查项 | 验收标准 |
|------|--------|---------|
| SKILL.md | frontmatter完整 | 包含name、version、description |
| SKILL.md | 工作流程 | 包含至少5步工作流程 |
| SKILL.md | 输出规范 | 包含质量检查清单（≥10项） |
| README.md | 功能介绍 | 包含核心功能列表 |
| README.md | 快速开始 | 包含使用方式说明 |
| design-system.md | 颜色系统 | 包含≥4种强调色定义 |
| design-system.md | 排版系统 | 包含≥5级字号定义 |
| module-library.md | 模块数量 | 包含≥10种模块 |
| module-library.md | 代码完整性 | 每个模块包含HTML+CSS |

## 模板功能测试

### 测试步骤

1. **复制模板**
   ```bash
   cp assets/template.html /tmp/test-page.html
   ```

2. **在浏览器中打开**
   - 检查页面是否正常渲染
   - 检查控制台是否有JavaScript错误

3. **功能验证清单**

| 功能 | 测试方法 | 预期结果 |
|------|---------|---------|
| 页面渲染 | 打开HTML文件 | 页面正常显示，无白屏 |
| 深色主题 | 默认加载 | 深色背景，浅色文字 |
| 主题切换 | 点击右上角按钮 | 切换为浅色主题，颜色适配 |
| 主题持久化 | 刷新页面 | 保持上次选择的主题 |
| 滚动进度条 | 向下滚动 | 顶部进度条宽度增加 |
| 入场动画 | 滚动到新区域 | 元素淡入+上移 |
| 导航链接 | 点击导航项 | 平滑滚动到对应章节 |
| 卡片悬停 | 鼠标悬停卡片 | 卡片上浮4px，阴影加深 |
| 响应式 | 缩小窗口到<768px | 单列布局，导航链接隐藏 |
| 减少动画 | 系统开启减少动画 | 入场动画禁用 |

### 浏览器兼容性测试

在以下浏览器中验证模板功能：
- Chrome 90+
- Edge 90+
- Firefox 88+
- Safari 14+

## 输出质量测试

使用Skill生成一个测试网页，然后验证：

### 基础质量检查（12项）

- [ ] HTML结构完整（DOCTYPE/head/body）
- [ ] 元数据已填写（title/description）
- [ ] 主题切换功能正常
- [ ] 响应式布局正常（桌面/平板/手机）
- [ ] 玻璃效果统一（使用CSS变量）
- [ ] 入场动画正常
- [ ] 滚动进度条正常
- [ ] 导航功能正常
- [ ] 内容完整无遗漏
- [ ] 无控制台错误
- [ ] 性能可接受（无明显卡顿）
- [ ] 无硬编码颜色值

### 设计一致性检查

- [ ] 所有颜色使用CSS变量
- [ ] 间距使用8px倍数
- [ ] 圆角使用--radius变量
- [ ] 阴影使用--shadow变量
- [ ] 动效使用--ease缓动函数
- [ ] 玻璃效果统一使用var(--glass)

## 性能测试

### 加载性能

| 指标 | 目标 | 测试方法 |
|------|------|---------|
| 文件大小 | ≤100KB | `ls -lh output.html` |
| 首次渲染 | <1s | 浏览器DevTools Performance |
| 交互响应 | <100ms | 点击/悬停响应时间 |

### 运行时性能

| 指标 | 目标 | 测试方法 |
|------|------|---------|
| 内存占用 | <50MB | 浏览器任务管理器 |
| FPS | ≥60 | 浏览器DevTools FPS meter |
| 滚动流畅 | 无卡顿 | 手动滚动测试 |

## 自动化测试

### 使用skill-optimizer审计

```bash
# 运行健康检查
python skill-optimizer/scripts/skill-opt.py audit --path ./html-page-creator

# 目标：总分≥85（A级）
```

### 模板HTML验证

```bash
# 使用HTML验证工具（如html-validate）
npx html-validate assets/template.html

# 检查无错误和警告
```

## 回归测试

每次修改后必须运行：

1. 文档完整性检查
2. 模板功能测试（在浏览器中验证）
3. skill-optimizer审计（确保分数不下降）
4. 生成一个测试网页，验证输出质量

---

**版本**：v1.0.0
**最后更新**：2026-09-13
