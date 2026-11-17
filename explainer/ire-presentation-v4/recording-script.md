# Ceous: Efficient Retrieval Adaptation from Limited Reranker Feedback

## Recording script, corrected V4 · Nilanjan Sarkar · IIIT Hyderabad

**Scope:** 25 main slides followed by 5 appendix slides. No final author conclusion has been supplied.

**Cautions:** The Manim figures are conceptual. The temperature and KL curves are illustrative, not logged Adam traces. Our DISCo-inspired experiment selects ten items from dense top-50, not the original corpus-level DISCo index.

### Slide 01 — Ceous: Efficient Retrieval Adaptation from Limited Reranker Feedback

We study how to adapt retrieval at inference time while keeping the embedding model and reranker frozen. The central question is whether a limited set of black-box reranker scores can be converted into a query representation that retrieves better from the full corpus. Our specific experiment changes which documents supply feedback to TTT-Embed: ordinary dense top-ranked documents versus a DISCo-inspired complementary selection policy.

**On-slide cues:** Project: Ceous; Course: M26CS4.406; 17 November 2026

### Slide 02 — The deployment constraint

In a deployed system, the retriever and reranker may be accessible only through interfaces. We can submit a query, retrieve candidates and observe scalar relevance scores, but we may not have permission to update model weights or inspect internal gradients. Full retraining can also require data, compute, deployment coordination and regression testing. The setting here is narrower: adapt one query at inference time using outputs the system already exposes.

**On-slide cues:** Frozen query/document encoders; Frozen black-box reranker; Accessible vectors, scalar scores and search API

### Slide 03 — A reranker cannot rescue a document it never sees

Dense retrieval compares a query vector with the stored document vectors and returns a candidate pool. A cross-encoder reranker can judge each supplied query-document pair more carefully, but it only reorders that supplied pool. If a relevant document is absent, reranking cannot introduce it. This motivates using reranker feedback to modify the query and then searching the full collection again.

**On-slide cues:** Retriever: searches the corpus; Reranker: scores supplied pairs; Adapted query: can trigger a new search

### Slide 04 — Relevance feedback has a long history

The underlying intuition predates neural retrieval. Classical vector-space relevance feedback, associated with Rocchio, moves a query representation toward relevant documents and away from non-relevant ones. Pseudo-relevance feedback applies a similar idea when relevance labels are not explicitly supplied by a person. Modern systems replace manually supplied labels with a learned reranker, but the operational question remains: how should evidence change the query used for the next search?

**On-slide cues:** Classical relevance feedback; Pseudo-relevance feedback; Inference-time query adaptation

### Slide 05 — Inference-time adaptation: use the evidence already available

Inference-time adaptation is useful when a system needs to respond to a particular query without updating and redeploying the underlying model. In retrieval, the query is already a compact representation of the information need. If feedback tells us which candidates better satisfy that need, we can use it to refine the query representation and issue another search. This is a local, request-time operation; it is not a claim that retraining is never useful.

**On-slide cues:** No encoder fine-tuning in this project; No reranker fine-tuning; Per-query state can be discarded after use

### Slide 06 — TOuR: optimise a test-time query representation

TOuR optimises the test query vector, not the encoder weights. For each test query, it retrieves current top-k contexts, asks a cross-encoder for pseudo-relevance scores, and takes a gradient update of q. Crucially, after an update it can retrieve a fresh candidate set and score again. The gradient is through inner products with fixed context embeddings; no cross-encoder gradient is required.

**On-slide cues:** q_{t+1} = q_t - eta * grad_q L; TOuR reretrieves during its test-time optimisation; Source: Sung et al., Findings ACL 2023, Eqs. 7-13

### Slide 07 — TOuR-hard and TOuR-soft

TOuR-hard forms the smallest teacher-probability-ranked set of pseudo-positive contexts whose cumulative teacher probability reaches threshold p. It maximises the student probability assigned to this set: minus log of the sum of student probabilities. TOuR-soft instead keeps all graded cross-encoder teacher probabilities and minimises KL divergence. The soft gradient moves the query toward the teacher-weighted document centroid and away from the student-weighted centroid. It is not merely a generic binary-versus-continuous classification difference.

