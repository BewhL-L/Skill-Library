# 三大技术栈源码阅读重点与阅读路线

> 供 source-code-reader 阅读源码时参考，按对应技术栈的阅读重点和路线执行。

---

## 源码阅读五步法详解

### 第一步：准备阶段（30分钟）
- 明确阅读目标（学习什么、解决什么问题）
- 搭建阅读环境（克隆代码、导入 IDE、能编译运行）
- 了解项目背景（官方文档、架构图、核心概念）
- 找到入口点（main 函数、启动类、配置文件）

### 第二步：宏观架构（1-2小时）
- 画出整体架构图（分层、模块、核心类）
- 理解模块划分和职责
- 梳理核心数据流（从输入到输出的完整链路）
- 识别核心接口和抽象层

### 第三步：核心流程（2-4小时）
- 选择 1-2 个核心流程深入阅读
- 画出时序图/调用链
- 理解每个步骤的作用和实现
- 关注设计模式和关键数据结构

### 第四步：细节深入（4-8小时）
- 深入核心类和关键方法
- 理解算法实现和性能优化
- 关注异常处理和边界条件
- 对比不同实现方式的优劣

### 第五步：总结输出（1-2小时）
- 整理架构图和时序图
- 撰写源码阅读笔记（按模板）
- 提炼设计思想和最佳实践
- 与知识库笔记关联（添加 [[]] 双链）

---

## 技术栈1：Java / Spring 源码

### Spring Framework 核心阅读路线

| 阶段 | 阅读内容 | 核心类 | 学习目标 |
|------|---------|--------|---------|
| 1. IoC 容器 | Bean 定义、加载、实例化、依赖注入 | BeanFactory、ApplicationContext、BeanDefinition、DefaultListableBeanFactory | 理解 IoC 原理、Bean 生命周期 |
| 2. AOP | 代理创建、切点匹配、通知执行 | JdkDynamicAopProxy、CglibAopProxy、Advisor、Pointcut | 理解动态代理、AOP 实现原理 |
| 3. 事务 | 事务传播、事务管理、回滚机制 | TransactionInterceptor、PlatformTransactionManager、TransactionAttribute | 理解事务原理、传播行为 |
| 4. MVC | 请求处理、参数解析、视图渲染 | DispatcherServlet、HandlerMapping、HandlerAdapter、ViewResolver | 理解 MVC 流程、请求处理 |
| 5. Boot 自动配置 | 条件装配、自动配置、Starter | @EnableAutoConfiguration、AutoConfigurationImportSelector、Condition | 理解自动配置原理、Starter 机制 |

### Spring 源码阅读重点

**IoC 核心流程**：
1. 资源加载：`ResourceLoader` 加载配置文件
2. Bean 定义解析：`BeanDefinitionReader` 解析为 `BeanDefinition`
3. Bean 定义注册：`BeanDefinitionRegistry` 注册到容器
4. Bean 实例化：`createBean()` 通过反射创建实例
5. 属性填充：`populateBean()` 注入依赖
6. 初始化：`initializeBean()` 执行初始化方法
7. 销毁：`destroyBean()` 执行销毁方法

**关键设计模式**：
- 工厂模式：BeanFactory
- 模板方法：AbstractApplicationContext
- 观察者模式：ApplicationEvent
- 策略模式：InstantiationStrategy
- 代理模式：AOP 动态代理
- 责任链：HandlerInterceptor

### MyBatis 源码阅读路线

| 阶段 | 阅读内容 | 核心类 |
|------|---------|--------|
| 1. 配置解析 | XML 解析、配置构建 | XMLConfigBuilder、Configuration |
| 2. SqlSession | 会话创建、执行器 | SqlSessionFactory、DefaultSqlSession、Executor |
| 3. Mapper 代理 | 接口代理、方法映射 | MapperProxyFactory、MapperProxy、MapperMethod |
| 4. SQL 执行 | 参数处理、SQL 执行、结果映射 | StatementHandler、ParameterHandler、ResultSetHandler |
| 5. 插件 | 拦截器、责任链 | Interceptor、InterceptorChain、Plugin |

---

## 技术栈2：Vue3 源码

### Vue3 核心阅读路线

| 阶段 | 阅读内容 | 核心模块 | 学习目标 |
|------|---------|---------|---------|
| 1. 响应式系统 | ref、reactive、effect、computed | @vue/reactivity | 理解响应式原理、依赖收集 |
| 2. 运行时核心 | 虚拟 DOM、组件、渲染 | @vue/runtime-core | 理解组件系统、渲染流程 |
| 3. 编译器 | 模板编译、AST、优化 | @vue/compiler-core | 理解编译原理、PatchFlag |
| 4. 运行时 DOM | DOM 操作、属性更新 | @vue/runtime-dom | 理解 DOM diff、事件处理 |
| 5. 应用入口 | createApp、插件、全局 API | vue | 理解应用启动、插件机制 |

### Vue3 源码阅读重点

**响应式系统核心流程**：
1. `reactive()`：通过 Proxy 拦截 get/set
2. `effect()`：创建副作用函数，首次执行触发依赖收集
3. 依赖收集：get 时 `track()` 收集 effect 到 dep
4. 触发更新：set 时 `trigger()` 执行 dep 中的 effect
5. `ref()`：对基本类型的封装，通过 `.value` 访问
6. `computed()`：缓存计算结果，依赖变化时重新计算

