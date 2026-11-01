# `~/.hermes` 目录清单：什么要迁、什么不要

按"换机器时该不该带走"分类。脚本 `export.sh` 的层级就是按这张表设计的。

## A. 配置与自定义资产（`config` 层，必带）

| 路径 | 是什么 | 备注 |
|---|---|---|
| `config.yaml` | 主配置：模型、agent、plugins、memory、display | 1–2 KB，改错了容易起不来，优先备份 |
| `SOUL.md` | 人设/系统提示词 | 纯文本，适合版本化 |
| `channel_directory.json` | 渠道目录（IM 等） | 为空说明没接外部渠道 |
| `skills/` | 自定义技能 | 注意里面的符号链接，见文末 |
| `plugins/` | **第三方插件代码**（mem0、minions、superpowers、open-design、oh-my-hermes 等） | `config.yaml` 的 `plugins.enabled` 只是启用名单，代码在这里。默认只记录 `plugins.txt`（名称 + git sha + origin），代码按需 `--with-plugins` 复制 |
| `hooks/` | 生命周期钩子 | 空目录很常见 |
| `desktop-plugins/` | 桌面端插件 | 不含依赖的可直接带走 |
| `cron/` | 定时任务定义 | `executions.db` 是历史，可不带 |
| `.env` | 密钥与运行时开关 | **只导键名**，见 `secrets.md` |

## B. 状态与历史（`state` 层，按需）

| 路径 | 是什么 | 为什么要特殊处理 |
|---|---|---|
| `memories/` | 热记忆：`MEMORY.md`（agent 笔记）+ `USER.md`（用户画像） | 纯文本直接拷；结构与限额见下节 |
| `sessions/` | 会话记录 | 体积随时间增长 |
| `state.db` | 主状态库（5–10 MB 起） | **必须用 SQLite 在线备份**，直接 `cp` 可能拿到半写状态 |
| `kanban.db` | 看板数据 | 同上 |
| `shared-state.db` | 共享状态 | 同上 |

### `memories/` 的内部结构（决定"恢复后为什么行为没变"）

| 文件 | 内容 | 写入方 |
|---|---|---|
| `MEMORY.md` | agent 自己的笔记：环境、约定、踩过的坑 | agent 通过 `memory` 工具写，约每 10 轮被提醒整理一次 |
| `USER.md` | 用户画像：偏好、口味、明确要求 | 同上 |

格式与限额（默认值，可在 `config.yaml` 的 `memory` 段调整）：

- 条目之间用 `\n§\n`（单独一行 `§`）分隔，**不是 markdown 列表**；
- `MEMORY.md` 上限 2200 字符、`USER.md` 上限 1375 字符；**写满后拒绝新增，不截断**，超限只会在日志里 WARN；
- 会话启动时**冻结成快照**注入 system prompt，会话中途的写入只落盘、**下个会话才生效**。

另有一条与恢复直接相关的规则：**内置记忆始终启用，外部 provider（mem0 / byterover / retaindb）同一时间只能挂一个**。`config.yaml` 的 `memory.provider` 若指向未安装的插件，外部记忆等于没开（内置部分不受影响）——恢复后先看这一项，再怀疑数据。

因此两种"看起来没恢复"都是正常的：

- 恢复备份后 agent 行为没变 → 快照是旧的，新开一个会话即可；
- 记忆是空的 → 只迁了 `state.db` 而漏了 `memories/`（两者互不替代）。

## C. 代码与工具（`full` 层）

| 路径 | 是什么 | 注意 |
|---|---|---|
| `hermes-agent/` | Hermes 源码 + `.venv` | **排除 `.venv`**（绝对路径 + 平台二进制，换机必坏）；排除 `.git` 可省一半体积 |
| `installs/` | 安装记录/版本 | 小，带上便于诊断 |
| `tools/` | 内置工具脚本 | 若被本地改过则必须带 |
| `skins/` | 界面主题 | 小 |

## D. 永远不要带（可重建 / 绑定原机器）

