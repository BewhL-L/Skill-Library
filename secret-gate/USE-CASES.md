# 使用场景

## 场景 1：日常开发仓库装闸门

**需求**：防止 `.env`、私钥、连接串被 `git add -A` 顺手提交。

```bash
bash scripts/install-hook.sh .
```

之后每次 `git commit` 都会先扫描暂存区；命中即拒绝提交，工作区文件原样保留。

**验收**：暂存一个假密钥（`sk-` + 30 个字符），提交必须红；删除后提交必须绿。

## 场景 2：CI 里兜底

**需求**：钩子可以被 `--no-verify` 绕过，最后一道防线放在 CI。

```yaml
- run: python path/to/secret-gate/scripts/gate.py . --all --json > gate.json
- run: python -c "import json,sys; sys.exit(1 if json.load(open('gate.json'))['findings'] else 0)"
```

## 场景 3：定时自动提交的前置检查

**需求**：无人值守的自动提交（`git-autocommit.ps1` 每日打包多个仓库）不能把半成品或密钥推上去。

做法：自动提交脚本在 `git add -A` 之后、`git commit` 之前调用 `gate.py --staged`；退出码非 0 就 `git reset` 并记日志，**不提交、不推送**。规则只有一份（`rules.json`），脚本里不重复维护正则。

**关键设计**：fail-closed。闸门不可用时宁可不提交，也不要"看起来提交成功"。

## 场景 4（不属于本技能）：清理已经被提交的密钥

本技能只管**提交前**。已经进历史的密钥需要 `git log -S 'sk-'` 定位、`filter-branch` / `git filter-repo` 重写历史、`push --force`，并在对方支持时申请清理缓存。这类工作见 `gitleaks` 的全历史扫描与各平台的密钥轮换流程。
