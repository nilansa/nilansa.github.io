#!/usr/bin/env python3
"""Read-only corpus audit: coverage, abstract completeness and potential identity collisions.

Uses only already checked-in venue/year JSON. No network, mutation or PDF access.
"""
from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from pathlib import Path

from paper_identity import paper_key

ROOT = Path(__file__).resolve().parents[1]


def audit(root=ROOT):
    catalog = json.loads((root / "catalog.json").read_text(encoding="utf-8"))
    output = {
        "schema": "cs-conf-corpus-audit-v1",
        "note": "Counts are venue/year source records, not unique scientific works; key collisions are review candidates, not automatic merges.",
        "source_records": 0, "shards": 0, "abstracts_present": 0,
        "abstracts_missing": 0, "records_with_paper_url": 0,
        "records_in_shards_with_undeclared_license": 0,
        "candidate_identity_collisions": 0,
        "venues": {},
        "collisions_sample": [],
    }
    seen = {}
    for venue, meta in sorted(catalog.get("venues", {}).items()):
        v = {"records": 0, "abstracts": 0, "shards": 0,
             "available_years": meta.get("available_years", []),
             "unindexed_years": meta.get("missing_years", []),
             "undeclared_license_shards": []}
        for year in meta.get("available_years", []):
            entry = meta.get("years", {}).get(str(year))
            if not entry:
                raise ValueError("Missing entry for " + venue + " " + str(year))
            path = root / entry["file"]
            raw = path.read_bytes()
            if hashlib.sha256(raw).hexdigest() != entry["sha256"]:
                raise ValueError("SHA-256 mismatch: " + entry["file"])
            if len(raw) != entry["bytes"]:
                raise ValueError("Byte length mismatch: " + entry["file"])
            bundle = json.loads(raw)
            if bundle.get("year") != year or (venue != "CVPR" and bundle.get("venue") != venue):
                raise ValueError("Wrong venue/year: " + entry["file"])
            papers = bundle.get("papers")
            if not isinstance(papers, list) or len(papers) != entry["count"]:
                raise ValueError("Record count mismatch: " + entry["file"])
            undeclared = "does not declare" in str(entry.get("license") or "").lower()
            if undeclared:
                v["undeclared_license_shards"].append(year)
                output["records_in_shards_with_undeclared_license"] += len(papers)
            output["shards"] += 1
            v["shards"] += 1
            for p in papers:
                output["source_records"] += 1
                v["records"] += 1
                if p.get("abstract"):
                    output["abstracts_present"] += 1
                    v["abstracts"] += 1
                else:
                    output["abstracts_missing"] += 1
                if p.get("paper_url") or p.get("cvf_url"):
                    output["records_with_paper_url"] += 1
                identity = paper_key(dict(p, venue=venue, year=year))
                location = venue + "/" + str(year) + "/" + str(p.get("id") or p.get("title") or "")
                if identity in seen:
                    output["candidate_identity_collisions"] += 1
                    if len(output["collisions_sample"]) < 20:
                        output["collisions_sample"].append({
                            "identity": identity, "first": seen[identity], "later": location})
                else:
                    seen[identity] = location
        output["venues"][venue] = v
    output["distinct_keys_observed"] = len(seen)
    return output


def main():
    print(json.dumps(audit(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
