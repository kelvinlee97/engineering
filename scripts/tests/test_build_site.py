from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts import build_site


class StageTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        root = Path(self._tmp.name)
        self.wiki = root / "wiki"
        self.out = root / "content"
        files = {
            "index.md": '---\nokf_version: "0.2"\n---\n# Engineering Wiki\n\n'
            "* [Domains](engineering/) - Pages.\n* [Log](log.md) - History.\n",
            "log.md": "# Log\n\n## 2026-09-24\n* x\n",
            "engineering/index.md": "# Domains\n\n* [Claude Code](cc/) - Claude.\n",
            "engineering/cc/index.md": "# Concept\n\n* [Page](page.md) - A page.\n",
            "engineering/cc/page.md": "---\ntype: Concept\ntitle: Page\n"
            "generated: { by: x, at: 2026-09-24T15:00:00Z }\n---\nBody\n",
        }
        for rel, text in files.items():
            path = self.wiki / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        self.count = build_site.stage(self.wiki, self.out, "Engineering Wiki")

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def staged(self, rel: str) -> tuple[dict[str, object], str]:
        return build_site.split((self.out / rel).read_text(encoding="utf-8"))

    def test_every_file_is_staged(self) -> None:
        self.assertEqual(self.count, 5)

    def test_root_index_gets_site_title_and_loses_h1(self) -> None:
        data, body = self.staged("index.md")
        self.assertEqual(data["title"], "Engineering Wiki")
        self.assertEqual(data["okf_version"], "0.2")
        self.assertFalse(body.lstrip().startswith("# Engineering Wiki"))

    def test_reserved_files_take_title_from_parent_link(self) -> None:
        self.assertEqual(self.staged("engineering/index.md")[0]["title"], "Domains")
        self.assertEqual(self.staged("engineering/cc/index.md")[0]["title"], "Claude Code")
        self.assertEqual(self.staged("log.md")[0]["title"], "Log")

    def test_section_heading_is_kept_on_sub_index(self) -> None:
        # Only a title-like H1 is dropped; a sub index starts with a section heading
        # that Quartz should still render.
        _, body = self.staged("engineering/cc/index.md")
        self.assertTrue(body.startswith("# Concept"))
        _, body = self.staged("engineering/index.md")
        self.assertFalse(body.lstrip().startswith("# Domains"))

    def test_concept_gets_modified_from_generated(self) -> None:
        data, _ = self.staged("engineering/cc/page.md")
        self.assertEqual(data["modified"], "2026-09-24T15:00:00Z")

    def test_source_files_are_untouched(self) -> None:
        text = (self.wiki / "engineering/cc/page.md").read_text(encoding="utf-8")
        self.assertNotIn("modified", text)


class CheckTest(unittest.TestCase):
    def test_reports_missing_page_and_broken_link(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "wiki").mkdir()
            (root / "wiki/a.md").write_text("x", encoding="utf-8")
            (root / "wiki/b.md").write_text("x", encoding="utf-8")
            (root / "public").mkdir()
            (root / "public/d.html").write_text("d")
            (root / "public/a.html").write_text('<a href="./d">d</a><a href="./c">c</a>')
            problems = build_site.check(root / "wiki", root / "public")
        self.assertIn("b: no page in the build output", problems)
        self.assertIn("a.html: broken link ./c", problems)
        self.assertNotIn("a.html: broken link ./d", problems)


if __name__ == "__main__":
    unittest.main()
