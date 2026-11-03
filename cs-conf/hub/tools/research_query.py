#!/usr/bin/env python3
"""Grounded, offline research retrieval across indexed conference-year shards.

No LLM, server, PDF download, network request or invented paper-level facets.
JSON output is suitable for an authorized research agent or a reproducible audit.
"""
from __future__ import annotations

import argparse
import heapq
import json
import re
from pathlib import Path

from paper_identity import paper_key, stable_uid

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "cs-conf-research-query-v1"


def tokens(value):
    return re.findall(r"[^\W_]+", str(value or "").casefold(), flags=re.UNICODE)


def score(paper, query):
    """Bounded lexical ranking: title > authors > abstract, with phrase boost."""
    words = list(dict.fromkeys(tokens(query)))
    if not words:
        return 1.0
    title = tokens(paper.get("title"))
    authors = tokens(paper.get("authors"))
    abstract = tokens(paper.get("abstract"))
    sets = (set(title), set(authors), set(abstract))
    value = sum(4.0 * (w in sets[0]) + 1.5 * (w in sets[1]) + (w in sets[2]) for w in words)
    phrase = " ".join(words)
    if len(words) > 1:
        if phrase in " ".join(title):
            value += 7
        elif phrase in " ".join(abstract):
            value += 3
    return float(value)


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def select_venues(catalog, taxonomy, venues=None, areas=None):
    available = catalog.get("venues", {})
    requested = set(venues or [])
    for area in areas or []:
        found = False
        for group in taxonomy.get("areas", []):
            if group.get("id") == area:
                for sub in group.get("subareas", []):
                    requested.update(sub.get("venues", []))
                found = True
            for sub in group.get("subareas", []):
                if sub.get("id") == area:
                    requested.update(sub.get("venues", []))
                    found = True
        if not found:
            raise ValueError("Unknown taxonomy area: " + area)
    if not requested:
        requested = {"CVPR"}
    indexed = sorted(v for v in requested if available.get(v, {}).get("available_years"))
    not_indexed = sorted(requested - set(indexed))
    return sorted(requested), indexed, not_indexed


def matches_filter(p, *, author="", topic="", track="", require_abstract=False):
    if require_abstract and not str(p.get("abstract") or "").strip():
        return False
    if author and author.casefold() not in str(p.get("authors") or "").casefold():
        return False
    if topic and topic.casefold() not in (" ".join(str(p.get(k) or "") for k in ("cluster", "primary_area"))).casefold():
        return False
    if track and track.casefold() not in str(p.get("track_status") or "").casefold():
        return False
    return True


def present(p, entry, venue, year, relevance):
    record = dict(p, venue=venue, year=year)
    source_url = str(record.get("paper_url") or record.get("cvf_url") or "")
    source_dataset = entry.get("dataset_url") or entry.get("source_url") or ""
    missing = [field for field in ("abstract", "doi", "code_url", "dataset_url")
               if not str(record.get(field) or "").strip()]
    return {
        "paper_uid": stable_uid(record),
        "source_record_id": record.get("id"),
        "title": record.get("title"),
        "authors": record.get("authors") or "",
        "venue": venue,
        "year": year,
        "abstract": record.get("abstract") or "",
        "paper_url": source_url,
        "pdf_url": record.get("pdf_url") or "",
        "track_status": record.get("track_status") or "unverified",
        "area_label": record.get("primary_area") or record.get("cluster") or "",
        "doi": record.get("doi") or "",
        "code_url": record.get("code_url") or "",
        "dataset_url": record.get("dataset_url") or "",
        "relevance": relevance,
        "provenance": {
            "record_source": record.get("source") or "not specified",
            "metadata_dataset_url": source_dataset,
            "metadata_file": entry.get("file"),
            "metadata_sha256": entry.get("sha256"),
            "license_declaration": entry.get("license") or "not supplied",
            "authority": "source label; acceptance track is not independently verified",
        },
        "missing_fields": missing,
        "inferred_facets": [],
    }


