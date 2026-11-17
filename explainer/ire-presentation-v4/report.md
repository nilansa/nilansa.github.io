# Ceous: Efficient Retrieval Adaptation from Limited Reranker Feedback

**Nilanjan Sarkar**  
IIIT Hyderabad · Information Retrieval and Extraction (M26CS4.406)  
Technical report · 17 November 2026

## Abstract

This project studies inference-time retrieval adaptation when an embedding retriever and a relevance reranker remain frozen. A query is encoded, a limited set of documents receives scalar reranker feedback, and an external query-space vector is fitted before a second search of the document collection. The principal experiments combine the query-wise objective of TTT-Embed with a feedback selector inspired by DISCo's collective contextual-token coverage. The selector changes which query-document pairs enter the fitting objective; the residual learner remains in the retriever's embedding space. We document the method lineage, the score-distribution objective, the query-normalisation gradient, the implemented selector, the FiQA-200 and HotpotQA-HardNegatives experiments, and separate project studies. Measurements retain their original query sets, candidate pools, metrics and decision status.

## 1. Problem setting

Dense retrieval encodes a query and documents as vectors and ranks the collection using similarity. A cross-encoder reranker evaluates a query-document pair jointly and returns a scalar relevance signal. The reranker can improve the ordering of candidates it receives, but cannot introduce a document that was never retrieved. Moreover, in many deployments the model weights, internal activations or training pipeline are not accessible.

The project studies a narrower interface. We assume access to (i) the query embedding, (ii) stored document embeddings, (iii) a black-box reranker score for selected pairs, and (iv) a search operation accepting a modified query vector. The embedding and reranking models remain frozen. Only an external query-space vector is optimised at inference time.

For query \(q\), let \(x_q,z_d\in\mathbb R^p\) be unit-normalised query and document vectors. The initial score and candidate pool are

\[
s_0(q,d)=x_q^\top z_d,\qquad C_M(q)=\operatorname{TopM}_{d\in\mathcal D}s_0(q,d).
\]

A selector \(\pi\) returns a feedback set \(S_\pi(q)\subseteq C_M(q)\) of fixed size \(B\). The reranker returns \(r_i=R(q,d_i)\) for each selected document. The principal experiments use \(M=50\), \(B=10\), and \(p=1024\). The corrected query searches the full collection again. This is different from direct reranking, which sorts only the supplied document IDs.

## 2. Method lineage

### 2.1 Classical relevance feedback

Classical vector-space relevance feedback, including the Rocchio family, changes a query representation using evidence from relevant and non-relevant documents. The broad geometric intuition is to move the query toward evidence judged useful and away from evidence judged unhelpful. Modern neural systems replace explicit user labels with pseudo-feedback from a learned cross-encoder, but the operational objective remains query refinement before another search.

### 2.2 TOuR

TOuR studies test-time query representation optimisation for dense retrieval using cross-encoder pseudo-feedback. Its hard and soft variants encode feedback at different levels of granularity. The query representation is updated and retrieval is executed again. TOuR is an antecedent for inference-time query optimisation; its hard/soft distinction should not be attributed to ReFIT.

### 2.3 ReFIT

ReFIT uses reranker feedback to refine a query representation and re-runs retrieval. Its practical contribution for this project is the separation between expensive teacher scoring and cheaper inner-loop optimisation: a fixed set of reranker scores can be reused during multiple query updates. The SCIDOCS ReFIT experiment in this project is separate from the DISCo–TTT-Embed experiments.

### 2.4 TTT-Embed

TTT-Embed represents the adaptation as an additive residual in the output embedding space and studies sharing scopes. Query-wise adaptation fits one residual for one rewarded query; task-wise adaptation shares a residual within a task; global adaptation shares across tasks. The main FiQA and H8 experiments use query-wise fitting.



### TOuR hard and soft query gradients (original method equations)

TOuR forms candidate probabilities from query–context inner products. Its **hard** variant identifies the smallest set of teacher-preferred contexts whose cumulative cross-encoder softmax probability exceeds a mass threshold \(p\). If \(C^{+}\) denotes this pseudo-positive set, TOuR-hard optimises

\[
\mathcal L_{\mathrm{hard}}(q)=-\log\sum_{c\in C^+} P_{\mathrm{retriever}}(c\mid q),
\qquad q_{t+1}=q_t-\eta\nabla_q\mathcal L_{\mathrm{hard}}.
\]

