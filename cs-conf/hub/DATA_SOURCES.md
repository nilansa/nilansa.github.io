# Research corpus sources: verification and redistribution gates

**Reviewed 2026-11-03.** This is an engineering source decision record, not a statement that the listed APIs have already been integrated. No publisher PDFs have been downloaded, and no new external metadata was inserted into the public corpus during this milestone.

## Current repository status

The checked-in \`catalog.json\` reports **130,361 venue/year records across 12 conferences (2022–2026)**, including **14,083 CVPR records**. This is not a count of globally deduplicated unique works. The existing 2022–2026 JSON shards remain unchanged in this milestone.

The \`ai-conferences/{VENUE}{YEAR}\` metadata used for most non-CVPR shards often has **no declared dataset license** in the saved catalog. This does not itself prove the records cannot be used, but it **does not grant permission to republish abstracts or PDFs**. Before enlarging or altering the public corpus, audit copyright/terms for the source and individual content types. For unverified rights, keep a locally processed index or link out to the authoritative publisher record. An official paper title/DOI and an independently copyrightable abstract need different treatment.

The CVPR archive uses \`choucsan/CVPR_Papers\`, whose dataset card declares MIT, and the original CVF proceedings URLs. A dataset license does not automatically change the copyright of underlying papers.

## Source comparison

| Source | Role and coverage | Current documented access | Rights / reliability gate | Action |
|---|---|---|---|---|
| [DBLP](https://dblp.org/faq/1474677.html) | Wide CS venue/year bibliography, authors, titles, publication URLs, persistent DBLP keys | XML/JSON/RDF/BibTeX and bulk XML; no login for published metadata | **CC0 metadata**. Not a reliable standalone source of abstracts, methods, dataset/code links or true track. | First source for breadth, conference/year identifiers and bibliographic deduplication; fetch targeted venue/year records or incremental snapshots |
| [OpenAlex](https://help.openalex.org/api/authentication/) | Cross-field works, topics, authors, DOI, related entities and citation graph | In 2026 basic requests can be keyless, but paging beyond first page needs a free key. Anonymous budget about **$0.10/day** and free-key budget **$1/day**, 10/s keyless and 30/s with free key; budget and rates can change. [Public snapshot](https://help.openalex.org/access/snapshot/) available without account, but roughly **750 GB** per format. | CC0 metadata. \`abstract_inverted_index\` must be reconstructed; availability varies; underlying publisher abstract/PDF rights remain separate. | Use selective DOI/work enrichment and link graph, not full snapshot for the first prototype |
| [Semantic Scholar](https://www.semanticscholar.org/product/api) | Scholarly paper graph, reference links, abstracts when available | Most public endpoints work without key but share a throttled pool; first key rate documented as 1 request/s. Separate datasets/download service. | API/data-service terms and redistribution rights need per-dataset review; abstracts can be absent. | Secondary citation/enrichment fallback, not venue acceptance authority |
| [Crossref](https://www.crossref.org/documentation/retrieve-metadata/rest-api/access-and-authentication/) | DOI identity and registered bibliographic data | No login; currently documented public **5 requests/s, concurrency 1**, polite **10 requests/s** (limits also communicated in response headers). | Public metadata, but deposited abstracts may have independent rights; DOI is not proof of acceptance track. | Stable DOI matching/normalization and targeted missing-field enrichment |
| [OpenReview](https://docs.openreview.net/how-to-guides/data-retrieval-and-modification/how-to-check-the-api-version-of-a-venue) | ML conference forum records, submissions and decisions when public | API 2 for current venues, legacy API 1 for some earlier years. Venue/API discovery and access permissions required. | Do not infer publication from a submission or public review; respect note visibility. | Official decision/track reconciliation for supported venues |
| [ACL Anthology](https://github.com/acl-org/acl-anthology) | Official computational-linguistics publications, authors and venue metadata | XML metadata in official repository; Python package | Use official ID and main/Findings/workshop distinctions; verify per-content redistribution before copying abstracts/PDFs. | First authoritative source for ACL/EMNLP/NAACL/EACL/COLING |
| [Official proceedings](https://openaccess.thecvf.com/) | Track/year truth and actual paper landing page | CVF, ECVA, PMLR, NeurIPS proceedings, AAAI proceedings, IEEE/ACM venue sites | Each publisher has distinct licenses, metadata fields and access. Link to legal PDFs instead of hosting them. | Authority for acceptance, track, paper URL, stable paper ID |
| [Hugging Face: ai-conferences](https://huggingface.co/datasets/ai-conferences) | Already used for 11 non-CVPR venues | Public versioned per-venue-year Parquet mirrors in current build | Most current cards lack declared licenses in \`catalog.json\`; treat source track labels as unverified. | Preserve existing data without rewriting, do rights review before expansion |
| [Hugging Face: papercli-papers](https://huggingface.co/datasets/GenAI4ELab/papercli-papers) | Searchable AI paper metadata, multiple venues from 2023 | Dataset card declares **CC-BY-4.0** | License on metadata compilation does **not** automatically permit republishing mirrored PDFs; verify version, source precision and attribution. | Evaluate for metadata enrichment only |
| [Hugging Face: top-conference-papers](https://huggingface.co/datasets/yufan/top-conference-papers) | 38,886 reported papers from 10 ML/NLP/IR/DM/RecSys venues over 2024–2026 | Public dataset page and per-venue configs | Explicit reuse license not confirmed at review time. | Discovery candidate, **not** a public rehosting source until rights are verified |

Crossref headers and service documentation should override historical rate-limit blog examples. OpenAlex prices and authentication changed during 2026: **do not** encode obsolete “unlimited free no-key bulk” assumptions. API keys are secrets; no key or credential may be committed or copied into user-visible pages.

## Canonical ingestion order

1. Get **conference, event year, track and official paper listing** from the publisher/proceedings or a directly attributable venue source. Use a curated manifest for one venue/year at a time; keep “not indexed”, “not held”, “unavailable”, “in progress” and “verified empty” distinct.
2. Add DBLP bibliographic IDs, DOI and author data. Normalize authoritative DOI, OpenReview and ACL Anthology IDs before attempting title/venue/year matching. Do not merge two different venue/year presentations merely because titles are similar.
3. Enrich available papers from OpenAlex, Crossref or Semantic Scholar using low-rate targeted requests. Record **field-level provenance** and retrieval/revision timestamps, not just one source label for the whole paper.
4. Respect **content-specific rights**: bibliographic facts, abstracts, PDF bodies and source code are not interchangeable. A missing or unclear license blocks adding public abstract/PDF text until resolved; official links and independently licensed bibliographic metadata can remain.
5. Write one shard per venue/year, audit duplicates, track status, abstract coverage, license declarations, source bytes and SHA-256. Use atomic replacement with a diff/back-up and keep existing CVPR hashes fixed.
6. Build facets independently: \`domain\`, \`task\`, \`method\`, \`dataset\`, \`evaluation\`, \`application\`, each with source span and origin/uncertainty. Never auto-promote a keyword hit into a validated method or novelty claim.
7. Export a compact, provenance-bearing retrieval index for assistants; return original publisher links, identify missing fields and explicitly mark unverified classifications. The archived main-venue dataset must remain usable without an LLM.

## Taxonomy and ranking

\`taxonomy.json\` is independently authored and is meant for **navigation**, not rankings. Venue names are descriptive facts. CSRankings' repository uses [CC BY-NC-ND 4.0](https://github.com/emeryberger/CSrankings/blob/gh-pages/README.md); no ranking values, code or proprietary derived datasets were imported. A venue can appear in multiple fields. Its papers do **not** automatically inherit all those field tags.

## Release gates

- Preserve all existing CVPR and non-CVPR shard hashes and counts until review.
- Confirm requested source license at the **field/content** level before adding any new public abstract or PDF body.
- Report scanned/available records, missing years, duplicate ambiguities, publication-type provenance and abstracts present vs absent.
- Verify at least five representative cross-field queries, metadata links, duplicate examples and negative “not indexed” cases.
- Test source/API budget controls and avoid new scheduled bulk download jobs until approved.
- Verify the static site works under a nested GitHub Pages path; no mandatory paid API or external JavaScript.
- Do not call lexical similarity a semantic or scientific novelty result.

## Next connector milestone

Develop an incremental source ingestion adapter for one high-value new field (proposed **Databases / SIGMOD + PVLDB** or **Operating Systems / SOSP + OSDI**) from official and CC0 metadata. Use 2022–2026 for baseline acceptance tests, then expand to 2017–2026 with measured coverage. Keep source text gated and missing metadata explicit.