def search(root, *, query="", venues=None, areas=None, year_from=2022, year_to=2026,
           author="", topic="", track="", require_abstract=False, limit=20):
    if not 1 <= limit <= 200:
        raise ValueError("Limit must be between 1 and 200")
    if year_from > year_to:
        raise ValueError("year-from must not exceed year-to")
    catalog = read_json(root / "catalog.json")
    taxonomy = read_json(root / "taxonomy.json")
    requested, indexed, unindexed = select_venues(catalog, taxonomy, venues, areas)
    scanned = matching = 0
    # Keep memory bounded even when many conferences are selected. Store only top-N.
    heap = []
    used = set()
    for venue in indexed:
        for year in range(year_from, year_to + 1):
            entry = catalog["venues"][venue].get("years", {}).get(str(year))
            if not entry:
                continue
            path = root / entry["file"]
            if not path.is_file():
                raise FileNotFoundError("Catalog shard missing: " + entry["file"])
            bundle = read_json(path)
            if bundle.get("year") != year or not isinstance(bundle.get("papers"), list):
                raise ValueError("Malformed shard: " + entry["file"])
            if venue != "CVPR" and bundle.get("venue") != venue:
                raise ValueError("Shard/venue mismatch: " + entry["file"])
            for p in bundle["papers"]:
                scanned += 1
                if not p.get("title") or not matches_filter(p, author=author, topic=topic, track=track, require_abstract=require_abstract):
                    continue
                relevance = score(p, query)
                if query.strip() and relevance <= 0:
                    continue
                matching += 1
                paper = dict(p, venue=venue, year=year)
                identity = paper_key(paper)
                # Deduplicate on the final selected results, not across the entire corpus.
                # A future importer must keep a full persistent equivalence table.
                order = (relevance, year, venue, str(p.get("title") or ""))
                row = (order, scanned, identity, present(p, entry, venue, year, relevance))
                if len(heap) < limit:
                    heapq.heappush(heap, row)
                elif order > heap[0][0]:
                    heapq.heapreplace(heap, row)
    hits = sorted(heap, key=lambda x: x[0], reverse=True)
    # Do not invent missing rows to compensate for collisions.
    deduped = []
    for _, _, identity, record in hits:
        if identity not in used:
            used.add(identity)
            deduped.append(record)
    return {
        "schema": SCHEMA,
        "query": query,
        "selection": {
            "requested_venues": requested, "indexed_venues": indexed,
            "unindexed_venues": unindexed, "taxonomy_areas": areas or [],
            "year_from": year_from, "year_to": year_to,
            "filters": {"author": author, "topic": topic, "track": track, "require_abstract": require_abstract},
        },
        "scanned_records": scanned,
        "matching_records_before_deduplication": matching,
        "returned_records": len(deduped),
        "results": deduped,
        "limitations": [
            "Lexical retrieval only; relevance is not novelty or semantic similarity.",
            "Main-track acceptance and derived method/task/evaluation facets are unverified unless an authoritative source says otherwise.",
            "Source abstracts and links may be missing or subject to independent rights; inspect the original publisher record.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", nargs="?", default="", help="Lexical paper search query; empty lists the selected corpus")
    parser.add_argument("--venue", action="append", help="Repeat for multiple venues (e.g. CVPR and ACL)")
    parser.add_argument("--area", action="append", help="Top-level taxonomy area or subarea ID")
    parser.add_argument("--year-from", type=int, default=2022)
    parser.add_argument("--year-to", type=int, default=2026)
    parser.add_argument("--author", default="")
    parser.add_argument("--topic", default="", help="Source area/cluster text, not an inferred topic")
    parser.add_argument("--track", default="", help="Only matched in source track_status text")
    parser.add_argument("--require-abstract", action="store_true")
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()
    try:
        response = search(ROOT, query=args.query, venues=args.venue, areas=args.area,
                          year_from=args.year_from, year_to=args.year_to, author=args.author,
                          topic=args.topic, track=args.track,
                          require_abstract=args.require_abstract, limit=args.limit)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.exit(2, "research_query: " + str(exc) + "\n")
    print(json.dumps(response, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
