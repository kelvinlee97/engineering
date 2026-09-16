"""Run with: python3 -m unittest discover -s Python -p 'test_*.py'."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent


class LogExampleTests(unittest.TestCase):
    def test_scripts_use_bundled_log_from_any_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            for cwd in (ROOT.parent, ROOT, Path(directory)):
                for script in (ROOT / "examples/aggregate_5xx_status.py", ROOT / "test.py"):
                    with self.subTest(cwd=cwd, script=script):
                        result = subprocess.run(
                            [sys.executable, str(script)],
                            cwd=cwd,
                            capture_output=True,
                            text=True,
                            check=True,
                        )
                        self.assertEqual(result.stdout.strip(), "3")

    def test_bilingual_generators_filter_status_not_response_size(self):
        lines = (ROOT / "examples/app.log").read_text(encoding="utf-8").splitlines()
        boundary_lines = [
            f'127.0.0.1 - - [time] "GET / HTTP/1.1" {status} 512 "-" "-"'
            for status in (200, 499, 500, 599, 600)
        ]
        for name in ("README.md", "README_ZH.md"):
            with self.subTest(language=name):
                text = (ROOT / "advanced/02-iterators-and-generators" / name).read_text(
                    encoding="utf-8"
                )
                function = text.split("def server_errors", 1)[1].split(
                    "\n\n\nfor line", 1
                )[0]
                namespace = {}
                exec("def server_errors" + function, namespace)
                filter_errors = namespace["server_errors"]
                self.assertEqual(len(list(filter_errors(lines))), 3)
                self.assertEqual(
                    list(filter_errors(boundary_lines)), boundary_lines[2:4]
                )
