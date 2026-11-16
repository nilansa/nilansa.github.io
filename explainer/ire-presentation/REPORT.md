# Inference-Time Retrieval with Frozen Models and Reranker Feedback

**Team Coeus**

## 1. Question and context

Can a fixed budget of reranker feedback improve a frozen dense retriever, and does choosing complementary feedback documents help more than scoring the highest-ranked documents? Microsoft's research challenge asks how to select data, formulate losses, and use expensive reward models efficiently for retrieval post-training [1]. We study a related inference-time setting: only a query vector is adjusted; neither model's weights are trained. It is therefore not a post-training result for model parameters.

Dense retrieval encodes each query and document as a vector and ranks documents by vector similarity. A stronger reranker jointly examines each selected query-document pair, but a direct rerank can only reorder its selected set. Query adaptation uses those scores to change the query vector and search the corpus again, potentially retrieving documents outside that set.

## 2. Prior work and our comparison

TOUR [2] updates individual query representations using cross-encoder feedback, with fixed encoders; its passage setting uses one retrieval-feedback step. ReFIT [3] distills reranker scores into a query vector and re-searches, using 100 optimization steps in its reported setup. For example, its Table 2 reports SCIDOCS Recall@100 of 37.8% for Contriever retrieval, 38.3% for reranking, and 40.1% for ReFIT. These published results use their own models, data, and evaluation and are not directly comparable with ours.

TTT-Embed [4] learns an additive embedding correction and studies global (shared across tasks), task-wise, and query-wise scopes, with reward budgets that vary by setting. We use its query-wise form. Our question is whether choosing ten documents for collective token coverage beats choosing the dense top ten, when both supply ten teacher scores. Inspired by DISCo [5], we greedily select from the same fixed dense top 50 using frozen BERT token representations. This fixed-pool approximation is not official DISCo retrieval; no trainable ColBERT model or DISCo token ANN index was used.

## 3. Controlled procedure

For each query, Qwen3-Embedding-0.6B searches all 57,638 FiQA documents; its top 50 form the common candidate pool. The Qwen3-Reranker-4B teacher scores ten selected pairs as Yes/No P(yes). We compare dense top ten, greedy BERT coverage, independently ranked BERT MaxSim, and a rank-matched selection control. Each TTT arm optimizes a fresh query correction for 300 full-batch Adam steps, then searches the full corpus again. All models remain frozen; the final list is not teacher-reranked. Direct teacher sorting and untouched dense search provide further baselines. [6]

## 4. Objective and selection

Let x and z<sub>i</sub> be the unit query and candidate-document vectors with 1,024 real coordinates, and v a correction vector of the same dimension. Let r<sub>i</sub> in [0,1] be the teacher's P(yes) for candidate i; i ranges over the ten selected documents. For a nonzero vector a, define unit(a) = a / ||a||, where ||a|| is its Euclidean length. The equal-length vectors permit a dot product, which returns a real similarity. For each selected i, the two distributions are:

p<sub>T</sub>(i) = exp(r<sub>i</sub>/0.02) / sum<sub>j</sub> exp(r<sub>j</sub>/0.02);  p<sub>S</sub>(i;v) = exp(unit(x+v) dot z<sub>i</sub>/0.05) / sum<sub>j</sub> exp(unit(x+v) dot z<sub>j</sub>/0.05).

The sums run over the same ten candidates. Each softmax converts scores into nonnegative probabilities summing to one. We minimize over v: min<sub>v</sub> { KL(p<sub>T</sub> || p<sub>S</sub>) + 0.3 ||v||² }, where KL is sum<sub>i</sub> p<sub>T</sub>(i) log[p<sub>T</sub>(i)/p<sub>S</sub>(i;v)] and ||v||² is the sum of squared coordinates. Thus the loss matches the student's relative scores to the teacher while penalizing large corrections. Adam starts v at zero with learning rate 0.01; deployment uses unit(x + alpha v), alpha = 0.5. [4, 6]

