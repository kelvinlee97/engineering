from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.knowledge_base import (
    AWS_GROUPS,
    HOME_TOPIC_EXCLUDE,
    LATEST_PER_AREA,
    SYMPTOM_ENTRIES,
    TOPIC_META,
    KnowledgeBaseError,
    _excerpt,
    _home_areas,
    _latest_documents,
    _summary_markdown,
    _reading_label,
    _reading_minutes,
    discover_documents,
    stage,
)


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

    def test_mermaid_requires_accessible_title_and_description(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            diagram = "# AWS\n\n```mermaid\nflowchart TD\nA --> B\n```\n"
            self._write(root, "AWS/README.md", diagram)
            self._write(root, "AWS/README_ZH.md", diagram.replace("# AWS", "# AWS 中文"))

            with self.assertRaisesRegex(KnowledgeBaseError, "missing accTitle"):
                discover_documents(root, ["AWS/README.md", "AWS/README_ZH.md"])

    def test_mermaid_types_and_order_must_match_pair(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            flowchart = (
                "# AWS\n\n```mermaid\nflowchart TD\n"
                "accTitle: Overview\naccDescr: A flows to B.\nA --> B\n```\n"
            )
            sequence = (
                "# AWS 中文\n\n```mermaid\nsequenceDiagram\n"
                "accTitle: 总览\naccDescr: A 向 B 发送请求。\nA->>B: request\n```\n"
            )
            self._write(root, "AWS/README.md", flowchart)
            self._write(root, "AWS/README_ZH.md", sequence)

            with self.assertRaisesRegex(KnowledgeBaseError, "different Mermaid diagram types"):
                discover_documents(root, ["AWS/README.md", "AWS/README_ZH.md"])

    def test_accessible_paired_mermaid_diagrams_pass(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            english = (
                "# AWS\n\n```mermaid\nflowchart TD\n"
                "accTitle: Overview\naccDescr: A flows to B.\nA --> B\n```\n"
            )
            chinese = english.replace("# AWS", "# AWS 中文").replace(
                "Overview\naccDescr: A flows to B.",
                "总览\naccDescr: A 流向 B。",
            )
            self._write(root, "AWS/README.md", english)
            self._write(root, "AWS/README_ZH.md", chinese)

            documents = discover_documents(
                root,
                ["AWS/README.md", "AWS/README_ZH.md"],
            )

            self.assertEqual(len(documents), 2)

    def test_stage_rewrites_links_and_excludes_internal_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            paths = [
                "README.md",
                "README_ZH.md",
                "AWS/README.md",
                "AWS/README_ZH.md",
                "Git/README.md",
                "Git/README_ZH.md",
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
            self._write(root, "Git/README.md", "# Git\n")
            self._write(root, "Git/README_ZH.md", "# Git 中文\n")
            self._write(root, "apple/container/README.md", "# Apple Container\n")
            self._write(root, "apple/container/README_ZH.md", "# Apple 容器\n")
            self._write(root, "AGENTS.md", "# Internal\n")
            self._write(root, ".agents/skills/youtube-transcript/SKILL.md", "# Skill\n")
            self._write(root, "pages/knowledge-base.css", "/* test stylesheet */\n")
            asset = root / "pages/assets/fonts/demo.woff2"
            asset.parent.mkdir(parents=True, exist_ok=True)
            asset.write_bytes(b"woff2")
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
            self.assertIn(">Start from a symptom, or pick a topic.</h1>", dashboard)
            self.assertIn('class="kb-hero"', dashboard)
            self.assertIn('class="kb-stats"', dashboard)
            self.assertIn('class="kb-topic-card__blurb"', dashboard)
            self.assertIn('class="kb-symptom"', dashboard)
            self.assertIn('class="kb-coverage__fill"', dashboard)
            chinese_dashboard = (output / "index_zh.md").read_text(encoding="utf-8")
            self.assertIn(
                ">从一个故障现象开始，或者直接挑一个主题。</h1>", chinese_dashboard
            )
            self.assertIn('class="kb-stats"', chinese_dashboard)
            self.assertIn('class="kb-symptom"', chinese_dashboard)
            self.assertIn('href="apple/container/"', dashboard)
            self.assertIn('href="archive/"', dashboard)
            self.assertIn('href="index_zh/"', dashboard)
            self.assertIn("document.querySelector('.md-search__input').focus()", dashboard)
            # The topic tabs render in the header, so the home page keeps its
            # full width by hiding the left rail that would only say "Home".
            self.assertIn("  - navigation", dashboard)
            self.assertIn('href="../"', (output / "index_zh.md").read_text(encoding="utf-8"))
            topics = (output / "topics/index.md").read_text(encoding="utf-8")
            self.assertIn('href="../apple/container/"', topics)
            self.assertIn('class="kb-topic-card__count">1 note</span>', topics)
            self.assertIn('class="kb-topic-card__monogram"', topics)
            self.assertTrue((output / "topics/index_zh.md").exists())
            self.assertTrue((output / "archive/index.md").exists())
            self.assertTrue((output / "archive/index_zh.md").exists())
            self.assertEqual(
                (output / "stylesheets/knowledge-base.css").read_text(encoding="utf-8"),
                "/* test stylesheet */\n",
            )
            self.assertEqual(
                (output / "assets/fonts/demo.woff2").read_bytes(),
                b"woff2",
            )
            self.assertTrue((output / "index.md").exists())
            self.assertFalse((output / "AGENTS.md").exists())

    def test_aws_nav_groups_are_unique_and_cover_every_service(self) -> None:
        """Every AWS page belongs to exactly one service family."""

        slugs = [slug for _, group in AWS_GROUPS for slug in group]
        self.assertEqual(len(slugs), len(set(slugs)), "duplicate AWS nav slug")

        root = Path(__file__).resolve().parents[2]
        documents = discover_documents(root)
        pages = {
            document.page
            for document in documents
            if document.language == "en"
            and document.page.startswith("AWS/")
            and document.page != "AWS/index.md"
        }
        mapped = {f"AWS/{slug}/index.md" for slug in slugs}
        self.assertEqual(
            pages - mapped,
            set(),
            "new AWS pages need a home in AWS_GROUPS",
        )
        self.assertEqual(mapped - pages, set(), "AWS_GROUPS names a missing page")
        self.assertNotIn("- More", _summary_markdown(documents))

    def test_summary_nests_sections_and_omits_chinese_pages(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._write(root, "Git/README.md", "# Git\n")
            self._write(root, "Git/README_ZH.md", "# Git 中文\n")
            self._write(root, "AWS/README.md", "# AWS\n")
            self._write(root, "AWS/README_ZH.md", "# AWS 中文\n")
            self._write(root, "AWS/s3/README.md", "# Amazon S3 - Runbook & Reference\n")
            self._write(root, "AWS/s3/README_ZH.md", "# Amazon S3 中文\n")
            documents = discover_documents(
                root,
                [
                    "Git/README.md",
                    "Git/README_ZH.md",
                    "AWS/README.md",
                    "AWS/README_ZH.md",
                    "AWS/s3/README.md",
                    "AWS/s3/README_ZH.md",
                ],
            )

            summary = _summary_markdown(documents)

            self.assertIn("- AWS\n", summary)
            self.assertIn("    - Storage & migration\n", summary)
            # The shared article-title suffix is trimmed for the sidebar.
            self.assertIn("        - [Amazon S3](AWS/s3/index.md)\n", summary)
            # Chinese pages reach readers through each article's language link.
            self.assertNotIn("index_zh.md", summary.replace("[中文 / Chinese](index_zh.md)", ""))

    def test_home_topics_all_have_a_name_and_blurb(self) -> None:
        """A tile with no curated name falls back to an article title."""

        root = Path(__file__).resolve().parents[2]
        documents = discover_documents(root)
        for language in ("en", "zh"):
            for area in _home_areas(documents, language):
                self.assertIn(area, TOPIC_META, f"{area} needs a TOPIC_META entry")
        for area in HOME_TOPIC_EXCLUDE:
            self.assertNotIn(area, _home_areas(documents, "en"))

    def test_symptom_entries_resolve_in_both_languages(self) -> None:
        root = Path(__file__).resolve().parents[2]
        pages = {document.page for document in discover_documents(root)}
        for entry in SYMPTOM_ENTRIES:
            page = entry[0]
            self.assertIn(page, pages)
            self.assertIn(page.replace("index.md", "index_zh.md"), pages)

    def test_latest_notes_are_capped_per_topic(self) -> None:
        root = Path(__file__).resolve().parents[2]
        documents = discover_documents(root)
        latest = _latest_documents(documents, "en")

        self.assertTrue(latest)
        counts: dict[str, int] = {}
        for document in latest:
            counts[document.area] = counts.get(document.area, 0) + 1
        self.assertLessEqual(max(counts.values()), LATEST_PER_AREA)

    def test_excerpt_skips_a_bare_lead_in_line(self) -> None:
        """Many articles open with the same colon-terminated lead-in."""

        text = (
            "# Amazon Athena\n\n"
            "This article answers three practical questions:\n\n"
            "Athena reads data straight out of S3, so partitioning and file "
            "layout decide the bill more than the query text does.\n"
        )

        self.assertTrue(_excerpt(text, "en").startswith("Athena reads data"))

    def test_reading_time_ignores_markdown_syntax(self) -> None:
        prose = " ".join(["word"] * 440)
        self.assertEqual(_reading_minutes(prose), 2)
        fenced = prose + "\n\n```\n" + " ".join(["noise"] * 2000) + "\n```\n"
        self.assertEqual(_reading_minutes(fenced), 2)
        self.assertEqual(_reading_minutes(""), 1)

    def test_reading_time_counts_cjk_separately(self) -> None:
        self.assertEqual(_reading_minutes("汉" * 800), 2)
        self.assertEqual(_reading_label("汉" * 800, "zh"), "约 2 分钟")
        self.assertEqual(_reading_label(" ".join(["word"] * 220), "en"), "1 min read")

    def test_excerpt_skips_headings_and_language_links(self) -> None:
        text = (
            "# Amazon S3\n\n"
            "English · [简体中文](README_ZH.md)\n\n"
            "## Overview\n\n"
            "- bullet\n\n"
            "> Facts verified against official AWS documentation: 2026-08-18\n\n"
            "Amazon S3 is an object storage service for storing and protecting any "
            "amount of data.\n"
        )
        self.assertEqual(
            _excerpt(text, "en"),
            "Amazon S3 is an object storage service for storing and protecting any "
            "amount of data.",
        )

    def test_excerpt_truncates_long_paragraphs(self) -> None:
        long_paragraph = "# T\n\n" + " ".join(["alpha"] * 60) + "\n"
        excerpt = _excerpt(long_paragraph, "en")
        self.assertTrue(excerpt.endswith("…"))
        self.assertLessEqual(len(excerpt), 151)

    def test_related_notes_are_appended_to_articles(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            paths = []
            for slug in ("s3", "redshift"):
                for name, heading in (
                    ("README.md", f"# Amazon {slug}"),
                    ("README_ZH.md", f"# Amazon {slug} 中文"),
                ):
                    relative = f"AWS/{slug}/{name}"
                    paths.append(relative)
                    self._write(root, relative, f"{heading}\n\nBody text.\n")
            self._write(root, "pages/knowledge-base.css", "/* test */\n")
            output = root / ".pages-build"

            stage(root, output, paths)

            article = (output / "AWS/s3/index.md").read_text(encoding="utf-8")
            self.assertIn('class="kb-related"', article)
            self.assertIn("Keep reading", article)
            self.assertIn('href="../redshift/"', article)
            self.assertIn('class="kb-meta__reading"', article)

            chinese = (output / "AWS/s3/index_zh.md").read_text(encoding="utf-8")
            self.assertIn("继续阅读", chinese)
            self.assertIn('href="../../redshift/index_zh/"', chinese)

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
