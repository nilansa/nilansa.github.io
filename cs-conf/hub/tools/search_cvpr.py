#!/usr/bin/env python3
"""Search the checked-in CVPR abstract index without network access."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
import textwrap
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOKEN_RE = re.compile(r"[\w+#.-]+", re.UNICODE)


def tokens(text: str) -> list[str]:
    return [clean for part in TOKEN_RE.findall(text) if (clean := part.strip(".-").casefold())]


def normalized(text: str) -> str:
    return " ".join(tokens(text))


def contains_whole_phrase(haystack: str, phrase: str) -> bool:
    return bool(phrase) and f" {phrase} " in f" {haystack} "


def rank_papers(papers: list[dict], query: str) -> list[dict]:
    query_terms = tokens(query)
    phrase = normalized(query.strip().strip('"\''))
    if not query_terms:
        return []
    fields = []
    document_frequency: Counter[str] = Counter()
    total_length = 0
    for paper in papers:
        title_terms = Counter(tokens(paper.get("title", "")))
        author_terms = Counter(tokens(paper.get("authors", "")))
        body_terms = Counter(tokens(paper.get("abstract", "")))
        combined = title_terms + author_terms + body_terms
        document_frequency.update(set(combined))
        length = sum(body_terms.values()) + sum(author_terms.values()) + 2 * sum(title_terms.values())
        total_length += length
        fields.append((title_terms, author_terms, body_terms, length))
    avg_length = max(total_length / max(len(papers), 1), 1)
    output = []
    for paper, (title_terms, author_terms, body_terms, length) in zip(papers, fields):
        score = 0.0
        for term in set(query_terms):
            tf = 3.0 * title_terms[term] + 1.2 * author_terms[term] + body_terms[term]
            if not tf:
                continue
            df = document_frequency[term]
            idf = math.log(1 + (len(papers) - df + 0.5) / (df + 0.5))
            score += idf * (tf * 2.2) / (tf + 1.2 * (0.25 + 0.75 * length / avg_length))
        title_text = normalized(paper.get("title", ""))
        abstract_text = normalized(paper.get("abstract", ""))
        author_text = normalized(paper.get("authors", ""))
        exact_in_title = contains_whole_phrase(title_text, phrase)
        exact_anywhere = any(contains_whole_phrase(field, phrase) for field in (title_text, author_text, abstract_text))
        if exact_in_title:
            score += 10.0
        elif exact_anywhere:
            score += 5.0
        for left, right in zip(query_terms, query_terms[1:]):
            bigram = f"{left} {right}"
            if any(contains_whole_phrase(field, bigram) for field in (title_text, author_text, abstract_text)):
                score += 1.6
        if score > 0:
            output.append({**paper, "score": round(score, 5)})
    return sorted(output, key=lambda item: (-item["score"], -item.get("year", 0), item.get("title", "").casefold()))


def load_papers(years: tuple[int, ...]) -> list[dict]:
    papers = []
    for year in years:
        path = ROOT / "data" / f"{year}.json"
        with path.open(encoding="utf-8") as stream:
            bundle = json.load(stream)
        if bundle.get("year") != year or not isinstance(bundle.get("papers"), list):
            raise ValueError(f"Invalid corpus file: {path}")
        papers.extend(bundle["papers"])
    return papers


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", help="Words or an exact phrase to find in titles, authors, and abstracts")
    parser.add_argument("--year", type=int, action="append", help="Limit to a year; repeat to select several")
    parser.add_argument("--years", help="Comma-separated year list, for example 2022,2024,2026")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--json", action="store_true", help="Write structured JSON to stdout")
    args = parser.parse_args()
    if args.limit < 1 or args.limit > 500:
        parser.error("--limit must be between 1 and 500")
    try:
        selected = list(args.year or [])
        if args.years:
            selected.extend(int(value) for value in args.years.split(",") if value.strip())
        years = tuple(sorted(set(selected or range(2022, 2027))))
        if any(year not in range(2022, 2027) for year in years):
            parser.error("years must be between 2022 and 2026")
        hits = rank_papers(load_papers(years), args.query)[:args.limit]
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"search_cvpr: {exc}", file=sys.stderr)
        return 1
    if args.json:
        json.dump(hits, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0
    if not hits:
        print("No matches.")
        return 0
    print(f"{'SCORE':>7}  {'YEAR':4}  TITLE — AUTHORS")
    print("─" * 110)
    for item in hits:
        title = textwrap.shorten(item["title"], width=68, placeholder="…")
        authors = textwrap.shorten(item["authors"], width=30, placeholder="…")
        print(f"{item['score']:7.3f}  {item['year']:4}  {title} — {authors}")
        print(f"         CVF: {item['cvf_url']}")
        print(f"         PDF: {item['pdf_url']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
