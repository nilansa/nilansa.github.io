# Sentence-to-source ledger

Every spoken sentence is mapped below. Paper statements are paraphrases, not invented quotations. Source locations use one-based PDF pages; equation and table numbers identify the exact object. Original explanatory examples are explicitly marked. A citation to a paper does not convert a proposed combination into a demonstrated result.

## Source register

### MSR — Microsoft Research challenge

Source: https://www.microsoft.com/en-us/research/academic-program/microsoft-research-fellowship/research-challenges/

Efficient and accurate post-training of retrieval models: Summary; Description ¶1–2; questions (1)–(3). Also verified against the supplied MSR-Research-Proposal.txt.

### TOUR-M — TOUR · method

Source: https://aclanthology.org/2023.findings-acl.354.pdf#page=3

Sung et al., Findings ACL 2023. PDF pp.3–5, §§3.1–3.5; Eqs.7–13. Encoders fixed: §3.1 ¶1. One step then retrieval: §3.2 paragraph after Eq.10. Caching: §3.5.

### TOUR-HS — TOUR · hard and soft

Source: https://aclanthology.org/2023.findings-acl.354.pdf#page=4

PDF pp.3–4, §3.2 Eq.8 (nucleus pseudo-positive set), Eq.9 (hard objective); §3.3 Eq.12 (forward KL), Eq.13 (update).

### TOUR-R — TOUR · Table 3

Source: https://aclanthology.org/2023.findings-acl.354.pdf#page=7

PDF p.7, printed p.5737, Table 3, DPR_multi rows, EntityQuestions Acc@20 and Acc@100. Iteration settings: Appendix D, PDF p.14, Table 7 (3 phrase-QA, 1 passage).

### REFIT-I — ReFIT · premise

Source: https://arxiv.org/html/2305.11744v2#S1

Reddy et al., arXiv:2305.11744v2 (28 May 2024). Abstract ¶1; Introduction ¶1–4; Figure 1. Precomputable dual encoders versus joint cross-encoder: Introduction ¶3 and §3.1.

### REFIT-M — ReFIT · distillation

Source: https://arxiv.org/pdf/2305.11744v2#page=3

PDF p.3, §3.2 Eqs.5–7 and Algorithm 1; §4.1 (separate min-max normalization, teacher T=2, n=100, learning rate .005); §4.2 (rerank 125 comparator).

### REFIT-R — ReFIT · Table 6

Source: https://arxiv.org/pdf/2305.11744v2#page=6

PDF p.6, Table 6 BEIR column; §5.4 comparison. All plotted values are table-local. Table 2 mean is 69.0 whereas Table 6 reports 69.2; do not silently merge.

### REFIT-TIME — ReFIT · timing

Source: https://arxiv.org/pdf/2305.11744v2#page=3

PDF p.3, Table 1, GPU configuration: R&R K100 400 ms; R&R K125 490 ms; ReFIT K100 470 ms. Separate timing experiment; AMD EPYC 7352 and A100 setup.

### REFIT-SCI — ReFIT · SCIDOCS reference

Source: https://arxiv.org/pdf/2305.11744v2#page=4

PDF p.4, main Table 2 SCIDOCS row: 37.8, 38.3, 40.1 Recall@100. §4.1 specifies 100 steps and LR .005. An older project explainer incorrectly called 40.1 an appendix-only setting; the primary v2 paper governs this presentation.

### REFIT-L — ReFIT · limitations

Source: https://arxiv.org/html/2305.11744v2#S6.SS6.SSS1

§6.6.1, informative negatives; §8 Limitations, teacher quality and latency. Prior work already considers useful negatives and second-pass discovery.

### TTT-I — TTT-Embed · access assumptions

Source: https://arxiv.org/html/2608.12569v1#S1

Chen and Wu, arXiv:2608.12569v1. §1 ¶2–3; Figure 1; Appendix §8 final paragraph: embedding outputs and control of downstream vector search are required.

### TTT-RW — TTT-Embed · TOUR and ReFIT

Source: https://arxiv.org/html/2608.12569v1#S8

PDF p.13, Appendix §8, Pseudo-relevance feedback and query adaptation paragraph, sentences beginning “More closely related…” through the scope question; §3.4 lists evaluated baselines.

### TTT-S — TTT-Embed · sharing scopes

Source: https://arxiv.org/pdf/2608.12569v1#page=4

PDF p.4, §2.3 three scope definitions and following paragraphs. Appendix §10 Eq.14 gives task-balanced weights. §2.3 accepts externally selected rewarded pairs.

### TTT-M — TTT-Embed · residual objective

Source: https://arxiv.org/pdf/2608.12569v1#page=4

§2.2 Eqs.2–4: teacher and normalized student softmax distributions; forward KL plus ridge. §2.4 Eq.5 and final paragraph: alpha=n/(n+1), n counts distinct rewarded queries. Appendix §17.1 gives optimizer settings.

### TTT-B — TTT-Embed · budget results

Source: https://arxiv.org/pdf/2608.12569v1#page=6

PDF p.6, Table 1, average rows at b≈.01/global, b=10/task, b=100/query. §2.1 Eq.1 defines B and b. Appendix §12 candidate/budget paragraph gives first budget 150/12,263; Figure 2 is the full curve.

### TTT-P — TTT-Embed · evaluation protocol

Source: https://arxiv.org/pdf/2608.12569v1#page=15

§3.1; Appendix §12 and Table 6, PDF pp.15–16: 15 task revisions, 12,263 queries, full-corpus re-search. Table 2 and §4.2 distinguish held-out-query transfer from on-query adaptation.

### DISCO — DISCo · collective coverage

Source: https://proceedings.iclr.cc/paper_files/paper/2026/file/6ded182245f8e4db3963d2027174133d-Paper-Conference.pdf#page=3

Nair et al., ICLR 2026. §2 notation, pp.2–3 (contextual token/atom vectors); §3.1 Eq.2 and Algorithm 1 (set coverage); §§3.3–3.4 specialized index. Appendix B p.19 Diversity paragraph; Appendix E.5 p.23 last paragraph: coverage is not explicit diversity maximization.

### GQR — GQR · related work boundary

Source: https://arxiv.org/abs/2510.05038v3

Uzan et al., Guided Query Refinement, ICLR 2026. Abstract: primary query embeddings are refined using complementary-retriever scores. Also discussed in TTT-Embed Appendix §8.

### RUN — Our SCIDOCS run

Source: https://github.com/nilansa/ire-project-2026/issues/3#issuecomment-6908737534

