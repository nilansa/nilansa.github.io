# CS Conference Research Hub — Agent/API Guide

**Purpose:** machine-readable instructions for agents, scripts and researchers using the CS Conference Research Hub.

- **Live hub:** https://nilansa.github.io/cs-conf/hub/
- **Static data base URL:** https://nilansa.github.io/cs-conf/hub
- **Source repository:** https://github.com/nilansa/nilansa.github.io/tree/main/cs-conf/hub
- **Repository path:** cs-conf/hub/
- **Source snapshot checked:** 11 November 2026; main commit 969c415737f19a307d200fe88d8d306851a7102e

> **API status:** The published hub is a static, read-only website. It does **not** currently expose a server-side REST API, OpenAPI/Swagger specification, database service, or authenticated API. The supported machine interfaces are the static JSON files and the Python search CLI documented below. Do not assume routes such as /api/v1/search, /api/v1/health, or /api/v1/schema exist on GitHub Pages.

---

## 1. What the hub can do

The hub is a research-paper metadata archive and discovery workbench covering 12 computer-science conferences and the years 2022–2026.

Agents can use it to:

1. Search paper titles, authors and abstracts.
2. Search multiple conferences and years in one query.
3. Explore vision papers across CVPR, ICCV and ECCV.
4. Compare vision work with related methods from NeurIPS, ICML, ICLR, AAAI, ACL and other indexed venues.
5. Retrieve abstracts, author strings, paper identifiers, official publisher links and source provenance.
6. Inspect corpus coverage, missing years, source revisions, checksums and abstract coverage.
7. Find papers by author name by searching the author text.
8. Use the browser to pin papers and export/import a local paper collection.
9. Create a two-paper, cross-conference **UNTESTED** hypothesis packet in Idea Lab, then copy it as JSON or Markdown.

The archive stores metadata and abstracts. It does not host paper PDFs, search the full text of PDFs, run models, verify novelty, or decide whether a paper is genuinely novel.

## 2. Supported interfaces

| Interface | Use it for | Request style |
|---|---|---|
| Static JSON data | Read the catalogue and paper records | HTTP GET |
| Python multi-conference CLI | Ranked search across venues and years | Command line; optional JSON output |
| Browser UI | Interactive filters, search, pins and Idea Lab | Open the hub in a browser |
| Browser search worker | Internal implementation of browser search | JavaScript postMessage; not a public API |

All supported data access is read-only. There is no authentication token or API key.

## 3. Static JSON data API

### 3.1 Base URL and routes

Use HTTPS and append these paths to the base URL:

| Method | Path | Meaning |
|---|---|---|
| GET | /catalog.json | Conference catalogue, coverage, per-shard metadata and provenance |
| GET | /data/{YEAR}.json | CVPR paper bundle for that year |
| GET | /data/venues/{VENUE}/{YEAR}.json | Non-CVPR paper bundle for that venue and year |

Examples:

- https://nilansa.github.io/cs-conf/hub/catalog.json
- https://nilansa.github.io/cs-conf/hub/data/2026.json — CVPR 2026
- https://nilansa.github.io/cs-conf/hub/data/venues/ECCV/2024.json — ECCV 2024
- https://nilansa.github.io/cs-conf/hub/data/venues/NeurIPS/2025.json — NeurIPS 2025

Use the venue spelling and capitalization shown in the catalogue. For CVPR, use the shorter data/{YEAR}.json path; do not use data/venues/CVPR/.

There are no search query parameters on these file routes. Download the relevant JSON shard and filter/search its papers array locally, or use the Python CLI.

### 3.2 Catalogue schema

catalog.json has the following top-level structure:

~~~json
{
  "schema": "cs-conf-catalog-v1",
  "taxonomy": {
    "Computer Vision & 3D": ["CVPR", "ICCV", "ECCV"],
    "Machine Learning & AI": ["NeurIPS", "ICML", "ICLR", "AAAI"],
    "Language/NLP": ["ACL", "EMNLP", "NAACL"],
    "Robotics & Speech": ["ICRA", "ICASSP"]
  },
  "venues": {
    "CVPR": {
      "available_years": [2022, 2023, 2024, 2025, 2026],
      "years": {
        "2026": {
          "count": 4069,
          "file": "data/2026.json",
          "bytes": 9014661,
          "sha256": "<64-character SHA-256>",
          "source_url": "<source URL>",
          "revision": "<source revision>",
          "abstract_coverage": 1.0,
          "license": "<source license note>"
        }
      },
      "missing_years": [],
      "total_records": 14083
    }
  },
  "source_dataset": "https://huggingface.co/datasets/ai-conferences"
}
~~~

