# CS Conference Hub — research discovery implementation review

**Date:** 2026-11-03 (Asia/Kolkata)  
**Repository:** https://github.com/nilansa/nilansa.github.io  
**Development branch:** https://github.com/nilansa/nilansa.github.io/tree/cs-conf/research-discovery-v1-20261103/cs-conf/hub  
**Production deployment:** None. Main and the live published site were not modified.  
**File transfer:** GitHub connector reads and writes only; no ChatGPT ↔ Codex/local transfer, browser UI transfer, scratch index, credential sync or public PDF mirroring.

## Changes staged on the development branch

| Feature | Change | Boundary |
|---|---|---|
| CS-wide navigator | Independent taxonomy.json with **4 areas, 31 subareas and 105 distinct conference labels**, including AI, Systems, Theory, HCI, Robotics, Security, OS, Databases, Networks, Software Engineering, PL and more | The 12 indexed venues are selectable; the 93 others are labelled not indexed |
| Multi-conference UI | app.js and style.css show collapsible subareas and synchronized multi-area venue checkboxes, retaining the existing multi-venue search worker | No new published corpus |
| Years | Browser shows **2017–2026**, with unindexed years disabled and up to five currently available years selected by default | Actual indexed archive still only covers 2022–2026 |
| Evidence workbench | Replaced prescriptive problem-plus-method idea assembly with Paper A vs Paper B source-excerpt comparisons, research-check questions and cautious source warnings | No automatic novelty or compatibility claim; this is not an LLM |
| Research record contract | paper.schema.v2.json models identifiers, publication track, source rights, facets for task/method/domain/dataset/evaluation/application, and provenance | Contract only; old JSON records are unchanged |
| Identity and retrieval | tools/paper_identity.py provides conservative DOI/OpenReview/Anthology/title-venue-year keys; tools/research_query.py exposes JSON results with original source links and explicit missing fields | Offline lexical CLI, not a hosted semantic/API service |
| Corpus audit | tools/audit_corpus.py checks checksum/count coverage, abstract fields, existing links, license declarations and potential duplicate keys | Read-only, no records rewritten |
| Sources and QA | DATA_SOURCES.md, new Python tests and branch-only GitHub Actions checks | No external API ingestion or Claude Science/Codex integration was performed |

## Verified corpus audit

[Successful GitHub Actions run](https://github.com/nilansa/nilansa.github.io/actions/runs/41623281369) executed the read-only audit, tests and browser worker regressions.

| Metric | Verified |
|---|---:|
| Venues indexed | 12 |
| Venue/year shards | 53 |
| Source records (not globally deduplicated papers) | **130,361** |
| Records with abstracts | **108,343 (83.11%)** |
| Missing abstracts | **22,018 (16.89%)** |
| Records with paper landing URLs | **127,409 (97.74%)** |
| Records in source shards whose dataset card declares no license | **116,278 (89.20%)** |
| Conservative candidate identity collisions | **1**, two ICASSP 2026 records with different source IDs but the same title/year key; review manually |
| Distinct identity keys under current conservative rules | **130,360** |

**Important coverage gaps:** ICASSP's 15,089 records have no abstracts in the current source. ICRA has only 2,761 abstracts of 8,585 records (32.2%), and ECCV has 5,855 of 6,896 (84.9%). CVPR remains 14,083 records with 14,077 abstracts. These are limitations of indexed metadata, not claims about official publisher abstracts.

The **53 original static JSON shards total approximately 205.4 MiB**, and five-year CVPR JSON totals approximately 28.8 MiB. The browser processes selected shards sequentially and warns when transfer exceeds 30 MiB. These are file-size observations, not measured device memory, browser latency or semantic search quality.

**Rights gate:** No declared dataset license does not necessarily mean that reuse is prohibited, but it does not grant affirmative permission to redistribute all included abstracts. Underlying paper PDFs, abstract texts, compilation metadata and official proceedings may have distinct rights. No new records or PDFs were added to the live archive in this milestone.

## Tests

Branch CI was green at commit **5432079b3796c46e6ba92a3c8a81ddad0c118bda**. It reported **22 Python unit tests passed**, Python compilation, JavaScript syntax checks, 127,409 URL allowlist checks across 53 indexed shards, topic-only worker filtering, JSON contract parsing, and read-only SHA-256 validation. The first CI runs had failed on a legacy HTML assertion expecting the removed Idea Lab warning; that assertion was updated and subsequent complete tests passed.

No new browser end-to-end navigation/memory test or Claude Science agent evaluation has run yet. A green source-level CI is not a real-device UX or scientific result.

## Source decisions

DBLP CC0 for breadth, official proceedings/ACL Anthology/OpenReview for venue and track truth, Crossref DOI for identity, OpenAlex and Semantic Scholar for selective relationships and citations, and Hugging Face mirrors only after field-level rights/source verification. OpenAlex in 2026 supports limited keyless queries and a $1/day free-account API budget; do not assume historical unlimited use. Crossref public and polite pools have documented request/concurrency limits. CSRankings' CC BY-NC-ND ranking data/code were not imported.

## Next highest-value milestone

First ingest authoritative, lawfully reusable **SIGMOD/PVLDB (Databases)** or **SOSP/OSDI (Operating Systems)** metadata and properly verified track, starting with one representative recent year; then extend 2022–2026 and 2017–2021 with traceable provenance, abstract-rights gates and tests. Add source-field-level v2 normalization and citations only after source quality is verified. Benchmark natural-language/semantic retrieval against lexical search and test peak memory before adding a server or embedding index. When a truly authorized Claude Science/Codex session is available, test direct use of the grounded retrieval JSON with no unsynced file handoffs.

**Decision:** Continue the branch, **do not merge or deploy** until a browser interaction review and content-rights review are complete. All pre-existing CVPR and other venue/year data files remain untouched.
