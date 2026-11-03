# INSTALLATION

本 Skill 是纯文档型，安装 = 把目录放到 agent 能扫描到的 `skills/` 下，没有依赖、没有构建步骤。

## 1. 放置位置

| 场景 | 路径 |
|---|---|
| WorkBuddy（用户级） | `C:\Users\<你>\.workbuddy\skills\project-based-learning\` |
| WorkBuddy（项目级） | `<项目>/.workbuddy/skills/project-based-learning/` |
| Hermes / 其他 agent | 对应 agent 的 `skills/` 目录，或 `~/.hermes/skills/` |

目录名必须与 `SKILL.md` 中的 `name:` 一致（`project-based-learning`），否则部分 agent 会拒绝加载。

## 2. 两种安装方式

**方式一：复制**（简单，但改源码后要重新复制）

```bash
cp -r "源码目录/project-based-learning" ~/.workbuddy/skills/
```

**方式二：符号链接 / junction**（推荐，改源码即生效）

```powershell
# Windows：以管理员或开发者模式运行
New-Item -ItemType Junction -Path "$env:USERPROFILE\.workbuddy\skills\project-based-learning" `
         -Target "D:\path\to\project-based-learning"
```

```bash
# WSL / Linux
ln -sfn /mnt/d/path/to/project-based-learning ~/.workbuddy/skills/project-based-learning
```

> 多 agent 共存的场景，可用 `hermes-portability` 技能里的 `scripts/link-skill.ps1` 批量建链并记录状态。

## 3. 验证加载

1. 重启或刷新 agent（部分客户端需重启）；
2. 随便问一句"帮我规划一个 RAG 项目"，看是否命中本 Skill（回答里应出现 8 大部分结构）；
3. 若未命中：确认目录层级是 `skills/project-based-learning/SKILL.md`，而不是多套了一层目录。

## 4. 升级

```bash
# 复制方式
rm -rf ~/.workbuddy/skills/project-based-learning
cp -r "源码目录/project-based-learning" ~/.workbuddy/skills/

# 链接方式：无需操作，源码更新即生效（可能需要重启 agent 清缓存）
```

升级后按 `TESTING.md` 第 4 节做一次回归：同一输入重新生成，结构不能缩水。

## 5. 卸载

删除目录即可，本 Skill 不写任何外部状态（不建数据库、不写缓存、不改配置）。

## 6. 已知环境差异

| 环境 | 注意 |
|---|---|
| Windows + 中文路径 | 可用；但 junction 目标路径含空格时要用引号 |
| WSL | 跨 `/mnt/c` 链接可用，但 Obsidian 双链解析以 vault 内路径为准 |
| 只有一个 agent | 直接复制即可，不必建链 |
