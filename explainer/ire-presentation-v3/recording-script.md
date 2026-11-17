# Ceous: Efficient Retrieval Adaptation from Limited Reranker Feedback
## Recording script · V3 · 25 main slides + 5 appendix slides

**Timing:** approximately 20–22 minutes at a measured academic speaking pace.  
**Audience:** an IR researcher and a technically curious listener without prior exposure to TTT-Embed.  
**Evidence rule:** published method descriptions, our executed experiments, mathematical illustrations and future hypotheses are explicitly distinguished.  
**Closing interpretation:** intentionally left to the author.

### Slide 01 — Ceous: Efficient Retrieval Adaptation from Limited Reranker Feedback

We study how to adapt retrieval at inference time while keeping the embedding model and reranker frozen. The central question is whether a limited set of black-box reranker scores can be converted into a query representation that retrieves better from the full corpus. Our specific experiment changes which documents supply feedback to TTT-Embed: ordinary dense top-ranked documents versus a DISCo-inspired complementary selection policy.

### Slide 02 — The deployment constraint

In a deployed system, the retriever and reranker may be accessible only through interfaces. We can submit a query, retrieve candidates and observe scalar relevance scores, but we may not have permission to update model weights or inspect internal gradients. Full retraining can also require data, compute, deployment coordination and regression testing. The setting here is narrower: adapt one query at inference time using outputs the system already exposes.

### Slide 03 — A reranker cannot rescue a document it never sees

Dense retrieval compares a query vector with the stored document vectors and returns a candidate pool. A cross-encoder reranker can judge each supplied query-document pair more carefully, but it only reorders that supplied pool. If a relevant document is absent, reranking cannot introduce it. This motivates using reranker feedback to modify the query and then searching the full collection again.

### Slide 04 — Relevance feedback has a long history

The underlying intuition predates neural retrieval. Classical vector-space relevance feedback, associated with Rocchio, moves a query representation toward relevant documents and away from non-relevant ones. Pseudo-relevance feedback applies a similar idea when relevance labels are not explicitly supplied by a person. Modern systems replace manually supplied labels with a learned reranker, but the operational question remains: how should evidence change the query used for the next search?

### Slide 05 — Inference-time adaptation: use the evidence already available

Inference-time adaptation is useful when a system needs to respond to a particular query without updating and redeploying the underlying model. In retrieval, the query is already a compact representation of the information need. If feedback tells us which candidates better satisfy that need, we can use it to refine the query representation and issue another search. This is a local, request-time operation; it is not a claim that retraining is never useful.

### Slide 06 — TOuR: optimise a test-time query representation

TOuR makes query adaptation explicit for dense retrieval. It uses cross-encoder feedback on retrieved passages to define an objective for changing the test query representation. The updated query is then used for retrieval again. The important conceptual move is that a frozen retrieval model can still produce a different ranking because the input representation used for search has changed.

### Slide 07 — TOuR-hard and TOuR-soft

The hard variant turns feedback into a more discrete positive-versus-negative signal. The soft variant retains graded teacher preferences rather than collapsing them to a single binary target. This distinction matters because a reranker often knows that one candidate is much better than another, while several candidates may all be partially useful. Keeping relative preference information can provide a richer training target for the query update.

### Slide 08 — ReFIT: reuse reranker scores during query optimisation

ReFIT develops reranker-guided relevance feedback at inference time. Its practical usefulness is that the expensive reranker scores for a selected candidate set can be reused while the query representation is optimised. The inner optimisation does not require a fresh reranker call at every step. This separates expensive teacher inference from cheaper vector optimisation and a subsequent retrieval operation.

### Slide 09 — What the lineage contributes

These methods should not be treated as interchangeable names. TOuR established test-time query optimisation with hard and soft feedback variants. ReFIT distils reranker relevance information into a query representation while reusing teacher scores. TTT-Embed formulates an additive residual in the embedding output space and studies how that residual can be shared across queries or tasks. Our main experiments use the TTT-Embed query-wise objective.

### Slide 10 — TTT-Embed: represent adaptation as an external residual

Let x be the frozen query embedding and z_d a frozen document embedding. TTT-Embed introduces an external vector v and forms a corrected query from x and v. The vector is fitted so that the retriever's distribution over feedback documents approaches the reranker's preference distribution. This gives a compact adaptation state in the same output space used by the retriever. The encoder and stored document vectors remain unchanged.

### Slide 11 — What does the residual change geometrically?

The residual is a direction in the retriever's embedding space. Once added to the query and normalised, it changes the cosine similarity between that query and every stored document vector. A document does not need to have received reranker feedback to benefit from the changed ranking. The denominator from normalisation is common to all documents for one query, so the ranking is governed by the original score plus the residual's projection onto each document vector.

