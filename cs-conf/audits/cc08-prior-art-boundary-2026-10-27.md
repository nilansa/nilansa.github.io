# CC-08 independent research-audit boundary — 27 October 2026

Task: `20261026-csconf-research`. **Status: literature and public source-structure audit; not an independent Lean replay or scientific verification.**

## 1. Closest published methods

- [FIRE-Bench, ICML 2026](https://proceedings.mlr.press/v306/wang26d.html) tests whether AI research agents rediscover verifiable published ML findings. A broad "agent-science benchmark" is already covered.
- [Artisan / Automated Table Reproduction via Code Generation, ASE 2026](https://arxiv.org/abs/2602.10046) generates executable scripts that reproduce tables. The authors report 44/60 successful scripts on 60 tasks from 23 papers, and 20 previously unknown paper/artifact errors. A generic "agent reproduces paper results" claim is already covered.
- [AI-Driven Reproducibility and Analytical Robustness, preprint dated 16 Oct 2026](https://arxiv.org/abs/2610.23845) reports an agent replay over 2,190 claims from 20 SEER-based medical papers (77.4% successful reproduction) and investigates alternative analysis choices. This overlaps atomic-claim checks and robustness analysis.
- [SciRIGOR, Sep 2026 preprint](https://arxiv.org/abs/2609.06192) describes typed evidence graphs and claim-to-result support. Generic "construct an evidence graph" is also not new.

**Novelty decision:** CC-08 should not claim that it invented autonomous artifact replay, scientific claim verification, evidence-graph checking, or rediscovery benchmarks. The remaining candidate study is narrower: **measure the gap between self-reported certificate status, independently replayable source, theorem-statement fidelity, and domain-level scientific support in genuinely unedited agent-produced research artifacts, with independent audit time counted.** Whether this gap is a novel publishable result remains untested.

## 2. New source-structure check on the pinned agent-swarm corpus

Pinned [SECQUOIA/agent-swarm-research at `paper-v1`](https://github.com/SECQUOIA/agent-swarm-research/tree/paper-v1).

Inspected `minlp-notes/paper-multilinear-gap/formal/`. Its directory lists **41 `Formal/MultilinearGap/*.lean` files and seven `Formal/CubicGap/*.lean` files**. The root `Formal.lean` imports all 48 listed modules, including the stated endpoint modules. A standalone `lean-toolchain` pins `leanprover/lean4:v4.33.1`. The checked-in `Verify.lean` appears to iterate over declarations from `Formal` modules and reject transitive axioms other than `propext`, `Classical.choice` and `Quot.sound`. The source has a `lake-manifest.json`, verification scripts, and completion/run logs.

**Evidence boundary:** This confirms existence and consistency of the import inventory and auditing *source code*. The upstream authors' `VERIFICATION.md` reports 827 declarations checked and successful kernel replay, but those are their logged results. We did **not** compile Lean, inspect every proof, independently replay the proofs, or confirm that the formal statements faithfully capture all the English claims. The previous M1 four-row arithmetic checks and M3 accounting checks are separate, non-proof sanity tests. No estimate of a failure rate is justified.

## 3. Pre-registered next test

Freeze `paper-v1`; select 12 claim–artifact pairs using a deterministic selection fixed **before reviewing the selected claims**, with strata for proof-backed, experimental, and manuscript-only artifacts. Exclude previously inspected M1 and M3 from the unbiased sample (retain them only as pilot checks). For each pair, record: immutable source/ref/hash, claim statement, stated assumptions, artifact presence, external dependencies, exact reproduction command, toolchain version, independent command output, whether the theorem formalizes the same claim, external scientific check needed, reviewer minutes, and one of `not reachable / source exists / author-reported pass / independently replayed / meaning validated`. Never infer scientific correctness from a compiler exit code alone.

**Stop/pivot:** If the sample cannot be independently replayed, publish a transparent artifact/provenance methods note without a claimed scientific failure rate. If the same provenance/semantic-fidelity test is already established in direct prior work, retire the standalone novelty claim.

## 4. Submission and integrity rule

No paper or abstract is submission-ready. A source bundle, synthetic arithmetic check, or author-reported Lean run is not evidence of accepted publication or independent proof validation. No ChatGPT-to-Codex/local file transfer was performed here; these are direct connected GitHub source reads and writes, so the Codex-owned transfer index is unchanged.