**On-slide cues:** Hard: L = -log sum_{c in C_positive} p_student(c); Soft: L = KL(p_teacher || p_student); Soft: q_new = q + eta sum_i (p_teacher_i - p_student_i) z_i

### Slide 08 — ReFIT: reuse reranker scores during query optimisation

ReFIT addresses the situation where a reranker can judge only initially retrieved documents. The paper caches reranker scores and repeatedly updates the query vector by minimising teacher-to-student KL on that fixed slate, then searches the corpus again once. Its experimental recipe independently min-max normalises the reranker and retriever score lists. Because cross-encoder scores are often peaked, it uses teacher temperature T equals 2. The reported setup uses 100 query-gradient steps at learning rate 0.005. These are ReFIT paper settings, not the settings of our TTT-Embed experiments.

**On-slide cues:** Teacher softmax(minmax(reranker_scores) / 2); Student softmax(minmax(retriever_scores)); 100 gradient steps, LR 0.005; one second full retrieval

### Slide 09 — What the lineage contributes

The distinction is operational. TOuR may refresh the candidate set between query-gradient steps and uses hard or soft pseudo-feedback. ReFIT reuses one scored slate during 100 query-vector updates and applies a KL distillation loss after separate score normalisation. TTT-Embed learns an additive output-space residual v, rather than directly replacing the current query vector, and permits query, task, or global sharing of that state. Our combined DISCo experiment changes the feedback selection policy but retains the query-wise TTT-Embed objective.

**On-slide cues:** TOuR: pseudo-feedback + iterative reretrieval; ReFIT: cached teacher scores + KL + second retrieval; TTT-Embed: external residual + sharing scope

### Slide 10 — TTT-Embed: represent adaptation as an external residual

TTT-Embed begins with a frozen unit query embedding x and frozen unit document vectors z_i. It learns an external output-space residual v, initially zero. The student compares unit(x+v) with selected documents. The reranker is used only to supply fixed scalar targets for those documents; it is not differentiated through and neither the query encoder nor document index is updated. Our experiments fit an independent query-wise v for each query and selection arm.

**On-slide cues:** x_hat(v) = unit(x + v); x_new = unit(x + 0.5 * v_300) in query-wise FiQA; Encoder and reranker remain frozen

### Slide 11 — What does the residual change geometrically?

A residual is a geometrical correction to the frozen query. The vector v changes similarity with all documents, not only the ten teacher-scored documents. Normalisation makes the query unit length again. Because its denominator is common for one query, ranking depends on the original query-dot-document score plus the residual-dot-document score. The Manim animation on this slide is a conceptual two-dimensional projection; it is not an empirical embedding trace.

**On-slide cues:** x_new^T z_d = (x^T z_d + 0.5 v^T z_d) / ||x + 0.5 v||; Full corpus is searched after fitting; Manim: QueryResidual, conceptual geometry

### Slide 12 — Why turn scores into a distribution?

The teacher can output Yes/No probabilities, logit scores, or other scalar preferences. These are not on the same numerical scale as retriever cosine similarities. We convert scores over the same ten feedback document IDs into probability distributions with softmax. Teacher temperature tau_T is 0.02; student temperature tau_S is 0.05 in our query-wise run. Smaller temperature accentuates relative differences; it is not a calibration guarantee. ReFIT uses a different teacher scale and separate min-max normalisation.

**On-slide cues:** p_T(i) = softmax(r_i / tau_T); p_S(i;v) = softmax(unit(x+v)^T z_i / tau_S); tau_T=0.02; tau_S=0.05 in our recorded run

### Slide 13 — KL divergence turns preferences into a fitting objective

KL divergence is the loss that converts reranker preferences into a vector correction. The fixed teacher distribution p_T tells us which of the ten documents should receive probability; the student distribution p_S(v) is produced by the frozen retriever and changes with v. Forward KL, sum p_T log(p_T/p_S), penalises assigning too little student mass to teacher-preferred documents. We add ridge lambda times squared norm of v. Adam takes 300 steps at learning rate 0.01. The shown KL curve is illustrative, not logged experimental trajectory; the gradient uses the selected frozen document vectors and the normalisation Jacobian.

