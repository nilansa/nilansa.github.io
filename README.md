# ST100 Plus Learning Library

A small static library prepared for the root of `nilansa/nilansa.github.io`. In this task scratch, the site is under `shared/site`; in the canonical repository, its HTML and assets belong at the repository root:

```text
index.html
library.json
.nojekyll
assets/
explainers/
README.md
scripts/
  add_page.py
  test_library.py
```

The public site path will be `https://nilansa.github.io/` after publication. This task has not published or pushed anything. Original GreenHome source pages remain in `shared/source/greenhome` in the scratch and are not edited or part of the public site layout.

## Preview and check

From this task scratch, serve the staged site with:

```sh
python3 -m http.server 8000 --directory shared/site
```

In the canonical repository, run `python3 -m http.server 8000` from the repository root. Open `http://localhost:8000/`; the catalog is loaded with `fetch`, so opening `index.html` as a `file://` URL will not work.

Run the standard-library tests from either layout:

```sh
python3 scripts/test_library.py
```

The test script checks catalog records and counts, hosted-page `noindex`, local links and assets, runtime dependencies, privacy markers, and safe page intake. For JavaScript syntax, use `node --check shared/site/assets/app.js` in this task scratch or `node --check assets/app.js` in the canonical repository.

## Add one approved public page

Review and approve one HTML file and its contents first. Intake is explicit: the script reads only the named file and never scans or imports a directory. It adds the page under `explainers/<project>/` and one record to `library.json`. It does not publish private files, edit the supplied source, replace an existing destination, or overwrite an existing catalog ID. If a destination already exists, choose a different ID or resolve the conflict manually after review.

```sh
python3 scripts/add_page.py path/to/approved.html \
  --id insulation-guide \
  --title "Insulation guide" \
  --description "A short, source-grounded guide to insulation choices." \
  --project GreenHome \
  --category "Product & practice" \
  --tags retrofit insulation evidence
python3 scripts/test_library.py
```

The HTML must have a document title and be self-contained. Any local linked files must already exist at their corresponding site paths. Remote scripts, stylesheets, fonts, and other remote assets are rejected; ordinary external links are allowed. Intake adds a `noindex` robots directive.

## Commit and publish

From the canonical repository root, review the exact changes and stage only the intended site, documentation, and script files. Do not add the task scratch, transfer index, source files, or private material.

If a destination path already exists in the canonical repository, compare and resolve it deliberately before copying anything; do not replace a pre-existing page or source. Stage only reviewed paths, rather than whole directories that may contain unrelated files.

```sh
git status --short
git diff --check
git add -- .nojekyll index.html library.json README.md scripts/add_page.py scripts/test_library.py \
  assets/app.js assets/style.css \
  explainers/greenhome/assets/app.js explainers/greenhome/assets/style.css \
  explainers/greenhome/index.html explainers/greenhome/index-st100-v1.html \
  explainers/greenhome/01-dataset.html explainers/greenhome/02-models.html \
  explainers/greenhome/03-engine.html explainers/greenhome/04-llm.html \
  explainers/greenhome/05-demo.html explainers/greenhome/06-judges.html \
  explainers/greenhome/07-roadmap.html explainers/greenhome/08-retrofit-pipeline-st100plus.html
git diff --cached --stat
git diff --cached
git commit -m "Update ST100 Plus learning library"
git push origin HEAD
```

Publishing makes these pages publicly reachable at the site URL. `noindex` asks compliant search crawlers not to index a page; it is not privacy, authentication, or access control. Anyone who has a public page URL may be able to view it. Do not add private content, raw data, credentials, PDFs, or team-only documents.
