# INSTALLATION

## 前置条件

| 项 | 要求 | 检查命令 |
|---|---|---|
| 系统 | Windows + WSL2（Ubuntu），或原生 Linux | `uname -a` |
| Shell | bash 4+ | `bash --version \| head -1` |
| Python | 3.8+（仅用于 SQLite 备份与 manifest） | `python3 --version` |
| 工具 | `tar`、`gzip`、`git`（可选） | `tar --version` |
| Docker | 仅在备份 mem0 服务时需要 | `docker ps` |

缺少 `python3` 时脚本会直接退出并给出提示，不会产生半份备份。

## 安装位置

技能放在 **Windows 侧** 的用户技能目录：

```
C:\Users\<你>\.workbuddy\skills\hermes-portability\
```

WSL 里通过 `/mnt/c` 访问：

```bash
SK=/mnt/c/Users/23981/.workbuddy/skills/hermes-portability
ls "$SK/scripts"        # 应看到 export.sh restore.sh bootstrap.sh verify.sh
```

也可以整体复制进 WSL（`cp -r "$SK" ~/.workbuddy/skills/`），之后路径换成 `~`。两种方式等价，区别只是备份脚本的"位置"。

## 首次运行

```bash
# 1. 体检：确认当前安装可被正确识别
bash "$SK/scripts/verify.sh"

# 2. 备份
bash "$SK/scripts/export.sh"

# 3. 看产物
ls ~/hermes-backup/hermes-*/
```

首次 `verify.sh` 出现 `WARN` 属正常（数据库被运行中的 Hermes 占用、插件未全部安装等）。

## 升级

技能本身无状态，覆盖目录即可：

```bash
# 备份旧版（可选）
mv ~/.workbuddy/skills/hermes-portability ~/.workbuddy/skills/hermes-portability.bak
# 解压新版 zip 到 skills/
```

覆盖后重跑 `verify.sh`，确认脚本仍能识别当前 Hermes 版本。

## 卸载

```bash
rm -rf ~/.workbuddy/skills/hermes-portability
```

已生成的备份目录不受影响（它们不在技能目录内）。

## 与 Hermes 版本的关系

脚本只依赖**文件布局**（`~/.hermes` 下的目录名），不依赖 Hermes 的 Python API，因此小版本升级通常无需改动。

若某次大版本调整了目录名（例如 `plugins/` 改名），`verify.sh` 会因"启用了但找不到"而报警——这是设计上的早期信号，而不是静默失效。
