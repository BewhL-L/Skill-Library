# API 参考

> 5 个脚本均可作为 CLI 运行（`python scripts/xxx.py --help`），也可作为模块导入。
> 以下列出主要公共函数与返回结构；完整签名以源码为准。

## scan_project_facts.py — 项目事实扫描

### `scan(root, component_dirs, group_depth=1) -> dict`

扫描整个项目，返回结构化事实。关键字段：

- `code.python`：`{files, lines}`（Python 文件数 / 物理行数）。
- `code.frontend`：`{files, lines}`（前端文件数 / 行数）。
- `python_by_topdir`：按顶层（或 `--group-depth` 层）目录分组的规模。
- `tests`：`{files, functions, per_file}`（测试文件、用例数、每文件分布）。
- `components`：各组件目录的业务文件数（已排除 `__init__.py`）与 `init_files`。
- `docker_services`：compose 服务名列表。
- `requirements`：后端依赖包名（去版本）。
- `frontend_deps`：前端 dependencies / devDependencies。
- `env_keys`：`.env*` 键名（不含值）。

### 其他函数

- `iter_code_files(root, suffixes, exclude) -> Iterable[Path]`：遍历代码文件（排除依赖/缓存）。
- `count_test_functions(files) -> dict`：统计 `def test_`、`test(`、`it(`。
- `list_component_dirs(root, dirs) -> dict`：统计组件目录，返回 `exists/file_count/init_files`。
- `parse_docker_services(root) -> list[str]`：轻量解析 compose 顶层服务。
- `parse_env_keys(dirpath) -> list[str]`：只取键名，不读值。
- `parse_requirements(root) -> list[str]`：解析 requirements 包名。
- `group_by_topdir(files, root, depth) -> dict`：按目录层级分组统计。

## validate_md.py — Markdown 结构校验

### `validate(path, require_frontmatter=False) -> dict`

返回 `{ok, issues, heading_counts, fence_count}`：

- `ok`：是否无错误（severity 为 error 的问题为 0）。
- `issues`：`[{severity, message, line}]`。
- `heading_counts`：`{H1..H6}` 计数。

### 其他函数

- `split_frontmatter(text) -> tuple[Optional[str], str]`。
- `collect_headings(body, start=None, end=None) -> list[tuple[level,title]]`（围栏状态机）。
- `check_fences(body) -> list[dict]`：围栏未闭合检测。
- `check_heading_hierarchy(headings) -> list[dict]`：H1 唯一、层级跳跃。
- `check_tables(body) -> list[dict]`：表格列数一致性。
- `check_wikilinks(body) -> list[dict]`：检测空目标双链（左方括号后直接跟竖线、缺少目标页）。

## verify_zero_cut.py — 原文零删减比对

### `compare(original, new, allow_note=None) -> dict`

返回：

- `ok`：原文实质行是否都被保留（允许 `--allow-note` 声明的修正时需人工确认）。
- `exact_kept`：精确保留行数。
- `loose_kept`：归一化空白/标点后保留的行数。
- `missing` / `missing_details`：疑似删减数量与逐行明细。
- `total_substantive`：原文参与比对的实质行数。

比对策略：跳过纯标题、围栏、空白；先精确匹配，再宽松匹配，仍未命中判为疑似删减。

## make_toc.py — 目录生成

- `github_slug(title) -> str`：GitHub 锚点（小写、去标点、空白转连字符）。
- `collect_headings(text, start=None, end=None, levels=(2,3,4)) -> list[tuple[level,title]]`：
  围栏状态机提取标题，支持按标题文本限定区间。
- `build_toc(headings, min_level, max_level) -> str`：按层级缩进的 Markdown 列表。
- CLI 支持：`--details`（折叠）、`--title`、`--insert-after`、`--write`（自动生成 `.bak`）。

## check_docs.py — 文档与代码一致性

### CLI

| 参数 | 说明 |
|---|---|
| `--root` | 项目根（默认 `.`） |
| `--doc` | 待校验文档（默认 `README.md`） |
| `--tests` | 测试目录（默认 `backend/tests`） |
| `--openapi` | `openapi.json` 路径（可选，用于校验接口清单） |
| `--routes` | 每行一个路由路径的文本文件（可选） |
| `--forbid` / `--private` | 追加禁止表述 / 私有文件，可多次 |
| `--skip-git` | 跳过 git 私有文件检查 |
| `--json` | JSON 输出 |

### 检查项

1. 测试数量：文档 `N passed` / `N 个测试` vs `tests/` 下测试函数数（skip 单独计数）；
2. 文档路径：反引号内 `backend/` `frontend/` `docker/` `.github/` `scripts/` 路径必须存在；
3. 废弃表述：默认黑名单 + `--forbid`；
4. 私有文件：`git ls-files` 中不得出现私有文档与 `.env`；
5. 接口清单（可选）：`/api/...` 必须能在 `--openapi` 或 `--routes` 中找到。

### `check_numbers(text, tests_dir) -> list[str]`

返回问题列表；空列表表示一致。供测试或其它脚本直接复用。

## 退出码约定

- `validate_md.py` / `verify_zero_cut.py`：存在问题时退出码为 1，便于在 CI 中拦截。
- `scan_project_facts.py` / `make_toc.py`：成功为 0；参数 / 路径错误为非 0。
