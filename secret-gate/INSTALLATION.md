# 安装

## 系统要求

- Python 3.8+（**只用标准库，无 pip 依赖**）
- git（钩子由 Git for Windows 自带的 sh 执行，无需额外 shell）

## 给一个仓库装上闸门

```bash
bash scripts/install-hook.sh <仓库根>
```

它写入 `<仓库根>/.git/hooks/pre-commit`，内容只有一行：调用本技能的 `gate.py --staged`。已有非本技能钩子时先备份为 `pre-commit.bak.<时间戳>`。

卸载：

```bash
rm <仓库根>/.git/hooks/pre-commit
```

## 手动调用（不装钩子）

```bash
python scripts/gate.py <仓库根> --staged     # 只查暂存区
python scripts/gate.py <仓库根> --all        # 查所有已跟踪文件
python scripts/gate.py <仓库根> --all --json # 给 CI 解析
```

## 给 agent 装这个技能

技能目录只需可读；推荐做成链接，源码改完立刻生效：

- Windows：junction（无需管理员权限）
- Linux / WSL：`ln -sfn <源码目录> <安装位>`

## 验证

```bash
python tests/test_gate.py     # 7 个回归用例，应全绿
```
