# CS Conference Research Hub

A static, no-backend paper discovery and evidence-comparison workbench. Current indexed records cover 2022–2026; the ten-year selector also shows 2017–2021 as not yet indexed. It uses plain HTML, CSS, JavaScript, Web Workers, and Python build tools. The published site has no runtime package, paid API, embedding asset, external script, or PDF download.

## Use the site

Serve this directory over HTTP, for example:

```sh
python3 -m http.server 8000 --directory cs-conf/hub
```

Use the independently authored `taxonomy.json` to expand AI, Systems, Theory or Interdisciplinary into 31 subfields and select any of 105 listed venues. Only the 12 venues with existing metadata are selectable; unindexed venues are clearly disabled, not shown as zero papers. CVPR is selected by default, with up to five available years preselected. The coverage table marks source years that are unavailable. Search loads only selected shards, one at a time. A worker scans title, author, and abstract text, scores lexical and phrase matches, and retains at most 200 results from each shard. If the transfer estimate exceeds 30 MB, the page warns and lets you continue. No shard is silently truncated during scanning.

Pins stay in browser storage; old CVPR pins using `cvpr-research-hub-pins-v1` remain readable. Search text and paper-comparison packets are not sent to a server. The **Compare papers** workbench accepts any two papers, generates cited abstract excerpts and research questions, and explicitly avoids automatically mixing a method paper with a problem paper. Excerpts are unverified; the workbench is not an LLM or a novelty evaluator.

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


## Research discovery foundation (development branch, 2026-11-03)

The taxonomy is independently written and is **not a CSRankings ranking or a redistribution of its non-derivative-licensed dataset**. A venue may appear in multiple areas; its papers do not automatically inherit all those subject labels. New venues (such as SIGMOD, SOSP, OSDI, SIGCOMM, CCS, CHI and STOC) are presently **navigation entries, not indexed papers**.

- `taxonomy.json`: Four top-level areas, 31 subareas and 105 distinct venue labels, with aliases and multi-area placement.
- `paper.schema.v2.json`: Forward-compatible research metadata contract separating official fields, provenance, task, method, domain, dataset, evaluation and application. It is **not** retroactively applied to existing v1 records.
- `tools/paper_identity.py`: Conservative stable paper keys, preferring DOI, OpenReview and Anthology identifiers before normalized title+venue+year.
- `tools/research_query.py`: Offline, JSON-speaking research retrieval across indexed venue/year shards, with explicit missing fields, source-attributed links and metadata checksum, plus transparent "unindexed" venue warnings. This is lexical retrieval only.
- `DATA_SOURCES.md`: Evidence-based source/API/rights comparison, ingestion precedence, missing-year logic and publication/reuse safety gates.
- `tests/test_research_discovery.py`: Registry, multi-venue, identity, provenance and negative-path contract tests.

### Agent-facing retrieval examples

```sh
python3 cs-conf/hub/tools/research_query.py "retrieval adaptation" --venue CVPR --venue ACL --year-from 2022 --year-to 2026 --limit 15
python3 cs-conf/hub/tools/research_query.py "query performance" --area databases --year-from 2017 --year-to 2026 --require-abstract
python3 cs-conf/hub/tools/research_query.py "memory" --venue NeurIPS --author Chen --limit 10
```

The second command correctly reports that SIGMOD/PVLDB/ICDE etc. have **not yet been ingested**; it must not fabricate a results set. A connected agent can read the JSON through a permitted local command/file integration. This work does **not** imply ChatGPT or Claude Science has already connected to the index. No public API server or paid dependency is introduced.

For release and tests:

```sh
python3 -m unittest discover -s cs-conf/hub/tests -p "test_*.py"
node --check cs-conf/hub/app.js
node --check cs-conf/hub/search-worker.js
```

New source ingestion must follow the content-rights gates in `DATA_SOURCES.md`. Existing non-CVPR dataset cards often declare no license, so this branch does not re-publish new abstracts or mirror PDFs. The original CVPR files and all venue/year JSON shards remain untouched.
