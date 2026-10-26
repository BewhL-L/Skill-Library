---
name: devops-deployment-guide
description: DevOps 与部署运维指南。为全栈+AI应用生成从本地开发到生产部署的完整运维方案，包含 Docker 容器化、Docker Compose 编排、Kubernetes 部署、CI/CD 流水线、监控告警、日志收集、Nginx 反向代理、数据库部署与备份。当用户需要部署项目、要求生成 Dockerfile、需要 K8s 部署方案、询问"怎么部署到服务器"、需要 CI/CD 流水线、或要求监控告警方案时使用。支持 Java/Spring Boot、Vue3/前端、Python/FastAPI、AI应用/LangChain、MySQL/Redis 等技术栈的部署。
---

# DevOps 与部署运维指南

> 为项目生成**从本地到生产**的完整部署运维方案，包含容器化、编排、CI/CD、监控、日志，解决"代码写好了但不会部署"的问题。

---

## 核心原则

1. **环境一致性**：开发、测试、生产环境使用相同的容器镜像，避免"在我机器上能跑"
2. **基础设施即代码**：所有部署配置（Dockerfile、docker-compose、K8s YAML、CI/CD 配置）版本化管理
3. **无状态应用**：应用容器无状态，状态存在数据库/缓存/对象存储，支持水平扩展
4. **健康检查**：所有服务有健康检查端点，编排系统自动重启不健康的实例
5. **可观测性**：日志、指标、链路追踪三件套齐全，问题可定位、可追溯

---

## 部署架构分层

| 层级 | 组件 | 职责 |
|------|------|------|
| 接入层 | Nginx / API Gateway | 负载均衡、SSL 终止、限流、路由 |
| 应用层 | Docker 容器 / K8s Pod | 运行应用服务，无状态、可水平扩展 |
| 服务层 | 微服务 / 中间件 | 业务服务、消息队列、缓存 |
| 数据层 | MySQL / Redis / 对象存储 | 数据持久化，有状态、需备份 |
| 运维层 | Prometheus / Grafana / ELK | 监控、日志、告警 |

---

## 各技术栈部署要点概览

> 各技术栈的完整 Dockerfile 模板、部署要点、K8s 配置、Docker Compose 模板、CI/CD 流水线详见 [references/deployment-reference.md](references/deployment-reference.md)，生成部署方案时按对应技术栈的模板执行。

| 技术栈 | 基础镜像 | 核心部署要点 | 健康检查 |
|--------|---------|------------|---------|
| Java/Spring Boot | eclipse-temurin:17-jre-alpine | JVM 参数调优、优雅停机、配置外部化 | /actuator/health |
| Vue3/前端 | nginx:alpine（多阶段构建） | SPA 路由回退、静态资源缓存、Gzip、CDN | HTTP 200 |
| Python/FastAPI | python:3.11-slim | Gunicorn+Uvicorn workers、异步不阻塞、连接池 | /health |
| AI/LangChain | python:3.11-slim | API Key 管理、模型缓存、流式响应、超时限流、成本监控 | /health |
| MySQL | mysql:8.0 | 主从复制、备份策略、慢查询日志、连接池 | mysqladmin ping |
| Redis | redis:7-alpine | RDB+AOF 持久化、内存策略、主从/哨兵/集群 | redis-cli ping |

---

## 使用示例

**输入**："我有一个 Vue3 + Spring Boot + MySQL + Redis 的全栈项目，帮我生成完整的 Docker Compose 部署方案，包含 Nginx 反向代理和监控"

**输出**：
- 优化的多阶段 Dockerfile（前端 nginx:alpine、后端 eclipse-temurin:17-jre-alpine）
- 完整 docker-compose.yml（frontend、backend、mysql、redis、nginx、prometheus、grafana）
- Nginx 配置（反向代理、负载均衡、SSL、静态资源缓存、Gzip）
- 健康检查配置（每个服务的健康检查端点）
- 资源限制（CPU、内存 requests/limits）
- 环境变量和密钥管理（.env 模板）
- 部署步骤和回滚步骤
- 监控方案（Prometheus 指标采集、Grafana 仪表盘、告警规则）
- 与 `[[Docker]]` `[[Nginx]]` 等知识库笔记双向链接