The example is abbreviated. Read the live catalog.json for the complete catalogue and exact per-year values.

Important catalogue fields:

- schema: catalogue schema identifier.
- taxonomy: broad discovery groups; these are not official conference rankings.
- venues: map keyed by venue name.
- available_years: years for which a shard exists.
- years: per-year metadata, keyed by the year as a string.
- years[year].count: number of records in that shard.
- years[year].file: relative path to the JSON shard.
- years[year].bytes: expected shard size in bytes.
- years[year].sha256: SHA-256 of the checked-in shard.
- years[year].source_url and dataset_url: source locations.
- years[year].revision: source dataset revision where available.
- abstract_count and abstract_coverage: abstract availability where supplied.
- license: source dataset's license declaration or an explicit note that the dataset card does not declare one.
- missing_years: years with no shard in this source snapshot. A missing year is **not** a zero-paper count.
- total_records: total records across the available years for that venue.

Optional fields differ slightly between the original CVPR corpus and the newer multi-venue catalogue. Do not assume every optional provenance field exists for every venue.

### 3.3 Current corpus coverage

The checked catalogue contains **130,361 records** across 12 venues.

| Venue | Records | Available years |
|---|---:|---|
| CVPR | 14,083 | 2022, 2023, 2024, 2025, 2026 |
| ICCV | 4,857 | 2023, 2025 |
| ECCV | 6,896 | 2022, 2024, 2026 |
| NeurIPS | 23,108 | 2022–2026 |
| ICML | 15,269 | 2022–2026 |
| ICLR | 13,982 | 2022–2026 |
| AAAI | 12,405 | 2022–2026 |
| ACL | 6,709 | 2022–2026 |
| EMNLP | 7,656 | 2022–2026 |
| NAACL | 1,722 | 2022, 2024, 2025 |
| ICRA | 8,585 | 2022–2026 |
| ICASSP | 15,089 | 2022–2026 |

**Vision-specific coverage:**

- CVPR: all five years, 2022–2026.
- ECCV: 2022, 2024 and 2026; 2023 and 2025 are unavailable.
- ICCV: 2023 and 2025; 2022, 2024 and 2026 are unavailable.

Always consult catalog.json before requesting a venue/year combination. The CLI skips absent files, so an agent should not silently interpret a skipped year as evidence that no papers exist.

### 3.4 Paper bundle structure

Every shard is a JSON object containing a papers array.

A non-CVPR shard has this structure:

~~~json
{
  "venue": "ECCV",
  "year": 2024,
  "source": "https://huggingface.co/datasets/...",
  "papers": [
    {
      "id": "eccv-2024-<stable-id>",
      "venue": "ECCV",
      "year": 2024,
      "title": "Example paper title",
      "authors": "Author One, Author Two",
      "abstract": "Paper abstract...",
      "paper_url": "https://eccv.ecva.net/...",
      "pdf_url": "https://...",
      "source": "Curated venue record · ai-conferences",
      "track_status": "Curated venue record; track not independently verified",
      "cluster": "Computer Vision & 3D",
      "primary_area": "Computer Vision & 3D"
    }
  ]
}
~~~

The field values above are illustrative, not a real paper record.

Common paper fields:

| Field | Meaning |
|---|---|
| id | Record identifier; use it to deduplicate records |
| venue | Conference name; may be added by the browser/CLI for legacy CVPR records |
| year | Publication year |
| title | Paper title |
| authors | Author names as a display/search string |
| abstract | Abstract text; may be empty |
| paper_url | Trusted publisher paper page, when available |
| pdf_url | Trusted publisher PDF URL, when available |
| source | Dataset/provenance label |
| track_status | Track attribution or an explicit unverified status |
| cluster | Discovery area label |
| primary_area | Source area/keyword label or venue-level fallback |

The legacy CVPR bundle uses data/{YEAR}.json and contains top-level year, source and papers. Its records include:

- id, title, authors, abstract, year
- abstract_status
- pdf_url, pdf_status
- cvf_url, cvf_reference_type
- source, cluster
- track_status, track_basis

For CVPR, the browser and multi-conference CLI normalize cvf_url into paper_url and identify the record as CVPR. The original CVPR shard may not contain the normalized venue or paper_url field. Preserve the original fields when saving records; do not discard provenance fields.

