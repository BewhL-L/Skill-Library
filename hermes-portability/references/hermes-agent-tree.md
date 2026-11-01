# `hermes-agent/`：源码目录说明

`~/.hermes/hermes-agent/` 是 Hermes 的**源码检出目录**，也是 editable 安装（`pip install -e`）的目标位置。它既不是配置，也不是数据——删掉它 Hermes 就跑不起来，但重建它的代价很低。

## 目录构成（实测）

| 路径 | 作用 | 体积 |
|---|---|---|
| `hermes_cli/` | `hermes` 命令本体：子命令注册、参数解析、gateway 生命周期 | 33 MB |
| `agent/` | agent 运行时：对话循环、工具调用、上下文组装 | 16 MB |
| `plugins/` | **内置**插件（`cron_providers`、`kanban`、`memory`、`disk-cleanup`…），与 `~/.hermes/plugins/` 的第三方插件是两回事 | 14 MB |
| `acp_adapter/` | ACP（Agent Client Protocol）适配层 | 小 |
| `apps/`、`assets/`、`skins/` | 应用入口、静态资源、主题 | 小 |
| `pyproject.toml` / `poetry.lock` | 依赖声明 | KB 级 |
| `.venv/` | 依赖虚拟环境（Python 3.12 + 全部第三方包） | **151 MB** |
| `.git/` | 完整提交历史 | **1.2 GB** |

源码部分共 **7,544 个 `.py` 文件**（不含 `.venv`），量级约 100 MB。

## 为什么 `full` 层排除 `.venv` 和 `.git`

| 排除项 | 理由 |
|---|---|
| `.venv/` | 内含绝对路径与 `linux-x64` 二进制；换机器、换 Python 版本后必然失效。重建成本：一条 `pip install -e .` 或官方安装器。 |
| `.git/` | 1.2 GB，占整个目录体积的 90% 以上；历史对"能跑起来"没有贡献。重建成本：`git clone`。 |

排除后 `full` 层的 `hermes-agent/` 约 100 MB，而不是 1.4 GB。这也是为什么 `full` 不是默认层——大多数换机场景不需要带源码。

## 恢复方式

**推荐**：用官方安装器重建，而不是从备份搬源码。

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

它会把源码放到 `~/.hermes/hermes-agent`、创建 `.venv`、装依赖、写 `installs/` 与 `tools/`。

**从备份恢复源码后**（`--tier full`）：

```bash
cd ~/.hermes/hermes-agent
.venv/bin/pip install -e .     # 前提：.venv 已由安装器创建
```

注意：备份里没有 `.venv`，所以必须先让安装器生成虚拟环境，再对源码做 editable 安装；不能只解压源码就期望能跑。

## 如何验证它是好的

```bash
ls ~/.hermes/hermes-agent/pyproject.toml          # 源码在位
ls ~/.hermes/hermes-agent/.venv/bin/hermes        # 虚拟环境在位
.venv/bin/python -c "import hermes_cli; print(hermes_cli.__file__)"
```

最后一条应指向 `~/.hermes/hermes-agent/hermes_cli/__init__.py`；如果指向 `site-packages`，说明当前是普通安装而非 editable，源码改了不会生效。

## 与备份层级的关系

| 层级 | 是否包含 `hermes-agent/` | 说明 |
|---|---|---|
| `config` | 否 | 只带配置与技能 |
| `state` | 否 | 再加记忆与会话；代码仍由安装器提供 |
| `full` | 是（排除 `.venv`、`.git`） | 需要"连代码一起搬"时使用，例如自己改过源码 |

## 常见误解

- **"源码在，Hermes 就能跑"** —— 不成立，缺 `.venv` 时依赖全部缺失。
- **"把 `.venv` 一起拷过去最省事"** —— 短期可行，换 Python 版本或换机器后会出现难以定位的 `ImportError`。
- **"内置插件在 `~/.hermes/plugins/`"** —— 不成立，内置插件在此目录的 `plugins/` 下；`~/.hermes/plugins/` 只放第三方插件。
