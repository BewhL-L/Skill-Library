# 使用案例

> skill-optimizer 的真实使用场景和最佳实践。

---

## 目录

- [案例一：优化一个新建的纯文档型 Skill](#案例一优化一个新建的纯文档型-skill)
- [案例二：优化一个代码驱动型 Skill](#案例二优化一个代码驱动型-skill)
- [案例三：批量优化一个目录下的所有 Skill](#案例三批量优化一个目录下的所有-skill)
- [案例四：追踪优化效果（优化前后对比）](#案例四追踪优化效果优化前后对比)
- [案例五：持续集成（定期维护）](#案例五持续集成定期维护)

---

## 案例一：优化一个新建的纯文档型 Skill

### 场景

你刚创建了一个纯文档型 Skill（如 `algorithm-practice-trainer`），只有 SKILL.md 和 references/ 目录，想快速提升质量。

### 操作步骤

```bash
# 1. 先检测类型，确认是纯文档型
python scripts/skill-opt.py type --path ./algorithm-practice-trainer

# 预期输出：
# 📋 类型: 纯文档型
# 📊 Audit 评估模式: doc-only 模式（8个维度）
# 🔧 Optimize 适用范围: docs, basic_config

# 2. 运行健康检查，了解当前状况
python scripts/skill-opt.py audit --path ./algorithm-practice-trainer

# 预期输出：
# 总分: 50-60/100（C级）
# 低分维度：documentation（缺少README/CHANGELOG等）
# 高分维度：doc_structure / trigger_scenarios / output_spec / references_depth

# 3. 预览自动优化将执行的操作
python scripts/skill-opt.py optimize --path ./algorithm-practice-trainer --dry-run

# 预期输出：
# 将创建：README.md, CHANGELOG.md, FAQ.md, .gitignore, .editorconfig 等
# 自动跳过：pyproject.toml, Makefile, CI/CD（纯文档型不适用）

# 4. 执行自动优化
python scripts/skill-opt.py optimize --path ./algorithm-practice-trainer --auto

# 5. 再次运行健康检查，验证优化效果
python scripts/skill-opt.py audit --path ./algorithm-practice-trainer

# 预期输出：
# 总分: 75-85/100（B级）
# 提升约 20-25 分
```

### 关键要点

- 纯文档型**不会**生成 pyproject.toml、Makefile、CI/CD 等不适用的文件
- 纯文档型**不会**生成测试文件（无代码可测试）
- 重点关注 4 个文档型专属维度：doc_structure / trigger_scenarios / output_spec / references_depth

---

## 案例二：优化一个代码驱动型 Skill

### 场景

你有一个代码驱动型 Skill（如 `obsidian-knowledge-base-creator`），有完整的 Python 脚本，但缺少测试和工程化配置。

### 操作步骤

```bash
# 1. 检测类型
python scripts/skill-opt.py type --path ./obsidian-knowledge-base-creator

# 预期输出：
# 📋 类型: 混合型 或 代码驱动型
# 📊 Audit 评估模式: hybrid 模式（11个维度）或 code-driven 模式（8个维度）

# 2. 健康检查
python scripts/skill-opt.py audit --path ./obsidian-knowledge-base-creator

# 重点关注：
# - code_quality：类型注解覆盖、异常处理
# - testing：测试覆盖率
# - engineering：CI/CD、pre-commit、lint

# 3. 只优化文档和配置（先不碰代码）
python scripts/skill-opt.py optimize --path ./obsidian-knowledge-base-creator --only docs,config

# 4. 生成测试
python scripts/skill-opt.py tests --path ./obsidian-knowledge-base-creator --type all

# 5. 生成 API 文档
python scripts/skill-opt.py docs --path ./obsidian-knowledge-base-creator --type api

# 6. 一键全流程（检查→优化→文档→测试→验证）
python scripts/skill-opt.py all --path ./obsidian-knowledge-base-creator
```

### 关键要点

- 代码驱动型会生成完整的工程化配置（pyproject.toml、Makefile、CI/CD、pre-commit）
- 测试生成会自动解析 Python 函数，生成单元测试模板
- API 文档会自动解析函数签名和 docstring
- `all` 命令会执行完整流程，并在最后显示优化前后对比

---

## 案例三：批量优化一个目录下的所有 Skill

### 场景

你有一个目录包含 16 个 Skill，想一次性优化所有 Skill 并生成对比报告。

### 操作步骤

```bash
# 1. 预览批量优化（不修改文件）
python scripts/skill-opt.py batch --path ./my-skills --dry-run --output batch-preview.json

# 预期输出：
# 发现 Skill: 16 个
# 逐个处理...
# 批量优化报告：
# Skill名称        类型       优化前  优化后  变化   更改
# algorithm-practice-trainer  doc-only  55.6  55.6  +0.0  6
# bug-troubleshooter          doc-only  52.3  52.3  +0.0  8
# ...
# 成功: 16/16 | 平均提升: +0.0 分 | 总提升: +0.0 分

# 2. 确认预览结果无误后，执行实际批量优化
python scripts/skill-opt.py batch --path ./my-skills --output batch-report.json

# 预期输出：
# 成功: 16/16 | 平均提升: +20.5 分 | 总提升: +328.0 分

# 3. 查看批量报告（JSON格式）
cat batch-report.json | python -m json.tool
```

### 批量报告 JSON 结构

```json
{
  "batch_time": "2026-09-01T10:00:00",
  "base_dir": "/path/to/my-skills",
  "total_skills": 16,
  "success_count": 16,
  "total_score_diff": 328.0,
  "avg_score_diff": 20.5,
  "results": [
    {
      "name": "algorithm-practice-trainer",
      "type": "doc-only",
      "before": 55.6,
      "after": 78.5,
      "diff": 22.9,
      "changes": 6,
      "errors": 0
    }
  ]
}
```

### 关键要点

- batch 命令会自动跳过失败的 Skill，继续处理其他 Skill
- dry-run 模式下分数不变（+0.0），但更改数显示将执行的操作
- 批量报告包含每个 Skill 的详细数据，可用于后续分析
- 建议先 dry-run 预览，确认无误后再实际执行

---

## 案例四：追踪优化效果（优化前后对比）

### 场景

你对一个 Skill 进行了多轮优化，想精确追踪每一轮的优化效果。

### 操作步骤

```bash
# 1. 优化前：保存基线报告
python scripts/skill-opt.py audit --path ./my-skill --format json --output round0-before.json

# 2. 第一轮优化：只补全文档
python scripts/skill-opt.py optimize --path ./my-skill --only docs
python scripts/skill-opt.py audit --path ./my-skill --format json --output round1-after.json

# 3. 对比第一轮优化效果
python scripts/skill-opt.py diff --before round0-before.json --after round1-after.json

# 预期输出：
# 📈 总分对比:
#    优化前: 55.6/100
#    优化后: 70.2/100
#    变化: +14.6 分
#
# 📊 各维度对比:
#    documentation  35.0 → 75.0  +40.0 ✅ 提升
#    metadata       95.0 → 95.0   +0.0 ➖ 持平
#    ...

# 4. 第二轮优化：添加工程化配置
python scripts/skill-opt.py optimize --path ./my-skill --only config
python scripts/skill-opt.py audit --path ./my-skill --format json --output round2-after.json

# 5. 对比第二轮优化效果
python scripts/skill-opt.py diff --before round1-after.json --after round2-after.json

# 6. 总对比（从基线到最终）
python scripts/skill-opt.py diff --before round0-before.json --after round2-after.json --output total-diff.json
```

### 关键要点

- diff 命令可以对比任意两个 audit 报告，不限于相邻轮次
- 逐维度对比可以精确知道每轮优化了哪些方面
- 问题数对比可以验证优化是否真正减少了问题
- 建议每轮优化后都保存 audit 报告，便于回溯

---

## 案例五：持续集成（定期维护）

### 场景

你有多个 Skill 在持续维护，想定期运行健康检查，监控质量变化。

### 操作步骤

#### Windows 定时任务（PowerShell）

```powershell
# 创建每周运行的健康检查脚本
$checkScript = @'
$skillsDir = "C:\path\to\my\skills"
$reportDir = "C:\path\to\reports"
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"

Get-ChildItem $skillsDir -Directory | Where-Object { Test-Path "$($_.FullName)\SKILL.md" } | ForEach-Object {
    $reportFile = "$reportDir\$($_.Name)-$timestamp.json"
    python "C:\path\to\skill-optimizer\scripts\audit-skill.py" --path $_.FullName --format json --output $reportFile
    Write-Output "Checked: $($_.Name) -> $reportFile"
}
'@

$checkScript | Out-File "C:\path\to\weekly-check.ps1" -Encoding utf8

# 创建定时任务（每周一早上9点运行）
schtasks /create /tn "SkillWeeklyCheck" /tr "powershell -File C:\path\to\weekly-check.ps1" /sc weekly /d MON /st 09:00
```

#### Linux/macOS cron 任务

```bash
# 编辑 crontab
crontab -e

# 添加每周一早上9点运行的任务
0 9 * * 1 /path/to/python /path/to/skill-optimizer/scripts/skill-opt.py batch --path /path/to/skills --output /path/to/reports/weekly-$(date +\%Y\%m\%d).json
```

### 质量监控指标

定期关注以下指标：

| 指标 | 健康范围 | 警告阈值 | 行动 |
|------|---------|---------|------|
| audit 总分 | >= 70 | < 60 | 运行 optimize 自动优化 |
| critical 问题数 | 0 | > 0 | 立即修复 |
| 文档完整性 | >= 70 | < 50 | 补全缺失文档 |
| 代码质量（代码型） | >= 80 | < 60 | 添加类型注解和异常处理 |
| 测试覆盖（代码型） | >= 50 | < 30 | 运行 generate-tests.py |

---

## 最佳实践总结

1. **先检测类型，再优化**：用 `type` 命令确认 Skill 类型，避免盲目套用代码型优化
2. **先预览，后执行**：用 `--dry-run` 预览优化操作，确认无误后再实际执行
3. **保存每轮报告**：每轮优化前后都保存 audit 报告，用 `diff` 追踪效果
4. **批量优化用 batch**：多个 Skill 时用 `batch` 命令，一次性处理并生成对比报告
5. **定期维护**：用定时任务定期运行 audit，监控质量变化
6. **关注专属维度**：纯文档型关注 4 个文档型专属维度，代码型关注代码/测试/工程化维度

---

> **版本**：v1.8.0
>
> **最后更新**：2026-09-01
