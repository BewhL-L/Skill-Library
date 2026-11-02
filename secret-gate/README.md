# secret-gate

提交前的敏感内容闸门。在 `git commit` 之前检查即将入库的文件里有没有密钥、私钥、内嵌凭据的连接串、私密文档、依赖目录或超大文件——命中即阻止提交，并给出 `文件:行 [规则] 原因`。

它不判断代码好坏，只回答一个问题：**这批即将入库的文件里，有没有不该公开的东西。**

## 为什么需要它

`git add -A` 是这类事故的主要入口。一次真实的代价：私有文档被顺手提交并推到公开仓库，清理要 `filter-branch` 重写全部历史 + force push，而远端仍可能缓存旧对象。规则只有一条——**不可逆的动作，不该交给没有判断力的东西**。

## 三种用法

```bash
python scripts/gate.py --staged              # pre-commit 钩子用，只查暂存区
python scripts/gate.py <仓库> --all          # 体检：查所有已跟踪文件
python scripts/gate.py <仓库> --all --json   # 机器可读，给 CI 用
```

退出码：`0` 通过、`1` 有违规、`2` 用法错误或不在 git 仓库。

## 文件

| 文件 | 用途 |
|---|---|
| `SKILL.md` | 给 agent 的使用说明与规则表 |
| `rules.json` | 路径规则、内容正则、白名单、体积上限 |
| `scripts/gate.py` | 扫描器，stdlib，Win / WSL 通用 |
| `scripts/install-hook.sh` | 给仓库装 `pre-commit` 钩子 |
| `tests/test_gate.py` | 规则回归测试（7 例） |

## 文档

- [快速开始](QUICKSTART.md) —— 三条命令跑通
- [使用场景](USE-CASES.md) —— 装钩子 / CI / 体检
- [常见问题](FAQ.md) —— 误报、漏报、钩子不生效
- [安装](INSTALLATION.md) · [安全边界](SECURITY.md) · [贡献](CONTRIBUTING.md) · [变更日志](CHANGELOG.md)

## 许可

MIT
