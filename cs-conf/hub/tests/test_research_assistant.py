"""Offline tests for the local conference research bridge."""
import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import research_assistant as ra


class ResearchAssistantTests(unittest.TestCase):
    def test_publisher_allowlist_rejects_bad_domains_and_credentials(self):
        good = "https://openaccess.thecvf.com/content/CVPR2026/paper.pdf"
        self.assertEqual(ra.official_url(good), good)
        for url in (
            "http://openaccess.thecvf.com/paper.pdf",
            "https://openaccess.thecvf.com.evil.org/paper.pdf",
            "https://user:password@openaccess.thecvf.com/paper.pdf",
            "https://openaccess.thecvf.com:bogus/paper.pdf",
            "https://openaccess.thecvf.com:444/paper.pdf",
            "https://169.254.169.254/latest/meta-data/",
            "https://openreview.net/forum?id=foo&redirect=https://evil.org",
            "file:///etc/passwd",
        ):
            self.assertEqual(ra.official_url(url), "", url)
        self.assertEqual(ra.official_url("https://arxiv.org/abs/2409.12345"), "")
        self.assertEqual(ra.official_url("https://arxiv.org/abs/2409.12345", True),
                         "https://arxiv.org/abs/2409.12345")

    def test_cito_search_uses_actual_hits_and_preserves_provenance(self):
        payload = {
            "hits": [{"id": "135466290", "title": "TVQA+: Spatio-Temporal Grounding",
                      "year": 2020, "abstract": "Temporal localization"}],
            "corpus_release": "2026-10", "corpus_synced_at": "2026-11-01",
            "attribution": "Data from Semantic Scholar",
        }
        with patch.object(ra, "fetch_json", return_value=payload) as fetch:
            result = ra.discover("video temporal grounding", "cito", "semantic", 2)
        self.assertEqual(len(result["papers"]), 1)
        self.assertEqual(result["papers"][0]["title"],
                         "TVQA+: Spatio-Temporal Grounding")
        self.assertEqual(result["papers"][0]["source_type"], "index-metadata-only")
        self.assertEqual(result["papers"][0]["notebook_ready"], False)
        self.assertEqual(result["provenance"]["corpus_release"], "2026-10")
        self.assertIn("mode=semantic", fetch.call_args[0][0])

    def test_semantic_scholar_metadata_and_no_secrets_in_output(self):
        payload = {"data": [{"paperId": "p123", "title": "Paper A",
                             "year": 2025, "venue": "CVPR", "abstract": "abc",
                             "url": "https://www.semanticscholar.org/paper/p123",
                             "openAccessPdf": {"url": "https://example.org/paper.pdf"}}]}
        with patch.object(ra, "fetch_json", return_value=payload) as fetch:
            data = ra.discover("test", "semantic-scholar")
        self.assertEqual(data["papers"][0]["id"], "p123")
        self.assertNotIn("S2_API_KEY", str(data))
        self.assertIn("academic-graph", data["mode"])
        self.assertIn("fields=", fetch.call_args[0][0])

    def test_pins_to_manifest_preserves_official_and_skips_untrusted(self):
        records = {"schema": "cs-conference-hub-pins-v1", "pins": [
            {"id": "1", "title": "Official", "venue": "CVPR",
             "year": 2026, "pdf_url": "https://openaccess.thecvf.com/o.pdf"},
            {"id": "2", "title": "Untrusted", "venue": "CVPR",
             "year": 2026, "paper_url": "https://evil.example/paper.pdf"},
            {"id": "3", "title": "Duplicate", "venue": "CVPR",
             "year": 2026, "pdf_url": "https://openaccess.thecvf.com/o.pdf"},
        ]}
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "pins.json"
            p.write_text(json.dumps(records))
            manifest = ra.make_manifest(str(p), "Video understanding")
        self.assertEqual(len(manifest["sources"]), 1)
        self.assertEqual(manifest["sources"][0]["status"], "SELECTED_NOT_INGESTED")
        self.assertFalse(manifest["sources"][0]["peer_review_verified"])
        self.assertEqual(len(manifest["skipped"]), 1)
        self.assertIn("Local", manifest["privacy"])

    def test_source_selection_does_not_overwrite_existing_file(self):
        with tempfile.TemporaryDirectory() as td:
            pins = Path(td) / "pins.json"
            pins.write_text('{"pins":[]}')
            out = Path(td) / "manifest.json"
            out.write_text("keep me")
            with contextlib.redirect_stdout(io.StringIO()) as output:
                rc = ra.cli_main(["select", str(pins), "--topic", "T",
                                  "--output", str(out)])
            self.assertEqual(rc, 2)
            self.assertEqual(out.read_text(), "keep me")
            self.assertIn("refusing to overwrite", output.getvalue())

    def test_upload_requires_explicit_confirmation_before_any_cli_call(self):
        with patch.object(ra, "notebook_command") as cli:
            with contextlib.redirect_stdout(io.StringIO()) as output:
                rc = ra.cli_main(["notebook-add", "/unread/manifest",
                                  "--notebook-id", "123456"])
        self.assertEqual(rc, 2)
        self.assertIn("Nothing was uploaded", output.getvalue())
        cli.assert_not_called()

    def test_missing_auth_blocks_unsourced_q_and_a(self):
        with patch.object(ra, "notebook_ready", return_value={"ready": False}):
            with patch.object(ra, "notebook_command") as cli:
                with contextlib.redirect_stdout(io.StringIO()) as output:
                    rc = ra.cli_main(["ask", "What has been done?",
                                      "--notebook-id", "paper123"])
        self.assertEqual(rc, 2)
        self.assertIn("not authenticated", output.getvalue())
        cli.assert_not_called()

    def test_authenticated_answer_requires_a_nonempty_notebook_source_list(self):
        with patch.object(ra, "notebook_ready", return_value={"ready": True}):
            with patch.object(ra, "notebook_command", return_value={"sources": []}) as cli:
                with contextlib.redirect_stdout(io.StringIO()) as output:
                    rc = ra.cli_main(["ask", "What has been done?",
                                      "--notebook-id", "paper123"])
        self.assertEqual(rc, 2)
        self.assertIn("no sources", output.getvalue())
        self.assertEqual(cli.call_count, 2)  # use context then list sources

    def test_rejects_invalid_queries(self):
        with self.assertRaises(ra.ResearchError):
            ra.discover("X" * 301)
        with self.assertRaises(ra.ResearchError):
            ra.discover("q", limit=40)


if __name__ == "__main__":
    unittest.main()
