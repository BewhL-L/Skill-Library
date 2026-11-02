# 贡献

## 开发环境

无第三方依赖。Python 3.8+、git 即可：

```bash
python tests/test_gate.py     # 7 个回归用例，改任何东西之前先跑通
```

## 改规则（`rules.json`）的规矩

1. **每条新规则都要配一个测试**：在 `tests/test_gate.py` 里加真阳性（会被拦）和真阴性（不该被拦）各一。
2. **不要把假密钥写进源码**，运行时拼接（`"sk-" + "a" * 30`）。写死的字面量会让测试文件自己被闸门拦下。
3. **改完跑 `python tests/test_gate.py`**，并实测一次真拦截：

   ```bash
   echo 'sk-'$(printf 'a%.0s' {1..30}) > leak.txt
   git add leak.txt && git commit -m "should fail"   # 必须被拒
   rm leak.txt && git reset
   ```

4. **宁可误报，不可漏报**。误报改一次白名单，漏报要重写 git 历史。

## 提交

沿用 Conventional Commits：`feat:` / `fix:` / `docs:` / `test:` / `chore:`。提交信息说清"为什么改"和"怎么验证的"。

## 代码风格

- 只用标准库（`gate.py` 保持零依赖，是它能被任何仓库直接调用的前提）。
- 新增逻辑要有类型注解与异常处理，退出码语义保持 `0/1/2` 不变。
