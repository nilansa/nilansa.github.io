#!/usr/bin/env python3
"""Build the static CVPR abstract corpus from the Hugging Face JSONL files."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
DATASET = "https://huggingface.co/datasets/choucsan/CVPR_Papers"
YEARS = tuple(range(2022, 2027))
TOKEN_RE = re.compile(r"[\w+#.-]+", re.UNICODE)
LINK_CHECK_DATE = "2026-11-02"
KNOWN_CVF_404 = {
    (2022, "Accelerating Neural Network Optimization Through an Automated Control Theory Lens"),
    (2022, "E2V-SDE: From Asynchronous Events to Fast and Continuous Video Reconstruction via Neural Stochastic Differential Equations"),
    (2022, "A Graph Matching Perspective With Transformers on Video Instance Segmentation"),
    (2024, "SportsSloMo: A New Benchmark and Baselines for Human-centric Video Frame Interpolation"),
    (2024, "GenHowTo: Learning to Generate Actions and State Transformations from Instructional Videos"),
    (2024, "DePT: Decoupled Prompt Tuning"),
}


class BuildError(ValueError):
    pass


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def is_safe_pdf_url(value: str) -> bool:
    try:
        parsed = urllib.parse.urlsplit(value.strip())
        return (
            parsed.scheme == "https"
            and parsed.hostname in {"openaccess.thecvf.com", "www.openaccess.thecvf.com"}
            and parsed.username is None
            and parsed.password is None
            and parsed.port in (None, 443)
            and parsed.path.lower().endswith(".pdf")
            and not parsed.query
            and not parsed.fragment
        )
    except (ValueError, AttributeError):
        return False


def is_safe_cvf_page_url(value: str) -> bool:
    try:
        parsed = urllib.parse.urlsplit(value.strip())
        paper_page = (
            parsed.scheme == "https"
            and parsed.hostname in {"openaccess.thecvf.com", "www.openaccess.thecvf.com"}
            and parsed.username is None
            and parsed.password is None
            and parsed.port in (None, 443)
            and parsed.path.lower().endswith(".html")
            and not parsed.query
            and not parsed.fragment
        )
        year_listing = (
            parsed.scheme == "https"
            and parsed.hostname in {"openaccess.thecvf.com", "www.openaccess.thecvf.com"}
            and parsed.username is None
            and parsed.password is None
            and parsed.port in (None, 443)
            and re.fullmatch(r"/CVPR20\d{2}", parsed.path, re.I)
            and parsed.query == "day=all"
            and not parsed.fragment
        )
        return bool(paper_page or year_listing)
    except (ValueError, AttributeError):
        return False


def _title_key(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).casefold()
    return " ".join(re.findall(r"\w+", value, re.UNICODE))


class CVFIndexParser(HTMLParser):
    """Read paper titles and original links from one CVF year listing."""

    def __init__(self, base_url: str):
        super().__init__(convert_charrefs=True)
        self.base_url = base_url
        self.entries: list[dict] = []
        self.current: dict | None = None
        self.in_title = False
        self.in_anchor = False
        self.anchor_href = ""
        self.anchor_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "dt" and "ptitle" in (values.get("class") or "").split():
            self._finish()
            self.current = {"title": "", "page_url": "", "pdf_url": ""}
            self.in_title = True
        elif tag == "a":
            self.in_anchor = True
            self.anchor_href = values.get("href") or ""
            self.anchor_text = []
            if self.in_title and self.current and self.anchor_href:
                self.current["page_url"] = urllib.parse.urljoin(self.base_url, self.anchor_href)

    def handle_data(self, data: str) -> None:
        if self.in_title and self.current:
            self.current["title"] += data
        if self.in_anchor:
            self.anchor_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self.in_anchor:
            label = " ".join("".join(self.anchor_text).split()).casefold()
            if self.current and not self.current["pdf_url"] and self.anchor_href.casefold().endswith(".pdf") and label == "pdf":
                self.current["pdf_url"] = urllib.parse.urljoin(self.base_url, self.anchor_href)
            self.in_anchor = False
        elif tag == "dt" and self.in_title:
            self.in_title = False

    def _finish(self) -> None:
        if self.current and self.current["title"].strip():
            self.entries.append({**self.current, "title": " ".join(self.current["title"].split())})
        self.current = None

    def close(self) -> None:
        super().close()
        self._finish()


def _fetch_cvf_index(year: int) -> tuple[bytes, dict[str, dict]]:
    url = f"https://openaccess.thecvf.com/CVPR{year}?day=all"
    request = urllib.request.Request(url, headers={"User-Agent": "CVPR-Research-Hub/1.0 proceedings-link-reconciliation"})
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            if response.status != 200:
                raise BuildError(f"HTTP {response.status} fetching CVF listing {url}")
            raw = response.read()
    except (urllib.error.URLError, TimeoutError) as exc:
        raise BuildError(f"Could not fetch CVF listing {url}: {exc}") from exc
    parser = CVFIndexParser(url)
    parser.feed(raw.decode("utf-8", "replace"))
    parser.close()
    index: dict[str, dict] = {}
    for entry in parser.entries:
        index.setdefault(_title_key(entry["title"]), entry)
    if not index:
        raise BuildError(f"CVF listing had no paper entries: {url}")
    return raw, index


def _track(year: int, source_url: str, bibtex: str, filename: str, cvf_confirmed: bool = False) -> tuple[str, str, str]:
    combined = f"{source_url} {bibtex} {filename}".casefold()
    booktitle = ""
    match = re.search(r"booktitle\s*=\s*[\{\"]([^}\"]+)", bibtex, re.I)
    if match:
        booktitle = match.group(1).casefold()
    if "workshop" in booktitle or f"cvpr{year}w" in combined or f"cvprw_{year}" in combined:
        return "CVPR workshop (source-confirmed)", "CVF URL or BibTeX", "workshop"
    if "computer vision and pattern recognition" in booktitle and "workshop" not in booktitle:
        return "CVPR main (BibTeX-confirmed)", "BibTeX booktitle", "main"
    if cvf_confirmed:
        return "CVPR main (CVF listing-confirmed)", "CVF proceedings listing", "main"
    path = urllib.parse.urlsplit(source_url).path.casefold()
    if re.search(rf"/content/cvpr{year}/", path) or re.search(rf"/content_cvpr_{year}/", path):
        return "CVPR main (CVF-link-confirmed)", "CVF PDF URL", "main"
    return "CVPR main candidate", "Dataset labels the source CVPR; track not confirmed", "candidate"


def _cluster(text: str) -> str:
    text = text.casefold()
    rules = (
        ("3D & geometry", ("3d", "point cloud", "depth", "mesh", "gaussian splatting", "pose estimation", "neural radiance", "lidar", "reconstruction")),
        ("Vision & language", ("vision-language", "vision language", "visual question", "multimodal", "image-text", "text-image", "vlm", "language-guided")),
        ("Generative models", ("diffusion", "generative", "image synthesis", "video synthesis", "image generation", "text-to-image", "gan")),
        ("Video & motion", ("video", "temporal", "action recognition", "motion", "tracking", "event camera")),
        ("Medical imaging", ("medical", "clinical", "radiology", "pathology", "lesion", "mri", "ct scan")),
        ("Robotics & embodied", ("robot", "embodied", "manipulation", "autonomous driving", "navigation")),
        ("Recognition & detection", ("segmentation", "detection", "recognition", "classification", "object tracking", "face recognition")),
        ("Learning & robustness", ("self-supervised", "few-shot", "semi-supervised", "unlearning", "robustness", "domain adaptation", "data-efficient")),
    )
    return next((name for name, terms in rules if any(term in text for term in terms)), "Other vision")


def _edition(year: int, filename: str, bibtex: str) -> str:
    if "workshop" in bibtex.casefold() or "_cvprw_" in filename.casefold() or "cvprw" in filename.casefold():
        return f"CVPR{year}W"
    return f"CVPR{year}"


def _cvf_urls(year: int, title: str, source_url: str, pdf_path: str, bibtex: str, cvf_entry: dict | None = None) -> tuple[str, str, bool, str, str]:
    source_safe = is_safe_pdf_url(source_url)
    parsed = urllib.parse.urlsplit(source_url) if source_safe else None
    raw_name = Path((parsed.path if parsed else pdf_path).replace("\\", "/")).name
    if not raw_name.lower().endswith(".pdf") or raw_name in {".pdf", "..pdf"}:
        raise BuildError(f"Cannot derive a CVF PDF name from {source_url!r} or {pdf_path!r}")
    edition = _edition(year, raw_name, bibtex)
    pdf_url = source_url if source_safe else f"https://openaccess.thecvf.com/content/{edition}/papers/{urllib.parse.quote(raw_name)}"
    page_name = raw_name[:-4] + ".html"
    page_url = f"https://openaccess.thecvf.com/content/{edition}/html/{urllib.parse.quote(page_name)}"
    page_type = "paper page"
    pdf_status = "CVF-listed; HTTP status not individually checked"
    if cvf_entry:
        if is_safe_pdf_url(cvf_entry.get("pdf_url", "")):
            pdf_url = cvf_entry["pdf_url"]
        if is_safe_cvf_page_url(cvf_entry.get("page_url", "")):
            page_url = cvf_entry["page_url"]
    if (year, title) in KNOWN_CVF_404:
        page_url = f"https://openaccess.thecvf.com/CVPR{year}?day=all"
        page_type = "year proceedings listing"
        pdf_status = f"HTTP 404 by HEAD on {LINK_CHECK_DATE}"
    if not is_safe_pdf_url(pdf_url):
        raise BuildError(f"Unsafe or invalid CVF PDF URL: {pdf_url!r}")
    if not is_safe_cvf_page_url(page_url):
        raise BuildError(f"Unsafe or invalid CVF paper URL: {page_url!r}")
    if not is_safe_cvf_page_url(page_url):
        raise BuildError(f"Unsafe or invalid CVF paper/listing URL: {page_url!r}")
    return pdf_url, page_url, (not source_safe or pdf_url != source_url), page_type, pdf_status


def _parse_year(year: int, raw: bytes, cvf_index: dict[str, dict]) -> tuple[list[dict], dict]:
    rows: list[dict] = []
    seen: set[tuple[str, str]] = set()
    empty_abstracts = invalid_links = repaired_links = duplicate_count = year_mismatches = 0
    empty_abstract_titles: list[str] = []
    cvf_listing_matched = source_links_replaced = dead_pdf_links = 0
    track_counts: Counter[str] = Counter()
    for line_number, line in enumerate(raw.splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise BuildError(f"{year} line {line_number}: invalid JSON: {exc}") from exc
        if not isinstance(row, dict):
            raise BuildError(f"{year} line {line_number}: record is not an object")
        title = str(row.get("title") or "").strip()
        authors = str(row.get("authors") or "").strip()
        abstract = str(row.get("abstract") or "").strip()
        pdf_path = str(row.get("pdf_path") or "").strip()
        original_url = str(row.get("download_url") or "").strip()
        bibtex = str(row.get("bibtex") or "")
        if not title or not authors:
            raise BuildError(f"{year} line {line_number}: missing title or authors")
        if not abstract:
            empty_abstracts += 1
            empty_abstract_titles.append(title)
        path_year = re.match(r"^(\d{4})/", pdf_path.replace("\\", "/"))
        if path_year and int(path_year.group(1)) != year:
            year_mismatches += 1
            raise BuildError(f"{year} line {line_number}: pdf_path belongs to {path_year.group(1)}")
        if not path_year:
            year_mismatches += 1
            raise BuildError(f"{year} line {line_number}: pdf_path has no year prefix")
        key = (title.casefold(), authors.casefold())
        if key in seen:
            duplicate_count += 1
            raise BuildError(f"{year} line {line_number}: duplicate title/author pair {title!r}")
        seen.add(key)
        cvf_entry = cvf_index.get(_title_key(title))
        cvf_listing_matched += cvf_entry is not None
        if not is_safe_pdf_url(original_url):
            invalid_links += 1
        pdf_url, cvf_url, repaired, cvf_reference_type, pdf_status = _cvf_urls(year, title, original_url, pdf_path, bibtex, cvf_entry)
        repaired_links += repaired
        source_links_replaced += pdf_url != original_url
        dead_pdf_links += pdf_status.startswith("HTTP 404")
        status, basis, track = _track(year, original_url if is_safe_pdf_url(original_url) else pdf_url, bibtex, Path(pdf_url).name, cvf_entry is not None)
        track_counts[track] += 1
        stable_id = hashlib.sha256(f"{year}\0{title}\0{authors}".encode("utf-8")).hexdigest()[:16]
        rows.append({
            "id": stable_id,
            "title": title,
            "authors": authors,
            "abstract": abstract,
            "abstract_status": "available" if abstract else "missing in source metadata",
            "pdf_url": pdf_url,
            "pdf_status": pdf_status,
            "cvf_url": cvf_url,
            "cvf_reference_type": cvf_reference_type,
            "year": year,
            "source": "Hugging Face dataset",
            "cluster": _cluster(f"{title} {abstract}"),
            "track_status": status,
            "track_basis": basis,
        })
    rows.sort(key=lambda paper: (paper["title"].casefold(), paper["id"]))
    stats = {
        "count": len(rows),
        "empty_abstracts": empty_abstracts,
        "empty_abstract_titles": empty_abstract_titles,
        "invalid_input_urls": invalid_links,
        "repaired_pdf_links": repaired_links,
        "duplicates": duplicate_count,
        "year_mismatches": year_mismatches,
        "cvf_listing_matched": cvf_listing_matched,
        "cvf_listing_unmatched": len(rows) - cvf_listing_matched,
        "source_links_replaced": source_links_replaced,
        "checked_404_pdf_links": dead_pdf_links,
        "track_counts": dict(sorted(track_counts.items())),
    }
    return rows, stats


def _fetch(year: int) -> bytes:
    url = f"{DATASET}/resolve/main/{year}/meta.jsonl"
    request = urllib.request.Request(url, headers={"User-Agent": "CVPR-Research-Hub/1.0 metadata-ingester"})
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            if response.status != 200:
                raise BuildError(f"HTTP {response.status} fetching {url}")
            return response.read()
    except (urllib.error.URLError, TimeoutError) as exc:
        raise BuildError(f"Could not fetch {url}: {exc}") from exc


def build(years: tuple[int, ...], data_dir: Path, provenance_path: Path) -> dict:
    per_year: dict[str, dict] = {}
    unavailable_pdf_links: list[dict] = []
    for year in years:
        source = _fetch(year)
        cvf_listing, cvf_index = _fetch_cvf_index(year)
        papers, stats = _parse_year(year, source, cvf_index)
        if stats["count"] == 0:
            raise BuildError(f"{year}: source returned no papers")
        unavailable_pdf_links.extend(
            {"year": paper["year"], "title": paper["title"], "url": paper["pdf_url"], "status": paper["pdf_status"]}
            for paper in papers if paper["pdf_status"].startswith("HTTP 404")
        )
        output = json.dumps({"year": year, "source": "Hugging Face dataset", "papers": papers}, ensure_ascii=False, separators=(",", ":")).encode("utf-8") + b"\n"
        output_path = data_dir / f"{year}.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(output)
        per_year[str(year)] = {
            **stats,
            "source_url": f"{DATASET}/resolve/main/{year}/meta.jsonl",
            "source_bytes": len(source),
            "source_sha256": sha256_bytes(source),
            "cvf_listing_url": f"https://openaccess.thecvf.com/CVPR{year}?day=all",
            "cvf_listing_bytes": len(cvf_listing),
            "cvf_listing_sha256": sha256_bytes(cvf_listing),
            "output_file": output_path.name,
            "output_bytes": len(output),
            "output_sha256": sha256_bytes(output),
        }
        print(f"{year}: {stats['count']} papers; {stats['cvf_listing_matched']} CVF matches; {stats['source_links_replaced']} links replaced; {len(output)} bytes; sha256 {sha256_bytes(output)}")
    total = sum(item["count"] for item in per_year.values())
    provenance = {
        "schema": "cvpr-hypothesis-hub-provenance-v1",
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "total_papers": total,
        "years": per_year,
        "sources": [
            {
                "name": "CVPR_Papers dataset",
                "url": DATASET,
                "metadata_url_pattern": f"{DATASET}/resolve/main/{{year}}/meta.jsonl",
                "license": "MIT (dataset card)",
                "attribution": "Dataset maintained by Zhishan Zou; metadata is sourced from CVF Open Access.",
            },
            {
                "name": "Computer Vision Foundation Open Access",
                "url": "https://openaccess.thecvf.com/",
                "listing_url_pattern": "https://openaccess.thecvf.com/CVPR{year}?day=all",
                "role": "Official proceedings listings reconcile paper titles to original paper and PDF links. Paper rights remain with authors or other rights holders.",
            },
        ],
        "limitations": [
            "This site stores paper metadata and abstracts only. It does not download or host PDFs.",
            "Some source records have no abstract. They remain searchable by title and authors, are marked in the interface, and cannot be selected as Idea Lab evidence.",
            "Six CVF PDF endpoints returned HTTP 404 to a HEAD request on 2026-11-02. Their records point to the official year proceedings listing, and the unavailable PDF links are marked instead of shown as active downloads.",
            "A CVPR source label alone does not prove main-track acceptance. Track labels are upgraded only when a CVF URL or BibTeX field identifies the track; otherwise the item remains a CVPR main candidate.",
            "Historical accepted papers are examples, not a guarantee of future acceptance.",
            "Topic clusters are simple keyword labels for discovery. They are not official CVPR categories.",
        ],
        "url_validation": "All input and output PDF links are checked for HTTPS, the CVF host, a .pdf path, and absence of credentials, query strings, and fragments. CVF listing links are matched by normalized title. Only the six known unavailable links were checked with HTTP HEAD; no PDF body was fetched.",
        "link_checks": {"checked_on": LINK_CHECK_DATE, "method": "HTTP HEAD request; no PDF body fetched", "unavailable_count": len(unavailable_pdf_links), "unavailable": unavailable_pdf_links},
        "cvf_reference_method": "Where a title matches, paper-page and PDF URLs come from the official CVF proceedings listing. Unmatched titles use a safe source link or a filename-derived CVF URL. Listing match counts and source hashes are recorded per year.",
    }
    provenance_path.parent.mkdir(parents=True, exist_ok=True)
    provenance_path.write_text(json.dumps(provenance, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return provenance


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--years", default=",".join(map(str, YEARS)), help="Comma-separated years (default: 2022-2026)")
    parser.add_argument("--data-dir", type=Path, default=ROOT / "data")
    parser.add_argument("--provenance", type=Path, default=ROOT / "provenance.json")
    args = parser.parse_args()
    try:
        years = tuple(int(value) for value in args.years.split(",") if value.strip())
        if not years or len(set(years)) != len(years) or any(year not in YEARS for year in years):
            raise BuildError(f"Years must be unique values from {YEARS}; got {years}")
        result = build(years, args.data_dir, args.provenance)
        print(f"Validated and wrote {result['total_papers']} records across {len(result['years'])} years.")
        return 0
    except (BuildError, OSError) as exc:
        print(f"build_cvpr_hub: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