Completed run report, 16 Nov 2026 11:31 IST: 1,000 queries; 25,657 documents; 125,000 physical scores; metrics and frozen-checkpoint settings. Merged predictions SHA256 87a4c0fb58dcf15486ece6591a6a25c736171b2c918cc2b683cb5747c2976727; metrics SHA256 d480dd7d27925952b231cd00162adbab365d5e981a8c0d6567058987396cda8a. Values read from coordinator records, not recomputed in this presentation pass.

### RUN-CI — Our SCIDOCS uncertainty

Source: https://github.com/nilansa/ire-project-2026/issues/3#issuecomment-6909019011

Final issue update: 5,000 paired bootstrap resamples, ReFIT−raw +.065 pp, CI [−.180,+.325]; 22 wins/19 losses/959 ties; 100 new IDs outside top125 across 68 queries, zero judged positive.

### STATUS — Experiment status snapshot

Source: https://github.com/nilansa/nilansa.github.io/blob/ceb196e1cde8e259e694cf8a9b55ecb30a77fbc1/explainer/explainers/ire-retrieval-feedback-global-state-2026-11-16.html

Published study handover, 16 Nov 2026, plus 13 inspected comments in project issue #3. FiQA/TTT/H8 work is mentioned without a verified numeric result. This establishes only what is verified for this deck; it does not prove that no local run exists.

### PLAN — Controlled project comparison

Source: https://github.com/nilansa/ire-project-2026/blob/c550bc0152f4264117a36024619dfb04ad02807b/research/BLACKBOX_RERANKER_FEEDBACK_CONTROLLED_COMPARISON_20261116.md

Status header; §3 planned benchmark; §6 status. Compare correction rules on identical scored pairs; compare acquisition policies at equal budget but potentially different pairs. Design, not measurement.

### SCIFACT — Earlier SciFact screen

Source: https://github.com/nilansa/ire-project-2026/blob/c550bc0152f4264117a36024619dfb04ad02807b/experiments/inference-time-ceous-20261115/RESULTS.md

Primary MedCPT results and cost/limitations. 405 DEV and 100 previously exposed INNER queries; 5,183 documents. TOUR-style DEV .747601 versus rerank20 .744338, extra full scan. Optional contextual evidence, not the main result chart.

### DERIVATION — Our explanations and examples

Source: #derivation

SOURCE_LEDGER.md, Mathematical explanations and original examples. Includes output-interface reasoning, the candidate-set schematic, toy probability and coverage examples, and the fixed-teacher forward-KL derivative for unnormalized dot-product logits. The displayed gradient assumes no min-max or vector normalization.

### HYPOTHESIS — Our research hypothesis

Source: #hypothesis

SOURCE_LEDGER.md, Hypothesis boundary. Coverage-aware selection may improve residual learning at fixed teacher budget. This combination is proposed here, not established by DISCo, TTT-Embed or our completed run.

### DESIGN — Our evaluation design

Source: #experiment-design

SOURCE_LEDGER.md, Experiment design. Sampling, controls, cost accounting and evidence requirements are proposed protocol choices, not reported findings.

### BRIEF — Presentation scope

Source: #presentation-scope

User brief, 16 Nov 2026: Queos Labs IRE presentation; no encoder or reranker weight updates; source-backed script and proposed complementary-feedback study.

## Sentence ledger

