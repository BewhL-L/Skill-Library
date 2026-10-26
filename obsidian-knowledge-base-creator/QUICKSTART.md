# 🚀 5 分钟快速上手

> 本指南帮助你在 5 分钟内完成工具安装、生成第一个知识库、并开始使用。

---

## ⏱️ 时间线

| 步骤 | 时间 | 操作 |
|------|------|------|
| 1 | 1 分钟 | 运行安装脚本，检测环境和依赖 |
| 2 | 1 分钟 | 生成演示知识库，查看效果 |
| 3 | 1 分钟 | 用 Obsidian 打开，浏览示例笔记 |
| 4 | 1 分钟 | 生成自己的知识库 |
| 5 | 1 分钟 | 创建第一篇标准化笔记 |

---

## 📦 步骤 1：安装（1 分钟）

### Windows 用户

双击运行 `install.bat`，脚本会自动：
1. 检测 Python 环境（需要 3.7+）
2. 安装 PyYAML 依赖
3. 验证所有脚本文件完整
4. 验证核心功能

### 手动安装

如果 install.bat 无法运行，手动执行：

```bash
# 1. 确认 Python 已安装
python --version

# 2. 安装依赖
pip install pyyaml

# 3. 验证
python scripts/config.py
```

### 安装 Obsidian

如果还没有安装 Obsidian：
1. 下载：https://obsidian.md/
2. 安装后打开，选择「打开文件夹作为仓库」

---

## 🎯 步骤 2：生成演示知识库（1 分钟）

运行以下命令，一键生成包含 5 篇高质量示例笔记的演示知识库：

```bash
kb.bat init --name "演示知识库" --path ./demo --demo
```

**输出示例**：
```
🚀 初始化知识库: 演示知识库
📁 创建目录结构... (11 个分类)
📄 创建核心文件... (Home + MOC + 学习路线)
📄 创建分类 MOC... (11 个 MOC)
⚙️  复制 Obsidian 配置... (4 个文件)
📝 复制示例笔记... (13 个文件)
✅ 知识库初始化完成！
```

**`--demo` 模式包含**：
- 5 篇高质量示例笔记（Git入门 / Vue3高级 / JVM专家 / 全栈项目 / 15道面试题）
- 11 个分类 MOC（预置 mindmap、学习路线、文档索引）
- 综合导航 MOC + 学习路线总览
- .obsidian 配置（外观/插件/快捷键/图谱配色）

---

## 👀 步骤 3：用 Obsidian 打开（1 分钟）

1. 打开 Obsidian
2. 选择「打开文件夹作为仓库」
3. 选择刚才生成的 `demo` 文件夹
4. 从 `00-综合导航/Home.md` 开始浏览

**推荐浏览顺序**：
1. `Home.md` — 知识库首页，了解整体结构
2. `MOC-综合导航.md` — 全库内容地图，mindmap 全景
3. `学习路线总览.md` — 四阶段学习路径
4. `07-通用工具/Git快速上手.md` — 入门级示例笔记
5. `02-后端开发/JVM性能调优实战.md` — 专家级深度笔记
6. `99-项目实战/实战-个人博客系统.md` — 完整项目实战
7. `10-面试题汇总/Java后端面试题汇总.md` — 15 道高频面试题

**体验亮点**：
- 🎨 HTML/CSS 动画卡片（流程步骤、对比展示）
- 🧠 Mermaid 思维导图（知识体系全景）
- 📊 精美表格（对比、统计、索引）
- 🔗 双链网络（点击 `[[]]` 跳转）
- ⚙️ 预置 Obsidian 配置（主题色、插件、快捷键）

---

## 🏗️ 步骤 4：生成自己的知识库（1 分钟）

### 基础模式（默认 12 分类）

```bash
kb.bat init --name "我的知识库" --path ./my-kb --theme "全栈+AI"
```

### 自定义主题（AI 工程化）

```bash
kb.bat init --name "AI知识库" --path ./ai-kb --config themes/ai-engineering.yaml
```

AI 主题使用 8 个自定义分类（大模型基础 / Prompt工程 / RAG / AI Agent / 多模态 / AI工程化 等）。

### 自定义配置

1. 复制配置模板：`copy assets\config-template.yaml .kb-config.yaml`
2. 编辑 `.kb-config.yaml`，自定义分类、标签、难度、学习路线
3. 初始化时自动加载：`kb.bat init --name "自定义库" --path ./custom`

---

## ✏️ 步骤 5：创建第一篇笔记（1 分钟）

```bash
kb.bat note --title "Redis 缓存策略" --category "数据库与缓存" --difficulty 3 --kb-root ./my-kb
```

