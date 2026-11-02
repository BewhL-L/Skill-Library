# 快速开始

## 前提

Python 3.8+（**无第三方依赖**）与 git。Windows 上用 Git Bash 执行钩子相关命令。

## 三条命令跑通

```bash
# 1) 体检：扫当前仓库所有已跟踪文件
python scripts/gate.py <仓库根> --all

# 2) 装成 pre-commit 钩子（以后每次 commit 自动拦）
bash scripts/install-hook.sh <仓库根>

# 3) 验证闸门真的会拦（故意造一个假密钥）
echo 'sk-'$(printf 'a%.0s' {1..30}) > leak.txt
git add leak.txt && git commit -m "should fail"    # 必须被拒绝
rm leak.txt && git reset
```

## 看懂输出

```
gate: 拦截 1 处（检查 1 个文件）
  leak.txt:1  [openai-key] 疑似 OpenAI/SiliconFlow 密钥

处置：移除该内容，或确认无误后在 rules.json 的 allow 里加白名单。
```

`文件:行 [规则] 原因` 三段对应 `rules.json` 里的规则 id，改规则就改那里。

## 下一步

- 规则与白名单：`rules.json`
- 误报怎么处理：[FAQ.md](FAQ.md)
- 能力边界（不扫历史、不做熵检测）：[SECURITY.md](SECURITY.md)