TOuR-soft preserves the reranker's graded preferences as \(P_{\mathrm{teacher}}\) and minimises \(D_{\mathrm{KL}}(P_{\mathrm{teacher}}\|P_{\mathrm{retriever}})\). With frozen context vectors \(c_i\), the soft update has the interpretable form

\[
q_{t+1}=q_t+\eta\sum_i\Big(P_{\mathrm{teacher}}(c_i\mid q_t)-P_{\mathrm{retriever}}(c_i\mid q_t)\Big)c_i.
\]

A higher teacher than student probability attracts the query toward that context; the converse contributes an opposing direction. TOuR may retrieve a new candidate set after each query-gradient step. These are source-paper Eqs. 8–13 (Sung et al., ACL Findings 2023), not newly run project results.

### ReFIT score normalisation and its gradient

ReFIT caches a single slate of reranker scores, then optimises the **query vector itself** (not a separately shared residual) to match the reranker's relevance distribution. Its reported implementation performs **min–max normalisation separately** on retriever scores and cross-encoder scores. Because cross-encoder scores can be sharply concentrated, it uses teacher softmax temperature \(T=2\). It then minimises

\[
\mathcal L_{\mathrm{ReFIT}}(q)=D_{\mathrm{KL}}\big(\operatorname{softmax}(\widehat{R}/T)\,\|\,\operatorname{softmax}(\widehat{s}(q))\big)
\]

and updates \(q_{t+1}=q_t-\eta\nabla_q\mathcal L_{\mathrm{ReFIT}}\) for 100 steps with learning rate 0.005 in the reported setup. The teacher is a fixed score distribution; the available derivative is through the retriever score function and query vector, **not through the black-box reranker**. ReFIT then issues a second search. Where separate min–max scaling is applied during optimisation, the derivative must account for that scaling; it should not be replaced with the unnormalised cosine-softmax gradient without stating the simplification. See ReFIT §§3.2 and 4.1 (Reddy et al., arXiv:2305.11744v2).

### TTT-Embed sharing scopes

The original framework distinguishes exactly three reward-reuse scopes: **global-wise** (one residual shared across tasks), **task-wise** (shared over rewarded queries from one task), and **query-wise** (a separate residual for each query). The term *local* is a descriptive contrast to global reuse, not a fourth named central scope. Our DISCo-feedback FiQA and H8 experiments used **query-wise** updates. The task-wise FiQA cross-fit is a separate experiment and must not be merged with them.

## 3. Query-wise TTT-Embed objective

For one query, omit the query subscript and let \(S=\{d_1,\ldots,d_B\}\). The teacher distribution is formed from the reranker scores:

\[
p_i^T=\frac{\exp(r_i/\tau_T)}{\sum_{j=1}^{B}\exp(r_j/\tau_T)},\qquad \tau_T=0.02.
\]

For candidate residual \(v\), define \(u(v)=\operatorname{unit}(x+v)\). The student distribution uses the frozen retriever document vectors:

\[
p_i^S(v)=\frac{\exp(u(v)^\top z_i/\tau_S)}
{\sum_{j=1}^{B}\exp(u(v)^\top z_j/\tau_S)},\qquad \tau_S=0.05.
\]

The loss is forward KL plus ridge regularisation:

\[
\mathcal L(v)=\sum_{i=1}^{B}p_i^T\log\frac{p_i^T}{p_i^S(v)}
+\lambda\|v\|_2^2,\qquad \lambda=0.3.
\]

The teacher probabilities are fixed during optimisation. The student probabilities change with \(v\). Softmax converts two score lists with different scales into distributions over the same selected document IDs. Temperature controls concentration; it does not make the two underlying scoring models equivalent.

### 3.1 Gradient through query normalisation

Let \(a=x+v\), \(u=a/\|a\|_2\). The Jacobian of normalisation is

\[
J(a)=\frac{\partial u}{\partial a}=\frac{I-uu^\top}{\|a\|_2}.
\]

For student logit \(\ell_i=u^\top z_i/\tau_S\), the derivative of the KL term with respect to \(\ell_i\) is \(p_i^S-p_i^T\). Therefore,

