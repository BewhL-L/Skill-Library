# 工程底座六件套（生成时就装上，不要事后补）

> 这份清单解决一个具体问题：AI 生成的项目**功能齐全但底座缺失**——
> 能跑、能演示，一改结构就崩，一上线就出事，面试一问"怎么发布"就卡住。
> 六件套的共同特征：**10 年不过时，且能在 1 天内装完**。

## 目录

1. 判断标准：什么算"底座"
2. 六件套总表
3. 每件的最小实现与验收命令
4. 反模式：假完备
5. 在生成流程中的插入位置
6. 交付前 checklist

---

## 1. 判断标准：什么算"底座"

一个能力算底座，要同时满足三条：

1. **换框架也还在**：不是某个库的特性，而是工程共识（迁移、索引、CI、日志）；
2. **缺了会出事**：不是"更好"，而是"迟早翻车"（改表结构、并发、密钥泄漏）；
3. **能自动验证**：装完有命令能证明它在工作。

按这三条筛，绝大多数"热门技术"不入选——它们是表层，1-3 年就换。

## 2. 六件套总表

| # | 底座 | 缺失后果 | 最小实现 | 验收命令 |
|---|---|---|---|---|
| 1 | 版本化 schema | 改表靠手写脚本，线上无法回滚 | Alembic baseline + `db_bootstrap.py` | `alembic upgrade head` 空库建全 |
| 2 | 索引 | 数据一多就全表扫，P95 崩 | 外键列 + 高频查询复合索引 | `EXPLAIN` 出现 `SEARCH` 而非 `SCAN` |
| 3 | 质量门 | 代码能跑但不敢改 | lint + test + build + 镜像 | CI 四门全绿 |
| 4 | 文档断言 | 文档与代码脱节，误导使用者 | `check_docs.py` 进 CI | 改错一个数字，CI 变红 |
| 5 | 私有边界 | 私有文档/密钥进公开仓库 | `.gitignore` + `git ls-files` 断言 | 私有文件被跟踪时 CI 红 |
| 6 | 生产默认安全 | 演示配置直接上线 | 关自动建表、关互操作、令牌校验 | 关掉开关后接口返回 503/404 |

## 3. 每件的最小实现与验收命令

### 3.1 版本化 schema

```bash
alembic init migrations          # 只做一次
alembic revision --autogenerate -m "baseline"
alembic upgrade head
```

配套 `scripts/db_bootstrap.py` 处理三种库：空库建全 / 老库 `stamp` / 已纳管升级。
应用侧把 `AUTO_CREATE_TABLES` 默认设为 `false`——**create_all 只建缺失的表，不会改已有表结构**，留着它只会掩盖迁移缺失。

验收：空库一条命令建出全部表；迁移本身有测试（`test_migrations.py`）。

### 3.2 索引

不是"给所有列加索引"，而是按查询建：

```sql
-- 真实查询：WHERE kb_id = ? AND status = ? ORDER BY created_at DESC
CREATE INDEX ix_docs_kb_status_created ON documents(kb_id, status, created_at);
```

**把排序列放进索引**，否则过滤走索引、排序还要建临时 B 树。
验收：`EXPLAIN QUERY PLAN` 从 `SCAN` 变 `SEARCH`，且不再出现 `USE TEMP B-TREE FOR ORDER BY`。

### 3.3 质量门（CI）

四道门，缺一不可：

```yaml
- ruff check .            # 静态检查：能抓 undefined name 这类真 bug
- python -m pytest -q     # 必须用 -m，console script 不会把 CWD 加进 sys.path
- npm run build           # 含类型检查
- docker build            # 镜像能构建，才证明 Dockerfile 没坏
```

**结果以机器可读产物为准，不要读终端**：

```bash
python -m pytest -q --junitxml=.pytest/junit.xml
grep -o 'tests="[0-9]*" [^>]*' .pytest/junit.xml      # tests / failures / errors 三个数
```

终端摘要行和退出码都可能被环境改写——实测过一次"118 条用例全绿、退出码却是 1"
（终端插件抢先接管输出，吞掉了摘要行并重写了退出码）。只看退出码会把"通过"判成失败，
只看被截断的摘要又会把"失败"当成通过。把 junit 里的三个数当唯一判据，
顺带让"通过"这件事有了可归档的物证。

验收：随便提交一个语法错误，CI 必须红。

> 分工：本节只给 CI 判据。文档里那些 `N passed` 该怎么产生、改完怎么同步，
> 见 `project-processization/references/05-文档一致性与防漂移.md`「数字从哪来」（仅在已安装该 Skill 时可用）。
> 两边不要各维护一份阈值与取数逻辑。

