# CHANGELOG

遵循语义化版本：`MAJOR.MINOR.PATCH`。技能类项目以"行为变化"为 MINOR，以"文档/措辞"为 PATCH。

## [0.2.2] — 2026-11-02

### 文档

- `SKILL.md` 新增「**恢复后必查 5 项**」：容器 restart 策略、`MEM0_TELEMETRY`、`sync_max_chars`、嵌入维度与 `memories.vector(1024)` 的绑定、`ALL_MEMORIES_LIMIT=1000`。这五项错了都不会报错，只会让记忆"悄悄不工作"——实测曾因 restart 策略缺失，服务停摆 13 小时无人察觉。
- `SKILL.md` 关键约束新增一条：Windows 侧经 `\\wsl.localhost` 写入的脚本**没有执行位**（9p `chmod` 不生效，对照实验 644→600→705 恒为 644；`execve` 返回 `EACCES` 而 `ls -l` 仍显示可执行）。因此本技能脚本一律以 `bash "$SK/scripts/*.sh"` 调用，不依赖执行位。
- `references/inventory.md` 把 `memories/` 从一行扩为结构说明：`MEMORY.md`（agent 笔记）/ `USER.md`（用户画像）的职责、条目以 `\n§\n` 分隔、默认上限 2200 / 1375 字符且写满即拒、会话启动冻结成快照（中途写入下个会话才生效），并给出两种"看起来没恢复"的判别：行为没变是快照旧，记忆为空是只迁了 `state.db` 漏了 `memories/`。
- `references/inventory.md` 补充恢复规则：**内置记忆始终启用，外部 provider（mem0 / byterover / retaindb）同一时间只能挂一个**；`memory.provider` 指向未安装插件时，外部记忆等于没开。

## [0.2.1] — 2026-11-02

### 修复

- **`bootstrap.sh` 会丢掉安装器刚建好的环境**：它原先调用 `restore.sh --force`，会把 `~/.hermes` 整体改名为 `.bak`，`--tier state` 的备份里没有 `.venv`/`installs`/`tools`，还原后 Hermes 反而起不来。新增 `restore.sh --merge`（覆盖叠加），bootstrap 改用 `--merge`。
- `bootstrap.sh` 未检查安装结果：`curl | bash` 失败会被管道掩盖。现在校验退出码，并确认 `$TO/hermes-agent/.venv/bin/hermes` 存在，否则中止。
- `restore.sh` 允许同时传 `--force --merge`（merge 静默生效）：改为互斥报错。
- `export.sh` 的 `pg_dump` 硬编码 `-U postgres`：改为从 mem0 的 `.env` 读 `POSTGRES_USER`，缺省回落 `postgres`。
- `plugins.txt` 里 mem0 仍提示"re-run with --with-plugins"，但它的代码其实已随 `files/hermes/plugins/mem0` 复制；改为如实说明。

### 文档

- 新增 `references/hermes-agent-tree.md`：`hermes-agent/` 的目录构成、体积（源码 7,544 个 `.py`、`.venv` 151 MB、`.git` 1.2 GB）、为何 `full` 层排除二者、如何用安装器或 `pip install -e .` 重建。
- `SKILL.md` 补充 `--force` 与 `--merge` 的适用场景；`API.md` 同步参数表。

## [0.2.0] — 2026-11-01

### 新增

- **mem0 四处全覆盖**：配置项、`~/.hermes/plugins/mem0` 代码、`MEM0_API_KEY` 键名、`~/mem0/server` Docker 栈（compose + env 键名 + `pg_dump`）。
  - 插件代码**始终复制**（292 KB，非 git 仓库，无法按 sha 重建）。
  - Docker 栈默认备份，`--no-mem0-service` 可跳过，`MEM0_SERVICE_DIR` 可改路径。
- **`scripts/bootstrap.sh`**：新机器一条命令完成"安装 → 还原 → 体检 → 待办清单"。未装 Hermes 时需 `--yes` 才执行官方安装脚本。
- **`plugins.txt`**：记录第三方插件名 + git sha + origin，避免"启用了但没代码"。
- `--with-plugins`：需要连插件代码一起带走时的显式开关（排除 `node_modules`/`.git`/`dist`）。
- `verify.sh` 新增插件一致性检查：`config.yaml` 的 `plugins.enabled` 对不上实际目录时给出 WARN 与修法。

### 变更

- **默认层级 `config` → `state`**：换机场景下配置和记忆本就该一起走，默认值对齐真实用法。
- `export.sh` 的 `--tier` 说明改为累积语义（config < state < full）。
- RESTORE.md 与 `restore.sh` 增加 mem0 Docker 栈的恢复步骤（含 `gunzip | psql` 一行命令）。

### 修复

- **失败的 SQLite 备份会留下 0 字节 `.db`**：改为先写系统临时文件，成功才 `mv` 进备份树（否则还原时会装上一个空库，且没有任何提示）。
- 锁定的数据库可能无限阻塞：给每个 dump 加 20s 超时，失败降级为 WARN。
- `tar -C "<Windows 路径>"` 被 GNU tar 的反斜杠转义破坏（`\23981` → `\023981`）：改为子 shell `cd` 后再打包/解包。
- `[ "$tier" = "full" ]` 变量名大小写不一致，`set -u` 下直接 `unbound variable` 退出。
- `file://wsl.localhost/...` 让 SQLite URI 解析失败：增加普通连接回退。
- 运行中的数据库返回 `locked` 被误判为 FAIL：改判 WARN 并注明"Hermes 正在运行"。
- 脚本内 `rm -f` 触发安全策略：改为"有内容才写文件"，不做删除。

### 文档

- 新增 README / QUICKSTART / CHANGELOG / FAQ / SECURITY / LICENSE / examples。
- 新增 INSTALLATION / ARCHITECTURE / API / TESTING / DEBUGGING / CONTRIBUTING / CODE_OF_CONDUCT（由 skill-optimizer 的文档完整性维度驱动）。
- `SKILL.md` 补齐「核心原则」「工作流程」「输出规范」「质量标准」四节，并把三个使用场景改为三级标题（审计可识别）。
- `references/inventory.md` 增加判定流程图与"重建代价"表；`references/secrets.md` 扩充到含 mem0 四项密钥、轮换与 401 排查。

### 评分（skill-optimizer v1.8.0）

| 阶段 | 总分 | 等级 | 主要缺口 |
|---|---|---|---|
| v0.1.0 初版 | 48.5 | D | 文档 0 分、缺输出规范、场景 0 个 |
| 补 SKILL.md 四节 + 场景 | 83.5 | B | 缺 7 份文档、references 过浅 |
| 补全文档与 references | **99.0** | **S** | 仅剩"未使用 argparse"（bash 脚本不适用） |

> 已知限制：审计项「未使用 argparse」对 bash 脚本无法满足。脚本用 `case` 解析参数并统一提供 `--help`，行为等价；未为了评分伪造 Python 入口。

## [0.1.0] — 2026-11-01

### 新增

- 三层导出（`config` / `state` / `full`），SQLite 走 `backup()` API 保证一致。
- `restore.sh`：非空目标默认拒绝，`--force` 时先改名为 `.bak.<时间>`。
- `verify.sh`：配置、密钥完整性、数据库完整性、gateway 状态、自定义资产五类检查。
- `references/inventory.md`：`~/.hermes` 逐目录该不该迁的判定表。
