# Bug 排查助手

> Bug 排查与问题诊断助手。根据错误信息、日志、堆栈、现象，生成系统化的排查路线、根因分析、修复方案和预防措施。当用户遇到报错、需要排查问题、要求分析错误日志、询问"为什么会出现XX错误"、需要修复方案、或要求排查性能问题时使用。支持 Java（Spring/JVM/MyBatis）、前端（Vue3/TypeScript/构建工具）、Python（FastAPI/异步）、AI应用（LLM/RAG/Agent）、数据库（MySQL/Redis）、运维（Docker/K8s/Linux）六大领域的问题排查。

---

## 功能特性

### 核心原则

- **先复现，再排查**：无法稳定复现的问题难以根本解决，先找到复现路径
- **从外到内**：先看错误信息和堆栈，再看日志，再看代码，最后看环境
- **假设驱动**：提出假设 → 验证假设 → 排除/确认，不盲目试错
- **二分法**：通过注释代码、切换环境、对比版本，快速缩小问题范围
- **根因修复**：不只修复表面症状，必须找到根本原因并修复，同时加预防措施

---

## 快速开始

详见 [SKILL.md](SKILL.md) 中的使用流程和输出规范。

---

## 文档结构

```
bug-troubleshooter/
├── SKILL.md                          # 核心文档（功能说明/使用流程/输出规范）
├── README.md                         # 项目首页（本文件）
├── CHANGELOG.md                      # 版本变更记录
├── .gitignore                        # Git 忽略配置
├── .editorconfig                     # 编辑器配置
```└── references/
    └── faq.md
    └── troubleshooting-reference.md

---

## 版本信息

- **当前版本**：v1.0.0
- **最后更新**：2026-08-31
- **基于**：skill-optimizer 25 轮优化方法论 + skill-creator-for-work 规范

---

## 许可证

MIT License
