# IRE end-sem exam lab — independent study edition (20 Nov 2026)

Source-first static website for CS4.406.

- 69 original self-contained topic pages under `topics/`.
- 118 original multiple-choice questions + 69 viva/short-answer prompts.
- Three interactive 30-question mock sets from the same question bank.
- Source-specific scope, 2026 theory-key reasoning, and explicit distinction from the 2025 sample.
- No accounts, cookies, analytics, third-party assets, external JavaScript, or backend.
- No copied full course PDFs included. Instructor-only materials are cited by filename/page but not republished.
- LocalStorage saves checked lessons and optionally missed questions *on your device only*.
- The title pages have `noindex` meta tags until publication/visibility is decided.

## Run locally

`python3 -m http.server 8765 --directory site` then open http://localhost:8765/

## Caveats

- Only the final syllabus top-level areas are confirmed: Quiz-2 material, ranking, A/B testing. Detailed A/B experimental designs beyond Goodman's linked reading are learning extensions, **not** a guaranteed exam blueprint.
- The no-numerics announcement was for Quiz-2 specifically.
- The original Quiz-1 had individualized assignment work; this site covers its general theory answers only.
- Questions here are original mock material and must not be misrepresented as past or future examination questions.

Run `python3 test_site.py` from this builder folder for structural tests.
