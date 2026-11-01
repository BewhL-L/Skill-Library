---
name: hermes-portability
version: 0.3.1
description: Backup, migrate, and rebuild a complete Hermes (hermes-agent) installation on WSL — config, skills, third-party plugins (including mem0), memories, sessions, and the external mem0 Docker stack. 当用户提到"换电脑/重装 WSL/重装系统 要迁移 Hermes""备份 ~/.hermes""恢复 Hermes 环境""Hermes 起不来、少了什么""mem0 插件怎么跟着走"时使用；也支持只导出配置做增量备份、或在新机器上一条命令完成安装+还原+体检。
agent_created: true
---

# Hermes 迁移与备份

## 核心原则

1. **一次命令能重建一台机器**：新机器上 `bootstrap.sh` 完成安装 → 还原 → 体检，不需要人肉对照清单。
2. **可重建的不备份**：缓存、`.venv`、`node_modules`、便携二进制（`tools/`）一律排除；留下的是"重建不出来的东西"。
3. **密钥永不入包**：`.env` 只留键名，`auth.json` 不导出；恢复后按清单补值、重新登录。
4. **mem0 按一等公民处理**：它分布在四处（配置、插件代码、密钥、独立 Docker 栈），少一处就会出现"配置在、记忆读不出来"。
5. **备份可验证、可回滚**：每份备份带 `manifest.json` 与 `RESTORE.md`；还原默认拒绝覆盖非空目录，加 `--force` 也先改名保留。

## 何时使用（使用场景）

| 场景 | 触发说法 | 用哪个命令 |
|---|---|---|
| 换新电脑，一次配好 | "换电脑了，帮我把 Hermes 整套搬过去" | `bootstrap.sh --from <备份>` |
| 日常/升级前备份 | "备份一下 Hermes"、"升级前留个底" | `export.sh`（默认 config+state） |
| 只想带走配置和技能 | "不要历史记录，只要配置" | `export.sh --tier config` |
| 换机后环境不对 | "Hermes 起不来"、"插件启用了但没生效" | `verify.sh` |
| mem0 记忆丢失/迁移 | "mem0 的数据要一起搬" | `export.sh`（默认含 mem0 服务） |

## 使用场景（输入 / 输出）

### 场景 1：例行备份

```
输入：用户说"备份一下 Hermes"
执行：bash "$SK/scripts/export.sh"
输出：
  [2/4] copying files
    + config.yaml ... + plugins/mem0
    + mem0-service/mem0_app.sql.gz
  [3/4] writing manifest
    + manifest.json (737 files, 26.5 MB)
  done: /home/luo/hermes-backup/hermes-20261102-0004  (30M)
```

### 场景 2：换新电脑

```
输入：用户给出备份目录，要求"一条命令配好"
执行：bash "$SK/scripts/bootstrap.sh" --from <备份> --yes
输出：
  == 1/4 环境检查 ==   hermes 未安装 → 执行官方安装
  == 2/4 还原 ==       files restored
  == 3/4 体检 ==       0 fail, 4 warn
  == 4/4 待办清单 ==   [ ] 填 .env  [ ] 重登  [ ] 重装插件  [ ] 恢复 mem0 栈
  环境已就绪（verify 无 FAIL）
```

### 场景 3：环境异常排查

```
输入：用户说"Hermes 起来了但记忆是空的"
执行：bash "$SK/scripts/verify.sh"
输出：
  WARN  keys with empty value (fill them): MEM0_API_KEY
  WARN  enabled in config.yaml but not installed: minions
  summary: 0 fail, 2 warn
  → 按提示补 key、还原 plugins/，再跑一次
```

## 三层备份（高层包含低层）

| 层 | 内容 | 体积 | 适用 |
|---|---|---|---|
| `config` | `config.yaml`、`SOUL.md`、`channel_directory.json`、`skills/`、`hooks/`、`cron/`、`desktop-plugins/`、插件清单、**mem0 插件代码**、`.env` 键名 | 20–30 MB | 只要配置与技能 |
| `state`（**默认**） | 上一项 + `memories/`、`sessions/`、`state.db`、`kanban.db`、`shared-state.db`（SQLite 在线备份） | +几十 MB | 换机后接着用记忆与对话 |
| `full` | 上一项 + `hermes-agent/` 源码（排除 `.venv`）、`installs/`、`tools/`、`skins/` | 数百 MB | 连代码与运行时一起搬 |

