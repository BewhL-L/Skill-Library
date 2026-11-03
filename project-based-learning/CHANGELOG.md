# 变更日志

本项目所有重要变更都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

---

## [v1.0.1] - 2026-11-03

### 变更

- 新增「边界与交接」：明确本 Skill 只出方案，不生成项目代码、不生成逐章学习指南。
- 升级为「三 Skill 定位卡」：方案 → 项目 → 指南 三行对照，含"不做什么 / 下一步"；完整表见仓库根 `Skill依赖关系图谱.md`。
- 协作表补两行：要直接生成可运行项目 → `project-scaffolder`；项目已存在、要精读与验收 → `project-processization`。
- description 补边界说明，减少三个"项目类"Skill 的触发重叠。

---

## [v1.0.0] - 2026-08-31

### 新增

- 初始版本发布
- 项目驱动学习生成器 核心功能
### 使用场景

- 场景一：生成完整项目方案
- 场景二：生成项目某一部分的详细方案
- 场景三：基于现有项目扩展

### 参考文档

- references/faq.md
- references/project-templates.md
- references/project-types-and-templates.md

### 基于

- skill-optimizer 25 轮优化方法论
- skill-creator-for-work 规范

---

## 版本类型说明

- **Added**：新增功能
- **Changed**：功能变更
- **Deprecated**：即将废弃的功能
- **Removed**：已移除的功能
- **Fixed**：Bug 修复
- **Security**：安全相关修复
