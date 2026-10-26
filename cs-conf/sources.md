# CS Conf — evolving research program

Status: initial research-index snapshot, 2026-10-26 (Asia/Kolkata).  
Task ID: `20261026-csconf-research`.  
Public index: https://nilansa.github.io/cs-conf/  
Machine-readable state: [data.json](data.json).

## Purpose
Scout conferences across computer science and related science, compare their current submission policies with actual accepted papers, and maintain many independent, falsifiable research branches. Prefer experiments that can be executed and audited cheaply. Publish only substantiated, reproducible findings.

**Never infer acceptance probability from one accepted paper. Never invent results or citations. Do not automatically submit.** Multiple papers are fine if their contributions are genuinely distinct and venue policies permit it. Do not dual-submit substantially overlapping work.

## Primary read order for every new research session
1. Read this file and [data.json](data.json), especially `checkedAt`, the active `branches`, `policies` and `deadlines`.
2. Re-verify any imminent deadline or conference policy on its own official organizer site. Dates on this page are a dated snapshot, not a live API.
3. For the chosen branch, read at least the closest relevant papers and the accepted-paper patterns of its target venue; differentiate an existing method from a proposed new one.
4. Read the associated decision record in the private research inbox when connected. Never publish private collaborator notes, unpublished metrics, confidential data, tokens or private meeting transcripts.
5. Decide one next action (novelty audit, no-compute test, controlled experiment, replication, abstract, retire). Write what evidence would **falsify** the claim.
6. Update relevant public-safe fields in `data.json`, set a fresh checked date, and reference original sources. If publication fails, report it rather than claiming success.

## Research pipeline
### G0: Venue and policy
Verify conference scope, abstract date versus full paper date, page limits, human-review obligations, AI-writing restrictions, authorship, reciprocal-review quota, dual submission and publication/registration cost. For example, PAKDD 2027 allows generative AI only for grammatical correction; Interspeech 2027 rejects entirely AI-developed or AI-written papers; RSS 2027 permits LLM use and encourages disclosure. **Do not route AI-authored manuscripts to venues that prohibit them.**

### G1: Scientific question
Use FORMULATE:
- **Objects:** datasets, models, hypotheses, interventions and assumptions.
- **Observed phenomenon:** what has already been measured?
- **Question:** what is unknown (not the same as a mechanism)?
- **Mechanism:** causal explanation or proposed algorithm.
- **Metric and falsification:** a measurement that can disagree with the hypothesis.
- **Constraints:** compute, wall time, seeds, licenses, robustness, human validation.

Write each symbol's domain and a tiny example. Use ASD-STE100 technical English.

### G2: Novelty and experimental design
Make a 5–10 paper comparison table of the closest related work before deep compute. Lock the test split and key controls; note anything that came from development data. Compare against strong contemporaneous methods, not only naive baselines. For theory, independently verify proofs and generate counterexamples; a GPT-generated proof is not evidence without checking.

### G3: Cheapest decisive pilot
Prefer a small released checkpoint, local one-GPU test, toy problem, simulator, or simple synthetic-image experiment. Budget full compute including data preprocessing, model selection, additional teacher calls and failed runs. Only scale when the pilot yields a real signal under matched controls.

### G4: Evidence audit
Report primary metric, confidence interval or repeated seeds where appropriate, dataset split, prompt setup, ablations, total compute, and failed tests. Avoid cherry-picked figures that contradict quantitative findings. For a negative result, identify why it is generalizable and whether the target venue welcomes rigorous falsifications.

### G5: Paper
Write while experiments evolve. Strong story: problem → a narrow finding → mechanism → evidence → limitation. Every claim must map to a table, figure, theorem or cited study. Define all metrics and include appropriate aggregate statistics. Draft an abstract only after the hypothesis and evidence are clear (RSS Stage 1 permits preliminary experiments but demands a complete scientific plan).

### G6: Human approval
Check authorship and coauthor consent, licenses, paper anonymization, AI-use disclosure, live venue requirements and active concurrent submissions. No automatic final submission.

