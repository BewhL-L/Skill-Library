# 常见问题

## 安装与环境

### Q: 需要安装哪些依赖？
A: 本工具仅使用 Python 标准库，**无需安装任何第三方依赖**。只需 Python 3.8+ 即可运行。

### Q: 支持哪些操作系统？
A: Windows / macOS / Linux 均支持。路径处理使用 `pathlib`，编码统一使用 UTF-8。

### Q: 如何作为豆包 Skill 使用？
A: 将整个文件夹复制到豆包用户技能目录：
- Windows: `C:\Users\{用户名}\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\.user_skills\`
- macOS: `~/Library/Application Support/Doubao/User Data/Default/.doubao/agent_mode/workspace/.user_skills/`

然后重启豆包即可。

---

## 使用相关

### Q: audit 和 optimize 有什么区别？
A:
- **audit**（健康检查）：只读操作，评估 Skill 现状，生成报告和建议，不修改任何文件。
- **optimize**（自动优化）：会修改文件，自动补全缺失的文档和配置。

建议先运行 audit 了解现状，再用 optimize 的 `--dry-run` 预览，最后执行优化。

### Q: --dry-run 是什么意思？
A: 预览模式。只显示将要执行的操作和将要创建的文件，**不会实际修改任何文件**。建议首次使用时先加 `--dry-run` 确认效果。

### Q: --only 参数怎么用？
A: 指定只优化某些部分，多个用逗号分隔：
```bash
# 只优化文档
python skill-opt.py optimize --path ./my-skill --only docs

# 只优化配置
python skill-opt.py optimize --path ./my-skill --only config

# 优化文档和配置
python skill-opt.py optimize --path ./my-skill --only docs,config
```

可选值：`docs`（文档）、`code`（代码）、`config`（配置）。

### Q: 生成的测试都是 pass，有用吗？
A: 生成的测试是**模板**，包含 TODO 注释。你需要根据实际功能填充测试逻辑。模板的作用是：
1. 提供测试文件结构
2. 提示需要测试的场景（正常/边界/错误）
3. 统一测试命名和风格

### Q: 生成的文档内容需要修改吗？
A: 是的。自动生成的文档是**基础模板**，你需要：
- API 文档：补充函数的详细说明和示例
- FAQ：根据真实用户问题补充
- 使用案例：替换为真实场景
- 架构文档：根据实际架构修改

---

## 优化方法论

### Q: 为什么是 25 轮？可以少一些吗？
A: 25 轮是基于实战经验总结的**完整优化路径**，分为 5 个阶段。你可以：
- 只做前 5 轮（基础完善）→ 达到 B 级
- 做到第 10 轮（质量提升）→ 达到 A-级
- 做到第 15 轮（工程化）→ 达到 A 级
- 全部 25 轮 → 达到 S 级

根据你的目标选择合适的轮次。

### Q: 每轮优化需要多长时间？
A: 取决于 Skill 的现状和复杂度：
- 第 1-5 轮（基础）：每轮 1-2 小时
- 第 6-10 轮（质量）：每轮 2-4 小时
- 第 11-15 轮（工程化）：每轮 1-2 小时（很多可自动化）
- 第 16-20 轮（文档）：每轮 2-3 小时
- 第 21-25 轮（打磨）：每轮 1-2 小时

总计约 40-60 小时，可以分散到 2-4 周完成。

### Q: audit 分数低怎么办？
A: 按以下优先级提升：
1. 🔴 先修复 P0 问题（功能 Bug、核心文档缺失）
2. 🟠 再修复 P1 问题（代码质量、测试、工程化）
3. 🟡 然后完善 P2（文档、示例、性能）
4. 🟢 最后追求 P3（社区、高级功能）

运行 `python skill-opt.py optimize --auto` 可以自动完成很多 P1/P2 项。

### Q: 优化到什么程度算好？
A: 参考 [QUALITY-STANDARDS.md](QUALITY-STANDARDS.md)：
- 自用：B 级（70+ 分）即可
- 分享给朋友：A 级（85+ 分）
- 公开发布：S 级（95+ 分）

---

## 常见错误

### Q: 提示 "路径不存在"
A: 检查 `--path` 参数是否正确，路径可以是相对路径或绝对路径：
```bash
# 相对路径
python skill-opt.py audit --path ./my-skill

# 绝对路径
python skill-opt.py audit --path "C:\Users\name\my-skill"
```

### Q: 中文乱码怎么办？
A: Windows 用户设置环境变量：
```bash
set PYTHONIOENCODING=utf-8
```
或使用 PowerShell：
```powershell
$env:PYTHONIOENCODING="utf-8"
```

### Q: 生成的文件覆盖了原有内容怎么办？
A: 本工具的设计原则是**不覆盖已有文件**。如果文件已存在，会跳过并提示 "已存在，跳过"。但建议在优化前备份重要文件。

### Q: audit 报告中的维度权重是怎么算的？
A: 8 大维度的权重：
- 元数据：15%
- 文档：20%
- 代码质量：20%
- 测试：15%
- 工程化：10%
- 模板：10%
- 易用性：5%
- 可维护性：5%

总分 = Σ（维度得分 × 权重）

---

## 高级用法

### Q: 可以集成到 CI/CD 吗？
A: 可以。示例 GitHub Actions：
```yaml
- name: Skill Quality Check
  run: |
    python skill-opt.py audit --path . --format json --output report.json
    # 可以设置质量门禁，总分低于 80 则失败
```

### Q: 可以批量优化多个 Skill 吗？
A: 可以，写一个批处理脚本：
```bash
# Windows
for /d %d in (*) do python skill-opt.py all --path "%d"

# macOS/Linux
for dir in */; do python skill-opt.py all --path "$dir"; done
```

### Q: 如何自定义优化规则？
A: 修改 `scripts/` 目录下的脚本：
- `audit-skill.py`：自定义检查项和权重
- `optimize-skill.py`：自定义生成的文档和配置模板
- `generate-docs.py`：自定义文档格式
- `generate-tests.py`：自定义测试模板

---

## 其他

### Q: 如何贡献代码？
A: 参考 CONTRIBUTING.md，流程：
1. Fork 项目
2. 创建功能分支
3. 提交更改（遵循 Conventional Commits）
4. 运行测试
5. 提交 Pull Request

### Q: 有商业支持吗？
A: 联系项目维护者获取商业支持、定制开发、培训等服务。

### Q: 如何报告 Bug？
A: 在 GitHub 提交 Issue，包含：
1. 问题描述
2. 复现步骤
3. 预期行为
4. 实际行为
5. 环境信息（OS/Python版本/工具版本）

---

> **没有找到你的问题？**
> 请提交 Issue 或查看 [OPTIMIZATION-GUIDE.md](OPTIMIZATION-GUIDE.md) 获取更详细的说明。
