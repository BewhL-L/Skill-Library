# DevOps 与部署运维指南

> DevOps 与部署运维指南。为全栈+AI应用生成从本地开发到生产部署的完整运维方案，包含 Docker 容器化、Docker Compose 编排、Kubernetes 部署、CI/CD 流水线、监控告警、日志收集、Nginx 反向代理、数据库部署与备份。当用户需要部署项目、要求生成 Dockerfile、需要 K8s 部署方案、询问"怎么部署到服务器"、需要 CI/CD 流水线、或要求监控告警方案时使用。支持 Java/Spring Boot、Vue3/前端、Python/FastAPI、AI应用/LangChain、MySQL/Redis 等技术栈的部署。

---

## 功能特性

### 核心原则

- **环境一致性**：开发、测试、生产环境使用相同的容器镜像，避免"在我机器上能跑"
- **基础设施即代码**：所有部署配置（Dockerfile、docker-compose、K8s YAML、CI/CD 配置）版本化管理
- **无状态应用**：应用容器无状态，状态存在数据库/缓存/对象存储，支持水平扩展
- **健康检查**：所有服务有健康检查端点，编排系统自动重启不健康的实例
- **可观测性**：日志、指标、链路追踪三件套齐全，问题可定位、可追溯

---

## 快速开始

详见 [SKILL.md](SKILL.md) 中的使用流程和输出规范。

---

## 文档结构

```
devops-deployment-guide/
├── SKILL.md                          # 核心文档（功能说明/使用流程/输出规范）
├── README.md                         # 项目首页（本文件）
├── CHANGELOG.md                      # 版本变更记录
├── .gitignore                        # Git 忽略配置
├── .editorconfig                     # 编辑器配置
```└── references/
    └── deployment-reference.md

---

## 版本信息

- **当前版本**：v1.0.0
- **最后更新**：2026-08-31
- **基于**：skill-optimizer 25 轮优化方法论 + skill-creator-for-work 规范

---

## 许可证

MIT License