**mem0 的四处，全部覆盖**：

| # | 位置 | 处理方式 |
|---|---|---|
| 1 | `config.yaml`（`memory.provider: mem0` + `plugins.enabled`） | 随 config 复制 |
| 2 | `~/.hermes/plugins/mem0/`（292 KB，**不是 git 仓库**） | **始终整份复制**（无法按 sha 重建） |
| 3 | `.env` 的 `MEM0_API_KEY` | 只导出键名 |
| 4 | `~/mem0/server` 的 Docker 栈（compose + `.env` + PostgreSQL） | 备份 compose、env 键名、`containers.txt`、`pg_dump` 压缩包 |

第四处可用 `--no-mem0-service` 跳过，或用 `MEM0_SERVICE_DIR` 指向其他路径。

**恢复后必查 5 项**（这些错了不会报错，只会"记忆悄悄不工作"）：

| 项 | 怎么查 | 为什么 |
|---|---|---|
| 容器 restart 策略 | `docker inspect <容器> --format '{{.HostConfig.RestartPolicy.Name}}'`，应为 `unless-stopped` | 默认 `no`：Docker 一重启容器就不回来，同步变成静默失败（实测曾停摆 13 小时无人察觉） |
| `MEM0_TELEMETRY` | `docker exec <容器> printenv MEM0_TELEMETRY` | 本地部署无需上报；顺带消掉日志里的 PostHog 告警 |
| `sync_max_chars` | `~/.hermes/mem0.json`，默认 450 | 每条消息送去做抽取的原文长度，太小会截断长回复里的结论 |
| 嵌入维度 | `memories.vector(1024)` 与 `.env` 的 `MEM0_DEFAULT_EMBEDDER_MODEL` 必须匹配 | 换 embedder 需重建全部向量，否则检索直接报维度错 |
| 列表接口上限 | 服务端 `ALL_MEMORIES_LIMIT=1000` | 导出脚本的 `top_k` 超过它会 422 |

## 工作流程

技能装在 Windows 侧，WSL 里通过 `/mnt/c` 访问：

```bash
SK=/mnt/c/Users/23981/.workbuddy/skills/hermes-portability
```

**让所有 agent 读到同一份源码**

