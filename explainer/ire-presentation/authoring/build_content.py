from pathlib import Path
import json, re, csv, argparse

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description='Generate the source-grounded IRE presentation script and content.')
parser.add_argument('--output', type=Path, default=ROOT / 'web')
OUT = parser.parse_args().output.resolve()
OUT.mkdir(parents=True, exist_ok=True)
BASE = 'https://github.com/nilansa/ire-project-2026/blob/c550bc0152f4264117a36024619dfb04ad02807b/'
sources = {
 'MSR': dict(title='Microsoft Research challenge', url='https://www.microsoft.com/en-us/research/academic-program/microsoft-research-fellowship/research-challenges/', locator='Efficient and accurate post-training of retrieval models: Summary; Description ¶1–2; questions (1)–(3). Also verified against the supplied MSR-Research-Proposal.txt.'),
 'TOUR-M': dict(title='TOUR · method', url='https://aclanthology.org/2023.findings-acl.354.pdf#page=3', locator='Sung et al., Findings ACL 2023. PDF pp.3–5, §§3.1–3.5; Eqs.7–13. Encoders fixed: §3.1 ¶1. One step then retrieval: §3.2 paragraph after Eq.10. Caching: §3.5.'),
 'TOUR-HS': dict(title='TOUR · hard and soft', url='https://aclanthology.org/2023.findings-acl.354.pdf#page=4', locator='PDF pp.3–4, §3.2 Eq.8 (nucleus pseudo-positive set), Eq.9 (hard objective); §3.3 Eq.12 (forward KL), Eq.13 (update).'),
 'TOUR-R': dict(title='TOUR · Table 3', url='https://aclanthology.org/2023.findings-acl.354.pdf#page=7', locator='PDF p.7, printed p.5737, Table 3, DPR_multi rows, EntityQuestions Acc@20 and Acc@100. Iteration settings: Appendix D, PDF p.14, Table 7 (3 phrase-QA, 1 passage).'),
 'REFIT-I': dict(title='ReFIT · premise', url='https://arxiv.org/html/2305.11744v2#S1', locator='Reddy et al., arXiv:2305.11744v2 (28 May 2024). Abstract ¶1; Introduction ¶1–4; Figure 1. Precomputable dual encoders versus joint cross-encoder: Introduction ¶3 and §3.1.'),
 'REFIT-M': dict(title='ReFIT · distillation', url='https://arxiv.org/pdf/2305.11744v2#page=3', locator='PDF p.3, §3.2 Eqs.5–7 and Algorithm 1; §4.1 (separate min-max normalization, teacher T=2, n=100, learning rate .005); §4.2 (rerank 125 comparator).'),
 'REFIT-R': dict(title='ReFIT · Table 6', url='https://arxiv.org/pdf/2305.11744v2#page=6', locator='PDF p.6, Table 6 BEIR column; §5.4 comparison. All plotted values are table-local. Table 2 mean is 69.0 whereas Table 6 reports 69.2; do not silently merge.'),
 'REFIT-TIME': dict(title='ReFIT · timing', url='https://arxiv.org/pdf/2305.11744v2#page=3', locator='PDF p.3, Table 1, GPU configuration: R&R K100 400 ms; R&R K125 490 ms; ReFIT K100 470 ms. Separate timing experiment; AMD EPYC 7352 and A100 setup.'),
 'REFIT-SCI': dict(title='ReFIT · SCIDOCS reference', url='https://arxiv.org/pdf/2305.11744v2#page=4', locator='PDF p.4, main Table 2 SCIDOCS row: 37.8, 38.3, 40.1 Recall@100. §4.1 specifies 100 steps and LR .005. An older project explainer incorrectly called 40.1 an appendix-only setting; the primary v2 paper governs this presentation.'),
 'REFIT-L': dict(title='ReFIT · limitations', url='https://arxiv.org/html/2305.11744v2#S6.SS6.SSS1', locator='§6.6.1, informative negatives; §8 Limitations, teacher quality and latency. Prior work already considers useful negatives and second-pass discovery.'),
 'TTT-I': dict(title='TTT-Embed · access assumptions', url='https://arxiv.org/html/2608.12569v1#S1', locator='Chen and Wu, arXiv:2608.12569v1. §1 ¶2–3; Figure 1; Appendix §8 final paragraph: embedding outputs and control of downstream vector search are required.'),
 'TTT-RW': dict(title='TTT-Embed · TOUR and ReFIT', url='https://arxiv.org/html/2608.12569v1#S8', locator='PDF p.13, Appendix §8, Pseudo-relevance feedback and query adaptation paragraph, sentences beginning “More closely related…” through the scope question; §3.4 lists evaluated baselines.'),
 'TTT-S': dict(title='TTT-Embed · sharing scopes', url='https://arxiv.org/pdf/2608.12569v1#page=4', locator='PDF p.4, §2.3 three scope definitions and following paragraphs. Appendix §10 Eq.14 gives task-balanced weights. §2.3 accepts externally selected rewarded pairs.'),
 'TTT-M': dict(title='TTT-Embed · residual objective', url='https://arxiv.org/pdf/2608.12569v1#page=4', locator='§2.2 Eqs.2–4: teacher and normalized student softmax distributions; forward KL plus ridge. §2.4 Eq.5 and final paragraph: alpha=n/(n+1), n counts distinct rewarded queries. Appendix §17.1 gives optimizer settings.'),
 'TTT-B': dict(title='TTT-Embed · budget results', url='https://arxiv.org/pdf/2608.12569v1#page=6', locator='PDF p.6, Table 1, average rows at b≈.01/global, b=10/task, b=100/query. §2.1 Eq.1 defines B and b. Appendix §12 candidate/budget paragraph gives first budget 150/12,263; Figure 2 is the full curve.'),
 'TTT-P': dict(title='TTT-Embed · evaluation protocol', url='https://arxiv.org/pdf/2608.12569v1#page=15', locator='§3.1; Appendix §12 and Table 6, PDF pp.15–16: 15 task revisions, 12,263 queries, full-corpus re-search. Table 2 and §4.2 distinguish held-out-query transfer from on-query adaptation.'),
 'DISCO': dict(title='DISCo · collective coverage', url='https://proceedings.iclr.cc/paper_files/paper/2026/file/6ded182245f8e4db3963d2027174133d-Paper-Conference.pdf#page=3', locator='Nair et al., ICLR 2026. §2 notation, pp.2–3 (contextual token/atom vectors); §3.1 Eq.2 and Algorithm 1 (set coverage); §§3.3–3.4 specialized index. Appendix B p.19 Diversity paragraph; Appendix E.5 p.23 last paragraph: coverage is not explicit diversity maximization.'),
 'GQR': dict(title='GQR · related work boundary', url='https://arxiv.org/abs/2510.05038v3', locator='Uzan et al., Guided Query Refinement, ICLR 2026. Abstract: primary query embeddings are refined using complementary-retriever scores. Also discussed in TTT-Embed Appendix §8.'),
 'RUN': dict(title='Our SCIDOCS run', url='https://github.com/nilansa/ire-project-2026/issues/3#issuecomment-6908737534', locator='Completed run report, 16 Nov 2026 11:31 IST: 1,000 queries; 25,657 documents; 125,000 physical scores; metrics and frozen-checkpoint settings. Merged predictions SHA256 87a4c0fb58dcf15486ece6591a6a25c736171b2c918cc2b683cb5747c2976727; metrics SHA256 d480dd7d27925952b231cd00162adbab365d5e981a8c0d6567058987396cda8a. Values read from coordinator records, not recomputed in this presentation pass.'),
 'RUN-CI': dict(title='Our SCIDOCS uncertainty', url='https://github.com/nilansa/ire-project-2026/issues/3#issuecomment-6909019011', locator='Final issue update: 5,000 paired bootstrap resamples, ReFIT−raw +.065 pp, CI [−.180,+.325]; 22 wins/19 losses/959 ties; 100 new IDs outside top125 across 68 queries, zero judged positive.'),
 'FIQA_RUN': dict(title='Our reported FiQA TTT pilot', url='https://github.com/nilansa/ire-project-2026/blob/main/research/CEOUS_COMPLEMENTARY_FEEDBACK_2PAGE_WORKING_20261116.md#4-completed-ceous-measurements-not-directly-comparable', locator='Ceous two-page working report, 16 Nov 2026, §4 table, FiQA task-wise TTT-Embed row, and paragraph immediately after the table. Git blob dfc022cf7b12af4e198f85def4411b91de7c8a03. 648 queries, full 57,638-document corpus; frozen Qwen3-Embedding-0.6B and Qwen3-Reranker-4B; five-fold cross-fit, 80% feedback/20% unscored evaluation, 10 pairs per feedback query. Held-out nDCG@10 .46722→.46313; source-reported delta −.00408, 95% CI [−.01072,+.00262]. Every fold improved in-sample; prior task exposure is disclosed. Selected references item 6 says the original FiQA run ledger is private. These reported values were not independently recomputed here. The displayed means subtract to −.00409; preserve the separately reported delta without inventing its underlying precision. Neither completed measurement tests complementary selection.'),
 'PLAN': dict(title='Controlled project comparison', url=BASE+'research/BLACKBOX_RERANKER_FEEDBACK_CONTROLLED_COMPARISON_20261116.md', locator='Status header; §3 planned benchmark; §6 status. Compare correction rules on identical scored pairs; compare acquisition policies at equal budget but potentially different pairs. Design, not measurement.'),
 'SCIFACT': dict(title='Earlier SciFact screen', url=BASE+'experiments/inference-time-ceous-20261115/RESULTS.md', locator='Primary MedCPT results and cost/limitations. 405 DEV and 100 previously exposed INNER queries; 5,183 documents. TOUR-style DEV .747601 versus rerank20 .744338, extra full scan. Optional contextual evidence, not the main result chart.'),
 'DERIVATION': dict(title='Our explanations and examples', url='#derivation', locator='SOURCE_LEDGER.md, Mathematical explanations and original examples. Includes output-interface reasoning, the candidate-set schematic, toy probability and coverage examples, and the fixed-teacher forward-KL derivative for unnormalized dot-product logits. The displayed gradient assumes no min-max or vector normalization.'),
 'HYPOTHESIS': dict(title='Our research hypothesis', url='#hypothesis', locator='SOURCE_LEDGER.md, Hypothesis boundary. Coverage-aware selection may improve residual learning at fixed teacher budget. This combination is proposed here, not established by DISCo, TTT-Embed or our completed runs.'),
 'DESIGN': dict(title='Our evaluation design', url='#experiment-design', locator='SOURCE_LEDGER.md, Experiment design. Sampling, controls, cost accounting and evidence requirements are proposed protocol choices, not reported findings.'),
 'BRIEF': dict(title='Presentation scope', url='#presentation-scope', locator='User brief, 16 Nov 2026: Queos Labs IRE presentation; no encoder or reranker weight updates; source-backed script and proposed complementary-feedback study.')
}

