from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.knowledge_base import KnowledgeBaseError, discover_documents, stage


class KnowledgeBaseTests(unittest.TestCase):
    def test_discovers_pairs_and_derives_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._write(root, "AWS/README.md", "# AWS\n")
            self._write(root, "AWS/README_ZH.md", "# AWS 中文\n")

            documents = discover_documents(
                root,
                ["AWS/README.md", "AWS/README_ZH.md"],
            )

            english = next(document for document in documents if document.language == "en")
            self.assertEqual(english.page, "AWS/index.md")
            self.assertEqual(english.pair_page, "AWS/index_zh.md")
            self.assertEqual(english.area, "AWS")
            self.assertEqual(english.kind, "catalog")
            self.assertEqual(english.pair_title, "AWS 中文")

    def test_missing_pair_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._write(root, "AWS/README.md", "# AWS\n")

            with self.assertRaisesRegex(KnowledgeBaseError, "missing paired document"):
                discover_documents(root, ["AWS/README.md"])

    def test_missing_local_link_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._write(root, "AWS/README.md", "# AWS\n\n[Missing](missing/README.md)\n")
            self._write(root, "AWS/README_ZH.md", "# AWS 中文\n")

            with self.assertRaisesRegex(KnowledgeBaseError, "missing local link target"):
                discover_documents(root, ["AWS/README.md", "AWS/README_ZH.md"])

    def test_stage_rewrites_links_and_excludes_internal_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            paths = [
                "README.md",
                "README_ZH.md",
                "AWS/README.md",
                "AWS/README_ZH.md",
                "apple/container/README.md",
                "apple/container/README_ZH.md",
                "AGENTS.md",
                ".agents/skills/youtube-transcript/SKILL.md",
            ]
            self._write(
                root,
                "README.md",
                "# Engineering\n\n[AWS](AWS/) · [Rules](AGENTS.md) · "
                "[Skill](.agents/skills/youtube-transcript/)\n",
            )
            self._write(root, "README_ZH.md", "# 工程\n")
            self._write(root, "AWS/README.md", "# AWS\n")
            self._write(root, "AWS/README_ZH.md", "# AWS 中文\n")
            self._write(root, "apple/container/README.md", "# Apple Container\n")
            self._write(root, "apple/container/README_ZH.md", "# Apple 容器\n")
            self._write(root, "AGENTS.md", "# Internal\n")
            self._write(root, ".agents/skills/youtube-transcript/SKILL.md", "# Skill\n")
            self._write(root, "pages/knowledge-base.css", "/* test stylesheet */\n")
            output = root / ".pages-build"

            stage(root, output, paths)

            repository = (output / "repository/index.md").read_text(encoding="utf-8")
            self.assertIn("../AWS/index.md", repository)
            self.assertIn(
                "https://github.com/kelvinlee97/engineering/blob/main/AGENTS.md",
                repository,
            )
            self.assertIn(
                "https://github.com/kelvinlee97/engineering/tree/main/.agents/skills/youtube-transcript",
                repository,
            )
            self.assertIn('class="kb-meta"', repository)
            self.assertIn("kb_language: en", repository)
            dashboard = (output / "index.md").read_text(encoding="utf-8")
            self.assertIn('href="apple/container/"', dashboard)
            self.assertIn('href="topics/"', dashboard)
            self.assertIn('href="archive/"', dashboard)
            self.assertIn('href="index_zh/"', dashboard)
            self.assertIn("document.querySelector('.md-search__input').focus()", dashboard)
            self.assertIn("  - footer", dashboard)
            self.assertIn('href="../"', (output / "index_zh.md").read_text(encoding="utf-8"))
            topics = (output / "topics/index.md").read_text(encoding="utf-8")
            self.assertIn('href="../apple/container/"', topics)
            self.assertIn('class="kb-topic-card__count">1 note</span>', topics)
            self.assertTrue((output / "topics/index_zh.md").exists())
            self.assertTrue((output / "archive/index.md").exists())
            self.assertTrue((output / "archive/index_zh.md").exists())
            self.assertEqual(
                (output / "stylesheets/knowledge-base.css").read_text(encoding="utf-8"),
                "/* test stylesheet */\n",
            )
            self.assertTrue((output / "index.md").exists())
            self.assertFalse((output / "AGENTS.md").exists())

    def test_youtube_pairs_keep_video_id(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            paths = [
                "YouTube/startup/lesson/summary.md",
                "YouTube/startup/lesson/summary_zh.md",
            ]
            source = "# Lesson\n\nSource: https://www.youtube.com/watch?v=5-G9WHwQMwQ\n"
            self._write(root, paths[0], source)
            self._write(root, paths[1], source.replace("# Lesson", "# 课程"))

            documents = discover_documents(root, paths)

            self.assertEqual({document.video_id for document in documents}, {"5-G9WHwQMwQ"})
            self.assertEqual({document.kind for document in documents}, {"video-summary"})

    @staticmethod
    def _write(root: Path, relative: str, text: str) -> None:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
