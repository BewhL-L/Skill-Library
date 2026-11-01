# 密钥清单与恢复步骤

导出时**只保留键名**，值一律丢弃。恢复后按本清单补齐。

## 1. `.env` 里的键（本机实测存在的）

| 键 | 用途 | 从哪里取 | 优先级 |
|---|---|---|---|
| `OPENAI_API_KEY` | OpenAI 兼容接口的主密钥 | 各服务商控制台 | 高 |
| `OPENAI_BASE_URL` | 兼容接口地址（豆包/硅基流动/DeepSeek 等） | 与服务商文档一致，**不是密钥** | 高 |
| `DEEPSEEK_API_KEY` | 推理模型 | DeepSeek 控制台 | 中 |
| `SILICONFLOW_API_KEY` | 硅基流动（embedding / 模型） | 硅基流动控制台 | 中 |
| `MEM0_API_KEY` | mem0 记忆服务 | mem0 控制台 | **高** |
| `TERMINAL_ENV` | 终端环境标识 | 保持原值，不算密钥 | 低 |
| `NO_PROXY` / `no_proxy` | 代理白名单 | 保持原值（含 `localhost,127.0.0.1`） | 低 |

> 键集合随版本变化。**以备份里的 `.env.example` 为准**，不要照抄这张表。

## 2. mem0 专项：四处缺一不可

mem0 不是"一个 key 就够"的组件，它在四个位置各有一份必要信息：

| # | 位置 | 缺了会怎样 | 恢复动作 |
|---|---|---|---|
| 1 | `config.yaml` → `memory.provider: mem0`、`plugins.enabled` 含 `mem0` | 回落默认记忆后端，旧记忆读不到 | 随 config 还原，`grep mem0 ~/.hermes/config.yaml` 确认 |
| 2 | `~/.hermes/plugins/mem0/` | 启用名单里有、代码没有（多为静默失败） | 备份已整份复制，确认目录存在即可 |
| 3 | `.env` → `MEM0_API_KEY` | 写入/检索 401 | 补值后 `hermes gateway restart` |
| 4 | `~/mem0/server` Docker 栈 + PostgreSQL | 历史记忆整体丢失 | `docker compose up -d` 后导入 `mem0_app.sql.gz` |

第 4 项的完整命令：

```bash
cd ~/mem0/server
cp <备份>/mem0-service/.env.example .env     # 填 POSTGRES_PASSWORD / API keys
docker compose up -d
gunzip -c <备份>/mem0-service/mem0_app.sql.gz | \
  docker exec -i $(docker ps --format '{{.Names}}' | grep -E 'mem0.*postgres' | head -1) \
  psql -U postgres -d mem0_app
```

导入前建议先确认库是空的（`\dt` 无表），否则先 `DROP SCHEMA public CASCADE; CREATE SCHEMA public;`——这一句会清空现有数据，务必确认后再执行。

## 3. `auth.json`

- 内容：Hermes 登录令牌（账号/ACP 等）。
- **不进备份**：等同密码，且换机后通常需要重新授权。
- 恢复后执行 `hermes auth --help` 查看当前版本的登录子命令，按提示重新登录。

## 4. 补齐步骤

```bash
cp ~/.hermes/.env.example ~/.hermes/.env
chmod 600 ~/.hermes/.env

# 逐个填，不留在 shell 历史里：
read -rs KEY && printf 'OPENAI_API_KEY=%s\n' "$KEY" >> ~/.hermes/.env && unset KEY

bash /mnt/c/Users/23981/.workbuddy/skills/hermes-portability/scripts/verify.sh
```

`verify.sh` 会分别列出「声明了但缺失」与「有键但值为空」的项。

## 5. 常见 401 / 403 排查

| 现象 | 先查 | 再查 |
|---|---|---|
| 调用模型 401 | 键名是否拼错（`OPENAI_API_KEY` ≠ `OPENAI_KEY`） | `OPENAI_BASE_URL` 是否指向对应服务商 |
| mem0 401 | `MEM0_API_KEY` 是否存在且非空 | 该 key 是否属于当前环境（云端 vs 自建） |
| 全部 403 | 账号额度/权限 | 代理是否把请求改写（`NO_PROXY` 是否漏了本机地址） |
| 时好时坏 | 代理链路 | `.env` 里是否有重复键（后出现的覆盖前面的） |

查重复键：`grep -n '^OPENAI_API_KEY=' ~/.hermes/.env`，出现两次就是问题。

## 6. 轮换建议

换机器视为"凭据可能暴露"，按此顺序轮换：

1. 新机器先填**新** key 并验证可用；
2. 控制台吊销**旧** key；
3. 最后清理旧机器的 `~/.hermes/.env` 与 `auth.json`。

顺序不能反——先吊销会导致旧机器无法回滚验证。

## 7. 三条纪律

1. **不要把 `.env` 加进任何 git 仓库**，即使是私有仓库；备份目录同理。
2. **不要用明文把密钥贴在聊天/文档里**；共享走密码管理器。
3. 备份目录权限 `700`，上传网盘前先加密（见 `SECURITY.md`）。