slides=[]
def add(chapter,title,subtitle,kind,evidence,takeaway,visual,sentences,pointers,refs,caveat=''):
    i=len(slides)+1
    notes=[]
    for j,item in enumerate(sentences,1):
        text,source_ids=item[:2]
        mode=item[2] if len(item)>2 else 'Source-grounded paraphrase'
        notes.append(dict(id=f'S{i:02d}.{j:02d}',text=text,refs=source_ids.split(),type=mode))
    slides.append(dict(number=i,id=f's{i:02d}',chapter=chapter,title=title,subtitle=subtitle,kind=kind,evidence=evidence,takeaway=takeaway,visual=visual,notes=notes,pointers=pointers,refs=refs.split(),caveat=caveat))

add('The question','Frozen models.\nBetter retrieval?','Test-time retrieval with black-box reranker feedback and no model weight updates.','cover','Research question','Can better feedback change where we search?',{},[
 ('Our project asks whether a deployed retrieval system can improve at test time while both model backbones remain frozen.','BRIEF','Project scope'),
 ('We assume that the embedding service returns vectors and that a reranker returns relevance scores for selected query-document pairs.','TTT-I'),
 ('The editable object is an external query representation, so the method still learns even though it does not fine-tune either model.','TTT-I TTT-M'),
 ('We will follow the progression from TOUR to ReFIT and then to the reusable state in TTT-Embed.','BRIEF','Presentation structure'),
 ('After the papers, we will inspect our SCIDOCS reproduction gap and the reported FiQA task-wise TTT pilot.','RUN RUN-CI FIQA_RUN'),
 ('Finally, can candidates covering complementary evidence teach a better residual under the same feedback budget?','HYPOTHESIS','Our hypothesis'),
 ('That last step is the hypothesis we want to test, rather than a result we can already claim.','HYPOTHESIS','Claim boundary')
],['Open on the title, then point to “black-box feedback”.','Emphasize that model weights stay frozen; the external vector can still change.'],'BRIEF TTT-I RUN FIQA_RUN HYPOTHESIS')

add('The question','What should expensive\nfeedback buy us?','The Microsoft research challenge is the starting point.','origin','Research motivation','We narrow the problem to useful adaptation after deployment.',{},[
 ('The Microsoft challenge asks how high-quality reward feedback can improve retrieval models and downstream retrieval or generation.','MSR'),
 ('It identifies three practical questions: which query-document pairs deserve scoring, which learning loss should use those scores, and how to control computational cost.','MSR'),
 ('These decisions are connected: a powerful teacher helps only when we spend its judgments well.','MSR','Our synthesis'),
 ('Our project narrows that broad post-training agenda to a deployed system with frozen model weights and a fixed document index.','BRIEF TTT-I','Project scope'),
 ('The question becomes what can be learned outside those models, directly from the feedback available at inference.','BRIEF TTT-I','Our synthesis'),
 ('The literature supplies several query-update mechanisms, while our proposed study returns to the first Microsoft question: which documents should receive expensive feedback?','MSR HYPOTHESIS','Our synthesis'),
 ('This is our scoped research problem, not a method prescribed by Microsoft.','BRIEF','Claim boundary')
],['Move across “Select → Learn → Spend”.','End on the selection column; it returns near the end of the talk.'],'MSR TTT-I HYPOTHESIS')

add('The question','What can we change\nat inference?','Black box means an output interface is available; internal weights and gradients are not required.','access','Problem setting','Frozen encoders. Frozen reranker. Editable vector.',{},[
 ('There are three interfaces in our setting: an embedding service, a document-vector index, and a relevance-scoring teacher.','TTT-I'),
 ('We can read their outputs and issue another vector search, but we do not update encoder weights, reranker weights, or stored document embeddings.','TTT-I TTT-M'),
 ('Instead, we optimize a small vector after the embedding service has produced its answer.','TTT-M'),
 ('An inaccessible retriever cannot be fine-tuned through a vector-only interface.','TTT-I'),
 ('A black-box reranker by itself does not prevent training an accessible retriever, because its scores can still supply targets.','DERIVATION','Logical clarification'),
 ('Our restriction is therefore no model weight updates, with output access sufficient for external optimization.','BRIEF TTT-I','Project scope'),
 ('If a service returns only document identifiers and offers no vector interface, this assumption may fail.','TTT-I'),
 ('Keep that boundary in mind when applying the method to closed models.','TTT-I','Explanation')
],['Point to the two locked model boxes, then the blue external vector.','Read the allowed interface row; do not say that the teacher is unavailable.'],'TTT-I TTT-M')

add('The question','Why is reranking\nnot enough?','A stronger judge can only reorder the candidates it receives.','bottleneck','Method premise','A missed document needs another retrieval step.',{},[
 ('A dense retriever quickly searches precomputed document vectors and returns a short candidate list.','REFIT-I'),
 ('A cross-encoder reranker reads each query-document pair jointly and assigns a more detailed relevance score.','REFIT-I'),
 ('In the diagram, the relevant document outside the candidate boundary never reaches that judge.','DERIVATION','Illustrative explanation'),
 ('Reordering a fixed set of K documents can improve their order, but cannot change Recall at K for that same set.','REFIT-I'),
 ('Reranking 125 documents and keeping 100 can improve Recall at 100, making it a useful comparator.','REFIT-M'),
 ('The feedback question is whether the scores can change the query vector and send it back into the full index.','REFIT-I'),
 ('That second search could retrieve an item absent from the first list, rather than only reshuffling documents already seen.','REFIT-I'),
 ('The next methods turn this possibility into an optimization procedure.','TOUR-M REFIT-M','Transition')
],['Point to the outlined candidate set, then the single relevant item outside it.','Trace the second-search arrow back into the full corpus.'],'REFIT-I REFIT-M')

add('TOUR','Ask. Move.\nSearch again.','TOUR optimizes the already-computed query representation.','tour-loop','Published method','The index stays fixed while the query moves.',{},[
 ('Start at the original query vector, q zero, and retrieve nearby candidates from the fixed index.','TOUR-M'),
 ('TOUR asks a cross-encoder to score those candidates and treats the outputs as pseudo relevance feedback.','TOUR-M'),
 ('The query representation then takes a gradient step using that signal, while both encoders remain fixed.','TOUR-M'),
 ('Follow the blue arrow to q one: fresh retrieval can now return a different neighborhood.','TOUR-M','Diagram explanation'),
 ('The method can repeat this retrieve-score-update process, with cached scores and early stopping reducing some repeated work.','TOUR-M'),
 ('The number of rounds is task-dependent: its reported settings allow up to three for phrase question answering and one for passage retrieval.','TOUR-R'),
 ('The mechanism is moving the query and searching again; TOUR does not always run three rounds.','TOUR-M TOUR-R','Explanation'),
 ('Next, we examine how TOUR converts teacher scores into a learning signal.','TOUR-HS','Transition')
],['Trace the loop clockwise: retrieve, score, update, retrieve.','Point to moving q₀ and q₁; the gray document points never move.'],'TOUR-M TOUR-R')

