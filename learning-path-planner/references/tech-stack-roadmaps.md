# 四大技术栈详细知识点清单

> 供 learning-path-planner 生成学习路线时参考，确保知识点覆盖全面、顺序合理。

## 一、Java 全栈方向

### 初期（4-6 周）
- Java 基础：语法、面向对象、集合框架（List/Map/Set）、异常处理、IO/NIO
- JVM 基础：内存结构、类加载过程、垃圾回收基础
- MySQL 基础：SQL 语法、索引基础、事务、常用函数
- Spring Boot 入门：自动配置、starter、RESTful API、配置文件
- Maven：依赖管理、生命周期、多模块项目
- Git：基础命令、分支管理、协作流程

### 中期（6-8 周）
- Spring Boot 进阶：拦截器/过滤器、AOP、事件机制、自动配置原理
- MyBatis：XML 映射、动态 SQL、一级/二级缓存、分页插件
- Redis：数据结构、持久化、缓存策略、分布式锁
- Spring MVC：请求处理流程、参数绑定、返回值处理、文件上传
- 接口设计：RESTful 规范、统一返回体、异常处理、接口文档（Swagger）
- 单元测试：JUnit 5、Mockito、Spring Boot Test

### 后期（8-10 周）
- Spring Cloud：注册中心（Nacos/Eureka）、配置中心、网关（Gateway）、负载均衡（OpenFeign）
- 消息队列：RabbitMQ/Kafka，消息可靠性、死信队列、延迟队列
- 分布式事务：Seata、TCC、Saga、最终一致性
- JVM 调优：垃圾收集器选择、内存参数调优、GC 日志分析、OOM 排查
- 高并发：线程池、并发工具（AQS/CountDownLatch/CyclicBarrier）、ConcurrentHashMap
- 性能优化：SQL 优化、索引优化、缓存优化、压测（JMeter）

### 专家（持续学习）
- Spring 源码：IoC 容器初始化、Bean 生命周期、AOP 实现、事务实现
- MyBatis 源码：SqlSession 工作流程、Mapper 代理、插件机制
- 分布式架构：CAP/BASE、一致性算法（Raft/Paxos）、分布式 ID、限流熔断（Sentinel）
- 云原生：Docker、Kubernetes 基础、Service Mesh、可观测性（Prometheus/Grafana）
- 架构设计：领域驱动设计（DDD）、微服务拆分、高可用设计、容量规划

---

## 二、Vue3 + TypeScript 方向

### 初期（3-4 周）
- TypeScript 基础：类型系统、接口、泛型、类型守卫、装饰器
- Vue3 基础：模板语法、响应式基础、计算属性、侦听器、条件/列表渲染
- 组合式 API：setup、ref/reactive、computed/watch、生命周期钩子、自定义 Hook
- 组件基础：Props、Emit、插槽、组件通信、动态组件
- Vite 基础：项目搭建、配置文件、依赖预构建、HMR 原理
- CSS 基础：Flexbox、Grid、响应式设计、CSS 变量

### 中期（4-6 周）
- Vue Router：路由配置、动态路由、导航守卫、路由懒加载、滚动行为
- Pinia：状态管理、Getters、Actions、插件、持久化
- 组件设计：组件封装原则、v-model 实现、透传 Attributes、依赖注入（Provide/Inject）
- 工程化：ESLint + Prettier、Husky + lint-staged、Commitlint、环境变量
- 单元测试：Vitest、Vue Test Utils、测试驱动开发
- 常用库：Axios 封装、Element Plus / Ant Design Vue、ECharts、Day.js

### 后期（6-8 周）
- Vue3 响应式原理：Proxy、Reflect、依赖收集、触发更新、effect 调度
- 虚拟 DOM：VNode 结构、Diff 算法（双端对比）、Patch 流程、静态提升
- 编译优化：PatchFlag、Block Tree、缓存事件处理、静态提升
- 性能优化：组件懒加载、虚拟列表、防抖节流、内存泄漏排查、首屏优化
- 微前端：qiankun、wujie、应用隔离、通信机制
- TypeScript 进阶：条件类型、映射类型、模板字面量类型、类型体操

### 专家（持续学习）
- Vue3 源码：编译器（parse/transform/generate）、运行时（renderer/component）、响应式系统
- Vite 源码：插件机制、依赖预构建（esbuild）、HMR 实现、Rollup 集成
- 前端架构：微前端架构、组件库设计、Monorepo（pnpm workspace + Turborepo）
- 跨端方案：uni-app、Taro、Electron、Flutter Web
- 工程化体系：构建工具对比（Webpack/Vite/Rspack）、CI/CD、自动化测试、性能监控

---

## 三、Python 全栈方向