### Slide 12 — Why turn scores into a distribution?

The reranker may return scalar scores whose absolute range is not directly comparable with the retriever's cosine similarities. TTT-Embed converts the selected teacher scores into a probability distribution with softmax and a temperature. The temperature controls concentration: a smaller value puts more mass on the highest-scoring items, while a larger value spreads probability more evenly. The student uses its own temperature because its score scale and desired sharpness are separate modelling choices.

### Slide 13 — KL divergence turns preferences into a fitting objective

The teacher distribution is fixed after reranker scoring. The student distribution changes as v changes. Forward KL divergence, DKL(p_T || p_S), penalises the student when it assigns too little probability to items the teacher prefers. A ridge term discourages unnecessarily large residuals. We optimise only v, using Adam. The curve shown here is a mathematical illustration of the objective, not a logged loss trace from the experiment.

### Slide 14 — Query-wise, task-wise and global adaptation

TTT-Embed studies different scopes for sharing the residual. Query-wise adaptation fits one vector from one query's feedback. Task-wise adaptation shares a vector across rewarded queries in a task. Global adaptation shares across tasks. Sharing can pool more feedback, but it also assumes that different queries or tasks benefit from a common direction. Our DISCo-feedback FiQA and H8 experiments use query-wise fitting; the separate task-wise FiQA cross-fit is a different experiment.

### Slide 15 — Complementary retrieval: retrieve evidence with different strengths

A query may ask about several entities, relations or constraints. Dense retrieval can return several passages that are individually similar but repeat the same aspect. Complementary retrieval tries to obtain evidence with different strengths: lexical retrieval can recover exact terms, diversification can reduce redundancy, and aspect-coverage methods can represent multiple facets. Examples include MMR, xQuAD or IA-Select, hybrid BM25-plus-dense retrieval, and collective token coverage.

### Slide 16 — ColBERT and DISCo are related, but not the same

ColBERT-style late interaction scores a document by matching each query token to its best document-token match. That score is computed per document. DISCo instead selects a set whose union collectively covers the query-token representations. Once an aspect is already covered by the selected set, another document repeating it contributes less marginal coverage. This is why DISCo is relevant to feedback-set construction, but it does not automatically guarantee relevance.

### Slide 17 — DISCo: select a set for collective query-token coverage

DISCo represents query and document content with contextual token vectors. For each query token, the set receives credit for its best matching token across all selected documents. A greedy algorithm adds the candidate with the largest marginal increase in this objective. In a multi-hop question, one passage may cover the first entity or relation while another supplies the second piece of evidence. The selected set is judged collectively rather than one document at a time.

### Slide 18 — Why complementary feedback can change the residual

The TTT-Embed gradient depends on the difference between student and teacher probabilities, weighted by the selected Qwen document vectors and projected through query normalisation. If the selected set contains repeated evidence, those vectors may provide a narrow or redundant set of directions. A complementary set may expose additional directions. But coverage is calculated using BERT token representations, while the residual is fitted in Qwen's embedding space. The hypothesis therefore requires alignment: a newly covered aspect must also be relevant and informative in the Qwen space. This is a mechanism to test, not a guarantee.

### Slide 19 — Two different meanings of DISCo + TTT-Embed

Our completed FiQA and H8 implementation first retrieves a dense top-fifty pool with Qwen. BERT contextual-token coverage selects ten documents inside that pool. The Qwen reranker scores those ten, and query-wise TTT-Embed fits the residual. This tests the feedback-selection principle. It does not replace the initial Qwen retriever with the original DISCo corpus index. A true complementary first-stage retriever that discovers candidates outside the dense pool is a distinct experiment and has not been run here.

### Slide 20 — FiQA-200: controlled feedback-selection experiment

The FiQA experiment uses the full 57,638-document collection and 200 predetermined queries. Qwen3-Embedding-0.6B supplies a common dense top-fifty pool. Each selector chooses ten documents; Qwen3-Reranker-4B provides the teacher scores; query-wise TTT-Embed fits an independent residual with 300 Adam steps. The corrected query searches the complete corpus again. The primary metric is nDCG@10 against FiQA relevance judgements. The query set had prior project exposure, so this is an exploratory paired comparison.

### Slide 21 — FiQA-200: recorded full-corpus retrieval results

Standard dense-feedback TTT records nDCG@10 of 0.505956. DISCo-style coverage TTT records 0.480703. Other recorded arms include MMR, hybrid retrieval, BERT MaxSim and BM25 feedback. The paired coverage-minus-dense TTT difference is minus 0.025253, with a descriptive paired interval from minus 0.043324 to minus 0.007492. Coverage minus rank-matched TTT is plus 0.004556, with an interval spanning zero. These are the archived experiment values; no new run is implied.