add('TOUR','Hard labels,\nor soft guidance?','Both are pseudo feedback. The distinction belongs to TOUR.','hard-soft','Published method','Hard selects a set. Soft preserves relative preferences.',{},[
 ('TOUR provides the hard and soft feedback objectives; these are not ReFIT variants.','TOUR-HS'),
 ('In the hard version, teacher probabilities select a small pseudo-positive set using a cumulative-probability threshold.','TOUR-HS'),
 ('The hard loss increases total student probability on that set, without requiring it to copy every probability.','TOUR-HS'),
 ('In the soft version, the entire teacher distribution becomes the target through forward KL divergence.','TOUR-HS'),
 ('These three bars are a teaching example, not benchmark measurements.','DERIVATION','Original teaching example'),
 ('With teacher probabilities point six, point three and point one, an example threshold of point eight selects the first two documents.','DERIVATION','Original teaching example'),
 ('Soft guidance retains the preference for the first document over the second, which the hard membership decision discards.','TOUR-HS DERIVATION','Explanation'),
 ('In both cases, pseudo labels may be wrong, and the encoders remain unchanged.','TOUR-M','Explanation')
],['Point to the bracket over A and B in Hard.','Then point to all three bar heights in Soft. The illustrative threshold is .8, not the paper default.'],'TOUR-HS','Illustrative probabilities and threshold. TOUR Appendix D uses its own tuned settings.')

add('TOUR','Does moving the\nquery recover more?','TOUR paper · DPR on EntityQuestions · passage retrieval.','tour-chart','Published results','Reranking changes order; another search can change the set.',{},[
 ('This chart redraws TOUR Table three for the DPR passage retriever on EntityQuestions.','TOUR-R'),
 ('The vertical axis is answer-containing passage accuracy, shown at depths twenty and one hundred.','TOUR-R'),
 ('First compare retrieval with reranking: accuracy at twenty rises from 57.9 to 64.4, while accuracy at one hundred stays at 70.8.','TOUR-R'),
 ('The unchanged deeper value illustrates the fixed-candidate limitation discussed earlier.','TOUR-R REFIT-I','Our interpretation'),
 ('Now follow the blue TOUR-soft bars: the reported values are 66.2 at twenty and 72.5 at one hundred.','TOUR-R'),
 ('The higher deeper value is consistent with retrieving answer-containing passages that were missed by the original set.','TOUR-R','Our interpretation'),
 ('These are published results for a specific model and dataset, not our project measurements.','TOUR-R','Evidence boundary'),
 ('They show the mechanism can help, without guaranteeing the same gain on another corpus.','TOUR-R','Interpretation boundary')
],['Name the y-axis and the two bar colors before reading values.','Compare Acc@100 for Retrieve and Rerank, then point to TOUR soft at 72.5.'],'TOUR-R')

add('ReFIT','Can we reuse\none scored set?','ReFIT performs many inexpensive vector updates before re-retrieval.','refit-loop','Published method','One teacher pass. Many vector steps. One fresh search.',{},[
 ('ReFIT starts from retrieve-and-rerank, separating an expensive feedback round from inexpensive optimization steps.','REFIT-M'),
 ('The teacher scores a fixed candidate set once, and those scores remain targets throughout the inner update.','REFIT-M'),
 ('The method performs one hundred query-vector steps in the reported main configuration, then runs a second retrieval over the corpus.','REFIT-M'),
 ('One hundred vector steps therefore does not mean one hundred calls to the reranker.','REFIT-M','Explanation'),
 ('The objective makes the retriever distribution resemble the teacher distribution, while all model weights and document vectors remain fixed.','REFIT-M'),
 ('The paper normalizes both score lists separately and uses a teacher temperature of two.','REFIT-M'),
 ('Faithful reproduction matters because these details can change the optimization signal.','REFIT-M','Implementation reasoning'),
 ('The contrast with TOUR is the organization of feedback and updates; both methods can retrieve new documents.','TOUR-M REFIT-M','Our synthesis')
],['Circle “score once”, then point inside the 100-step update box.','Follow the final arrow to the same full corpus index.'],'REFIT-M TOUR-M')

add('ReFIT','What is KL\nteaching the student?','Minimize disagreement with a fixed teacher distribution.','kl','Mathematical explanation','Give more student probability to documents the teacher prefers.',{},[
 ('Teacher and student are distributions over the same candidates, not models we train together here.','REFIT-M'),
 ('The teacher distribution comes from reranker scores; the student distribution comes from the current query-document similarities.','REFIT-M'),
 ('Read the equation as a weighted penalty for disagreement, with teacher probabilities providing weights.','REFIT-M','Mathematical explanation'),
 ('We minimize KL from teacher to student; we do not maximize KL and we do not change the teacher.','REFIT-M'),
 ('For a fixed teacher, this is equivalent to maximizing teacher-weighted log probability under the student.','DERIVATION','Elementary derivation'),
 ('In the illustrative bars, the teacher favors document A while the student places too much probability on C.','DERIVATION','Original teaching example'),
 ('A useful vector update should reduce that discrepancy, though the shared embedding geometry couples the candidate scores.','DERIVATION','Mathematical explanation'),
 ('The distribution on the right illustrates closer agreement, not a guaranteed result of one gradient step.','DERIVATION','Illustration boundary')
],['Read teacher first in KL(teacher ∥ student).','Point to A, then C, and use the “After” button to reveal an illustrative closer distribution.'],'REFIT-M DERIVATION')

add('ReFIT','Is the feedback\nworth another search?','ReFIT paper · BEIR Recall@100 · Table 6.','refit-chart','Published results','Quality and total cost both belong in the comparison.',{},[
 ('These five bars reproduce the BEIR column from ReFIT Table six.','REFIT-R'),
 ('Recall at one hundred rises from 66.8 for retrieval to 67.6 for the larger-pool reranking comparator.','REFIT-R'),
 ('The paper reports 68.4 for TOUR hard, 68.1 for TOUR soft, and 69.2 for ReFIT in this comparison.','REFIT-R'),
 ('ReFIT is 1.6 percentage points above reranking here; that gap is specific to this comparison.','REFIT-R','Arithmetic and qualification'),
 ('The separate timing strip comes from Table one: ReFIT takes 470 milliseconds in its GPU configuration.','REFIT-TIME'),
 ('That is slower than reranking one hundred candidates at 400 milliseconds, but faster than reranking 125 at 490 milliseconds.','REFIT-TIME'),
 ('The two comparisons show why both candidate depth and extra index searches must be counted.','REFIT-M REFIT-TIME','Our interpretation'),
 ('The source notes preserve the paper’s different aggregate values rather than silently editing them.','REFIT-R','Editorial provenance')
],['Read the baseline bars left to right; isolate the 67.6 → 69.2 gap.','Treat the timing strip as a separate experiment, not the x-axis of this score plot.'],'REFIT-R REFIT-TIME','Table 6 reports 69.2; Table 2 reports 69.0 for a BEIR mean. All bars here come only from Table 6.')

add('Our evidence','What happened\nin our SCIDOCS run?','1,000 queries · all 25,657 documents · frozen Contriever and MiniLM.','our-chart','Project result','The run completed. The ReFIT gain was not reproduced.',{},[
 ('Now we move from published tables to our recorded full-corpus SCIDOCS experiment.','RUN'),
 ('We used one thousand queries and all 25,657 documents, with frozen Contriever-msmarco and MiniLM checkpoints.','RUN'),
 ('Our Recall at one hundred was 37.8067 for raw retrieval, 38.3450 for direct rerank-125, and 37.8717 for the ReFIT attempt.','RUN'),
 ('The first two match the paper references at their displayed precision, while the adaptation result does not reach the paper’s 40.1.','RUN REFIT-SCI'),
 ('The paired-bootstrap interval for ReFIT minus raw runs from minus 0.180 to plus 0.325 percentage points, spanning zero.','RUN-CI'),
 ('This is an unresolved reproduction gap, not evidence that ReFIT cannot work.','RUN-CI','Interpretation boundary'),
 ('Our recorded update count, learning rate and teacher temperature match the paper’s v2 settings.','RUN REFIT-SCI','Source-grounded paraphrase'),
 ('Matching those settings does not independently validate the implementation.','RUN REFIT-SCI','Interpretation boundary')
],['Point to each blue local bar, then the hollow paper-reference marker.','End on the interval spanning zero; do not describe it as a confirmed positive gain.'],'RUN RUN-CI REFIT-SCI','Recorded run and bootstrap analysis; raw metrics were not recomputed in this presentation pass.')

add('TTT-Embed','Can one query\nteach the next?','TTT-Embed changes how long feedback survives.','reuse','Authors’ framing','From a query-private update to a reusable external state.',{},[
 ('The previous methods adapt the representation of the query currently being served.','TOUR-M REFIT-M'),
 ('TTT-Embed asks whether some of that feedback can survive and help later queries without entering the encoder weights.','TTT-I TTT-S'),
 ('Its related-work section describes TOUR as query-level optimization and ReFIT as distillation into a query vector before another search.','TTT-RW'),
 ('The authors group these approaches as keeping the optimized state private to the current query.','TTT-RW'),
 ('Point to the two paths: a private state is used once, while a shared residual can be reused by other queries.','TTT-S','Diagram explanation'),
 ('This is the TTT-Embed authors’ framing of prior work, not our experimental result.','TTT-RW','Attribution boundary'),
 ('Their reported baselines do not establish a matched head-to-head victory over TOUR or ReFIT.','TTT-RW'),
 ('The new organizing question is where the state should be shared when relevance judgments have a limited budget.','TTT-S TTT-B')
],['Trace the top private path; then follow the bottom shared-vector fan-out.','Explicitly say this characterization comes from TTT-Embed Appendix §8.'],'TTT-RW TTT-S')