| Sentence | Exact spoken sentence | Evidence type | Source and precise location |
|---|---|---|---|
| S01.01 | Our project asks whether a deployed retrieval system can improve at test time while both model backbones remain frozen. | Project scope | BRIEF: User brief, 16 Nov 2026: Queos Labs IRE presentation; no encoder or reranker weight updates; source-backed script and proposed complementary-feedback study. |
| S01.02 | We assume that the embedding service returns vectors and that a reranker returns relevance scores for selected query-document pairs. | Source-grounded paraphrase | TTT-I: Appendix §8, PDF p.13, final paragraph on the returned-embedding and downstream-search interfaces; §2.1, p.3, opening setup paragraph. |
| S01.03 | The editable object is an external query representation, so the method still learns even though it does not fine-tune either model. | Source-grounded paraphrase | TTT-I: Figure 1, PDF p.2, caption; TTT-M: §2.2, pp.3–4, Eqs.3–4, the residual is the optimization variable. |
| S01.04 | We will follow the progression from TOUR to ReFIT and then to the reusable state in TTT-Embed. | Presentation structure | BRIEF: User brief, 16 Nov 2026: Queos Labs IRE presentation; no encoder or reranker weight updates; source-backed script and proposed complementary-feedback study. |
| S01.05 | After the published evidence, we will inspect our completed SCIDOCS attempt and its unresolved reproduction gap. | Source-grounded paraphrase | RUN: Completed run report, 16 Nov 2026 11:31 IST: 1,000 queries; 25,657 documents; 125,000 physical scores; metrics and frozen-checkpoint settings. Merged predictions SHA256 87a4c0fb58dcf15486ece6591a6a25c736171b2c918cc2b683cb5747c2976727; metrics SHA256 d480dd7d27925952b231cd00162adbab365d5e981a8c0d6567058987396cda8a. Values read from coordinator records, not recomputed in this presentation pass.; RUN-CI: Final issue update: 5,000 paired bootstrap resamples, ReFIT−raw +.065 pp, CI [−.180,+.325]; 22 wins/19 losses/959 ties; 100 new IDs outside top125 across 68 queries, zero judged positive. |
| S01.06 | Finally, can candidates covering complementary evidence teach a better residual under the same feedback budget? | Our hypothesis | HYPOTHESIS: SOURCE_LEDGER.md, Hypothesis boundary. Coverage-aware selection may improve residual learning at fixed teacher budget. This combination is proposed here, not established by DISCo, TTT-Embed or our completed run. |
| S01.07 | That last step is the hypothesis we want to test, rather than a result we can already claim. | Claim boundary | HYPOTHESIS: SOURCE_LEDGER.md, Hypothesis boundary. Coverage-aware selection may improve residual learning at fixed teacher budget. This combination is proposed here, not established by DISCo, TTT-Embed or our completed run. |
| S02.01 | The Microsoft challenge asks how high-quality reward feedback can improve retrieval models and downstream retrieval or generation. | Source-grounded paraphrase | MSR: supplied challenge text, Summary, sole paragraph. |
| S02.02 | It identifies three practical questions: which query-document pairs deserve scoring, which learning loss should use those scores, and how to control computational cost. | Source-grounded paraphrase | MSR: Description, research questions (1) Data Selection, (2) Loss Formulation, and (3) Computational Efficiency. |
| S02.03 | These decisions are connected: a powerful teacher helps only when we spend its judgments well. | Our synthesis | MSR: our synthesis of research questions (1)–(3), not a separately reported paper finding. |
| S02.04 | Our project narrows that broad post-training agenda to a deployed system with frozen model weights and a fixed document index. | Project scope | BRIEF: user-requested no-weight-update setting. TTT-I: §2 opening paragraph, PDF p.3, fixed backbone and index. |
| S02.05 | The question becomes what can be learned outside those models, directly from the feedback available at inference. | Our synthesis | BRIEF: our problem formulation. TTT-I: Introduction, paragraph on learning an external vector from returned embeddings. |
| S02.06 | The literature supplies several query-update mechanisms, while our proposed study returns to the first Microsoft question: which documents should receive expensive feedback? | Our synthesis | MSR: question (1), Data Selection. HYPOTHESIS: our candidate-selection proposal; the Microsoft challenge does not name it. |
| S02.07 | This is our scoped research problem, not a method prescribed by Microsoft. | Claim boundary | BRIEF: User brief, 16 Nov 2026: Queos Labs IRE presentation; no encoder or reranker weight updates; source-backed script and proposed complementary-feedback study. |
| S03.01 | There are three interfaces in our setting: an embedding service, a document-vector index, and a relevance-scoring teacher. | Source-grounded paraphrase | TTT-I: §2.1, PDF p.3, opening paragraph; Appendix §8, PDF p.13, final access-assumptions paragraph. |
| S03.02 | We can read their outputs and issue another vector search, but we do not update encoder weights, reranker weights, or stored document embeddings. | Source-grounded paraphrase | TTT-I: Figure 1 caption, PDF p.2; §2 opening paragraph, p.3. TTT-M: §2.2 Eq.4 optimizes only the external residual. |
| S03.03 | Instead, we optimize a small vector after the embedding service has produced its answer. | Source-grounded paraphrase | TTT-M: §2.2, PDF pp.3–4, Eq.3 (vector addition) and Eq.4 (residual objective). |
| S03.04 | An inaccessible retriever cannot be fine-tuned through a vector-only interface. | Source-grounded paraphrase | TTT-I: Introduction paragraph on parameter access; Appendix §8 final paragraph. Claim is restricted to a vector-only API, not all services called black boxes. |
| S03.05 | A black-box reranker by itself does not prevent training an accessible retriever, because its scores can still supply targets. | Logical clarification | DERIVATION: Source ledger, output-interface reasoning. This follows from scores being usable targets when a separate retriever is trainable; it is a clarification, not an experiment. |
| S03.06 | Our restriction is therefore no model weight updates, with output access sufficient for external optimization. | Project scope | BRIEF: user-requested frozen-model scope. TTT-I: Appendix §8 final paragraph, output access and control of vector search. |
| S03.07 | If a service returns only document identifiers and offers no vector interface, this assumption may fail. | Source-grounded paraphrase | TTT-I: Appendix §8, PDF p.13, final paragraph distinguishing the returned-vector setting from a service exposing only ranked identifiers. |
| S03.08 | Keep that boundary in mind when applying the method to closed models. | Explanation | TTT-I: Appendix §8 final paragraph; explanatory reminder of the stated interface boundary. |
| S04.01 | A dense retriever quickly searches precomputed document vectors and returns a short candidate list. | Source-grounded paraphrase | REFIT-I: §3.1, PDF p.2, paragraph after Eq.3 on precomputed passage embeddings and nearest-neighbor retrieval. |
| S04.02 | A cross-encoder reranker reads each query-document pair jointly and assigns a more detailed relevance score. | Source-grounded paraphrase | REFIT-I: §3.1, PDF p.3, reranker paragraph before Eq.4; Introduction, paragraph comparing dual and cross encoders. |
| S04.03 | In the diagram, the relevant document outside the candidate boundary never reaches that judge. | Illustrative explanation | DERIVATION: original candidate-set schematic. The unseen relevant item is an illustrative example, not a retrieved case from the papers. |
| S04.04 | Reordering a fixed set of K documents can improve their order, but cannot change Recall at K for that same set. | Source-grounded paraphrase | REFIT-I: Abstract ¶1 and Introduction opening paragraph. Fixed-set cardinality qualifier makes the Recall@K claim precise. |
| S04.05 | Reranking 125 documents and keeping 100 can improve Recall at 100, making it a useful comparator. | Source-grounded paraphrase | REFIT-M: §4.2, PDF pp.3–4, final comparison-design paragraph: retrieve/rerank125 but evaluate Recall@100. |
| S04.06 | The feedback question is whether the scores can change the query vector and send it back into the full index. | Source-grounded paraphrase | REFIT-I: Figure 1 and Introduction paragraph describing inference-time distillation followed by second retrieval. |
| S04.07 | That second search could retrieve an item absent from the first list, rather than only reshuffling documents already seen. | Source-grounded paraphrase | REFIT-I: Figure 1 caption and Introduction distillation paragraph; possibility of discovery is not a per-query guarantee. |
| S04.08 | The next methods turn this possibility into an optimization procedure. | Transition | TOUR-M: Sung et al., Findings ACL 2023. PDF pp.3–5, §§3.1–3.5; Eqs.7–13. Encoders fixed: §3.1 ¶1. One step then retrieval: §3.2 paragraph after Eq.10. Caching: §3.5.; REFIT-M: PDF p.3, §3.2 Eqs.5–7 and Algorithm 1; §4.1 (separate min-max normalization, teacher T=2, n=100, learning rate .005); §4.2 (rerank 125 comparator). |
| S05.01 | Start at the original query vector, q zero, and retrieve nearby candidates from the fixed index. | Source-grounded paraphrase | TOUR-M: §3.1, PDF p.3, first two paragraphs; Eq.7 scores the retrieved candidates. |
| S05.02 | TOUR asks a cross-encoder to score those candidates and treats the outputs as pseudo relevance feedback. | Source-grounded paraphrase | TOUR-M: §3.1, PDF p.3, Eq.7 and following paragraph on pseudo labels without gold relevance. |
| S05.03 | The query representation then takes a gradient step using that signal, while both encoders remain fixed. | Source-grounded paraphrase | TOUR-M: §3.1 opening paragraph (fixed encoders); §3.2, PDF p.4, Eq.10 (query-vector gradient descent). |
| S05.04 | Follow the blue arrow to q one: fresh retrieval can now return a different neighborhood. | Diagram explanation | TOUR-M: §3.2, PDF p.4, paragraph after Eq.10 (one step followed by retrieval); Figure 1 (schematic vector movement). |
| S05.05 | The method can repeat this retrieve-score-update process, with cached scores and early stopping reducing some repeated work. | Source-grounded paraphrase | TOUR-M: §3.5, PDF p.5, sole paragraph on maximum iterations, early stopping and cached reranker scores. |
| S05.06 | The number of rounds is task-dependent: its reported settings allow up to three for phrase question answering and one for passage retrieval. | Source-grounded paraphrase | TOUR-R: Appendix D, PDF p.14, Table 7, Max iterations row: 3 for phrase QA and 1 for both passage settings. |
| S05.07 | The mechanism is moving the query and searching again; TOUR does not always run three rounds. | Explanation | TOUR-M: §3.2 Eq.10 and following paragraph. TOUR-R: Appendix D Table 7; task-specific interpretation. |
| S05.08 | Next, we examine how TOUR converts teacher scores into a learning signal. | Transition | TOUR-HS: §3.2 and §3.3 headings and objectives; presentation transition. |
| S06.01 | TOUR provides the hard and soft feedback objectives; these are not ReFIT variants. | Source-grounded paraphrase | TOUR-HS: §3.2 TOUR with Hard Labels and §3.3 TOUR with Soft Labels; ReFIT §2 acknowledges these as TOUR variants. |
| S06.02 | In the hard version, teacher probabilities select a small pseudo-positive set using a cumulative-probability threshold. | Source-grounded paraphrase | TOUR-HS: §3.2, PDF pp.3–4, Eq.8 and adjacent paragraph specifying a smallest cumulative-probability pseudo-positive set. |
| S06.03 | The hard loss increases total student probability on that set, without requiring it to copy every probability. | Source-grounded paraphrase | TOUR-HS: §3.2, PDF p.4, Eq.9 and following paragraph. The loss maximizes marginal probability of the selected set. |
| S06.04 | In the soft version, the entire teacher distribution becomes the target through forward KL divergence. | Source-grounded paraphrase | TOUR-HS: §3.3, PDF p.4, opening paragraph and Eq.12, forward KL from teacher probabilities to student probabilities. |
| S06.05 | These three bars are a teaching example, not benchmark measurements. | Original teaching example | DERIVATION: original toy-probability example recorded in the source ledger; no experimental provenance is asserted. |
| S06.06 | With teacher probabilities point six, point three and point one, an example threshold of point eight selects the first two documents. | Original teaching example | DERIVATION: toy teacher [.6,.3,.1] and illustrative nucleus threshold .8; cumulative sum .9 selects A and B. The paper default threshold is different. |
| S06.07 | Soft guidance retains the preference for the first document over the second, which the hard membership decision discards. | Explanation | TOUR-HS: §3.3 opening paragraph explains that hard labels use teacher scores for a membership decision. DERIVATION: the A/B comparison applies that explanation to the toy example. |
| S06.08 | In both cases, pseudo labels may be wrong, and the encoders remain unchanged. | Explanation | TOUR-M: §3.1 first and third paragraphs (frozen encoders and model-provided pseudo labels). Possibility of label error is a logical qualification. |
| S07.01 | This chart redraws TOUR Table three for the DPR passage retriever on EntityQuestions. | Source-grounded paraphrase | TOUR-R: PDF p.7, Table 3, DPR_multi rows and EntityQuestions columns. |
| S07.02 | The vertical axis is answer-containing passage accuracy, shown at depths twenty and one hundred. | Source-grounded paraphrase | TOUR-R: Table 3 caption and §4.3 paragraph defining top-K accuracy as presence of an answer in the retrieved passages. |
| S07.03 | First compare retrieval with reranking: accuracy at twenty rises from 57.9 to 64.4, while accuracy at one hundred stays at 70.8. | Source-grounded paraphrase | TOUR-R: Table 3, EntityQuestions, DPR_multi and +Re-ranker rows: 57.9/70.8 and 64.4/70.8. |
| S07.04 | The unchanged deeper value illustrates the fixed-candidate limitation discussed earlier. | Our interpretation | TOUR-R: unchanged70.8 in Table 3. REFIT-I: fixed-set Recall@K premise. This is our interpretation of the table. |
| S07.05 | Now follow the blue TOUR-soft bars: the reported values are 66.2 at twenty and 72.5 at one hundred. | Source-grounded paraphrase | TOUR-R: Table 3, EntityQuestions, DPR_multi +TOURsoft row: 66.2/72.5. |
| S07.06 | The higher deeper value is consistent with retrieving answer-containing passages that were missed by the original set. | Our interpretation | TOUR-R: Table 3 and §4.3 results paragraph. Interprets higher hit-rate after retrieval; it does not establish exact per-document identities. |
| S07.07 | These are published results for a specific model and dataset, not our project measurements. | Evidence boundary | TOUR-R: Table 3 caption, dataset and model labels. These values are from the paper, not our run. |
| S07.08 | They show the mechanism can help, without guaranteeing the same gain on another corpus. | Interpretation boundary | TOUR-R: bounded interpretation of Table 3; no universal generalization claim. |
| S08.01 | ReFIT starts from retrieve-and-rerank, separating an expensive feedback round from inexpensive optimization steps. | Source-grounded paraphrase | REFIT-M: Algorithm 1 and §3.2 final two paragraphs, PDF p.3; §5.4 contrasts inner update allocation with TOUR. |
| S08.02 | The teacher scores a fixed candidate set once, and those scores remain targets throughout the inner update. | Source-grounded paraphrase | REFIT-M: Algorithm 1 computes teacher distribution once in step2, before the repeated query-vector update loop. |
| S08.03 | The method performs one hundred query-vector steps in the reported main configuration, then runs a second retrieval over the corpus. | Source-grounded paraphrase | REFIT-M: §4.1, PDF p.3, final sentence specifies n100; §3.2 final paragraph specifies second full-index retrieval. |
| S08.04 | One hundred vector steps therefore does not mean one hundred calls to the reranker. | Explanation | REFIT-M: Algorithm 1, step2 versus steps3–7. Counts gradient updates separately from teacher scoring. |
| S08.05 | The objective makes the retriever distribution resemble the teacher distribution, while all model weights and document vectors remain fixed. | Source-grounded paraphrase | REFIT-M: §3.2, Eqs.5–7, Algorithm 1; cached document embeddings are read from the index rather than updated. |
| S08.06 | The paper normalizes both score lists separately and uses a teacher temperature of two. | Source-grounded paraphrase | REFIT-M: §4.1, PDF p.3, first paragraph: separate min-max normalization and teacher temperature T2. |
| S08.07 | Faithful reproduction matters because these details can change the optimization signal. | Implementation reasoning | REFIT-M: §4.1 normalization and temperature choices. Our implementation reasoning: these choices affect the distributions defining the loss. |
| S08.08 | The contrast with TOUR is the organization of feedback and updates; both methods can retrieve new documents. | Our synthesis | TOUR-M: §3.2 step-and-retrieve paragraph. REFIT-M: Algorithm 1 and §3.2 final paragraph. Our comparison of the two update organizations. |
| S09.01 | Teacher and student are distributions over the same candidates, not models we train together here. | Source-grounded paraphrase | REFIT-M: §3.2 Eqs.5–7 and Algorithm 1; teacher scores fixed while query vector changes. |
| S09.02 | The teacher distribution comes from reranker scores; the student distribution comes from the current query-document similarities. | Source-grounded paraphrase | REFIT-M: §3.2 Eq.5 (reranker distribution) and Eq.6 (retriever distribution). |
| S09.03 | Read the equation as a weighted penalty for disagreement, with teacher probabilities providing weights. | Mathematical explanation | REFIT-M: §3.2 Eq.7. Our reading of the standard forward-KL expression, expanded in the source ledger. |
| S09.04 | We minimize KL from teacher to student; we do not maximize KL and we do not change the teacher. | Source-grounded paraphrase | REFIT-M: §3.2 Eq.7 and Algorithm 1 gradient-descent update. Direction is teacher to student. |
| S09.05 | For a fixed teacher, this is equivalent to maximizing teacher-weighted log probability under the student. | Elementary derivation | DERIVATION: Source ledger, Forward KL, fixed teacher. The teacher-entropy term is constant with respect to the student vector. |
| S09.06 | In the illustrative bars, the teacher favors document A while the student places too much probability on C. | Original teaching example | DERIVATION: original toy distributions teacher[.6,.3,.1] and student[.2,.3,.5]. |
| S09.07 | A useful vector update should reduce that discrepancy, though the shared embedding geometry couples the candidate scores. | Mathematical explanation | DERIVATION: one vector determines all candidate dot products, so candidate logits cannot generally be set independently. |
| S09.08 | The distribution on the right illustrates closer agreement, not a guaranteed result of one gradient step. | Illustration boundary | DERIVATION: original closer distribution[.5,.3,.2], intentionally not claimed as a simulated optimizer iterate. |
| S10.01 | These five bars reproduce the BEIR column from ReFIT Table six. | Source-grounded paraphrase | REFIT-R: PDF p.6, Table 6, BEIR column, all five rows. |
| S10.02 | Recall at one hundred rises from 66.8 for retrieval to 67.6 for the larger-pool reranking comparator. | Source-grounded paraphrase | REFIT-R: Table 6 BEIR Retrieve66.8 and Rerank67.6. REFIT-M: §4.2 defines the rerank125 comparator. |
| S10.03 | The paper reports 68.4 for TOUR hard, 68.1 for TOUR soft, and 69.2 for ReFIT in this comparison. | Source-grounded paraphrase | REFIT-R: Table 6 BEIR TOURhard68.4, TOURsoft68.1, ReFIT69.2. |
| S10.04 | ReFIT is 1.6 percentage points above reranking here; that gap is specific to this comparison. | Arithmetic and qualification | REFIT-R: arithmetic69.2−67.6=1.6 percentage points from Table 6; no relative-percent or cross-benchmark claim. |
| S10.05 | The separate timing strip comes from Table one: ReFIT takes 470 milliseconds in its GPU configuration. | Source-grounded paraphrase | REFIT-TIME: PDF p.3, Table 1, ReFIT total GPU470ms; timing is not the quality chart’s experimental axis. |
| S10.06 | That is slower than reranking one hundred candidates at 400 milliseconds, but faster than reranking 125 at 490 milliseconds. | Source-grounded paraphrase | REFIT-TIME: Table 1 total GPU row: R&R100400ms, R&R125490ms, ReFIT100470ms. |
| S10.07 | The two comparisons show why both candidate depth and extra index searches must be counted. | Our interpretation | REFIT-M: §4.2 baseline design. REFIT-TIME: Table 1 retrieval/reranking/distillation breakdown; our cost interpretation. |
| S10.08 | The source notes preserve the paper’s different aggregate values rather than silently editing them. | Editorial provenance | REFIT-R: Table 2 BEIR average69.0 versus Table 6 BEIR69.2. This is an editorial source-consistency note. |
| S11.01 | Now we move from published tables to our recorded full-corpus SCIDOCS experiment. | Source-grounded paraphrase | RUN: completed SCIDOCS run report opening paragraph and metric list, issuecomment6908737534. |
| S11.02 | We used one thousand queries and all 25,657 documents, with frozen Contriever-msmarco and MiniLM checkpoints. | Source-grounded paraphrase | RUN: opening paragraph:1000 queries,25657 documents and the named frozen checkpoints. |
| S11.03 | Our Recall at one hundred was 37.8067 for raw retrieval, 38.3450 for direct rerank-125, and 37.8717 for the ReFIT attempt. | Source-grounded paraphrase | RUN: three-item measured Recall@100 list, raw37.8067, rerank12538.3450, ReFIT37.8717. |
| S11.04 | The first two match the paper references at their displayed precision, while the adaptation result does not reach the paper’s 40.1. | Source-grounded paraphrase | RUN: measured list. REFIT-SCI: v2 Table 2 SCIDOCS last three columns37.8,38.3,40.1. Agreement is after rounding, not bitwise identity. |
| S11.05 | The paired-bootstrap interval for ReFIT minus raw runs from minus 0.180 to plus 0.325 percentage points, spanning zero. | Source-grounded paraphrase | RUN-CI: issuecomment6909019011, paired-bootstrap ReFIT-minus-raw result and95% interval. |
| S11.06 | This is an unresolved reproduction gap, not evidence that ReFIT cannot work. | Interpretation boundary | RUN and RUN-CI: bounded interpretation of one implementation/run; no claim that the method fails generally. |
| S11.07 | Our recorded update count, learning rate and teacher temperature match the paper’s v2 settings. | Source-grounded paraphrase | RUN: completion-report configuration paragraph (100 updates, LR.005,T2). REFIT-SCI: v2 §4.1 explicitly states the same nominal settings. |
| S11.08 | Matching those settings does not independently validate the implementation. | Interpretation boundary | RUN and REFIT-SCI: matching reported settings does not establish preprocessing or code equivalence. Raw run artifacts were not recomputed in this presentation pass. |
| S12.01 | The previous methods adapt the representation of the query currently being served. | Source-grounded paraphrase | TOUR-M: §3.1 instance-level query optimization. REFIT-M: §3.2 query-specific distillation. |
| S12.02 | TTT-Embed asks whether some of that feedback can survive and help later queries without entering the encoder weights. | Source-grounded paraphrase | TTT-I: Introduction paragraphs on discarded query-specific rewards and external state. TTT-S: §2.3 scope definitions. |
| S12.03 | Its related-work section describes TOUR as query-level optimization and ReFIT as distillation into a query vector before another search. | Source-grounded paraphrase | TTT-RW: Appendix §8, PDF p.13, pseudo-relevance-feedback/query-adaptation paragraph, TOUR and ReFIT descriptions. |
| S12.04 | The authors group these approaches as keeping the optimized state private to the current query. | Source-grounded paraphrase | TTT-RW: same Appendix §8 paragraph, concluding query-private-state characterization. |
| S12.05 | Point to the two paths: a private state is used once, while a shared residual can be reused by other queries. | Diagram explanation | TTT-S: §2.3 three scope definitions. The diagram is an original schematic of the stated reuse relationship. |
| S12.06 | This is the TTT-Embed authors’ framing of prior work, not our experimental result. | Attribution boundary | TTT-RW: Appendix §8 characterization is attributed to TTT-Embed; not an experiment by this project. |
| S12.07 | Their reported baselines do not establish a matched head-to-head victory over TOUR or ReFIT. | Source-grounded paraphrase | TTT-RW: §3.4 Baselines lists raw retrieval, direct reranking and the three TTT scopes; it does not report a matched TOUR/ReFIT benchmark. |
| S12.08 | The new organizing question is where the state should be shared when relevance judgments have a limited budget. | Source-grounded paraphrase | TTT-S: §2.3 concluding discussion of specificity versus reuse. TTT-B: §2.1 Eq.1 workload budget. |
| S13.01 | TTT-Embed defines three sharing scopes for an external residual. | Source-grounded paraphrase | TTT-S: §2.3, PDF p.4, three sharing-scope definitions. |
| S13.02 | A global vector pools feedback across tasks for one embedding model and serves every query using that model. | Source-grounded paraphrase | TTT-S: §2.3 global-wise definition. |
| S13.03 | A task vector pools feedback only within a particular task and serves other queries from that task. | Source-grounded paraphrase | TTT-S: §2.3 task-wise definition. |
| S13.04 | A query vector uses one query’s scored candidates and remains specific to that query. | Source-grounded paraphrase | TTT-S: §2.3 query-wise definition. |
| S13.05 | The learning mechanism stays the same; the grouping of feedback and reuse changes. | Source-grounded paraphrase | TTT-S: §2.3 opening and following paragraphs: one objective with different feedback grouping and reuse. |
| S13.06 | Global learning balances task contributions so tasks with more queries do not automatically dominate the loss. | Source-grounded paraphrase | TTT-S: Appendix §10, PDF p.14, Eq.14 and explanation of task-balanced global weights. |
| S13.07 | A query without its own feedback has no query-specific correction, but it can still receive a learned task or global correction. | Source-grounded paraphrase | TTT-S: §2.3 paragraph following the definitions, behavior for unrewarded queries. |
| S13.08 | The tradeoff is sharing scarce feedback broadly or spending enough to specialize narrowly; the best choice is empirical. | Our synthesis | TTT-S: §2.3 scope discussion. TTT-B: §4.1 empirical budget/scope comparison. The tradeoff is our synthesis of those statements. |
| S14.01 | The student adds a learned residual to the original normalized query vector, then normalizes again. | Source-grounded paraphrase | TTT-M: §2.2 Eq.3, normalized x_q+v used during learning. |
| S14.02 | Its candidate probabilities are compared with fixed teacher probabilities through forward KL divergence. | Source-grounded paraphrase | TTT-M: §2.2 Eq.2 teacher distribution, Eq.3 student distribution and Eq.4 forward-KL objective. |
| S14.03 | The loss averages over the state’s feedback queries and adds a ridge penalty to discourage an excessive residual. | Source-grounded paraphrase | TTT-M: §2.2 Eq.4. TTT-S: Appendix §10 query weights; the average can be task-balanced. |
| S14.04 | Only the external residual is optimized; the embedding model, teacher and stored document vectors remain frozen. | Source-grounded paraphrase | TTT-I: Figure 1 caption and §2 opening paragraph. TTT-M: Eq.4 optimizes only v. |
| S14.05 | After learning, deployment scales the residual by alpha: n divided by n plus one. | Source-grounded paraphrase | TTT-M: §2.4 Eq.5 and adjacent deployment paragraph; shrinkage is applied after the full-residual fit. |
| S14.06 | Here n counts distinct rewarded queries, not documents, so one query scored against many documents still gives alpha equal to one half. | Source-grounded paraphrase | TTT-M: §2.4 final paragraph defines n as distinct rewarded queries and gives query-wise alpha1/2. |
| S14.07 | Shared states supported by more queries receive less shrinkage under this rule. | Source-grounded paraphrase | TTT-M: §2.4 Eq.5; n/(n+1) increases toward1 as distinct rewarded-query count increases. |
| S14.08 | The corrected vector searches the existing full index, so the result set can differ from the feedback candidates. | Source-grounded paraphrase | TTT-P: Appendix §12, Embedding and retrieval protocol paragraph, full-corpus re-search using the corrected query. |
| S15.01 | These are three published operating points from Table one, not a reconstructed continuous curve. | Source-grounded paraphrase | TTT-B: PDF p.6, Table 1, selected budget/scope columns; no unsampled curve is reconstructed. |
| S15.02 | The vertical axis shows nDCG-at-ten gains on a hundred-point scale, averaged over the reported tasks and embedding models. | Source-grounded paraphrase | TTT-B: Table 1 caption and Average rows, gain in nDCG@10×100 across tasks and five embedding models. |
| S15.03 | At the smallest budget, a global state gives 1.23 points while direct reranking gives approximately zero. | Source-grounded paraphrase | TTT-B: Table 1 low-budget Average row: global1.23, direct−.01, verbally approximated as zero. Appendix §12 gives exact budget150/12263. |
| S15.04 | At ten judgments per workload query, the selected task scope gains 6.36 points against 3.21 for direct reranking. | Source-grounded paraphrase | TTT-B: Table 1 b10 Average row: task6.36 and direct3.21. |
| S15.05 | At one hundred, the selected query scope reaches 8.36 against 7.80. | Source-grounded paraphrase | TTT-B: Table 1 b100 Average row: query8.36 and direct7.80. |
| S15.06 | Both budget and scope change across columns; this is not one fixed method’s learning curve. | Chart interpretation | TTT-B: Table 1 column headings change scope alongside budget; this is an interpretation of the selected plotted columns. |
| S15.07 | Budget here counts scored query-document pairs averaged across the workload; it is not complete wall-clock cost. | Source-grounded paraphrase | TTT-B: §2.1 Eq.1 and following paragraph define B and b as feedback-pair counts, excluding base embedding and ANN costs. |
| S15.08 | These paper averages describe the tested regime; our smaller pilot cannot promise to match them. | Comparison boundary | TTT-P: §3.1 and Appendix §12 specify the paper workload. Our statement limits extrapolation to a different pilot sample. |
| S16.01 | We currently have a completed SCIDOCS ReFIT attempt and an earlier exploratory SciFact query-update screen. | Source-grounded paraphrase | RUN: completed SCIDOCS report. SCIFACT: pinned RESULTS.md, primary MedCPT screen and limitations. |
| S16.02 | The project handover mentions TTT-Embed and a coverage pilot, but the inspected records provide no verified numerical results. | Source-grounded paraphrase | STATUS: inspected published handover and issue3 comments at the stated snapshot; absence of a verified numeric result in those records only. |
| S16.03 | That means this presentation should not say that TTT-Embed has been reproduced, beaten, or shown to fail. | Evidence boundary | STATUS: evidence boundary derived from the inspected snapshot, not a verdict on the underlying TTT method. |
| S16.04 | It also does not prove that no separate local experiment is running or has just finished. | Access boundary | STATUS: scope of access in this presentation pass; no claim that all local processes/artifacts were inspected. |
| S16.05 | We can update the marked result slot when its run identifier, settings and metrics become available. | Editorial decision | DESIGN: editorial requirement for the replacement result page: identify the run, configuration and measured metrics. |
| S16.06 | A weak gain cannot be blamed simply on missing model-weight access, because the paper is designed for that exact interface. | Logical clarification | TTT-I: §1 parameter-access premise and Appendix §8 final paragraph. Lack of weight access is part of the intended setting, not a diagnosed failure cause. |
| S16.07 | Before interpreting a discrepancy, we need the actual corpus, candidate selection, score calibration, scope and evaluation protocol. | Evaluation reasoning | TTT-M: §2.2 distributions/objective. TTT-P: Appendix §12 evaluation and candidate construction. Our checklist follows the protocol dependencies. |
| S16.08 | Those checks make the next comparison meaningful. | Evaluation reasoning | DESIGN: SOURCE_LEDGER.md, Experiment design. Sampling, controls, cost accounting and evidence requirements are proposed protocol choices, not reported findings. |
| S17.01 | DISCo studies a different retrieval goal: selecting a small collection whose members collectively cover the query. | Source-grounded paraphrase | DISCO: Abstract and §1 first two paragraphs; §2 formalizes collection-level query coverage. |
| S17.02 | Its representations use contextual token or atom vectors, rather than requiring literal bigram or n-gram matches. | Source-grounded paraphrase | DISCO: §2 notation paragraph, PDF pp.2–3, contextual atoms/token-vector representations. Literal n-gram matching is not a required mechanism. |
| S17.03 | The illustrative matrix shows how four candidates cover three query facets. | Original teaching example | DERIVATION: original four-document, three-facet coverage matrix in the source ledger; illustrative rather than measured. |
| S17.04 | After choosing document one, document two adds almost the same coverage, while document four contributes strongly to a missing facet. | Original teaching example | DERIVATION: toy matrix, conditional on d1 already selected; d2 marginal coverage.05 versus d4.80. |
| S17.05 | The max-per-facet objective avoids giving repeated credit merely for covering an already covered component. | Source-grounded paraphrase | DISCO: §3.1 Eq.2 and immediately following paragraph explaining max coverage of each query atom. |
| S17.06 | This is query-focused complementarity; the paper does not explicitly optimize a generic diversity objective. | Source-grounded paraphrase | DISCO: Appendix B, p.19, Diversity paragraph; Appendix E.5, p.23, final paragraph on not explicitly incorporating diversity. |
| S17.07 | Full DISCo uses a specialized index; borrowing its objective on a candidate pool gives only a coverage-inspired selector. | Method boundary | DISCO: §§3.3–3.4 augmented representation and specialized index. HYPOTHESIS: the restricted candidate-pool selector is our proposal, not the full DISCo algorithm. |
| S17.08 | Our next question is whether choosing feedback candidates this way can improve a residual, which DISCo itself does not establish. | Our hypothesis | HYPOTHESIS: proposed coverage-to-residual experiment; DISCo reports coverage retrieval, not this residual-learning combination. |
| S18.01 | In a simplified softmax model, the gradient is a weighted sum of scored document vectors. | Our derivation | DERIVATION: Source ledger, Simplified gradient. Assumes unnormalized dot-product logits and fixed teacher probabilities. |
| S18.02 | The weight for each document is the student probability minus the teacher probability. | Our derivation | DERIVATION: derivative of forward KL with respect to each student logit is p_student−p_teacher. |
| S18.03 | This shows why the selected candidates matter: they determine the available directions in that local learning signal. | Our inference | DERIVATION: chain rule yields a linear combination of selected document vectors; geometric interpretation is ours. |
| S18.04 | If many candidates contribute similar directions, complementary evidence might expose useful disagreements that the initial neighborhood misses. | Our hypothesis | HYPOTHESIS: proposed usefulness of complementary candidate directions; not an established result. |
| S18.05 | It might also introduce irrelevant or noisy feedback, so the geometric picture is motivation rather than a proof of improvement. | Hypothesis limitation | HYPOTHESIS: noise/irrelevance is a possibility considered by our proposal, not a measured failure rate. |
| S18.06 | This simplified gradient omits the score and vector normalizations used by the actual methods. | Mathematical scope | DERIVATION: displayed gradient omits ReFIT min-max score normalization and TTT-Embed unit normalization; it is not their exact implemented derivative. |
| S18.07 | Generic complementary-retriever guidance already appears in GQR, and ReFIT already discusses informative negatives. | Source-grounded paraphrase | GQR: abstract, complementary-retriever scores guiding a primary query embedding. REFIT-L: §6.6.1 on informative negatives. |
| S18.08 | Our proposed contribution must therefore be the controlled coverage-based candidate selection study under a matched feedback budget. | Proposed contribution | HYPOTHESIS: narrowed proposed contribution after the cited prior-art boundary; not an exhaustive novelty claim. |
| S19.01 | Begin with one hundred to two hundred prespecified queries, retaining the full document corpus. | Proposed protocol | DESIGN: proposed query sampling protocol requested by the user; full corpus retained in every arm. |
| S19.02 | Fewer queries reduce cost but cannot guarantee the paper’s average or a narrow uncertainty interval. | Statistical reasoning | DESIGN: statistical qualification: sample size alone does not determine the mean or confidence-interval width. |
| S19.03 | Compare base top-K feedback with a coverage-inspired selector, plus a broader-pool control and random selection from the same pool. | Proposed protocol | DESIGN: proposed candidate-selection controls, not previously completed runs. |
| S19.04 | Fix query identifiers, teacher, student embeddings, feedback count, loss, optimizer and sharing scope across candidate selectors. | Proposed protocol | PLAN: controlled-comparison design, acquisition-policy comparison. DESIGN: hold the learner and budget fixed while candidate identities may differ. |
| S19.05 | Charge additional retrieval and selection separately, even if teacher-pair counts match. | Proposed cost accounting | DESIGN: cost-accounting proposal; equal teacher counts do not imply equal full runtime. |
| S19.06 | Search the full index after adaptation, then report nDCG, recall, paired uncertainty and judged positives found outside the initial pool. | Proposed evaluation | DESIGN: proposed full-index evaluation, paired estimates and judged-positive discovery measures. |
| S19.07 | For shared states, separate feedback queries from held-out evaluation queries; report single-query adaptation as a different regime. | Proposed protocol | TTT-P: §4.2 and Table 2 distinguish held-out-query transfer. DESIGN: our proposed separation of feedback and evaluation queries. |
| S19.08 | Any helper retriever supplies document IDs; the residual still uses vectors from the same frozen student embedding space. | Implementation requirement | DESIGN: implementation consequence of using a single frozen student embedding space; helper-vector dimensions cannot be substituted into that objective. |
| S20.01 | The literature shows that relevance scores can improve query representations without updating model weights. | Source-grounded paraphrase | TOUR-M: §3.1–3.3 frozen encoders and optimized query vector. REFIT-M: §3.2 same output-space adaptation principle. |
| S20.02 | TTT-Embed studies persistent external states and how sharing scope interacts with the feedback budget. | Source-grounded paraphrase | TTT-S: §2.3 scope definitions. TTT-B: §4.1/Table 1 budget-dependent empirical comparison. |
| S20.03 | Our completed SCIDOCS attempt matches the raw and reranking references, but leaves the ReFIT adaptation gain unresolved. | Source-grounded paraphrase | RUN: three SCIDOCS measured values. REFIT-SCI: v2 Table 2 references; matching means at displayed precision. |
| S20.04 | Next, we propose examining which documents supply the learning signal, rather than assuming a different update rule is enough. | Research direction | HYPOTHESIS: proposed candidate-selection focus, not a causal explanation of the reproduction gap. |
| S20.05 | DISCo offers a coverage principle that may guide selection, while GQR and earlier feedback work constrain what we can claim as new. | Our synthesis | DISCO: §3.1 coverage objective. GQR: abstract complementary guidance. REFIT-L: §6.6.1 informative negatives. Our synthesis defines a narrower question. |
| S20.06 | We will call the combination useful only if a controlled comparison improves retrieval under disclosed feedback and computation costs. | Success criterion | DESIGN: prospective success criterion, requiring a controlled measured gain and disclosed costs. |
| S20.07 | Until verified TTT and selection results arrive, this remains a hypothesis with a concrete evaluation plan. | Claim boundary | STATUS: no verified TTT/selection metrics in the inspected snapshot. HYPOTHESIS: current proposed conclusion. |
| S20.08 | The next experiment is designed to answer that question. | Closing | BRIEF: User brief, 16 Nov 2026: Queos Labs IRE presentation; no encoder or reranker weight updates; source-backed script and proposed complementary-feedback study. |