### 初期（3-4 周）
- Python 基础：语法、数据结构（list/dict/set/tuple）、函数、面向对象、异常处理
- 高级特性：装饰器、生成器、迭代器、上下文管理器、列表推导式
- 文件操作：文件读写、CSV/JSON、路径处理（pathlib）
- 虚拟环境：venv、conda、pip、requirements.txt
- 数据库基础：SQLite、MySQL 连接（pymysql）、基础 CRUD

### 中期（4-6 周）
- FastAPI：路由、请求体、依赖注入、中间件、CORS、自动文档
- Django：MTV 模式、ORM、Admin、表单、认证系统
- ORM：SQLAlchemy Core/ORM、查询优化、关系映射、迁移（Alembic）
- RESTful API：接口设计、认证（JWT/OAuth2）、分页、序列化
- 缓存：Redis（redis-py）、缓存策略、分布式锁
- 测试：pytest、unittest、mock、覆盖率

### 后期（6-8 周）
- 异步编程：asyncio、aiohttp、异步 ORM、并发控制
- 消息队列：Celery、RabbitMQ/Redis 作为 broker、定时任务
- 性能优化：代码性能分析（cProfile）、内存优化、并发模型选择
- 部署：Gunicorn/Uvicorn、Nginx 反向代理、Supervisor、Docker
- 安全：SQL 注入防护、XSS/CSRF、密码哈希、API 限流
- 日志：logging 模块、结构化日志、日志收集

### 专家（持续学习）
- Python 源码：CPython 解释器、GIL 机制、内存管理（引用计数/分代回收）
- 高性能服务：异步框架对比（FastAPI/Tornado/Sanic）、连接池、性能调优
- 架构设计：微服务（Nameko）、事件驱动、CQRS、领域驱动设计
- 数据工程：Pandas、NumPy、数据管道、ETL
- 云原生：Kubernetes 部署、服务网格、可观测性

---

## 四、AI 应用开发方向

### 初期（3-4 周）
- LLM 基础：Transformer 架构、注意力机制、Tokenization、上下文窗口
- Prompt 工程：零样本/少样本、思维链（CoT）、角色设定、输出格式控制
- API 调用：OpenAI API / 国内大模型 API、流式输出、函数调用（Function Calling）
- Embedding：向量表示、相似度计算（余弦相似度）、常用 Embedding 模型
- RAG 基础：检索增强生成流程、文档切分（Chunking）、向量存储、简单检索
- Python 基础：必要的 Python 编程能力

### 中期（4-6 周）
- LangChain：Chain、Prompt Template、Output Parser、Memory、Agent
- LlamaIndex：索引类型（Vector/Tree/Keyword）、查询引擎、响应合成
- 向量数据库：Chroma、FAISS、Milvus、Pinecone，索引类型，检索优化
- Agent 开发：ReAct 模式、工具调用、多 Agent 协作、规划与执行
- 多轮对话：对话历史管理、上下文压缩、记忆机制（短期/长期）
- 评估：RAG 评估（检索质量/生成质量）、LLM 评估、人工评估

### 后期（6-8 周）
- RAG 进阶：混合检索（BM25+向量）、重排序（Reranker）、查询改写、多路召回
- Agent 框架：AutoGen、CrewAI、LangGraph，状态管理、人机协作
- 多模态：图文理解（GPT-4V/Qwen-VL）、语音识别/合成、视频理解
- 微调入门：LoRA/QLoRA、数据集准备、训练流程（PEFT）、效果评估
- 推理优化：量化（GPTQ/AWQ）、KV Cache、批处理、模型蒸馏
- 部署：vLLM、Ollama、模型服务化、API 网关、限流

### 专家（持续学习）
- LLM 推理优化：PagedAttention、Continuous Batching、Speculative Decoding、Tensor Parallel
- 分布式部署：多卡推理、模型并行、流水线并行、集群调度（K8s）
- Agent 编排：复杂工作流设计、错误恢复、长期规划、多 Agent 通信协议
- RAG 架构设计：分层检索、知识图谱增强 RAG、多模态 RAG、实时 RAG
- 私有化部署：本地模型选型、硬件配置、安全隔离、数据隐私
- 前沿研究：Agent 记忆机制、工具学习、世界模型、AGI 方向

---

## 使用说明

1. 生成学习路线时，从对应方向的对应阶段提取知识点
2. 每个知识点标注优先级（P0/P1/P2），P0 为该阶段必学
3. 知识点顺序遵循依赖关系，前置知识点排在前面
4. 可根据用户目标（求职/进阶/项目）调整知识点覆盖范围
5. 每个知识点应对应知识库中的一篇笔记，无对应笔记时标注「待创建」
