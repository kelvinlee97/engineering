from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts import wiki_index


def page(type_: str, title: str, desc: str) -> str:
    return f"---\ntype: {type_}\ntitle: {title}\ndescription: {desc}\n---\nBody\n"


class WikiIndexTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.wiki = Path(self._tmp.name) / "wiki"
        files = {
            "index.md": '---\nokf_version: "0.2"\n---\n# Wiki\n\nIntro.\n\n# Concept\n\n* stale\n',
            "engineering/index.md": "# Domains\n\n* [Ops](ops/) - Ops.\n",
            "engineering/ops/b.md": page("Playbook", "Beta", "Second."),
            "engineering/ops/a.md": page("Concept", "Alpha", "First."),
            "sources/s.md": page("Source Summary", "Src", "A source."),
        }
        for rel, text in files.items():
            path = self.wiki / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_root_keeps_head_and_lists_every_page_by_type(self) -> None:
        out, problems = wiki_index.render(self.wiki)
        root = out[self.wiki / "index.md"]
        self.assertEqual(problems, [])
        head = '---\nokf_version: "0.2"\n---\n# Wiki\n\nIntro.\n\n# Concept'
        self.assertTrue(root.startswith(head))
        self.assertNotIn("stale", root)
        self.assertLess(root.index("# Concept"), root.index("# Playbook"))
        self.assertLess(root.index("# Playbook"), root.index("# Source Summary"))
        self.assertIn("* [Alpha](engineering/ops/a.md) - First.", root)

    def test_directory_index_uses_local_paths(self) -> None:
        out, _ = wiki_index.render(self.wiki)
        self.assertIn("* [Beta](b.md) - Second.", out[self.wiki / "engineering/ops/index.md"])

    def test_hand_written_domain_index_is_left_alone(self) -> None:
        out, _ = wiki_index.render(self.wiki)
        self.assertNotIn(self.wiki / "engineering/index.md", out)

    def test_missing_domain_entry_is_reported(self) -> None:
        extra = self.wiki / "engineering/new/c.md"
        extra.parent.mkdir()
        extra.write_text(page("Concept", "C", "C."), encoding="utf-8")
        _, problems = wiki_index.render(self.wiki)
        self.assertEqual(problems, ["engineering/index.md: add an entry for new/"])

    def test_domain_entry_may_link_to_its_index_file(self) -> None:
        (self.wiki / "engineering/index.md").write_text(
            "# Domains\n\n* [Ops](ops/index.md) - Ops.\n", encoding="utf-8"
        )
        _, problems = wiki_index.render(self.wiki)
        self.assertEqual(problems, [])

    def test_check_mode_reports_stale_without_writing(self) -> None:
        root = self.wiki / "index.md"
        before = root.read_text(encoding="utf-8")
        self.assertEqual(wiki_index.main(["--wiki", str(self.wiki), "--check"]), 1)
        self.assertEqual(root.read_text(encoding="utf-8"), before)
        self.assertEqual(wiki_index.main(["--wiki", str(self.wiki)]), 0)
        self.assertEqual(wiki_index.main(["--wiki", str(self.wiki), "--check"]), 0)


if __name__ == "__main__":
    unittest.main()
