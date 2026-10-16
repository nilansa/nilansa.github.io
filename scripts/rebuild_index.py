#!/usr/bin/env python3
"""Regenerate the simple dated HTML index from explainer/library.json."""
import argparse
import html
import json
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / 'explainer/library.json'
INDEX = ROOT / 'explainer/index.html'


def sort_key(entry):
    day = date.fromisoformat(entry['date'])
    created = datetime.fromisoformat(entry['indexed_at'].replace('Z', '+00:00'))
    if created.tzinfo is None:
        raise ValueError('indexed_at needs a timezone')
    return day, created.astimezone(timezone.utc)


def build(entries):
    if len({entry['id'] for entry in entries}) != len(entries):
        raise ValueError('duplicate page IDs')
    entries = sorted(entries, key=sort_key, reverse=True)
    lines = [
        '<!doctype html>', '<html lang="en">', '<head>',
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        '<meta name="robots" content="noindex,nofollow,noarchive">',
        '<title>Index of HTML pages</title>',
        '<style>',
        'body { background: white; color: #111; max-width: 800px; margin: 32px auto; padding: 0 20px; font: 16px/1.45 Georgia, "Times New Roman", serif; }',
        'h1 { font-size: 1.8em; font-weight: normal; }',
        'ul { list-style: none; padding: 0; }',
        'li { margin: 0 0 16px; }',
        'a { color: #0645ad; text-decoration: underline; }',
        'a:visited { color: #551a8b; }',
        'time, .desc { color: #555; font-size: 0.9em; }',
        '</style>', '</head>', '<body>',
        '<h1>Index of HTML pages</h1>', '<ul>',
    ]
    for e in entries:
        if not e['title'].strip() or not e['description'].strip():
            raise ValueError('missing title or description')
        parsed = urlsplit(e['url'])
        if parsed.scheme != 'https' and not (
            e['url'].startswith('./') and (INDEX.parent / unquote(parsed.path)).is_file()
        ):
            raise ValueError('invalid or missing link: ' + e['url'])
        day = date.fromisoformat(e['date'])
        lines += [
            '<li><time datetime="{}">{}</time> — <a href="{}">{}</a>'.format(
                day.isoformat(), day.strftime('%d %b %Y'),
                html.escape(e['url'], quote=True), html.escape(e['title'])
            ),
            '<div class="desc">{}</div></li>'.format(html.escape(e['description']))
        ]
    return '\n'.join(lines + ['</ul>', '</body>', '</html>', ''])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    entries = json.loads(CATALOG.read_text())
    expected = build(entries)
    # Regression: October must sort after August; later entries win date ties.
    cases = [
        {'date':'2026-08-30','indexed_at':'2026-08-30T12:00:00+05:30'},
        {'date':'2026-10-01','indexed_at':'2026-10-01T12:00:00+05:30'},
        {'date':'2026-10-01','indexed_at':'2026-10-01T13:00:00+05:30'},
    ]
    assert sorted(cases, key=sort_key, reverse=True) == [cases[2], cases[1], cases[0]]
    if args.check:
        if INDEX.read_text() != expected:
            raise SystemExit('FAIL: run scripts/rebuild_index.py')
        print(f'PASS: {len(entries)} links; ISO dates/times sorted newest first')
    else:
        INDEX.write_text(expected)
        print(f'Updated /explainer/: {len(entries)} dated links')

if __name__ == '__main__':
    main()
