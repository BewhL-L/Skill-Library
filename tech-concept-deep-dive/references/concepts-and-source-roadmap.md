# 核心概念与源码阅读路线

> 供 tech-concept-deep-dive 选择拆解深度和源码分析方向时参考。

## 一、各技术栈核心概念清单

### Java 方向（按优先级排序）
| 概念 | 难度 | 源码可分析 | 拆解重点 |
|------|------|-----------|---------|
| Spring IoC 容器 | ⭐⭐⭐⭐ | ✅ | BeanDefinition 加载、Bean 实例化、依赖注入 |
| Spring AOP | ⭐⭐⭐⭐ | ✅ | JDK 动态代理 vs CGLIB、拦截器链、织入时机 |
| Spring 事务 | ⭐⭐⭐⭐ | ✅ | 事务传播、事务隔离、回滚规则、事务同步 |
| Spring 循环依赖 | ⭐⭐⭐⭐ | ✅ | 三级缓存、提前暴露、AOP 代理与循环依赖 |
| MyBatis 工作流程 | ⭐⭐⭐ | ✅ | SqlSession、Mapper 代理、StatementHandler |
| JVM 垃圾回收 | ⭐⭐⭐⭐ | ❌ | GC Roots、标记算法、收集器对比、GC 日志 |
| JVM 类加载 | ⭐⭐⭐ | ❌ | 双亲委派、加载过程、热部署 |
| synchronized 原理 | ⭐⭐⭐⭐ | ❌ | 对象头、锁升级（偏向→轻量→重量）、monitor |
| AQS | ⭐⭐⭐⭐ | ✅ | CLH 队列、state、acquire/release、Condition |
| ConcurrentHashMap | ⭐⭐⭐⭐ | ✅ | 分段锁→CAS+synchronized、扩容、size 计算 |
| Redis 持久化 | ⭐⭐⭐ | ❌ | RDB vs AOF、混合持久化、重启恢复 |
| Redis 集群 | ⭐⭐⭐⭐ | ❌ | 主从复制、哨兵、Cluster 分片、故障转移 |
| MySQL 索引 | ⭐⭐⭐ | ❌ | B+ 树、聚簇/非聚簇、最左前缀、覆盖索引 |
| MySQL MVCC | ⭐⭐⭐⭐ | ❌ | undo log、read view、可见性判断 |
| 分布式事务 | ⭐⭐⭐⭐ | ❌ | 2PC、TCC、Saga、本地消息表、最终一致性 |

### Vue3 方向
| 概念 | 难度 | 源码可分析 | 拆解重点 |
|------|------|-----------|---------|
| 响应式原理 | ⭐⭐⭐⭐ | ✅ | Proxy、track/trigger、effect、依赖收集 |
| ref vs reactive | ⭐⭐⭐ | ✅ | ref 包装、reactive 代理、自动解包 |
| 虚拟 DOM | ⭐⭐⭐⭐ | ✅ | VNode、patch、diff 算法、静态提升 |
| 组件渲染流程 | ⭐⭐⭐⭐ | ✅ | 组件实例化、setup 执行、渲染、更新 |
| 编译优化 | ⭐⭐⭐⭐ | ✅ | PatchFlag、Block Tree、缓存事件、hoistStatic |
| 计算属性 | ⭐⭐⭐ | ✅ | 懒计算、缓存、依赖追踪、dirty 标记 |
| 侦听器 | ⭐⭐⭐ | ✅ | watch vs watchEffect、immediate、deep、flush |
| 生命周期 | ⭐⭐ | ❌ | 各阶段调用时机、与选项式对应 |
| 依赖注入 | ⭐⭐⭐ | ❌ | provide/inject、响应式注入、层级查找 |
| Vite HMR | ⭐⭐⭐⭐ | ✅ | 模块边界、热更新边界、状态保留 |
| Vite 依赖预构建 | ⭐⭐⭐ | ✅ | esbuild、CJS→ESM、依赖扫描、缓存 |

