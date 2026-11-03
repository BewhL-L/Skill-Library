# 变更日志

本项目所有重要变更都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

---

## [v1.0.2] - 2026-11-03

### 新增

- 「工程实践基线」：验收写成"命令 + 期望输出"，数字取自机器可读产物（junit xml），不抄终端摘要行；四类静默失败（配置旁路 / 绝对阈值 / 校验未同步 / 取消异常）各配一条验收。
- 提交纪律：`commit` 是批准、`push` 是传输；按模块提交、按路径 `git add`、装 `secret-gate` 的 pre-commit 闸门。
- 环境一致性验收：改一行 → 重启 → 确认生效，防"跑的是旧副本"。
- 质量检查清单新增 4 项对应上述要求。

### 背景

- 2026-11-02/03 实战沉淀：一轮"测试全绿但依然可能错"的代码审查（24 文件 / +908 −123）里，问题几乎都是"看起来正常"的静默失败；同期的 Git 自动化又踩了"改了源码、加载的是旧副本"与 `git add -A` 带出私密文件两次事故。方案层不写进去，学习者必然重踩。

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
