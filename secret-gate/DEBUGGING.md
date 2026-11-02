# 调试

## 钩子没生效

```bash
# 1) 单独跑钩子，看输出
bash .git/hooks/pre-commit

# 2) 看钩子内容里的路径是否还有效（技能目录被移动过就会失效）
cat .git/hooks/pre-commit

# 3) 确认 git 真的在跑钩子（故意造一个会被拦的文件）
echo 'sk-'$(printf 'a%.0s' {1..30}) > leak.txt
git add leak.txt && git commit -m "should fail"
```

三步定位：第 1 步报错 → 钩子/路径问题；第 1 步通过但第 3 步放行 → git 没执行钩子（检查 `.git/hooks/pre-commit` 是否可执行、是否用了 `--no-verify`）。

## 该拦的没拦

| 可能原因 | 怎么确认 |
|---|---|
| 规则写错 | 在 `rules.json` 里找到 `rule` id，看 `pattern` 是否真匹配该行（正则里 `\.` 要转义） |
| 文件在白名单 | `allow` 是整文件跳过；`git check-ignore` 无关，看的是 `rules.json` |
| 二进制扩展名 | `.png/.zip/...` 只查文件名与体积，不查内容 |
| 文件超过体积上限 | 超限会拦（`file-too-large`），但不会继续读内容 |
| 扫描的不是你以为的范围 | `--staged` 只看暂存区；`git add` 过的才算 |

## 误报太多

1. 从输出里抄 `rule` id，去 `rules.json` 定位 pattern；
2. 优先改内容为占位符；不行再按**路径**加 `allow`；
3. 如果某条规则对整个仓库误报，说明 pattern 太宽——收窄它比堆白名单更治本。

## 编码问题（Windows）

- PowerShell 脚本含中文时必须存成 **UTF-8 with BOM**，否则 PS 5.1 按 GBK 读，字符串会被截断成语法错误。
- git 输出非 ASCII 路径会被转义成 `\346\226\207…`：调用 git 时加 `-c core.quotepath=false`，并把 `[Console]::OutputEncoding` 设为 UTF-8。

## Python 版本

`gate.py` 只用标准库，Python 3.8+ 即可。若报 `ImportError`，说明被当成了别的解释器——用 `python -V` 确认，Windows 上注意别用 WindowsApps 的商店占位程序。