**On-slide cues:** L(v) = KL(p_T || p_S(v)) + 0.3 ||v||^2; grad_v L = (I-uu^T)/(tau_S ||x+v||) * sum_i (p_S-p_T)_i z_i + 2 lambda v; 300 Adam steps, LR=0.01; KL schematic is not measured

### Slide 14 — Query-wise, task-wise and global adaptation

The original TTT-Embed framework offers exactly three sharing scopes. Query-wise fits one vector from one rewarded query; task-wise shares a vector across several rewarded queries of one retrieval task; global-wise shares across retrieval tasks. The paper finds that the desirable scope can shift with available reward budget. These are not four separate modes: local adaptation refers generically to a per-query correction, not an additional fourth sharing scope. Our FiQA-200 and H8 DISCo experiments use only query-wise fitting.

**On-slide cues:** Query-wise: one query, one v; Task-wise: shared within one task; Global-wise: shared across tasks; local is not a fourth scope

### Slide 15 — Complementary retrieval: retrieve evidence with different strengths

A query may ask about several entities, relations or constraints. Dense retrieval can return several passages that are individually similar but repeat the same aspect. Complementary retrieval tries to obtain evidence with different strengths: lexical retrieval can recover exact terms, diversification can reduce redundancy, and aspect-coverage methods can represent multiple facets. Examples include MMR, xQuAD or IA-Select, hybrid BM25-plus-dense retrieval, and collective token coverage.

**On-slide cues:** MMR: relevance with redundancy penalty; BM25 + dense / rank fusion: lexical-semantic complementarity; Aspect coverage: represent multiple query facets

### Slide 16 — ColBERT and DISCo are related, but not the same

ColBERT-style late interaction scores a document by matching each query token to its best document-token match. That score is computed per document. DISCo instead selects a set whose union collectively covers the query-token representations. Once an aspect is already covered by the selected set, another document repeating it contributes less marginal coverage. This is why DISCo is relevant to feedback-set construction, but it does not automatically guarantee relevance.

**On-slide cues:** ColBERT: per-document MaxSim; DISCo: set-level collective coverage; Coverage ≠ relevance guarantee

### Slide 17 — DISCo: select a set for collective query-token coverage

DISCo is designed for collective contextual query-token coverage, where several passages may jointly answer a multi-aspect question. At each greedy selection step, the value of a document is how much additional query-token coverage it brings given the already selected set. It is not the same as independently ranking each document by MaxSim. We applied this collective-coverage idea within the initial Qwen dense top-50 slate, choosing ten. The animation from the earlier version is genuine Manim, with synthetic token-similarity values; no reranker or retrieval experiment is depicted in those synthetic numbers.

**On-slide cues:** F_q(S) = sum_j max(0, max_{d in S} h_j(d)); Marginal gain: F(S union {d}) - F(S); Manim: CollectiveCoverage, illustrative matrix

### Slide 18 — Why complementary feedback can change the residual

A useful feedback slate must carry both relevant teacher preferences and geometrically informative vectors. The normalisation Jacobian projects the weighted residual gradient onto the tangent plane of the current query direction. Complementary documents can diversify the vector directions but only if their reranker scores distinguish useful evidence. Because BERT token coverage selects IDs while the TTT residual uses Qwen embeddings, improved BERT coverage does not prove improved Qwen retrieval. This is a falsifiable mechanism hypothesis, not an established theorem of performance.

**On-slide cues:** grad_v L = J(x+v)/tau_S * sum_i (p_S-p_T)_i z_i + 2 lambda v; J(a) = (I-uu^T) / ||a||; Selection aspect coverage and residual-space alignment are distinct

### Slide 19 — Two different meanings of DISCo + TTT-Embed