\[
\nabla_v\mathcal L(v)=
\frac{I-uu^\top}{\tau_S\|x+v\|_2}
\sum_{i=1}^{B}(p_i^S-p_i^T)z_i+2\lambda v.
\]

The reranker is not differentiated through. Its scalar scores are constants. The gradient uses accessible Qwen document vectors and the student–teacher probability difference.

### 3.2 Optimisation and deployment

The FiQA implementation initialises each residual at zero and performs 300 full-batch Adam steps at learning rate 0.01. The same ten teacher targets are reused throughout the inner loop. This is a finite numerical iterate, not an exact symbolic minimiser.

TTT-Embed's deployment coefficient is \(\alpha_g=n_g/(n_g+1)\), where \(n_g\) is the number of distinct rewarded queries in a sharing group. Query-wise fitting has \(n_g=1\), hence \(\alpha=0.5\):

\[
x_{\mathrm{new}}=\operatorname{unit}(x+0.5v_{300}).
\]

For every stored document vector,

\[
x_{\mathrm{new}}^\top z_d=
\frac{x^\top z_d+0.5v_{300}^\top z_d}{\|x+0.5v_{300}\|_2}.
\]

For a fixed query, the denominator is common across documents. The ranking is therefore induced by the original similarity plus the residual's projection onto each document vector. This is why the final evaluation searches the full corpus again, including unscored documents.

## 4. Complementary feedback selection

### 4.1 Collective coverage

DISCo studies set-level collective coverage of contextual query-token representations. Let \(Q=\{u_1,\ldots,u_m\}\) be query token vectors and \(X_d\) the contextual token vectors for document \(d\). A coverage objective can be written as

\[
F(S,Q)=\sum_{j=1}^{m}\max_{t\in\cup_{d\in S}X_d}u_j^\top t.
\]

Greedy selection adds the document with the largest marginal increase in the objective. This differs from independent per-document MaxSim: the marginal value of a document depends on what the selected set already covers.

### 4.2 Implemented selector

The FiQA and H8 experiments apply exact greedy coverage within the shared Qwen dense top-50 pool. Frozen `bert-base-uncased` contextual tokens are used for selection; special and padding tokens are excluded and retained vectors are normalised. Define

\[
h_j(d)=\max_{t\in X_d}\cos(u_j,t),\qquad
F_q(S)=\sum_j\max(0,\max_{d\in S}h_j(d)).
\]

Starting with \(S_0=\varnothing\), the selector repeatedly chooses

\[
d_{t+1}\in\arg\max_{d\in C_{50}(q)\setminus S_t}
\left[F_q(S_t\cup\{d\})-F_q(S_t)\right],
\]

until ten distinct IDs have been selected. Ties are resolved by original dense rank. BERT supplies selection features; the selected IDs identify Qwen document vectors used in TTT-Embed. The BERT and Qwen vectors are not mixed.

This is a DISCo-inspired fixed-pool selector, not a reproduction of the original DISCo specialised corpus index. The first-stage Qwen dense retriever remains in place.

### 4.3 Geometric hypothesis

The TTT gradient depends on the teacher–student probability difference weighted by the selected Qwen document vectors. A complementary selection policy can therefore change the directions available to the residual update. However, the coverage selector operates on BERT contextual-token features while the residual is fitted in Qwen's vector space. A newly covered token aspect helps only if its selected documents are relevant and their Qwen vectors provide useful directions under the teacher–student discrepancy. This is a hypothesis to test, not a guarantee that diversity improves retrieval.

## 5. FiQA-200 experiment

The FiQA2018 collection contains 57,638 documents. The experiment uses 200 predetermined query IDs selected by hash ordering without using relevance labels. Qwen3-Embedding-0.6B retrieves a common dense top-50 pool. Each selection arm supplies ten documents to Qwen3-Reranker-4B. A separate query-wise residual is fitted for each query and arm, then the corrected query searches all 57,638 stored document vectors again.

The comparison includes raw dense retrieval, dense top-ten TTT, DISCo-style coverage TTT, MMR TTT, hybrid TTT, BERT MaxSim TTT and BM25 TTT. Additional controls include rank-matched and uniform-random selection and direct teacher sorting. The query set had prior project exposure; the result is exploratory.

### 5.1 Recorded full-corpus metrics