### Slide 22 — Query-level examples: promotions and regressions

The casebook contains query-level rank transitions. For the education-loan query, a judged document moves from raw rank 27 to dense-TTT rank 10 and coverage-TTT rank 1; the coverage reranker score was 0.987568. For the LLC query, a judged document already at raw rank 1 remains rank 1 under dense TTT but moves to rank 3 under coverage TTT. These cases illustrate both a promotion and a regression. They do not by themselves establish why the selector chose the document; the saved archive does not include every token-level marginal coverage contribution.

### Slide 23 — HotpotQA-HardNegatives: a second DISCo-guided TTT study

The H8 experiment uses the MTEB HotpotQA-HardNegatives collection with 225,621 documents and 1,000 queries. The recorded arms include dense TTT, coverage TTT, MMR, k-centre, D-optimal, random and shuffled-teacher controls. Coverage TTT records pooled nDCG@10 of 0.7496 compared with 0.7346 for dense TTT. The preregistered DEV400 difference is plus 0.0103, but its interval includes zero, so the registered decision gate was not passed. The later 600-query group is post-decision exploratory evidence.

### Slide 24 — Intermediate diagnostics and a separate coverage-only study

On FiQA, coverage selects documents at a much deeper mean dense rank than the dense top-ten arm, and its feedback-set judged recall is lower. The teacher target also has lower effective support. A separate HotpotQA diagnostic selected two supporting paragraphs from ten supplied paragraphs without reranking or TTT: dense top-two found both supports in 124 of 400 cases, while unnormalised DISCo-style coverage did so in 194 of 400. This is a different task and metric; it must not be merged with the TTT retrieval results.

### Slide 25 — Scope of the evidence and the next measurements

The completed evidence includes FiQA-200 and HotpotQA-HN H8 DISCo-inspired feedback selection with query-wise TTT-Embed. Separate project studies include task-wise FiQA cross-fitting, SCIDOCS ReFIT, SciFact frozen-cache comparisons and an earlier ANN pilot. The current evidence does not establish that an original DISCo index would outperform dense candidate generation, nor does it settle which query properties predict useful complementary feedback. The next useful analysis is a paired, query-level examination of reranker scores on dense and coverage slates, followed by a separately approved first-stage complementary-retrieval experiment.

### Slide 26 — Appendix · Method identity and terminology

The original DISCo method uses a specialized contextual-token retrieval and indexing pipeline. Our implementation borrows its collective coverage objective inside a Qwen dense top-fifty pool, using frozen BERT-base-uncased token features. The reranker and TTT-Embed are separate downstream components added by our project. This appendix records the terminology needed to avoid claiming a full DISCo reproduction.

### Slide 27 — Appendix · Additional FiQA diagnostics

The diagnostic table shows how the feedback slate differs before optimisation. Coverage's selected documents come from deeper initial dense ranks on average and contain fewer judged positives according to the qrels. The teacher distribution is also more concentrated by the effective-support measure. These values describe the inputs and fitted vectors; they do not by themselves identify a causal explanation for the aggregate retrieval difference.

### Slide 28 — Appendix · Other project experiments

The project also contains a FiQA task-wise cross-fit over all 648 queries, where a shared task residual is fitted on training folds and evaluated on held-out queries. It records nDCG@10 of 0.46722 for raw retrieval and 0.46313 for the shared residual. The SCIDOCS ReFIT experiment covers 1,000 queries and reports Recall@100 of 37.8067% for raw Contriever, 38.3450% for direct reranking and 37.8717% for ReFIT. These are separate experiments, not additional DISCo-TTT arms.

### Slide 29 — Appendix · H8 controls and paired comparisons

H8 compares several selection policies with the same general teacher-feedback budget. The development set was the preregistered decision set. Its coverage-minus-dense TTT confidence interval includes zero. The later 600-query group was evaluated after the decision, and its interval is positive. The pooled result is descriptive. We preserve all three rather than presenting the pooled value as if it were a preregistered success.

### Slide 30 — Appendix · References and reproducibility

The method lineage is grounded in the TOuR, ReFIT, TTT-Embed and DISCo papers. The local experiment records identify the FiQA and H8 runs, the selection and fitting implementations, and the separate diagnostics. Published method descriptions are not treated as evidence that our implementation reproduced every component of the original paper systems.

## Recording notes

- Do not read every equation aloud. Explain what each term does, then point to the equation.
- On slides 12–13, explicitly say the plotted softmax/KL curves are mathematical illustrations, not a saved optimisation trace.
- On slide 19, say “DISCo-inspired fixed-pool feedback selector,” not “we reproduced DISCo.”
- On slide 23, separate the preregistered DEV400 decision from the later post-decision 600.
- Do not add a final effectiveness conclusion; the author will provide the interpretation.