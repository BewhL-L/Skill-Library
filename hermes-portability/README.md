# hermes-portability

把一台机器上的 Hermes（`hermes-agent`）完整搬到另一台机器：配置、技能、第三方插件（含 mem0）、记忆、会话、数据库，以及 mem0 那套独立的 Docker 服务。

**目标**：新电脑上一条命令，把"能重建的"交给安装器，"重建不出来的"交给备份。

## 为什么需要它

Hermes 的状态散在十几处：`config.yaml` 是配置，`skills/` 是技能，`plugins/` 是插件代码，`.env` 是密钥，`state.db` 是会话，`memories/` 是长期记忆——而 mem0 又横跨"配置 + 插件 + 密钥 + 一个独立 Docker 栈"四处。手工搬漏一处，症状往往是"能启动但记忆是空的"。

这个技能把这份清单固化成脚本与检查项。

## 三层备份

| 层 | 带什么 | 体积 |
|---|---|---|
| `config` | 配置、技能、hooks、cron、mem0 插件代码、`.env` 键名 | 20–30 MB |
| `state`（默认） | config + 记忆、会话、三个 SQLite 库 | +几十 MB |
| `full` | state + Hermes 源码、`installs/`、`tools/`、`skins/` | 数百 MB |

## 快速开始

```bash
SK=/mnt/c/Users/23981/.workbuddy/skills/hermes-portability

bash "$SK/scripts/export.sh"                       # 备份（默认 config+state+mem0）
bash "$SK/scripts/bootstrap.sh" --from <备份目录> --yes   # 新机器一条命令
bash "$SK/scripts/verify.sh"                       # 体检
```

详细步骤见 [QUICKSTART.md](QUICKSTART.md)；命令参数见 [SKILL.md](SKILL.md)。

## 目录结构

```
hermes-portability/
├── SKILL.md               # 触发条件、工作流、输出规范、质量标准
├── README.md              # 本文件
├── QUICKSTART.md          # 三个场景的最短路径
├── CHANGELOG.md           # 版本记录
├── FAQ.md                 # 常见问题
├── SECURITY.md            # 密钥与数据安全策略
├── examples/              # 备份产物示例
├── scripts/
│   ├── export.sh          # 导出
│   ├── restore.sh         # 还原
│   ├── bootstrap.sh       # 新机器：安装+还原+体检
│   └── verify.sh          # 只读体检
└── references/
    ├── inventory.md       # ~/.hermes 逐目录说明
    └── secrets.md         # 密钥清单（含 mem0 专项）
```

## 设计取舍

- **不打包 `.venv` 与 `tools/`**：平台绑定，官方安装器能重建，带过去只会变大且必坏。
- **第三方插件默认只记清单**：`plugins.txt` 记录名称 + git sha + origin，按 sha 可精确重建；`open-design` 单个就 400 MB 以上。
- **mem0 例外，始终整份复制**：它不是 git 仓库，没有 sha 可依赖，而体积只有 292 KB。
- **密钥绝不入包**：`.env` 只导出键名，`auth.json` 跳过。

## 兼容性

- 目标环境：WSL2（Ubuntu）、bash 4+、`python3`、`tar`、`gzip`
- 已在 Windows 侧的 Git Bash 验证 `config` 层可跑（`state`/`full` 建议在 WSL 内执行）
- Hermes 版本：以 `~/.hermes/hermes-agent` 为准，脚本不依赖具体版本号

## 许可

MIT，见 [LICENSE](LICENSE)。