| Feedback method | nDCG@10 | Recall@10 | Recall@100 |
|---|---:|---:|---:|
| Raw dense | 0.461751 | 0.540268 | 0.782553 |
| Dense first ten + TTT | 0.505956 | 0.583074 | 0.803775 |
| Coverage ten + TTT | 0.480703 | 0.567483 | 0.799134 |
| MMR ten + TTT | 0.504594 | 0.564463 | 0.813528 |
| Hybrid ten + TTT | 0.500191 | 0.562087 | 0.808704 |
| BERT MaxSim ten + TTT | 0.488074 | 0.568472 | 0.801718 |
| BM25 ten + TTT | 0.462804 | 0.541671 | 0.808585 |

Coverage TTT minus dense TTT is −0.025253 nDCG@10, with exploratory paired percentile-bootstrap interval [−0.043324, −0.007492]. Coverage TTT minus the mean rank-matched control is +0.004556, with interval [−0.012944, +0.023087]. Coverage beats dense-feedback TTT on 30 queries, ties on 109 and loses on 61.

The mean overlap between dense and coverage feedback sets is 3.99 documents. The adapted top-ten output lists overlap by 7.655 documents on average.

### 5.2 Stage-level diagnostics

| Diagnostic | Dense first ten | Coverage ten |
|---|---:|---:|
| Judged feedback-set recall | 0.540268 | 0.397735 |
| Queries with ≥1 judged feedback document | 152/200 | 128/200 |
| Mean initial dense rank selected | 5.50 | 19.73 |
| Teacher target effective support | 3.957 | 2.893 |
| Mean correction-vector norm | 0.3491 | 0.3347 |

The initial top-50 pool has mean judged Recall@50 0.718097 and oracle nDCG@10 0.757200. Relative to dense-feedback TTT, coverage gains 16 judged-positive top-ten query-document events and loses 17. Six gains are selected feedback documents; ten are unselected documents inside the original top-50. At top-100, coverage gains nine and loses nine; all nine gains are outside the initial top-50. These are query-document events, not unique documents.

### 5.3 Query-level cases

For the education-loan query 603, judged document 456440 moves from raw rank 27 to dense-TTT rank 10 and coverage-TTT rank 1. Coverage selected it and assigned \(P_{\mathrm{yes}}=0.987568\). The passage is comparatively generic, so human adjudication is needed before calling it a better answer to the complete query.

For the Facebook-public-listing query 3801, judged document 390529 moves 12 → 5 → 1. MMR and hybrid also reach the same nDCG on this query; it does not isolate coverage as the unique cause.

For the LLC query 895, judged document 416268 is rank 1 in raw retrieval and dense TTT, but coverage places it at rank 3. For the Roth IRA query 8512, judged document 32811 moves 2 → 1 → 2. The casebook contains these and the full 200-query record; examples are not a substitute for aggregate results.

## 6. HotpotQA-HardNegatives H8

H8 uses the MTEB HotpotQAHardNegatives collection with 225,621 documents, 1,000 queries and 2,000 relevance judgements. The 400-query development group was fixed as the preregistered decision set; the later 600-query group was evaluated after the development decision. Both groups use the same frozen hyperparameters and feedback budget.

| Arm | DEV400 | Later 600 | Pooled 1,000 |
|---|---:|---:|---:|
| Raw dense | 0.6557 | 0.6775 | 0.6688 |
| Dense top-ten TTT | 0.7195 | 0.7447 | 0.7346 |
| Coverage TTT | 0.7298 | 0.7628 | 0.7496 |
| MMR TTT | 0.6956 | 0.7187 | 0.7094 |
| K-centre TTT | 0.6679 | 0.6932 | 0.6831 |
| D-optimal TTT | 0.6670 | 0.6884 | 0.6798 |
| Random TTT (20 draws) | 0.6536 | 0.6735 | 0.6655 |

Coverage TTT minus dense TTT is +0.0103 [−0.0041, +0.0251] on DEV400; +0.0181 [+0.0062, +0.0303] on the later 600; and +0.0150 [+0.0057, +0.0245] pooled. The preregistered DEV400 interval includes zero, so the registered decision gate was not passed. The later 600 is post-decision exploratory evidence; the pooled value is descriptive and does not replace the preregistered decision.