add('TTT-Embed','Three scopes.\nOne residual idea.','Global, task and query are sharing scopes—not three separate retrieval tasks.','scopes','Published method','The scope chooses who contributes feedback and who can reuse it.',{},[
 ('TTT-Embed defines three sharing scopes for an external residual.','TTT-S'),
 ('A global vector pools feedback across tasks for one embedding model and serves every query using that model.','TTT-S'),
 ('A task vector pools feedback only within a particular task and serves other queries from that task.','TTT-S'),
 ('A query vector uses one query’s scored candidates and remains specific to that query.','TTT-S'),
 ('The learning mechanism stays the same; the grouping of feedback and reuse changes.','TTT-S'),
 ('Global learning balances task contributions so tasks with more queries do not automatically dominate the loss.','TTT-S'),
 ('A query without its own feedback has no query-specific correction, but it can still receive a learned task or global correction.','TTT-S'),
 ('The tradeoff is sharing scarce feedback broadly or spending enough to specialize narrowly; the best choice is empirical.','TTT-S TTT-B','Our synthesis')
],['Point to one shared vector on the left, one per task in the middle, one per query on the right.','Say “scope” every time; do not call the three columns tasks.'],'TTT-S')

add('TTT-Embed','How does the\nresidual learn?','The residual is optimized outside the frozen embedding model.','residual','Published method','Fit the teacher distribution, then control the correction magnitude.',{},[
 ('The student adds a learned residual to the original normalized query vector, then normalizes again.','TTT-M'),
 ('Its candidate probabilities are compared with fixed teacher probabilities through forward KL divergence.','TTT-M'),
 ('The loss averages over the state’s feedback queries and adds a ridge penalty to discourage an excessive residual.','TTT-M TTT-S'),
 ('Only the external residual is optimized; the embedding model, teacher and stored document vectors remain frozen.','TTT-I TTT-M'),
 ('After learning, deployment scales the residual by alpha: n divided by n plus one.','TTT-M'),
 ('Here n counts distinct rewarded queries, not documents, so one query scored against many documents still gives alpha equal to one half.','TTT-M'),
 ('Shared states supported by more queries receive less shrinkage under this rule.','TTT-M'),
 ('The corrected vector searches the existing full index, so the result set can differ from the feedback candidates.','TTT-P')
],['Point to the blue v in the update formula; then the KL fitting term and ridge term.','Finish on n = rewarded queries and α = .5 for a query-private state.'],'TTT-M TTT-S TTT-P')

add('TTT-Embed','What does the\nfeedback budget change?','Published gains over raw retrieval · 15 tasks · five embedding models.','ttt-chart','Published results','Low budgets favor sharing in the paper’s tested regime.',{},[
 ('These are three published operating points from Table one, not a reconstructed continuous curve.','TTT-B'),
 ('The vertical axis shows nDCG-at-ten gains on a hundred-point scale, averaged over the reported tasks and embedding models.','TTT-B'),
 ('At the smallest budget, a global state gives 1.23 points while direct reranking gives approximately zero.','TTT-B'),
 ('At ten judgments per workload query, the selected task scope gains 6.36 points against 3.21 for direct reranking.','TTT-B'),
 ('At one hundred, the selected query scope reaches 8.36 against 7.80.','TTT-B'),
 ('Both budget and scope change across columns; this is not one fixed method’s learning curve.','TTT-B','Chart interpretation'),
 ('Budget here counts scored query-document pairs averaged across the workload; it is not complete wall-clock cost.','TTT-B'),
 ('These paper averages describe another workload; our single-task, held-out pilot tests a narrower question.','TTT-P FIQA_RUN','Comparison boundary')
],['Define the gain axis before comparing the bars.','Point to the task-scope pair: 6.36 − 3.21 = 3.15 points.','Mention that b≈.01 is rounded; exact b=150/12,263.'],'TTT-B TTT-P FIQA_RUN')

add('Our evidence','Did the FiQA residual\nhelp held-out queries?','648 queries · all 57,638 documents · five-fold task-wise TTT pilot.','status','Reported project result','The pilot reports no reliable held-out gain. Coverage selection is still untested.',{'metric':'nDCG@10','raw':0.46722,'adapted':0.46313,'reportedDelta':-0.00408,'ci95':[-0.01072,0.00262],'sourceId':'FIQA_RUN'},[
 ('Our reported FiQA pilot tests task-wise TTT on 648 queries and the full 57,638-document corpus.','FIQA_RUN'),
 ('It uses frozen Qwen3-Embedding-0.6B and Qwen3-Reranker-4B.','FIQA_RUN'),
 ('Five-fold cross-fitting uses eighty percent for feedback and twenty percent for unscored evaluation, with ten pairs per feedback query.','FIQA_RUN'),
 ('Held-out nDCG at ten moves from 0.46722 to 0.46313.','FIQA_RUN'),
 ('The source reports a change of minus 0.00408, with a ninety-five-percent interval from minus 0.01072 to plus 0.00262.','FIQA_RUN'),
 ('Every fold improved in-sample, but the held-out interval spans zero, providing no reliable evidence of transfer to unscored queries.','FIQA_RUN','Reported result and bounded interpretation'),
 ('Prior task exposure is disclosed; the private raw artifacts were not independently recomputed for this presentation.','FIQA_RUN','Reported limitation and review boundary'),
 ('One task does not replicate the full paper, and complementary selection remains untested.','FIQA_RUN TTT-P','Evidence boundary')
],['Read the y-axis as raw nDCG@10, not percent; compare raw .46722 with adapted .46313.','Point to the source-reported delta −.00408 and its 95% interval [−.01072,+.00262], which spans zero.','Explain that feedback-query improvement did not yield a reliable held-out gain. Prior task exposure is disclosed; the raw artifacts were not recomputed here.'],'FIQA_RUN TTT-P','Source: working report §4, FiQA row. The displayed rounded means subtract to −.00409, while the report gives Δ−.00408; retain its reported delta and interval. This single exposed task is not the paper’s full replication and does not test complementary selection.')

add('The hypothesis','What if the next document\nadds missing evidence?','DISCo motivates collective query coverage.','coverage','Published idea + illustration','Useful complementarity is coverage of the query.',{},[
 ('DISCo studies a different retrieval goal: selecting a small collection whose members collectively cover the query.','DISCO'),
 ('Its representations use contextual token or atom vectors, rather than requiring literal bigram or n-gram matches.','DISCO'),
 ('The illustrative matrix shows how four candidates cover three query facets.','DERIVATION','Original teaching example'),
 ('After choosing document one, document two adds almost the same coverage, while document four contributes strongly to a missing facet.','DERIVATION','Original teaching example'),
 ('The max-per-facet objective avoids giving repeated credit merely for covering an already covered component.','DISCO'),
 ('This is query-focused complementarity; the paper does not explicitly optimize a generic diversity objective.','DISCO'),
 ('Full DISCo uses a specialized index; borrowing its objective on a candidate pool gives only a coverage-inspired selector.','DISCO HYPOTHESIS','Method boundary'),
 ('Our next question is whether choosing feedback candidates this way can improve a residual, which DISCo itself does not establish.','HYPOTHESIS','Our hypothesis')
],['Click d₂, then d₄ in the matrix to compare marginal coverage.','Point to facet C when explaining the .80 gain. All matrix values are illustrative.'],'DISCO HYPOTHESIS')

add('The hypothesis','Could better candidates\nteach a better direction?','Our proposed bridge from collective coverage to residual learning.','gradient','Hypothesis','Change the feedback set, then measure what the learned vector does.',{},[
 ('In a simplified softmax model, the gradient is a weighted sum of scored document vectors.','DERIVATION','Our derivation'),
 ('The weight for each document is the student probability minus the teacher probability.','DERIVATION','Our derivation'),
 ('This shows why the selected candidates matter: they determine the available directions in that local learning signal.','DERIVATION','Our inference'),
 ('If many candidates contribute similar directions, complementary evidence might expose useful disagreements that the initial neighborhood misses.','HYPOTHESIS','Our hypothesis'),
 ('It might also introduce irrelevant or noisy feedback, so the geometric picture is motivation rather than a proof of improvement.','HYPOTHESIS','Hypothesis limitation'),
 ('This simplified gradient omits the score and vector normalizations used by the actual methods.','DERIVATION','Mathematical scope'),
 ('Generic complementary-retriever guidance already appears in GQR, and ReFIT already discusses informative negatives.','GQR REFIT-L'),
 ('Our proposed contribution must therefore be the controlled coverage-based candidate selection study under a matched feedback budget.','HYPOTHESIS','Proposed contribution')
],['Compare the nearly aligned candidate arrows with the broader useful directions.','Point to “simplified” before explaining the gradient; end on the hypothesis label.'],'DERIVATION GQR REFIT-L HYPOTHESIS')