### 3.5 Direct HTTP examples

Set the base URL once:

~~~bash
BASE="https://nilansa.github.io/cs-conf/hub"

# Inspect the catalogue and CVPR coverage.
curl -fsSL "$BASE/catalog.json" | jq '.venues.CVPR'

# Read a CVPR shard.
curl -fsSL "$BASE/data/2026.json" |
  jq '{year, paper_count: (.papers | length), example: .papers[0]}'

# Read an ECCV shard.
curl -fsSL "$BASE/data/venues/ECCV/2024.json" |
  jq '{venue, year, paper_count: (.papers | length), example: .papers[0]}'

# Retrieve one record by its ID after obtaining the ID from search.
PAPER_ID="replace-with-real-id"
curl -fsSL "$BASE/data/2026.json" |
  jq --arg id "$PAPER_ID" '.papers[] | select(.id == $id)'
~~~

For a paper in a non-CVPR venue, use that venue's shard path. There is no dedicated /paper/{id} endpoint.

### 3.6 Minimal Python data client

This example uses Python's standard library and does not require an API key or third-party package:

~~~python
import json
from urllib.request import urlopen

BASE = "https://nilansa.github.io/cs-conf/hub"

def get_json(relative_path: str):
    url = f"{BASE}/{relative_path}"
    with urlopen(url, timeout=30) as response:
        return json.load(response)

def get_catalog():
    return get_json("catalog.json")

def get_shard(venue: str, year: int):
    if venue == "CVPR":
        path = f"data/{year}.json"
    else:
        path = f"data/venues/{venue}/{year}.json"
    return get_json(path)

catalog = get_catalog()
print(catalog["venues"]["CVPR"]["available_years"])

eccv_2024 = get_shard("ECCV", 2024)
print(len(eccv_2024["papers"]))
~~~

Validate venue and year against the catalogue before constructing a path. Cache downloaded shards during a research task rather than downloading the same file repeatedly.

---

## 4. Python multi-conference search CLI

### 4.1 What it does

The supported multi-venue search command is:

~~~bash
python3 cs-conf/hub/tools/search_conferences.py
~~~

It reads checked-in JSON files only. It does not fetch new papers, call an external LLM, download PDFs, or require network access after the repository has been obtained.

Run it from the repository root. Python 3.8 or newer is recommended.

### 4.2 Arguments

| Argument | Required? | Default | Description |
|---|---|---|---|
| query | Yes | — | Words or a quoted phrase searched in titles, authors and abstracts |
| --venue VENUE | No | CVPR | Venue to search; repeat to search multiple venues |
| --year YEAR | No | All years 2022–2026 | Year to search; repeat to select multiple years |
| --limit N | No | 10 | Maximum results returned; allowed range 1–500 |
| --json | No | Off | Emit a structured JSON object to stdout |

Allowed venue values:

~~~text
CVPR ICCV ECCV NeurIPS ICML ICLR AAAI ACL EMNLP NAACL ICRA ICASSP
~~~

The venue and year arguments are repeatable. The same year selection applies to every selected venue. Check coverage first so the agent knows which venue/year pairs are actually present.

### 4.3 Basic examples

Search CVPR across all available years (CVPR is the default venue):

~~~bash
python3 cs-conf/hub/tools/search_conferences.py "video object segmentation" --limit 30
~~~

Search a phrase in CVPR:

~~~bash
python3 cs-conf/hub/tools/search_conferences.py '"3D Gaussian Splatting"' \
  --venue CVPR --year 2024 --year 2025 --limit 25 --json
~~~

Search CVPR and ECCV for years available in both:

~~~bash
python3 cs-conf/hub/tools/search_conferences.py "diffusion restoration" \
  --venue CVPR --venue ECCV \
  --year 2024 --year 2026 --limit 40 --json
~~~

Search CVPR and ICCV for years available in both:

~~~bash
python3 cs-conf/hub/tools/search_conferences.py "open vocabulary segmentation" \
  --venue CVPR --venue ICCV \
  --year 2023 --year 2025 --limit 50 --json
~~~

Search vision and language work together:

~~~bash
python3 cs-conf/hub/tools/search_conferences.py "visual grounding" \
  --venue CVPR --venue ECCV --venue ACL \
  --year 2024 --year 2026 --limit 50 --json
~~~

Compare computer-vision papers with general ML methods:

