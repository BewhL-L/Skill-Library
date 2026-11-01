# QUICKSTART

三个场景，按需选一条。所有命令在 **WSL 终端**执行。

```bash
SK=/mnt/c/Users/23981/.workbuddy/skills/hermes-portability
```

## 场景一：日常备份（升级 Hermes 前也做一次）

```bash
bash "$SK/scripts/export.sh"
```

默认 `state` 层：配置 + 技能 + 插件清单 + mem0 四处 + 记忆 + 会话 + 数据库。

产物：

```
~/hermes-backup/hermes-20261101-2330/
├── manifest.json      # 来源主机、Hermes 版本、文件数与总大小
├── RESTORE.md         # 这份备份的恢复步骤
├── plugins.txt        # 第三方插件：名称 / sha / origin
├── mem0-service/      # compose + env 键名 + pg_dump
└── files/hermes/      # 实际内容
```

判断成功：末行出现 `done: <路径> (<体积>)`。

## 场景二：换新电脑，一条命令搞定

新机器先装 WSL 与 Docker，然后把备份拷进来（`scp` / 移动硬盘 / 从 `\\wsl.localhost` 拖进 WSL）。

```bash
bash "$SK/scripts/bootstrap.sh" --from ~/hermes-backup/hermes-20261101-2330 --yes
```

它依次做四件事：

1. 检查 `tar`、`python3`；没装 Hermes 就调用官方安装器（`--yes` 才执行远程脚本）
2. `restore.sh` 还原（目标非空会先改名保留）
3. `verify.sh` 体检
4. 打印待办：填密钥、重新登录、重装插件、恢复 mem0 Docker 栈

判断成功：末行 `环境已就绪（verify 无 FAIL）`。

## 场景三：环境不对劲，先体检

```bash
bash "$SK/scripts/verify.sh"
```

输出 `OK / WARN / FAIL`，重点看两类：

| 输出 | 含义 | 处理 |
|---|---|---|
| `enabled in config.yaml but not installed` | 配置启用了插件但代码不在 | 从备份还原 `~/.hermes/plugins/` |
| `keys with empty value` | `.env` 有键无值 | 按 `references/secrets.md` 填 |
| `state.db is locked` | Hermes 正在运行 | 正常，停服务后再跑可校验 |

## 只想带走配置（不带记忆）

```bash
bash "$SK/scripts/export.sh" --tier config
```

体积最小（20 MB 左右），跨 Hermes 版本最稳。

## 连第三方插件代码一起带走

```bash
bash "$SK/scripts/export.sh" --with-plugins
```

会额外复制 `~/.hermes/plugins/` 下所有插件（排除 `node_modules`、`.git`、`dist`）。`open-design` 体积很大，确认磁盘再跑。

## 不需要 mem0 Docker 栈

```bash
bash "$SK/scripts/export.sh" --no-mem0-service
```

mem0 的另外三处（配置、插件代码、环境变量键名）仍会备份。
