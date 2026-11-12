#!/usr/bin/env python3
"""Conference Hub research bridge: discovery, selected sources, cited NotebookLM Q&A.

All notebook contents and selection manifests stay local. Never use this to
claim novelty or complete-paper understanding from title/abstract matches.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, urlopen

CITO_SEARCH = "https://api.cito.fim.ai/search"
S2_SEARCH = "https://api.semanticscholar.org/graph/v1/paper/search"
SAFE_HOSTS = frozenset({
    "openaccess.thecvf.com", "eccv.ecva.net", "eccv2022.ecva.net",
    "eccv2024.ecva.net", "ecva.net", "www.ecva.net",
    "aclanthology.org", "www.aclanthology.org",
    "proceedings.neurips.cc", "proceedings.mlr.press",
    "openreview.net", "ojs.aaai.org", "aaai.org",
    "ieeexplore.ieee.org", "openaccess.thecvf.com",
    "roboticsproceedings.org", "www.roboticsproceedings.org",
    "dblp.org", "www.dblp.org",
})
PREPRINT_HOSTS = frozenset({"arxiv.org", "www.arxiv.org"})
SCHEMA = "cs-conference-research-sources-v1"
DEFAULT_PROFILE = "default"
USER_AGENT = "CSConferenceResearchHub/1.0 (research-only discovery)"
MAX_SOURCES = 100


class ResearchError(RuntimeError):
    """A user-actionable error, with no secret-bearing exception trace."""


def json_output(value):
    print(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True))


def official_url(value, allow_preprint=False):
    """Return a trusted HTTPS source URL, or empty string."""
    if not isinstance(value, str) or len(value) > 2048:
        return ""
    try:
        u = urlsplit(value)
    except ValueError:
        return ""
    if u.scheme != "https" or u.username or u.password or u.fragment:
        return ""
    if u.hostname not in SAFE_HOSTS and not (
        allow_preprint and u.hostname in PREPRINT_HOSTS
    ):
        return ""
    try:
        port = u.port
    except ValueError:
        return ""
    if port not in (None, 443):
        return ""
    if u.query and not (
        u.hostname == "openreview.net"
        and u.path in ("/forum", "/pdf")
        and re.fullmatch(r"id=[A-Za-z0-9_-]{6,80}", u.query)
    ):
        return ""
    return value


def fetch_json(url, headers=None, timeout=15):
    req = Request(url, headers={"User-Agent": USER_AGENT, **(headers or {})})
    try:
        with urlopen(req, timeout=timeout) as response:
            if response.geturl().split("/", 3)[:3] != url.split("/", 3)[:3]:
                raise ResearchError("Provider redirected to a different host; refused")
            raw = response.read(3_000_001)
            if len(raw) > 3_000_000:
                raise ResearchError("Provider response exceeded the size limit")
            return json.loads(raw)
    except HTTPError as exc:
        if exc.code == 429:
            raise ResearchError("Provider rate limit (HTTP 429); retry later") from None
        raise ResearchError("Provider failed with HTTP {}".format(exc.code)) from None
    except (URLError, TimeoutError) as exc:
        raise ResearchError("Provider unavailable: {}".format(type(exc).__name__)) from None
    except (ValueError, json.JSONDecodeError):
        raise ResearchError("Provider returned an invalid response") from None


def discover(query, provider="cito", mode="hybrid", limit=10):
    if not query or len(query) > 300:
        raise ResearchError("Query must contain 1–300 characters")
    if not (1 <= limit <= 30):
        raise ResearchError("Limit must be between 1 and 30")
    if provider == "cito":
        url = CITO_SEARCH + "?" + urlencode({"q": query, "mode": mode, "limit": limit})
        data = fetch_json(url)
        hits = data.get("hits", [])
        if not isinstance(hits, list):
            raise ResearchError("Unexpected Cito response schema")
        papers = [
            {
                "id": str(p.get("id", "")),
                "title": p.get("title") or "",
                "year": p.get("year"),
                "venue": p.get("venue") or "",
                "abstract": p.get("abstract") or "",
                "source_url": p.get("url") or "",
                "source_type": "index-metadata-only",
                "notebook_ready": False,
                "provider": "Cito",
            }
            for p in hits if isinstance(p, dict)
        ]
        return {
            "provider": "Cito (independent; Semantic Scholar-derived corpus)",
            "mode": mode,
            "query": query,
            "provenance": {
                "corpus_release": data.get("corpus_release"),
                "corpus_synced_at": data.get("corpus_synced_at"),
                "attribution": data.get("attribution"),
            },
            "papers": papers,
            "warning": "Discovery is not full-paper reading or verified peer-review status.",
        }
    if provider == "semantic-scholar":
        params = {"query": query, "limit": limit,
                  "fields": "title,year,venue,abstract,url,openAccessPdf,externalIds,authors"}
        headers = {}
        if os.getenv("S2_API_KEY"):
            headers["x-api-key"] = os.environ["S2_API_KEY"]
        data = fetch_json(S2_SEARCH + "?" + urlencode(params), headers)
        hits = data.get("data", [])
        if not isinstance(hits, list):
            raise ResearchError("Unexpected Semantic Scholar response schema")
        papers = []
        for p in hits:
            if not isinstance(p, dict):
                continue
            oa = p.get("openAccessPdf") or {}
            papers.append({
                "id": p.get("paperId", ""),
                "title": p.get("title") or "",
                "year": p.get("year"),
                "venue": p.get("venue") or "",
                "abstract": p.get("abstract") or "",
                "source_url": p.get("url") or "",
                "open_access_pdf_url": oa.get("url", "") if isinstance(oa, dict) else "",
                "external_ids": p.get("externalIds") or {},
                "source_type": "index-metadata-only",
                "notebook_ready": False,
                "provider": "Semantic Scholar (Allen Institute for AI)",
            })
        return {"provider": "Semantic Scholar (Allen Institute for AI)",
                "mode": "academic-graph", "query": query, "papers": papers,
                "warning": "Metadata search does not establish venue track or paper findings."}
    raise ResearchError("Unknown discovery provider")


def make_manifest(pins_path, topic, allow_preprint=False):
    try:
        data = json.loads(Path(pins_path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ResearchError("Cannot read pin export: {}".format(type(exc).__name__)) from None
    if isinstance(data, dict) and data.get("schema") not in (None, "cs-conference-hub-pins-v1"):
        raise ResearchError("Unsupported pin export schema")
    records = data if isinstance(data, list) else data.get("pins", [])
    if not isinstance(records, list):
        raise ResearchError("Pins must be a JSON array")
    sources, skipped, seen = [], [], set()
    for row in records[:MAX_SOURCES]:
        if not isinstance(row, dict) or not row.get("title"):
            continue
        candidates = (row.get("pdf_url"), row.get("paper_url"), row.get("cvf_url"))
        accepted = next((x for x in candidates if official_url(x, allow_preprint)), "")
        paper_id = str(row.get("id", "")).strip()
        if not accepted:
            skipped.append({"id": paper_id, "reason": "No trusted publisher URL"})
            continue
        if accepted in seen:
            continue
        seen.add(accepted)
        sources.append({
            "id": paper_id,
            "title": str(row["title"])[:500],
            "venue": row.get("venue") or "CVPR",
            "year": row.get("year"),
            "url": accepted,
            "source_kind": "preprint" if urlsplit(accepted).hostname in PREPRINT_HOSTS else "publisher-host",
            "peer_review_verified": False,
            "status": "SELECTED_NOT_INGESTED",
            "provenance": row.get("source") or "CS Conference Hub pin export",
        })
    return {
        "schema": SCHEMA, "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "topic": topic[:160], "sources": sources, "skipped": skipped,
        "preprints_explicitly_selected": bool(allow_preprint),
        "privacy": "Local selected-paper manifest. No papers were uploaded.",
        "warning": "Trusted URL is not confirmation of main-track acceptance or claimed results.",
    }


def read_manifest(path):
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        raise ResearchError("Cannot read selected-paper manifest") from None
    if not isinstance(data, dict) or data.get("schema") != SCHEMA:
        raise ResearchError("Invalid selected-paper manifest schema")
    sources = data.get("sources")
    if not isinstance(sources, list) or len(sources) > MAX_SOURCES:
        raise ResearchError("Invalid manifest source list")
    return data


def notebook_command(args, profile, timeout=90):
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,50}", profile):
        raise ResearchError("Invalid NotebookLM profile name")
    cli = os.getenv("NOTEBOOKLM_BIN") or shutil.which("notebooklm") or "/Users/nilan/.local/bin/notebooklm"
    if not Path(cli).exists():
        raise ResearchError("NotebookLM CLI not installed")
    try:
        result = subprocess.run([cli, "-p", profile] + args,
                                text=True, capture_output=True, timeout=timeout, check=False)
    except subprocess.TimeoutExpired:
        raise ResearchError("NotebookLM timed out") from None
    if result.returncode:
        raise ResearchError("NotebookLM command failed; check CLI authentication and notebook ID")
    try:
        return json.loads(result.stdout)
    except (ValueError, TypeError):
        return {"output": result.stdout.strip()[:10000]}


def notebook_ready(profile):
    try:
        data = notebook_command(["auth", "check", "--test", "--passive", "--json"], profile, 25)
        status = str(data.get("status", "unknown"))
        ready = status.lower() in ("ok", "success", "authenticated", "valid", "healthy")
        ready = ready or data.get("authenticated") is True or data.get("ok") is True
        return {"ready": ready, "status": status}
    except ResearchError:
        return {"ready": False, "status": "NOT_AUTHENTICATED_OR_UNAVAILABLE"}


def notebook_source_rows(observed):
    """Recognize explicit source collections; unknown schemas never imply readiness."""
    if isinstance(observed, list):
        return observed
    if isinstance(observed, dict):
        for key in ("sources", "items", "data"):
            if isinstance(observed.get(key), list):
                return observed[key]
    return []


def require_notebook_auth(profile):
    if not notebook_ready(profile)["ready"]:
        raise ResearchError("NotebookLM is not authenticated. On Mac run: notebooklm -p {} login".format(profile))


def notebook_use(notebook_id, profile):
    if not re.fullmatch(r"[A-Za-z0-9_-]{6,150}", notebook_id):
        raise ResearchError("Invalid notebook ID")
    notebook_command(["use", notebook_id], profile, 30)


def cli_main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest="action", required=True)
    search = subs.add_parser("search", help="Live scholarly discovery, metadata only")
    search.add_argument("query")
    search.add_argument("--provider", choices=("cito", "semantic-scholar"), default="cito")
    search.add_argument("--mode", choices=("hybrid", "semantic", "keyword"), default="hybrid")
    search.add_argument("--limit", type=int, default=10)
    pins = subs.add_parser("select", help="Prepare a private NotebookLM source manifest from hub pins")
    pins.add_argument("pins_json")
    pins.add_argument("--topic", required=True)
    pins.add_argument("--output", required=True)
    pins.add_argument("--allow-preprint", action="store_true")
    status = subs.add_parser("notebook-status", help="Check authentication without copying credentials")
    status.add_argument("--profile", default=DEFAULT_PROFILE)
    create = subs.add_parser("notebook-create", help="Create a topic-specific private notebook")
    create.add_argument("title")
    create.add_argument("--profile", default=DEFAULT_PROFILE)
    add = subs.add_parser("notebook-add", help="Upload only the user-selected manifest URLs")
    add.add_argument("manifest")
    add.add_argument("--notebook-id", required=True)
    add.add_argument("--profile", default=DEFAULT_PROFILE)
    add.add_argument("--confirm-upload", action="store_true")
    add.add_argument("--allow-preprint", action="store_true")
    ask = subs.add_parser("ask", help="Ask NotebookLM only after verifying source presence")
    ask.add_argument("question")
    ask.add_argument("--notebook-id", required=True)
    ask.add_argument("--profile", default=DEFAULT_PROFILE)
    opts = parser.parse_args(argv)
    try:
        if opts.action == "search":
            json_output(discover(opts.query, opts.provider, opts.mode, opts.limit))
        elif opts.action == "select":
            if not opts.topic.strip() or len(opts.topic) > 160:
                raise ResearchError("Topic must contain 1–160 characters")
            manifest = make_manifest(opts.pins_json, opts.topic, opts.allow_preprint)
            target = Path(opts.output).expanduser().resolve()
            repo_root = Path(__file__).resolve().parents[3]
            if target == repo_root or repo_root in target.parents:
                raise ResearchError("Private manifests must be saved outside the website repository")
            if target.exists():
                raise ResearchError("Output already exists; refusing to overwrite")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            json_output({"saved_to": str(target), "selected": len(manifest["sources"]),
                         "skipped": len(manifest["skipped"]), "uploaded": False})
        elif opts.action == "notebook-status":
            json_output({"profile": opts.profile, **notebook_ready(opts.profile)})
        elif opts.action == "notebook-create":
            require_notebook_auth(opts.profile)
            if not 1 <= len(opts.title.strip()) <= 140:
                raise ResearchError("Notebook title must contain 1–140 characters")
            json_output(notebook_command(["create", opts.title, "--json"], opts.profile))
        elif opts.action == "notebook-add":
            if not opts.confirm_upload:
                raise ResearchError("Upload requires --confirm-upload. Nothing was uploaded.")
            manifest = read_manifest(opts.manifest)
            sources = manifest["sources"]
            if not sources:
                raise ResearchError("No selected official sources in manifest")
            for s in sources:
                if not isinstance(s, dict) or official_url(
                        s.get("url"), bool(opts.allow_preprint and manifest.get("preprints_explicitly_selected"))
                ) != s.get("url"):
                    raise ResearchError("Manifest contains a URL not on the trusted publisher list")
            require_notebook_auth(opts.profile)
            notebook_use(opts.notebook_id, opts.profile)
            saved = []
            for source in sources:
                outcome = notebook_command(["source", "add", source["url"], "--json"], opts.profile, 120)
                saved.append({"title": source["title"], "url": source["url"],
                              "add_response": outcome, "status": "ADDED_PROCESSING_NOT_VERIFIED"})
            observed = notebook_command(["source", "list", "--json"], opts.profile, 90)
            json_output({"added": saved, "notebook_sources": observed,
                         "warning": "Source listing does not prove processing finished or citation accuracy."})
        elif opts.action == "ask":
            if not opts.question.strip() or len(opts.question) > 2000:
                raise ResearchError("Question must contain 1–2000 characters")
            require_notebook_auth(opts.profile)
            notebook_use(opts.notebook_id, opts.profile)
            observed = notebook_command(["source", "list", "--json"], opts.profile)
            sources = notebook_source_rows(observed)
            if not sources:
                raise ResearchError("Notebook has no sources; refusing ungrounded answer")
            response = notebook_command(["ask", opts.question, "--json"], opts.profile, 180)
            json_output({"engine": "NotebookLM unofficial CLI", "question": opts.question,
                         "response": response, "citation_warning":
                         "Use NotebookLM citation source IDs to verify exact passages; any proposed research gap remains a hypothesis."})
        return 0
    except ResearchError as exc:
        json_output({"error": str(exc), "status": "BLOCKED_OR_INVALID"})
        return 2


if __name__ == "__main__":
    sys.exit(cli_main())