~~~bash
python3 cs-conf/hub/tools/search_conferences.py "test time adaptation" \
  --venue CVPR --venue NeurIPS --venue ICLR \
  --year 2024 --year 2025 --year 2026 --limit 60 --json
~~~

Search for an author by name:

~~~bash
python3 cs-conf/hub/tools/search_conferences.py '"Author Name"' \
  --venue CVPR --year 2024 --year 2025 --year 2026 --limit 30 --json
~~~

Author search is ordinary text matching over the author field. There is no separate author endpoint.

### 4.4 JSON response

With --json, the CLI returns one JSON object:

~~~json
{
  "query": "visual grounding",
  "venues": ["CVPR", "ECCV", "ACL"],
  "years": [2024, 2026],
  "results": [
    {
      "id": "record-id",
      "venue": "CVPR",
      "year": 2026,
      "title": "Paper title",
      "authors": "Author One, Author Two",
      "abstract": "Paper abstract...",
      "paper_url": "https://openaccess.thecvf.com/...",
      "pdf_url": "https://openaccess.thecvf.com/...",
      "source": "Hugging Face dataset",
      "score": 4.12345
    }
  ]
}
~~~

This is an abbreviated example. Actual results preserve the available source-record fields and add a search score, a venue, and a normalized paper_url.

Use jq to inspect or post-process results:

~~~bash
python3 cs-conf/hub/tools/search_conferences.py "visual grounding" \
  --venue CVPR --venue ECCV --year 2024 --year 2026 --limit 50 --json |
  jq '.results[] | {venue, year, title, authors, score, paper_url}'
~~~

Save results for a reproducible research audit:

~~~bash
python3 cs-conf/hub/tools/search_conferences.py "visual grounding" \
  --venue CVPR --venue ECCV --year 2024 --year 2026 --limit 50 --json \
  > visual-grounding-cvpr-eccv.json
~~~

### 4.5 Search and ranking behaviour

- The Python CLI uses the BM25-style ranker in tools/search_cvpr.py.
- It searches title, author and abstract text.
- Title matches receive greater weight than author or abstract matches.
- Exact phrase matches and adjacent word pairs receive ranking boosts.
- Results are ordered by descending score, then newer year, venue and title.
- The score is a retrieval-ranking value, **not** a probability, confidence score, quality score or novelty score.
- Compare scores only within the same query/run. Do not treat scores from different queries as directly comparable.
- The CLI does not provide --topic, --sort, --author, --similar, or --semantic options.

The browser's search worker uses a separate, simpler lexical scorer. Browser scores and CLI scores are not on the same scale and their result order can differ.

### 4.6 Important CLI behaviour

- If --venue is omitted, the CLI searches CVPR only.
- If --year is omitted, it searches 2022–2026.
- --limit must be between 1 and 500.
- Missing venue/year files are skipped by the CLI. Read the catalogue first and report skipped/unavailable years explicitly.
- The CLI does not expose an API for fetching a paper by ID. Fetch the appropriate shard and filter its papers array.
- The CLI does not download or inspect the paper PDF.

---

## 5. Browser UI usage

Open https://nilansa.github.io/cs-conf/hub/.

### 5.1 Search across conferences

1. Select one or more research-field groups.
2. For computer vision, use **Computer Vision & 3D** and select CVPR, ECCV and/or ICCV.
3. Select one or more years.
4. Check the availability matrix before searching. A dash means that source shard is unavailable.
5. Enter a search phrase or terms.
6. Optionally enter a topic/area label.
7. Choose Best match, Newest first, Oldest first or Title A–Z.
8. Open a result to inspect its abstract, authors, track status and publisher links.

The page loads only selected venue/year shards, one at a time. It estimates the metadata transfer size and warns when the selected files exceed 30 MB. The browser retains up to 200 matching results per selected shard and displays results in pages of 40.

### 5.2 Topic/area filter

The topic field filters source area labels and CVPR keyword clusters. It is a metadata filter, not embedding-based semantic search. All topic words must match the record's area/cluster text.

Examples of useful labels/terms include:

- 3D reconstruction
- geometry
- segmentation
- retrieval
- diffusion
- speech
- robotics

The exact available labels depend on the source records. Inspect cluster and primary_area rather than assuming a fixed controlled vocabulary.

### 5.3 Pins

- Use **Pin** on a result to save it in the current browser.
- Pins are stored in browser localStorage; they are not uploaded to a server or synchronized automatically across devices.
- Use **Export pins** to save a JSON backup.
- Use **Import pins** to restore a previously exported collection.
- The export schema is cs-conference-hub-pins-v1, with exported_at and pins fields.
- The current browser key is cs-conference-hub-pins-v1; the older cvpr-research-hub-pins-v1 key remains readable.