The H8 experiment also includes shuffled-teacher controls. Its separate standalone HotpotQA coverage diagnostic is not the same task: it selects two supporting paragraphs from ten supplied paragraphs, with no reranker and no TTT residual. Both-support selection was 124/400 (31.0%) for dense top-two, 194/400 (48.5%) for unnormalised DISCo-style coverage, 142/400 (35.5%) for length-normalised coverage, and 82/400 (20.5%) for MMR. These percentages must not be merged with H8 nDCG.

## 7. Other project experiments (separate protocols)

A FiQA task-wise cross-fit covers all 648 queries using five folds. A shared task residual is fitted on 80% of queries in each fold and evaluated on the held-out 20%. Recorded nDCG@10 is 0.46722 for raw retrieval and 0.46313 for the shared-residual arm; paired difference −0.00408 [−0.01072, +0.00262]. This is not the query-wise FiQA-200 experiment.

The SCIDOCS ReFIT run covers 1,000 queries, 25,657 documents and 4,928 positive judgements. Frozen Contriever-MSMARCO and MiniLM-L6 checkpoints were used. Recorded Recall@100 is 37.8067% for raw Contriever, 38.3450% for direct rerank-125, and 37.8717% for ReFIT query adaptation. It is a separate ReFIT study.

The earlier ANN pilot trained ANCE branches on a positive-enriched 50,000-passage MS MARCO subset, using HNSW or IVF-Flat candidates and MiniLM-L6 teacher scores. The SciFact frozen-cache comparison reused existing embeddings and teacher-score caches. These studies update different objects or use different protocols and are not part of the DISCo–TTT-Embed main comparison.

## 8. Evidence boundaries and next analyses

The completed FiQA and H8 runs test DISCo-inspired feedback selection within a dense top-50 candidate pool. They do not test the original DISCo index as a replacement first-stage retriever. BM25 and hybrid feedback are separate arms in FiQA; they are not evidence that a new complementary first-stage retrieval system has been evaluated.

A useful archival follow-up is to compare the teacher-score distributions on dense and coverage slates query by query, inspect overlap and relevance judgements, and link those differences to the fitted residual and subsequent document rank changes. A true complementary first-stage retrieval experiment should be registered separately, with candidate-pool recall, matched teacher budget and a full-corpus second search.

No final research conclusion is supplied here; the author will provide the closing interpretation.

## References

1. Mujeen Sung et al. *Optimizing Test-Time Query Representations for Dense Retrieval*. Findings of ACL, 2023. https://aclanthology.org/2023.findings-acl.354/
2. Revanth Gangi Reddy et al. *ReFIT: Relevance Feedback from a Reranker during Inference*. arXiv:2305.11744. https://arxiv.org/abs/2305.11744
3. Tianyu Chen and Jiaxing Wu. *Test-Time Optimization of Query Embeddings with Ranking Aware Reward Maximization*. arXiv:2608.12569. https://arxiv.org/abs/2608.12569
4. Kartik Nair et al. *A Dense Subset Index for Collective Query Coverage*. ICLR, 2026. https://openreview.net/forum?id=cUdODCFjUM
5. Gerard Salton, Edward A. Fox and Harry Wu. *The SMART Retrieval System—Experiments in Automatic Document Processing*. 1971.
6. Ceous experiment record. FiQA-200 complementary feedback selection, 16 November 2026. Task `ire-disco-tttembed-selection-20261116-0700`; records include `RESULTS.md`, `RUN_SPEC.md`, `fit_querywise.py` and `selection_arms.py`.
7. Ceous experiment record. H8 DISCo-guided feedback selection for TTT-Embed on HotpotQA-HardNegatives, 16 November 2026. Task `ceous-disco-ttt-20261116-0820`.
8. Ceous experiment record. Standalone HotpotQA complementary-evidence diagnostic, 15 November 2026.


## Visual provenance

The V4 presentation reuses three **genuine Manim-rendered videos** from the preceding reviewed edition: `FrozenFeedback`, `CollectiveCoverage`, and `QueryResidual`. Their original Python scene definitions are provided in `manim-scenes.py`; the MP4 files and exported static figures are included with the website. The animated values and 2-D geometry are **illustrative**, and the scenes were **not freshly rendered** for V4. The temperature examples and KL-curve illustrations elsewhere in the earlier V3 build were ordinary plots, not Manim renders or measured optimiser traces.