---

## 工作流程

### 场景一：生成完整部署方案

1. 确认需求：
   - 项目技术栈和服务清单
   - 部署环境（单机 Docker / Docker Compose / K8s 集群）
   - 域名和 SSL 需求
   - 是否需要 CI/CD
   - 监控和日志需求

2. 生成 Dockerfile：为每个服务生成优化的 Dockerfile（多阶段构建、最小基础镜像、非 root 用户）

3. 生成编排配置：
   - 单机：docker-compose.yml（服务、网络、卷、环境变量）
   - K8s：Deployment、Service、ConfigMap、Secret、Ingress、HPA

4. 生成 Nginx 配置：反向代理、负载均衡、SSL、静态资源缓存、Gzip

5. 生成 CI/CD 流水线：代码提交→构建→测试→推送镜像→部署→验证

6. 生成监控方案：Prometheus 指标采集、Grafana 仪表盘、告警规则、日志收集（ELK/Loki）

7. 生成运维手册：部署步骤、回滚步骤、常见问题排查、备份恢复

### 场景二：生成单个服务的 Dockerfile

1. 确认服务技术栈和构建工具
2. 生成优化的 Dockerfile：
   - 多阶段构建（构建阶段 + 运行阶段）
   - 最小基础镜像（alpine / slim）
   - 依赖缓存层（先复制依赖文件，再复制源码）
   - 非 root 用户运行
   - 健康检查
   - 合理的 EXPOSE 和 CMD/ENTRYPOINT
3. 提供 .dockerignore 配置

### 场景三：生成 CI/CD 流水线

1. 确认 CI/CD 平台（GitHub Actions / GitLab CI / Jenkins）
2. 生成流水线配置：
   - 触发条件（push / PR / tag）
   - 阶段划分（代码检查→测试→构建→推送→部署）
   - 环境变量和密钥管理
   - 缓存策略（依赖缓存、构建缓存）
   - 部署策略（滚动更新 / 蓝绿 / 金丝雀）
3. 提供流水线优化建议

---

## 输出规范

1. Dockerfile 必须使用多阶段构建，镜像体积最小化
2. 所有配置文件必须有注释，说明每个配置项的作用
3. 环境变量和密钥必须分离（ConfigMap / Secret / .env）
4. 健康检查必须配置（HTTP 端点或命令）
5. 资源限制必须配置（CPU、内存 requests/limits）
6. 部署方案必须包含回滚步骤
7. 监控方案必须有具体的告警阈值
8. 所有命令和配置必须可直接使用，不是占位符

---

## 质量检查清单

- [ ] Dockerfile 使用多阶段构建，镜像体积最小化
- [ ] 所有配置文件有注释，说明每个配置项的作用
- [ ] 环境变量和密钥分离（ConfigMap / Secret / .env）
- [ ] 健康检查已配置（HTTP 端点或命令）
- [ ] 资源限制已配置（CPU、内存 requests/limits）
- [ ] 部署方案包含回滚步骤
- [ ] 监控方案有具体的告警阈值
- [ ] 所有命令和配置可直接使用，不是占位符
- [ ] 各技术栈的部署要点与实际技术栈匹配
- [ ] CI/CD 流水线有明确的阶段和触发条件

---

## 与其他 Skill 的协作

- **与 `project-based-learning` 协作**：项目方案的部署部分用本 skill 生成完整部署方案
- **与 `bug-troubleshooter` 协作**：部署中遇到的问题用排查助手定位和解决
- **与 `system-design-planner` 协作**：高可用部署架构用系统设计生成器设计
- **与 `learning-path-planner` 协作**：DevOps 技能纳入学习路线的后期阶段
- **与 `cheatsheet-generator` 协作**：Docker/K8s/Nginx 常用命令整理成速查表

---

> **版本**：v1.0.0
>
> **最后更新**：2026-08-31
>
> **基于**：skill-optimizer 25 轮优化方法论 + skill-creator-for-work 规范