| 路径 | 原因 |
|---|---|
| `cache/`、`image_cache/`、`audio_cache/` | 纯缓存，重建即可 |
| `sandboxes/`、`terminal-sessions/` | 会话期临时目录 |
| `backups/`、`.curator_backups/` | 旧备份，容易嵌套膨胀 |
| `source-checks/`、`telemetry/` | 校验与遥测数据 |
| `*.lock`（`.env.lock`、`auth.lock` 等） | 进程锁，带过去会阻塞启动 |
| `gateway.sock` | Unix socket，跨机器无意义 |
| `*.db-wal`、`*.db-shm` | SQLite 的临时日志，必须让数据库自己生成 |
| `node_modules/`、`__pycache__/`、`.venv/` | 与平台绑定 |

## 刻意排除，但不是"缓存"

这几个目录体积小、名字像数据，容易被误判为"该带"，实际都不带：

| 目录 | 内容 | 为什么不带 |
|---|---|---|
| `state/` | `gateway.heartbeat`、`gateway.lifecycle.json`、`gateway.loop-tick.<pid>.sock` | 进程心跳与 Unix socket，带到新机器会指向不存在的进程；新装时 Hermes 自动生成 |
| `images/` | `clip_2026xxxx.png`（对话里粘贴的截图） | 会话附件，随对话存在，不承担配置或记忆职责 |
| `kanban/` | 看板附件目录（本机为空） | 真正的数据在 `kanban.db`，目录只是附件落脚点 |
| `bot_relay/`、`desktop/`、`disk-cleanup/` | 各子系统的运行状态 | 可由运行时重建，且常含 PID/路径 |

判断标准还是同一条：**删掉后 Hermes 重启能自愈的，就不带**。`state/` 里的 socket 文件是典型反例——带过去不仅无用，还可能让进程误以为已有实例在跑。

## 符号链接

`skills/` 里若出现指向仓库外的软链（例如 `CLAUDE.md -> AGENTS.md` 这类），用 `find -type l` 能列出来。导出时脚本会写进 `symlinks.txt`，恢复后需要手工重建，否则相关技能会静默失效。

## 判断原则

1. **能重建的不带**（缓存、依赖、锁、socket）。
2. **能文本化的优先文本**（配置、记忆、任务定义），便于 diff 与版本化。
3. **数据库走 API 不走文件复制**（`sqlite3.backup()`）。
4. **密钥永不进备份包**。

## 判定流程（遇到新目录时按此走）

```
新目录 X
 ├─ 删除后 Hermes 能自行重建吗？
 │    ├─ 能（cache/、*.lock、gateway.sock、__pycache__）→ 不带
 │    └─ 不能 → 继续
 ├─ 体积是否与平台绑定（linux-x64、.venv、node_modules）？
 │    ├─ 是（tools/、.venv/）→ 不带，改为重装
 │    └─ 否 → 继续
 ├─ 是代码还是数据？
 │    ├─ 代码且是 git 仓库 → 只记 sha（plugins.txt），可选 --with-plugins
 │    ├─ 代码但非 git 仓库 → 整份复制（plugins/mem0 就是这种）
 │    └─ 数据（memories/、sessions/、*.db）→ state 层，数据库走 backup()
 └─ 决策写回本文件，并同步 SKILL.md 的层级表
```

## 各目录的"重建代价"

| 目录 | 丢了之后怎么恢复 | 代价 |
|---|---|---|
| `config.yaml` | 手工重写 | 高（几十个字段，且改错会起不来） |
| `skills/` | 从各自来源重装 | 中（自定义的无法重建） |
| `plugins/mem0` | 无上游可拉 | **不可重建** |
| 其他 `plugins/` | `git clone` + 切到 `plugins.txt` 里的 sha | 低（需网络） |
| `memories/`、`sessions/` | 无 | **不可重建** |
| `state.db`、`kanban.db` | 无 | **不可重建** |
| `hermes-agent/` | 官方安装器 | 低 |
| `installs/`、`tools/`、`skins/` | 官方安装器 / 重新下载 | 低（但耗时、耗流量） |
| `cache/`、`*-cache/` | 自动重建 | 无 |

这张表是分层设计的依据：**"不可重建"的东西必须在 `state` 及以下层级里被完整带走**。

## 与 mem0 的关系

mem0 横跨四类：

- 配置（`config.yaml`）→ 文本，`config` 层
- 代码（`plugins/mem0/`）→ 非 git，整份复制
- 密钥（`.env`）→ 只留键名
- 数据（`~/mem0/server` 的 PostgreSQL）→ 不在 `~/.hermes` 内，单独 `pg_dump`

因此它在文档里被单列一节，而不是散落在"插件"与"数据"两处。
