import hashlib
import json
import sys
import unittest
from pathlib import Path
from urllib.parse import urlsplit

HUB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HUB / "tools"))
import build_cvpr_hub
import search_cvpr


class CorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.provenance = json.loads((HUB / "provenance.json").read_text(encoding="utf-8"))

    def test_year_files_match_provenance_and_schema(self):
        self.assertEqual(set(self.provenance["years"]), {"2022", "2023", "2024", "2025", "2026"})
        total = 0
        ids = set()
        for year_text, expected in self.provenance["years"].items():
            year = int(year_text)
            raw = (HUB / "data" / f"{year}.json").read_bytes()
            self.assertEqual(len(raw), expected["output_bytes"])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), expected["output_sha256"])
            bundle = json.loads(raw)
            self.assertEqual(bundle["year"], year)
            self.assertEqual(len(bundle["papers"]), expected["count"])
            self.assertGreater(expected["count"], 0)
            total += expected["count"]
            for paper in bundle["papers"]:
                for key in ("id", "title", "authors", "abstract", "abstract_status", "pdf_url", "pdf_status", "cvf_url", "cvf_reference_type", "year", "source", "cluster", "track_status", "track_basis"):
                    self.assertIn(key, paper)
                self.assertEqual(paper["year"], year)
                self.assertEqual(paper["source"], "Hugging Face dataset")
                if paper["abstract"]:
                    self.assertEqual(paper["abstract_status"], "available")
                else:
                    self.assertEqual(paper["abstract_status"], "missing in source metadata")
                self.assertTrue(build_cvpr_hub.is_safe_pdf_url(paper["pdf_url"]))
                page = urlsplit(paper["cvf_url"])
                self.assertEqual(page.scheme, "https")
                self.assertIn(page.hostname, {"openaccess.thecvf.com", "www.openaccess.thecvf.com"})
                self.assertTrue(build_cvpr_hub.is_safe_cvf_page_url(paper["cvf_url"]))
                self.assertNotIn(paper["id"], ids)
                ids.add(paper["id"])
        self.assertEqual(total, self.provenance["total_papers"])

    def test_validation_statistics_are_clean(self):
        expected_empty = {"2022": 3, "2023": 0, "2024": 3, "2025": 0, "2026": 0}
        expected_404 = {"2022": 3, "2023": 0, "2024": 3, "2025": 0, "2026": 0}
        for year, item in self.provenance["years"].items():
            self.assertEqual(item["empty_abstracts"], expected_empty[year])
            self.assertEqual(item["invalid_input_urls"], 0)
            self.assertEqual(item["duplicates"], 0)
            self.assertEqual(item["year_mismatches"], 0)
            self.assertEqual(item["cvf_listing_matched"] + item["cvf_listing_unmatched"], item["count"])
            self.assertEqual(item["checked_404_pdf_links"], expected_404[year])
        self.assertEqual(self.provenance["link_checks"]["unavailable_count"], 6)

    def test_url_safety_and_cvf_repair(self):
        self.assertTrue(build_cvpr_hub.is_safe_pdf_url("https://openaccess.thecvf.com/content/CVPR2026/papers/sample.pdf"))
        for unsafe in (
            "http://openaccess.thecvf.com/papers/sample.pdf",
            "https://attacker.example/sample.pdf",
            "https://user@openaccess.thecvf.com/sample.pdf",
            "https://openaccess.thecvf.com/sample.pdf?token=x",
            "https://openaccess.thecvf.com/sample.html",
        ):
            self.assertFalse(build_cvpr_hub.is_safe_pdf_url(unsafe), unsafe)
        pdf, page, repaired, page_type, pdf_status = build_cvpr_hub._cvf_urls(2026, "Sample Paper", "https://invalid.example/no.pdf", "2026/pdf/sample_CVPR_2026_paper.pdf", "")
        self.assertTrue(repaired)
        self.assertTrue(build_cvpr_hub.is_safe_pdf_url(pdf))
        self.assertIn("CVPR2026/html/sample_CVPR_2026_paper.html", page)
        self.assertEqual(page_type, "paper page")
        self.assertIn("not individually", pdf_status)
        self.assertTrue(build_cvpr_hub.is_safe_cvf_page_url("https://openaccess.thecvf.com/CVPR2022?day=all"))

    def test_cvf_listing_parser_reads_original_links(self):
        parser = build_cvpr_hub.CVFIndexParser("https://openaccess.thecvf.com/CVPR2026?day=all")
        parser.feed('<dt class="ptitle"><a href="/content/CVPR2026/html/Sample_paper.html">Sample Paper</a></dt><dd>[<a href="/content/CVPR2026/papers/Sample_paper.pdf">pdf</a>]</dd>')
        parser.close()
        self.assertEqual(len(parser.entries), 1)
        self.assertEqual(parser.entries[0]["title"], "Sample Paper")
        self.assertEqual(parser.entries[0]["page_url"], "https://openaccess.thecvf.com/content/CVPR2026/html/Sample_paper.html")
        self.assertEqual(parser.entries[0]["pdf_url"], "https://openaccess.thecvf.com/content/CVPR2026/papers/Sample_paper.pdf")

    def test_search_ranking_and_phrase_boost(self):
        papers = [
            {"id":"a", "year":2025, "title":"Electric car tracking", "authors":"A. Researcher", "abstract":"A tracking system for road scenes."},
            {"id":"b", "year":2024, "title":"Vehicle scenes", "authors":"B. Researcher", "abstract":"We study electric color cues and car detection."},
            {"id":"c", "year":2025, "title":"Diffusion for Image Restoration", "authors":"C. Researcher", "abstract":"The paper improves image restoration."},
        ]
        phrase_hits = search_cvpr.rank_papers(papers, '"electric car"')
        self.assertEqual(phrase_hits[0]["id"], "a")
        title_hits = search_cvpr.rank_papers(papers, "diffusion")
        self.assertEqual(title_hits[0]["id"], "c")
        self.assertGreater(title_hits[0]["score"], 0)

    def test_basic_ui_markup(self):
        html = (HUB / "index.html").read_text(encoding="utf-8")
        for marker in ("Find the problem", "id=\"search\"", "id=\"collection\"", "id=\"idea-lab\"", "id=\"provenance\"", "UNTESTED"):
            self.assertIn(marker, html)
        self.assertTrue((HUB / "style.css").is_file())
        self.assertTrue((HUB / "app.js").is_file())
        self.assertIn("search-worker.js", (HUB / "app.js").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