add('The hypothesis','What would a\nfair test look like?','Reduce the query sample; keep the complete document index.','protocol','Proposed experiment','Same teacher budget. Same residual learner. Different candidate selection.',{},[
 ('Begin with one hundred to two hundred prespecified queries, retaining the full document corpus.','DESIGN','Proposed protocol'),
 ('Fewer queries reduce cost but cannot guarantee the paper’s average or a narrow uncertainty interval.','DESIGN','Statistical reasoning'),
 ('Compare base top-K feedback with a coverage-inspired selector, plus a broader-pool control and random selection from the same pool.','DESIGN','Proposed protocol'),
 ('Fix query identifiers, teacher, student embeddings, feedback count, loss, optimizer and sharing scope across candidate selectors.','PLAN DESIGN','Proposed protocol'),
 ('Charge additional retrieval and selection separately, even if teacher-pair counts match.','DESIGN','Proposed cost accounting'),
 ('Search the full index after adaptation, then report nDCG, recall, paired uncertainty and judged positives found outside the initial pool.','DESIGN','Proposed evaluation'),
 ('For shared states, separate feedback queries from held-out evaluation queries; report single-query adaptation as a different regime.','TTT-P DESIGN','Proposed protocol'),
 ('Any helper retriever supplies document IDs; the residual still uses vectors from the same frozen student embedding space.','DESIGN','Implementation requirement')
],['Point to the full-corpus block: it stays intact in every arm.','Trace selector A and B into the identical learner, then the same evaluation.'],'PLAN TTT-P DESIGN')

add('The hypothesis','What can we\nconclude today?','A testable direction, with clear evidence boundaries.','closing','Provisional conclusion','Can coverage-aware feedback make each judgment more useful?',{},[
 ('The literature shows that relevance scores can improve query representations without updating model weights.','TOUR-M REFIT-M'),
 ('TTT-Embed studies persistent external states and how sharing scope interacts with the feedback budget.','TTT-S TTT-B'),
 ('Our SCIDOCS attempt matches the raw and reranking references, but leaves the ReFIT adaptation gain unresolved.','RUN REFIT-SCI'),
 ('Next, we propose examining which documents supply the learning signal, rather than assuming a different update rule is enough.','HYPOTHESIS','Research direction'),
 ('DISCo offers a coverage principle that may guide selection, while GQR and earlier feedback work constrain what we can claim as new.','DISCO GQR REFIT-L','Our synthesis'),
 ('We will call the combination useful only if a controlled comparison improves retrieval under disclosed feedback and computation costs.','DESIGN','Success criterion'),
 ('The FiQA pilot reports no reliable held-out gain, while coverage-aware selection still awaits a controlled test.','FIQA_RUN HYPOTHESIS','Claim boundary'),
 ('The next experiment is designed to answer that question.','BRIEF','Closing')
],['Read the three evidence lines from established to measured to proposed.','Finish on the question and pause; do not announce a complementary-selection gain.'],'TOUR-M REFIT-M TTT-S RUN FIQA_RUN DISCO HYPOTHESIS')

metadata=dict(title='Frozen models. Better retrieval?',subtitle='Test-time retrieval with black-box reranker feedback and no model weight updates.',team='Queos Labs',project='IRE Project · Ceous',authors=['Nilanjan Sarkar'],affiliation='IIIT Hyderabad',date='16 November 2026',task='ire-web-presentation-20261116',version='First review edition',sourceCutoff='Project evidence checked 16 November 2026, including the published FiQA task-wise TTT pilot. SCIDOCS and FiQA values are reported project measurements, not independently recomputed here; complementary selection remains untested.',canonical='https://nilansa.github.io/explainer/ire-presentation/')

