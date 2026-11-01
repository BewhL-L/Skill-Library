# CONTRIBUTING

这是**个人使用的技能**（single-user），不对外开放贡献流程。以下规则用于未来的自己。

## 修改前

1. 先跑一遍基线：`bash scripts/verify.sh`，记下当前的 fail/warn 数；
2. 备份一份当前技能目录（或依赖 git 仓库的提交记录）；
3. 明确改动属于哪一类：脚本行为 / 文档 / 层级定义。

## 改动脚本时的约定

| 约定 | 原因 |
|---|---|
| 只用 bash + `python3` + `tar` + `gzip` | 新机器上不一定有 rsync、jq、7z |
| 不引入 `rm -f` | 沙箱/审计环境会拦截；用"有内容才写文件"替代 |
| 所有路径用变量（`HERMES_HOME`、`MEM0_SERVICE_DIR`） | 便于在临时目录里做回归 |
| 失败必须给出下一步命令 | 不许只说"失败了" |
| 新增参数必须更新 `API.md` 与 `SKILL.md` 的输出规范 | 三处不同步会误导后续使用 |

## 提交信息

```
fix(export): 修复 tar -C 在 Windows 路径下的转义问题

现象：备份目录被写成 C\:\\Users\023981\\...
根因：GNU tar 把 \2 当作八进制转义。
改法：改为子 shell cd 后再打包，避免向 tar 传 Windows 路径。
验证：Git Bash + WSL UNC 路径下导出成功，体积与文件数符合预期。
```

## 回归清单

- [ ] `bash -n scripts/*.sh` 全通过
- [ ] `export.sh` 在真实 `~/.hermes` 上产出 `done:` 行，体积合理
- [ ] `restore.sh` 对非空目标仍拒绝
- [ ] `verify.sh` 对健康安装 `0 fail`
- [ ] `CHANGELOG.md` 已更新（版本号 + 变更点）

## 版本号

- 行为变化（新增参数、默认层级、新增备份内容）→ MINOR
- 文档、措辞、注释 → PATCH
- 破坏兼容（备份目录结构变化）→ MAJOR，并在 `CHANGELOG` 写明迁移方式
