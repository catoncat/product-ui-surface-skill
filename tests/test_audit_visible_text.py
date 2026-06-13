import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "product-ui-surface" / "scripts" / "audit_visible_text.py"


class AuditVisibleTextTest(unittest.TestCase):
    def run_script(self, args, stdin=""):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            input=stdin,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_default_patterns_fail_on_brief_leakage(self):
        result = self.run_script([], "这个界面旨在帮助用户高效管理 agentic workflow\n")
        self.assertEqual(result.returncode, 1)
        self.assertIn("帮助用户", result.stdout)
        self.assertIn("agentic workflow", result.stdout)

    def test_clean_visible_text_passes(self):
        result = self.run_script([], "Skills\n已启用\n停用\n重新扫描\n")
        self.assertEqual(result.returncode, 0)
        self.assertIn("No brief-leak terms found.", result.stdout)

    def test_contract_file_adds_forbidden_brief_terms(self):
        with tempfile.TemporaryDirectory() as tmp:
            contract = Path(tmp) / "surface-language-contract.md"
            contract.write_text(
                "# Surface Language Contract\n\n"
                "forbidden_brief_terms:\n"
                "- 智能编排体验\n"
                "- context leakage\n\n"
                "copy_rules:\n"
                "- Titles name objects.\n",
                encoding="utf-8",
            )
            result = self.run_script(["--contract", str(contract)], "智能编排体验\n")
        self.assertEqual(result.returncode, 1)
        self.assertIn("智能编排体验", result.stdout)

    def test_allow_term_suppresses_matching_findings(self):
        result = self.run_script(["--allow", "用于"], "用于\n系统会\n")
        self.assertEqual(result.returncode, 1)
        self.assertNotIn("term='用于'", result.stdout)
        self.assertIn("term='系统会'", result.stdout)

    def test_allow_file_suppresses_matching_findings(self):
        with tempfile.TemporaryDirectory() as tmp:
            allow_file = Path(tmp) / "allow.txt"
            allow_file.write_text("用于\n", encoding="utf-8")
            result = self.run_script(["--allow-file", str(allow_file)], "用于\n")
        self.assertEqual(result.returncode, 0)

    def test_no_defaults_only_uses_project_terms(self):
        result = self.run_script(["--no-defaults", "--term", "内部词"], "帮助用户\n内部词\n")
        self.assertEqual(result.returncode, 1)
        self.assertNotIn("term='帮助用户'", result.stdout)
        self.assertIn("term='内部词'", result.stdout)

    def test_exclude_skips_matching_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "visible.txt").write_text("Skills\n", encoding="utf-8")
            (root / "README.md").write_text("这个界面旨在帮助用户\n", encoding="utf-8")
            result = self.run_script(["--exclude", "README.md", str(root)])
        self.assertEqual(result.returncode, 0)

    def test_json_output_reports_findings(self):
        result = self.run_script(["--json"], "系统会\n")
        self.assertEqual(result.returncode, 1)
        payload = json.loads(result.stdout)
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["findings"][0]["term"], "系统会")


if __name__ == "__main__":
    unittest.main()