# Exact locations supplement the reusable source register for each spoken claim.
sentence_locations = {'S01.02': 'TTT-I: Appendix §8, PDF p.13, final paragraph on the returned-embedding and downstream-search interfaces; '
           '§2.1, p.3, opening setup paragraph.',
 'S01.03': 'TTT-I: Figure 1, PDF p.2, caption; TTT-M: §2.2, pp.3–4, Eqs.3–4, the residual is the optimization '
           'variable.',
 'S02.01': 'MSR: supplied challenge text, Summary, sole paragraph.',
 'S02.02': 'MSR: Description, research questions (1) Data Selection, (2) Loss Formulation, and (3) Computational '
           'Efficiency.',
 'S02.03': 'MSR: our synthesis of research questions (1)–(3), not a separately reported paper finding.',
 'S02.04': 'BRIEF: user-requested no-weight-update setting. TTT-I: §2 opening paragraph, PDF p.3, fixed backbone and '
           'index.',
 'S02.05': 'BRIEF: our problem formulation. TTT-I: Introduction, paragraph on learning an external vector from '
           'returned embeddings.',
 'S02.06': 'MSR: question (1), Data Selection. HYPOTHESIS: our candidate-selection proposal; the Microsoft challenge '
           'does not name it.',
 'S03.01': 'TTT-I: §2.1, PDF p.3, opening paragraph; Appendix §8, PDF p.13, final access-assumptions paragraph.',
 'S03.02': 'TTT-I: Figure 1 caption, PDF p.2; §2 opening paragraph, p.3. TTT-M: §2.2 Eq.4 optimizes only the external '
           'residual.',
 'S03.03': 'TTT-M: §2.2, PDF pp.3–4, Eq.3 (vector addition) and Eq.4 (residual objective).',
 'S03.04': 'TTT-I: Introduction paragraph on parameter access; Appendix §8 final paragraph. Claim is restricted to a '
           'vector-only API, not all services called black boxes.',
 'S03.05': 'DERIVATION: Source ledger, output-interface reasoning. This follows from scores being usable targets when '
           'a separate retriever is trainable; it is a clarification, not an experiment.',
 'S03.06': 'BRIEF: user-requested frozen-model scope. TTT-I: Appendix §8 final paragraph, output access and control of '
           'vector search.',
 'S03.07': 'TTT-I: Appendix §8, PDF p.13, final paragraph distinguishing the returned-vector setting from a service '
           'exposing only ranked identifiers.',
 'S03.08': 'TTT-I: Appendix §8 final paragraph; explanatory reminder of the stated interface boundary.',
 'S04.01': 'REFIT-I: §3.1, PDF p.2, paragraph after Eq.3 on precomputed passage embeddings and nearest-neighbor '
           'retrieval.',
 'S04.02': 'REFIT-I: §3.1, PDF p.3, reranker paragraph before Eq.4; Introduction, paragraph comparing dual and cross '
           'encoders.',
 'S04.03': 'DERIVATION: original candidate-set schematic. The unseen relevant item is an illustrative example, not a '
           'retrieved case from the papers.',
 'S04.04': 'REFIT-I: Abstract ¶1 and Introduction opening paragraph. Fixed-set cardinality qualifier makes the '
           'Recall@K claim precise.',
 'S04.05': 'REFIT-M: §4.2, PDF pp.3–4, final comparison-design paragraph: retrieve/rerank125 but evaluate Recall@100.',
 'S04.06': 'REFIT-I: Figure 1 and Introduction paragraph describing inference-time distillation followed by second '
           'retrieval.',
 'S04.07': 'REFIT-I: Figure 1 caption and Introduction distillation paragraph; possibility of discovery is not a '
           'per-query guarantee.',
 'S05.01': 'TOUR-M: §3.1, PDF p.3, first two paragraphs; Eq.7 scores the retrieved candidates.',
 'S05.02': 'TOUR-M: §3.1, PDF p.3, Eq.7 and following paragraph on pseudo labels without gold relevance.',
 'S05.03': 'TOUR-M: §3.1 opening paragraph (fixed encoders); §3.2, PDF p.4, Eq.10 (query-vector gradient descent).',
 'S05.04': 'TOUR-M: §3.2, PDF p.4, paragraph after Eq.10 (one step followed by retrieval); Figure 1 (schematic vector '
           'movement).',
 'S05.05': 'TOUR-M: §3.5, PDF p.5, sole paragraph on maximum iterations, early stopping and cached reranker scores.',
 'S05.06': 'TOUR-R: Appendix D, PDF p.14, Table 7, Max iterations row: 3 for phrase QA and 1 for both passage '
           'settings.',
 'S05.07': 'TOUR-M: §3.2 Eq.10 and following paragraph. TOUR-R: Appendix D Table 7; task-specific interpretation.',
 'S05.08': 'TOUR-HS: §3.2 and §3.3 headings and objectives; presentation transition.',
 'S06.01': 'TOUR-HS: §3.2 TOUR with Hard Labels and §3.3 TOUR with Soft Labels; ReFIT §2 acknowledges these as TOUR '
           'variants.',
 'S06.02': 'TOUR-HS: §3.2, PDF pp.3–4, Eq.8 and adjacent paragraph specifying a smallest cumulative-probability '
           'pseudo-positive set.',
 'S06.03': 'TOUR-HS: §3.2, PDF p.4, Eq.9 and following paragraph. The loss maximizes marginal probability of the '
           'selected set.',
 'S06.04': 'TOUR-HS: §3.3, PDF p.4, opening paragraph and Eq.12, forward KL from teacher probabilities to student '
           'probabilities.',
 'S06.05': 'DERIVATION: original toy-probability example recorded in the source ledger; no experimental provenance is '
           'asserted.',
 'S06.06': 'DERIVATION: toy teacher [.6,.3,.1] and illustrative nucleus threshold .8; cumulative sum .9 selects A and '
           'B. The paper default threshold is different.',
 'S06.07': 'TOUR-HS: §3.3 opening paragraph explains that hard labels use teacher scores for a membership decision. '
           'DERIVATION: the A/B comparison applies that explanation to the toy example.',
 'S06.08': 'TOUR-M: §3.1 first and third paragraphs (frozen encoders and model-provided pseudo labels). Possibility of '
           'label error is a logical qualification.',
 'S07.01': 'TOUR-R: PDF p.7, Table 3, DPR_multi rows and EntityQuestions columns.',
 'S07.02': 'TOUR-R: Table 3 caption and §4.3 paragraph defining top-K accuracy as presence of an answer in the '
           'retrieved passages.',
 'S07.03': 'TOUR-R: Table 3, EntityQuestions, DPR_multi and +Re-ranker rows: 57.9/70.8 and 64.4/70.8.',
 'S07.04': 'TOUR-R: unchanged70.8 in Table 3. REFIT-I: fixed-set Recall@K premise. This is our interpretation of the '
           'table.',
 'S07.05': 'TOUR-R: Table 3, EntityQuestions, DPR_multi +TOURsoft row: 66.2/72.5.',
 'S07.06': 'TOUR-R: Table 3 and §4.3 results paragraph. Interprets higher hit-rate after retrieval; it does not '
           'establish exact per-document identities.',
 'S07.07': 'TOUR-R: Table 3 caption, dataset and model labels. These values are from the paper, not our run.',
 'S07.08': 'TOUR-R: bounded interpretation of Table 3; no universal generalization claim.',
 'S08.01': 'REFIT-M: Algorithm 1 and §3.2 final two paragraphs, PDF p.3; §5.4 contrasts inner update allocation with '
           'TOUR.',
 'S08.02': 'REFIT-M: Algorithm 1 computes teacher distribution once in step2, before the repeated query-vector update '
           'loop.',
 'S08.03': 'REFIT-M: §4.1, PDF p.3, final sentence specifies n100; §3.2 final paragraph specifies second full-index '
           'retrieval.',
 'S08.04': 'REFIT-M: Algorithm 1, step2 versus steps3–7. Counts gradient updates separately from teacher scoring.',
 'S08.05': 'REFIT-M: §3.2, Eqs.5–7, Algorithm 1; cached document embeddings are read from the index rather than '
           'updated.',
 'S08.06': 'REFIT-M: §4.1, PDF p.3, first paragraph: separate min-max normalization and teacher temperature T2.',
 'S08.07': 'REFIT-M: §4.1 normalization and temperature choices. Our implementation reasoning: these choices affect '
           'the distributions defining the loss.',
 'S08.08': 'TOUR-M: §3.2 step-and-retrieve paragraph. REFIT-M: Algorithm 1 and §3.2 final paragraph. Our comparison of '
           'the two update organizations.',
 'S09.01': 'REFIT-M: §3.2 Eqs.5–7 and Algorithm 1; teacher scores fixed while query vector changes.',
 'S09.02': 'REFIT-M: §3.2 Eq.5 (reranker distribution) and Eq.6 (retriever distribution).',
 'S09.03': 'REFIT-M: §3.2 Eq.7. Our reading of the standard forward-KL expression, expanded in the source ledger.',
 'S09.04': 'REFIT-M: §3.2 Eq.7 and Algorithm 1 gradient-descent update. Direction is teacher to student.',
 'S09.05': 'DERIVATION: Source ledger, Forward KL, fixed teacher. The teacher-entropy term is constant with respect to '
           'the student vector.',
 'S09.06': 'DERIVATION: original toy distributions teacher[.6,.3,.1] and student[.2,.3,.5].',
 'S09.07': 'DERIVATION: one vector determines all candidate dot products, so candidate logits cannot generally be set '
           'independently.',
 'S09.08': 'DERIVATION: original closer distribution[.5,.3,.2], intentionally not claimed as a simulated optimizer '
           'iterate.',
 'S10.01': 'REFIT-R: PDF p.6, Table 6, BEIR column, all five rows.',
 'S10.02': 'REFIT-R: Table 6 BEIR Retrieve66.8 and Rerank67.6. REFIT-M: §4.2 defines the rerank125 comparator.',
 'S10.03': 'REFIT-R: Table 6 BEIR TOURhard68.4, TOURsoft68.1, ReFIT69.2.',
 'S10.04': 'REFIT-R: arithmetic69.2−67.6=1.6 percentage points from Table 6; no relative-percent or cross-benchmark '
           'claim.',
 'S10.05': 'REFIT-TIME: PDF p.3, Table 1, ReFIT total GPU470ms; timing is not the quality chart’s experimental axis.',
 'S10.06': 'REFIT-TIME: Table 1 total GPU row: R&R100400ms, R&R125490ms, ReFIT100470ms.',
 'S10.07': 'REFIT-M: §4.2 baseline design. REFIT-TIME: Table 1 retrieval/reranking/distillation breakdown; our cost '
           'interpretation.',
 'S10.08': 'REFIT-R: Table 2 BEIR average69.0 versus Table 6 BEIR69.2. This is an editorial source-consistency note.',
 'S11.01': 'RUN: completed SCIDOCS run report opening paragraph and metric list, issuecomment6908737534.',
 'S11.02': 'RUN: opening paragraph:1000 queries,25657 documents and the named frozen checkpoints.',
 'S11.03': 'RUN: three-item measured Recall@100 list, raw37.8067, rerank12538.3450, ReFIT37.8717.',
 'S11.04': 'RUN: measured list. REFIT-SCI: v2 Table 2 SCIDOCS last three columns37.8,38.3,40.1. Agreement is after '
           'rounding, not bitwise identity.',
 'S11.05': 'RUN-CI: issuecomment6909019011, paired-bootstrap ReFIT-minus-raw result and95% interval.',
 'S11.06': 'RUN and RUN-CI: bounded interpretation of one implementation/run; no claim that the method fails '
           'generally.',
 'S11.07': 'RUN: completion-report configuration paragraph (100 updates, LR.005,T2). REFIT-SCI: v2 §4.1 explicitly '
           'states the same nominal settings.',
 'S11.08': 'RUN and REFIT-SCI: matching reported settings does not establish preprocessing or code equivalence. Raw '
           'run artifacts were not recomputed in this presentation pass.',
 'S12.01': 'TOUR-M: §3.1 instance-level query optimization. REFIT-M: §3.2 query-specific distillation.',
 'S12.02': 'TTT-I: Introduction paragraphs on discarded query-specific rewards and external state. TTT-S: §2.3 scope '
           'definitions.',
 'S12.03': 'TTT-RW: Appendix §8, PDF p.13, pseudo-relevance-feedback/query-adaptation paragraph, TOUR and ReFIT '
           'descriptions.',
 'S12.04': 'TTT-RW: same Appendix §8 paragraph, concluding query-private-state characterization.',
 'S12.05': 'TTT-S: §2.3 three scope definitions. The diagram is an original schematic of the stated reuse '
           'relationship.',
 'S12.06': 'TTT-RW: Appendix §8 characterization is attributed to TTT-Embed; not an experiment by this project.',
 'S12.07': 'TTT-RW: §3.4 Baselines lists raw retrieval, direct reranking and the three TTT scopes; it does not report '
           'a matched TOUR/ReFIT benchmark.',
 'S12.08': 'TTT-S: §2.3 concluding discussion of specificity versus reuse. TTT-B: §2.1 Eq.1 workload budget.',
 'S13.01': 'TTT-S: §2.3, PDF p.4, three sharing-scope definitions.',
 'S13.02': 'TTT-S: §2.3 global-wise definition.',
 'S13.03': 'TTT-S: §2.3 task-wise definition.',
 'S13.04': 'TTT-S: §2.3 query-wise definition.',
 'S13.05': 'TTT-S: §2.3 opening and following paragraphs: one objective with different feedback grouping and reuse.',
 'S13.06': 'TTT-S: Appendix §10, PDF p.14, Eq.14 and explanation of task-balanced global weights.',
 'S13.07': 'TTT-S: §2.3 paragraph following the definitions, behavior for unrewarded queries.',
 'S13.08': 'TTT-S: §2.3 scope discussion. TTT-B: §4.1 empirical budget/scope comparison. The tradeoff is our synthesis '
           'of those statements.',
 'S14.01': 'TTT-M: §2.2 Eq.3, normalized x_q+v used during learning.',
 'S14.02': 'TTT-M: §2.2 Eq.2 teacher distribution, Eq.3 student distribution and Eq.4 forward-KL objective.',
 'S14.03': 'TTT-M: §2.2 Eq.4. TTT-S: Appendix §10 query weights; the average can be task-balanced.',
 'S14.04': 'TTT-I: Figure 1 caption and §2 opening paragraph. TTT-M: Eq.4 optimizes only v.',
 'S14.05': 'TTT-M: §2.4 Eq.5 and adjacent deployment paragraph; shrinkage is applied after the full-residual fit.',
 'S14.06': 'TTT-M: §2.4 final paragraph defines n as distinct rewarded queries and gives query-wise alpha1/2.',
 'S14.07': 'TTT-M: §2.4 Eq.5; n/(n+1) increases toward1 as distinct rewarded-query count increases.',
 'S14.08': 'TTT-P: Appendix §12, Embedding and retrieval protocol paragraph, full-corpus re-search using the corrected '
           'query.',
 'S15.01': 'TTT-B: PDF p.6, Table 1, selected budget/scope columns; no unsampled curve is reconstructed.',
 'S15.02': 'TTT-B: Table 1 caption and Average rows, gain in nDCG@10×100 across tasks and five embedding models.',
 'S15.03': 'TTT-B: Table 1 low-budget Average row: global1.23, direct−.01, verbally approximated as zero. Appendix §12 '
           'gives exact budget150/12263.',
 'S15.04': 'TTT-B: Table 1 b10 Average row: task6.36 and direct3.21.',
 'S15.05': 'TTT-B: Table 1 b100 Average row: query8.36 and direct7.80.',
 'S15.06': 'TTT-B: Table 1 column headings change scope alongside budget; this is an interpretation of the selected '
           'plotted columns.',
 'S15.07': 'TTT-B: §2.1 Eq.1 and following paragraph define B and b as feedback-pair counts, excluding base embedding '
           'and ANN costs.',
 'S15.08': 'TTT-P: §3.1 and Appendix §12 specify the paper workload. FIQA_RUN: working report §4 FiQA row specifies '
           'one task and held-out cross-fitting; the pilot does not replicate the full paper workload.',
 'S16.01': 'FIQA_RUN: working report §4, table, FiQA task-wise TTT-Embed row, Dataset and feedback column: 648 queries '
           'and 57,638 documents. Exact report Git blob dfc022cf7b12af4e198f85def4411b91de7c8a03.',
 'S16.02': 'FIQA_RUN: §4 table, FiQA row, Experiment column names frozen Qwen3-Embedding-0.6B and Qwen3-Reranker-4B.',
 'S16.03': 'FIQA_RUN: §4 table, FiQA row, Dataset and feedback column: 5 folds, 80% feedback/20% unscored evaluation '
           'and 10 rewarded pairs per training query.',
 'S16.04': 'FIQA_RUN: §4 table, FiQA row, Raw → adapted column: held-out nDCG@10 .46722→.46313. Raw nDCG units, not '
           'percentages.',
 'S16.05': 'FIQA_RUN: §4 table, FiQA row, Raw → adapted column: separately reported delta −.00408 and 95% CI '
           '[−.01072,+.00262]. The displayed rounded means subtract to −.00409; preserve the source-reported delta '
           'without inventing hidden precision.',
 'S16.06': 'FIQA_RUN: §4 table, FiQA row, Interpretation column says every fold improved in-sample and no reliable '
           'held-out transfer. The adjacent interval crosses zero; its bounded interpretation is stated here.',
 'S16.07': 'FIQA_RUN: §4 table, FiQA Interpretation column discloses one exposed task. Selected references item 6 '
           'identifies the original private FiQA cross-fit run ledger. This presentation read the report, not the '
           'private raw artifacts, and did not independently recompute the result.',
 'S17.01': 'DISCO: Abstract and §1 first two paragraphs; §2 formalizes collection-level query coverage.',
 'S17.02': 'DISCO: §2 notation paragraph, PDF pp.2–3, contextual atoms/token-vector representations. Literal n-gram '
           'matching is not a required mechanism.',
 'S17.03': 'DERIVATION: original four-document, three-facet coverage matrix in the source ledger; illustrative rather '
           'than measured.',
 'S17.04': 'DERIVATION: toy matrix, conditional on d1 already selected; d2 marginal coverage.05 versus d4.80.',
 'S17.05': 'DISCO: §3.1 Eq.2 and immediately following paragraph explaining max coverage of each query atom.',
 'S17.06': 'DISCO: Appendix B, p.19, Diversity paragraph; Appendix E.5, p.23, final paragraph on not explicitly '
           'incorporating diversity.',
 'S17.07': 'DISCO: §§3.3–3.4 augmented representation and specialized index. HYPOTHESIS: the restricted candidate-pool '
           'selector is our proposal, not the full DISCo algorithm.',
 'S17.08': 'HYPOTHESIS: proposed coverage-to-residual experiment; DISCo reports coverage retrieval, not this '
           'residual-learning combination.',
 'S18.01': 'DERIVATION: Source ledger, Simplified gradient. Assumes unnormalized dot-product logits and fixed teacher '
           'probabilities.',
 'S18.02': 'DERIVATION: derivative of forward KL with respect to each student logit is p_student−p_teacher.',
 'S18.03': 'DERIVATION: chain rule yields a linear combination of selected document vectors; geometric interpretation '
           'is ours.',
 'S18.04': 'HYPOTHESIS: proposed usefulness of complementary candidate directions; not an established result.',
 'S18.05': 'HYPOTHESIS: noise/irrelevance is a possibility considered by our proposal, not a measured failure rate.',
 'S18.06': 'DERIVATION: displayed gradient omits ReFIT min-max score normalization and TTT-Embed unit normalization; '
           'it is not their exact implemented derivative.',
 'S18.07': 'GQR: abstract, complementary-retriever scores guiding a primary query embedding. REFIT-L: §6.6.1 on '
           'informative negatives.',
 'S18.08': 'HYPOTHESIS: narrowed proposed contribution after the cited prior-art boundary; not an exhaustive novelty '
           'claim.',
 'S19.01': 'DESIGN: proposed query sampling protocol requested by the user; full corpus retained in every arm.',
 'S19.02': 'DESIGN: statistical qualification: sample size alone does not determine the mean or confidence-interval '
           'width.',
 'S19.03': 'DESIGN: proposed candidate-selection controls, not previously completed runs.',
 'S19.04': 'PLAN: controlled-comparison design, acquisition-policy comparison. DESIGN: hold the learner and budget '
           'fixed while candidate identities may differ.',
 'S19.05': 'DESIGN: cost-accounting proposal; equal teacher counts do not imply equal full runtime.',
 'S19.06': 'DESIGN: proposed full-index evaluation, paired estimates and judged-positive discovery measures.',
 'S19.07': 'TTT-P: §4.2 and Table 2 distinguish held-out-query transfer. DESIGN: our proposed separation of feedback '
           'and evaluation queries.',
 'S19.08': 'DESIGN: implementation consequence of using a single frozen student embedding space; helper-vector '
           'dimensions cannot be substituted into that objective.',
 'S20.01': 'TOUR-M: §3.1–3.3 frozen encoders and optimized query vector. REFIT-M: §3.2 same output-space adaptation '
           'principle.',
 'S20.02': 'TTT-S: §2.3 scope definitions. TTT-B: §4.1/Table 1 budget-dependent empirical comparison.',
 'S20.03': 'RUN: three SCIDOCS measured values. REFIT-SCI: v2 Table 2 references; matching means at displayed '
           'precision.',
 'S20.04': 'HYPOTHESIS: proposed candidate-selection focus, not a causal explanation of the reproduction gap.',
 'S20.05': 'DISCO: §3.1 coverage objective. GQR: abstract complementary guidance. REFIT-L: §6.6.1 informative '
           'negatives. Our synthesis defines a narrower question.',
 'S20.06': 'DESIGN: prospective success criterion, requiring a controlled measured gain and disclosed costs.',
 'S20.07': 'FIQA_RUN: §4 table, FiQA Interpretation column reports no reliable held-out transfer; paragraph '
           'immediately after the table says neither completed measurement tests complementary selection. HYPOTHESIS: '
           'the controlled selection comparison remains proposed.',
 'S01.05': 'RUN and RUN-CI: completed SCIDOCS report and bootstrap interval. FIQA_RUN: working report §4, FiQA '
           'task-wise TTT-Embed row; this is a reported project pilot, not independently recomputed evidence.',
 'S16.08': 'FIQA_RUN: §4 table, FiQA Interpretation column distinguishes this one task from the paper’s 15-task '
           'replication; paragraph immediately after the table says neither experiment tests complementary pair '
           'selection. TTT-P: §3.1 and Appendix §12 define the paper’s 15-task workload.'}

