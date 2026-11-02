# API

## 命令行

```bash
python scripts/gate.py [path] [--staged | --all] [--rules <rules.json>] [--json]
```

| 参数 | 说明 |
|---|---|
| `path` | 仓库或目录，默认 `.` |
| `--staged` | 只检查暂存区（`git diff --cached --name-only`），pre-commit 钩子用 |
| `--all` | 检查所有已跟踪文件（`git ls-files`） |
| `--rules` | 规则文件路径，默认 `<技能目录>/rules.json` |
| `--json` | 机器可读输出 |

`--staged` 与 `--all` 互斥；都不给时按 `path` 递归扫描文件系统（不看 git）。

## 退出码

| 码 | 含义 |
|---|---|
| 0 | 通过 |
| 1 | 发现违规（stderr 有清单） |
| 2 | 用法错误 / 不在 git 仓库 / 规则文件缺失 |

## 文本输出

```
gate: 拦截 2 处（检查 37 个文件）
  backend/.env:1  [env-file] 环境文件常含密钥，应以 .env.example 入库
  app/config.py:12  [openai-key] 疑似 OpenAI/SiliconFlow 密钥

处置：移除该内容，或确认无误后在 rules.json 的 allow 里加白名单。
```

通过时打印 `gate: 通过（检查 N 个文件）`。

## JSON 输出

```json
{
  "checked": 37,
  "findings": [
    {"file": "backend/.env", "line": 1, "rule": "env-file", "why": "环境文件常含密钥，应以 .env.example 入库"}
  ]
}
```

`line` 为 0 表示文件级命中（文件名规则、体积），否则是行号（内容规则）。

## 规则文件 `rules.json`

| 字段 | 类型 | 含义 |
|---|---|---|
| `deny_paths[]` | `{id, pattern, why}` | 文件名/路径正则 |
| `content[]` | `{id, pattern, why}` | 内容正则，逐行匹配 |
| `allow[]` | glob 数组 | 白名单（相对路径），命中则整文件跳过 |
| `max_file_bytes` | int | 单文件体积上限，超出即拦截 |