### 3.4 文档断言

四类断言：测试数量、路径存在、废弃表述、私有文件（可选加接口清单）。

**脚本来源（避免两份漂移）**：

| 情况 | 做法 |
|---|---|
| 已安装 `project-processization` | 直接复制其 `scripts/check_docs.py`，**不改逻辑**；上游改了再同步 |
| 未安装 | 自实现最小版（标准库，约 80 行），只做四类断言 |

> 复制后允许追加**一段项目本地配置**（废弃表述清单、私有文件清单、默认根目录），
> 但**校验逻辑不要改**。上游修掉的问题——例如 `POST /api/x` 这种带方法前缀的接口引用
> 曾被整类跳过——才能靠一次 diff 回灌到所有项目；逻辑各改各的，两份脚本会悄悄分叉。

最小版实现要点：

1. 测试数：`ast` 解析 `tests/**/test_*.py` 的 `def test_`，模块级 `pytestmark = pytest.mark.skip` 的计入总数不计入 passed；
2. 路径：抓文档里反引号包裹的 `backend/ frontend/ docker/ .github/ scripts/` 路径，逐个 `exists()`（`scripts/x.py` 兼容 `backend/scripts/x.py`）；
3. 废弃表述：黑名单 grep（旧目录名、旧字段名、旧数字）；
4. 私有文件：`git ls-files` 结果里不得出现 `*指导书*.md`、`.env`、`*.db`。

验收：**反向验证**——故意把测试数改错一位，脚本必须报错。

> 适用范围：本项与语言无关；除它之外的 `index` / `defaults` / `deadconfig` 只对 Python 生效。

### 3.5 私有边界

```gitignore
# 私有文档
项目学习指导书.md
# 密钥
.env
```

```python
# check_docs.py 内：只查已跟踪文件，本地存在但被忽略的不算
tracked = subprocess.run(["git", "ls-files"], ...).stdout.splitlines()
```

**禁止 `git add -A`**：它是私有文档误入仓库的头号入口。提交前先 `git status --short`。

**提交粒度**：一个模块一条提交（`feat(retrieval): …` / `chore(deploy): …`），不要攒一周的改动压成一条 `init`。判断标准是"这条能不能单独 revert、单独讲清楚"——不能，就该拆。

**从约定到闸门**：`.gitignore` 与"提交前看一眼 status"都依赖人记得——漏一次就是 2026-10-27 那种事故。给仓库装 `secret-gate` 技能的 pre-commit 钩子（`bash <skill-dir>/secret-gate/scripts/install-hook.sh .`），`.env`、私钥块、`user:pass@host` 形式的内嵌凭据会在提交那一刻被直接拒绝，工作区文件原样保留。把"禁止 `git add -A`"从口号变成可执行的检查。

验收：`git ls-files | grep 私有文件名` 无输出；CI 里有对应断言。闸门验收：暂存一个假密钥（运行时拼接的 `sk-` 加 30 个字符），`git commit` 必须红。

### 3.6 生产默认安全

| 开关 | 默认值 | 原因 |
|---|---|---|
| `AUTO_CREATE_TABLES` | `false` | 强制走迁移 |
| `A2A_ENABLED`（互操作） | `false` | 开放即等于把知识库暴露给任意调用方 |
| 危险工具 | 白名单 + 超时 | 模型可能被注入诱导调用 |
| 令牌比较 | 常量时间 | 防时序侧信道 |

验收：关掉开关，对应接口返回 503/404，而不是"静默降级为可用"。

### 3.7 容器编排约定

生成 `docker-compose.yml` 时按这四条写，能避开三类"不报错"的坑：

| 约定 | 写法 | 原因 |
|---|---|---|
| 不设 `container_name` | 留空，用 Compose 生成的 `<项目>-<服务>-<序号>` | 写死了就无法 `--scale`，也不能用另一个项目名并排跑 dev/prod |
| 端口绑回环 | `"127.0.0.1:5432:5432"` | 裸写 `"5432:5432"` 是对全网卡暴露，而 Postgres/Redis/Qdrant 默认都没鉴权 |
| 被依赖服务必须有 healthcheck | `depends_on: {db: {condition: service_healthy}}`，且 `db` 里确有 `healthcheck` | 缺 healthcheck 时 Compose 直接报 `container xxx has no healthcheck configured`；只写 `service_started` 等于"进程起了就算就绪" |
| bind mount 前先校验路径 | 启动脚本断言 `.env` 是**文件**、`uploads/data` 是**目录** | 源路径不存在时 Docker 会静默建空目录：`.env` 变目录会让 `env_file` 报 `is a directory`，数据目录变空目录则完全无报错，表现为"上传的文件消失" |

