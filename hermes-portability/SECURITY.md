# SECURITY

## 威胁模型

备份目录是"一个文件夹"，它最常见的三种泄漏路径：

1. 被同步到网盘（OneDrive / iCloud / 坚果云）或自动上传到对象存储；
2. 被误 `git add` 进仓库（本项目历史上发生过一次文档误入公开仓库）；
3. 被拷到共享盘、临时目录、别人机器上排查问题。

因此本技能按"备份包可能被公开"来设计。

## 包里**没有**什么

| 内容 | 处理 |
|---|---|
| `.env` 的值 | 只导出键名，生成 `.env.example` |
| `auth.json` | 完全不导出（等同密码） |
| `node_modules`、`.venv`、缓存、日志 | 排除（与安全无关，但缩小暴露面） |

脚本里没有任何"顺手打包整个 `~/.hermes`"的路径。

## 包里**有**什么（需要你自行保护）

`state` 层与 `full` 层包含：

- `memories/`：长期记忆，往往是个人与项目的真实描述；
- `sessions/`：完整对话记录；
- `state.db` / `kanban.db`：会话与任务数据；
- `mem0-service/*.sql.gz`：mem0 服务的数据库导出（含记忆正文）。

这些**不是密钥，但属于隐私**。建议：

```bash
chmod -R 700 ~/hermes-backup          # 只允许本人读
# 上传网盘前先加密（age 或 gpg 均可）
tar czf - hermes-20261101-2330 | age -p > hermes-20261101-2330.tar.gz.age
```

## 密钥补齐时的注意事项

- 不要用 `echo $KEY >> .env` 留 shell 历史，用 `read -rs`（见 `references/secrets.md`）；
- 不要在聊天、Issue、文档里贴真实 key；
- `.env` 权限建议 `600`：`chmod 600 ~/.hermes/.env`。

## 换机后建议轮换

换机器是"凭据可能已暴露"的信号之一（旧机器可能被转卖、重装前未清理）。优先级：

1. `MEM0_API_KEY`（若 mem0 是云端托管）
2. `OPENAI_API_KEY` / `DEEPSEEK_API_KEY` / `SILICONFLOW_API_KEY`
3. Hermes 登录态（`auth.json` 对应的账号）

轮换顺序：先在新机器填新 key 验证可用，再在旧机器/控制台吊销旧 key——避免中途把自己锁在门外。

## 旧机器怎么处理

至少在旧机器上执行：

```bash
hermes gateway stop
rm -rf ~/.hermes/.env ~/.hermes/auth.json ~/.hermes/sessions ~/.hermes/memories
```

`rm -rf` 只针对明确路径，不要对整个 `~/.hermes` 执行（可能误删你还要用的东西）。

## 报告问题

这是个人使用的技能，没有漏洞奖励流程。发现脚本会写入超出预期范围的内容（例如把 `.env` 打进包里），请直接停用并修正 `scripts/export.sh`。
