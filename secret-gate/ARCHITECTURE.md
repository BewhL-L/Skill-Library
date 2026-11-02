# 架构

## 扫描流程

```
收集文件            --staged: git diff --cached --name-only
                    --all:    git ls-files
                    路径:     目录递归（跳过二进制扩展名）
     │
     ▼
白名单（allow）      命中 → 整文件跳过
     │
     ▼
文件名规则          deny_paths 正则 → 记录 file:0
     │
     ▼
体积上限            > max_file_bytes → 记录 file:0，不再读内容
     │
     ▼
内容规则            逐行跑 content 正则 → 记录 file:line
     │
     ▼
退出码              有 findings → 1；否则 0
```

## 设计取舍

| 取舍 | 理由 |
|---|---|
| **stdlib only** | 任何仓库可以直接调用，不需要 venv / pip install；这是它能当"通用闸门"的前提 |
| **fail-closed** | 找不到 `gate.py` 或扫描器异常时**拒绝提交**。静默放行会让防线失效而无人察觉 |
| **规则只有一份** | 定时提交脚本（`git-autocommit.ps1`）也调用同一个 `gate.py`，正则不在两处维护 |
| **不做熵检测 / 不扫历史** | 只拦"提交前"这一段，保持简单可靠；全历史扫描交给 `gitleaks` |
| **白名单按路径不按内容** | 内容白名单会永久放过某模式，真正密钥常与误报同形；路径白名单可控 |

## 与外部的接线

| 接入点 | 方式 | 语义 |
|---|---|---|
| git hook | `scripts/install-hook.sh` 写 `pre-commit`，执行 `gate.py --staged` | 每次提交都过闸门 |
| 自动提交 | `git-autocommit.ps1` 在 `git add -A` 后、commit 前调用 | 无人值守场景的前置检查 |
| CI | `gate.py . --all --json` | 钩子可被 `--no-verify` 绕过，CI 是最后一道 |

## 已知边界

- 正则匹配**已知模式**，不承诺"检测一切密钥"（见 [SECURITY.md](SECURITY.md)）。
- 二进制文件只查文件名与体积，不查内容。
- 白名单会让整个文件跳过检查；加白名单前先确认那行确实可以公开。