验收：`docker compose config` 通过；`docker compose up -d` 后 `docker compose ps` 全部显示 `(healthy)`。

### 3.8 装了却没通电：四类静默失败

六件套的失效方式，主要不是"缺"，而是**装了没生效**。这类 bug 的共同特征：
**测试全绿、日志无错、接口返回 200**，只在换一种配置、换一个数据量、换一条退出路径时才失效。

#### ① 绕过统一入口（配置维度失效）

| 项 | 内容 |
|---|---|
| 症状 | 开发环境一切正常；把 `VECTOR_PROVIDER` 从 `chroma` 改成 `qdrant`（或反之）后，该模块返回空结果，接口 200，日志一行不报 |
| 根因 | 模块顶层写了 `from ..services.vector_store import vector_store`，拿到的是**导入那一刻**构造好的实例；工厂 `get_vector_store()` 里对配置的分支判断被整段绕过 |
| 关键判断 | 同一个错误在两个以上文件里出现，说明缺的不是那几行 import，而是**"唯一入口"这条约束**——修法是立规矩，不是补代码 |
| 验收 | ①`grep -rn "^from .*services.* import [a-z_]*_store$" app/` 应为**空**——业务代码只 import 工厂 `get_*`（遗留单例若还要兼容旧调用，就地注明"禁止新增引用"，并只允许测试引用）；②补一条"改 provider 后工厂返回类型随之变化"的用例 |

```python
# ✗ 模块级单例：配置改了，这里永远拿旧实例
from ..services.vector_store import vector_store

# ✓ 工厂：每次按当前配置取
from ..services.vector_store import get_vector_store
store = get_vector_store()
```

> 这条最值得单独记：它让"六件套里的配置项"变成死配置——`.env` 里改了、代码里没读，
> 而 §4 的 `grep 配置名` 又能搜到读取处，于是静态检查也放过它。

#### ② 用绝对数值当门槛（数据量维度失效）

| 项 | 内容 |
|---|---|
| 症状 | 小语料 / 空库时召回恒为空；灌够数据后自己"恢复"，本地难以复现 |
| 根因 | BM25 的 IDF 是 `log(1 + (N-n+0.5)/(n+0.5))`，**分数量级随语料规模变化**：小语料里查询词几乎"出现在全部 chunk"，n≈N，idf 被压到 0.05~0.29；写死 `score >= 0.5` 就把结果全过滤了 |
| 反向同样成立 | 语料变大后同一个词可能只在少数 chunk 出现，idf 升到 1~4，0.5 的门槛又形同虚设——**同一个数字在小语料上误杀、在大语料上失效**，这才是"绝对阈值"真正的问题 |
| 正确写法 | 相对门槛，并取"绝对与相对的较小值"，保证 top1 永不被误杀 |
| 可证不变量 | `floor = min(ABS_MIN, top × RATIO)` ⇒ `floor ≤ RATIO × top < top`（RATIO<1），所以最高分那条一定留下 |

实测（K1=1.5、B=0.75，查询词在全部 chunk 各出现 1 次，数据来自真实实现）：

| 语料 chunk 数 | 1 | 2 | 3 | 5 | 10 |
|---|---|---|---|---|---|
| 单次命中分 | 0.2877 | 0.1823 | 0.1335 | 0.0870 | 0.0465 |
| 纯绝对值 0.5 判定 | 杀掉 | 杀掉 | 杀掉 | 杀掉 | 杀掉 |
| `min(0.5, 0.25×top)` | 0.0719 | 0.0456 | 0.0334 | 0.0218 | 0.0116 |

注意分数随语料变大反而**下降**（因为 n 跟着 N 一起涨），"数据越少分越高"是反直觉的错误假设。

```python
if scored:
    top = max(s for s, _ in scored)
    floor = min(settings.BM25_MIN_SCORE, top * settings.BM25_MIN_SCORE_RATIO)
    scored = [(s, d) for s, d in scored if s >= floor]
```

验收：把阈值参数临时调到极大（如 999），断言 top1 **仍然**在结果里。这条用例必须能红——
把实现改回纯绝对值它就得失败，否则等于没测。

#### ③ 加了启动期校验，没回头改快速开始（文档维度失效）

