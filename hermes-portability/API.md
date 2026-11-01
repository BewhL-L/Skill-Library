# API

四个脚本的命令行接口。所有参数都支持 `--help`。

## 环境变量

| 变量 | 默认值 | 作用 |
|---|---|---|
| `HERMES_HOME` | `$HOME/.hermes` | 源/目标安装目录 |
| `MEM0_SERVICE_DIR` | `$HOME/mem0/server` | mem0 Docker 栈所在目录 |

## export.sh

```bash
bash export.sh [--tier config|state|full] [--out DIR] [--with-plugins] [--no-mem0-service]
```

| 参数 | 默认 | 说明 |
|---|---|---|
| `--tier` | `state` | 累积层级：config < state < full |
| `--out` | `$HOME/hermes-backup` | 输出根目录，实际产物在 `<out>/hermes-YYYYMMDD-HHMM/` |
| `--with-plugins` | 关 | 复制 `~/.hermes/plugins/` 全部代码（排除 node_modules/.git/dist） |
| `--no-mem0-service` | 开（即默认备份） | 跳过 mem0 Docker 栈 |

退出码：`0` 成功；`1` 环境不满足（无 python3 / HERMES_HOME 不存在）；`2` 参数错误。

产出：`manifest.json`、`RESTORE.md`、`files/hermes/`、`plugins.txt`（无 `--with-plugins` 时）、`mem0-service/`（未跳过时）。

## restore.sh

```bash
bash restore.sh --from BACKUP_DIR [--to DIR] [--force]
```

| 参数 | 必需 | 说明 |
|---|---|---|
| `--from` | 是 | 含 `manifest.json` 的备份目录 |
| `--to` | 否 | 默认 `$HERMES_HOME`；非空时必须配 `--force` 或 `--merge` |
| `--force` | 否 | 把现有目录改名为 `<to>.bak.<时间>` 后整目录还原 |
| `--merge` | 否 | 覆盖叠加：保留目标已有的 `.venv`、`installs/`、`tools/`，只写入备份里有的文件 |

退出码：`0` 成功；`1` 备份无效或目标非空未加 `--force`；`2` 参数错误。

行为：还原后若无 `.env` 而有 `.env.example`，自动复制并打印待填键名。

## bootstrap.sh

```bash
bash bootstrap.sh --from BACKUP_DIR [--to DIR] [--yes]
```

| 参数 | 说明 |
|---|---|
| `--from` | 必需 |
| `--to` | 默认 `$HERMES_HOME` |
| `--yes` | 未安装 Hermes 时，允许直接执行官方安装脚本；不加则打印命令并退出 |

退出码：`0` 全部通过；`1` 缺少依赖或未确认安装；其他为 `verify.sh` 的返回码。

## verify.sh

```bash
bash verify.sh [--home DIR]
```

只读。检查项：目录、`config.yaml`、`.env` 键完整性、`auth.json`、`hermes` 可执行文件、三个 SQLite 库、`gateway_state.json`、`skills/hooks/desktop-plugins`、启用插件与目录一致性。

退出码：`0` 无 FAIL；`1` 至少一项 FAIL。WARN 不影响退出码。

输出格式：

```
  OK    config.yaml parses (has 'agent')
  WARN  state.db is locked (Hermes is running) — integrity not checked
  FAIL  hermes executable not found — run the official installer

summary: 1 fail, 1 warn
```

## 退出码约定

| 码 | 含义 | 使用者应做什么 |
|---|---|---|
| 0 | 成功 / 无 FAIL | 继续下一步 |
| 1 | 业务性失败（可修复） | 按输出提示处理 |
| 2 | 参数错误 | 看 `--help` |
