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
