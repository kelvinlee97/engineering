from __future__ import annotations

import re
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
tags: [agents]
sources:
  - id: src
    resource: https://example.com/src
generated: { by: claude-code/wiki-v1, at: 2026-09-24T15:00:00Z }
status: draft
---
A subagent runs in isolation.[^src] See [other](other.md).

## Related

- Source: [Source](../sources/src.md)

[^src]: Source
"""

SUMMARY = """\
---
type: Source Summary
title: Source
description: The source.
tags: [agents]
sources:
  - id: src
    resource: https://example.com/src
generated: { by: claude-code/wiki-v1, at: 2026-09-24T15:00:00Z }
status: draft
---
A source.[^src]

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
        self.write("sources/src.md", SUMMARY)
        self.write("sources/index.md", "* [Source](src.md) - The source.\n")
        with (self.wiki / "index.md").open("a", encoding="utf-8") as fh:
            fh.write("* [Source](sources/src.md) - The source.\n")
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
        self.write("eng/extra.md", PAGE.replace("A child agent with its own context.", "Extra."))
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

    def test_directory_link_in_index_fails(self) -> None:
        with (self.wiki / "index.md").open("a", encoding="utf-8") as fh:
            fh.write("* [Domains](eng/) - Concept pages.\n")
        self.assertTrue(any("links a directory" in e for e in self.run_check().errors))

    def test_type_outside_vocabulary_fails(self) -> None:
        self.write("eng/subagent.md", PAGE.replace("type: Concept", "type: Thing"))
        self.assertTrue(any("not in the vocabulary" in e for e in self.run_check().errors))

    def test_missing_style_fields_fail(self) -> None:
        page = PAGE.replace("tags: [agents]\n", "").replace("status: draft\n", "status: done\n")
        self.write("eng/subagent.md", page)
        errors = self.run_check().errors
        self.assertTrue(any("`tags`" in e for e in errors))
        self.assertTrue(any("`status`" in e for e in errors))

    def test_generated_at_must_be_utc(self) -> None:
        self.write("eng/subagent.md", PAGE.replace("15:00:00Z", "15:00:00+08:00"))
        self.assertTrue(any("generated.at" in e for e in self.run_check().errors))

    def test_uncited_source_fails(self) -> None:
        self.write("eng/subagent.md", PAGE.replace(".[^src]", ".").replace("[^src]: Source\n", ""))
        self.assertTrue(any("never cited" in e for e in self.run_check().errors))

    def test_h1_in_body_fails(self) -> None:
        self.write("eng/subagent.md", PAGE.replace("A subagent runs", "# Title\n\nA subagent runs"))
        self.assertTrue(any("H1" in e for e in self.run_check().errors))

    def test_missing_related_and_summary_link_fail(self) -> None:
        related = "## Related\n\n- Source: [Source](../sources/src.md)\n"
        self.write("eng/subagent.md", PAGE.replace(related, ""))
        errors = self.run_check().errors
        self.assertTrue(any("## Related" in e for e in errors))
        self.assertTrue(any("sources/src.md" in e for e in errors))

    def test_mermaid_without_accessibility_metadata_fails(self) -> None:
        diagram = "```mermaid\nflowchart LR\n    accTitle: T\n    A --> B\n```\n\n"
        self.write("eng/subagent.md", PAGE.replace("## Related", diagram + "## Related"))
        errors = self.run_check().errors
        self.assertTrue(any("missing `accDescr`" in e for e in errors))
        self.assertFalse(any("missing `accTitle`" in e for e in errors))

    def test_claude_md_lists_the_same_type_vocabulary(self) -> None:
        claude_md = (Path(__file__).resolve().parents[2] / "CLAUDE.md").read_text(encoding="utf-8")
        line = next(ln for ln in claude_md.splitlines() if "`type` vocabulary" in ln)
        block = claude_md[claude_md.index(line):].split("\n\n", 1)[0].split("Add a new", 1)[0]
        self.assertEqual(set(re.findall(r"`([A-Z][A-Za-z ]+)`", block)), wiki_check.TYPES)


if __name__ == "__main__":
    unittest.main()