Our completed FiQA and H8 implementation first retrieves a dense top-fifty pool with Qwen. BERT contextual-token coverage selects ten documents inside that pool. The Qwen reranker scores those ten, and query-wise TTT-Embed fits the residual. This tests the feedback-selection principle. It does not replace the initial Qwen retriever with the original DISCo corpus index. A true complementary first-stage retriever that discovers candidates outside the dense pool is a distinct experiment and has not been run here.

**On-slide cues:** Executed: Qwen top-50 → BERT coverage top-10 → Qwen reranker → TTT-Embed → full search; Not executed: original DISCo index replacing Qwen candidate generation; Do not call the completed run an exact DISCo reproduction

### Slide 20 — FiQA-200: controlled feedback-selection experiment

The FiQA experiment uses the full 57,638-document collection and 200 predetermined queries. Qwen3-Embedding-0.6B supplies a common dense top-fifty pool. Each selector chooses ten documents; Qwen3-Reranker-4B provides the teacher scores; query-wise TTT-Embed fits an independent residual with 300 Adam steps. The corrected query searches the complete corpus again. The primary metric is nDCG@10 against FiQA relevance judgements. The query set had prior project exposure, so this is an exploratory paired comparison.

**On-slide cues:** 57,638 documents · 200 queries; Top-50 candidate pool · 10 feedback pairs; Qwen3-Embedding-0.6B · Qwen3-Reranker-4B · BERT-base-uncased

### Slide 21 — FiQA-200: recorded full-corpus retrieval results

Standard dense-feedback TTT records nDCG@10 of 0.505956. DISCo-style coverage TTT records 0.480703. Other recorded arms include MMR, hybrid retrieval, BERT MaxSim and BM25 feedback. The paired coverage-minus-dense TTT difference is minus 0.025253, with a descriptive paired interval from minus 0.043324 to minus 0.007492. Coverage minus rank-matched TTT is plus 0.004556, with an interval spanning zero. These are the archived experiment values; no new run is implied.

**On-slide cues:** Primary baseline: dense top-10 + TTT = 0.505956; Coverage + TTT = 0.480703; Paired intervals and all other arms shown in the chart

### Slide 22 — Query-level examples: promotions and regressions

The casebook contains query-level rank transitions. For the education-loan query, a judged document moves from raw rank 27 to dense-TTT rank 10 and coverage-TTT rank 1; the coverage reranker score was 0.987568. For the LLC query, a judged document already at raw rank 1 remains rank 1 under dense TTT but moves to rank 3 under coverage TTT. These cases illustrate both a promotion and a regression. They do not by themselves establish why the selector chose the document; the saved archive does not include every token-level marginal coverage contribution.

**On-slide cues:** Education loan: 27 → 10 → 1; LLC query: 1 → 1 → 3; Selected examples must be read alongside all 200 cases

### Slide 23 — HotpotQA-HardNegatives: a second DISCo-guided TTT study

The H8 experiment uses the MTEB HotpotQA-HardNegatives collection with 225,621 documents and 1,000 queries. The recorded arms include dense TTT, coverage TTT, MMR, k-centre, D-optimal, random and shuffled-teacher controls. Coverage TTT records pooled nDCG@10 of 0.7496 compared with 0.7346 for dense TTT. The preregistered DEV400 difference is plus 0.0103, but its interval includes zero, so the registered decision gate was not passed. The later 600-query group is post-decision exploratory evidence.

**On-slide cues:** 225,621 documents · 1,000 queries; DEV400: +0.0103 [−0.0041, +0.0251]; Later 600: +0.0181 [+0.0062, +0.0303]

### Slide 24 — Intermediate diagnostics and a separate coverage-only study

On FiQA, coverage selects documents at a much deeper mean dense rank than the dense top-ten arm, and its feedback-set judged recall is lower. The teacher target also has lower effective support. A separate HotpotQA diagnostic selected two supporting paragraphs from ten supplied paragraphs without reranking or TTT: dense top-two found both supports in 124 of 400 cases, while unnormalised DISCo-style coverage did so in 194 of 400. This is a different task and metric; it must not be merged with the TTT retrieval results.

**On-slide cues:** FiQA feedback recall: dense 0.5403 vs coverage 0.3977; Mean selected rank: 5.50 vs 19.73; Standalone diagnostic: 31.0% vs 48.5% · no TTT