## Mathematical explanations and original examples

**Output-interface reasoning.** A teacher that returns scores can supervise a separate trainable retriever without exposing teacher weights. A vector-only retriever API does not itself expose a route to update that retriever’s weights. These are logical interface distinctions, not empirical results.

**Candidate-set schematic.** The relevant item drawn outside the initial candidate boundary is an original explanatory example. Reordering a fixed set cannot add an item outside it; a fresh retrieval can change membership. No observed embedding geometry or measured result is implied.

**Forward KL, fixed teacher.** With teacher probabilities t_i and student p_i, KL(t∥p)=Σ_i t_i log(t_i/p_i). The term Σ_i t_i log t_i is constant, so minimizing this KL is equivalent to maximizing Σ_i t_i log p_i. Neither operation changes the teacher.

**Simplified gradient.** Let student logits be uᵀz_i, without normalization or min-max scaling. The derivative with respect to each logit is p_i−t_i. By the chain rule, ∇_u L=Σ_i(p_i−t_i)z_i. The exact normalized TTT objective and min-max-normalized ReFIT implementation have additional dependencies; this displayed identity is a pedagogical special case.

**Toy KL plot.** Teacher [.6,.3,.1], initial student [.2,.3,.5], illustrative closer student [.5,.3,.2]. The third vector is a teaching example, not a simulated or guaranteed optimizer iterate.

