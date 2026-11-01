# DEBUGGING

排查顺序：先看脚本退出码，再看备份目录结构，最后看内容。

## 常见症状

| 症状 | 可能原因 | 验证 | 处理 |
|---|---|---|---|
| `HERMES_HOME not found` | 在 Windows 侧跑，`$HOME` 指向 `C:\Users\...` | `echo $HERMES_HOME` | 显式传 `HERMES_HOME=~/.hermes`，或进 WSL 跑 |
| `python3 not found` | 精简容器/新装系统 | `command -v python3` | 安装 python3，或改用 `--tier config` 并手工备份数据库 |
| 备份体积突然翻倍 | 过滤失效（某个插件带了 `node_modules`） | `du -sh <备份>/files/hermes/*` | 检查 `tar --exclude` 是否被改动 |
| `restore.sh` 报 `target exists` | 目标非空 | `ls -A ~/.hermes` | 确认后加 `--force`（会先改名保留） |
| `verify.sh` 报 `invalid uri authority` | 在 Windows 侧访问 UNC 路径 | 看路径是否以 `//` 开头 | 脚本已回退普通连接；仍失败则进 WSL 跑 |
| `state.db is locked` | Hermes 正在运行 | `hermes gateway status` | 正常；要校验完整性先停服务 |
| `enabled in config.yaml but not installed` | 插件代码没搬过来 | `ls ~/.hermes/plugins` | 从备份 `files/hermes/plugins/` 还原，或 `--with-plugins` 重导 |
| `hermes not on PATH` | 只装了 venv | `ls ~/.hermes/hermes-agent/.venv/bin/hermes` | 用绝对路径，或把 venv/bin 加进 PATH |

## 定位"少带了什么"

备份目录里有 `manifest.json`，用它做集合比较：

```bash
python3 - <<'PY'
import json
m = json.load(open("备份目录/manifest.json"))
have = {f["path"].split("files/hermes/")[-1] for f in m["files"] if "files/hermes/" in f["path"]}
want = {"config.yaml", "SOUL.md", "plugins/mem0", "memories/MEMORY.md"}
print("缺失:", sorted(want - have))
PY
```

## mem0 专项排查

| 现象 | 检查点 | 命令 |
|---|---|---|
| 记忆写入 401 | `MEM0_API_KEY` 是否为空/拼错 | `grep -n '^MEM0_API_KEY=' ~/.hermes/.env` |
| 插件加载失败 | 目录与启用名是否一致 | `ls ~/.hermes/plugins/mem0; grep -A10 '^plugins:' ~/.hermes/config.yaml` |
| 服务起不来 | compose 与容器状态 | `cd ~/mem0/server && docker compose ps; docker compose logs --tail 30 mem0` |
| 数据为空 | pg_dump 是否导入 | `docker exec -i <pg容器> psql -U postgres -d mem0_app -c '\dt'` |

## 日志与现场

| 内容 | 位置 |
|---|---|
| Hermes 主日志 | `~/.hermes/` 下的 `*.log`，或 `hermes gateway status` 输出 |
| mem0 服务日志 | `docker compose logs -f mem0` |
| 备份过程输出 | 脚本 stdout；建议重跑时加 `2>&1 \| tee export.log` |
| 备份元信息 | `<备份>/manifest.json`（tier、文件数、版本、mem0 是否包含） |

## 回滚

还原失败时的现场保护：

1. 目标目录在 `--force` 下已被改名为 `~/.hermes.bak.<时间>`；
2. 直接 `mv ~/.hermes.bak.<时间> ~/.hermes` 即可回到操作前；
3. 不要删 `*.bak.*` 目录，直到新环境验证通过。