for s in slides:
    s['wordCount']=len(re.findall(r"\b[\w’'-]+\b",' '.join(n['text'] for n in s['notes'])))
    s['secondsAt130Wpm']=round(s['wordCount']/130*60)
    assert 120 <= s['wordCount'] <= 130, (s['number'], s['wordCount'])
    for n in s['notes']:
        assert all(r in sources for r in n['refs']),n
        n['exactLocation'] = sentence_locations.get(n['id'], '; '.join(f"{r}: {sources[r]['locator']}" for r in n['refs']))

data=dict(meta=metadata,sources=sources,slides=slides)
OUT.joinpath('content.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')

script=['# Frozen models. Better retrieval?','',metadata['subtitle'],'','**Queos Labs · IRE Project · IIIT Hyderabad**','',', '.join(metadata['authors']),'','16 November 2026 · First review edition','',
 '## How to use this script','',
 'Twenty pages, each intended for about one minute. The spoken text is source-grounded paraphrase, with original teaching examples, deductions and the proposed hypothesis explicitly identified in SOURCE_LEDGER.md. Pointer notes are stage directions and are not part of the narration. Read at a natural pace; pause briefly over plots. Exact durations depend on delivery.','',
 'The title states the access constraint precisely: model weights stay frozen, while a query vector or external residual is optimized. A black-box teacher remains available through its relevance scores.','',
 'Published results, reported project measurements and untested hypotheses are separately labelled. The SCIDOCS values come from project run reports with recorded hashes; the FiQA task-wise TTT pilot comes from the published working report, §4. This pass did not independently recompute either run’s raw artifacts. FiQA reports no reliable held-out gain on one previously exposed task. Neither completed measurement tests complementary selection.','']
