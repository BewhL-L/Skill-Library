# FAQ

## 1. 备份里有我的 API Key 吗？

没有。`.env` 只导出**键名**（生成 `.env.example`），`auth.json` 完全不碰。恢复后需要手工填值并重新登录。

这样做是因为备份目录经常被同步到网盘或误提交进仓库——一次泄漏就够。

## 2. 为什么 mem0 要单独处理，不能跟着"插件"一起备份？

因为 mem0 横跨四个位置，缺一处就会出现"能启动、但记忆是空的"：

| # | 位置 | 不备份的后果 |
|---|---|---|
| 1 | `config.yaml` 的 `memory.provider` / `plugins.enabled` | Hermes 回落默认记忆后端 |
| 2 | `~/.hermes/plugins/mem0/` 代码 | 启用了但插件不存在（多为静默失败） |
| 3 | `.env` 的 `MEM0_API_KEY` | 调用 401，记忆写入失败 |
| 4 | `~/mem0/server` Docker 栈（PostgreSQL） | 历史记忆直接丢失 |

其中第 2 项**不是 git 仓库**，没有 sha 可依赖，所以脚本对它特殊处理：无论是否 `--with-plugins`，都整份复制。

## 3. 我只想恢复记忆，不想覆盖现在的配置，可以吗？

可以，但要手工做：从备份里单独取

```bash
cp -a <备份>/files/hermes/memories/. ~/.hermes/memories/
cp -a <备份>/files/hermes/sessions/. ~/.hermes/sessions/
```

数据库（`state.db` 等）不要直接拷——它可能带 `-wal`/`-shm`，必须三件一起或停服务后拷。更稳的是用 `sqlite3 .backup`。

`restore.sh` 是整目录还原，不做部分合并。

## 3.1 `--force` 和 `--merge` 有什么区别？什么时候用哪个？

| 参数 | 行为 | 适用 |
|---|---|---|
| `--force` | 把现有 `~/.hermes` 改名为 `~/.hermes.bak.<时间>`，再整目录还原 | 干净重装、原目录已坏、想要一份可回滚的旧副本 |
| `--merge` | 保留目标已有文件，只写入备份里有的 | 安装器刚装好（已有 `.venv`/`installs`/`tools`），只需要补配置与数据 |

**`bootstrap.sh` 内部用 `--merge`**。如果这里误用 `--force`，会把安装器刚建好的 `.venv` 换掉，而 `state` 层备份里没有 `.venv`，结果是"文件齐了但 Hermes 起不来"——这是 0.2.1 修掉的一个真实缺陷。

## 4. `full` 层里的 `installs/`、`tools/`、`skins/` 是什么？要带吗？

| 目录 | 是什么 | 建议 |
|---|---|---|
| `installs/` | Hermes 自身的运行时安装状态（`bootstrap`、`environments`、`pm-runtime`），由安装器生成 | 可重建，一般不带 |
| `tools/` | 随包下载的便携二进制：node、python、ffmpeg、ripgrep、uv、chromium，目录名带 `linux-x64` | **不要带**，平台绑定且体积大 |
| `skins/` | 界面主题 | 改过主题才带 |

`full` 层的真正价值是 `hermes-agent/` 源码（且已排除 `.venv`），其余三项属于"能重造"。

## 5. 换机器后 Hermes 能启动，但记忆/会话是空的？

按顺序查：

1. `bash verify.sh` —— 看是否有 `keys with empty value`（`.env` 没填）
2. 确认备份层级：`config` 层**不含** `memories/` 与 `state.db`
3. 看 `manifest.json` 里的 `tier` 字段是不是 `state` 或 `full`
4. mem0 场景：确认 `~/mem0/server` 的 Docker 栈起来了，且 `pg_dump` 已导入

## 6. 备份多大？多久做一次？

- `config`：20–30 MB（主要是 `skills/`）
- `state`：再多几十 MB（`state.db` 随会话增长）
- `full`：数百 MB（源码 + `installs/`）

建议：**升级 Hermes 前必做一次**（`state` 层），平时每周一次即可。真正会丢的是"未提交的自定义技能"和"新产生的记忆"，两者都在 `state` 层里。

## 7. 备份能跨 Hermes 大版本吗？

配置能，数据库不一定。跨大版本时建议：

1. 先 `--tier config` 迁移，让新版本自己建库；
2. 确认新版本能启动后，再决定是否导入旧的 `state.db`；
3. 导入前先备份新生成的空库，导入失败可回滚。
