# CVPR Research Hypothesis Hub

A static, no-build-tools paper search and hypothesis workbench for CVPR metadata from 2022 through 2026. It uses plain HTML, CSS, JavaScript, Web Workers, and Python's standard library. There is no server component, JavaScript CDN, external font, or PDF download.

## Use the site

Serve this directory as static files. For example, from the repository root:

```sh
python3 -m http.server 8000 --directory cs-conf/hub
```

Open the server's root page. The browser fetches a year file only after a search starts. A Web Worker builds a lexical inverted index and ranks title, author, and abstract matches. The ranking uses BM25-style term weights, a title boost, exact phrase boosts, and adjacent-word boosts. Topic clusters are keyword rules and are for discovery only.

Paper pins and imported pin files stay in this browser's local storage. Search text and Idea Lab packets are not sent anywhere. Use Export pins to save a local JSON copy. Do not put private notes in this public repository.

## Build and validate metadata

The ingester downloads the five JSONL metadata files and one official proceedings HTML listing per year. It uses the listings to match paper titles to CVF's original paper and PDF links. It never downloads a paper PDF.

```sh
python3 cs-conf/hub/tools/build_cvpr_hub.py
```

The script checks each record's year path, title and authors, abstract presence, duplicate title/author key, and safe CVF PDF URL. It matches title records to the official CVF year listing, then uses the listing's paper and PDF URLs where it finds a match. The current source has six records with a null abstract (three in 2022 and three in 2024). It keeps these records, marks the abstract as unavailable, and prevents them from being used as Idea Lab evidence. It writes compact year files and `provenance.json`, which records source and output byte counts, SHA256 values, record counts, CVF listing match counts, repaired-link counts, validation counts, and track signals. The checksums below are from the checked-in generated files, not estimates.

### Corpus snapshot

| Year | Records | File bytes | SHA256 |
|---|---:|---:|---|
| 2022 | 2,074 | 4,300,265 | `e64495c6c1564b0e5d46fbfd6adcb7cad067a1ca95c7142780b123c75a499399` |
| 2023 | 2,353 | 4,949,638 | `bf2d6a05fd2a4b62fbb73332bbab95e3464a3b6319dcd90b9b1df12695895d7e` |
| 2024 | 2,716 | 5,744,772 | `5cbf968a8a4d576e634bca1c7e3cc10df60d82b31f5bd51a5e14c8b94d12b94a` |
| 2025 | 2,871 | 6,222,618 | `6d405e18a90ec8f36043fa64bda2eba9eadc2b469a70fb1f9126cfd269ead3c5` |
| 2026 | 4,069 | 9,014,661 | `a943a072385222f9ed9e1abfb04aa109bd688f7e4c7ea0c329740681bf841695` |

`provenance.json` is the source of truth for those values. The page displays the same counts and hashes. The corpus total is stored there.

## Search from a terminal

The CLI reads the same checked-in JSON files and does not need a network connection:

```sh
python3 cs-conf/hub/tools/search_cvpr.py "open vocabulary detection" --years 2024,2025 --limit 8
python3 cs-conf/hub/tools/search_cvpr.py '"3D reconstruction"' --year 2026 --json
```

It searches title, author, and abstract fields. A title match ranks above an otherwise similar abstract match. Exact phrases and adjacent query words receive a boost. `--year` can be repeated; `--years` accepts a comma-separated list. `--json` returns full paper records and scores.

## Inspect papers and propose a hypothesis

1. Search a concrete problem, method, or task term in the site or CLI. Open the original CVF paper page and PDF. Read the full paper, including its method, evaluation, limitations, and references. Abstracts alone are not evidence of a result.
2. Check the CVF page and BibTeX for the publication track. The dataset's `CVPR` label alone does not verify a main-track acceptance. If the source does not confirm a track, the hub labels it **CVPR main candidate**.
3. In Idea Lab, select a problem paper and a method paper from different keyword clusters. Read the extracted sentences in context. The extraction uses simple sentence patterns; it is not an LLM summary and can miss limitations or contributions.
4. Treat the output as an **UNTESTED hypothesis**. Choose and cite a strong, task-matched public baseline before a test. Keep the data split, inputs, training budget, compute budget, and metric matched. State in advance what result would falsify the idea. The hub invents no baselines or results.
5. Search related work and inspect both papers before claiming novelty. A combination of two papers does not prove novelty. Historical acceptance does not guarantee future acceptance.

Example terminal workflow:

```sh
python3 cs-conf/hub/tools/search_cvpr.py "domain adaptation segmentation" --years 2023,2024,2025 --limit 12 --json
```

Open the returned `cvf_url` and `pdf_url` yourself to inspect source papers. This CLI does not download or parse PDFs.

## Attribution and limits

Metadata and abstracts are derived from the [CVPR_Papers dataset](https://huggingface.co/datasets/choucsan/CVPR_Papers), whose dataset card lists an MIT license. The dataset credits Zhishan Zou and identifies CVF Open Access as its source. Paper and PDF references point to the [Computer Vision Foundation Open Access repository](https://openaccess.thecvf.com/). CVF states that paper rights remain with authors or other rights holders. This site stores metadata and abstracts only; it does not redistribute PDFs.

The source dataset can change. Re-run the ingester to refresh it; each run updates the source and output hashes in `provenance.json`. Topic labels are keyword-derived. Track statements are limited to explicit CVF URL or BibTeX signals. A paper listed here is not a guarantee of acceptance for future work.

## Checks recorded for this snapshot

Observed results for the current checked-in snapshot (no estimates):

- Corpus: 14,083 records across five years; six source records have no abstract (three in 2022 and three in 2024). All six remain searchable by title and authors and are marked in the UI.
- Corpus byte counts and SHA256: generated and recorded in `provenance.json`; the data file bytes are listed above.
- Python unit tests, Node syntax checks, CLI query, and local static HTTP fetch: results are recorded after the final verification pass.
- Estimated file sizes: none are presented as measured values.
