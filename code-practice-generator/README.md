# 代码实践生成器

> 全栈+AI工程化代码实践生成器。为指定技术概念或知识点生成可独立运行的最小代码项目（含完整目录结构、依赖配置、README），并生成梯度练习题（基础→进阶→挑战）附答案和解析。支持 Java/Spring Boot、Vue3+TypeScript、Python/FastAPI/Django、AI应用（LangChain/RAG/Agent）四大技术栈。当用户需要练习某个技术点、要求生成可运行的代码示例、需要练习题、或学习笔记中缺少实操项目时使用。生成的代码项目可与 Obsidian 知识库笔记双向链接。

---

## 功能特性

### 核心原则

- **可运行**：每个项目必须能在标准环境中直接运行，包含完整的依赖配置和启动说明
- **最小完整**：项目只包含演示目标概念所需的最小代码，但结构完整、符合生产规范
- **梯度练习**：练习题分基础→进阶→挑战三个难度，覆盖从"会用"到"精通"的路径
- **答案解析**：每道题都有完整答案和详细解析，解析说明"为什么这样写"
- **知识联动**：项目与知识库笔记双向链接，代码中的关键概念标注对应笔记

---

## 快速开始

详见 [SKILL.md](SKILL.md) 中的使用流程和输出规范。

---

## 文档结构

```
code-practice-generator/
├── SKILL.md                          # 核心文档（功能说明/使用流程/输出规范）
├── README.md                         # 项目首页（本文件）
├── CHANGELOG.md                      # 版本变更记录
├── .gitignore                        # Git 忽略配置
├── .editorconfig                     # 编辑器配置
```└── references/
    └── exercise-patterns.md
    └── faq.md
    └── project-starters.md

---

## 版本信息

- **当前版本**：v1.0.0
- **最后更新**：2026-08-31
- **基于**：skill-optimizer 25 轮优化方法论 + skill-creator-for-work 规范

---

## 许可证

MIT License
