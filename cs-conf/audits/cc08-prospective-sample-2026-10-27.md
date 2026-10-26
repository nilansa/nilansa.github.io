# CC-08 — prospective source-audit pilot (27 October 2026)

Task: `20261026-csconf-research`. Scope: research protocol and public source facts only. **No independent Lean compilation, semantic correctness verdict, corpus failure-rate estimate, or paper acceptance is claimed.** Detailed working judgments stay in the private CS Conf discussion.

## The claim and the research gap

Existing work on research-agent reproduction (FIRE-Bench, Artisan, SEER-Repro and SciRIGOR) already covers independent reproduction and claim-to-evidence auditing. More directly, [Beyond Compilation: Evaluating Faithful Natural-Language-to-Lean Statement Formalization](https://arxiv.org/abs/2606.31002) measures the gap between successful Lean compilation and faithful expression of the intended theorem. **Do not claim either idea as novel.**

Our narrower pilot asks whether **self-reported verification status, a pinned source revision, actual independently replayable artifacts, and the manuscript's precise assumptions** remain connected across a released body of *unedited research-agent output*. The potential contribution would be a transparent provenance-and-auditor-cost protocol applied to real autonomous research records, rather than a generic Lean formalizer benchmark. The novelty and its external validity remain uncertain.

## Frozen sample, before case inspection

- Corpus: [SECQUOIA/agent-swarm-research at `paper-v1`](https://github.com/SECQUOIA/agent-swarm-research/tree/paper-v1), inventory `README.md` Git blob `0c03c238501704b48402a377bcbd49d29ad18fdf`.
- Inventory: 53 **research entries**, of which 45 are paper candidates and eight are experimental-program proposals. An entry is **not** necessarily an independent manuscript or one research claim.
- Exclude the two previous convenience examples, M1 and M3, before drawing the prospective sample. Four strata are the repository authors' **self-reported** Lean labels: Done, Partial, Possible, Not applicable.
- Sort each eligible stratum by ascending hex SHA-256 of UTF-8 `CC08-20261027-audit-v1|<ID>`. Break ties by ID. Choose the first three. This is a deterministic stratified **research-entry sample**, not an unbiased sample of all atomic claims. The Done stratum has only three eligible items after exclusions.

| Upstream Lean-status stratum | Locked entries |
|---|---|
| Done | M15, M2, Q11 |
| Partial | Q10, Q2, Q1 |
| Possible | M22, M19, Q4 |
| Not applicable | M18, CA2, CA5 |

**Selection was timestamp-locked in the private research decision issue before selected manuscript/proof contents were opened.** Do not replace inaccessible cases with easier ones.

## Predeclared audit unit and decisions

For each entry, take the first main numbered theorem or explicit central claim in its *own* manuscript/section. If none exists, take its first precise, externally checkable assertion in the named notes/program section. If no attributable assertion is available, record it as **inaccessible**. Flag shared summary PDFs as clustered entries, not independent manuscripts. The reviewer must record the exact statement, all premises, source commit/blob, toolchain/dependencies, attempted command, checker output, and time spent.

Record separate evidence levels: E0 author/meta assertion; E1 identified original source bytes; E2 author-reported verification; E3 independent clean replay on the matching version; E4 fidelity between formal or executable test and precise manuscript claim; E5 independent domain/data validation. **E3 does not entail E4 or E5.** Entries marked Not applicable must be assessed against their relevant empirical or theoretical evidence, not penalized for lacking Lean.

Report missing and inaccessible items, stratum-specific descriptive totals, and human audit cost. A 12-entry heterogeneous pilot must not become a corpus-wide failure percentage or a comparison against human scientists. Independent checks need authorized executable environments and frozen hashes. No automatic paper submission.

## First selected entry: public source-access precheck only

M2 is the first selected published-manuscript entry checked for source access. The public [package README](https://github.com/SECQUOIA/agent-swarm-research/blob/paper-v1/minlp-notes/paper-cubic-gap/README.md) and [paper source](https://github.com/SECQUOIA/agent-swarm-research/blob/paper-v1/minlp-notes/paper-cubic-gap/main.tex) give a cubic relaxation-gap bound `1610000/743033 <= R(3) <= 31/12` for nonnegative coefficients on finite nonnegative boxes, with a defined positive denominator. The [coverage map](https://github.com/SECQUOIA/agent-swarm-research/blob/paper-v1/minlp-notes/paper-cubic-gap/formal/COVERAGE.md) links the theorem to Lean declarations; the [upstream verification record](https://github.com/SECQUOIA/agent-swarm-research/blob/paper-v1/minlp-notes/paper-cubic-gap/formal/VERIFICATION.md) **reports**, but we have not reproduced, a 61-module build and 1,247-declaration audit.

Importantly, the README explicitly states that its delivery SHA-256 manifest is for an earlier snapshot and does not match several later manuscript, verification, and build-record revisions. Thus a failed check against that **historical** manifest would not itself show that the current formal theorem is false. The audit must first freeze one coherent source revision and match the correct manifest. **No formal correctness or semantic-fidelity verdict has been reached for M2.**

## Other branches and venue fit

CC-15: [When2Speak](https://arxiv.org/abs/2605.05626) already studies speaking versus staying silent in text-based multi-party dialogues; a generic speak/silent classifier is not new. HEARTBEAT's **causal streaming audio, timing, and interruption** setting is more specific; official released datasets/scorers still need authenticated access verification before a benchmark run. Do not substitute When2Speak scores for the HEARTBEAT challenge score.

CC-04: without its saved ranked candidates, a genuinely untouched entity-cluster-disjoint test and complete match labels, no real retrieval claim is ready. Do not use the tuned E7/E12 holdout as a final test.

Organizer rechecks on 27 October: [MLSys](https://mlsys.org/Conferences/2027/Dates) October 30 noon PDT; [CVPR](https://cvpr.thecvf.com/Conferences/2027/CallForPapers) November 10 registration and November 16 paper (AoE); [RSS](https://roboticsconference.org/information/cfp/) December 4 extended abstract. Venue scope, AI-use restrictions, full data provenance and human approval remain submission gates.

**Execution disclosure:** This report used public web and authorized GitHub read actions. The private sample lock and direct public-source edits are not ChatGPT↔Codex/local artifact transfers. No local scratch/transfer index was written, no private unpublished measurements were made public, and no GPU, Lean replay, challenge registration, or submission occurred.