### Slide 25 — Scope of the evidence and the next measurements

The completed evidence includes FiQA-200 and HotpotQA-HN H8 DISCo-inspired feedback selection with query-wise TTT-Embed. Separate project studies include task-wise FiQA cross-fitting, SCIDOCS ReFIT, SciFact frozen-cache comparisons and an earlier ANN pilot. The current evidence does not establish that an original DISCo index would outperform dense candidate generation, nor does it settle which query properties predict useful complementary feedback. The next useful analysis is a paired, query-level examination of reranker scores on dense and coverage slates, followed by a separately approved first-stage complementary-retrieval experiment.

**On-slide cues:** No final research conclusion supplied; Reranker agreement analysis: archival analysis proposed; True first-stage complementary retrieval: future experiment

### Slide 26 — Appendix · Method identity and terminology

The original DISCo method uses a specialized contextual-token retrieval and indexing pipeline. Our implementation borrows its collective coverage objective inside a Qwen dense top-fifty pool, using frozen BERT-base-uncased token features. The reranker and TTT-Embed are separate downstream components added by our project. This appendix records the terminology needed to avoid claiming a full DISCo reproduction.

**On-slide cues:** DISCo paper: set-level coverage; Our selector: fixed-pool coverage; Qwen retriever and reranker remain distinct

### Slide 27 — Appendix · Additional FiQA diagnostics

The diagnostic table shows how the feedback slate differs before optimisation. Coverage's selected documents come from deeper initial dense ranks on average and contain fewer judged positives according to the qrels. The teacher distribution is also more concentrated by the effective-support measure. These values describe the inputs and fitted vectors; they do not by themselves identify a causal explanation for the aggregate retrieval difference.

**On-slide cues:** Dense vs coverage feedback recall: 0.540268 vs 0.397735; Mean selected rank: 5.50 vs 19.73; Effective support: 3.957 vs 2.893

### Slide 28 — Appendix · Other project experiments

The project also contains a FiQA task-wise cross-fit over all 648 queries, where a shared task residual is fitted on training folds and evaluated on held-out queries. It records nDCG@10 of 0.46722 for raw retrieval and 0.46313 for the shared residual. The SCIDOCS ReFIT experiment covers 1,000 queries and reports Recall@100 of 37.8067% for raw Contriever, 38.3450% for direct reranking and 37.8717% for ReFIT. These are separate experiments, not additional DISCo-TTT arms.

**On-slide cues:** FiQA task-wise cross-fit: 648 queries; 0.46722 vs 0.46313; SCIDOCS ReFIT: 1,000 queries; Recall@100 37.8717%; Different methods, datasets and protocols

### Slide 29 — Appendix · H8 controls and paired comparisons

H8 compares several selection policies with the same general teacher-feedback budget. The development set was the preregistered decision set. Its coverage-minus-dense TTT confidence interval includes zero. The later 600-query group was evaluated after the decision, and its interval is positive. The pooled result is descriptive. We preserve all three rather than presenting the pooled value as if it were a preregistered success.

**On-slide cues:** DEV400 +0.0103 [−0.0041,+0.0251]; Post-decision 600 +0.0181 [+0.0062,+0.0303]; Pooled 1,000 +0.0150 [+0.0057,+0.0245]

### Slide 30 — Appendix · References and reproducibility

The method lineage is grounded in the TOuR, ReFIT, TTT-Embed and DISCo papers. The local experiment records identify the FiQA and H8 runs, the selection and fitting implementations, and the separate diagnostics. Published method descriptions are not treated as evidence that our implementation reproduced every component of the original paper systems.

**On-slide cues:** TOuR · Findings of ACL 2023; ReFIT · arXiv:2305.11744; TTT-Embed · arXiv:2608.12569

## Paper sources

- TOuR: https://aclanthology.org/2023.findings-acl.354/
- ReFIT: https://arxiv.org/html/2305.11744v2
- TTT-Embed: https://arxiv.org/abs/2608.12569
- DISCo: https://openreview.net/forum?id=cUdODCFjUM
