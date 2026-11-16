# Frozen models. Better retrieval?

Test-time retrieval with black-box reranker feedback and no model weight updates.

**Queos Labs · IRE Project · IIIT Hyderabad**

Nilanjan Sarkar, Raman Rayaprolu

16 November 2026 · First review edition

## How to use this script

Twenty pages, each intended for about one minute. The spoken text is source-grounded paraphrase, with original teaching examples, deductions and the proposed hypothesis explicitly identified in SOURCE_LEDGER.md. Pointer notes are stage directions and are not part of the narration. Read at a natural pace; pause briefly over plots. Exact durations depend on delivery.

The title states the access constraint precisely: model weights stay frozen, while a query vector or external residual is optimized. A black-box teacher remains available through its relevance scores.

Published results, reported project measurements and untested hypotheses are separately labelled. The SCIDOCS values come from project run reports with recorded hashes; the FiQA task-wise TTT pilot comes from the published working report, §4. This pass did not independently recompute either run’s raw artifacts. FiQA reports no reliable held-out gain on one previously exposed task. Neither completed measurement tests complementary selection.

## Page 01 — Frozen models. Better retrieval?

**On screen:** Test-time retrieval with black-box reranker feedback and no model weight updates.

**Evidence:** Research question · **Spoken words:** 126 · **Estimated delivery:** 58 seconds at 130 words/minute

**Takeaway:** Can better feedback change where we search?

### Spoken script

Our project asks whether a deployed retrieval system can improve at test time while both model backbones remain frozen. We assume that the embedding service returns vectors and that a reranker returns relevance scores for selected query-document pairs. The editable object is an external query representation, so the method still learns even though it does not fine-tune either model. We will follow the progression from TOUR to ReFIT and then to the reusable state in TTT-Embed. After the papers, we will inspect our SCIDOCS reproduction gap and the reported FiQA task-wise TTT pilot. Finally, can candidates covering complementary evidence teach a better residual under the same feedback budget? That last step is the hypothesis we want to test, rather than a result we can already claim.

### Pointer notes

- Open on the title, then point to “black-box feedback”.
- Emphasize that model weights stay frozen; the external vector can still change.

### Sentence provenance