## Near-term priority
- **MLSys 2027**: 2026-10-30 at noon PDT. The systems contribution must be measured. Greenfield projects are unlikely to be responsibly ready in days.
- **CVPR 2027**: 2026-11-10 enrollment; 2026-11-16 full. The [published author guidelines](https://cvpr.thecvf.com/Conferences/2027/AuthorGuidelines) require an LLM Usage Statement even for grammar assistance; the reciprocal-reviewer quota generally permits only **one submission with no eligible reviewer among the coauthors**. Author lists and OpenReview profiles must be complete by Nov 10. Good scientific fit does not override these administrative limits.
- **ISCA 2027**: 2026-11-09 main-track abstract; 2026-11-16 full paper; 2026-12-06 industry-track abstract; 2026-12-13 industry-track full paper. [Official CFP](https://iscaconf.org/isca2027/submit/callforpapers.php) forbids placeholder abstracts, caps main-track submissions at eight per author, and requires disclosure for AI-generated substantive scientific content.
- **PAKDD 2027**: 2026-11-20. The applied track explicitly welcomes sound case studies, carefully explained failures and operational lessons; it does not require algorithmic novelty. **Its AI-use restrictions make heavily AI-written submissions ineligible.**
- **RSS 2027**: 2026-12-04 six-page extended abstract; 2027-04-16 invited final paper. Work can start with a hypothesis and complete method rather than a finished experimental suite.
- **ACL 2027**: 2027-01-04 last ARR submission cycle. Has main and short-paper options; check mandatory limitations.
- **SIGIR 2027**: January abstract/full dates on the official draft are currently **proposed** and must be checked again.
- **Interspeech 2027**: 2027-02-09 deadline, but AI-developed/written submissions are prohibited.

## Accepted-paper anchor examples (titles only; not claims of easy acceptance)
The [PAKDD 2025 organizer's accepted-paper page](https://pakdd2025.org/accepted-papers/) includes:
- "Differentiable Good Arm Identification"
- "LinearAPT: An Adaptive Algorithm for the Fixed-Budget Thresholding Linear Bandit Problem"
- "Clustering-based Meta Bayesian Optimization with Theoretical Guarantee"
- "Informed Augmentation Selection Improves Tabular Contrastive Learning"
- "Machine Learning Techniques for Data Reduction of Climate Applications"
- "Time Series Treatment Effects Analysis with Always-Missing Controls"
- "Focus On What Matters: Guiding Vision Transformers Towards Justification"
- "Bridging Semantic and Emotional Gaps in Speech Emotion Recognition"
- "Deep Interactions for Multimodal Molecular Property Prediction"
- "Representing Higher-Order Networks with Spectral Moments"

These establish actual **scope diversity**. They do not establish that any particular new paper is low-effort or likely to be accepted. Each closest paper still requires a full methods and experiments reading before novelty is asserted.

## Second literature audit: October 26, 2026 (public-safe)
- **CC-10**: [What-If World](https://arxiv.org/abs/2605.27589) already studies counterfactual physical-variable interventions in generated driving and robotic-manipulation videos. Crucially, it explicitly names **downstream utility measurement** as future work. But [CausalNav](https://arxiv.org/abs/2608.07809) also reports that world-model structure can fail to predict control benefit, while [ExecutionBridge](https://arxiv.org/abs/2610.22041) tests a frozen planner under execution shift. The remaining proposed question is narrow: can controlled **rigid geometry errors** induce action-ranking reversals, at fixed planner/camera/appearance quality? The 2D paired pilot is *only designed*, not run.
- **CC-02**: [GRU-D (2018)](https://www.nature.com/articles/s41598-018-24271-9) already shows that missingness patterns can contain predictive information. [CMT-MAE (AAAI 2025)](https://ojs.aaai.org/index.php/AAAI/article/view/34145) uses learned masking. A generic mask-leakage paper therefore lacks novelty. Test the **extra conditional information in mask indices** beyond visible patches and fixed mask-count/geometry controls, then test whether it affects MIM training conclusions.
- **CC-08**: [CausalVerify (Sep 2026)](https://arxiv.org/abs/2609.07944) measures failures in end-to-end LLM-made empirical causal analyses even when code executes. A new research-agent paper should measure **experiment-selection bias under frozen wall time and withheld seeds**, not claim execution equals validity.
- **Conference policy correction**: CVPR 2027 now has a full [LLM author policy](https://cvpr.thecvf.com/Conferences/2027/AuthorGuidelines), replacing the earlier 'policy under development' note. No AI-use statement means desk rejection. ISCA 2027 has a distinct AI disclosure rule; consult each venue.

No new experiments, manuscript, or submission occurred as part of this audit.

## Research-agent precedents
- [The AI Scientist (Nature, 2026)](https://www.nature.com/articles/s41586-026-10265-5) and [AI Scientist v2](https://github.com/SakanaAI/AI-Scientist-v2): ideation, coding, running experiments, writing, and automated reviews. One controlled ICLR 2025 workshop submission passed initial peer-review thresholds; this is not evidence of main-track acceptance or unconstrained automated publication.
- [Karpathy autoresearch](https://github.com/karpathy/autoresearch): tightly constrained single-GPU, five-minute fixed-budget experiment loop. A compelling example of safe comparison under frozen task settings, not automatically a novel paper.
- [Agent Laboratory](https://arxiv.org/abs/2501.04227): literature, experiments, and reports with optional human guidance.
- [Robin (Nature, 2026)](https://www.nature.com/articles/s41586-026-10652-y): literature→hypotheses→data analysis→refinement; human scientists still execute laboratory experiments.
- [PaperBench](https://openai.com/index/paperbench/): independent paper-replication benchmark; helps frame the limits of agent claims.

## Writing exemplar
[Using OCR Heads to Verbalize Image Semantics](https://arxiv.org/abs/2609.18823) by Feucht and colleagues is a coherent interpretability story: identify heads causally important to OCR, project their semantics into vocabulary space, localize image concepts, then intervene and analyze failures. Its strength is an explicit mechanism and linked evidence, not that a language model could polish the words.

## Organizer policies and deadline sources
All verified deadline source URLs, per-venue links, and policy links are retained in [data.json](data.json). Particularly important: [CVPR 2027](https://cvpr.thecvf.com/Conferences/2027/CallForPapers), [MLSys 2027](https://mlsys.org/Conferences/2027/CallForResearchPapers), [PAKDD 2027 Authors Kit](https://pakdd2027.org/pages/calls/authors-kit), [RSS 2027](https://roboticsconference.org/information/cfp/), [ACL 2027](https://2027.aclweb.org/calls/main/), [Interspeech 2027](https://interspeech2027.org/calls/call_for_papers/), [ICLR 2027 AI author policy](https://iclr.cc/Conferences/2027/AIPolicyForAuthors).

## Public/private boundary and sync
This is a public website. A private GitHub issue is used for discussion and decision records, when connected; the user's ChatGPT conversation is another discussion channel. Automatic hourly chat tasks do **not** create background GPU experiments or live website updates by themselves. Changes must be made and verified through authorized connector calls. Do not place scratch files, secret credentials, unpublished private results or transfer manifests in this public directory.

The user's separate cross-surface sync-first requirements apply whenever the workflow actually transfers artifacts between ChatGPT and Codex/local computers: stable task ID `20261026-csconf-research`, private scratch, Codex-authored transfer index, verified hashes and no browser UI transfers. The present initial publishing operation used direct connected GitHub file actions; there was no Codex/local file handoff.

## Third literature audit: October 26, 2026 (public-safe)
- **Formal correction to CC-02:** The earlier diagnostic `I(Y; M | V)` is **identically zero** when `V` includes visible patch positions and `M` is their complement: `H(M|V)=0`. This is a mathematical definition issue, not an experiment. Replace it with a position-only sampling-policy probe: `S` denotes visible positions; `B` denotes visible patch **values with positions intentionally excluded**; compare `S`, `B`, `(S,B)` against fixed/random selection with matched visible counts. A toy positive result is not enough for novelty. Prior art: [MAE (CVPR 2022)](https://arxiv.org/abs/2111.06377), [AdaMAE](https://arxiv.org/abs/2211.09120).
- **CC-04:** [DeepBlocker (PVLDB 2021)](https://github.com/qcri/DeepBlocker) and [Entity Resolution in Practice (2026)](https://arxiv.org/abs/2607.26298) preclude claiming a novel multi-route blocker by itself. The test is **all-links recall at equal global candidate count and total retrieval time**, comparing uniform versus uncertainty-based per-query allocation on a previously untouched stratified test split. This is a testable idea, not a proven algorithm.
- **CC-06:** Event/boundary selection alone is established: [BMVC 2021 event boundary alignment](https://www.bmva-archive.org.uk/bmvc/2021/assets/papers/0878.pdf), [Ground, Cover, and Refine (2026)](https://arxiv.org/abs/2608.01660), and [MemoryCard (2026)](https://arxiv.org/abs/2606.05917). The remaining question is whether query-agnostic **GEBD** adds downstream value beyond query/event baselines at exactly the same frame budget and detector cost. No new videos evaluated.
- **CC-10:** [Geometric Action Model (2026)](https://arxiv.org/abs/2606.17046) already links geometry and robot actions. The proposed controlled test will stratify by unperturbed planner action-cost margin and measure true regret, avoiding the tautology that obstacle size can alter a path. No controlled pilot run.
- **CC-12 + new deadline:** [MIDL 2027 official dates](https://2027.midl.io/important-dates): full-paper abstract enrollment **Nov 30, 2026**, full paper **Dec 4, 2026**, both 23:59 AoE; short-paper date remains **TBD**. The [call](https://2027.midl.io/call-for-papers) welcomes robustness and validation; there is also a [Clinical Translation & Validation track](https://2027.midl.io/author-instructions). Generic cell-video realism/temporal consistency is already explored by [microscopy diffusion (2025)](https://arxiv.org/abs/2503.18583). A potential nonclinical test is **biologically meaningful topology/lineage faults versus visual scores**, grounded in [Cell Tracking Challenge](https://www.nature.com/articles/s41592-023-01879-y); it is untested.
- **COSYNE 2027:** [Official call](https://www.cosyne.org/abstracts-submission) says abstracts are closed (main abstract deadline was Oct 18, 2026). The open workshop proposal deadline, Nov 1, is **not** a research-paper submission deadline.

**Read/write boundary:** These are public-safe bibliographic and experimental-plan updates only. Private collaborator metrics and decisions stay in the private issue. Direct GitHub edits are not a Codex/local handoff; therefore no cross-surface transfer manifest is generated. No experiments, abstracts, or papers have been submitted in this audit.


## Fourth literature audit: October 26, 2026 (public-safe)
- **CC-04: major prior-art collision.** [QASP (2026)](https://arxiv.org/abs/2607.29606) predicts per-query recall progression and adaptively chooses search effort; [Progressive Entity Resolution (2025)](https://arxiv.org/abs/2503.08298) and [SPER (CIKM 2026)](https://doi.org/10.1145/3799682.3840729) schedule entity comparisons under fixed budgets. [BEACON (SIGMOD 2026)](https://arxiv.org/abs/2603.11391) is a *label-annotation-budget* paper, not retrieval-comparison allocation. Do **not** claim adaptive budgets, progressive blocking, or entity-matching budgets are novel. Narrow hypothesis: maximize **complete-link coverage** of multi-match source entities under a *single global candidate/computation budget* using a calibrated per-query maximum-positive-rank curve. This objective is distinct from pair-recall scheduling but still needs an exact novelty audit and strong baselines. Report positive-query-only and zero-match cases separately to avoid vacuous success.
- **CC-11: elementary formulation, not a theorem contribution.** For positive query `i`, define `T_i` as the rank of its furthest true matching target; completion at cap `K_i` means `T_i<=K_i`. Estimate `F_i(k)=Pr(T_i<=k|features)` and maximize `sum_i F_i(K_i)` with `sum_i K_i<=B`. This is an ordinary budget allocation / multiple-choice knapsack structure; a formulation or toy counterexample alone cannot establish novelty. Simple analytic contrast: source A has four true links at ranks 1–4, sources B and C have one true link each at rank 2, total budget 4. A:4, B:0, C:0 gives pair recall 4/6 and one completely resolved source; A:0, B:2, C:2 gives pair recall 2/6 and two completely resolved sources. No empirical data used.
- **CC-08: negative-result premise challenged.** [What Fits (Into Few Tokens) Doesn't Overfit (2026)](https://arxiv.org/abs/2606.11045) finds agent-discovered methods often survive compact reproduction despite adaptive benchmark search; deliberately induced overfit fails the same test. [AI Research Agents Narrow Scientific Exploration (2026)](https://arxiv.org/abs/2605.27905) finds agents concentrate idea generation near starting literature; [DeepAnalyze (ICML 2026)](https://proceedings.mlr.press/v306/zhang26aq.html) demonstrates broad end-to-end data analysis. A useful agent audit must search for the **boundary conditions** of reliability and independent idea discovery rather than assume failure.
- **New deadline and policy:** [CHIIR 2027 short paper](https://chiir2027.github.io/short-papers.html), **Oct 29 2026 AoE**, 4 pages plus references, no separate abstract enrollment; related demo/resource/industry tracks have the same date on organizer pages, but their own calls govern format. [CHIIR AI policy](https://chiir2027.github.io/generative-ai-policy.html) distinguishes allowed writing assistance from AI-conducted research (which needs disclosure). In-person presentation and potential ACM open-access charges must be considered. No CS Conf branch has a CHIIR-ready validated result. [ICASSP 2027](https://2027.ieeeicassp.org/call-for-papers/) full-paper deadline was **Sep 23, 2026**, so it is already closed.
- **SYNC / integrity:** This audit uses direct authorized GitHub file actions, not any ChatGPT↔Codex/local file transfer. Stable task ID remains `20261026-csconf-research`; do not create a ChatGPT-authored transfer index. No experiments, accepted results, or manuscripts are claimed.


## Fifth literature audit: October 26, 2026 (public-safe)

- **CC-01 — RETIRE standalone metric-only paper route.** In addition to [PDI-Bench](https://arxiv.org/abs/2605.15185), [TriWorldBench (Sept 2026)](https://arxiv.org/abs/2609.26314) studies multi-view robot-video geometry and [RGraph-Eval (Oct 22, 2026)](https://arxiv.org/abs/2610.31121) evaluates task-grounded object, interaction and 3D motion using scene graphs. New visual/geometric scores alone do not constitute a defensible new CVPR contribution. Keep downstream scientific relevance under CC-10, but do not double-count papers.
- **CC-10 — major newly documented prior-art collision.** [Beyond Task Success: Stage-Wise Reliability of World Model Planning under Sensing Degradation (Sep 2026)](https://arxiv.org/abs/2609.07126) already tests paired visual/temporal corruption on 50 world-model robot-planning tasks, including **frozen candidate action-sequence rankings, predicted future differences and task success**. That blocks the generic claim that sensing errors have never been related to planner preference. Residual question, if any: do *object geometry-specific* errors affect decision regret differently from brightness/occlusion/blur under matched conditions? Reproduce/inspect the published baseline before any novel claim. High novelty risk, no runs.
- **CC-04 — precise objective separation after checking the primary papers.** [Progressive Entity Resolution (PACMMOD/SIGMOD 2025)](https://arxiv.org/abs/2503.08298) maximizes **early pair recovery** and explicitly excludes expensive verification time from its own runtime definition. [QASP (July 2026)](https://arxiv.org/abs/2607.29606) estimates **ANN search-neighbor recall** as probe depth changes; its recall is not the recall of all semantically true business matches. A multi-positive-source *complete-link* objective at fixed global budget could differ, but proving a distinct objective is not proof of a better algorithm. The next pilot requires full positive-label provenance and both **equal-candidate-count** and **equal-end-to-end-time** comparisons (including learned-policy inference, retrieval, indexing and matching).
- **CC-11 — executable sanity check, not research evidence.** For two source queries let cumulative completion curves be `F_A(0,1,2)=(0,.40,.41)` and `F_B=(0,0,1)`, budget `B=2`. A deterministic one-step marginal greedy gives allocation `(2,0)` with objective `0.41`; exhaustive enumeration gives `(0,2)` with objective `1.00`. Verified by a tiny CPU enumerator in this cycle. This shows nonconcave completion curves defeat naive greedy; it is a standard algorithmic phenomenon, **not** a novel theorem or performance on real entity-resolution data.
- **CC-08 — exact end-to-end agent precedent, with limitations.** [Gusev and Bernal Neira, *AI Agent Swarms as Researchers* (Sep 2026)](https://arxiv.org/abs/2609.35719) provide the [agent-swarm-research public corpus](https://github.com/SECQUOIA/agent-swarm-research). Their README specifies that the `paper-v1` tag includes untouched agent notes, proofs, code, draft manuscripts, and agent reviews, with no author scientific edits as of Sep 25. The authors explicitly say much output is not independently verified, and a full-paper artifact does *not* mean accepted/published. Proposed CPU-first study: fixed, blinded claim-verification audit stratified by available certificates, measuring independent review time and failure types. No such sample audit executed this cycle.
- **ARRSI workshop practical route:** [Organizer CFP](https://ar-rsi.github.io/) confirms October 30, 2026, 11:59pm AoE, including four-page position papers and reporting standards for human intervention, compute, failed runs and evidence. CC-08 might fit a **carefully substantiated position**; no submission-ready evidence or claim of acceptance yet.

Direct connected GitHub edits only; no ChatGPT↔Codex/local file transfer, so no new transfer manifest. No real ER, robotics, vision, or GPU benchmarks, abstract enrollment, manuscript submission or venue acceptance in this cycle.
