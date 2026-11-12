# Local semantic retrieval prototype

This optional Python CLI searches the hub's checked-in `catalog.json` and JSON shards. It does not change the static site or the Node API. The SQLite index and vector file stay in a local cache outside the repository.

## Install the optional tools

The CLI uses only Python's standard library for metadata indexing, FTS5, and tests. A real build or search needs NumPy and Sentence Transformers. PDF draft comparison also needs PyMuPDF. Install them only in an isolated environment:

```sh
uv venv --python 3.11 ~/.venvs/cs-conf-hub-semantic
uv pip install --python ~/.venvs/cs-conf-hub-semantic/bin/python numpy sentence-transformers
# Optional, only for PDF drafts:
uv pip install --python ~/.venvs/cs-conf-hub-semantic/bin/python pymupdf
```

The app never installs packages. If the model is not in the local Hugging Face cache, only the explicit `build` command can fetch its weights. `search` and `compare` use cached weights in offline mode.

## Build and search

Run commands from the repository root. Build once to create the local index from the catalog and all available checked-in venue/year shards:

```sh
~/.venvs/cs-conf-hub-semantic/bin/python cs-conf/hub/tools/semantic_retrieval.py build
```

The build verifies each shard's catalog count, size, and SHA-256. It writes to `~/Library/Caches/cs-conference-hub/semantic-index/` on macOS. It stores one SQLite FTS5 corpus, one row-aligned `.npy` float16 vector matrix, and a provenance manifest. A rebuild requires `--rebuild`; staged files replace the previous index only after the new index is complete. Use `--index-dir PATH` or `CS_CONF_HUB_INDEX_DIR` to choose another local path outside the repository.

Search accepts natural language and repeated venue/year filters:

```sh
~/.venvs/cs-conf-hub-semantic/bin/python cs-conf/hub/tools/semantic_retrieval.py search 'robot planning with language models' --venue ACL --venue NeurIPS --year 2024 --year 2025 --limit 10
```

SQLite FTS5 ranks the complete indexed corpus, so inverse document frequency is shared across all venue shards. BM25 weights title, author, and abstract text as 8:4:1. The author field also gets a phrase match for an author-like query. Dense ranking computes cosine against every row that passes the selected filters, in exact dot-product blocks; there is no ANN index. Reciprocal rank fusion uses `1/(60 + rank)` for each of the BM25 and dense lists. Results show the filtered BM25 rank, dense cosine, fused rank, paper URL, and shard source URL. “Abstract unavailable” marks title-only metadata.

The BGE query instruction follows the [official model card](https://huggingface.co/BAAI/bge-small-en-v1.5). Stored paper vectors use title plus abstract; papers without an abstract use title only. The manifest records the model revision, catalog and shard hashes, build time, vector layout, and index file hashes.

## Compare a draft locally

```sh
~/.venvs/cs-conf-hub-semantic/bin/python cs-conf/hub/tools/semantic_retrieval.py compare --draft ~/Documents/draft.md --limit 10
~/.venvs/cs-conf-hub-semantic/bin/python cs-conf/hub/tools/semantic_retrieval.py compare --draft ~/Documents/draft.pdf --limit 10
```

Text and Markdown are read as UTF-8. PDF text is extracted locally by optional PyMuPDF. The CLI splits the draft into 180-word chunks with 40 words of overlap, embeds each chunk, and averages the normalized chunk vectors into a document representation. It compares that representation and each chunk with the archive's title-plus-abstract vectors, then shows related records and each record's strongest matching draft chunk. It never uploads or saves the draft or its extracted text.

The archive contains metadata and abstracts, not complete papers or PDFs. These results are metadata-to-draft similarity signals. They are not full-paper-to-full-paper novelty detection, a confidence score, or proof that an idea is novel or already published. Raw cosine values are uncalibrated; do not use a numeric cutoff as a decision rule. A missing archive abstract means its vector represents only the title.

## Disk, memory, and limits

The checked-in catalog lists 130,361 records. A 384-dimensional float16 matrix for that corpus is 95.48 MiB on disk. Search memory-maps it and computes dense scores in 8,192-row blocks (about 12 MiB for each float32 block); SQLite and Python also hold candidate IDs and scores. Build reads one JSON shard at a time and embeds batches of 64. The CPU model and framework add several hundred MiB or more, depending on installed versions. Plan for roughly 0.5–1.5 GiB peak memory during a build; measure on the target Mac before a full build.

The current corpus is metadata only. Abstracts longer than the model's input limit may be truncated by Sentence Transformers. The local prototype does not download the corpus, fetch papers, create a UI control, or modify GitHub Pages. Search quality still needs evaluation on real queries and judgments before anyone treats it as production retrieval.

## Safe validation

The tests use small synthetic shards and a deterministic fake embedder. They do not download the corpus or model weights:

```sh
python3 -m unittest discover -s cs-conf/hub/tests
```

This checks FTS5 indexing, BM25/dense/RRF ranking, repeated filters, chunk overlap, missing abstracts, local PDF dependency errors, comparison output, and that a failed staged rebuild leaves the previous index intact. No 130,000-paper encoding is part of the tests.
