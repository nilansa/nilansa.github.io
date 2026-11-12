# CS Conference Research Hub

A static, no-backend paper search and research workbench for conference records from 2022–2026. It uses plain HTML, CSS, JavaScript, Web Workers, and Python build tools. The published site has no runtime package, paid API, embedding asset, external script, or PDF download.

## Use the site

Serve this directory over HTTP, for example:

```sh
python3 -m http.server 8000 --directory cs-conf/hub
```

Choose one or more fields, conferences, years, and an optional source topic or area label. CVPR 2026 is selected by default. The coverage table marks source years that are unavailable. Search loads only selected shards, one at a time. A worker scans title, author, and abstract text, scores lexical and phrase matches, and retains at most 200 results from each shard. If the transfer estimate exceeds 30 MB, the page warns and lets you continue. No shard is silently truncated during scanning.

Pins stay in browser storage; old CVPR pins using `cvpr-research-hub-pins-v1` remain readable. Search text and Idea Lab packets are not sent to a server. Idea Lab accepts papers from different venues even when they share a field. Every packet is labelled **UNTESTED** and cites each paper's venue and original source.

## Corpus and build

The existing `data/2022.json` through `data/2026.json` CVPR corpus is reused without modification. Other available venue/year records are stored in compact JSON at `data/venues/{VENUE}/{year}.json`. `catalog.json` records per-shard counts, byte sizes, checksums, source URLs and revisions, license information when declared, abstract coverage, and unavailable years. An unavailable year is not a zero-paper acceptance count.

The source is the `ai-conferences/{VENUE}{YEAR}` dataset on Hugging Face. The build uses `uv` and `pyarrow` only at build time; these are not browser or runtime dependencies. Rebuilds write one normalized shard at a time and leave identical files untouched:

```sh
uv run --with pyarrow python cs-conf/hub/tools/build_conferences.py
```

The existing CVPR builder and `search_cvpr.py` are preserved. The multi-venue search CLI is:

```sh
python3 cs-conf/hub/tools/search_conferences.py "diffusion restoration" --venue CVPR --venue ECCV --venue ACL --year 2022 --year 2026 --limit 20
python3 cs-conf/hub/tools/search_conferences.py '"visual instruction tuning"' --venue ACL --venue EMNLP --year 2024 --json
```

It reads checked-in JSON only and emits original trusted paper links and source labels. It does not fetch data or PDFs.

## Source limits

The dataset is a curated metadata collection. A record in it does not independently verify that the paper appeared in the conference's main track. The page labels track status as unverified unless the source provides a track label, and even a source-provided label remains attributed to that dataset. Only HTTPS paper or PDF URLs on the configured conference publisher domains are retained. Missing and untrusted URLs stay empty.

Some ICRA and ICASSP source records do not have abstracts. They remain findable by title and authors, show “Abstract unavailable,” but cannot be selected as evidence in Idea Lab until an abstract and trusted source link are available. A dataset card that declares no license is shown as such; paper rights remain with authors or other rights holders. Field labels and area fallbacks support discovery only. They are not conference rankings, acceptance predictions, or official classifications.

The old CVPR snapshots retain their own provenance in `provenance.json`. See `catalog.json` for actual non-CVPR source revisions, license declarations, counts, and hashes.

## Release QA

Run Python unit tests, JavaScript syntax checks and the Node worker security tests under the tests folder. The Node test checks stored URLs against browser/worker allowlists and checks topic-only filtering. Search ranking is approximate: the Python CLI uses the original CVPR BM25-style scorer, while the browser uses a bounded per-shard lexical scorer, so score scales and result order may differ. Full-text similarity and independent novelty verification are not implemented.

## Research assistant (local, opt-in)

The archival website remains static. A separate, testable CLI can search Cito or Semantic Scholar, export selected hub pins to a private source manifest, and use an authenticated NotebookLM CLI to ask source-grounded questions. Optional local semantic retrieval (BM25 + BGE + RRF) is available as a prototype; its index must be built separately. See [RESEARCH_ASSISTANT.md](RESEARCH_ASSISTANT.md) and [SEMANTIC_RETRIEVAL.md](SEMANTIC_RETRIEVAL.md). The site does **not** claim deployed full-text semantic retrieval or AI chat.
