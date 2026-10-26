# 6 大领域常见问题排查速查与工具速查

> 供 bug-troubleshooter 排查问题时参考，按领域查找常见问题的原因和排查关键点。

---

## 一、Java / Spring 方向

| 问题 | 常见原因 | 排查关键点 |
|------|---------|-----------|
| NullPointerException | 对象未初始化、空指针调用链 | 看堆栈行号，检查该对象的赋值路径 |
| OutOfMemoryError | 内存泄漏、堆太小、大对象 | jmap dump → MAT 分析 → 找大对象/泄漏点 |
| StackOverflowError | 递归调用、循环依赖 | 看堆栈是否重复出现相同方法 |
| ClassNotFoundException | 依赖缺失、版本冲突、类加载器问题 | mvn dependency:tree，检查 jar 包 |
| BeanCreationException | Bean 定义错误、循环依赖、属性注入失败 | 看 Caused by，找到真正出错的 Bean |
| 事务不生效 | 自调用、非 public、异常被 catch、传播级别 | 检查方法调用方式、异常类型、代理是否生效 |
| 循环依赖 | 构造器注入、多例 Bean、AOP 代理 | 看报错中的 Bean 链，改为 setter 注入 |
| 接口超时 | 慢 SQL、下游服务慢、线程池满、GC | 看调用链，定位最慢的环节 |

**JVM 排查工具**：
| 工具 | 用途 | 常用命令 |
|------|------|---------|
| jstack | 线程堆栈 | `jstack <pid> > thread.txt` |
| jmap | 内存 dump | `jmap -dump:format=b,file=heap.hprof <pid>` |
| jstat | GC 统计 | `jstat -gcutil <pid> 1000 10` |
| Arthas | 在线诊断 | `dashboard`、`thread -n 3`、`trace` |
| MAT | 堆内存分析 | 分析 dump 文件，找内存泄漏 |

---

## 二、前端方向

| 问题 | 常见原因 | 排查关键点 |
|------|---------|-----------|
| 响应式不生效 | 解构丢失、替换整个对象、ref 未 .value | 检查是否用了 reactive 解构、是否直接赋值 |
| 内存泄漏 | 定时器未清除、事件监听未移除、闭包引用 | 组件卸载时清理所有副作用 |
| 白屏 | JS 报错、路由配置错、资源加载失败 | 看控制台报错、Network 面板 |
| 构建失败 | 依赖版本冲突、TypeScript 类型错误、配置错 | 看构建日志第一个错误 |
| HMR 不生效 | 组件名不规范、边界问题、状态不可保留 | 检查组件是否有 name、是否在边界内 |
| 样式不生效 | 选择器优先级、scoped 限制、CSS 加载顺序 | 检查元素计算样式、看是否被覆盖 |
| 跨域错误 | 后端未配置 CORS、代理配置错 | 检查响应头 Access-Control-Allow-Origin |
| 性能卡顿 | 大列表未虚拟化、频繁重渲染、计算属性滥用 | Performance 面板分析、Vue Devtools |

---

## 三、Python / FastAPI 方向

| 问题 | 常见原因 | 排查关键点 |
|------|---------|-----------|
| ImportError | 路径问题、依赖缺失、循环导入 | 检查 sys.path、requirements.txt、导入链 |
| 异步阻塞 | 在 async 路由中调用同步阻塞函数 | 检查是否有 time.sleep/requests 等同步调用 |
| 连接池耗尽 | 慢查询占连接、连接未释放、配置太小 | 检查连接数、慢查询、连接释放 |
| 内存泄漏 | 全局变量累积、大对象未释放、循环引用 | tracemalloc、objgraph 分析 |
| 500 错误 | 未捕获异常、参数校验失败、依赖注入错误 | 看日志完整堆栈、检查 Pydantic 模型 |
| 性能差 | 同步阻塞、未用连接池、N+1 查询、未缓存 | 定位瓶颈、改用异步/连接池/缓存 |
| 部署失败 | 端口被占、权限不足、依赖版本不兼容 | 看启动日志、检查端口/权限/版本 |

---

## 四、AI 应用方向