for s in slides:
    script += [f"## Page {s['number']:02d} — {s['title'].replace(chr(10),' ')}",'',f"**On screen:** {s['subtitle']}",'',f"**Evidence:** {s['evidence']} · **Spoken words:** {s['wordCount']} · **Estimated delivery:** {s['secondsAt130Wpm']} seconds at 130 words/minute",'',f"**Takeaway:** {s['takeaway']}",'','### Spoken script','']
    script += [' '.join(n['text'] for n in s['notes']),'','### Pointer notes','']
    script += [f'- {p}' for p in s['pointers']]
    if s['caveat']: script += ['',f"**Technical note:** {s['caveat']}"]
    script += ['','### Sentence provenance','']
    script += [f"- **{n['id']}** {n['type']}. Sources: "+', '.join(f"[{r}]({sources[r]['url']})" for r in n['refs']) + f". Location: {n['exactLocation']}" for n in s['notes']]
    script += ['']
script += ['## Reference register','']
for sid,src in sources.items(): script += [f"### {sid} — {src['title']}",'',src['url'],'',src['locator'],'']
OUT.joinpath('PRESENTATION_SCRIPT.md').write_text('\n'.join(script)+'\n')

ledger=['# Sentence-to-source ledger','',
 'Every spoken sentence is mapped below. Paper statements are paraphrases, not invented quotations. Source locations use one-based PDF pages; equation and table numbers identify the exact object. Original explanatory examples are explicitly marked. A citation to a paper does not convert a proposed combination into a demonstrated result.','',
 '## Source register','']
for sid,src in sources.items(): ledger += [f"### {sid} — {src['title']}",'',f"Source: {src['url']}",'',src['locator'],'']
ledger += ['## Sentence ledger','', '| Sentence | Exact spoken sentence | Evidence type | Source and precise location |','|---|---|---|---|']
rows=[]
for s in slides:
    for n in s['notes']:
        provenance=n['exactLocation']
        esc=lambda x:x.replace('|','\\|').replace('\n',' ')
        ledger.append('| '+' | '.join(esc(x) for x in [n['id'],n['text'],n['type'],provenance])+' |')
        rows.append([s['number'],n['id'],n['text'],n['type'],'; '.join(n['refs']),'; '.join(sources[r]['url'] for r in n['refs']),provenance])
ledger += ['','## Mathematical explanations and original examples','',
 '**Output-interface reasoning.** A teacher that returns scores can supervise a separate trainable retriever without exposing teacher weights. A vector-only retriever API does not itself expose a route to update that retriever’s weights. These are logical interface distinctions, not empirical results.','',
 '**Candidate-set schematic.** The relevant item drawn outside the initial candidate boundary is an original explanatory example. Reordering a fixed set cannot add an item outside it; a fresh retrieval can change membership. No observed embedding geometry or measured result is implied.','',
 '**Forward KL, fixed teacher.** With teacher probabilities t_i and student p_i, KL(t∥p)=Σ_i t_i log(t_i/p_i). The term Σ_i t_i log t_i is constant, so minimizing this KL is equivalent to maximizing Σ_i t_i log p_i. Neither operation changes the teacher.','',
 '**Simplified gradient.** Let student logits be uᵀz_i, without normalization or min-max scaling. The derivative with respect to each logit is p_i−t_i. By the chain rule, ∇_u L=Σ_i(p_i−t_i)z_i. The exact normalized TTT objective and min-max-normalized ReFIT implementation have additional dependencies; this displayed identity is a pedagogical special case.','',
 '**Toy KL plot.** Teacher [.6,.3,.1], initial student [.2,.3,.5], illustrative closer student [.5,.3,.2]. The third vector is a teaching example, not a simulated or guaranteed optimizer iterate.','',
 '**Toy coverage matrix.** d₁=(.9,.2,.1), d₂=(.85,.25,.1), d₃=(.2,.8,.1), d₄=(.1,.2,.9). Under sum of column maxima, F({d₁})=1.20; adding d₂ gives 1.25 (gain .05); d₃ gives 1.80 (gain .60); d₄ gives 2.00 (gain .80). These are illustrative scores, not experiment measurements.','',
 '## Hypothesis boundary','',
 'The new proposal is a matched-budget study of coverage-aware candidate selection for learning an external residual. Neither DISCo nor TTT-Embed proves that their combination improves retrieval. Complementary-retriever guidance already exists in GQR, and ReFIT discusses informative negatives. Do not claim novelty for those broader ideas.','',
 '## Experiment design','',
 'Use a prespecified query sample with the full corpus. Freeze student vectors, teacher, loss, optimizer, state scope and evaluation. Compare top-K candidates with coverage-aware and broader-pool/random controls at the same unique teacher-pair budget. Account for the selector and extra searches. Measure paired retrieval quality and judged-positive discovery beyond the initial candidate pool. Evaluate shared-state transfer on separate feedback and evaluation queries. This protocol is proposed, not executed by this presentation task.','',
 '## Numerical provenance and known inconsistencies','',
 '- TOUR chart: Table 3 EntityQuestions DPR_multi, not a reconstructed Figure 2 latency curve. Acc@K is answer-containing passage accuracy, distinct from macro Recall@K and nDCG.','- ReFIT chart: all BEIR values are from Table 6. Table 2 reports 69.0 for an aggregate whereas Table 6 reports 69.2; neither value has been edited to conceal the difference.','- ReFIT SCIDOCS reference: v2 main Table 2 reports 37.8/38.3/40.1; §4.1 gives 100 steps, LR .005, teacher T=2 and separate score min-max normalization. The previous project explainer’s appendix-only characterization is not used. Matching these nominal settings does not independently validate implementation fidelity.','- TTT chart: Table 1 average gains, with scope changing across the three shown budgets. The low-budget label .01 rounds 150/12,263. Do not subtract rounded cells to invent extra precision or join these bars into a full curve.','- Our SCIDOCS values and bootstrap interval are from linked completed-run reports. Artifact hashes are recorded; the raw predictions were not accessed/recomputed in this pass. “New document” means outside the initial 125; “none judged positive” does not mean all are truly irrelevant.','- Our FiQA task-wise TTT pilot is a reported project measurement from FIQA_RUN §4, not an independently recomputed result. Raw nDCG@10 .46722→.46313; separately reported delta −.00408, 95% CI [−.01072,+.00262]. The rounded displayed means subtract to −.00409; the source-reported delta is preserved. Five-fold cross-fitting evaluates unscored queries, but prior task exposure is disclosed. One task is not a full-paper replication; neither completed measurement tests complementary selection.','',
 '## Presentation scope','',
 'This is a first review edition prepared from the user’s 16 November brief. It is a presentation and research explanation, not a new model experiment. The bibliography is selective, focused on the requested method sequence; it is not an exhaustive novelty review.','']
OUT.joinpath('SOURCE_LEDGER.md').write_text('\n'.join(ledger)+'\n')
with OUT.joinpath('SOURCE_LEDGER.csv').open('w',newline='') as f:
    writer=csv.writer(f);writer.writerow(['Page','Sentence ID','Spoken sentence','Evidence type','Source IDs','Source URLs','Exact source locations']);writer.writerows(rows)

# The Markdown script and ledger exist before browser presentation code is generated.
OUT.joinpath('content.js').write_text('window.DECK = '+json.dumps(data,ensure_ascii=False,separators=(',',':'))+';\n')
print('Pages:',len(slides),'Sentences:',len(rows),'Words:',sum(s['wordCount'] for s in slides))
for s in slides: print(s['number'],s['wordCount'],s['secondsAt130Wpm'],s['title'].replace('\n',' '))