技能通常存在两份：你编辑的源码目录、agent 加载的安装目录。改一份，另一份不会变——这是"改了却没生效"最常见的原因。本技能自带脚本把安装位换成 **junction**（Windows 下无需管理员权限，对读取方透明），此后源码即唯一事实源：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "$SK\scripts\link-skill.ps1" -DryRun   # 先看会动谁
powershell -NoProfile -ExecutionPolicy Bypass -File "$SK\scripts\link-skill.ps1"           # 只改已安装的副本
```

- 自动扫描 `~\*\skills` 与常见 agent 目录（`.workbuddy` / `.claude` / `.codex` / `.agents` / `.cc-switch` / `Doubao`…），不写死单一工具；
- 默认**只处理已存在的副本**，不会把技能装进没装过它的 agent；确需安装时加 `-Install`；
- 实体目录先移到 `%LOCALAPPDATA%\SkillLinkBackups\<name>-<时间戳>` 再建链接——备份**不能**留在技能根目录，否则会被当成第二个同名技能；
- 重复执行是幂等的（已正确链接则报 `already-linked`）；WSL / Linux 侧等价命令：`ln -sfn <源码目录> <安装位>`。
- **安装位里的平台元数据**（如 WorkBuddy 的 `_user_meta.json`）：改成链接后它会落在源码目录，需加进 `.gitignore`；这份元数据不进版本库，**换机器克隆仓库后不会有**，在新机器上重新导入一次技能即可再生——丢失的只是 `source` / `installedAt` 这类记账信息，不影响加载与运行。

**导出**

```bash
bash "$SK/scripts/export.sh"                          # 默认 state：配置+记忆+mem0
bash "$SK/scripts/export.sh" --tier full --out /mnt/d/backup
bash "$SK/scripts/export.sh" --with-plugins           # 连第三方插件代码（体积大）
```

**还原（已有 Hermes）**

```bash
bash "$SK/scripts/restore.sh" --from <备份目录> --to ~/.hermes --force   # 整目录替换，旧的改名保留
bash "$SK/scripts/restore.sh" --from <备份目录> --to ~/.hermes --merge   # 覆盖叠加，保留 .venv/installs/tools
```

`--force` 与 `--merge` 二选一：前者适合"干净重装"，后者适合"安装器刚装好、只补配置"——`bootstrap.sh` 内部用的就是 `--merge`，否则会把安装器刚生成的 `.venv` 一起换掉。

**新机器一条命令**

```bash
bash "$SK/scripts/bootstrap.sh" --from <备份目录> --yes
```

**体检**

```bash
bash "$SK/scripts/verify.sh"
```

## 输出规范

| 命令 | 产出 | 成功判据 |
|---|---|---|
| `export.sh` | `<out>/hermes-YYYYMMDD-HHMM/`，含 `manifest.json`、`RESTORE.md`、`files/hermes/`、`plugins.txt`、`mem0-service/` | 末行打印 `done: <路径> (<体积>)`，退出码 0 |
| `restore.sh` | 目标目录就位 + `.env` 待填清单 + 下一步步骤 | 打印 `files restored`，退出码 0 |
| `bootstrap.sh` | 安装 + 还原 + 体检串起来 | 末行 `环境已就绪（verify 无 FAIL）` |
| `verify.sh` | 逐项 `OK/WARN/FAIL` + 汇总 | `summary: 0 fail`，退出码 0 |

质量要求：任何失败都必须给出**可执行的下一步**（命令或文件路径），不允许只报"失败了"。

## 质量标准（交付前自查）

- [ ] `export.sh` 在真实 `~/.hermes` 上跑通，且 `manifest.json` 的文件数与磁盘一致
- [ ] 备份里没有 `.env` 明文、没有 `auth.json`
- [ ] `restore.sh` 对非空目标默认拒绝，`--force` 会先改名保留
- [ ] `verify.sh` 能发现"config 启用了但插件没装"
- [ ] mem0 四处齐全（配置/插件/键名/pg_dump）
- [ ] 安装位是 junction（`(Get-Item <安装位>).LinkType` 为 `Junction`），或已用 `scripts/link-skill.ps1` 同步并 `diff -rq` 校验
- [ ] 脚本只用 bash + python3 + tar + gzip，不引入额外依赖

## 关键约束

- **数据库不能直接 `cp`**：`state.db` 可能在写事务中，必须用 SQLite `backup()` API（脚本已实现）。
- **不要备份 `.venv`**：绝对路径 + 平台二进制，换机器必坏。
- **`full` 层的 `installs/`、`tools/`、`skins/`**：`installs/` 是 Hermes 自己的运行时安装状态（bootstrap/environments/pm-runtime），`tools/` 是随包下载的便携二进制（node/python/ffmpeg/ripgrep/uv/chromium，`linux-x64`），`skins/` 是界面主题。三者都能由官方安装器重建，属于"体积大、可重造"，只在 `full` 层提供。
- **软链**：`skills/` 里的符号链接导出时记录到 `symlinks.txt`，恢复后需手工重建。
- **路径**：备份目录用纯英文路径；Windows 与 WSL 之间搬运用 `cp`/`scp`，避免 `tar -C` 吃 Windows 反斜杠。
- **Windows 侧写入的脚本没有执行位**：经 `\\wsl.localhost` 写的文件，`chmod` 在 9p 侧不生效（实测 644→600→705 恒为 644），Linux 里 `execve` 会返回 `EACCES`，而 `ls -l` 仍显示可执行。因此本技能脚本一律用 `bash "$SK/scripts/*.sh"` 调用，不依赖执行位。

## 文件说明

| 文件 | 用途 |
|---|---|
| `scripts/export.sh` | 导出（`--tier`、`--with-plugins`、`--no-mem0-service`） |
| `scripts/restore.sh` | 还原（`--from`、`--to`、`--force`） |
| `scripts/bootstrap.sh` | 新机器一条命令：安装 + 还原 + 体检 |
| `scripts/verify.sh` | 只读体检，`OK/WARN/FAIL` |
| `scripts/link-skill.ps1` | 把各 agent 的安装位换成指向源码的 junction（`-DryRun` / `-Install`） |
| `references/inventory.md` | `~/.hermes` 每个目录该不该迁 |
| `references/hermes-agent-tree.md` | `hermes-agent/` 源码目录构成、为何排除 `.venv`/`.git`、如何重建 |
| `references/secrets.md` | 密钥清单、mem0 专项、补齐与轮换 |
