"""Offline contract tests; run with python3 -m unittest discover -s cs-conf/hub/tests."""
from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

HUB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HUB / "tools"))
import paper_identity
import research_query


class TaxonomyTests(unittest.TestCase):
    def test_four_primary_areas_and_independent_subareas(self):
        taxonomy = json.loads((HUB / "taxonomy.json").read_text(encoding="utf-8"))
        self.assertEqual(taxonomy["schema"], "cs-conf-research-taxonomy-v1")
        self.assertEqual([a["id"] for a in taxonomy["areas"]], ["ai", "systems", "theory", "interdisciplinary"])
        subareas = [s for area in taxonomy["areas"] for s in area["subareas"]]
        self.assertGreaterEqual(len(subareas), 30)
        self.assertEqual(len({s["id"] for s in subareas}), len(subareas))
        all_venues = {v for s in subareas for v in s["venues"]}
        self.assertGreaterEqual(len(all_venues), 80)
        self.assertTrue({"SOSP", "OSDI", "SIGMOD", "SIGCOMM", "CCS", "STOC", "CHI"} <= all_venues)

    def test_existing_corpus_membership_and_licensing_not_misrepresented(self):
        catalog = json.loads((HUB / "catalog.json").read_text(encoding="utf-8"))
        taxonomy = json.loads((HUB / "taxonomy.json").read_text(encoding="utf-8"))
        all_venues = {v for area in taxonomy["areas"] for sub in area["subareas"] for v in sub["venues"]}
        self.assertTrue(set(catalog["venues"]) <= all_venues)
        self.assertEqual(sum(meta["total_records"] for meta in catalog["venues"].values()), 130361)
        self.assertEqual(catalog["venues"]["CVPR"]["total_records"], 14083)
        self.assertEqual(catalog["venues"]["ICCV"]["missing_years"], [2022, 2024, 2026])
        self.assertIn("does not declare", catalog["venues"]["ICCV"]["years"]["2025"]["license"].lower())

    def test_ui_uses_real_catalog_and_nested_multiselect(self):
        app = (HUB / "app.js").read_text(encoding="utf-8")
        self.assertIn('fetch("taxonomy.json")', app)
        self.assertIn('new Set(checked(".venue-check"))', app)
        self.assertIn('function syncVenue(', app)
        self.assertIn('" · not indexed"', app)


class IdentityTests(unittest.TestCase):
    def test_doi_priority_over_title(self):
        a = {"title": "A Paper", "venue": "CVPR", "year": 2025, "doi": "DOI:10.1234/ABC"}
        b = {"title": "Different Title", "venue": "ACL", "year": 2026, "doi": "https://doi.org/10.1234/abc"}
        self.assertEqual(paper_identity.paper_key(a), "doi:10.1234/abc")
        self.assertEqual(paper_identity.stable_uid(a), paper_identity.stable_uid(b))

    def test_openreview_and_anthology_links(self):
        a = {"title": "A", "venue": "ICLR", "year": 2026,
             "paper_url": "https://openreview.net/forum?id=AbCdEfghi9"}
        b = {"title": "B", "venue": "ACL", "year": 2024,
             "paper_url": "https://aclanthology.org/2024.acl-long.20/"}
        self.assertEqual(paper_identity.paper_key(a), "openreview:AbCdEfghi9")
        self.assertEqual(paper_identity.paper_key(b), "anthology:2024.acl-long.20")

    def test_fallback_keeps_different_venues_distinct(self):
        a = {"title": "  Efficient INDEX–design!", "venue": "SIGMOD", "year": 2024}
        b = {"title": "Efficient Index design", "venue": "OSDI", "year": 2024}
        self.assertNotEqual(paper_identity.paper_key(a), paper_identity.paper_key(b))
        self.assertEqual(paper_identity.normalize_title(a["title"]), paper_identity.normalize_title(b["title"]))

    def test_bad_identity_rejected(self):
        with self.assertRaises(ValueError):
            paper_identity.paper_key({"title": "A", "year": 2024})


class ResearchQueryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "data").mkdir()
        (self.root / "data/venues/ACL").mkdir(parents=True)
        taxonomy = json.loads((HUB / "taxonomy.json").read_text(encoding="utf-8"))
        (self.root / "taxonomy.json").write_text(json.dumps(taxonomy), encoding="utf-8")
        cvpr = {"venue": "CVPR", "year": 2024, "papers": [
            {"id": "a", "title": "Adaptive Retrieval in Video", "authors": "Ada Lovelace",
             "abstract": "A new retrieval method for video.", "source": "official", "paper_url": "https://openaccess.thecvf.com/",
             "cluster": "Computer Vision"},
            {"id": "b", "title": "Picture of an Ocean", "authors": "Babbage", "abstract": "", "source": "archive"},
        ]}
        acl = {"venue": "ACL", "year": 2024, "papers": [
            {"id": "c", "title": "Adaptive Retrieval for Dialogue", "authors": "Grace Hopper",
             "abstract": "Retrieval for language.", "source": "official", "paper_url": "https://aclanthology.org/2024.acl-long.20/"}]}
        for file, bundle in [("data/2024.json", cvpr), ("data/venues/ACL/2024.json", acl)]:
            raw = (json.dumps(bundle) + "\n").encode("utf-8")
            (self.root / file).write_bytes(raw)
        def entry(file, count):
            raw = (self.root / file).read_bytes()
            return {"file": file, "count": count, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(),
                    "source_url": "https://example.edu/metadata", "license": "unknown"}
        catalog = {"venues": {"CVPR": {"available_years": [2024], "years": {"2024": entry("data/2024.json", 2)}},
                              "ACL": {"available_years": [2024], "years": {"2024": entry("data/venues/ACL/2024.json", 1)}}}}
        (self.root / "catalog.json").write_text(json.dumps(catalog), encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_research_across_venues_with_provenance(self):
        result = research_query.search(self.root, query="adaptive retrieval", venues=["CVPR", "ACL", "OSDI"],
                                       year_from=2022, year_to=2026)
        self.assertEqual(result["scanned_records"], 3)
        self.assertEqual(result["matching_records_before_deduplication"], 2)
        self.assertEqual(result["returned_records"], 2)
        self.assertEqual({p["venue"] for p in result["results"]}, {"CVPR", "ACL"})
        self.assertEqual(result["selection"]["unindexed_venues"], ["OSDI"])
        self.assertTrue(all(x["provenance"]["metadata_sha256"] and x["inferred_facets"] == [] for x in result["results"]))

    def test_author_abstract_and_source_area_filters(self):
        result = research_query.search(self.root, query="retrieval", venues=["CVPR", "ACL"],
                                       author="ADA", topic="vision", require_abstract=True)
        self.assertEqual(result["returned_records"], 1)
        self.assertEqual(result["results"][0]["source_record_id"], "a")

    def test_area_selection_deduplicates_venue_names(self):
        taxonomy = json.loads((self.root / "taxonomy.json").read_text())
        catalog = json.loads((self.root / "catalog.json").read_text())
        requested, indexed, unindexed = research_query.select_venues(catalog, taxonomy, areas=["ai"])
        self.assertEqual(len(requested), len(set(requested)))
        self.assertTrue({"CVPR", "ACL"} <= set(indexed))
        self.assertIn("NeurIPS", unindexed)

    def test_invalid_input_and_missing_shard_do_not_silently_skip(self):
        with self.assertRaises(ValueError):
            research_query.search(self.root, year_from=2025, year_to=2024)
        with self.assertRaises(ValueError):
            research_query.search(self.root, areas=["nonexistent"])
        (self.root / "data/2024.json").unlink()
        with self.assertRaises(FileNotFoundError):
            research_query.search(self.root, venues=["CVPR"], year_from=2024, year_to=2024)


if __name__ == "__main__":
    unittest.main()
