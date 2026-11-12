# Conference Hub — Research Assistant

**Status: local CLI working for scholarly discovery and selected-source preparation; full-paper NotebookLM Q&A requires a valid NotebookLM session. The public GitHub Pages website remains a static, read-only metadata browser and has no AI chat backend.**

## What exists and what it proves

| Capability | Command / component | Evidence and limitations |
| --- | --- | --- |
| Curated collection | [Conference Hub](https://nilansa.github.io/cs-conf/hub/), 130,361 records in 12 venues | Title, author, abstract, catalog provenance; not independent main-track verification |
| Local hybrid retrieval | `tools/semantic_retrieval.py` | SQLite FTS5 BM25 + optional local BGE dense vectors + RRF; **requires separate model install and index build**; not deployed on the public web |
| Broader semantic discovery | `tools/research_assistant.py search` via **Cito** | Cito's hosted retrieval (independent third-party service, not Allen AI); 2026 corpus date/attribution returned where supplied; remote queries go to Cito |
| Academic Graph discovery | `tools/research_assistant.py search --provider semantic-scholar` | [Semantic Scholar](https://www.semanticscholar.org/product/api) is operated by Allen Institute for AI. Anonymous calls can receive HTTP 429; use a legitimate personal API key supplied as `S2_API_KEY` locally when needed, never commit keys |
| Select papers | `tools/research_assistant.py select` | Trusted HTTPS publisher URLs from the browser's **Export pins** JSON, saved as a private manifest; no PDF downloaded or uploaded |
| Source-grounded answers | `notebook-create`, `notebook-add`, `ask` via local NotebookLM CLI | Requires an authenticated account with source ingestion finished. Source identifiers are NotebookLM attribution, not guaranteed factual correctness or novelty validation |

NotebookLM integration uses [`notebooklm-py`](https://github.com/teng-lin/notebooklm-py), an **unofficial** CLI for Google's NotebookLM web interface, not a supported Google public consumer NotebookLM API. It can break if the web interface changes.

## Research workflow

1. **Discover.** Search the curated hub for proceedings, then retrieve broader candidates using Cito or Semantic Scholar. Never equate discovery results with accepted main-track papers.
2. **Select.** Pin relevant papers in the existing hub and click **Export pins**. This keeps your choices local to the browser until exported. The command below creates a local selection manifest without transmitting anything.
3. **Verify.** Open each publisher paper page, verify the work's actual venue, publication version, task definition, dataset, baselines, and date. The manifest marks peer review as unverified.
4. **Ingest only selected sources.** Use the chosen private NotebookLM profile, create a topic-specific notebook and add the selected URLs with explicit upload authorization. Verify source status in NotebookLM; a source-list row can still be processing or error.
5. **Ask exact questions.** Distinguish *direct source statements*, *abstract-level indications*, and *hypotheses*. Ask for source-linked answers that cite relevant passages. If there is not enough source material, record **not established by the supplied papers**.
6. **Test hypotheses.** Draft possible contributions, closest prior art, controlled experiment, baselines, falsification condition, expected failure modes. An assistant cannot certify novelty or acceptance.

### Command examples

Run from the site repository root; all paths in manifests should be local private paths, not checked into Git:

```sh
python3 cs-conf/hub/tools/research_assistant.py search 'temporal grounding for video question answering' --provider cito --mode semantic --limit 10
python3 cs-conf/hub/tools/research_assistant.py search 'video temporal consistency' --provider semantic-scholar --limit 10

# Export pins from the hub browser first. No source upload in this step.
python3 cs-conf/hub/tools/research_assistant.py select ~/Downloads/cs-conference-hub-pins.json \
  --topic 'Video QA · temporal evidence' \
  --output ~/Documents/video-qa-sources.json

# One-time user-run login only when authentication is missing:
# notebooklm -p default login
python3 cs-conf/hub/tools/research_assistant.py notebook-status --profile default

# Authenticated operation: first create a topic notebook and read its ID.
python3 cs-conf/hub/tools/research_assistant.py notebook-create 'Conference Hub · Video QA' --profile default

# Explicitly send ONLY these selected publisher URLs to NotebookLM.
python3 cs-conf/hub/tools/research_assistant.py notebook-add ~/Documents/video-qa-sources.json \
  --notebook-id YOUR_NOTEBOOK_ID --profile default --confirm-upload

# Inspect source list/processing status before relying on the answers:
notebooklm -p default source list --json --notebook YOUR_NOTEBOOK_ID

python3 cs-conf/hub/tools/research_assistant.py ask \
  'Which experiments on temporal grounding are explicitly reported by these sources? Quote the evidence and identify source IDs.' \
  --notebook-id YOUR_NOTEBOOK_ID --profile default
```

NotebookLM can return structured response/citation metadata as JSON. The local bridge requires at least one notebook source and retains this original response rather than inventing passages. A source existing in NotebookLM does not prove that its extraction completed, or that every citation verifies a claim; manually open cited passages. NotebookLM source quotas and service limits can change. URLs may be fetched by Google/NotebookLM when you explicitly confirm.

A selected arXiv preprint is **not** verified peer-reviewed. By default the CLI excludes preprints; both `select --allow-preprint` and `notebook-add --allow-preprint` must be supplied explicitly to permit uploading preprints. Non-publisher or untrusted hosts are not accepted.

### Example questions that produce research value

- **What has been done?** “Across the selected papers, which methods have been evaluated for event-boundary localization in VideoQA? Give a table of datasets, metrics, baselines and the exact cited sections. Write ‘not specified’ when missing.”
- **What remains unresolved?** “Which limitations are explicitly acknowledged in these papers? Which gaps are our deductions rather than statements in the literature?”
- **What can we do next?** “Propose three falsifiable changes to temporal retrieval, each linked to a prior method, a controlled baseline, a dataset, an outcome metric, and a failure criterion. Mark all proposals as UNTESTED.”
- **Does an idea already exist?** “Find the closest work, spell out exact shared and differing assumptions, and recommend a broader literature search. Do not claim novelty.”
- **Help with our draft.** “Check every claim against supplied paper citations. Separate verified quantitative numbers from unverified or missing evidence.”

## Assistant access and data policy

Agents in ChatGPT with authorized Mac terminal access can call the same local script through the existing connected computer tooling, consuming its **structured JSON**. Codex on this Mac also has the [Cito MCP endpoint](https://api.cito.fim.ai/mcp) configured (no key checked in). Claude Code may use the same documented endpoint via its own MCP configuration, without starting a separate agent loop.

The standalone semantic prototype is described in [SEMANTIC_RETRIEVAL.md](SEMANTIC_RETRIEVAL.md). Its index (SQLite + vector array) stays outside the Git repo; it is not generated by tests. Example setup:

```sh
uv venv --python 3.11 ~/.venvs/cs-conf-hub-semantic
uv pip install --python ~/.venvs/cs-conf-hub-semantic/bin/python numpy sentence-transformers
~/.venvs/cs-conf-hub-semantic/bin/python cs-conf/hub/tools/semantic_retrieval.py build
~/.venvs/cs-conf-hub-semantic/bin/python cs-conf/hub/tools/semantic_retrieval.py search 'video question answering' --venue CVPR --year 2026
```

Never sync private selected-paper lists, extracted PDFs, original manuscripts, cookies, auth profiles, API keys, or notebook conversations to the public GitHub repository. The GitHub Pages site cannot provide a secure private hosted NotebookLM session. The CLI never uploads without `--confirm-upload`, never logs keys, and returns clear errors on missing auth or provider rate limits. Browser pins remain private until the user exports them and sends an explicitly selected set to NotebookLM.

## Tests and live status

```sh
python3 -m unittest discover -s cs-conf/hub/tests
node --check cs-conf/hub/app.js
node --test cs-conf/hub/tests/test_worker.js
```

The remote Cito search endpoint was reachable on 13 November 2026. An unauthenticated Semantic Scholar request returned HTTP 429 and was correctly reported as rate-limited. NotebookLM authentication was not verified for the intended NotebookLM profile, so no notebook was created and no paper ingested or answered in that account. A source-grounded answer must be treated as **unavailable**, not simulated, until authorization and actual ingestion succeed.
