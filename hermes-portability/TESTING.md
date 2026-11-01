# TESTING

## 验证过的内容（2026-11-01，真实环境）

测试对象：WSL2 Ubuntu 上的实际 `~/.hermes`（含 20 个技能分类、5 个第三方插件、运行中的 mem0 Docker 栈）。

| 用例 | 命令 | 期望 | 实际 |
|---|---|---|---|
| 导出 config 层 | `export.sh --tier config` | 生成 manifest + files | ✅ 729 文件 / 20.6 MB |
| 导出含 mem0 | `export.sh --tier config` | `mem0-service/` 有 compose + env 键名 + pg_dump | ✅ 6 张表 / 342 行 dump |
| 插件清单 | 同上 | `plugins.txt` 5 行（含 mem0 标记非 git） | ✅ |
| 还原 | `restore.sh --from ... --to <临时目录>` | 文件就位、生成 `.env`、打印待填项 | ✅ |
| 覆盖保护 | 对同一目标再跑一次 | 拒绝并提示 `--force` | ✅ |
| 体检（正常） | `verify.sh` | `0 fail`，数据库 locked 为 WARN | ✅ 0 fail / 4 warn |
| 失败路径 | `POSTGRES_HOST=no-such-host` 跑导出脚本的等待逻辑 | 退避后抛出 | ✅（见 mem0 修复记录） |
| 语法检查 | `bash -n scripts/*.sh` | 无错误 | ✅ |

## 可复现的验证步骤

```bash
SK=/mnt/c/Users/23981/.workbuddy/skills/hermes-portability

# 1. 语法
for f in "$SK"/scripts/*.sh; do bash -n "$f" || echo "FAIL $f"; done

# 2. 导出到临时目录
TMP=$(mktemp -d)
HERMES_HOME=~/.hermes bash "$SK/scripts/export.sh" --tier config --out "$TMP"

# 3. 结构断言
test -f "$TMP"/hermes-*/manifest.json && echo "manifest ok"
test -f "$TMP"/hermes-*/files/hermes/config.yaml && echo "config ok"
test -d "$TMP"/hermes-*/files/hermes/plugins/mem0 && echo "mem0 plugin ok"

# 4. 还原到临时目标
bash "$SK/scripts/restore.sh" --from "$TMP"/hermes-* --to "$TMP/restored"

# 5. 体检
bash "$SK/scripts/verify.sh" --home ~/.hermes
```

## 真实环境记录（2026-11-02 00:04，WSL）

在 WSL 内对运行中的 Hermes 执行默认（`state`）导出，三个数据库全部在线备份成功：

```
tier: state
dest: /home/luo/hermes-backup/hermes-20261102-0004
[2/4] copying files
  + plugins/mem0
  + mem0-service/mem0_app.sql.gz
  ~ state.db (sqlite online backup)
  ~ kanban.db (sqlite online backup)
  ~ shared-state.db (sqlite online backup)
[3/4] writing manifest
  + manifest.json (737 files, 26.5 MB)
done: /home/luo/hermes-backup/hermes-20261102-0004  (30M)
```

结论：`state` 层在原生文件系统上可用；Windows 侧同样的操作会因 9p 锁失败并降级为 WARN，属预期差异。

## 未自动化、需人工确认的部分

- **跨机器真实迁移**：需要第二台机器或全新 WSL 发行版，目前只做了"还原到临时目录"的等价验证。
- **mem0 数据导入**：`gunzip | psql` 一步未在清空库上实测（会破坏现有数据）。
- **Hermes 大版本升级后的兼容性**：依赖目录布局，未做版本矩阵测试。

## 回归关注点

改动脚本后，至少重跑三条：

1. `export.sh` 的 `done:` 行出现且体积合理（config 层 20–30 MB，突然翻倍说明过滤失效）
2. `restore.sh` 对非空目标仍然拒绝
3. `verify.sh` 的 `summary` 行 fail 数为 0（对健康安装）

## 已知检测盲区

- 脚本无法判断 `memories/` 内容是否"过期"或"矛盾"，只保证搬过去。
- `verify.sh` 不校验 `.env` 的值是否正确（避免把密钥读进日志），只校验"是否存在/是否为空"。
