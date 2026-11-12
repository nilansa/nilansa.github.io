# BookHub research specification — 13 November 2026

This document preserves the product reasoning behind the current executable [BookHub](https://nilansa.github.io/books/hub/). It is a *design record*, not a claim that all features are implemented.

## Goal

A reader asks **“Help me understand video question answering, its roots in video retrieval, and its open scientific questions.”**

A good system should return a navigable **learning route** and an evidence packet—not a plausible but unverifiable synthesis. The user needs (1) classic textbook foundations, (2) the concrete chapter locations to read, (3) definitions and connections, (4) modern conference-paper evidence, (5) useful tests of understanding, (6) a persistent research desk, and (7) a portable, agent-readable record.

### Canonical user journeys

| Journey | Steps | Outcome |
| --- | --- | --- |
| Discover | Topic → books → verified chapters → related concepts | A reading path rather than undifferentiated PDF search results |
| Understand | Ask a question → answer from memory → check original chapter → record uncertainty | Recognized gaps and retained knowledge |
| Compare | Classical concept → ConfHub query → published contemporary papers | Claims separated by era and methodology |
| Investigate | Save sources → state hypothesis → identify a plausible counterexample → define measurable experiment | A research agenda, *not* a novelty guarantee |
| Continue | Export JSON + copy Markdown brief → agent independently reopens sources | Transferable context instead of a single uninspectable chat |

## Layer model

| Layer | Node types | Primary storage | Status |
| --- | --- | --- | --- |
| L0: Library | Book, author, publisher, edition, file pointer | `books/books.json` | Live: 22 books |
| L1: Structure | Part, chapter, section, figure, theorem, exercise, source page | `books/hub/atlas.json` starter | Partial: 23 indexed chapter entries |
| L2: Curriculum | Concept, learning question, reading route, self-rating | Atlas + browser workspace | Live: 14 editorial concepts, basic review queue |
| L3: Evidence graph | paper, claim, experiment, method, limitation, dataset, metric, supporting source span | Versioned private graph | Not implemented |
| L4: Learning agent | grounded answer, Socratic hint, quiz with verified answer, misconception diagnosis | Authorized model + private context | Not implemented; user can copy study brief |
| L5: Agent interface | search, list chapters, graph neighborhoods, source-backed answers, workspace read/write | Read-only MCP/API + opt-in private state | Not installed |

All cross-document connections need epistemic labels. **Being adjacent in a concept graph never means causal influence, paper dependency, or a verified experimental result.**

### Future structured graph edge

```json
{
  "from": "concept:temporal-boundaries",
  "to": "paper:<persistent-id>",
  "relation": "defined_in | extends | contrasts | evaluated_in | prerequisite_of",
  "source": {
    "type": "book | paper",
    "id": "<source-id>",
    "page_or_section": "<verified-location>",
    "extract_sha256": "<hash-of-source-span>"
  },
  "epistemic_status": "direct_source | reviewer_annotation | model_candidate | contradicted",
  "reviewed_by": "human | verified_extractor | not_reviewed",
  "last_checked": "YYYY-MM-DD"
}
```

A model-produced *candidate* edge is **not promoted to direct source evidence** without checking the relevant source. When comparing old and new work, annotate whether the older concept is (a) a general mathematical principle, (b) a method with assumptions, (c) an obsolete implementation, or (d) a still-open problem.

## Existing products and research worth borrowing

The best solution is not to copy one vendor's UI. Each component solves a different problem.

| Tool / research | Borrow this | Main benefit | Limitation / integration choice |
| --- | --- | --- | --- |
| **Google Research — Learn Your Way** (2025) | Transform textbooks into multiple representations, adjustable level, visual maps, self-checks | Learning from a *source* rather than merely generating summaries | Experimental product; Google's reported efficacy finding is product-reported. Keep canonical catalog/graph independent |
| **Google Gemini Guided Learning / LearnLM** (2025–26) | Ask follow-up questions, guide step by step, adapt depth | Promotes active work instead of instant answers | Model cannot independently guarantee source correctness; tie every claim to a chapter |
| **Gemini / NotebookLM notebooks** (2026) | Source-centric notebooks, citations, flashcards, study guides, diagnostic quizzes | Strong companion for privately uploaded authorized books | Provider quotas, product boundaries, account-specific support; do not treat its private library as automatically accessible via BookHub |
| **Anthropic Claude for Education — Learning mode** (2025) | Socratic questioning, ask for supporting evidence | Promotes independent reasoning | Product availability varies; separate generic Claude Projects from institutional Learning mode |
| **Claude Projects** (2026) | Per-topic project context and RAG when large | Agent reasoning across a constrained corpus | Hosted knowledge is not a canonical, provenance-verified graph |
| **Zotero** | Bibliographic management, native PDF annotations, citation-linked notes | Durable human-verified evidence and return-to-page links | Requires integration and a strategy for book citation structures |
| **GROBID / Docling** | Parse PDFs into structured text, document hierarchy, tables | Builds citation-grade private ingestion | Scans, OCR, book TOCs, formulas and page offsets can be wrong; benchmark first |
| **Pre-LLM learning science** | Practice testing and distributed practice, self-explanation | Evidence-backed learning mechanics independent of model | Review schedules must be tested, not conflated with correct answers |

**Sources:** [Google Learn Your Way](https://blog.google/products-and-platforms/products/education/learn-your-way/); [Google Guided Learning](https://blog.google/products-and-platforms/products/education/guided-learning/); [Gemini study notebooks](https://blog.google/innovation-and-ai/products/gemini-app/gemini-study-notebooks/); [Gemini textbook additions](https://blog.google/innovation-and-ai/products/gemini-notebook/new-access-textbooks/); [Claude Learning mode](https://www.anthropic.com/news/introducing-claude-for-education); [Claude Projects](https://support.claude.com/en/articles/9517075-what-are-projects); [Zotero PDF reader](https://www.zotero.org/support/pdf_reader); [GROBID](https://github.com/grobidOrg/grobid); [Dunlosky et al. 2013](https://www.psychologicalscience.org/journals/pspi/1529100612453266/). Access confirmed November 2026.

### Why active recall and spacing

Dunlosky et al. (2013) reviewed ten learning strategies. Practice testing and distributed practice earned the highest utility assessments; self-explanation was rated moderate. This motivated **basic, self-rated** active recall in BookHub's current reading desk. "Needs another pass" schedules tomorrow; "Explained and checked" schedules seven days later. **These are product defaults, not an evidence-validated spaced repetition algorithm and not automatic verification of mastery.** A proper adaptive scheduler should be benchmarked and allow users to override the date.

## Detailed execution status

### Deployed and smoke-tested

- `/books/hub/` public static site, off-white editorial style, responsive layout, no external scripts
- Source-grounded chapter headings from three books and a 14-node editorial map
- Search and filter by books, chapters, concepts, current-browser pinned ConfHub papers
- Interactive map inspection; private Drive source links where authorization permits
- Named research desks, notes, locally persisted stacks, JSON import/export and agent brief
- Two-way query transfer between BookHub and ConfHub
- Active recall queue and self-ratings (implemented after initial smoke test; JavaScript syntax verified)
- Linked from Books, Personal links and ConfHub
- GitHub Pages and `atlas.json` confirmed reachable; initial live browser test passed search, concept inspection and stack persistence

### Still needs evidence before calling production-complete

- End-to-end browser re-test of newly added self-rating dates and ConfHub-to-BookHub query links
- Actual note persistence on page reload, plus import/export round-trip
- Real private source ingestion and page-level citations for every indexed concept
- Search quality benchmark against a representative human-labeled question set
- Private authenticated sync between devices
- Executable installed MCP server for ChatGPT, Codex and Claude
- Accessibility testing (mobile, screen reader, keyboard) and error telemetry without collecting user notes

## How an agent should use the current data today

1. Use the connected GitHub source files `books/books.json` and `books/hub/atlas.json` for lookup of book and chapter metadata.
2. Use an authorized connected Google Drive read of a book only when necessary; never assume page offsets match printed pagination.
3. Use the ConfHub paper corpus for paper metadata and abstracts, then open publisher or proceedings source before making detailed claims.
4. Produce: **concept → foundational source(s) → modern paper(s) → comparison → unresolved assumption → testable question**.
5. Distinguish (1) directly quoted or verified source details, (2) inference, (3) untested speculation. Export user work only on explicit request.

Never publicly expose original copyrighted PDF bodies, confidential notes, credentials, internal research content or private Drive folder listings.

## Quality gates for the next iteration

- Every answerable reading question must point to at least one exact source identifier and passage/page.
- Baseline retrieval benchmark for chapter lookup (keyword + BM25), followed by hybrid semantic search with reranking. Compare Recall@5/10, MRR, and citation accuracy against held-out annotations.
- The concept graph should distinguish **requires**, **similar-to**, **extends**, **contradicts**, **used-by**, **evaluated-on**, and **unknown relationship**.
- Every error or wrong suggestion should become a reusable regression case.
- Copying research desk JSON to an agent is an explicit user action; never silently transmit notes or PDFs to third-party providers.