### Python 方向
| 概念 | 难度 | 源码可分析 | 拆解重点 |
|------|------|-----------|---------|
| GIL | ⭐⭐⭐⭐ | ❌ | 全局解释器锁、多线程限制、释放时机 |
| 装饰器 | ⭐⭐⭐ | ❌ | 函数装饰器、类装饰器、带参数装饰器、wraps |
| 生成器 | ⭐⭐⭐ | ❌ | yield、send、throw、close、生成器表达式 |
| 上下文管理器 | ⭐⭐⭐ | ❌ | __enter__/__exit__、contextlib、异常处理 |
| 元类 | ⭐⭐⭐⭐ | ❌ | type、__new__、类创建过程、元类应用 |
| 描述符 | ⭐⭐⭐⭐ | ❌ | __get__/__set__/__delete__、property、方法绑定 |
| 内存管理 | ⭐⭐⭐⭐ | ❌ | 引用计数、分代回收、循环引用、内存池 |
| asyncio | ⭐⭐⭐⭐ | ✅ | 事件循环、协程、Task、Future、调度 |
| WSGI/ASGI | ⭐⭐⭐ | ❌ | 接口规范、中间件、同步 vs 异步 |
| FastAPI 依赖注入 | ⭐⭐⭐ | ✅ | Depends、依赖树、作用域、覆盖依赖 |

### AI 应用方向
| 概念 | 难度 | 源码可分析 | 拆解重点 |
|------|------|-----------|---------|
| Transformer 架构 | ⭐⭐⭐⭐ | ❌ | 自注意力、多头注意力、前馈网络、位置编码 |
| Attention 机制 | ⭐⭐⭐⭐ | ❌ | Q/K/V、缩放点积、掩码、计算复杂度 |
| Tokenization | ⭐⭐⭐ | ❌ | BPE、WordPiece、SentencePiece、特殊 token |
| Embedding | ⭐⭐⭐ | ❌ | 向量表示、相似度、维度选择、模型对比 |
| RAG 流程 | ⭐⭐⭐ | ❌ | 文档切分、向量化、检索、生成、引用 |
| 向量检索 | ⭐⭐⭐⭐ | ❌ | ANN 算法（HNSW/IVF）、索引类型、召回率 |
| ReAct Agent | ⭐⭐⭐ | ✅ | 推理-行动循环、工具调用、观察、终止条件 |
| Function Calling | ⭐⭐⭐ | ❌ | 函数定义、参数解析、调用、结果返回 |
| 提示工程 | ⭐⭐ | ❌ | 零样本/少样本、CoT、角色、输出格式 |
| 微调（LoRA） | ⭐⭐⭐⭐ | ❌ | 低秩适配、冻结主干、rank/alpha、合并 |
| 量化 | ⭐⭐⭐⭐ | ❌ | INT8/INT4、GPTQ/AWQ、KV Cache 量化、精度损失 |

---

## 二、源码阅读路线

### Spring 源码阅读顺序
1. **入门**：BeanFactory vs ApplicationContext、Bean 生命周期概览
2. **核心**：BeanDefinition 加载（XmlBeanDefinitionReader）、Bean 实例化（createBean）、依赖注入（populateBean）
3. **进阶**：AOP 代理创建（AbstractAutoProxyCreator）、拦截器链（ReflectiveMethodInvocation）
4. **高级**：事务管理（TransactionInterceptor）、循环依赖（三级缓存）、事件机制

### Vue3 源码阅读顺序
1. **入门**：项目结构（packages/）、monorepo、构建流程
2. **响应式**：reactivity/src/（ref、reactive、effect、track、trigger）
3. **运行时**：runtime-core/src/（component、renderer、vnode、scheduler）
4. **编译器**：compiler-core/src/（parse、transform、generate、codegen）
5. **整合**：createApp 启动流程、首次渲染、更新流程

### MyBatis 源码阅读顺序
1. **入门**：SqlSessionFactoryBuilder、SqlSessionFactory、SqlSession
2. **核心**：Configuration、MapperProxy（动态代理）、MapperMethod
3. **执行**：Executor、StatementHandler、ParameterHandler、ResultSetHandler
4. **插件**：Interceptor、InterceptorChain、四大对象拦截点
5. **高级**：一级/二级缓存、延迟加载、动态 SQL 解析

---

## 三、拆解深度选择指南

| 深度 | 适用场景 | 原理要求 | 源码要求 | 问题数量 |
|------|---------|---------|---------|---------|
| L2 进阶 | 入门概念、工具用法 | 基本机制说明 | 不要求 | ≥2 |
| L3 高级 | 核心概念、生产使用 | 架构设计+工作流程 | 核心片段 | ≥4 |
| L4 专家 | 面试高频、原理研究 | 完整机制+设计决策 | 关键模块源码 | ≥5 |
| L5 资深 | 架构设计、源码贡献 | 深度源码+对比方案 | 多模块源码 | ≥6 |

**选择规则**：
- 用户未指定深度时，默认 L3 高级
- 面试相关概念 → L4 专家
- 工具/框架入门 → L2 进阶
- 用户明确要求"源码级"→ L4 或 L5
- 概念难度为 ⭐⭐⭐⭐ 及以上 → 至少 L3
