# BookHub

Book-centered research workbench for the existing Books catalog and CS Conference Research Hub.

**Published website:** https://nilansa.github.io/books/hub/

**Formal architecture and evaluated learning/research tools:** [RESEARCH.md](./RESEARCH.md).

## What runs today (2026-11-13)

- Responsive, static A24-inspired site: `index.html`, `hub.css`, `hub.js`.
- Reads `../books.json` (canonical 22-book catalog) and `atlas.json` (curated concept graph); nothing is copied from private PDF bodies into the public repository.
- Lexical search over books, verified chapter headings, curated concept descriptions, and previously pinned ConfHub papers from the same browser origin.
- Concept map with verified *book/chapter source associations* and **editorially curated** learning relationships. Edges are NOT claims of empirical validation, novelty, or historical priority.
- Separate, locally persisted workspaces with notes, collections, export/import of JSON, and a Markdown brief for an external agent.
- A self-assessed active-recall queue for saved concepts. Answer a diagnostic question, check the source, then mark needs work (review tomorrow) or explained-and-checked (review in seven days). Dates are **simple reminders**, not automated grading or a validated spaced repetition scheduler.
- Bidirectional search handoff: BookHub concepts link to ConfHub `?q=` and the ConfHub search box offers to search the same query in BookHub. Each search engine retains its own scope.
- Entry points from /books/, /personal-links/, and /cs-conf/hub/. /PERSONAL_LINKS.md is synchronized.

## Intended architecture

```
                          PUBLIC / STATIC
 Books catalog (books.json) -----> BookHub <----- Curated atlas (atlas.json)
                                       |
            concept → chapter → book    |    concept → ConfHub search
                                       |
                         per-browser research desks
                           (localStorage, JSON export)
                                       |
                user-initiated copy study brief to any agent

                          PRIVATE / NOT IN GITHUB
       Original copyrighted PDFs in authorized Google Drive
        private local structural extraction and citations (future)
            personal/agent research notes and fulltext indices
```

**Canonical source** of book metadata remains `books/books.json`. Do not maintain a divergent list in BookHub.

### BookHub data model

| Entity | Identity | Evidence |
| --- | --- | --- |
| Book | `book:<slug>` | Catalog record, publisher link, authorized Drive file link |
| Chapter | `chapter:<id>` | Transcribed contents heading and printed book page (when verified) |
| Concept | `concept:<id>` | Editorial learning definition and diagnostic question |
| Pinned paper | `paper:<id>` | ConfHub browser pin; paper source URL |
| Concept edge | `from,to,relation` | Curated study relation; not automatically inferred or validated |
| Workspace | local `id` | User notes and saved IDs, stored per browser |

Relationships among concepts are not the same as a citation graph or experimental dependency graph; source provenance must be maintained. A question such as "How did an idea develop?" needs explicit paper citations before an edge can be promoted to an evidence-backed historical claim.

### Source anthology

Confirmed from the **tables of contents in the connected private Drive PDFs** (source file bodies are not published):

1. Michael S. Lew (ed.), *Principles of Visual Information Retrieval* (2001).
2. A. Rosenfeld, D. Doermann and D. DeMenthon (eds.), *Video Mining* (2003).
3. Q. Wu et al., *Visual Question Answering: From Theory to Application* (2022).

`atlas.json` holds a **starter selection** of 23 chapter records, 14 concepts and 18 links, not a complete chapter-by-chapter annotation of all 22 books. Printed page numbers may differ from PDF page positions; null means unverified. Summaries and questions are newly written, not copied.

## Why this shape (trade-offs)

| Option | Strength | Limit | Role |
| --- | --- | --- | --- |
| NotebookLM / Gemini study notebooks | Source-grounded explanations, study artifacts, adaptive practice | Provider-specific notebooks; not the canonical, version-controlled cross-domain graph | Optional learning and quiz layer |
| Claude Projects | Flexible project knowledge with optional automatic RAG | Vendor-hosted knowledge, version/portability and quota constraints | Optional agent reasoning workspace |
| Zotero | Durable bibliographic metadata, citations and PDF annotations | No built-in automated research graph with the requested ConfHub connection | Future citation/annotation backbone |
| GROBID / Docling | Local structured parsing of PDFs into sections/tables/references | Extraction noise, especially scanned books and complex typography | Future private ingestion |
| Custom BookHub | Unified schema, own design, auditable links, flexible export and ConfHub navigation | Engineering maintenance, no built-in general AI or hosted sync | Canonical frontend / knowledge map |

**Research principle:** source extraction → verifiable locations → semantic indexing → explicit graph relations → uncertainty annotation → testing. Do not let an LLM silently substitute generated relationships for evidence.

## Browser-only storage, privacy and limitations

- This GitHub Pages website is **public**. No private PDFs, personal research notes, or secrets should be committed to it.
- Local workspaces and pins use browser `localStorage`. This is not encrypted storage, user login, or cross-device sync; browser cleanup or private mode can delete them. Export JSON frequently; import is available.
- Study brief copy and JSON exports are initiated by the reader. A shared browser should not hold confidential notes.
- Google Drive links point to files in the user's authorized account. A link does not grant public access.
- `robots.txt` and `noindex` are courtesy requests, **not access control**.
- Search is **lexical**, not OCR, semantic embedding/RAG, PDF full-text search, or a 130k-paper federated index. ConfHub uses its own archive search.
- ConfHub pins are accessible only on the same browser origin/device. If stored in another browser, export/import is needed or papers must be pinned again there.
- Graph edges are editorial, and citation-grade source extraction must precede factual claims.
- The domain model is non-exhaustive and will need richer hierarchy: formal prerequisite, analogy, competing definitions, supporting/contradicting evidence, historical lineage, and explicit unknowns.

## Next engineering milestones (not implemented)

1. Private ingest from authorized Drive using a controlled local worker. SHA-256, provenance, page-layout extraction (PyMuPDF/GROBID/Docling), per-page references, de-duplication, and citation validation.
2. Search index combining exact text (BM25), embeddings and source-level reranking; measure retrieval with a human-labeled evaluation set.
3. Versioned knowledge graph with typed, evidence-backed edges and contradiction tracking. Require a source location on all claims.
4. Protected, opt-in multi-device workspace synchronization; never store private full text in this public Pages repo.
5. Read-only MCP tools for agents: `search_books`, `list_chapters`, `explain_concept_with_sources`, `neighbor_concepts`, `related_confhub_papers`. Do not label a tool as installed until tested.
6. Improve the basic self-rated review reminders into a well-tested spaced-retrieval schedule with optional private source-grounded answer keys and conceptual transfer questions. No model-generated answer should count as established fact without source verification.

## QA checklist

- Public page and atlas JSON resolve to 200.
- Browser console shows no JS exceptions; 22 books, 23 chapters, 14 concepts display.
- Search for `video`; switch to Chapters and Concepts.
- Select **Video representations** node and verify chapter source links.
- Add a concept to a workspace, edit notes, reload, and verify persistence; export/import a test workspace.
- Open an active recall question, self-rate it and confirm the next review date persists across reload.
- Follow the ConfHub search from a concept (pre-filled query).
- Verify links in /books/, /personal-links/ and ConfHub.
- Test on mobile and keyboard-only access.

## Maintenance

When modifying the public page, keep `PERSONAL_LINKS.md` and `personal-links/index.html` synchronized. Preserve the Books six-shelf taxonomy and the existing ConfHub design/metadata. Any source parsing or AI synthesis of private PDFs must happen in an authorized private backend, not in GitHub Pages.