| 问题 | 常见原因 | 排查关键点 |
|------|---------|-----------|
| LLM 调用超时 | 网络问题、模型过载、prompt 太长 | 检查 API 状态、缩短 prompt、增加超时 |
| 回答不相关 | 检索质量差、prompt 设计差、上下文不够 | 检查检索结果、优化 prompt、增加上下文 |
| 幻觉 | 上下文不足、模型编造、prompt 未约束 | 增加检索结果、要求引用来源、降低 temperature |
| Agent 死循环 | 工具调用失败、规划能力不足、终止条件不清 | 检查工具返回、优化 prompt、加最大轮次 |
| Embedding 报错 | 文本超长、API key 无效、模型不支持 | 检查文本长度、API 配置、模型文档 |
| 向量检索不准 | 切分策略差、Embedding 模型不匹配、索引参数 | 检查 Chunk 质量、换 Embedding 模型、调索引参数 |
| 成本过高 | 未缓存、prompt 过长、频繁调用、用了贵模型 | 加缓存、优化 prompt、批量调用、换便宜模型 |
| 速率限制 | 调用太频繁、未做限流、API 配额不足 | 加限流/重试、检查配额、升级套餐 |

---

## 五、数据库方向

| 问题 | 常见原因 | 排查关键点 |
|------|---------|-----------|
| 慢查询 | 索引失效、全表扫描、锁等待、数据量过大 | EXPLAIN 看执行计划、检查索引使用 |
| 死锁 | 事务顺序不一致、索引间隙锁 | SHOW ENGINE INNODB STATUS 看死锁日志 |
| 连接池满 | 慢查询占连接、连接泄漏、配置太小 | SHOW PROCESSLIST、检查连接释放 |
| 主从延迟 | 大事务、DDL、从库性能差、网络 | SHOW SLAVE STATUS、看 Seconds_Behind_Master |
| 索引失效 | 函数/运算、隐式转换、前导模糊、OR 条件 | EXPLAIN 看 type、key、rows |
| 数据不一致 | 主从延迟、事务隔离、并发更新、缓存不一致 | 检查主从状态、事务隔离级别、缓存更新策略 |
| Redis 慢 | 大 key、热 key、持久化阻塞、内存满 | slowlog、bigkeys、hotkeys、info memory |
| Redis 缓存问题 | 穿透/击穿/雪崩、缓存不一致、内存淘汰 | 检查缓存策略、加布隆过滤器/互斥锁/过期时间 |

---

## 六、运维 / Linux 方向

| 问题 | 常见原因 | 排查关键点 |
|------|---------|-----------|
| CPU 过高 | 死循环、频繁 GC、计算密集、挖矿进程 | top/htop 看进程、jstack 看线程 |
| 内存过高 | 内存泄漏、缓存过大、大对象、配置不当 | free -h、jmap、MAT 分析 |
| 磁盘满 | 日志未清理、大文件、core dump、镜像堆积 | df -h、du -sh、找大文件 |
| IO 高 | 频繁读写、日志太多、数据库慢、交换分区 | iostat、iotop、检查日志/数据库 |
| 网络不通 | 防火墙、端口未开、DNS、路由、代理 | ping、telnet、traceroute、检查防火墙 |
| 连接数过多 | TIME_WAIT 堆积、连接未释放、配置太小 | ss -s、检查连接释放、调内核参数 |
| 服务启动失败 | 端口被占、权限不足、配置错、依赖缺失 | 看启动日志、检查端口/权限/配置/依赖 |
| Docker 容器退出 | 应用崩溃、OOM、配置错、健康检查失败 | docker logs、docker inspect、检查 OOM |

---

## Linux 排查工具速查

| 工具 | 用途 | 常用命令 |
|------|------|---------|
| top/htop | 进程资源 | `top -c`、`htop` |
| iostat | IO 统计 | `iostat -xz 1` |
| vmstat | 内存/CPU | `vmstat 1` |
| ss/netstat | 网络连接 | `ss -tlnp`、`netstat -anp` |
| tcpdump | 抓包 | `tcpdump -i any port 8080 -w cap.pcap` |
| dstat | 综合统计 | `dstat -cdlmnpsy` |
| free | 内存 | `free -h` |
| df/du | 磁盘 | `df -h`、`du -sh *` |
| journalctl | 系统日志 | `journalctl -u service-name -f` |
| docker | 容器 | `docker logs`、`docker stats`、`docker inspect` |

---

## 数据库排查工具速查

| 工具 | 用途 | 常用命令 |
|------|------|---------|
| EXPLAIN | 执行计划 | `EXPLAIN SELECT ...` |
| slow log | 慢查询 | `SHOW VARIABLES LIKE 'slow%'` |
| PROCESSLIST | 当前连接 | `SHOW FULL PROCESSLIST` |
| INNODB STATUS | InnoDB 状态 | `SHOW ENGINE INNODB STATUS` |
| redis-cli | Redis 诊断 | `SLOWLOG GET 10`、`INFO memory`、`BIGKEYS` |
| mycli | MySQL 客户端 | 带语法高亮和自动补全 |
| percona-toolkit | MySQL 工具集 | pt-query-digest、pt-deadlock-logger |
