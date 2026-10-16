#!/usr/bin/env python3
"""Local structural, link, and privacy checks for the static library."""

from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "shared" / "site"
if not SITE.is_dir():
    SITE = ROOT
SOURCE = ROOT / "shared" / "source" / "greenhome"
EXPECTED_EXTERNAL = {
    "https://nilansa.github.io/ire-project-2026/",
    "https://nilansa.github.io/ire-project-2026/metrics.html",
}
PRIVATE_TEXT = re.compile(
    r"/Users/|/home/|/private/|tskey-[A-Za-z0-9_-]{10,}|"
    r"github_pat_[A-Za-z0-9_]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|"
    r"AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----|"
    r"(?:[A-Za-z0-9-]+\.)+tail[a-z0-9.-]*\.net",
    re.IGNORECASE,
)


class References(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.references = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        for name in ("href", "src", "poster"):
            if attrs.get(name):
                self.references.append((tag, name, attrs[name], attrs.get("rel", "").casefold().split()))
        if tag == "a" and attrs.get("name"):
            self.ids.add(attrs["name"])


def audit_html(path):
    parser = References()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


class LibraryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.entries = json.loads((SITE / "library.json").read_text(encoding="utf-8"))

    def test_catalog_entries_and_targets(self):
        self.assertGreaterEqual(len(self.entries), 12)
        self.assertEqual(len({entry["id"] for entry in self.entries}), len(self.entries))
        self.assertEqual(len({entry["url"] for entry in self.entries}), len(self.entries))
        local = [entry for entry in self.entries if entry["url"].startswith("./")]
        external = {entry["url"] for entry in self.entries if entry["url"].startswith("https://")}
        self.assertEqual(len(local), len(self.entries) - 2)
        self.assertEqual(external, EXPECTED_EXTERNAL)
        for entry in self.entries:
            for field in ("id", "title", "description", "project", "category", "tags", "url"):
                self.assertIn(field, entry)
            self.assertTrue(entry["tags"])
        for entry in local:
            target = (SITE / entry["url"][2:]).resolve()
            self.assertTrue(target.is_file(), f"missing catalog target: {entry['url']}")
        if SOURCE.is_dir():
            source_pages = {path.name for path in SOURCE.glob("*.html")}
            copied_pages = {Path(entry["url"]).name for entry in local}
            self.assertTrue(source_pages <= copied_pages)
            robots = '<meta name="robots" content="noindex,nofollow,noarchive">'
            for filename in source_pages:
                original = (SOURCE / filename).read_text(encoding="utf-8")
                copied = (SITE / "explainers" / "greenhome" / filename).read_text(encoding="utf-8")
                self.assertEqual(copied.count(robots), 1)
                self.assertEqual(copied.replace(robots, "", 1), original, f"unexpected source edit: {filename}")
            for asset in ("style.css", "app.js"):
                self.assertEqual(
                    (SOURCE / "assets" / asset).read_bytes(),
                    (SITE / "explainers" / "greenhome" / "assets" / asset).read_bytes(),
                    f"asset copy differs: {asset}",
                )

    def test_all_hosted_html_is_noindex_and_local_links_resolve(self):
        html_files = sorted(SITE.rglob("*.html"))
        local_entries = [entry for entry in self.entries if entry["url"].startswith("./")]
        self.assertEqual(len(html_files), len(local_entries) + 1)
        checked_links = 0
        for path in html_files:
            text = path.read_text(encoding="utf-8")
            self.assertRegex(text, re.compile(r'<meta\s+name=["\']robots["\']\s+content=["\'][^"\']*\bnoindex\b', re.I), str(path))
            parser = audit_html(path)
            for tag, attr, reference, _rel in parser.references:
                parts = urlsplit(reference)
                if parts.scheme or parts.netloc or reference.startswith("//"):
                    if tag == "script" or (tag == "link" and "stylesheet" in text[max(0, text.find(reference) - 200):text.find(reference)].casefold()):
                        self.fail(f"remote code/style dependency in {path}: {reference}")
                    continue
                if not parts.path:
                    if parts.fragment:
                        self.assertIn(unquote(parts.fragment), parser.ids, f"missing fragment in {path}: {reference}")
                    continue
                target = (path.parent / unquote(parts.path)).resolve()
                if target.is_dir():
                    target = target / "index.html"
                self.assertTrue(target.is_relative_to(SITE.resolve()), f"link escapes site: {path}: {reference}")
                self.assertTrue(target.is_file(), f"missing linked file: {path}: {reference}")
                checked_links += 1
                if parts.fragment:
                    target_parser = audit_html(target) if target.suffix.casefold() == ".html" else None
                    if target_parser:
                        self.assertIn(unquote(parts.fragment), target_parser.ids, f"missing fragment: {path}: {reference}")
        type(self).checked_local_links = checked_links
        type(self).hosted_html_count = len(html_files)
        self.assertTrue((SITE / "explainers/greenhome/assets/style.css").is_file())
        self.assertTrue((SITE / "explainers/greenhome/assets/app.js").is_file())
        self.assertGreaterEqual(checked_links, 50)

    def test_library_counts_come_from_loaded_catalog(self):
        landing = (SITE / "index.html").read_text(encoding="utf-8")
        script = (SITE / "assets" / "app.js").read_text(encoding="utf-8")
        self.assertIn('id="intro-count"', landing)
        self.assertIn('id="sidebar-count"', landing)
        self.assertIn("const count = entries.length;", script)
        self.assertIn("updateLibraryCounts();", script)
        self.assertGreaterEqual(len(self.entries), 12)

    def test_ire_entry_titles_and_descriptions(self):
        entries = {entry["id"]: entry for entry in self.entries}
        self.assertEqual(entries["ire-project"]["title"], "Search-Induced Supervision")
        self.assertEqual(entries["ire-project-metrics"]["title"], "Retrieval Metrics & Research Audit")
        self.assertIn("search-induced supervision", entries["ire-project"]["description"].casefold())
        self.assertIn("retrieval metrics", entries["ire-project-metrics"]["description"].casefold())

    def test_runtime_has_no_remote_asset_or_api_dependency(self):
        for path in SITE.rglob("*.html"):
            for tag, attr, reference, _rel in audit_html(path).references:
                parts = urlsplit(reference)
                if parts.scheme or parts.netloc or reference.startswith("//"):
                    if tag not in {"a", "area"}:
                        self.fail(f"remote runtime asset in {path}: {reference}")
        for path in SITE.rglob("*.css"):
            text = path.read_text(encoding="utf-8")
            self.assertNotRegex(text, re.compile(r"@import\s+(?:url\()?\s*['\"]?https?://", re.I), str(path))
            self.assertNotRegex(text, re.compile(r"url\(\s*['\"]?https?://", re.I), str(path))
        for path in SITE.rglob("*.js"):
            text = path.read_text(encoding="utf-8")
            self.assertNotRegex(text, re.compile(r"fetch\s*\(\s*['\"]https?://|XMLHttpRequest|importScripts\s*\(", re.I), str(path))

    def test_privacy_notice_and_exported_text_scan(self):
        landing = (SITE / "index.html").read_text(encoding="utf-8")
        self.assertIn("Link-only, not access-controlled.", landing)
        for path in SITE.rglob("*"):
            if path.is_file() and path.suffix.casefold() in {".html", ".json", ".js", ".css", ".md"}:
                text = path.read_text(encoding="utf-8")
                self.assertIsNone(PRIVATE_TEXT.search(text), f"private path or secret-like string in {path.relative_to(SITE)}")

    def test_explicit_page_intake_in_both_layouts(self):
        script = ROOT / "scripts" / "add_page.py"
        for layout in ("scratch", "repository"):
            with self.subTest(layout=layout), tempfile.TemporaryDirectory(prefix="library-test-") as temp:
                temp_root = Path(temp)
                site = temp_root / "shared" / "site" if layout == "scratch" else temp_root
                site.mkdir(parents=True, exist_ok=True)
                (site / "library.json").write_text("[]\n", encoding="utf-8")
                script_dir = temp_root / "scripts"
                script_dir.mkdir(exist_ok=True)
                local_script = script_dir / "add_page.py"
                local_script.write_text(script.read_text(encoding="utf-8"), encoding="utf-8")
                source = temp_root / "approved.html"
                source_text = "<!doctype html><html><head><title>Approved</title></head><body><main>Public guide.</main></body></html>\n"
                source.write_text(source_text, encoding="utf-8")
                args = [
                    sys.executable, str(local_script), str(source), "--id", "approved-guide", "--title", "Approved guide",
                    "--description", "An approved public guide.", "--project", "GreenHome",
                    "--category", "Further reading", "--tags", "guide", "evidence",
                ]
                added = subprocess.run(args, capture_output=True, text=True, check=False)
                self.assertEqual(added.returncode, 0, added.stderr)
                destination = site / "explainers" / "greenhome" / "approved-guide.html"
                original = destination.read_text(encoding="utf-8")
                self.assertIn('name="robots" content="noindex,nofollow,noarchive"', original)
                self.assertEqual(source.read_text(encoding="utf-8"), source_text)
                self.assertEqual(len(json.loads((site / "library.json").read_text(encoding="utf-8"))), 1)

                rejected = subprocess.run(args, capture_output=True, text=True, check=False)
                self.assertEqual(rejected.returncode, 1)
                self.assertIn("already exists", rejected.stderr)
                self.assertEqual(destination.read_text(encoding="utf-8"), original)
                self.assertEqual(len(json.loads((site / "library.json").read_text(encoding="utf-8"))), 1)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(LibraryTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result.wasSuccessful():
        print("\nMETRIC\tVALUE")
        print(f"catalog_entries\t{len(LibraryTests.entries)}")
        print(f"hosted_html_noindex\t{LibraryTests.hosted_html_count}")
        print(f"source_pages_copied\t{sum(1 for _ in SOURCE.glob('*.html'))}")
        print(f"local_links_and_assets_checked\t{LibraryTests.checked_local_links}")
    raise SystemExit(not result.wasSuccessful())
