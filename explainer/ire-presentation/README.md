# IRE presentation

**Frozen models. Better retrieval?**

Test-time retrieval with black-box reranker feedback and no model weight updates.

Queos Labs · Nilanjan Sarkar and Raman Rayaprolu · IIIT Hyderabad

## Present

Open `index.html` from this directory on a static web server or GitHub Pages. The deck has 20 pages and approximately 20 minutes of narration. All runtime assets are local; no model call, analytics, remote font or third-party script is required.

| Control | Action |
|---|---|
| Left / Right arrow | Previous / next page |
| Space | Next page |
| Home / End | First / last page |
| N | Speaker notes with pointer cues |
| S | Sentence-level sources |
| O | Page overview |
| F | Full screen |
| Escape | Close an open panel |
| Presenter | Open a separate synchronized speaker window |

The page selector and buttons provide the same navigation. Add `?page=11` to start at a particular page, or `?presenter=1&page=11` to open its speaker view. The presenter view includes a timer, the full script, pointer notes and the next page title. Keyboard shortcuts do not override typing in fields.

Two figures are interactive: the KL explanation on page 9 and the marginal-coverage example on page 17. Their numbers are original teaching examples, explicitly labelled as illustrations.

## Read and revise

- `PRESENTATION_SCRIPT.md`: complete narration, pointing cues, technical notes and sentence provenance.
- `SOURCE_LEDGER.md`: source register, 158-sentence provenance ledger, exact locations, equations and claim boundaries.
- `SOURCE_LEDGER.csv`: the same sentence ledger in an Excel-compatible table.
- `content.json` and `content.js`: structured content. The website loads `content.js` without a network fetch.
- `visuals.js`: exact published/project values and original SVG/HTML teaching diagrams.
- `styles.css`, `app.js`, `index.html`: visual presentation and navigation.

The source-controlled authoring script is in `authoring/build_content.py`. From the presentation directory, regenerate content with:

```sh
python3 authoring/build_content.py --output .
```

The authoring script enforces 120–130 narrated words per page and validates source references. Recheck the diagram and script together whenever a value or method description changes. No learning algorithm is implemented or run by this website.

## Evidence snapshot

Published plots identify their paper and table. The SCIDOCS plot uses the completed-run reports linked in the ledger. The reported raw and direct-reranking results match the paper references at displayed precision; the ReFIT attempt leaves an unresolved reproduction gap. Recorded headline settings match ReFIT v2. The raw predictions were not recomputed during preparation of this deck.

TTT-Embed and complementary-feedback numerical outcomes are **not verified in this edition**. This is not a claim that no separate run exists. Page 16 is the explicit evidence boundary. Update it only with a concrete run record.

## Updating results

Record the run ID, corpus and model revisions, query IDs, score normalization, teacher budget, scope, optimizer, full-corpus search, paired metrics and uncertainty. Include source artifact hashes and a canonical result URL. Preserve the previous result and its provenance. Then update the authoring script, `visuals.js` if needed, and the source ledger together. Do not turn a pilot into a claimed full-paper reproduction.

The website deliberately includes only final presentation assets and public-safe source references. It does not contain private scratch data or remote-machine credentials.
