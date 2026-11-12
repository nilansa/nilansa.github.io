"""No-download tests for local hybrid retrieval and draft comparison."""
import hashlib
import json
import re
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

HUB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HUB / "tools"))
import semantic_retrieval as retrieval


class FakeEmbedder:
    """Stable synthetic vectors; tests never load real weights."""

    def encode(self, texts, **_kwargs):
        output = []
        for text in texts:
            text = text.replace(retrieval.QUERY_PREFIX, "")
            vector = [0.0] * retrieval.DIMENSION
            for word in re.findall(r"\w+", text.casefold()):
                position = int(hashlib.sha256(word.encode("utf-8")).hexdigest()[:8], 16) % retrieval.DIMENSION
                vector[position] += 1.0
            output.append(vector)
        return output


def write_fixture(root):
    hub = root / "hub"
    records = {
        ("ACL", 2024): [
            {"id": "acl-a", "title": "Robot planning with language models", "authors": "Jane Doe", "abstract": "A robot system learns plans from language.", "paper_url": "https://aclanthology.org/2024.acl-long.1/"},
        ],
        ("ACL", 2025): [
            {"id": "acl-b", "title": "Robot planning in images", "authors": "Jane Doe", "abstract": "", "paper_url": ""},
        ],
        ("CVPR", 2023): [
            {"id": "cvpr-c", "title": "Vision restoration with diffusion", "authors": "Alice Smith", "abstract": "Image restoration uses diffusion models.", "cvf_url": "https://openaccess.thecvf.com/content/CVPR2023/html/example.html"},
        ],
        ("NeurIPS", 2022): [
            {"id": "neurips-d", "title": "Graph representations for learning", "authors": "Ravi Shah", "abstract": "Graphs encode relations between learned objects."},
        ],
    }
    venue_metadata = {}
    for (venue, year), papers in records.items():
        rel = "data/venues/{}/{}.json".format(venue, year)
        path = hub / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        raw = (json.dumps({"venue": venue, "year": year, "papers": papers}) + "\n").encode("utf-8")
        path.write_bytes(raw)
        venue_metadata.setdefault(venue, {"available_years": [], "years": {}})
        venue_metadata[venue]["available_years"].append(year)
        venue_metadata[venue]["years"][str(year)] = {
            "file": rel,
            "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "count": len(papers),
            "source_url": "Hugging Face dataset" if venue == "CVPR" else "https://huggingface.co/datasets/ai-conferences/{}/resolve/main/data/train.parquet".format(venue + str(year)),
        }
    (hub / "catalog.json").write_text(json.dumps({
        "schema": "cs-conf-catalog-v1",
        "source_dataset": "https://huggingface.co/datasets/ai-conferences",
        "venues": venue_metadata,
    }), encoding="utf-8")
    return hub


class SemanticRetrievalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.temp.name)
        cls.hub = write_fixture(cls.root)
        cls.index = cls.root / "local-cache" / "index"
        cls.manifest = retrieval.build_index(cls.index, FakeEmbedder(), hub_root=cls.hub, batch_size=2)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_pipeline_smoke_builds_global_fts_and_aligned_float16_vectors(self):
        self.assertEqual(self.manifest["paper_count"], 4)
        self.assertEqual(self.manifest["abstract_missing_count"], 1)
        self.assertEqual(self.manifest["vector_dimension"], 384)
        rows, dimension, offset = retrieval.read_npy_info(self.index / "paper-vectors.npy")
        self.assertEqual((rows, dimension), (4, 384))
        self.assertGreater(offset, 10)
        self.assertEqual(self.index.stat().st_mode & 0o777, 0o700)
        for filename in ("manifest.json", "papers.sqlite3", "paper-vectors.npy"):
            self.assertEqual((self.index / filename).stat().st_mode & 0o777, 0o600)
        connection = sqlite3.connect(str(self.index / "papers.sqlite3"))
        try:
            self.assertEqual(connection.execute("SELECT count(*) FROM paper_fts").fetchone()[0], 4)
            self.assertEqual(connection.execute("SELECT count(*) FROM papers").fetchone()[0], rows)
        finally:
            connection.close()
        saved = json.loads((self.index / "manifest.json").read_text())
        self.assertEqual(saved["source_shards"][0]["sha256"], self.manifest["source_shards"][0]["sha256"])

    def test_hybrid_ranking_reports_real_components_and_rrf_order(self):
        results = retrieval.search_index(
            self.index, "robot planning", ["ACL"], [2024, 2025], 10, FakeEmbedder(),
        )
        self.assertEqual({(row["venue"], row["year"]) for row in results}, {("ACL", 2024), ("ACL", 2025)})
        self.assertEqual([row["rrf_rank"] for row in results], list(range(1, len(results) + 1)))
        self.assertTrue(all(row["bm25_rank"] is not None for row in results))
        self.assertTrue(all(-1.0 <= row["cosine_similarity"] <= 1.0 for row in results))
        for row in results:
            expected = 1 / (retrieval.RRF_K + row["bm25_rank"]) + 1 / (retrieval.RRF_K + row["dense_rank"])
            self.assertAlmostEqual(row["rrf_score"], expected)

    def test_multi_venue_and_year_filters_apply_to_fused_results(self):
        results = retrieval.search_index(
            self.index, "robot vision", ["ACL", "CVPR"], [2023, 2025], 10, FakeEmbedder(),
        )
        self.assertTrue(results)
        self.assertTrue(all(row["venue"] in ("ACL", "CVPR") for row in results))
        self.assertTrue(all(row["year"] in (2023, 2025) for row in results))
        self.assertNotIn(("ACL", 2024), {(row["venue"], row["year"]) for row in results})

    def test_non_url_source_label_falls_back_to_catalog_dataset_link(self):
        results = retrieval.search_index(self.index, "vision restoration", ["CVPR"], [2023], 5, FakeEmbedder())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["source_url"], "https://huggingface.co/datasets/ai-conferences")

    def test_authors_phrase_and_missing_abstract_flag(self):
        results = retrieval.search_index(self.index, "Jane Doe", ["ACL"], [2025], 5, FakeEmbedder())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["authors"], "Jane Doe")
        self.assertTrue(results[0]["abstract_missing"])

    def test_chunking_uses_overlap(self):
        chunks = retrieval.chunk_text("one two three four five six seven eight", chunk_words=5, overlap=2)
        self.assertEqual(chunks, ["one two three four five", "four five six seven eight"])
        self.assertEqual(retrieval.chunk_text("  "), [])

    def test_compare_reports_document_and_strongest_chunk_matches(self):
        results = retrieval.compare_draft(self.index, "Robot planning with language models improve a robot system.", FakeEmbedder(), 2)
        self.assertTrue(results)
        self.assertIn("document_cosine", results[0])
        self.assertIn("strongest_chunk_cosine", results[0])
        self.assertGreaterEqual(results[0]["strongest_chunk_index"], 1)
        self.assertTrue(results[0]["draft_excerpt"])

    def test_pdf_error_is_clear_when_optional_dependency_is_missing(self):
        path = self.root / "draft.pdf"
        path.write_bytes(b"synthetic placeholder")
        with patch.dict(sys.modules, {"fitz": None}):
            with self.assertRaisesRegex(RuntimeError, "optional PyMuPDF"):
                retrieval.extract_draft_text(path)

    def test_failed_build_does_not_replace_existing_index(self):
        previous_hash = retrieval.sha256_file(self.index / "manifest.json")

        class BrokenEmbedder:
            def encode(self, texts, **_kwargs):
                return [[0.0] * retrieval.DIMENSION for _ in texts]

        with self.assertRaisesRegex(ValueError, "zero vector"):
            retrieval.build_index(self.index, BrokenEmbedder(), hub_root=self.hub, rebuild=True, batch_size=2)
        self.assertEqual(retrieval.sha256_file(self.index / "manifest.json"), previous_hash)


if __name__ == "__main__":
    unittest.main()
