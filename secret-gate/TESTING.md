# 测试

## 位置与运行

```bash
python tests/test_gate.py     # unittest，7 个用例，约 3 秒
```

## 用例构成

| 用例 | 类型 | 验证什么 |
|---|---|---|
| `test_clean_repo_passes` | 真阴性 | 干净内容必须放行 |
| `test_env_file_blocked` | 真阳性 | `.env` 文件名 + 内容密钥双命中 |
| `test_private_key_blocked` | 真阳性 | `id_rsa` 文件名 + 私钥块内容 |
| `test_credentialed_url_blocked` | 真阳性 | `user:pass@host` 形式的内嵌凭据（带 scheme 前缀） |
| `test_example_env_allowed` | 真阴性 | `.env.example` 白名单 |
| `test_json_output_shape` | 输出契约 | JSON 里 `checked` 与 `findings` 形状 |
| `test_all_mode_ignores_untracked` | 范围 | `--all` 不扫未跟踪文件 |

## 加规则时的规矩

1. **真阳性 + 真阴性各一**。只测会拦的，等于没测（改坏规则会把所有文件都拦下，而你不知道）。
2. **假密钥运行时拼接**（`FAKE_OPENAI = "sk-" + "a1b2c3d4e5" * 3`）。写死字面量会让测试文件自己被闸门拦下——技能必须能通过自己的检查。
3. 改完跑 `python tests/test_gate.py`，再实测一次真拦截（见 [CONTRIBUTING.md](CONTRIBUTING.md)）。

## 已知的测试盲区

- 未覆盖：超大文件（`max_file_bytes`）路径、`--rules` 自定义规则文件、Windows 与 WSL 路径分隔符混用。补用例时从这三处入手。
- 不测"钩子是否被 git 调用"——那是 git 的行为，靠手动验证（见 [DEBUGGING.md](DEBUGGING.md)）。