**Toy coverage matrix.** d₁=(.9,.2,.1), d₂=(.85,.25,.1), d₃=(.2,.8,.1), d₄=(.1,.2,.9). Under sum of column maxima, F({d₁})=1.20; adding d₂ gives 1.25 (gain .05); d₃ gives 1.80 (gain .60); d₄ gives 2.00 (gain .80). These are illustrative scores, not experiment measurements.

## Hypothesis boundary

The new proposal is a matched-budget study of coverage-aware candidate selection for learning an external residual. Neither DISCo nor TTT-Embed proves that their combination improves retrieval. Complementary-retriever guidance already exists in GQR, and ReFIT discusses informative negatives. Do not claim novelty for those broader ideas.

## Experiment design

Use a prespecified query sample with the full corpus. Freeze student vectors, teacher, loss, optimizer, state scope and evaluation. Compare top-K candidates with coverage-aware and broader-pool/random controls at the same unique teacher-pair budget. Account for the selector and extra searches. Measure paired retrieval quality and judged-positive discovery beyond the initial candidate pool. Evaluate shared-state transfer on separate feedback and evaluation queries. This protocol is proposed, not executed by this presentation task.

## Numerical provenance and known inconsistencies

- TOUR chart: Table 3 EntityQuestions DPR_multi, not a reconstructed Figure 2 latency curve. Acc@K is answer-containing passage accuracy, distinct from macro Recall@K and nDCG.
- ReFIT chart: all BEIR values are from Table 6. Table 2 reports 69.0 for an aggregate whereas Table 6 reports 69.2; neither value has been edited to conceal the difference.
- ReFIT SCIDOCS reference: v2 main Table 2 reports 37.8/38.3/40.1; §4.1 gives 100 steps, LR .005, teacher T=2 and separate score min-max normalization. The previous project explainer’s appendix-only characterization is not used. Matching these nominal settings does not independently validate implementation fidelity.
- TTT chart: Table 1 average gains, with scope changing across the three shown budgets. The low-budget label .01 rounds 150/12,263. Do not subtract rounded cells to invent extra precision or join these bars into a full curve.
- Our SCIDOCS values and bootstrap interval are from linked completed-run reports. Artifact hashes are recorded; the raw predictions were not accessed/recomputed in this pass. “New document” means outside the initial 125; “none judged positive” does not mean all are truly irrelevant.
- TTT and coverage results remain unverified in the inspected snapshot, not asserted to be nonexistent.

## Presentation scope

This is a first review edition prepared from the user’s 16 November brief. It is a presentation and research explanation, not a new model experiment. The bibliography is selective, focused on the requested method sequence; it is not an exhaustive novelty review.