### 5.4 Idea Lab

Idea Lab accepts two different papers:

1. Select a paper as the **problem paper**.
2. Select another paper as the **method paper**.
3. Review the generated evidence packet.
4. Copy it as JSON or Markdown.

The packet has schema cs-conference-hypothesis-packet-v1 and includes:

- status: always UNTESTED.
- hypothesis: a proposed connection between the selected papers.
- evidence: the selected papers, source links and extracted abstract sentences.
- comparison: suggested baseline, controls and reporting requirements.
- falsification: a test that could show the proposed connection does not work.
- novelty_warning: a reminder that combining two papers does not prove novelty.

**Important:** Idea Lab uses simple sentence-pattern matching to extract candidate challenge/method sentences. It does not use an LLM, verify the interpretation, establish novelty, run experiments or validate the hypothesis. Treat its output as a starting evidence packet only. A paper without a usable abstract or trusted paper link cannot be selected as Idea Lab evidence.

---

## 6. Internal browser worker contract (not a public REST API)

The browser UI delegates search to search-worker.js. This is an internal JavaScript interface, useful if an engineer is extending the current frontend. It is not a stable external API and should not be called as an HTTP endpoint.

Example request:

~~~javascript
worker.postMessage({
  type: "search",
  requestId: 1,
  query: "visual grounding",
  shards: [
    { venue: "CVPR", year: 2024 },
    { venue: "ECCV", year: 2024 },
    { venue: "ACL", year: 2024 }
  ],
  sort: "relevance",
  topic: "",
  offset: 0,
  limit: 40
});
~~~

Supported sort values:

- relevance
- newest
- oldest
- title

The worker emits messages carrying the same requestId:

- progress: shard download/scan progress.
- results: total, retained, offset, results and number of shards.
- error: an error message.

Cancel a running request:

~~~javascript
worker.postMessage({ type: "cancel", requestId: 1 });
~~~

The worker fetches the selected static JSON files relative to its own location. It scans title, author and abstract fields, applies the optional topic filter, and retains at most 200 hits per shard. Do not mistake this worker message contract for a deployed REST service.

---

## 7. Provenance, quality and limitations

### 7.1 Data sources

- CVPR records reuse the existing choucsan/CVPR_Papers dataset and retain provenance in provenance.json; CVF Open Access proceedings listings are used to reconcile paper pages and PDF links.
- Other conference/year shards are built from the ai-conferences/{VENUE}{YEAR} Hugging Face datasets.
- catalog.json records source revisions, source URLs, file sizes, checksums, abstract coverage and license declarations where available.

Follow the paper's publisher link for the authoritative paper. The archive is a discovery index, not the publisher of record.

### 7.2 Track labels

A record's presence in a venue shard does not independently prove that it appeared in the conference's main track. track_status and related fields preserve source attribution or state that the track is not independently verified. Do not convert an unverified label into a confirmed acceptance claim.

### 7.3 Missing abstracts and links

Some records have no abstract or no trusted paper URL. They may still be discoverable by title/author, but they provide weaker evidence. ICRA and ICASSP records have historically had incomplete abstract coverage in some source years. Check the record itself and the catalogue's abstract coverage.

### 7.4 No semantic or full-text search

The current implementation does not provide:

- Embedding/vector search.
- Semantic similarity or find_similar_papers endpoints.
- Citation graph traversal.
- Full-text PDF indexing or PDF retrieval.
- An LLM research agent or automated novelty verification.
- A dedicated author lookup endpoint.
- A server-side REST API or database.

An agent may approximate broader discovery by issuing several lexical queries, merging/deduplicating results by id, then using its own reasoning to compare the abstracts and inspecting the original papers. It must label that synthesis as agent analysis, not a hub-provided semantic-search result.

### 7.5 Privacy

The browser UI performs search locally after downloading selected public metadata shards. Search text and Idea Lab packets are not sent to a hub backend. Pins are local to the browser unless the user explicitly exports and transfers them.

---

## 8. Recommended agent workflow

Use this sequence for a research question, especially a CVPR/vision problem:

