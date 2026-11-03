# DEBUGGING

排查顺序固定为三步：**看 JSON 报告 → 单维度复跑 → 造最小复现**。不要一上来读 899 行源码。

## 1. 先拿结构化现场

```bash
python scripts/audit-skill.py --path <技能目录> --format json --output report.json
```

JSON 里有三样关键信息，比终端彩色输出有用：

| 字段 | 用途 |
|---|---|
| `dimensions.*.issues` | 每条扣分对应的原始问题，含 severity |
| `weights_used` | 本次用了哪套权重（类型检测会影响权重） |
| `skill_type` / `type_info` | 判定成什么类型，是否符合预期 |

分数不对时，先看 `weights_used`——很可能是类型被判错，而不是规则坏了。

## 2. 症状 → 原因 → 处理

| 症状 | 最可能的原因 | 验证 / 处理 |
|---|---|---|
| 明明有 frontmatter，却报「缺少 frontmatter」 | 文件开头带 UTF-8 BOM（`EF BB BF`） | `python -c "print(open('SKILL.md','rb').read(3))"`；1.9.3 起读取统一用 `utf-8-sig`，若仍报错说明是别的编码（UTF-16/GBK） |
| 分数整体偏高/偏低，但每项都"看起来对" | 类型判错导致换了权重表 | 看 JSON 的 `skill_type`；纯文档型技能被当成代码驱动型时，code_quality 会拖分 |
| 类型注解覆盖率异常低 | 正则只匹配**单行**签名，多行 `def (` 续行不被计入 | 把多行签名合并成单行，或接受该误差（规则已知局限） |
| 某个技能 usability 只有 80，但明明用了 argparse | 1.9.4 之前该维度只看第一个 `.py` 文件 | 升级到 1.9.4（已改为扫描全部源文件）；临时可把带 argparse 的文件排到前面 |
| templates 恒为 30 | `templates/`、`assets/`、`examples/`、`references/` 一个都没有 | 建任一目录即可 +50；再建 `examples/` +20 |
| 文档维度总是 90 | 缺 `TESTING.md`、`DEBUGGING.md`（各 −5） | 补齐即满分 |
| 在 Windows 上审计报 `invalid uri authority` 之类 | UNC 路径（`\\wsl.localhost\...`）被当成 URI authority | 改用 `\\wsl$\...` 或先复制到本地盘；脚本内 SQLite 相关代码已做回退 |
| 中文路径下输出乱码 | 终端代码页非 UTF-8 | `chcp 65001`，或用 `--format json` 输出后读文件 |
| `python -m pytest` 报 `No module named pytest` | 未装开发依赖 | `pip install -r requirements.txt` |

## 3. 造最小复现

不要拿真实技能反复试，建一个三文件的最小技能：

```bash
mkdir -p /tmp/min-skill && cd /tmp/min-skill
printf -- '---\nname: min-skill\ndescription: 用于复现的最小技能\n---\n\n# min\n' > SKILL.md
mkdir scripts && printf 'def f(x):\n    return x\n' > scripts/a.py
python /path/to/skill-optimizer/scripts/audit-skill.py --path . --format json
```

预期：metadata 满分、code_quality 因无注解扣分、templates 30、documentation 很低。任何与预期的偏差都是规则问题，而不是目标技能的问题。

## 4. 脚本无法直接 import 时

`scripts/` 下的文件名带连字符（如 `audit-skill.py`），**不能** `import audit-skill`。测试与二次开发统一用：

```python
import importlib.util, pathlib
spec = importlib.util.spec_from_file_location("audit_skill", pathlib.Path("scripts/audit-skill.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
```

`tests/conftest.py` 已把项目根加入 `sys.path`，但那只解决包导入，不解决连字符文件名。

## 5. 已知误判（不是 bug，是规则边界）

1. **bash 脚本被判「未使用 argparse」**：可用性维度按 Python 生态设计，bash 用 `case` 解析参数属等价实现。
2. **检查器/生成器类技能 templates 得 30**：它不产出模板文件，目录本就不该存在。
3. **单行正则统计签名**：多行 `def` 与装饰器链可能漏计。

> **1.9.4 已修复的两项**（原先记在此处）：
> - 可用性维度只扫描第一个 `.py` 文件就 `break`，文件顺序会决定 argparse 判定；
> - 代码质量维度把 `tests/` 里的函数计入注解与 docstring 覆盖率。
> 现在统一走 `iter_source_files()`：跳过依赖/缓存目录与测试目录，扫描全部源码文件。

遇到以上情况，正确做法是**在结论里注明"规则不适用"**，而不是去改目标技能迎合规则。

## 6. 回滚

规则改动导致大面积误判时：

```bash
git -C <repo> diff scripts/audit-skill.py     # 先看改了什么
git -C <repo> checkout -- scripts/audit-skill.py
```

没有 git 时，审计器本身不带备份；改之前先复制一份 `audit-skill.py.bak`。
