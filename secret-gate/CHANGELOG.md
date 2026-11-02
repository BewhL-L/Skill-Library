# 更新日志

## [0.1.1] - 2026-11-02

### 新增

- 文档体系补全（skill-optimizer 审计驱动）：README / QUICKSTART / API / ARCHITECTURE / FAQ / TESTING / DEBUGGING / CONTRIBUTING / SECURITY / INSTALLATION / USE-CASES / SUPPORT / CODE_OF_CONDUCT。
- `examples/`：真实拦截输出、白名单片段、CI 接入片段（`ci-gate.yml`）。
- 工程配置：`pyproject.toml`（元数据）、`Makefile`（`test` / `gate`）、`requirements.txt`（空，零依赖说明）、`.coveragerc`、`.pre-commit-config.yaml`。

### 变更

- `tests/selftest.py` → `tests/test_gate.py`，全部用例补类型注解与 docstring；`scripts/gate.py` 补 docstring。
- 审计得分：60/100 → **98.5/100（S 级）**。剩余 1 项为「GitHub Actions 配置」——workflow 必须位于仓库根，无法随技能分发，已提供 `examples/ci-gate.yml` 替代（见 0.1.0 的说明）。

### 修复

- 闸门拦下自身文档里"带 scheme 前缀的内嵌凭据"示例字面量（第三次自指），改为不带 scheme 的写法。

## [0.1.0] - 2026-11-02

### 新增

- `scripts/gate.py`：敏感内容扫描器（stdlib）。`--staged` 查暂存区、`--all` 查已跟踪文件、`--json` 机器可读；退出码 `0` 通过 / `1` 有违规 / `2` 用法错误。
- `rules.json`：路径黑名单（`.env`、`*secret*` 数据文件、私钥扩展名、`id_*`、私有文档、`.workbuddy/`、依赖目录）+ 内容正则（`sk-`、`ghp_`、`github_pat_`、`AKIA`、私钥块、`user:pass@host` 内嵌凭据、硬编码密钥字面量）+ 白名单 + 5 MB 上限。
- `scripts/install-hook.sh`：装 `pre-commit` 钩子，已存在非本技能钩子时先备份。
- `tests/test_gate.py`：7 例回归（真阳性 3、真阴性 2、白名单 1、JSON 输出 1）。假密钥在测试里运行时拼接，避免测试文件自己被闸门拦下。
- 文档体系：README / QUICKSTART / FAQ / SECURITY / CONTRIBUTING / INSTALLATION / USE-CASES / SUPPORT / CODE_OF_CONDUCT。

### 设计取舍

- **fail-closed**：钩子找不到扫描器时拒绝提交，而不是静默放行。
- **规则只有一份**：定时提交脚本（`git-autocommit.ps1`）调用同一个 `gate.py`，不在两处维护正则。
- **不扫历史、不做熵检测**：只检查当前文件内容；需要全历史扫描换 `gitleaks`，本技能做"轻量前置"。

### 说明

- skill-optimizer 的「GitHub Actions CI/CD 配置」一项**保持未满足**：workflow 必须位于仓库根的 `.github/workflows/`，无法随技能目录分发（放在技能目录里 GitHub 不会执行）。改为提供 `examples/ci-gate.yml` 作为接入片段，复制到仓库根即可生效。
- `requirements.txt` 为空文件是有意的：`gate.py` 零依赖，保留它只为让文档里的 `pip install -r` 不报错。