- **S01.01** Project scope. Sources: [BRIEF](#presentation-scope). Location: BRIEF: User brief, 16 Nov 2026: Queos Labs IRE presentation; no encoder or reranker weight updates; source-backed script and proposed complementary-feedback study.
- **S01.02** Source-grounded paraphrase. Sources: [TTT-I](https://arxiv.org/html/2608.12569v1#S1). Location: TTT-I: Appendix §8, PDF p.13, final paragraph on the returned-embedding and downstream-search interfaces; §2.1, p.3, opening setup paragraph.
- **S01.03** Source-grounded paraphrase. Sources: [TTT-I](https://arxiv.org/html/2608.12569v1#S1), [TTT-M](https://arxiv.org/pdf/2608.12569v1#page=4). Location: TTT-I: Figure 1, PDF p.2, caption; TTT-M: §2.2, pp.3–4, Eqs.3–4, the residual is the optimization variable.
- **S01.04** Presentation structure. Sources: [BRIEF](#presentation-scope). Location: BRIEF: User brief, 16 Nov 2026: Queos Labs IRE presentation; no encoder or reranker weight updates; source-backed script and proposed complementary-feedback study.
- **S01.05** Source-grounded paraphrase. Sources: [RUN](https://github.com/nilansa/ire-project-2026/issues/3#issuecomment-6908737534), [RUN-CI](https://github.com/nilansa/ire-project-2026/issues/3#issuecomment-6909019011), [FIQA_RUN](https://github.com/nilansa/ire-project-2026/blob/main/research/CEOUS_COMPLEMENTARY_FEEDBACK_2PAGE_WORKING_20261116.md#4-completed-ceous-measurements-not-directly-comparable). Location: RUN and RUN-CI: completed SCIDOCS report and bootstrap interval. FIQA_RUN: working report §4, FiQA task-wise TTT-Embed row; this is a reported project pilot, not independently recomputed evidence.
- **S01.06** Our hypothesis. Sources: [HYPOTHESIS](#hypothesis). Location: HYPOTHESIS: SOURCE_LEDGER.md, Hypothesis boundary. Coverage-aware selection may improve residual learning at fixed teacher budget. This combination is proposed here, not established by DISCo, TTT-Embed or our completed runs.
- **S01.07** Claim boundary. Sources: [HYPOTHESIS](#hypothesis). Location: HYPOTHESIS: SOURCE_LEDGER.md, Hypothesis boundary. Coverage-aware selection may improve residual learning at fixed teacher budget. This combination is proposed here, not established by DISCo, TTT-Embed or our completed runs.

## Page 02 — What should expensive feedback buy us?

**On screen:** The Microsoft research challenge is the starting point.

**Evidence:** Research motivation · **Spoken words:** 126 · **Estimated delivery:** 58 seconds at 130 words/minute

**Takeaway:** We narrow the problem to useful adaptation after deployment.

### Spoken script

The Microsoft challenge asks how high-quality reward feedback can improve retrieval models and downstream retrieval or generation. It identifies three practical questions: which query-document pairs deserve scoring, which learning loss should use those scores, and how to control computational cost. These decisions are connected: a powerful teacher helps only when we spend its judgments well. Our project narrows that broad post-training agenda to a deployed system with frozen model weights and a fixed document index. The question becomes what can be learned outside those models, directly from the feedback available at inference. The literature supplies several query-update mechanisms, while our proposed study returns to the first Microsoft question: which documents should receive expensive feedback? This is our scoped research problem, not a method prescribed by Microsoft.

### Pointer notes

- Move across “Select → Learn → Spend”.
- End on the selection column; it returns near the end of the talk.

### Sentence provenance

- **S02.01** Source-grounded paraphrase. Sources: [MSR](https://www.microsoft.com/en-us/research/academic-program/microsoft-research-fellowship/research-challenges/). Location: MSR: supplied challenge text, Summary, sole paragraph.
- **S02.02** Source-grounded paraphrase. Sources: [MSR](https://www.microsoft.com/en-us/research/academic-program/microsoft-research-fellowship/research-challenges/). Location: MSR: Description, research questions (1) Data Selection, (2) Loss Formulation, and (3) Computational Efficiency.
- **S02.03** Our synthesis. Sources: [MSR](https://www.microsoft.com/en-us/research/academic-program/microsoft-research-fellowship/research-challenges/). Location: MSR: our synthesis of research questions (1)–(3), not a separately reported paper finding.
- **S02.04** Project scope. Sources: [BRIEF](#presentation-scope), [TTT-I](https://arxiv.org/html/2608.12569v1#S1). Location: BRIEF: user-requested no-weight-update setting. TTT-I: §2 opening paragraph, PDF p.3, fixed backbone and index.
- **S02.05** Our synthesis. Sources: [BRIEF](#presentation-scope), [TTT-I](https://arxiv.org/html/2608.12569v1#S1). Location: BRIEF: our problem formulation. TTT-I: Introduction, paragraph on learning an external vector from returned embeddings.
- **S02.06** Our synthesis. Sources: [MSR](https://www.microsoft.com/en-us/research/academic-program/microsoft-research-fellowship/research-challenges/), [HYPOTHESIS](#hypothesis). Location: MSR: question (1), Data Selection. HYPOTHESIS: our candidate-selection proposal; the Microsoft challenge does not name it.
- **S02.07** Claim boundary. Sources: [BRIEF](#presentation-scope). Location: BRIEF: User brief, 16 Nov 2026: Queos Labs IRE presentation; no encoder or reranker weight updates; source-backed script and proposed complementary-feedback study.

## Page 03 — What can we change at inference?

**On screen:** Black box means an output interface is available; internal weights and gradients are not required.

**Evidence:** Problem setting · **Spoken words:** 126 · **Estimated delivery:** 58 seconds at 130 words/minute

**Takeaway:** Frozen encoders. Frozen reranker. Editable vector.

### Spoken script

There are three interfaces in our setting: an embedding service, a document-vector index, and a relevance-scoring teacher. We can read their outputs and issue another vector search, but we do not update encoder weights, reranker weights, or stored document embeddings. Instead, we optimize a small vector after the embedding service has produced its answer. An inaccessible retriever cannot be fine-tuned through a vector-only interface. A black-box reranker by itself does not prevent training an accessible retriever, because its scores can still supply targets. Our restriction is therefore no model weight updates, with output access sufficient for external optimization. If a service returns only document identifiers and offers no vector interface, this assumption may fail. Keep that boundary in mind when applying the method to closed models.

### Pointer notes

- Point to the two locked model boxes, then the blue external vector.
- Read the allowed interface row; do not say that the teacher is unavailable.

### Sentence provenance

- **S03.01** Source-grounded paraphrase. Sources: [TTT-I](https://arxiv.org/html/2608.12569v1#S1). Location: TTT-I: §2.1, PDF p.3, opening paragraph; Appendix §8, PDF p.13, final access-assumptions paragraph.
- **S03.02** Source-grounded paraphrase. Sources: [TTT-I](https://arxiv.org/html/2608.12569v1#S1), [TTT-M](https://arxiv.org/pdf/2608.12569v1#page=4). Location: TTT-I: Figure 1 caption, PDF p.2; §2 opening paragraph, p.3. TTT-M: §2.2 Eq.4 optimizes only the external residual.
- **S03.03** Source-grounded paraphrase. Sources: [TTT-M](https://arxiv.org/pdf/2608.12569v1#page=4). Location: TTT-M: §2.2, PDF pp.3–4, Eq.3 (vector addition) and Eq.4 (residual objective).
- **S03.04** Source-grounded paraphrase. Sources: [TTT-I](https://arxiv.org/html/2608.12569v1#S1). Location: TTT-I: Introduction paragraph on parameter access; Appendix §8 final paragraph. Claim is restricted to a vector-only API, not all services called black boxes.
- **S03.05** Logical clarification. Sources: [DERIVATION](#derivation). Location: DERIVATION: Source ledger, output-interface reasoning. This follows from scores being usable targets when a separate retriever is trainable; it is a clarification, not an experiment.
- **S03.06** Project scope. Sources: [BRIEF](#presentation-scope), [TTT-I](https://arxiv.org/html/2608.12569v1#S1). Location: BRIEF: user-requested frozen-model scope. TTT-I: Appendix §8 final paragraph, output access and control of vector search.
- **S03.07** Source-grounded paraphrase. Sources: [TTT-I](https://arxiv.org/html/2608.12569v1#S1). Location: TTT-I: Appendix §8, PDF p.13, final paragraph distinguishing the returned-vector setting from a service exposing only ranked identifiers.
- **S03.08** Explanation. Sources: [TTT-I](https://arxiv.org/html/2608.12569v1#S1). Location: TTT-I: Appendix §8 final paragraph; explanatory reminder of the stated interface boundary.

## Page 04 — Why is reranking not enough?

**On screen:** A stronger judge can only reorder the candidates it receives.

**Evidence:** Method premise · **Spoken words:** 129 · **Estimated delivery:** 60 seconds at 130 words/minute

**Takeaway:** A missed document needs another retrieval step.

### Spoken script

A dense retriever quickly searches precomputed document vectors and returns a short candidate list. A cross-encoder reranker reads each query-document pair jointly and assigns a more detailed relevance score. In the diagram, the relevant document outside the candidate boundary never reaches that judge. Reordering a fixed set of K documents can improve their order, but cannot change Recall at K for that same set. Reranking 125 documents and keeping 100 can improve Recall at 100, making it a useful comparator. The feedback question is whether the scores can change the query vector and send it back into the full index. That second search could retrieve an item absent from the first list, rather than only reshuffling documents already seen. The next methods turn this possibility into an optimization procedure.

### Pointer notes

- Point to the outlined candidate set, then the single relevant item outside it.
- Trace the second-search arrow back into the full corpus.

### Sentence provenance

- **S04.01** Source-grounded paraphrase. Sources: [REFIT-I](https://arxiv.org/html/2305.11744v2#S1). Location: REFIT-I: §3.1, PDF p.2, paragraph after Eq.3 on precomputed passage embeddings and nearest-neighbor retrieval.
- **S04.02** Source-grounded paraphrase. Sources: [REFIT-I](https://arxiv.org/html/2305.11744v2#S1). Location: REFIT-I: §3.1, PDF p.3, reranker paragraph before Eq.4; Introduction, paragraph comparing dual and cross encoders.
- **S04.03** Illustrative explanation. Sources: [DERIVATION](#derivation). Location: DERIVATION: original candidate-set schematic. The unseen relevant item is an illustrative example, not a retrieved case from the papers.
- **S04.04** Source-grounded paraphrase. Sources: [REFIT-I](https://arxiv.org/html/2305.11744v2#S1). Location: REFIT-I: Abstract ¶1 and Introduction opening paragraph. Fixed-set cardinality qualifier makes the Recall@K claim precise.
- **S04.05** Source-grounded paraphrase. Sources: [REFIT-M](https://arxiv.org/pdf/2305.11744v2#page=3). Location: REFIT-M: §4.2, PDF pp.3–4, final comparison-design paragraph: retrieve/rerank125 but evaluate Recall@100.
- **S04.06** Source-grounded paraphrase. Sources: [REFIT-I](https://arxiv.org/html/2305.11744v2#S1). Location: REFIT-I: Figure 1 and Introduction paragraph describing inference-time distillation followed by second retrieval.
- **S04.07** Source-grounded paraphrase. Sources: [REFIT-I](https://arxiv.org/html/2305.11744v2#S1). Location: REFIT-I: Figure 1 caption and Introduction distillation paragraph; possibility of discovery is not a per-query guarantee.
- **S04.08** Transition. Sources: [TOUR-M](https://aclanthology.org/2023.findings-acl.354.pdf#page=3), [REFIT-M](https://arxiv.org/pdf/2305.11744v2#page=3). Location: TOUR-M: Sung et al., Findings ACL 2023. PDF pp.3–5, §§3.1–3.5; Eqs.7–13. Encoders fixed: §3.1 ¶1. One step then retrieval: §3.2 paragraph after Eq.10. Caching: §3.5.; REFIT-M: PDF p.3, §3.2 Eqs.5–7 and Algorithm 1; §4.1 (separate min-max normalization, teacher T=2, n=100, learning rate .005); §4.2 (rerank 125 comparator).

## Page 05 — Ask. Move. Search again.

**On screen:** TOUR optimizes the already-computed query representation.

**Evidence:** Published method · **Spoken words:** 130 · **Estimated delivery:** 60 seconds at 130 words/minute

**Takeaway:** The index stays fixed while the query moves.

### Spoken script

Start at the original query vector, q zero, and retrieve nearby candidates from the fixed index. TOUR asks a cross-encoder to score those candidates and treats the outputs as pseudo relevance feedback. The query representation then takes a gradient step using that signal, while both encoders remain fixed. Follow the blue arrow to q one: fresh retrieval can now return a different neighborhood. The method can repeat this retrieve-score-update process, with cached scores and early stopping reducing some repeated work. The number of rounds is task-dependent: its reported settings allow up to three for phrase question answering and one for passage retrieval. The mechanism is moving the query and searching again; TOUR does not always run three rounds. Next, we examine how TOUR converts teacher scores into a learning signal.

### Pointer notes

- Trace the loop clockwise: retrieve, score, update, retrieve.
- Point to moving q₀ and q₁; the gray document points never move.

### Sentence provenance

- **S05.01** Source-grounded paraphrase. Sources: [TOUR-M](https://aclanthology.org/2023.findings-acl.354.pdf#page=3). Location: TOUR-M: §3.1, PDF p.3, first two paragraphs; Eq.7 scores the retrieved candidates.
- **S05.02** Source-grounded paraphrase. Sources: [TOUR-M](https://aclanthology.org/2023.findings-acl.354.pdf#page=3). Location: TOUR-M: §3.1, PDF p.3, Eq.7 and following paragraph on pseudo labels without gold relevance.
- **S05.03** Source-grounded paraphrase. Sources: [TOUR-M](https://aclanthology.org/2023.findings-acl.354.pdf#page=3). Location: TOUR-M: §3.1 opening paragraph (fixed encoders); §3.2, PDF p.4, Eq.10 (query-vector gradient descent).
- **S05.04** Diagram explanation. Sources: [TOUR-M](https://aclanthology.org/2023.findings-acl.354.pdf#page=3). Location: TOUR-M: §3.2, PDF p.4, paragraph after Eq.10 (one step followed by retrieval); Figure 1 (schematic vector movement).
- **S05.05** Source-grounded paraphrase. Sources: [TOUR-M](https://aclanthology.org/2023.findings-acl.354.pdf#page=3). Location: TOUR-M: §3.5, PDF p.5, sole paragraph on maximum iterations, early stopping and cached reranker scores.
- **S05.06** Source-grounded paraphrase. Sources: [TOUR-R](https://aclanthology.org/2023.findings-acl.354.pdf#page=7). Location: TOUR-R: Appendix D, PDF p.14, Table 7, Max iterations row: 3 for phrase QA and 1 for both passage settings.
- **S05.07** Explanation. Sources: [TOUR-M](https://aclanthology.org/2023.findings-acl.354.pdf#page=3), [TOUR-R](https://aclanthology.org/2023.findings-acl.354.pdf#page=7). Location: TOUR-M: §3.2 Eq.10 and following paragraph. TOUR-R: Appendix D Table 7; task-specific interpretation.
- **S05.08** Transition. Sources: [TOUR-HS](https://aclanthology.org/2023.findings-acl.354.pdf#page=4). Location: TOUR-HS: §3.2 and §3.3 headings and objectives; presentation transition.

## Page 06 — Hard labels, or soft guidance?

**On screen:** Both are pseudo feedback. The distinction belongs to TOUR.

**Evidence:** Published method · **Spoken words:** 122 · **Estimated delivery:** 56 seconds at 130 words/minute

**Takeaway:** Hard selects a set. Soft preserves relative preferences.

### Spoken script

TOUR provides the hard and soft feedback objectives; these are not ReFIT variants. In the hard version, teacher probabilities select a small pseudo-positive set using a cumulative-probability threshold. The hard loss increases total student probability on that set, without requiring it to copy every probability. In the soft version, the entire teacher distribution becomes the target through forward KL divergence. These three bars are a teaching example, not benchmark measurements. With teacher probabilities point six, point three and point one, an example threshold of point eight selects the first two documents. Soft guidance retains the preference for the first document over the second, which the hard membership decision discards. In both cases, pseudo labels may be wrong, and the encoders remain unchanged.

### Pointer notes

- Point to the bracket over A and B in Hard.
- Then point to all three bar heights in Soft. The illustrative threshold is .8, not the paper default.

**Technical note:** Illustrative probabilities and threshold. TOUR Appendix D uses its own tuned settings.

### Sentence provenance

- **S06.01** Source-grounded paraphrase. Sources: [TOUR-HS](https://aclanthology.org/2023.findings-acl.354.pdf#page=4). Location: TOUR-HS: §3.2 TOUR with Hard Labels and §3.3 TOUR with Soft Labels; ReFIT §2 acknowledges these as TOUR variants.
- **S06.02** Source-grounded paraphrase. Sources: [TOUR-HS](https://aclanthology.org/2023.findings-acl.354.pdf#page=4). Location: TOUR-HS: §3.2, PDF pp.3–4, Eq.8 and adjacent paragraph specifying a smallest cumulative-probability pseudo-positive set.
- **S06.03** Source-grounded paraphrase. Sources: [TOUR-HS](https://aclanthology.org/2023.findings-acl.354.pdf#page=4). Location: TOUR-HS: §3.2, PDF p.4, Eq.9 and following paragraph. The loss maximizes marginal probability of the selected set.
- **S06.04** Source-grounded paraphrase. Sources: [TOUR-HS](https://aclanthology.org/2023.findings-acl.354.pdf#page=4). Location: TOUR-HS: §3.3, PDF p.4, opening paragraph and Eq.12, forward KL from teacher probabilities to student probabilities.
- **S06.05** Original teaching example. Sources: [DERIVATION](#derivation). Location: DERIVATION: original toy-probability example recorded in the source ledger; no experimental provenance is asserted.
- **S06.06** Original teaching example. Sources: [DERIVATION](#derivation). Location: DERIVATION: toy teacher [.6,.3,.1] and illustrative nucleus threshold .8; cumulative sum .9 selects A and B. The paper default threshold is different.
- **S06.07** Explanation. Sources: [TOUR-HS](https://aclanthology.org/2023.findings-acl.354.pdf#page=4), [DERIVATION](#derivation). Location: TOUR-HS: §3.3 opening paragraph explains that hard labels use teacher scores for a membership decision. DERIVATION: the A/B comparison applies that explanation to the toy example.
- **S06.08** Explanation. Sources: [TOUR-M](https://aclanthology.org/2023.findings-acl.354.pdf#page=3). Location: TOUR-M: §3.1 first and third paragraphs (frozen encoders and model-provided pseudo labels). Possibility of label error is a logical qualification.

## Page 07 — Does moving the query recover more?

**On screen:** TOUR paper · DPR on EntityQuestions · passage retrieval.

**Evidence:** Published results · **Spoken words:** 126 · **Estimated delivery:** 58 seconds at 130 words/minute

**Takeaway:** Reranking changes order; another search can change the set.

### Spoken script

This chart redraws TOUR Table three for the DPR passage retriever on EntityQuestions. The vertical axis is answer-containing passage accuracy, shown at depths twenty and one hundred. First compare retrieval with reranking: accuracy at twenty rises from 57.9 to 64.4, while accuracy at one hundred stays at 70.8. The unchanged deeper value illustrates the fixed-candidate limitation discussed earlier. Now follow the blue TOUR-soft bars: the reported values are 66.2 at twenty and 72.5 at one hundred. The higher deeper value is consistent with retrieving answer-containing passages that were missed by the original set. These are published results for a specific model and dataset, not our project measurements. They show the mechanism can help, without guaranteeing the same gain on another corpus.

### Pointer notes

- Name the y-axis and the two bar colors before reading values.
- Compare Acc@100 for Retrieve and Rerank, then point to TOUR soft at 72.5.

### Sentence provenance

- **S07.01** Source-grounded paraphrase. Sources: [TOUR-R](https://aclanthology.org/2023.findings-acl.354.pdf#page=7). Location: TOUR-R: PDF p.7, Table 3, DPR_multi rows and EntityQuestions columns.
- **S07.02** Source-grounded paraphrase. Sources: [TOUR-R](https://aclanthology.org/2023.findings-acl.354.pdf#page=7). Location: TOUR-R: Table 3 caption and §4.3 paragraph defining top-K accuracy as presence of an answer in the retrieved passages.
- **S07.03** Source-grounded paraphrase. Sources: [TOUR-R](https://aclanthology.org/2023.findings-acl.354.pdf#page=7). Location: TOUR-R: Table 3, EntityQuestions, DPR_multi and +Re-ranker rows: 57.9/70.8 and 64.4/70.8.
- **S07.04** Our interpretation. Sources: [TOUR-R](https://aclanthology.org/2023.findings-acl.354.pdf#page=7), [REFIT-I](https://arxiv.org/html/2305.11744v2#S1). Location: TOUR-R: unchanged70.8 in Table 3. REFIT-I: fixed-set Recall@K premise. This is our interpretation of the table.
- **S07.05** Source-grounded paraphrase. Sources: [TOUR-R](https://aclanthology.org/2023.findings-acl.354.pdf#page=7). Location: TOUR-R: Table 3, EntityQuestions, DPR_multi +TOURsoft row: 66.2/72.5.
- **S07.06** Our interpretation. Sources: [TOUR-R](https://aclanthology.org/2023.findings-acl.354.pdf#page=7). Location: TOUR-R: Table 3 and §4.3 results paragraph. Interprets higher hit-rate after retrieval; it does not establish exact per-document identities.
- **S07.07** Evidence boundary. Sources: [TOUR-R](https://aclanthology.org/2023.findings-acl.354.pdf#page=7). Location: TOUR-R: Table 3 caption, dataset and model labels. These values are from the paper, not our run.
- **S07.08** Interpretation boundary. Sources: [TOUR-R](https://aclanthology.org/2023.findings-acl.354.pdf#page=7). Location: TOUR-R: bounded interpretation of Table 3; no universal generalization claim.

## Page 08 — Can we reuse one scored set?

**On screen:** ReFIT performs many inexpensive vector updates before re-retrieval.

**Evidence:** Published method · **Spoken words:** 125 · **Estimated delivery:** 58 seconds at 130 words/minute

**Takeaway:** One teacher pass. Many vector steps. One fresh search.

### Spoken script

ReFIT starts from retrieve-and-rerank, separating an expensive feedback round from inexpensive optimization steps. The teacher scores a fixed candidate set once, and those scores remain targets throughout the inner update. The method performs one hundred query-vector steps in the reported main configuration, then runs a second retrieval over the corpus. One hundred vector steps therefore does not mean one hundred calls to the reranker. The objective makes the retriever distribution resemble the teacher distribution, while all model weights and document vectors remain fixed. The paper normalizes both score lists separately and uses a teacher temperature of two. Faithful reproduction matters because these details can change the optimization signal. The contrast with TOUR is the organization of feedback and updates; both methods can retrieve new documents.

### Pointer notes

- Circle “score once”, then point inside the 100-step update box.
- Follow the final arrow to the same full corpus index.

### Sentence provenance

- **S08.01** Source-grounded paraphrase. Sources: [REFIT-M](https://arxiv.org/pdf/2305.11744v2#page=3). Location: REFIT-M: Algorithm 1 and §3.2 final two paragraphs, PDF p.3; §5.4 contrasts inner update allocation with TOUR.
- **S08.02** Source-grounded paraphrase. Sources: [REFIT-M](https://arxiv.org/pdf/2305.11744v2#page=3). Location: REFIT-M: Algorithm 1 computes teacher distribution once in step2, before the repeated query-vector update loop.
- **S08.03** Source-grounded paraphrase. Sources: [REFIT-M](https://arxiv.org/pdf/2305.11744v2#page=3). Location: REFIT-M: §4.1, PDF p.3, final sentence specifies n100; §3.2 final paragraph specifies second full-index retrieval.
- **S08.04** Explanation. Sources: [REFIT-M](https://arxiv.org/pdf/2305.11744v2#page=3). Location: REFIT-M: Algorithm 1, step2 versus steps3–7. Counts gradient updates separately from teacher scoring.
- **S08.05** Source-grounded paraphrase. Sources: [REFIT-M](https://arxiv.org/pdf/2305.11744v2#page=3). Location: REFIT-M: §3.2, Eqs.5–7, Algorithm 1; cached document embeddings are read from the index rather than updated.
- **S08.06** Source-grounded paraphrase. Sources: [REFIT-M](https://arxiv.org/pdf/2305.11744v2#page=3). Location: REFIT-M: §4.1, PDF p.3, first paragraph: separate min-max normalization and teacher temperature T2.
- **S08.07** Implementation reasoning. Sources: [REFIT-M](https://arxiv.org/pdf/2305.11744v2#page=3). Location: REFIT-M: §4.1 normalization and temperature choices. Our implementation reasoning: these choices affect the distributions defining the loss.
- **S08.08** Our synthesis. Sources: [TOUR-M](https://aclanthology.org/2023.findings-acl.354.pdf#page=3), [REFIT-M](https://arxiv.org/pdf/2305.11744v2#page=3). Location: TOUR-M: §3.2 step-and-retrieve paragraph. REFIT-M: Algorithm 1 and §3.2 final paragraph. Our comparison of the two update organizations.

## Page 09 — What is KL teaching the student?

**On screen:** Minimize disagreement with a fixed teacher distribution.

**Evidence:** Mathematical explanation · **Spoken words:** 130 · **Estimated delivery:** 60 seconds at 130 words/minute

**Takeaway:** Give more student probability to documents the teacher prefers.

### Spoken script

Teacher and student are distributions over the same candidates, not models we train together here. The teacher distribution comes from reranker scores; the student distribution comes from the current query-document similarities. Read the equation as a weighted penalty for disagreement, with teacher probabilities providing weights. We minimize KL from teacher to student; we do not maximize KL and we do not change the teacher. For a fixed teacher, this is equivalent to maximizing teacher-weighted log probability under the student. In the illustrative bars, the teacher favors document A while the student places too much probability on C. A useful vector update should reduce that discrepancy, though the shared embedding geometry couples the candidate scores. The distribution on the right illustrates closer agreement, not a guaranteed result of one gradient step.

### Pointer notes

- Read teacher first in KL(teacher ∥ student).
- Point to A, then C, and use the “After” button to reveal an illustrative closer distribution.

### Sentence provenance

- **S09.01** Source-grounded paraphrase. Sources: [REFIT-M](https://arxiv.org/pdf/2305.11744v2#page=3). Location: REFIT-M: §3.2 Eqs.5–7 and Algorithm 1; teacher scores fixed while query vector changes.
- **S09.02** Source-grounded paraphrase. Sources: [REFIT-M](https://arxiv.org/pdf/2305.11744v2#page=3). Location: REFIT-M: §3.2 Eq.5 (reranker distribution) and Eq.6 (retriever distribution).
- **S09.03** Mathematical explanation. Sources: [REFIT-M](https://arxiv.org/pdf/2305.11744v2#page=3). Location: REFIT-M: §3.2 Eq.7. Our reading of the standard forward-KL expression, expanded in the source ledger.
- **S09.04** Source-grounded paraphrase. Sources: [REFIT-M](https://arxiv.org/pdf/2305.11744v2#page=3). Location: REFIT-M: §3.2 Eq.7 and Algorithm 1 gradient-descent update. Direction is teacher to student.
- **S09.05** Elementary derivation. Sources: [DERIVATION](#derivation). Location: DERIVATION: Source ledger, Forward KL, fixed teacher. The teacher-entropy term is constant with respect to the student vector.
- **S09.06** Original teaching example. Sources: [DERIVATION](#derivation). Location: DERIVATION: original toy distributions teacher[.6,.3,.1] and student[.2,.3,.5].
- **S09.07** Mathematical explanation. Sources: [DERIVATION](#derivation). Location: DERIVATION: one vector determines all candidate dot products, so candidate logits cannot generally be set independently.
- **S09.08** Illustration boundary. Sources: [DERIVATION](#derivation). Location: DERIVATION: original closer distribution[.5,.3,.2], intentionally not claimed as a simulated optimizer iterate.

## Page 10 — Is the feedback worth another search?

**On screen:** ReFIT paper · BEIR Recall@100 · Table 6.

**Evidence:** Published results · **Spoken words:** 130 · **Estimated delivery:** 60 seconds at 130 words/minute

**Takeaway:** Quality and total cost both belong in the comparison.

### Spoken script

These five bars reproduce the BEIR column from ReFIT Table six. Recall at one hundred rises from 66.8 for retrieval to 67.6 for the larger-pool reranking comparator. The paper reports 68.4 for TOUR hard, 68.1 for TOUR soft, and 69.2 for ReFIT in this comparison. ReFIT is 1.6 percentage points above reranking here; that gap is specific to this comparison. The separate timing strip comes from Table one: ReFIT takes 470 milliseconds in its GPU configuration. That is slower than reranking one hundred candidates at 400 milliseconds, but faster than reranking 125 at 490 milliseconds. The two comparisons show why both candidate depth and extra index searches must be counted. The source notes preserve the paper’s different aggregate values rather than silently editing them.

### Pointer notes

- Read the baseline bars left to right; isolate the 67.6 → 69.2 gap.
- Treat the timing strip as a separate experiment, not the x-axis of this score plot.

**Technical note:** Table 6 reports 69.2; Table 2 reports 69.0 for a BEIR mean. All bars here come only from Table 6.

### Sentence provenance

- **S10.01** Source-grounded paraphrase. Sources: [REFIT-R](https://arxiv.org/pdf/2305.11744v2#page=6). Location: REFIT-R: PDF p.6, Table 6, BEIR column, all five rows.
- **S10.02** Source-grounded paraphrase. Sources: [REFIT-R](https://arxiv.org/pdf/2305.11744v2#page=6). Location: REFIT-R: Table 6 BEIR Retrieve66.8 and Rerank67.6. REFIT-M: §4.2 defines the rerank125 comparator.
- **S10.03** Source-grounded paraphrase. Sources: [REFIT-R](https://arxiv.org/pdf/2305.11744v2#page=6). Location: REFIT-R: Table 6 BEIR TOURhard68.4, TOURsoft68.1, ReFIT69.2.
- **S10.04** Arithmetic and qualification. Sources: [REFIT-R](https://arxiv.org/pdf/2305.11744v2#page=6). Location: REFIT-R: arithmetic69.2−67.6=1.6 percentage points from Table 6; no relative-percent or cross-benchmark claim.
- **S10.05** Source-grounded paraphrase. Sources: [REFIT-TIME](https://arxiv.org/pdf/2305.11744v2#page=3). Location: REFIT-TIME: PDF p.3, Table 1, ReFIT total GPU470ms; timing is not the quality chart’s experimental axis.
- **S10.06** Source-grounded paraphrase. Sources: [REFIT-TIME](https://arxiv.org/pdf/2305.11744v2#page=3). Location: REFIT-TIME: Table 1 total GPU row: R&R100400ms, R&R125490ms, ReFIT100470ms.
- **S10.07** Our interpretation. Sources: [REFIT-M](https://arxiv.org/pdf/2305.11744v2#page=3), [REFIT-TIME](https://arxiv.org/pdf/2305.11744v2#page=3). Location: REFIT-M: §4.2 baseline design. REFIT-TIME: Table 1 retrieval/reranking/distillation breakdown; our cost interpretation.
- **S10.08** Editorial provenance. Sources: [REFIT-R](https://arxiv.org/pdf/2305.11744v2#page=6). Location: REFIT-R: Table 2 BEIR average69.0 versus Table 6 BEIR69.2. This is an editorial source-consistency note.

## Page 11 — What happened in our SCIDOCS run?

**On screen:** 1,000 queries · all 25,657 documents · frozen Contriever and MiniLM.

**Evidence:** Project result · **Spoken words:** 128 · **Estimated delivery:** 59 seconds at 130 words/minute

**Takeaway:** The run completed. The ReFIT gain was not reproduced.

### Spoken script

Now we move from published tables to our recorded full-corpus SCIDOCS experiment. We used one thousand queries and all 25,657 documents, with frozen Contriever-msmarco and MiniLM checkpoints. Our Recall at one hundred was 37.8067 for raw retrieval, 38.3450 for direct rerank-125, and 37.8717 for the ReFIT attempt. The first two match the paper references at their displayed precision, while the adaptation result does not reach the paper’s 40.1. The paired-bootstrap interval for ReFIT minus raw runs from minus 0.180 to plus 0.325 percentage points, spanning zero. This is an unresolved reproduction gap, not evidence that ReFIT cannot work. Our recorded update count, learning rate and teacher temperature match the paper’s v2 settings. Matching those settings does not independently validate the implementation.

### Pointer notes

- Point to each blue local bar, then the hollow paper-reference marker.
- End on the interval spanning zero; do not describe it as a confirmed positive gain.

**Technical note:** Recorded run and bootstrap analysis; raw metrics were not recomputed in this presentation pass.

### Sentence provenance

- **S11.01** Source-grounded paraphrase. Sources: [RUN](https://github.com/nilansa/ire-project-2026/issues/3#issuecomment-6908737534). Location: RUN: completed SCIDOCS run report opening paragraph and metric list, issuecomment6908737534.
- **S11.02** Source-grounded paraphrase. Sources: [RUN](https://github.com/nilansa/ire-project-2026/issues/3#issuecomment-6908737534). Location: RUN: opening paragraph:1000 queries,25657 documents and the named frozen checkpoints.
- **S11.03** Source-grounded paraphrase. Sources: [RUN](https://github.com/nilansa/ire-project-2026/issues/3#issuecomment-6908737534). Location: RUN: three-item measured Recall@100 list, raw37.8067, rerank12538.3450, ReFIT37.8717.
- **S11.04** Source-grounded paraphrase. Sources: [RUN](https://github.com/nilansa/ire-project-2026/issues/3#issuecomment-6908737534), [REFIT-SCI](https://arxiv.org/pdf/2305.11744v2#page=4). Location: RUN: measured list. REFIT-SCI: v2 Table 2 SCIDOCS last three columns37.8,38.3,40.1. Agreement is after rounding, not bitwise identity.
- **S11.05** Source-grounded paraphrase. Sources: [RUN-CI](https://github.com/nilansa/ire-project-2026/issues/3#issuecomment-6909019011). Location: RUN-CI: issuecomment6909019011, paired-bootstrap ReFIT-minus-raw result and95% interval.
- **S11.06** Interpretation boundary. Sources: [RUN-CI](https://github.com/nilansa/ire-project-2026/issues/3#issuecomment-6909019011). Location: RUN and RUN-CI: bounded interpretation of one implementation/run; no claim that the method fails generally.
- **S11.07** Source-grounded paraphrase. Sources: [RUN](https://github.com/nilansa/ire-project-2026/issues/3#issuecomment-6908737534), [REFIT-SCI](https://arxiv.org/pdf/2305.11744v2#page=4). Location: RUN: completion-report configuration paragraph (100 updates, LR.005,T2). REFIT-SCI: v2 §4.1 explicitly states the same nominal settings.
- **S11.08** Interpretation boundary. Sources: [RUN](https://github.com/nilansa/ire-project-2026/issues/3#issuecomment-6908737534), [REFIT-SCI](https://arxiv.org/pdf/2305.11744v2#page=4). Location: RUN and REFIT-SCI: matching reported settings does not establish preprocessing or code equivalence. Raw run artifacts were not recomputed in this presentation pass.

## Page 12 — Can one query teach the next?

**On screen:** TTT-Embed changes how long feedback survives.

**Evidence:** Authors’ framing · **Spoken words:** 130 · **Estimated delivery:** 60 seconds at 130 words/minute

**Takeaway:** From a query-private update to a reusable external state.

### Spoken script

The previous methods adapt the representation of the query currently being served. TTT-Embed asks whether some of that feedback can survive and help later queries without entering the encoder weights. Its related-work section describes TOUR as query-level optimization and ReFIT as distillation into a query vector before another search. The authors group these approaches as keeping the optimized state private to the current query. Point to the two paths: a private state is used once, while a shared residual can be reused by other queries. This is the TTT-Embed authors’ framing of prior work, not our experimental result. Their reported baselines do not establish a matched head-to-head victory over TOUR or ReFIT. The new organizing question is where the state should be shared when relevance judgments have a limited budget.

### Pointer notes

- Trace the top private path; then follow the bottom shared-vector fan-out.
- Explicitly say this characterization comes from TTT-Embed Appendix §8.

### Sentence provenance

- **S12.01** Source-grounded paraphrase. Sources: [TOUR-M](https://aclanthology.org/2023.findings-acl.354.pdf#page=3), [REFIT-M](https://arxiv.org/pdf/2305.11744v2#page=3). Location: TOUR-M: §3.1 instance-level query optimization. REFIT-M: §3.2 query-specific distillation.
- **S12.02** Source-grounded paraphrase. Sources: [TTT-I](https://arxiv.org/html/2608.12569v1#S1), [TTT-S](https://arxiv.org/pdf/2608.12569v1#page=4). Location: TTT-I: Introduction paragraphs on discarded query-specific rewards and external state. TTT-S: §2.3 scope definitions.
- **S12.03** Source-grounded paraphrase. Sources: [TTT-RW](https://arxiv.org/html/2608.12569v1#S8). Location: TTT-RW: Appendix §8, PDF p.13, pseudo-relevance-feedback/query-adaptation paragraph, TOUR and ReFIT descriptions.
- **S12.04** Source-grounded paraphrase. Sources: [TTT-RW](https://arxiv.org/html/2608.12569v1#S8). Location: TTT-RW: same Appendix §8 paragraph, concluding query-private-state characterization.
- **S12.05** Diagram explanation. Sources: [TTT-S](https://arxiv.org/pdf/2608.12569v1#page=4). Location: TTT-S: §2.3 three scope definitions. The diagram is an original schematic of the stated reuse relationship.
- **S12.06** Attribution boundary. Sources: [TTT-RW](https://arxiv.org/html/2608.12569v1#S8). Location: TTT-RW: Appendix §8 characterization is attributed to TTT-Embed; not an experiment by this project.
- **S12.07** Source-grounded paraphrase. Sources: [TTT-RW](https://arxiv.org/html/2608.12569v1#S8). Location: TTT-RW: §3.4 Baselines lists raw retrieval, direct reranking and the three TTT scopes; it does not report a matched TOUR/ReFIT benchmark.
- **S12.08** Source-grounded paraphrase. Sources: [TTT-S](https://arxiv.org/pdf/2608.12569v1#page=4), [TTT-B](https://arxiv.org/pdf/2608.12569v1#page=6). Location: TTT-S: §2.3 concluding discussion of specificity versus reuse. TTT-B: §2.1 Eq.1 workload budget.

## Page 13 — Three scopes. One residual idea.

**On screen:** Global, task and query are sharing scopes—not three separate retrieval tasks.

**Evidence:** Published method · **Spoken words:** 126 · **Estimated delivery:** 58 seconds at 130 words/minute

**Takeaway:** The scope chooses who contributes feedback and who can reuse it.

### Spoken script

TTT-Embed defines three sharing scopes for an external residual. A global vector pools feedback across tasks for one embedding model and serves every query using that model. A task vector pools feedback only within a particular task and serves other queries from that task. A query vector uses one query’s scored candidates and remains specific to that query. The learning mechanism stays the same; the grouping of feedback and reuse changes. Global learning balances task contributions so tasks with more queries do not automatically dominate the loss. A query without its own feedback has no query-specific correction, but it can still receive a learned task or global correction. The tradeoff is sharing scarce feedback broadly or spending enough to specialize narrowly; the best choice is empirical.

### Pointer notes

- Point to one shared vector on the left, one per task in the middle, one per query on the right.
- Say “scope” every time; do not call the three columns tasks.

### Sentence provenance

- **S13.01** Source-grounded paraphrase. Sources: [TTT-S](https://arxiv.org/pdf/2608.12569v1#page=4). Location: TTT-S: §2.3, PDF p.4, three sharing-scope definitions.
- **S13.02** Source-grounded paraphrase. Sources: [TTT-S](https://arxiv.org/pdf/2608.12569v1#page=4). Location: TTT-S: §2.3 global-wise definition.
- **S13.03** Source-grounded paraphrase. Sources: [TTT-S](https://arxiv.org/pdf/2608.12569v1#page=4). Location: TTT-S: §2.3 task-wise definition.
- **S13.04** Source-grounded paraphrase. Sources: [TTT-S](https://arxiv.org/pdf/2608.12569v1#page=4). Location: TTT-S: §2.3 query-wise definition.
- **S13.05** Source-grounded paraphrase. Sources: [TTT-S](https://arxiv.org/pdf/2608.12569v1#page=4). Location: TTT-S: §2.3 opening and following paragraphs: one objective with different feedback grouping and reuse.
- **S13.06** Source-grounded paraphrase. Sources: [TTT-S](https://arxiv.org/pdf/2608.12569v1#page=4). Location: TTT-S: Appendix §10, PDF p.14, Eq.14 and explanation of task-balanced global weights.
- **S13.07** Source-grounded paraphrase. Sources: [TTT-S](https://arxiv.org/pdf/2608.12569v1#page=4). Location: TTT-S: §2.3 paragraph following the definitions, behavior for unrewarded queries.
- **S13.08** Our synthesis. Sources: [TTT-S](https://arxiv.org/pdf/2608.12569v1#page=4), [TTT-B](https://arxiv.org/pdf/2608.12569v1#page=6). Location: TTT-S: §2.3 scope discussion. TTT-B: §4.1 empirical budget/scope comparison. The tradeoff is our synthesis of those statements.

## Page 14 — How does the residual learn?

**On screen:** The residual is optimized outside the frozen embedding model.

**Evidence:** Published method · **Spoken words:** 128 · **Estimated delivery:** 59 seconds at 130 words/minute

**Takeaway:** Fit the teacher distribution, then control the correction magnitude.

### Spoken script

The student adds a learned residual to the original normalized query vector, then normalizes again. Its candidate probabilities are compared with fixed teacher probabilities through forward KL divergence. The loss averages over the state’s feedback queries and adds a ridge penalty to discourage an excessive residual. Only the external residual is optimized; the embedding model, teacher and stored document vectors remain frozen. After learning, deployment scales the residual by alpha: n divided by n plus one. Here n counts distinct rewarded queries, not documents, so one query scored against many documents still gives alpha equal to one half. Shared states supported by more queries receive less shrinkage under this rule. The corrected vector searches the existing full index, so the result set can differ from the feedback candidates.

### Pointer notes

- Point to the blue v in the update formula; then the KL fitting term and ridge term.
- Finish on n = rewarded queries and α = .5 for a query-private state.

### Sentence provenance

- **S14.01** Source-grounded paraphrase. Sources: [TTT-M](https://arxiv.org/pdf/2608.12569v1#page=4). Location: TTT-M: §2.2 Eq.3, normalized x_q+v used during learning.
- **S14.02** Source-grounded paraphrase. Sources: [TTT-M](https://arxiv.org/pdf/2608.12569v1#page=4). Location: TTT-M: §2.2 Eq.2 teacher distribution, Eq.3 student distribution and Eq.4 forward-KL objective.
- **S14.03** Source-grounded paraphrase. Sources: [TTT-M](https://arxiv.org/pdf/2608.12569v1#page=4), [TTT-S](https://arxiv.org/pdf/2608.12569v1#page=4). Location: TTT-M: §2.2 Eq.4. TTT-S: Appendix §10 query weights; the average can be task-balanced.
- **S14.04** Source-grounded paraphrase. Sources: [TTT-I](https://arxiv.org/html/2608.12569v1#S1), [TTT-M](https://arxiv.org/pdf/2608.12569v1#page=4). Location: TTT-I: Figure 1 caption and §2 opening paragraph. TTT-M: Eq.4 optimizes only v.
- **S14.05** Source-grounded paraphrase. Sources: [TTT-M](https://arxiv.org/pdf/2608.12569v1#page=4). Location: TTT-M: §2.4 Eq.5 and adjacent deployment paragraph; shrinkage is applied after the full-residual fit.
- **S14.06** Source-grounded paraphrase. Sources: [TTT-M](https://arxiv.org/pdf/2608.12569v1#page=4). Location: TTT-M: §2.4 final paragraph defines n as distinct rewarded queries and gives query-wise alpha1/2.
- **S14.07** Source-grounded paraphrase. Sources: [TTT-M](https://arxiv.org/pdf/2608.12569v1#page=4). Location: TTT-M: §2.4 Eq.5; n/(n+1) increases toward1 as distinct rewarded-query count increases.
- **S14.08** Source-grounded paraphrase. Sources: [TTT-P](https://arxiv.org/pdf/2608.12569v1#page=15). Location: TTT-P: Appendix §12, Embedding and retrieval protocol paragraph, full-corpus re-search using the corrected query.

## Page 15 — What does the feedback budget change?

**On screen:** Published gains over raw retrieval · 15 tasks · five embedding models.

**Evidence:** Published results · **Spoken words:** 127 · **Estimated delivery:** 59 seconds at 130 words/minute

**Takeaway:** Low budgets favor sharing in the paper’s tested regime.

### Spoken script

These are three published operating points from Table one, not a reconstructed continuous curve. The vertical axis shows nDCG-at-ten gains on a hundred-point scale, averaged over the reported tasks and embedding models. At the smallest budget, a global state gives 1.23 points while direct reranking gives approximately zero. At ten judgments per workload query, the selected task scope gains 6.36 points against 3.21 for direct reranking. At one hundred, the selected query scope reaches 8.36 against 7.80. Both budget and scope change across columns; this is not one fixed method’s learning curve. Budget here counts scored query-document pairs averaged across the workload; it is not complete wall-clock cost. These paper averages describe another workload; our single-task, held-out pilot tests a narrower question.

### Pointer notes

- Define the gain axis before comparing the bars.
- Point to the task-scope pair: 6.36 − 3.21 = 3.15 points.
- Mention that b≈.01 is rounded; exact b=150/12,263.

### Sentence provenance

- **S15.01** Source-grounded paraphrase. Sources: [TTT-B](https://arxiv.org/pdf/2608.12569v1#page=6). Location: TTT-B: PDF p.6, Table 1, selected budget/scope columns; no unsampled curve is reconstructed.
- **S15.02** Source-grounded paraphrase. Sources: [TTT-B](https://arxiv.org/pdf/2608.12569v1#page=6). Location: TTT-B: Table 1 caption and Average rows, gain in nDCG@10×100 across tasks and five embedding models.
- **S15.03** Source-grounded paraphrase. Sources: [TTT-B](https://arxiv.org/pdf/2608.12569v1#page=6). Location: TTT-B: Table 1 low-budget Average row: global1.23, direct−.01, verbally approximated as zero. Appendix §12 gives exact budget150/12263.
- **S15.04** Source-grounded paraphrase. Sources: [TTT-B](https://arxiv.org/pdf/2608.12569v1#page=6). Location: TTT-B: Table 1 b10 Average row: task6.36 and direct3.21.
- **S15.05** Source-grounded paraphrase. Sources: [TTT-B](https://arxiv.org/pdf/2608.12569v1#page=6). Location: TTT-B: Table 1 b100 Average row: query8.36 and direct7.80.
- **S15.06** Chart interpretation. Sources: [TTT-B](https://arxiv.org/pdf/2608.12569v1#page=6). Location: TTT-B: Table 1 column headings change scope alongside budget; this is an interpretation of the selected plotted columns.
- **S15.07** Source-grounded paraphrase. Sources: [TTT-B](https://arxiv.org/pdf/2608.12569v1#page=6). Location: TTT-B: §2.1 Eq.1 and following paragraph define B and b as feedback-pair counts, excluding base embedding and ANN costs.
- **S15.08** Comparison boundary. Sources: [TTT-P](https://arxiv.org/pdf/2608.12569v1#page=15), [FIQA_RUN](https://github.com/nilansa/ire-project-2026/blob/main/research/CEOUS_COMPLEMENTARY_FEEDBACK_2PAGE_WORKING_20261116.md#4-completed-ceous-measurements-not-directly-comparable). Location: TTT-P: §3.1 and Appendix §12 specify the paper workload. FIQA_RUN: working report §4 FiQA row specifies one task and held-out cross-fitting; the pilot does not replicate the full paper workload.

## Page 16 — Did the FiQA residual help held-out queries?

**On screen:** 648 queries · all 57,638 documents · five-fold task-wise TTT pilot.

**Evidence:** Reported project result · **Spoken words:** 122 · **Estimated delivery:** 56 seconds at 130 words/minute

**Takeaway:** The pilot reports no reliable held-out gain. Coverage selection is still untested.

### Spoken script

Our reported FiQA pilot tests task-wise TTT on 648 queries and the full 57,638-document corpus. It uses frozen Qwen3-Embedding-0.6B and Qwen3-Reranker-4B. Five-fold cross-fitting uses eighty percent for feedback and twenty percent for unscored evaluation, with ten pairs per feedback query. Held-out nDCG at ten moves from 0.46722 to 0.46313. The source reports a change of minus 0.00408, with a ninety-five-percent interval from minus 0.01072 to plus 0.00262. Every fold improved in-sample, but the held-out interval spans zero, providing no reliable evidence of transfer to unscored queries. Prior task exposure is disclosed; the private raw artifacts were not independently recomputed for this presentation. One task does not replicate the full paper, and complementary selection remains untested.

### Pointer notes

- Read the y-axis as raw nDCG@10, not percent; compare raw .46722 with adapted .46313.
- Point to the source-reported delta −.00408 and its 95% interval [−.01072,+.00262], which spans zero.
- Explain that feedback-query improvement did not yield a reliable held-out gain. Prior task exposure is disclosed; the raw artifacts were not recomputed here.

**Technical note:** Source: working report §4, FiQA row. The displayed rounded means subtract to −.00409, while the report gives Δ−.00408; retain its reported delta and interval. This single exposed task is not the paper’s full replication and does not test complementary selection.

### Sentence provenance

- **S16.01** Source-grounded paraphrase. Sources: [FIQA_RUN](https://github.com/nilansa/ire-project-2026/blob/main/research/CEOUS_COMPLEMENTARY_FEEDBACK_2PAGE_WORKING_20261116.md#4-completed-ceous-measurements-not-directly-comparable). Location: FIQA_RUN: working report §4, table, FiQA task-wise TTT-Embed row, Dataset and feedback column: 648 queries and 57,638 documents. Exact report Git blob dfc022cf7b12af4e198f85def4411b91de7c8a03.
- **S16.02** Source-grounded paraphrase. Sources: [FIQA_RUN](https://github.com/nilansa/ire-project-2026/blob/main/research/CEOUS_COMPLEMENTARY_FEEDBACK_2PAGE_WORKING_20261116.md#4-completed-ceous-measurements-not-directly-comparable). Location: FIQA_RUN: §4 table, FiQA row, Experiment column names frozen Qwen3-Embedding-0.6B and Qwen3-Reranker-4B.
- **S16.03** Source-grounded paraphrase. Sources: [FIQA_RUN](https://github.com/nilansa/ire-project-2026/blob/main/research/CEOUS_COMPLEMENTARY_FEEDBACK_2PAGE_WORKING_20261116.md#4-completed-ceous-measurements-not-directly-comparable). Location: FIQA_RUN: §4 table, FiQA row, Dataset and feedback column: 5 folds, 80% feedback/20% unscored evaluation and 10 rewarded pairs per training query.
- **S16.04** Source-grounded paraphrase. Sources: [FIQA_RUN](https://github.com/nilansa/ire-project-2026/blob/main/research/CEOUS_COMPLEMENTARY_FEEDBACK_2PAGE_WORKING_20261116.md#4-completed-ceous-measurements-not-directly-comparable). Location: FIQA_RUN: §4 table, FiQA row, Raw → adapted column: held-out nDCG@10 .46722→.46313. Raw nDCG units, not percentages.
- **S16.05** Source-grounded paraphrase. Sources: [FIQA_RUN](https://github.com/nilansa/ire-project-2026/blob/main/research/CEOUS_COMPLEMENTARY_FEEDBACK_2PAGE_WORKING_20261116.md#4-completed-ceous-measurements-not-directly-comparable). Location: FIQA_RUN: §4 table, FiQA row, Raw → adapted column: separately reported delta −.00408 and 95% CI [−.01072,+.00262]. The displayed rounded means subtract to −.00409; preserve the source-reported delta without inventing hidden precision.
- **S16.06** Reported result and bounded interpretation. Sources: [FIQA_RUN](https://github.com/nilansa/ire-project-2026/blob/main/research/CEOUS_COMPLEMENTARY_FEEDBACK_2PAGE_WORKING_20261116.md#4-completed-ceous-measurements-not-directly-comparable). Location: FIQA_RUN: §4 table, FiQA row, Interpretation column says every fold improved in-sample and no reliable held-out transfer. The adjacent interval crosses zero; its bounded interpretation is stated here.
- **S16.07** Reported limitation and review boundary. Sources: [FIQA_RUN](https://github.com/nilansa/ire-project-2026/blob/main/research/CEOUS_COMPLEMENTARY_FEEDBACK_2PAGE_WORKING_20261116.md#4-completed-ceous-measurements-not-directly-comparable). Location: FIQA_RUN: §4 table, FiQA Interpretation column discloses one exposed task. Selected references item 6 identifies the original private FiQA cross-fit run ledger. This presentation read the report, not the private raw artifacts, and did not independently recompute the result.
- **S16.08** Evidence boundary. Sources: [FIQA_RUN](https://github.com/nilansa/ire-project-2026/blob/main/research/CEOUS_COMPLEMENTARY_FEEDBACK_2PAGE_WORKING_20261116.md#4-completed-ceous-measurements-not-directly-comparable), [TTT-P](https://arxiv.org/pdf/2608.12569v1#page=15). Location: FIQA_RUN: §4 table, FiQA Interpretation column distinguishes this one task from the paper’s 15-task replication; paragraph immediately after the table says neither experiment tests complementary pair selection. TTT-P: §3.1 and Appendix §12 define the paper’s 15-task workload.

## Page 17 — What if the next document adds missing evidence?

**On screen:** DISCo motivates collective query coverage.

**Evidence:** Published idea + illustration · **Spoken words:** 129 · **Estimated delivery:** 60 seconds at 130 words/minute

**Takeaway:** Useful complementarity is coverage of the query.

### Spoken script

DISCo studies a different retrieval goal: selecting a small collection whose members collectively cover the query. Its representations use contextual token or atom vectors, rather than requiring literal bigram or n-gram matches. The illustrative matrix shows how four candidates cover three query facets. After choosing document one, document two adds almost the same coverage, while document four contributes strongly to a missing facet. The max-per-facet objective avoids giving repeated credit merely for covering an already covered component. This is query-focused complementarity; the paper does not explicitly optimize a generic diversity objective. Full DISCo uses a specialized index; borrowing its objective on a candidate pool gives only a coverage-inspired selector. Our next question is whether choosing feedback candidates this way can improve a residual, which DISCo itself does not establish.

### Pointer notes

- Click d₂, then d₄ in the matrix to compare marginal coverage.
- Point to facet C when explaining the .80 gain. All matrix values are illustrative.

### Sentence provenance

- **S17.01** Source-grounded paraphrase. Sources: [DISCO](https://proceedings.iclr.cc/paper_files/paper/2026/file/6ded182245f8e4db3963d2027174133d-Paper-Conference.pdf#page=3). Location: DISCO: Abstract and §1 first two paragraphs; §2 formalizes collection-level query coverage.
- **S17.02** Source-grounded paraphrase. Sources: [DISCO](https://proceedings.iclr.cc/paper_files/paper/2026/file/6ded182245f8e4db3963d2027174133d-Paper-Conference.pdf#page=3). Location: DISCO: §2 notation paragraph, PDF pp.2–3, contextual atoms/token-vector representations. Literal n-gram matching is not a required mechanism.
- **S17.03** Original teaching example. Sources: [DERIVATION](#derivation). Location: DERIVATION: original four-document, three-facet coverage matrix in the source ledger; illustrative rather than measured.
- **S17.04** Original teaching example. Sources: [DERIVATION](#derivation). Location: DERIVATION: toy matrix, conditional on d1 already selected; d2 marginal coverage.05 versus d4.80.
- **S17.05** Source-grounded paraphrase. Sources: [DISCO](https://proceedings.iclr.cc/paper_files/paper/2026/file/6ded182245f8e4db3963d2027174133d-Paper-Conference.pdf#page=3). Location: DISCO: §3.1 Eq.2 and immediately following paragraph explaining max coverage of each query atom.
- **S17.06** Source-grounded paraphrase. Sources: [DISCO](https://proceedings.iclr.cc/paper_files/paper/2026/file/6ded182245f8e4db3963d2027174133d-Paper-Conference.pdf#page=3). Location: DISCO: Appendix B, p.19, Diversity paragraph; Appendix E.5, p.23, final paragraph on not explicitly incorporating diversity.
- **S17.07** Method boundary. Sources: [DISCO](https://proceedings.iclr.cc/paper_files/paper/2026/file/6ded182245f8e4db3963d2027174133d-Paper-Conference.pdf#page=3), [HYPOTHESIS](#hypothesis). Location: DISCO: §§3.3–3.4 augmented representation and specialized index. HYPOTHESIS: the restricted candidate-pool selector is our proposal, not the full DISCo algorithm.
- **S17.08** Our hypothesis. Sources: [HYPOTHESIS](#hypothesis). Location: HYPOTHESIS: proposed coverage-to-residual experiment; DISCo reports coverage retrieval, not this residual-learning combination.

## Page 18 — Could better candidates teach a better direction?

**On screen:** Our proposed bridge from collective coverage to residual learning.

**Evidence:** Hypothesis · **Spoken words:** 126 · **Estimated delivery:** 58 seconds at 130 words/minute

**Takeaway:** Change the feedback set, then measure what the learned vector does.

### Spoken script

In a simplified softmax model, the gradient is a weighted sum of scored document vectors. The weight for each document is the student probability minus the teacher probability. This shows why the selected candidates matter: they determine the available directions in that local learning signal. If many candidates contribute similar directions, complementary evidence might expose useful disagreements that the initial neighborhood misses. It might also introduce irrelevant or noisy feedback, so the geometric picture is motivation rather than a proof of improvement. This simplified gradient omits the score and vector normalizations used by the actual methods. Generic complementary-retriever guidance already appears in GQR, and ReFIT already discusses informative negatives. Our proposed contribution must therefore be the controlled coverage-based candidate selection study under a matched feedback budget.

### Pointer notes

- Compare the nearly aligned candidate arrows with the broader useful directions.
- Point to “simplified” before explaining the gradient; end on the hypothesis label.

### Sentence provenance

- **S18.01** Our derivation. Sources: [DERIVATION](#derivation). Location: DERIVATION: Source ledger, Simplified gradient. Assumes unnormalized dot-product logits and fixed teacher probabilities.
- **S18.02** Our derivation. Sources: [DERIVATION](#derivation). Location: DERIVATION: derivative of forward KL with respect to each student logit is p_student−p_teacher.
- **S18.03** Our inference. Sources: [DERIVATION](#derivation). Location: DERIVATION: chain rule yields a linear combination of selected document vectors; geometric interpretation is ours.
- **S18.04** Our hypothesis. Sources: [HYPOTHESIS](#hypothesis). Location: HYPOTHESIS: proposed usefulness of complementary candidate directions; not an established result.
- **S18.05** Hypothesis limitation. Sources: [HYPOTHESIS](#hypothesis). Location: HYPOTHESIS: noise/irrelevance is a possibility considered by our proposal, not a measured failure rate.
- **S18.06** Mathematical scope. Sources: [DERIVATION](#derivation). Location: DERIVATION: displayed gradient omits ReFIT min-max score normalization and TTT-Embed unit normalization; it is not their exact implemented derivative.
- **S18.07** Source-grounded paraphrase. Sources: [GQR](https://arxiv.org/abs/2510.05038v3), [REFIT-L](https://arxiv.org/html/2305.11744v2#S6.SS6.SSS1). Location: GQR: abstract, complementary-retriever scores guiding a primary query embedding. REFIT-L: §6.6.1 on informative negatives.
- **S18.08** Proposed contribution. Sources: [HYPOTHESIS](#hypothesis). Location: HYPOTHESIS: narrowed proposed contribution after the cited prior-art boundary; not an exhaustive novelty claim.

## Page 19 — What would a fair test look like?

**On screen:** Reduce the query sample; keep the complete document index.

**Evidence:** Proposed experiment · **Spoken words:** 130 · **Estimated delivery:** 60 seconds at 130 words/minute

**Takeaway:** Same teacher budget. Same residual learner. Different candidate selection.

### Spoken script

Begin with one hundred to two hundred prespecified queries, retaining the full document corpus. Fewer queries reduce cost but cannot guarantee the paper’s average or a narrow uncertainty interval. Compare base top-K feedback with a coverage-inspired selector, plus a broader-pool control and random selection from the same pool. Fix query identifiers, teacher, student embeddings, feedback count, loss, optimizer and sharing scope across candidate selectors. Charge additional retrieval and selection separately, even if teacher-pair counts match. Search the full index after adaptation, then report nDCG, recall, paired uncertainty and judged positives found outside the initial pool. For shared states, separate feedback queries from held-out evaluation queries; report single-query adaptation as a different regime. Any helper retriever supplies document IDs; the residual still uses vectors from the same frozen student embedding space.

### Pointer notes

- Point to the full-corpus block: it stays intact in every arm.
- Trace selector A and B into the identical learner, then the same evaluation.

### Sentence provenance

- **S19.01** Proposed protocol. Sources: [DESIGN](#experiment-design). Location: DESIGN: proposed query sampling protocol requested by the user; full corpus retained in every arm.
- **S19.02** Statistical reasoning. Sources: [DESIGN](#experiment-design). Location: DESIGN: statistical qualification: sample size alone does not determine the mean or confidence-interval width.
- **S19.03** Proposed protocol. Sources: [DESIGN](#experiment-design). Location: DESIGN: proposed candidate-selection controls, not previously completed runs.
- **S19.04** Proposed protocol. Sources: [PLAN](https://github.com/nilansa/ire-project-2026/blob/c550bc0152f4264117a36024619dfb04ad02807b/research/BLACKBOX_RERANKER_FEEDBACK_CONTROLLED_COMPARISON_20261116.md), [DESIGN](#experiment-design). Location: PLAN: controlled-comparison design, acquisition-policy comparison. DESIGN: hold the learner and budget fixed while candidate identities may differ.
- **S19.05** Proposed cost accounting. Sources: [DESIGN](#experiment-design). Location: DESIGN: cost-accounting proposal; equal teacher counts do not imply equal full runtime.
- **S19.06** Proposed evaluation. Sources: [DESIGN](#experiment-design). Location: DESIGN: proposed full-index evaluation, paired estimates and judged-positive discovery measures.
- **S19.07** Proposed protocol. Sources: [TTT-P](https://arxiv.org/pdf/2608.12569v1#page=15), [DESIGN](#experiment-design). Location: TTT-P: §4.2 and Table 2 distinguish held-out-query transfer. DESIGN: our proposed separation of feedback and evaluation queries.
- **S19.08** Implementation requirement. Sources: [DESIGN](#experiment-design). Location: DESIGN: implementation consequence of using a single frozen student embedding space; helper-vector dimensions cannot be substituted into that objective.

## Page 20 — What can we conclude today?

**On screen:** A testable direction, with clear evidence boundaries.

**Evidence:** Provisional conclusion · **Spoken words:** 129 · **Estimated delivery:** 60 seconds at 130 words/minute

**Takeaway:** Can coverage-aware feedback make each judgment more useful?

### Spoken script

The literature shows that relevance scores can improve query representations without updating model weights. TTT-Embed studies persistent external states and how sharing scope interacts with the feedback budget. Our SCIDOCS attempt matches the raw and reranking references, but leaves the ReFIT adaptation gain unresolved. Next, we propose examining which documents supply the learning signal, rather than assuming a different update rule is enough. DISCo offers a coverage principle that may guide selection, while GQR and earlier feedback work constrain what we can claim as new. We will call the combination useful only if a controlled comparison improves retrieval under disclosed feedback and computation costs. The FiQA pilot reports no reliable held-out gain, while coverage-aware selection still awaits a controlled test. The next experiment is designed to answer that question.

### Pointer notes

- Read the three evidence lines from established to measured to proposed.
- Finish on the question and pause; do not announce a complementary-selection gain.

### Sentence provenance

- **S20.01** Source-grounded paraphrase. Sources: [TOUR-M](https://aclanthology.org/2023.findings-acl.354.pdf#page=3), [REFIT-M](https://arxiv.org/pdf/2305.11744v2#page=3). Location: TOUR-M: §3.1–3.3 frozen encoders and optimized query vector. REFIT-M: §3.2 same output-space adaptation principle.
- **S20.02** Source-grounded paraphrase. Sources: [TTT-S](https://arxiv.org/pdf/2608.12569v1#page=4), [TTT-B](https://arxiv.org/pdf/2608.12569v1#page=6). Location: TTT-S: §2.3 scope definitions. TTT-B: §4.1/Table 1 budget-dependent empirical comparison.
- **S20.03** Source-grounded paraphrase. Sources: [RUN](https://github.com/nilansa/ire-project-2026/issues/3#issuecomment-6908737534), [REFIT-SCI](https://arxiv.org/pdf/2305.11744v2#page=4). Location: RUN: three SCIDOCS measured values. REFIT-SCI: v2 Table 2 references; matching means at displayed precision.
- **S20.04** Research direction. Sources: [HYPOTHESIS](#hypothesis). Location: HYPOTHESIS: proposed candidate-selection focus, not a causal explanation of the reproduction gap.
- **S20.05** Our synthesis. Sources: [DISCO](https://proceedings.iclr.cc/paper_files/paper/2026/file/6ded182245f8e4db3963d2027174133d-Paper-Conference.pdf#page=3), [GQR](https://arxiv.org/abs/2510.05038v3), [REFIT-L](https://arxiv.org/html/2305.11744v2#S6.SS6.SSS1). Location: DISCO: §3.1 coverage objective. GQR: abstract complementary guidance. REFIT-L: §6.6.1 informative negatives. Our synthesis defines a narrower question.
- **S20.06** Success criterion. Sources: [DESIGN](#experiment-design). Location: DESIGN: prospective success criterion, requiring a controlled measured gain and disclosed costs.
- **S20.07** Claim boundary. Sources: [FIQA_RUN](https://github.com/nilansa/ire-project-2026/blob/main/research/CEOUS_COMPLEMENTARY_FEEDBACK_2PAGE_WORKING_20261116.md#4-completed-ceous-measurements-not-directly-comparable), [HYPOTHESIS](#hypothesis). Location: FIQA_RUN: §4 table, FiQA Interpretation column reports no reliable held-out transfer; paragraph immediately after the table says neither completed measurement tests complementary selection. HYPOTHESIS: the controlled selection comparison remains proposed.
- **S20.08** Closing. Sources: [BRIEF](#presentation-scope). Location: BRIEF: User brief, 16 Nov 2026: Queos Labs IRE presentation; no encoder or reranker weight updates; source-backed script and proposed complementary-feedback study.

## Reference register

### MSR — Microsoft Research challenge

https://www.microsoft.com/en-us/research/academic-program/microsoft-research-fellowship/research-challenges/

Efficient and accurate post-training of retrieval models: Summary; Description ¶1–2; questions (1)–(3). Also verified against the supplied MSR-Research-Proposal.txt.

### TOUR-M — TOUR · method

https://aclanthology.org/2023.findings-acl.354.pdf#page=3

Sung et al., Findings ACL 2023. PDF pp.3–5, §§3.1–3.5; Eqs.7–13. Encoders fixed: §3.1 ¶1. One step then retrieval: §3.2 paragraph after Eq.10. Caching: §3.5.

### TOUR-HS — TOUR · hard and soft

https://aclanthology.org/2023.findings-acl.354.pdf#page=4

PDF pp.3–4, §3.2 Eq.8 (nucleus pseudo-positive set), Eq.9 (hard objective); §3.3 Eq.12 (forward KL), Eq.13 (update).

### TOUR-R — TOUR · Table 3

https://aclanthology.org/2023.findings-acl.354.pdf#page=7

PDF p.7, printed p.5737, Table 3, DPR_multi rows, EntityQuestions Acc@20 and Acc@100. Iteration settings: Appendix D, PDF p.14, Table 7 (3 phrase-QA, 1 passage).

### REFIT-I — ReFIT · premise

https://arxiv.org/html/2305.11744v2#S1

Reddy et al., arXiv:2305.11744v2 (28 May 2024). Abstract ¶1; Introduction ¶1–4; Figure 1. Precomputable dual encoders versus joint cross-encoder: Introduction ¶3 and §3.1.

### REFIT-M — ReFIT · distillation

https://arxiv.org/pdf/2305.11744v2#page=3

PDF p.3, §3.2 Eqs.5–7 and Algorithm 1; §4.1 (separate min-max normalization, teacher T=2, n=100, learning rate .005); §4.2 (rerank 125 comparator).

### REFIT-R — ReFIT · Table 6

https://arxiv.org/pdf/2305.11744v2#page=6

PDF p.6, Table 6 BEIR column; §5.4 comparison. All plotted values are table-local. Table 2 mean is 69.0 whereas Table 6 reports 69.2; do not silently merge.

### REFIT-TIME — ReFIT · timing

https://arxiv.org/pdf/2305.11744v2#page=3

PDF p.3, Table 1, GPU configuration: R&R K100 400 ms; R&R K125 490 ms; ReFIT K100 470 ms. Separate timing experiment; AMD EPYC 7352 and A100 setup.

### REFIT-SCI — ReFIT · SCIDOCS reference

https://arxiv.org/pdf/2305.11744v2#page=4

PDF p.4, main Table 2 SCIDOCS row: 37.8, 38.3, 40.1 Recall@100. §4.1 specifies 100 steps and LR .005. An older project explainer incorrectly called 40.1 an appendix-only setting; the primary v2 paper governs this presentation.

### REFIT-L — ReFIT · limitations

https://arxiv.org/html/2305.11744v2#S6.SS6.SSS1

§6.6.1, informative negatives; §8 Limitations, teacher quality and latency. Prior work already considers useful negatives and second-pass discovery.

### TTT-I — TTT-Embed · access assumptions

https://arxiv.org/html/2608.12569v1#S1

Chen and Wu, arXiv:2608.12569v1. §1 ¶2–3; Figure 1; Appendix §8 final paragraph: embedding outputs and control of downstream vector search are required.

### TTT-RW — TTT-Embed · TOUR and ReFIT

https://arxiv.org/html/2608.12569v1#S8

PDF p.13, Appendix §8, Pseudo-relevance feedback and query adaptation paragraph, sentences beginning “More closely related…” through the scope question; §3.4 lists evaluated baselines.

### TTT-S — TTT-Embed · sharing scopes

https://arxiv.org/pdf/2608.12569v1#page=4

PDF p.4, §2.3 three scope definitions and following paragraphs. Appendix §10 Eq.14 gives task-balanced weights. §2.3 accepts externally selected rewarded pairs.

### TTT-M — TTT-Embed · residual objective

https://arxiv.org/pdf/2608.12569v1#page=4

§2.2 Eqs.2–4: teacher and normalized student softmax distributions; forward KL plus ridge. §2.4 Eq.5 and final paragraph: alpha=n/(n+1), n counts distinct rewarded queries. Appendix §17.1 gives optimizer settings.

### TTT-B — TTT-Embed · budget results

https://arxiv.org/pdf/2608.12569v1#page=6

PDF p.6, Table 1, average rows at b≈.01/global, b=10/task, b=100/query. §2.1 Eq.1 defines B and b. Appendix §12 candidate/budget paragraph gives first budget 150/12,263; Figure 2 is the full curve.

### TTT-P — TTT-Embed · evaluation protocol

https://arxiv.org/pdf/2608.12569v1#page=15

§3.1; Appendix §12 and Table 6, PDF pp.15–16: 15 task revisions, 12,263 queries, full-corpus re-search. Table 2 and §4.2 distinguish held-out-query transfer from on-query adaptation.

### DISCO — DISCo · collective coverage

https://proceedings.iclr.cc/paper_files/paper/2026/file/6ded182245f8e4db3963d2027174133d-Paper-Conference.pdf#page=3

Nair et al., ICLR 2026. §2 notation, pp.2–3 (contextual token/atom vectors); §3.1 Eq.2 and Algorithm 1 (set coverage); §§3.3–3.4 specialized index. Appendix B p.19 Diversity paragraph; Appendix E.5 p.23 last paragraph: coverage is not explicit diversity maximization.

### GQR — GQR · related work boundary

https://arxiv.org/abs/2510.05038v3

Uzan et al., Guided Query Refinement, ICLR 2026. Abstract: primary query embeddings are refined using complementary-retriever scores. Also discussed in TTT-Embed Appendix §8.

### RUN — Our SCIDOCS run

https://github.com/nilansa/ire-project-2026/issues/3#issuecomment-6908737534

Completed run report, 16 Nov 2026 11:31 IST: 1,000 queries; 25,657 documents; 125,000 physical scores; metrics and frozen-checkpoint settings. Merged predictions SHA256 87a4c0fb58dcf15486ece6591a6a25c736171b2c918cc2b683cb5747c2976727; metrics SHA256 d480dd7d27925952b231cd00162adbab365d5e981a8c0d6567058987396cda8a. Values read from coordinator records, not recomputed in this presentation pass.

### RUN-CI — Our SCIDOCS uncertainty

https://github.com/nilansa/ire-project-2026/issues/3#issuecomment-6909019011

Final issue update: 5,000 paired bootstrap resamples, ReFIT−raw +.065 pp, CI [−.180,+.325]; 22 wins/19 losses/959 ties; 100 new IDs outside top125 across 68 queries, zero judged positive.

### FIQA_RUN — Our reported FiQA TTT pilot

https://github.com/nilansa/ire-project-2026/blob/main/research/CEOUS_COMPLEMENTARY_FEEDBACK_2PAGE_WORKING_20261116.md#4-completed-ceous-measurements-not-directly-comparable

Ceous two-page working report, 16 Nov 2026, §4 table, FiQA task-wise TTT-Embed row, and paragraph immediately after the table. Git blob dfc022cf7b12af4e198f85def4411b91de7c8a03. 648 queries, full 57,638-document corpus; frozen Qwen3-Embedding-0.6B and Qwen3-Reranker-4B; five-fold cross-fit, 80% feedback/20% unscored evaluation, 10 pairs per feedback query. Held-out nDCG@10 .46722→.46313; source-reported delta −.00408, 95% CI [−.01072,+.00262]. Every fold improved in-sample; prior task exposure is disclosed. Selected references item 6 says the original FiQA run ledger is private. These reported values were not independently recomputed here. The displayed means subtract to −.00409; preserve the separately reported delta without inventing its underlying precision. Neither completed measurement tests complementary selection.

### PLAN — Controlled project comparison

https://github.com/nilansa/ire-project-2026/blob/c550bc0152f4264117a36024619dfb04ad02807b/research/BLACKBOX_RERANKER_FEEDBACK_CONTROLLED_COMPARISON_20261116.md

Status header; §3 planned benchmark; §6 status. Compare correction rules on identical scored pairs; compare acquisition policies at equal budget but potentially different pairs. Design, not measurement.

### SCIFACT — Earlier SciFact screen

https://github.com/nilansa/ire-project-2026/blob/c550bc0152f4264117a36024619dfb04ad02807b/experiments/inference-time-ceous-20261115/RESULTS.md

Primary MedCPT results and cost/limitations. 405 DEV and 100 previously exposed INNER queries; 5,183 documents. TOUR-style DEV .747601 versus rerank20 .744338, extra full scan. Optional contextual evidence, not the main result chart.

### DERIVATION — Our explanations and examples

#derivation

SOURCE_LEDGER.md, Mathematical explanations and original examples. Includes output-interface reasoning, the candidate-set schematic, toy probability and coverage examples, and the fixed-teacher forward-KL derivative for unnormalized dot-product logits. The displayed gradient assumes no min-max or vector normalization.

### HYPOTHESIS — Our research hypothesis

#hypothesis

SOURCE_LEDGER.md, Hypothesis boundary. Coverage-aware selection may improve residual learning at fixed teacher budget. This combination is proposed here, not established by DISCo, TTT-Embed or our completed runs.

### DESIGN — Our evaluation design

#experiment-design

SOURCE_LEDGER.md, Experiment design. Sampling, controls, cost accounting and evidence requirements are proposed protocol choices, not reported findings.

### BRIEF — Presentation scope

#presentation-scope

User brief, 16 Nov 2026: Queos Labs IRE presentation; no encoder or reranker weight updates; source-backed script and proposed complementary-feedback study.