1. **Read the catalogue first.** Fetch catalog.json; identify the relevant venues and available years.
2. **Choose a bounded search.** Start with CVPR and the closest vision venue (ECCV or ICCV). Add NeurIPS/ICLR/ICML when the method may cross into general ML.
3. **Respect year intersections.** Do not assume every venue has every year. For example, ICCV is available only in 2023 and 2025 in this snapshot.
4. **Run several focused queries.** Search the task, method family, benchmark/dataset and known terminology separately. Use exact quotes for phrases when useful.
5. **Use JSON output.** Preserve the query, venues, years, score, record ID, abstract and source links.
6. **Deduplicate by id.** Keep the original venue/year and provenance fields.
7. **Inspect primary sources.** Open the publisher paper page and PDF at the source. Do not rely on the abstract alone for equations, experiments, limitations or novelty.
8. **Synthesize across papers.** Separate what a paper actually states from the agent's interpretation and proposed extension.
9. **Check novelty independently.** Search alternative names and adjacent methods; the hub does not certify novelty.
10. **Report coverage and limitations.** State the exact venues/years queried, unavailable pairs, result count, source links and whether conclusions are abstract-only or full-paper verified.

### Example task for an agent

~~~text
Use the CS Conference Research Hub as a literature-discovery source.

Research question:
Find recent approaches to open-vocabulary 3D scene understanding and identify
possible extensions that could be tested with modest compute.

Procedure:
1. Fetch https://nilansa.github.io/cs-conf/hub/catalog.json.
2. Check availability for CVPR, ECCV and ICCV before searching.
3. Search CVPR + ICCV for 2023 and 2025:
   "open vocabulary 3D", "open-vocabulary segmentation",
   "3D scene understanding", and "language-guided 3D".
4. Search CVPR + ECCV for 2024 and 2026:
   "3D scene understanding", "open-vocabulary 3D",
   and "vision language 3D".
5. Save JSON results and deduplicate by paper ID.
6. Group papers by problem, representation, supervision, method,
   benchmark and stated limitation.
7. Open the original publisher sources for the most relevant papers.
8. Propose research directions only after checking the papers.
9. For every proposed direction, cite supporting papers and distinguish:
   (a) source-backed facts,
   (b) your interpretation,
   (c) an untested hypothesis,
   (d) the experiment that could falsify it.
10. Do not claim the hub performed semantic search or verified novelty.
~~~

---

## 9. Local use and development

From the root of a local clone of nilansa/nilansa.github.io, run the site over HTTP:

~~~bash
python3 -m http.server 8000 --directory cs-conf/hub
~~~

Then open http://127.0.0.1:8000/.

Run a multi-conference search locally:

~~~bash
python3 cs-conf/hub/tools/search_conferences.py "visual grounding" \
  --venue CVPR --venue ECCV --venue ACL \
  --year 2024 --year 2026 --limit 50 --json
~~~

The checked-in JSON is sufficient for search. The multi-venue data build uses uv and pyarrow at build time; these are not browser/runtime dependencies. Do not run the dataset builder merely to search existing data.

Useful source files:

- README.md — site overview and current limitations.
- catalog.json — current coverage and shard manifest.
- app.js — browser UI, filters, pins and Idea Lab.
- search-worker.js — browser-side lexical search.
- tools/search_conferences.py — multi-venue CLI.
- tools/search_cvpr.py — CVPR BM25-style ranker.
- tools/build_conferences.py — non-CVPR shard builder.
- tools/build_cvpr_hub.py — CVPR corpus builder.
- provenance.json — CVPR source and validation record.
- tests/ — schema, source-link and search-worker checks.

## 10. Quick reference

| Need | Use |
|---|---|
| Discover available conferences/years | GET /catalog.json |
| Read CVPR papers for a year | GET /data/{YEAR}.json |
| Read ECCV/ICCV/NeurIPS/etc. papers | GET /data/venues/{VENUE}/{YEAR}.json |
| Search one or more venues | tools/search_conferences.py |
| Get structured search output | Add --json |
| Search an author name | Use the name as the CLI query |
| Retrieve one paper by ID | Fetch its shard and filter papers |
| Pin papers | Browser UI; local browser storage |
| Export/import pins | Browser UI; JSON file |
| Build a two-paper hypothesis packet | Browser UI Idea Lab |
| Semantic similarity / citation graph / full text | Not currently supported |
| REST API / API key / POST endpoint | Not currently provided |

**Agent rule:** Treat the catalogue and paper records as the source for what the hub contains; treat the publisher page as the source of truth for the paper; treat all research synthesis and novelty claims as the agent's own work requiring independent verification.