**渲染流程核心**：
1. `createApp()`：创建应用实例
2. `mount()`：挂载根组件
3. `render()`：渲染虚拟 DOM
4. `patch()`：对比新旧 VNode，执行更新
5. `diff()`：同层比较，优化更新（最长递增子序列）
6. `unmount()`：卸载组件，执行清理

**关键优化点**：
- PatchFlag：静态标记，精准更新
- Block Tree：动态节点收集，跳过静态节点
- 静态提升：静态节点提升到渲染函数外
- 缓存事件处理函数：避免重复创建
- 最长递增子序列：优化 DOM 移动

---

## 技术栈3：Python / FastAPI / LangChain 源码

### FastAPI 源码阅读路线

| 阶段 | 阅读内容 | 核心类 | 学习目标 |
|------|---------|--------|---------|
| 1. 应用创建 | FastAPI 类、路由注册 | FastAPI、APIRouter、Route | 理解应用结构、路由机制 |
| 2. 依赖注入 | 依赖解析、参数注入 | Depends、Dependant、solve_dependencies | 理解依赖注入原理 |
| 3. 请求处理 | 请求解析、参数验证、响应生成 | Request、Response、RequestValidationError | 理解请求处理流程 |
| 4. Pydantic 集成 | 数据验证、序列化 | BaseModel、Field、validator | 理解数据验证机制 |
| 5. 异步支持 | 异步路由、后台任务 | async def、BackgroundTasks | 理解异步处理 |

### FastAPI 核心流程

1. **应用启动**：`FastAPI()` 创建应用，`include_router()` 注册路由
2. **路由匹配**：请求到达，`Router` 匹配路径和方法
3. **依赖解析**：`solve_dependencies()` 递归解析所有 `Depends`
4. **参数验证**：Pydantic 验证请求参数（路径、查询、请求体）
5. **端点执行**：调用路由处理函数（同步/异步）
6. **响应序列化**：Pydantic 序列化响应数据
7. **响应返回**：返回 Response 对象

### LangChain 源码阅读路线

| 阶段 | 阅读内容 | 核心类 | 学习目标 |
|------|---------|--------|---------|
| 1. 核心抽象 | Chain、LLM、Prompt、Memory | Chain、BaseLLM、PromptTemplate、BaseMemory | 理解核心抽象和设计 |
| 2. LLM 封装 | 模型调用、流式、批处理 | OpenAI、ChatOpenAI、LLMResult | 理解 LLM 调用封装 |
| 3. Chain 组合 | 顺序链、路由链、转换链 | SequentialChain、RouterChain、TransformChain | 理解 Chain 组合机制 |
| 4. Agent | 规划、工具调用、执行 | Agent、Tool、AgentExecutor | 理解 Agent 核心循环 |
| 5. Retriever | 文档加载、切分、向量化、检索 | Document、TextSplitter、VectorStore、Retriever | 理解 RAG 检索流程 |

### LangChain 核心设计

**Chain 核心抽象**：
- `Chain`：所有链的基类，定义 `run()`、`call()`、`acall()` 接口
- `input_keys` / `output_keys`：声明输入输出键
- `_call()`：子类实现的核心逻辑
- `SequentialChain`：按顺序执行多个 Chain
- `RouterChain`：根据输入选择不同的 Chain

**Agent 核心循环**：
1. 规划：LLM 根据问题和可用工具，决定下一步行动
2. 行动：调用选定的工具，获取结果
3. 观察：将工具结果加入上下文
4. 重复：继续规划-行动-观察，直到得到最终答案
5. 终止：LLM 输出最终答案，Agent 结束

**RAG 检索流程**：
1. 文档加载：`DocumentLoader` 加载各种格式文档
2. 文档切分：`TextSplitter` 切分为 Chunk
3. 向量化：`Embeddings` 将 Chunk 转为向量
4. 存储：`VectorStore` 存储向量和原文
5. 检索：`Retriever` 根据查询检索相关 Chunk
6. 生成：将检索结果加入 Prompt，LLM 生成答案

---

## 源码阅读笔记模板

```markdown
---
title: XXX 源码阅读 - 模块名
category: 源码阅读
tags: [技术栈标签, 源码阅读]
difficulty: ⭐⭐⭐⭐
source_link: https://github.com/XXX
read_date: YYYY-MM-DD
---

# XXX 源码阅读 - 模块名

## 阅读目标
- 学习什么：XXX
- 解决什么问题：XXX

## 整体架构
（架构图描述或 Mermaid 图）

### 核心模块
| 模块 | 职责 | 核心类 |
|------|------|--------|
| 模块1 | XXX | ClassA |
| 模块2 | XXX | ClassB |

## 核心流程
### 流程1：XXX
（时序图描述）
1. 步骤1：XXX
2. 步骤2：XXX
3. 步骤3：XXX

### 关键代码
```python/java/typescript
// 核心代码片段，带注释
```

## 设计模式
| 模式 | 应用位置 | 作用 |
|------|---------|------|
| 模式1 | XXX | XXX |

## 关键数据结构
| 数据结构 | 作用 | 核心字段 |
|---------|------|---------|
| 结构1 | XXX | XXX |

## 性能优化点
1. XXX
2. XXX

## 关键 Takeaway
1. XXX
2. XXX
3. XXX

## 与知识库关联
- [[相关概念1]]
- [[相关概念2]]

## 实践启发
- 可以应用到项目中的点：XXX
```
