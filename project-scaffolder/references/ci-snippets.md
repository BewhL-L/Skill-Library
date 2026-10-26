# CI 片段库（复制 job / step，不要复制整份 workflow）

> 使用原则：**给片段，不给整文件**。用户项目里往往已有 `.github/workflows/`，
> 整文件覆盖会冲掉他们既有的部署/发布流程。正确做法是先看现有文件，再把 step 追加进去。

## 目录

1. 先看现场：合并而不是覆盖
2. 片段 A：Python 后端（lint + test + 文档断言）
3. 片段 B：Node 前端（安装 + 测试 + 构建）
4. 片段 C：镜像构建（不推送）
5. 片段 D：私有文件守卫（可选，放最前面最省时间）
6. 六个常见坑
7. 验收：让 CI 真的红一次

---

## 1. 先看现场：合并而不是覆盖

```bash
ls .github/workflows/          # 已有就合并，没有才新建
```

- 已有 `ci.yml`：把下面的 **step** 追加到对应 job 的 `steps:` 末尾；
- 没有任何 workflow：新建 `ci.yml`，把片段包成 `jobs.<name>`。

> 判断标准：**用户原有的 job 名字、触发条件、部署步骤一律不动**，只加校验步骤。

## 2. 片段 A：Python 后端

```yaml
  backend:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: backend        # 后端不在根目录时必填
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"          # 与 Dockerfile 保持一致
          cache: pip
          cache-dependency-path: backend/requirements.txt
      - name: Install
        run: |
          python -m pip install -U pip
          pip install -r requirements.txt
          pip install ruff==0.17.2        # 锁版本，避免规则漂移
      - name: Lint
        run: ruff check app tests scripts
      - name: Test
        env:
          LLM_API_KEY: test-key           # 测试用假客户端，给个占位即可
        run: python -m pytest -q          # 必须 -m，见坑 1
      - name: Docs consistency
        run: python scripts/check_docs.py --root . --tests backend/tests
```

## 3. 片段 B：Node 前端

```yaml
  frontend:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: frontend
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: npm
          cache-dependency-path: frontend/package-lock.json
      - name: Install
        run: npm ci                       # 必须提交 lock 文件；有 peer 冲突再加 --legacy-peer-deps
      - name: Test
        run: npm run test
      - name: Build
        run: npm run build                # 含类型检查（vue-tsc / tsc）
```

## 4. 片段 C：镜像构建（不推送）

```yaml
  docker:
    runs-on: ubuntu-latest
    needs: [backend, frontend]            # 前两道绿了再构建，省时间
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - name: Build backend image
        uses: docker/build-push-action@v6
        with:
          context: ./backend
          push: false
          cache-from: type=gha,scope=backend
          cache-to: type=gha,mode=max,scope=backend
      - name: Build frontend image
        uses: docker/build-push-action@v6
        with:
          context: ./frontend
          push: false
          cache-from: type=gha,scope=frontend
          cache-to: type=gha,mode=max,scope=frontend
```

## 5. 片段 D：私有文件守卫（可选）

```yaml
      - name: No private files tracked
        run: |
          if git ls-files | grep -Ei '指导书|内部复盘|(^|/)\.env$'; then
            echo "::error::私有文档或密钥被提交，请 git rm --cached 并加入 .gitignore"
            exit 1
          fi
```

放在最早的 job 里——越早失败，越省 runner 时间。

## 6. 六个常见坑

| 坑 | 现象 | 正确做法 |
|---|---|---|
| 1. 用 console script 跑 pytest | `ModuleNotFoundError: No module named 'app'`，收集阶段就崩（退出码 4） | `python -m pytest`（CWD 进 `sys.path`）；或在 pyproject 配 `pythonpath = ["."]` |
| 2. 没锁 lint 版本 | 昨天绿今天红，规则变了 | `ruff==0.17.2` 固定版本 |
| 3. `npm ci` 没有 lock | `npm ci can only install with an existing package-lock.json` | 提交 `package-lock.json`，别用 `npm install` 代替 |
| 4. 缓存 key 写错 | 每次都全量下载依赖 | `setup-python/node` 的 `cache-dependency-path` 必须指向真实锁文件 |
| 5. 在 PR 里读 secrets | fork 的 PR 拿到空值，步骤失败 | 测试只用占位值，需要真实密钥的 job 限制在 `push` 上 |
| 6. 只跑测试不跑迁移 | 本地能起，CI 绿，线上建不出表 | 加一步 `alembic upgrade head`（空库）或迁移单测 |

## 7. 验收：让 CI 真的红一次

接入后必须做一次反向验证，否则等于没接：

1. 故意写一个语法错误 → CI 必须红；
2. 故意把 README 的测试数改错 → `Docs consistency` 必须红；
3. `git add` 一个 `.env`（本地测试后删掉）→ 私有文件守卫必须红。

三次都红了，才能说明门禁真的在工作。
