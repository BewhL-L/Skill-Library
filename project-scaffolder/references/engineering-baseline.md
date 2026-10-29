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

验收：随便提交一个语法错误，CI 必须红。

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

验收：`git ls-files | grep 私有文件名` 无输出；CI 里有对应断言。

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

## 4. 反模式：假完备

生成时最容易产出"看起来有、实际没用"的东西。以下五种，出现任一即为不合格：

| 反模式 | 症状 | 检查 |
|---|---|---|
| 死配置 | 配置项只有定义、无人读取 | `grep 配置名` 全仓 |
| 零调用模块 | 缓存/工具类写好了但没人 import | `grep "import 模块名"` |
| 假 TTL | `set(key, v, ttl)` 的 ttl 未实现 | 写"等 2 秒再取"的用例 |
| 未接线能力 | 接口/页面都在，主链路不经过 | 从入口顺调用链 |
| 空实现 | 函数返回 `pass` / `TODO` | `grep -rn "TODO\|NotImplemented"` |

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
