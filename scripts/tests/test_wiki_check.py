from __future__ import annotations

import tempfile
import textwrap
import unittest
from pathlib import Path

from scripts import wiki_check

PAGE = """\
---
type: Concept
title: Subagent
description: A child agent with its own context.
sources:
  - id: src
    resource: https://example.com/src
---
A subagent runs in isolation.[^src] See [other](other.md).

[^src]: Source
"""


class WikiCheckTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.wiki = Path(self._tmp.name) / "wiki"
        self.write("index.md", '---\nokf_version: "0.2"\n---\n# Concept\n\n'
                   "* [Subagent](eng/subagent.md) - A child agent with its own context.\n")
        self.write("eng/index.md", "# Concept\n\n"
                   "* [Subagent](subagent.md) - A child agent with its own context.\n")
        self.write("eng/subagent.md", PAGE)
        self.write("log.md", "# Log\n\n## 2026-09-24\n* **Ingest**: x\n\n## 2026-09-01\n* y\n")

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def write(self, rel: str, text: str) -> None:
        path = self.wiki / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(textwrap.dedent(text), encoding="utf-8")

    def run_check(self) -> wiki_check.Report:
        return wiki_check.run(self.wiki, None, None)

    def test_valid_bundle_passes_with_broken_link_warning(self) -> None:
        report = self.run_check()
        self.assertEqual(report.errors, [])
        self.assertEqual(len(report.warnings), 1)
        self.assertIn("broken link other.md", report.warnings[0])

    def test_missing_type_fails(self) -> None:
        self.write("eng/subagent.md", PAGE.replace("type: Concept\n", ""))
        self.assertTrue(any("`type`" in e for e in self.run_check().errors))

    def test_missing_frontmatter_fails(self) -> None:
        self.write("eng/bare.md", "# No frontmatter\n")
        self.assertTrue(any("bare.md: missing frontmatter" in e for e in self.run_check().errors))

    def test_description_mismatch_fails(self) -> None:
        self.write("eng/index.md", "* [Subagent](subagent.md) - Something else.\n")
        self.assertTrue(any("differs" in e for e in self.run_check().errors))

    def test_unlisted_page_fails(self) -> None:
        self.write("eng/extra.md", "---\ntype: Concept\ndescription: Extra.\n---\nBody\n")
        errors = self.run_check().errors
        self.assertTrue(any("extra.md is not listed in the root index" in e for e in errors))
        self.assertTrue(any("extra.md: not listed in eng/index.md" in e for e in errors))

    def test_unknown_footnote_fails(self) -> None:
        self.write("eng/subagent.md", PAGE.replace("[^src]", "[^other]"))
        self.assertTrue(any("[^other]" in e for e in self.run_check().errors))

    def test_log_order_fails(self) -> None:
        self.write("log.md", "## 2026-09-01\n\n## 2026-09-24\n")
        self.assertTrue(any("newest first" in e for e in self.run_check().errors))

    def test_forbidden_name_fails(self) -> None:
        self.write("eng/README.md", PAGE)
        self.assertTrue(any("README.md is not allowed" in e for e in self.run_check().errors))

    def test_frontmatter_on_sub_index_fails(self) -> None:
        self.write("eng/index.md", "---\ntitle: x\n---\n"
                   "* [Subagent](subagent.md) - A child agent with its own context.\n")
        self.assertTrue(any("may not carry frontmatter" in e for e in self.run_check().errors))


if __name__ == "__main__":
    unittest.main()
