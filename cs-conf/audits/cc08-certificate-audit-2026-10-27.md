# CC-08: public agent-research artifact audit — 2026-10-27

Task: `20261026-csconf-research`. Audit type: **public artifact and arithmetic inspection**, **not a Lean compilation or independent scientific replication**. All inspected files are from the fixed [`paper-v1` tag](https://github.com/SECQUOIA/agent-swarm-research/tree/paper-v1) of Gusev and Bernal Neira's [AI Agent Swarms as Researchers](https://arxiv.org/abs/2609.35719).

## Objective and outcome

Determine which **independent verification steps** are required before an automated research system's self-reported result can count as trustworthy research.

| Sample | What the authors' exported material reports | What we checked independently | What is still unverified |
|---|---|---|---|
| **M1 — Sharp gaps for positive multilinear relaxations** | A complete paper, 48 Lean proof modules, 827 audited declarations, a standalone verification script and an exact finite-example table. | Retrieved the actual [main theorem source](https://github.com/SECQUOIA/agent-swarm-research/blob/paper-v1/minlp-notes/paper-multilinear-gap/formal/Formal/MultilinearGap/Results.lean), [finite-example claims](https://github.com/SECQUOIA/agent-swarm-research/blob/paper-v1/minlp-notes/paper-multilinear-gap/formal/Formal/MultilinearGap/Examples.lean), [cutoff formula](https://github.com/SECQUOIA/agent-swarm-research/blob/paper-v1/minlp-notes/paper-multilinear-gap/formal/Formal/MultilinearGap/ExactArithmetic.lean) and [verification record](https://github.com/SECQUOIA/agent-swarm-research/blob/paper-v1/minlp-notes/paper-multilinear-gap/formal/VERIFICATION.md). Independently calculated four printed rational examples (below) from the stated formulas. | Lean compilation and axiom closure in a clean environment; correspondence between the full paper and proved theorem assumptions; novelty; any external review. The project's [README](https://github.com/SECQUOIA/agent-swarm-research/blob/paper-v1/minlp-notes/paper-multilinear-gap/README.md) explicitly says historical delivery fingerprints were **not refreshed** after some revisions. |
| **M3 — Checkable lower bounds for convex MINLP** | Complete paper; 27 Lean modules; targeted proof/audit checks; a main experimental campaign with 289 model cases and a large certificate archive. | Read the [current verification record](https://github.com/SECQUOIA/agent-swarm-research/blob/paper-v1/minlp-notes/paper-certified-minlp/formal/VERIFICATION.md) and [project README](https://github.com/SECQUOIA/agent-swarm-research/blob/paper-v1/minlp-notes/paper-certified-minlp/README.md); checked that historical counts 188+92+9, frozen V1 counts 203+19+67, and predicted V3 counts 204+18+67 each sum to 289. These are arithmetic checks, **not independent certificate replay**. | Python checker and dependency behavior, dataset/model authenticity, certificate replay, statistical conclusions, project-wide kernel replay. The authors state standalone full-project replay was not run and the configured CI did not cover that standalone project. The paper-source archive predates later manuscript revisions. |

## Finite arithmetic reproduction for M1

Source definitions: `cutoffBudget(L,s)=(L-s+2)/2^s`; choose `s` so `cutoffBudget(L,s)>=1>=cutoffBudget(L,s+1)`. The paper's finite identity is `H=s+(L-s)/2^s`, with stated termwise gap `T=L`. We used exact integer numerator/denominator arithmetic, not floats.

| L | s | Independent H | Independent T/H | Matches reported example? |
|---:|---:|---:|---:|---|
| 2 | 1 | 3/2 | 4/3 | Yes |
| 8 | 2 | 7/2 | 16/7 | Yes |
| 16 | 3 | 37/8 | 128/37 | Yes |
| 64 | 5 | 219/32 | 2048/219 | Yes |

**Interpretation:** The table is internally consistent with the *stated* formulas. It does **not** independently establish that `H` equals the actual continuous convex-hull gap or that the general theorem is true. Source and proof correspondence require separate review. This is a finite check of a specified subclaim, not an automated paper verification.

## Main methodological finding

Treat the following as different certificate states:

1. **Claimed:** the agent wrote a mathematical or empirical statement.
2. **Present:** source files and purported supporting artifacts exist at a fixed revision.
3. **Locally reported:** the agent's own logs report passing checks.
4. **Independently replayed:** an external clean run compiles/replays those exact bytes and validates assumptions.
5. **Scientifically validated:** the result agrees with the intended problem, baselines, data and prior art.

A 'Lean Done' label can support **(2)** and a documented run can support **(3)**. It does not automatically establish **(4)** or **(5)**. Manuscript updates must be bound to their evidence through current hashes; historical manifests can be legitimate but must not be mislabeled as present-version attestations.

## Next locked test

Sample 10 claims from the already pinned `paper-v1` inventory, using a deterministic hash ranking over IDs and a preregistered balance of formal versus empirical versus notes-only evidence. Before checking conclusions, record evidence availability, Lean/version dependencies, predicted replay time, dataset rights, and whether an independent validator exists. For formal claims, reproduce a proof with the pinned Lean/Mathlib toolchain; for empirical claims, rerun one smallest certificate or data analysis using a clean environment. Include a manually chosen positive control and an intentionally broken artifact to test the audit itself.

Do not compute a 'verified research rate' from this two-item convenience sample. A later randomized audit must distinguish missing or unrun evidence from a false scientific claim. No paper or conference submission is implied.