For coverage, let h<sub>j</sub>(d) be the largest cosine similarity between query token j and any token in document d, using normalized frozen BERT contextual token vectors. For a selected document set S, F(S) = sum<sub>j</sub> max(0, max<sub>d in S</sub> h<sub>j</sub>(d)), with F(empty set) = 0. The sum runs over query tokens; max takes the best match among selected documents. Greedy selection adds the candidate with largest increase in F until ten are chosen. Independent MaxSim instead ranks each candidate by sum<sub>j</sub> max(0,h<sub>j</sub>(d)). BERT chooses document IDs; Qwen vectors remain the optimization and retrieval space. [5, 6]

<!-- PAGE BREAK -->

## 5. Results and interpretation

**FiQA**, 200 qrel-blind preselected, previously exposed queries; all corpus documents searched. Values are means over queries. nDCG@10 measures graded ranking quality in the first ten positions; Recall@k is the fraction of judged relevant documents found in the first k; MRR@10 averages reciprocal rank of the first relevant result. Higher is better. [6]

| Arm | nDCG@10 | Recall@10 | Recall@100 | MRR@10 |
|---|---:|---:|---:|---:|
| Untouched dense | .4618 | .5403 | .7826 | .5498 |
| Standard TTT: dense10 | .5060 | .5831 | .8038 | .5977 |
| Greedy coverage TTT | .4807 | .5675 | .7991 | .5551 |
| Independent BERT MaxSim TTT | .4881 | .5685 | .8017 | .5705 |
| Rank-matched TTT, mean of 3 | .4761 | .5701 | .8020 | .5442 |
| Uniform random TTT | .4617 | .5526 | .8058 | .5405 |
| Direct teacher sort, dense10 | .4856 | .5403 | .5403 | .5898 |
| Direct teacher sort, coverage10 | .3857 | .3977 | .3977 | .5228 |

Direct sorts return only ten documents, so their Recall@100 equals Recall@10; they are not 100-result retrieval comparisons. Coverage TTT minus standard TTT was −.0253 nDCG@10, paired 95% bootstrap CI [−.0438, −.0070]; versus rank-matched it was +.0046 [−.0134, +.0224]. Both prespecified gains were required; the decision is **PARK**. Equal teacher-pair counts do not equal total compute: coverage and MaxSim additionally encode the query and top-50 documents with BERT. FiQA is exploratory, not blind confirmation. [6]

**HotpotQA-HardNegatives H8:** pooled 1,000-query scores on 225,621 documents with ten teacher pairs per query for standard and coverage TTT were .7346 and .7496 nDCG@10, descriptively. The preregistered DEV400 difference was +.0103 [−.0041, +.0251], failing the required positive lower bound; H8 remains **PARK**. The subsequent 600-query analysis was post-decision and cannot serve as confirmation. A rank-matched control and matched extra-compute comparison were missing. [7]

**Limitations and next steps.** These results do not establish general superiority or novelty. Re-entry requires fresh held-out data, preregistered criteria, a rank-matched control, and accounting for encoder and search cost.

## References

[1] Microsoft Research, [Efficient and accurate post-training of retrieval models](https://www.microsoft.com/en-us/research/academic-program/microsoft-research-fellowship/research-challenges/). [2] Sung et al., [TOUR](https://aclanthology.org/2023.findings-acl.354/), Findings ACL 2023. [3] Reddy et al., [ReFIT](https://arxiv.org/abs/2305.11744), v2, Table 2. [4] Chen and Wu, [TTT-Embed](https://arxiv.org/abs/2608.12569), v1. [5] Nair et al., [DISCo](https://proceedings.iclr.cc/paper_files/paper/2026/file/6ded182245f8e4db3963d2027174133d-Paper-Conference.pdf), ICLR 2026. [6] Coeus, FiQA200 exploratory results, local `fiqa200-complementarity-v1/RESULTS.md`. [7] Coeus, H8 HotpotQA results, local `H8_RESULTS_HOTPOTQA_HN.md`.
