---
name: secret-gate
description: 提交前的敏感内容闸门。检查即将进入版本库的文件里是否有密钥、私钥、内嵌密码的连接串、私密文档、依赖目录或超大文件；命中即阻止提交并给出文件与行号，可装成 git pre-commit 钩子、接进定时提交脚本或 CI。当用户提到"提交前检查密钥""别把 .env 推上去""仓库里有没有泄露 token""给仓库装个 pre-commit 检查"时使用。
---

# secret-gate

提交前的最后一道闸门。它不判断代码好坏，只回答一个问题：**这批即将入库的文件里，有没有不该公开的东西。**

## 为什么需要它

`git add -A` 是这类事故的主要入口。2026-10-27 的一次真实事故：一份写着"AI 写了 90% 的代码"的私有文档被顺手提交并推到公开仓库，清理需要 `filter-branch` 重写全部历史 + force push，而且远端可能仍缓存旧对象。

规则只有一条：**不可逆的动作，不该交给没有判断力的东西。** 这条闸门就是给自动提交加的那个判断。

## 何时使用

| 场景 | 动作 |
|---|---|
| 仓库要装提交前检查 | `bash scripts/install-hook.sh <仓库根>` |
| 已经装了钩子，想手动体检一遍 | `python scripts/gate.py <仓库> --all` |
| 自动提交脚本接入 | 提交前调用 `--staged`，退出码非 0 就不提交 |
| CI 里兜底 | `--all --json`，解析 `findings` |

## 用法

```bash
python scripts/gate.py --staged            # 只查暂存区（钩子用）
python scripts/gate.py . --all             # 查所有已跟踪文件
python scripts/gate.py . --all --json      # 机器可读
```

退出码：`0` 通过、`1` 有违规、`2` 用法错误或不在 git 仓库。

输出形如：

```
secret_gate: 拦截 2 处（检查 1 个文件）
  .env:1  [env-file] 环境文件常含密钥，应以 .env.example 入库
  .env:1  [openai-key] 疑似 OpenAI/SiliconFlow 密钥
```

## 规则（`rules.json`，改完跑自测）

| 类 | 拦什么 |
|---|---|
| `deny_paths` | `.env`、`*secret*`、`*credential*`、`*.key/.pem/.p12/.pfx`、`id_rsa`/`id_ed25519`、私有文档、`.workbuddy/`、`node_modules/`、`__pycache__/` |
| `content` | `sk-…`、`ghp_…`、`github_pat_…`、`AKIA…`、`-----BEGIN * PRIVATE KEY-----`、`user:pass@host` 形式的内嵌凭据、硬编码的 `api_key/token = "…"` |
| 体积 | 单文件 > 5 MB |
| `allow` | 白名单 glob，默认放过 `**/.env.example` 与 `tests/fixtures/**` |

规则的取舍：**宁可误报，不可漏报**。误报改一次白名单，漏报要重写历史。

## 误报怎么处理

1. 确认内容确实可以公开（示例值、测试假数据）→ 在 `rules.json` 的 `allow` 里按路径加白名单，不要按内容加。
2. 只想放过某一行 → 把那行改成明显的占位符（`your-key-here`），比加规则更安全。
3. 确实需要保存真实样本 → 放 `tests/fixtures/`，该目录默认白名单。

## 自测

```bash
python tests/selftest.py     # 7 个用例：真阳性 3、真阴性 2、白名单 1、JSON 输出 1
```

改规则后必须跑一遍。**没有测试的规则等于没有规则**——它可能在某个版本后静默失效，而你不会知道。

## 文件

| 文件 | 用途 |
|---|---|
| `scripts/gate.py` | 扫描器，stdlib，Win / WSL 通用 |
| `rules.json` | 规则与白名单 |
| `scripts/install-hook.sh` | 装 `pre-commit` 钩子（Git for Windows 自带 sh，无需额外环境） |
| `tests/selftest.py` | 规则回归测试 |

## 已知边界

- 只做**当前文件内容**检查，不扫历史。已被提交的密钥要靠 `git log -S` 或 `gitleaks` 全历史扫描。
- 正则匹配，不做熵检测——高熵随机串若不含已知前缀会漏。需要更强覆盖时换 `gitleaks`，把本技能当"轻量前置"。
- 二进制文件跳过内容检查，只查文件名与体积。
