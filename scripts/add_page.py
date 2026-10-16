#!/usr/bin/env python3
"""Add one explicitly approved, self-contained HTML page to the library."""

import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "shared" / "site"
if not SITE.is_dir():
    SITE = ROOT
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PRIVATE_TEXT = re.compile(
    r"/Users/|/home/|/private/|tskey-[A-Za-z0-9_-]{10,}|"
    r"github_pat_[A-Za-z0-9_]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|"
    r"AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----|"
    r"(?:[A-Za-z0-9-]+\.)+tail[a-z0-9.-]*\.net",
    re.IGNORECASE,
)


class PageAudit(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.has_html = False
        self.has_head = False
        self.title_text = []
        self.in_title = False
        self.references = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "html":
            self.has_html = True
        elif tag == "head":
            self.has_head = True
        elif tag == "title":
            self.in_title = True
        for attr in ("href", "src", "poster"):
            if attrs.get(attr):
                self.references.append((tag, attr, attrs[attr], attrs.get("rel", "").casefold().split()))

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title_text.append(data)


def project_slug(project):
    return re.sub(r"[^a-z0-9]+", "-", project.casefold()).strip("-")


def add_noindex(document):
    robots = re.compile(r"<meta\b(?=[^>]*\bname\s*=\s*(['\"])robots\1)[^>]*>", re.I)
    match = robots.search(document)
    if match:
        tag = match.group(0)
        content = re.search(r"\bcontent\s*=\s*(['\"])(.*?)\1", tag, re.I)
        if content and "noindex" in content.group(2).casefold().split(","):
            return document
        if content:
            tag = tag[:content.start(2)] + "noindex,nofollow,noarchive" + tag[content.end(2):]
        else:
            tag = tag[:-1] + ' content="noindex,nofollow,noarchive">'
        return document[:match.start()] + tag + document[match.end():]
    head = re.search(r"<head\b[^>]*>", document, re.I)
    if not head:
        raise ValueError("HTML must contain a <head> element")
    return document[:head.end()] + '\n<meta name="robots" content="noindex,nofollow,noarchive">' + document[head.end():]


def validate_links(document, destination):
    audit = PageAudit()
    audit.feed(document)
    if not audit.has_html or not audit.has_head or not "".join(audit.title_text).strip():
        raise ValueError("HTML must contain <html>, <head>, and a non-empty <title>")
    for tag, attr, reference, _rel in audit.references:
        parts = urlsplit(reference)
        if parts.scheme or parts.netloc:
            if tag not in {"a", "area"}:
                raise ValueError(f"Remote assets are not allowed: {reference}")
            continue
        if not parts.path:
            continue
        linked = (destination.parent / unquote(parts.path)).resolve()
        try:
            linked.relative_to(SITE.resolve())
        except ValueError as exc:
            raise ValueError(f"Local link escapes the site: {reference}") from exc
        if linked.is_dir():
            linked = linked / "index.html"
        if not linked.is_file():
            raise ValueError(f"Local link does not exist in the site: {reference}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="one approved HTML file")
    parser.add_argument("--id", required=True, help="unique lowercase hyphenated entry ID")
    parser.add_argument("--title", required=True)
    parser.add_argument("--description", required=True)
    parser.add_argument("--project", required=True)
    parser.add_argument("--category", help="topic group; defaults to the project name")
    parser.add_argument("--tags", required=True, nargs="+", help="one or more search tags")
    args = parser.parse_args()

    try:
        if not SLUG.fullmatch(args.id):
            raise ValueError("--id must use lowercase letters, digits, and single hyphens")
        fields = [args.title, args.description, args.project, *(args.tags or [])]
        if any(not value.strip() or any(ord(char) < 32 for char in value) for value in fields):
            raise ValueError("title, description, project, and tags must be non-empty plain text")
        if PRIVATE_TEXT.search(" ".join(fields)):
            raise ValueError("metadata contains a private-path or secret-like string")
        project = project_slug(args.project)
        if not project:
            raise ValueError("--project must contain letters or digits")
        category = (args.category or args.project).strip()
        if not category or PRIVATE_TEXT.search(category):
            raise ValueError("--category must be non-empty public text")
        source = args.source.expanduser().resolve(strict=True)
        if source.suffix.casefold() != ".html" or not source.is_file():
            raise ValueError("source must be one existing .html file")
        document = source.read_text(encoding="utf-8")
        if PRIVATE_TEXT.search(document):
            raise ValueError("HTML contains a private-path or secret-like string")

        destination = SITE / "explainers" / project / f"{args.id}.html"
        catalog_path = SITE / "library.json"
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        if any(entry.get("id") == args.id for entry in catalog):
            raise ValueError(f"entry ID already exists: {args.id}")
        if destination.exists():
            raise ValueError(f"destination already exists: {destination.relative_to(SITE)}")

        document = add_noindex(document)
        validate_links(document, destination)
        entry = {
            "id": args.id,
            "title": args.title.strip(),
            "description": args.description.strip(),
            "project": args.project.strip(),
            "category": category,
            "tags": [tag.strip() for tag in args.tags],
            "url": "./" + destination.relative_to(SITE).as_posix(),
        }

        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("x", encoding="utf-8") as output:
            output.write(document)
        try:
            catalog.append(entry)
            catalog_path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        except Exception:
            destination.unlink(missing_ok=True)
            raise
        print(f"Added {entry['id']} -> {entry['url']}")
        print(f"Review {catalog_path.relative_to(ROOT)} and run: python3 scripts/test_library.py")
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        print(f"add_page: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