| 项 | 内容 |
|---|---|
| 症状 | CI 绿、单测绿；新人按 README 三条命令跑，第一步就崩 |
| 根因 | 校验加在代码里是对的，但 `.env.example` 里仍是占位值（`SECRET_KEY=change-me`），而新校验恰好拒绝占位值。**加校验的人知道要改，读文档的人不知道** |
| 验收 | 把快速开始命令**逐条复制到空目录实跑一遍**；或加一个 CI job 用 `.env.example` 起服务并探活 |

配套动作固定成三步，缺一步就是制造 ③：加校验 → 改 `.env.example`（标注必填 + 给出生成命令）→ 改快速开始。

#### ④ 异常只 catch 了一半（退出路径维度失效）

| 项 | 内容 |
|---|---|
| 症状 | 正常报错有兜底；用户关页面 / 断连 / 点取消时，库里留下半条记录（有提问、回答为空） |
| 根因 | `asyncio.CancelledError` 继承 `BaseException` 而非 `Exception`，`except Exception` 抓不到；流式接口的断开正是以它表现的 |
| 写法 | 先兜底、再上抛，**不要吞掉取消** |
| 验收 | 写一条"生成过程中取消协程"的用例，断言落库记录不是空回答 |

```python
except asyncio.CancelledError:
    _persist_stream_failure(message_id, partial, sources_data)   # 落已生成的部分
    raise                                                        # 取消必须向上传播
except Exception as e:
    _persist_stream_failure(message_id, partial, sources_data)
    logger.exception("stream failed: %s", e)
```

**一句话自检**：这段代码在**另一种配置 / 另一种数据量 / 另一条退出路径**下还成立吗？
三种里只要有一种没测过，就等于没测——因为线上出事的总是那一种。

## 4. 反模式：假完备

生成时最容易产出"看起来有、实际没用"的东西。以下七种，出现任一即为不合格：

| 反模式 | 症状 | 检查 |
|---|---|---|
| 死配置 | 配置项只有定义、无人读取 | `grep 配置名` 全仓 |
| 零调用模块 | 缓存/工具类写好了但没人 import | `grep "import 模块名"` |
| 假 TTL | `set(key, v, ttl)` 的 ttl 未实现 | 写"等 2 秒再取"的用例 |
| 未接线能力 | 接口/页面都在，主链路不经过 | 从入口顺调用链 |
| 空实现 | 函数返回 `pass` / `TODO` | `grep -rn "TODO\|NotImplemented"` |
| 配置旁路 | 工厂函数写着，业务代码却直接 import 单例 | `grep -rn "^from .* import .*_store" app/` 命中工厂外即不合格（见 3.8 ①） |
| 绝对阈值 | 门槛是固定数字，而分数尺度随数据量变化 | 把阈值调到极大，看 top1 是否仍返回（见 3.8 ②） |

**生成阶段就要避免**：要么接线，要么标注"旁路可用"，不要假装它在主链路里。

## 5. 在生成流程中的插入位置

| 时机 | 动作 |
|---|---|
| 第二步（产物规划） | 把六件套写进 WBS，标注为 P0（不是"后续优化"） |
| 第三步（生成产物） | 数据库/CI/脚本随代码一起生成，不留 TODO |
| 第六步（自检） | 用命令逐项验收，不靠"看起来有" |
| 第七步（Git 初始化） | `.gitignore` 含私有文档；提交前 `git status` 安全检查 |

## 6. 交付前 checklist

- [ ] `alembic upgrade head` 能在空库建全；迁移有测试
- [ ] 高频查询有复合索引，`EXPLAIN` 不是 `SCAN`
- [ ] CI 四门可跑（lint / test / build / docker）
- [ ] `check_docs.py` 在 CI 里，且做过反向验证
- [ ] `.gitignore` 含私有文档与 `.env`；`git ls-files` 干净
- [ ] `AUTO_CREATE_TABLES=false`；互操作能力默认关闭
- [ ] 无死配置、零调用模块、假 TTL、未接线能力
- [ ] 业务代码不直接 import 单例；改 provider / 改开关有对应用例（3.8 ①）
- [ ] 数值门槛是相对的，且有"top1 永不被过滤"的用例，且这条用例能红（3.8 ②）
- [ ] 快速开始按文档逐条实跑过，不只是"CI 绿"（3.8 ③）
- [ ] 流式 / 异步接口同时兜住 `Exception` 与 `CancelledError`，取消时也能落库（3.8 ④）
- [ ] 测试结论取自 `--junitxml` 产物，不依赖终端摘要行与退出码
