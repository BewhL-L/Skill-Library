# 各技术栈部署要点与 Docker/K8s 模板

> 供 devops-deployment-guide 生成部署方案时参考，按对应技术栈的部署要点执行。

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

## 各技术栈部署要点

### Java / Spring Boot 部署

**Dockerfile 模板**：
```dockerfile
FROM eclipse-temurin:17-jre-alpine
WORKDIR /app
COPY target/*.jar app.jar
EXPOSE 8080
ENV JAVA_OPTS="-Xms512m -Xmx1024m -XX:+UseG1GC"
ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar app.jar"]
```

**部署要点**：
- JVM 参数调优：堆大小、GC 算法、元空间
- 健康检查：`/actuator/health`
- 配置外部化：application-prod.yml 通过环境变量或配置中心注入
- 日志：输出到 stdout，由 Docker/K8s 收集
- 优雅停机：配置 `server.shutdown=graceful`

**K8s 部署要点**：
- 资源限制：requests/limits（CPU、内存）
- 就绪探针/存活探针：HTTP GET `/actuator/health`
- 滚动更新：maxSurge=1, maxUnavailable=0
- HPA：基于 CPU 使用率自动扩缩容

---

### Vue3 / 前端部署

**Dockerfile 模板（多阶段构建）**：
```dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**nginx.conf 要点**：
- SPA 路由回退：`try_files $uri $uri/ /index.html;`
- 静态资源缓存：JS/CSS 哈希文件名长期缓存，HTML 不缓存
- Gzip 压缩：开启 text/css、application/javascript
- 反向代理：`/api` 代理到后端服务

**部署要点**：
- 构建时注入环境变量：`.env.production`
- CDN 加速：静态资源上传到 CDN
- 版本管理：每个版本保留，支持快速回滚
- 性能优化：构建时代码分割、懒加载、Tree Shaking

---

### Python / FastAPI 部署

**Dockerfile 模板**：
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

**部署要点**：
- Gunicorn + Uvicorn workers：`gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker`
- 异步处理：确保所有 IO 操作都是异步的，避免阻塞事件循环
- 健康检查：`/health` 端点
- 数据库连接池：配置 pool_size、max_overflow
- 依赖锁定：`requirements.txt` 固定版本

---

### AI 应用 / LangChain 部署

**Dockerfile 模板**：
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
ENV PYTHONUNBUFFERED=1
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
```

**部署要点**：
- API Key 管理：通过环境变量或密钥管理服务注入，不写入代码
- 模型缓存：预下载模型到镜像，避免运行时下载
- 流式响应：SSE（Server-Sent Events）支持
- 超时控制：LLM 调用超时、整体请求超时
- 限流：基于用户/API Key 的速率限制
- 成本监控：记录 token 用量，计算成本
- 向量数据库：Milvus/Chroma 独立部署，数据持久化

---

### 数据库部署

**MySQL 部署要点**：
- 主从复制：读写分离，主库写、从库读
- 备份策略：全量备份（每日）+ 增量备份（Binlog）
- 慢查询日志：开启，阈值 1s
- 连接池：max_connections 合理配置
- 数据目录：使用独立磁盘，IO 性能优先
- 监控：QPS、连接数、慢查询、主从延迟

**Redis 部署要点**：
- 持久化：RDB（快照）+ AOF（追加日志）
- 内存策略：maxmemory-policy（allkeys-lru / volatile-lru）
- 主从复制：读写分离
- 哨兵/Sentinel：高可用自动故障转移
- 集群/Cluster：数据分片，水平扩展
- 监控：内存使用率、命中率、连接数、慢查询

---

### Docker Compose 模板

```yaml
version: '3.8'
services:
  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend

  backend:
    build: ./backend
    ports:
      - "8080:8080"
    environment:
      - SPRING_PROFILES_ACTIVE=prod
      - SPRING_DATASOURCE_URL=jdbc:mysql://mysql:3306/app
      - SPRING_REDIS_HOST=redis
    depends_on:
      - mysql
      - redis

  mysql:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=root
      - MYSQL_DATABASE=app
    volumes:
      - mysql_data:/var/lib/mysql
    ports:
      - "3306:3306"

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"

volumes:
  mysql_data:
  redis_data:
```

---

## CI/CD 流水线要点

| 阶段 | 动作 | 工具 |
|------|------|------|
| 代码提交 | 代码检查、单元测试 | ESLint/Prettier、JUnit/Pytest |
| 构建 | 编译、打包、构建镜像 | Maven/npm、Docker Build |
| 测试 | 集成测试、E2E 测试 | Postman/Newman、Cypress |
| 部署 | 推送镜像、部署到环境 | Docker Registry、K8s/Kubectl |
| 验证 | 健康检查、冒烟测试 | curl、自动化测试 |
| 监控 | 日志、指标、告警 | ELK、Prometheus、Grafana |
