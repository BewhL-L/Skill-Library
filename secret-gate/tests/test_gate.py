#!/usr/bin/env python3
"""secret_gate 的自测：真阳性、真阴性、白名单三条线。

运行：
    python tests/selftest.py
不需要 pytest，只用 unittest（stdlib）。
"""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
# 假密钥运行时拼接：写死在源码里会让本文件自己被闸门拦下（自指）
FAKE_OPENAI = "sk-" + "a1b2c3d4e5" * 3
FAKE_DSN = "postgresql://user:" + "pa55word" + "@localhost:5432/db"
PK_OPENSSH = "-----BEGIN " + "OPENSSH PRIVATE KEY-----"
PK_RSA = "-----BEGIN " + "RSA PRIVATE KEY-----"
GATE = HERE.parent / "scripts" / "gate.py"
RULES = HERE.parent / "rules.json"


def run_gate(repo: Path, *args: str) -> tuple[int, str]:
    proc = subprocess.run([sys.executable, str(GATE), str(repo), *args],
                          capture_output=True, text=True, encoding="utf-8", errors="replace")
    return proc.returncode, (proc.stdout + proc.stderr)


class GateTest(unittest.TestCase):
    def setUp(self) -> None:
        """准备一个空 git 仓库作为被检对象。"""
        self.repo = Path(tempfile.mkdtemp(prefix="gate-"))
        subprocess.run(["git", "-C", str(self.repo), "init", "-q"], check=True)
        subprocess.run(["git", "-C", str(self.repo), "config", "user.email", "t@t"], check=True)
        subprocess.run(["git", "-C", str(self.repo), "config", "user.name", "t"], check=True)

    def tearDown(self) -> None:
        """清理临时仓库。"""
        shutil.rmtree(self.repo, ignore_errors=True)

    def write(self, rel: str, text: str) -> None:
        """在临时仓库里写入一个文件。"""
        path = self.repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def stage_all(self) -> None:
        """把全部改动放进暂存区。"""
        subprocess.run(["git", "-C", str(self.repo), "add", "-A"], check=True)

    def test_clean_repo_passes(self) -> None:
        """干净内容必须放行。"""
        self.write("README.md", "# hello\n普通内容，没有密钥。\n")
        self.write("src/app.py", "def main():\n    return 1\n")
        self.stage_all()
        code, out = run_gate(self.repo, "--staged")
        self.assertEqual(code, 0, out)
        self.assertIn("通过", out)

    def test_env_file_blocked(self) -> None:
        """.env 文件名 + 内容密钥双命中。"""
        self.write(".env", "LLM_API_KEY=" + FAKE_OPENAI + "\n")
        self.stage_all()
        code, out = run_gate(self.repo, "--staged")
        self.assertEqual(code, 1, out)
        self.assertIn("env-file", out)
        self.assertIn("openai-key", out)

    def test_private_key_blocked(self) -> None:
        """SSH 私钥文件名与私钥块内容都会被拦。"""
        self.write("deploy/id_rsa", PK_OPENSSH + "\nabc\n")
        self.write("notes.md", "```\n" + PK_RSA + "\n```\n")
        self.stage_all()
        code, out = run_gate(self.repo, "--staged")
        self.assertEqual(code, 1, out)
        self.assertIn("ssh-key", out)
        self.assertIn("private-key-block", out)

    def test_credentialed_url_blocked(self) -> None:
        """URL 内嵌用户名密码会被拦。"""
        self.write("conf.py", 'DSN = "' + FAKE_DSN + '"\n')
        self.stage_all()
        code, out = run_gate(self.repo, "--staged")
        self.assertEqual(code, 1, out)
        self.assertIn("credentialed-url", out)

    def test_example_env_allowed(self) -> None:
        """.env.example 属白名单，应放行。"""
        self.write("backend/.env.example", "LLM_API_KEY=your-key-here\n")
        self.stage_all()
        code, out = run_gate(self.repo, "--staged")
        self.assertEqual(code, 0, out)

    def test_json_output_shape(self) -> None:
        """JSON 输出契约：checked 与 findings 字段。"""
        self.write("a.txt", FAKE_OPENAI + "\n")
        self.stage_all()
        proc = subprocess.run([sys.executable, str(GATE), str(self.repo), "--staged", "--json"],
                              capture_output=True, text=True, encoding="utf-8")
        data = json.loads(proc.stdout)
        self.assertEqual(data["checked"], 1)
        self.assertTrue(any(f["rule"] == "openai-key" for f in data["findings"]))

    def test_all_mode_ignores_untracked(self) -> None:
        """--all 只看已跟踪文件，不扫未跟踪。"""
        self.write("tracked.md", "# ok\n")
        self.stage_all()
        subprocess.run(["git", "-C", str(self.repo), "commit", "-qm", "init"], check=True)
        self.write("untracked.env", "x=1\n")
        code, out = run_gate(self.repo, "--all")
        self.assertEqual(code, 0, out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
