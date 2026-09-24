from __future__ import annotations

import re
import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree

from scripts.knowledge_base import (
    AWS_GROUPS,
    EXCERPT_LENGTH,
    FEED_LIMIT,
    HOME_DENSE_LIMIT,
    HOME_RICH_LIMIT,
    HOME_TOPIC_EXCLUDE,
    KIND_SLUGS,
    RICH_PER_AREA,
    SITE_URL,
    TOPIC_META,
    KnowledgeBaseError,
    _archive_years,
    _blog_documents,
    _dense_feed_html,
    _excerpt,
    _feed_xml,
    _home_areas,
    _lead_selection,
    _reading_label,
    _reading_minutes,
    _summary_markdown,
    discover_documents,
    stage,
)


class KnowledgeBaseTests(unittest.TestCase):
    def test_discovers_documents_and_derives_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._write(root, "AWS/README.md", "# AWS\n")

            documents = discover_documents(root, ["AWS/README.md"])

            self.assertEqual(len(documents), 1)
            document = documents[0]
            self.assertEqual(document.page, "AWS/index.md")
            self.assertEqual(document.area, "AWS")
            self.assertEqual(document.kind, "catalog")

    def test_missing_local_link_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._write(root, "AWS/README.md", "# AWS\n\n[Missing](missing/README.md)\n")

            with self.assertRaisesRegex(KnowledgeBaseError, "missing local link target"):
                discover_documents(root, ["AWS/README.md"])

    def test_mermaid_requires_accessible_title_and_description(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            diagram = "# AWS\n\n```mermaid\nflowchart TD\nA --> B\n```\n"
            self._write(root, "AWS/README.md", diagram)

            with self.assertRaisesRegex(KnowledgeBaseError, "missing accTitle"):
                discover_documents(root, ["AWS/README.md"])

    def test_accessible_mermaid_diagram_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            english = (
                "# AWS\n\n```mermaid\nflowchart TD\n"
                "accTitle: Overview\naccDescr: A flows to B.\nA --> B\n```\n"
            )
            self._write(root, "AWS/README.md", english)

            documents = discover_documents(root, ["AWS/README.md"])

            self.assertEqual(len(documents), 1)

    def test_stage_rewrites_links_and_excludes_internal_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            paths = [
                "README.md",
                "AWS/README.md",
                "Git/README.md",
                "apple/container/README.md",
                "AGENTS.md",
                ".agents/skills/youtube-transcript/SKILL.md",
            ]
            self._write(
                root,
                "README.md",
                "# Engineering\n\n[AWS](AWS/) · [Rules](AGENTS.md) · "
                "[Skill](.agents/skills/youtube-transcript/)\n",
            )
            self._write(root, "AWS/README.md", "# AWS\n")
            self._write(root, "Git/README.md", "# Git\n")
            self._write(root, "apple/container/README.md", "# Apple Container\n")
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
            dashboard = (output / "index.md").read_text(encoding="utf-8")
            # The deploy smoke test greps the live page for the site owner's
            # name, and a reader should see whose notes these are.
            self.assertIn("Kelvin", dashboard)
            self.assertIn('class="kb-tabs"', dashboard)
            self.assertIn('class="kb-lead__title"', dashboard)
            # Publication order is the only ranking: no topic tiles, no
            # curated shortcuts competing with the timeline.
            self.assertNotIn('class="kb-topic-card"', dashboard)
            self.assertIn('href="apple/container/"', dashboard)
            self.assertIn('href="archive/"', dashboard)
            # The timeline is the navigation, so the left rail stays hidden.
            self.assertIn("  - navigation", dashboard)
            topics = (output / "topics/index.md").read_text(encoding="utf-8")
            self.assertIn('href="../apple/container/"', topics)
            self.assertIn('class="kb-topic-card__count">1 note</span>', topics)
            archive = (output / "archive/index.md").read_text(encoding="utf-8")
            self.assertIn('class="kb-feed__month"', archive)
            # An article names its source file; the footer links to it.
            self.assertIn("kb_source: https://github.com/", repository)
            self.assertIn('class="kb-topic-card__monogram"', topics)
            self.assertTrue((output / "archive/index.md").exists())
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
            if document.page.startswith("AWS/") and document.page != "AWS/index.md"
        }
        mapped = {f"AWS/{slug}/index.md" for slug in slugs}
        self.assertEqual(
            pages - mapped,
            set(),
            "new AWS pages need a home in AWS_GROUPS",
        )
        self.assertEqual(mapped - pages, set(), "AWS_GROUPS names a missing page")
        self.assertNotIn("- More", _summary_markdown(documents))

    def test_summary_nests_sections(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._write(root, "Git/README.md", "# Git\n")
            self._write(root, "AWS/README.md", "# AWS\n")
            self._write(root, "AWS/s3/README.md", "# Amazon S3 - Runbook & Reference\n")
            documents = discover_documents(
                root,
                ["Git/README.md", "AWS/README.md", "AWS/s3/README.md"],
            )

            summary = _summary_markdown(documents)

            self.assertIn("- AWS\n", summary)
            self.assertIn("    - Storage & migration\n", summary)
            # The shared article-title suffix is trimmed for the sidebar.
            self.assertIn("        - [Amazon S3](AWS/s3/index.md)\n", summary)

    def test_home_topics_all_have_a_name_and_blurb(self) -> None:
        """A tile with no curated name falls back to an article title."""

        root = Path(__file__).resolve().parents[2]
        documents = discover_documents(root)
        for area in _home_areas(documents):
            self.assertIn(area, TOPIC_META, f"{area} needs a TOPIC_META entry")
        for area in HOME_TOPIC_EXCLUDE:
            self.assertNotIn(area, _home_areas(documents))

    def test_feed_is_reverse_chronological_and_grouped_by_month(self) -> None:
        """Publication order is the site's only ranking."""

        root = Path(__file__).resolve().parents[2]
        documents = discover_documents(root)
        notes = _blog_documents(documents)

        dates = [document.published for document in notes if document.published]
        self.assertEqual(dates, sorted(dates, reverse=True))

        feed = _dense_feed_html(notes[:HOME_DENSE_LIMIT], "index.md")
        self.assertEqual(
            feed.count('class="kb-row"'), min(HOME_DENSE_LIMIT, len(notes))
        )
        # Months appear once each, newest first.
        months = re.findall(r'id="feed-([0-9]{4}-[0-9]{2})"', feed)
        self.assertEqual(months, sorted(set(months), reverse=True))

    def test_archive_feed_holds_every_note(self) -> None:
        root = Path(__file__).resolve().parents[2]
        documents = discover_documents(root)
        notes = _blog_documents(documents)
        feed = _dense_feed_html(notes, "archive/index.md")
        self.assertEqual(feed.count('class="kb-row"'), len(notes))

    def test_lead_notes_keep_order_and_spread_topics(self) -> None:
        """The leads are the newest notes, minus a topic's third in a row."""

        root = Path(__file__).resolve().parents[2]
        notes = _blog_documents(discover_documents(root))

        lead, rest = _lead_selection(notes)

        self.assertEqual(len(lead), HOME_RICH_LIMIT)
        self.assertEqual(len(lead) + len(rest), len(notes))
        # Order is untouched: a lead is never older than what follows it.
        for chosen in lead:
            self.assertLessEqual(notes.index(chosen), len(lead) + RICH_PER_AREA)
        counts: dict[str, int] = {}
        for document in lead:
            counts[document.area] = counts.get(document.area, 0) + 1
        self.assertLessEqual(max(counts.values()), RICH_PER_AREA)
        dense = [document.source for document in rest]
        self.assertEqual(dense, sorted(set(dense), key=dense.index))

    def test_every_kind_has_its_own_timeline(self) -> None:
        """The tabs point at real pages."""

        root = Path(__file__).resolve().parents[2]
        documents = discover_documents(root)
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "build"
            stage(root, output)
            for kind, slug in KIND_SLUGS.items():
                present = any(document.kind == kind for document in documents)
                page = output / slug / "index.md"
                self.assertEqual(
                    page.is_file(), present, f"{slug}/index.md does not match its notes"
                )
                if present:
                    body = page.read_text(encoding="utf-8")
                    self.assertIn('aria-current="page"', body)

    def test_feed_carries_the_newest_notes(self) -> None:
        root = Path(__file__).resolve().parents[2]
        documents = discover_documents(root)
        notes = _blog_documents(documents)
        feed = _feed_xml(documents, {})
        root_element = ElementTree.fromstring(feed)
        items = root_element.findall(".//item")
        self.assertEqual(len(items), min(FEED_LIMIT, len(notes)))
        self.assertEqual(items[0].findtext("title"), notes[0].title)
        self.assertIn("feed.xml", feed)
        # Links are absolute, as a feed reader needs them.
        for item in items:
            self.assertTrue((item.findtext("link") or "").startswith(SITE_URL))

    def test_archive_splits_by_year(self) -> None:
        root = Path(__file__).resolve().parents[2]
        documents = discover_documents(root)
        years = [label for label, _ in _archive_years(documents)]
        self.assertEqual(years, sorted(years, reverse=True))
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "build"
            stage(root, output)
            # The newest year is the archive's front page; the others get one
            # page each.
            self.assertTrue((output / "archive/index.md").is_file())
            for year in years[1:]:
                self.assertTrue((output / "archive" / year / "index.md").is_file())

    def test_excerpt_skips_a_bare_lead_in_line(self) -> None:
        """Many articles open with the same colon-terminated lead-in."""

        text = (
            "# Amazon Athena\n\n"
            "This article answers three practical questions:\n\n"
            "Athena reads data straight out of S3, so partitioning and file "
            "layout decide the bill more than the query text does.\n"
        )

        self.assertTrue(_excerpt(text).startswith("Athena reads data"))

    def test_reading_time_ignores_markdown_syntax(self) -> None:
        prose = " ".join(["word"] * 440)
        self.assertEqual(_reading_minutes(prose), 2)
        fenced = prose + "\n\n```\n" + " ".join(["noise"] * 2000) + "\n```\n"
        self.assertEqual(_reading_minutes(fenced), 2)
        self.assertEqual(_reading_minutes(""), 1)

    def test_reading_label_reports_minutes(self) -> None:
        self.assertEqual(_reading_label(" ".join(["word"] * 220)), "1 min read")
        self.assertEqual(_reading_label(" ".join(["word"] * 440)), "2 min read")

    def test_excerpt_skips_headings_and_bullets(self) -> None:
        text = (
            "# Amazon S3\n\n"
            "## Overview\n\n"
            "- bullet\n\n"
            "> Facts verified against official AWS documentation: 2026-08-18\n\n"
            "Amazon S3 is an object storage service for storing and protecting any "
            "amount of data.\n"
        )
        self.assertEqual(
            _excerpt(text),
            "Amazon S3 is an object storage service for storing and protecting any "
            "amount of data.",
        )

    def test_excerpt_prefers_the_opening_framing_blockquote(self) -> None:
        text = (
            "# Amazon SQS\n\n"
            "> Facts verified against official AWS documentation: 2026-08-19\n\n"
            "> Amazon SQS is a fully managed message queue for decoupling "
            "distributed systems.\n\n"
            "## Overview\n\n"
            "> A later callout that should never become the excerpt text.\n"
        )
        self.assertEqual(
            _excerpt(text),
            "Amazon SQS is a fully managed message queue for decoupling "
            "distributed systems.",
        )

    def test_excerpt_keeps_punctuation_attached_to_emphasis(self) -> None:
        text = "# T\n\n> It becomes one **conversation**. Run `ls` first.\n"
        self.assertEqual(_excerpt(text), "It becomes one conversation. Run ls first.")

    def test_excerpt_truncates_long_paragraphs(self) -> None:
        long_paragraph = "# T\n\n" + " ".join(["alpha"] * 60) + "\n"
        excerpt = _excerpt(long_paragraph)
        self.assertTrue(excerpt.endswith("…"))
        self.assertLessEqual(len(excerpt), EXCERPT_LENGTH + 1)

    def test_related_notes_are_appended_to_articles(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            paths = []
            for slug in ("s3", "redshift"):
                relative = f"AWS/{slug}/README.md"
                paths.append(relative)
                self._write(root, relative, f"# Amazon {slug}\n\nBody text.\n")
            self._write(root, "pages/knowledge-base.css", "/* test */\n")
            output = root / ".pages-build"

            stage(root, output, paths)

            article = (output / "AWS/s3/index.md").read_text(encoding="utf-8")
            self.assertIn('class="kb-related"', article)
            self.assertIn("Keep reading", article)
            self.assertIn('href="../redshift/"', article)
            self.assertIn('class="kb-meta__reading"', article)

    def test_youtube_summary_keeps_video_id(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = "YouTube/startup/lesson/summary.md"
            source = "# Lesson\n\nSource: https://www.youtube.com/watch?v=5-G9WHwQMwQ\n"
            self._write(root, path, source)

            documents = discover_documents(root, [path])

            self.assertEqual({document.video_id for document in documents}, {"5-G9WHwQMwQ"})
            self.assertEqual({document.kind for document in documents}, {"video-summary"})

    @staticmethod
    def _write(root: Path, relative: str, text: str) -> None:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
