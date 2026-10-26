# 间隔重复复习助手

> 间隔重复复习助手。基于艾宾浩斯遗忘曲线和 SM-2 算法，为 Obsidian 知识库笔记生成个性化复习计划，自动计算复习间隔，生成今日复习清单和复习统计报告。当用户需要复习笔记、要求生成复习计划、询问"今天该复习什么"、需要复习统计、或要求管理笔记记忆状态时使用。支持新笔记纳入复习、复习质量评分、间隔自动计算、状态流转（new→learning→reviewing→mastered）、与 Obsidian Dataview 联动生成复习清单。生成的复习计划与知识库笔记深度联动。

---

## 功能特性

### 核心原则

- **科学间隔**：基于 SM-2 算法自动计算复习间隔，在遗忘临界点复习，效率最高
- **质量驱动**：复习质量决定下次间隔，记住了延长间隔，忘了缩短间隔
- **状态跟踪**：每篇笔记有明确的复习状态（new→learning→reviewing→mastered），可回退
- **数据驱动**：通过统计报告发现薄弱环节，针对性加强
- **工具联动**：与 Obsidian Dataview 联动，自动生成今日复习清单，无需手动整理

---

## 快速开始

详见 [SKILL.md](SKILL.md) 中的使用流程和输出规范。

---

## 文档结构

```
knowledge-review-spaced/
├── SKILL.md                          # 核心文档（功能说明/使用流程/输出规范）
├── README.md                         # 项目首页（本文件）
├── CHANGELOG.md                      # 版本变更记录
├── .gitignore                        # Git 忽略配置
├── .editorconfig                     # 编辑器配置
```└── references/
    └── review-algorithm.md
    └── review-templates.md

---

## 版本信息

- **当前版本**：v1.0.0
- **最后更新**：2026-08-31
- **基于**：skill-optimizer 25 轮优化方法论 + skill-creator-for-work 规范

---

## 许可证

MIT License