**参数说明**：
- `--title`：笔记标题（必填）
- `--category`：所属分类（必填，从 12 个分类中选择）
- `--difficulty`：难度等级 1-5（可选，默认 3）
- `--tags`：标签列表（可选）
- `--pre`：前置知识（可选）
- `--kb-root`：知识库根目录（用于自动推断输出路径）

**生成的笔记包含**：
- 完整 Frontmatter（10+ 字段）
- 五段式结构（概述→原理→实操→问题→拓展）
- 预置动画卡片和 Mermaid 图占位
- 填充指引注释（`<!-- 填充指引 -->`）
- 统一底部导航

**下一步**：
1. 打开生成的笔记，按填充指引填写内容
2. 完成后将 `status` 从 `📝 草稿` 改为 `✅ 内容已完善`
3. 更新对应分类的 MOC 索引

---

## 📋 常用命令速查

| 命令 | 功能 | 示例 |
|------|------|------|
| `init` | 初始化知识库 | `kb.bat init --name "我的库" --path ./my-kb` |
| `init --demo` | 生成演示知识库 | `kb.bat init --name "演示" --path ./demo --demo` |
| `init --config` | 使用自定义配置 | `kb.bat init --name "AI库" --path ./ai --config themes/ai-engineering.yaml` |
| `note` | 生成笔记 | `kb.bat note --title "主题" --category 前端开发 --kb-root ./my-kb` |
| `moc` | 生成/更新 MOC | `kb.bat moc --category 前端开发 --path ./my-kb/01-前端开发` |
| `audit` | 健康检查 | `kb.bat audit --kb-root ./my-kb` |
| `validate` | 质量校验 | `kb.bat validate --kb-root ./my-kb --strict` |
| `standardize` | 一键标准化 | `kb.bat standardize --kb-root ./my-kb` |
| `progress` | 学习进度报告 | `kb.bat progress --kb-root ./my-kb` |
| `info` | 显示帮助 | `kb.bat info` |

---

## ❓ 常见问题

### Q1：提示「未检测到 Python」
**A**：需要先安装 Python 3.7+。下载地址：https://www.python.org/downloads/，安装时勾选「Add Python to PATH」。

### Q2：提示「No module named 'yaml'」
**A**：运行 `pip install pyyaml` 安装依赖。或运行 `install.bat` 自动安装。

### Q3：生成的笔记是空的？
**A**：`generate-note.py` 生成的是标准化模板（含填充指引），需要手动填写内容。这是设计如此——模板保证结构统一，内容由你填充。

### Q4：MOC 中的链接是红色的（死链）？
**A**：红色链接表示目标笔记尚未创建。可以用 `generate-note.py` 创建对应笔记，或用 `kb.bat fix-link` 修复高频死链。

### Q5：如何自定义分类？
**A**：复制 `assets/config-template.yaml` 为 `.kb-config.yaml`，修改 `structure.categories` 部分，初始化时会自动加载。或使用 `themes/` 目录下的主题预设。

### Q6：Obsidian 中动画卡片不显示？
**A**：需要在 Obsidian 设置中开启「阅读视图」，HTML/CSS 卡片在阅读视图下渲染。编辑视图下显示为 HTML 代码。

### Q7：如何更新 MOC 索引？
**A**：新增笔记后运行 `kb.bat moc --category 分类名 --path 分类目录`，会自动扫描目录下的笔记并更新 MOC。

---

## 📚 更多资源

- **完整文档**：[SKILL.md](SKILL.md) — 完整功能和规范说明
- **模板说明**：[docs/TEMPLATES.md](docs/TEMPLATES.md) — 模板使用与自定义指南
- **Obsidian 指南**：[docs/OBSIDIAN-GUIDE.md](docs/OBSIDIAN-GUIDE.md) — Obsidian 配置与使用
- **常见问题**：[docs/FAQ.md](docs/FAQ.md) — 28 个常见问题解答
- **示例知识库**：`examples/sample-kb/` — 完整示例，可直接用 Obsidian 打开

---

## 🎉 完成！

你已经完成了 5 分钟快速上手：
- ✅ 安装了工具和依赖
- ✅ 生成了演示知识库
- ✅ 用 Obsidian 浏览了示例笔记
- ✅ 生成了自己的知识库
- ✅ 创建了第一篇标准化笔记

**下一步建议**：
1. 深入阅读 [SKILL.md](SKILL.md) 了解全部功能
2. 参考示例笔记的格式，创建自己的笔记
3. 用 `audit` 和 `validate` 命令检查知识库质量
4. 探索 `themes/` 目录下的主题预设，创建不同领域的知识库

---

> 💡 **提示**：遇到问题先查 [docs/FAQ.md](docs/FAQ.md)，或运行 `kb.bat info` 查看帮助。
