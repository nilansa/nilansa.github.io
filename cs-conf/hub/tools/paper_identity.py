#!/usr/bin/env python3
"""Stable paper IDs and conservative cross-source deduplication keys.

Never merge different venue/year records merely because their titles look alike.
Prefer publisher identifiers and preserve source record IDs separately.
"""
from __future__ import annotations

import hashlib
import re
import unicodedata
from urllib.parse import unquote, urlsplit

_DOI = re.compile(r"^10\.\d{4,9}/\S+$", re.IGNORECASE)
_OPENREVIEW = re.compile(r"^[A-Za-z0-9_-]{6,80}$")
_ANTHOLOGY = re.compile(r"^\d{4}\.[A-Za-z0-9_-]+\.\d+$")


def normalize_title(value: str) -> str:
    value = unicodedata.normalize("NFKC", str(value or "")).casefold()
    return " ".join(re.findall(r"[^\W_]+", value, flags=re.UNICODE))


def canonical_doi(value: str) -> str:
    value = str(value or "").strip()
    if not value:
        return ""
    if value.lower().startswith("doi:"):
        value = value[4:]
    if value.lower().startswith("https://doi.org/"):
        value = urlsplit(value).path.lstrip("/")
    value = unquote(value).strip().lower().rstrip(".,")
    return value if _DOI.fullmatch(value) else ""


def paper_key(paper: dict) -> str:
    """Return a source-agnostic key only when a trustworthy identifier exists."""
    doi = canonical_doi(paper.get("doi") or paper.get("DOI") or "")
    if not doi:
        landing = paper.get("paper_url") or paper.get("url") or ""
        if isinstance(landing, str) and landing.startswith("https://doi.org/"):
            doi = canonical_doi(landing)
    if doi:
        return "doi:" + doi

    review_id = str(paper.get("openreview_id") or "").strip()
    if not review_id:
        landing = str(paper.get("paper_url") or "")
        try:
            url = urlsplit(landing)
            if url.scheme == "https" and url.hostname == "openreview.net" and url.path in ("/forum", "/pdf"):
                from urllib.parse import parse_qs
                values = parse_qs(url.query).get("id", [])
                review_id = values[0] if len(values) == 1 else ""
        except ValueError:
            pass
    if _OPENREVIEW.fullmatch(review_id):
        return "openreview:" + review_id

    anthology_id = str(paper.get("anthology_id") or "").strip()
    if not anthology_id:
        try:
            url = urlsplit(str(paper.get("paper_url") or ""))
            if url.scheme == "https" and url.hostname == "aclanthology.org":
                anthology_id = url.path.strip("/").removesuffix(".pdf")
        except ValueError:
            pass
    if _ANTHOLOGY.fullmatch(anthology_id):
        return "anthology:" + anthology_id.lower()

    venue = re.sub(r"\s+", " ", str(paper.get("venue") or "").strip()).casefold()
    year = str(paper.get("year") or "").strip()
    title = normalize_title(paper.get("title") or "")
    if not (venue and year.isdigit() and title):
        raise ValueError("Cannot identify a paper without a title, venue and year")
    return "venue-title-year:" + hashlib.sha256((venue + "\n" + year + "\n" + title).encode("utf-8")).hexdigest()


def stable_uid(paper: dict) -> str:
    return "paper:" + hashlib.sha256(paper_key(paper).encode("utf-8")).hexdigest()[:24]
