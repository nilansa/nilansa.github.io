# Coeus — recording script

Estimated nine minutes with deliberate pacing and transitions.

## 01. Frozen models. Better retrieval?

Target: 25 seconds.

A search system can ask a stronger judge about a few documents. But can it use those judgments to find better documents elsewhere? We explore that question with frozen models and an editable query vector. On FiQA, coverage selection lost to the standard baseline.

Sources: FIQA

## 02. The shortlist has a boundary

Target: 40 seconds.

A dense retriever turns a query and documents into vectors, then uses similarity to find a shortlist. A reranker reads each query and candidate together and gives a relevance score. It can reorder that shortlist, but it cannot return a document that never entered it. Feedback offers another possibility: change the query representation and search the full collection again. The second search can reach a different neighborhood.

Sources: REFIT, TOUR

## 03. TOuR: ask, move, search

Target: 50 seconds.

TOuR turns that idea into a procedure. It retrieves candidates, asks a cross-encoder for scores, and uses those scores as pseudo-feedback to update the query vector. The query and document encoders stay fixed. The updated query then searches again. The paper uses different iteration settings for different tasks: its passage retrieval setting uses one step. This is test-time adaptation of a representation, not post-training the model weights.

Sources: TOUR, LEDGER

## 04. ReFIT: learn from the judge

Target: 50 seconds.

ReFIT also makes the reranker's preferences useful beyond the original shortlist. It scores the candidates once, then adjusts the query vector to make the retriever's candidate scores agree with the teacher. In the paper's experimental setting, it uses one hundred optimization steps on those scores before searching again. Those steps are not one hundred new teacher calls or searches. The point is to transfer information from a costly pairwise judge into a query that can be compared with every indexed document.

Sources: REFIT, LEDGER

## 05. TTT-Embed: where does the update live?

Target: 50 seconds.

TTT-Embed asks how to reuse this kind of feedback. It learns an external residual: a vector added to an embedding, while the embedding model and document index remain fixed. The same idea can operate at three scopes. A global residual is shared across tasks; a task residual is shared within a task; and a query-wise residual belongs to one query. Our experiment uses the last one. The paper studies budgets that vary with scope, so its settings should not be collapsed into a single budget.

Sources: TTT, LEDGER

## 06. Two distributions, one correction

Target: 45 seconds.

Here is the learning signal. For the same candidate documents, turn the teacher's scores into a probability distribution: numbers that sum to one. Do the same with similarities from the current query vector. Imagine the teacher places sixty percent of its weight on the first candidate, while the student places only twenty percent there. The loss measures their disagreement using forward KL divergence, from teacher to student. A second term penalizes a large residual vector, so agreement must be balanced against moving too far. The teacher stays fixed; only the external vector is optimized.

Sources: TTT, LEDGER

## 07. Fit, shrink, search

Target: 40 seconds.

In our query-wise run, we start the residual at zero and take three hundred Adam optimization steps using the ten teacher-scored candidates. Adam is an optimizer that repeatedly adjusts the residual to reduce the loss. After fitting, we use half of that residual: the TTT-Embed rule gives alpha one half for one rewarded query. Add it to the original query vector and normalize the result to unit length before the second search. The vectors have matching dimensions. This is our experimental setting; it is not a universal step budget from the papers.

Sources: TTT, FIQA

## 08. The Coeus pipeline

Target: 45 seconds.

Now to our experiment. We preselect two hundred FiQA queries without relevance labels and search all fifty-seven thousand, six hundred and thirty-eight documents using Qwen three embedding, zero point six billion. The first search gives a common pool of fifty. Each selection method chooses ten documents from that pool. Qwen three reranker, four billion, scores each query-document pair; a softmax over its Yes and No outputs gives the probability of Yes, which is our teacher score. We fit a separate residual for each query, search the full corpus again, and evaluate the returned ranking. Neither model's weights are fine-tuned.

Sources: FIQA

## 09. Coverage: choose what adds something

Target: 45 seconds.

Our selection hypothesis was that a set of documents covering different parts of the query might teach a more useful correction. We use frozen BERT base uncased to represent query and document tokens. For each query token, a document gets credit for its best-matching document token. Greedy selection repeatedly picks the document that adds the most coverage to the set so far. This is inspired by DISCo's set coverage, but operates only inside Qwen's fixed top fifty; it is not official DISCo retrieval.

Sources: DISCO, FIQA

## 10. FiQA: the standard baseline wins

Target: 50 seconds.

We measure ranking quality with normalized discounted cumulative gain at ten, or nDCG at ten. It rewards placing judged relevant documents near the top. Raw dense retrieval scores point four six one eight. Standard query-wise adaptation, using the dense top ten for feedback, reaches point five zero six zero. Greedy coverage reaches point four eight zero seven. Independent BERT MaxSim selection reaches point four eight eight one, and the rank-matched control averages point four seven six one. The queries were previously exposed, so this is an exploratory comparison, not blind confirmation or a reproduction of the paper's aggregate.

Sources: FIQA

## 11. The negative comparison is the result

Target: 45 seconds.

The main comparison is coverage minus standard adaptation. The difference is minus point zero two five three. Its paired ninety-five percent bootstrap interval runs from minus point zero four three eight to minus point zero zero seven zero. Both ends are below zero in this sample. The planned improvement was not demonstrated, and this configuration is parked. Ten teacher scores were matched, but BERT encoding and selection add work; equal teacher calls do not mean equal total cost. The interval measures uncertainty under this resampling procedure, not a guarantee about other collections.

Sources: FIQA

## 12. What the controls actually tell us

Target: 45 seconds.

The controls help locate the uncertainty. Directly sorting the dense ten by teacher score gives point four eight five six; sorting the coverage-selected ten gives point three eight five seven. Those are different sets as well as different rankings, and each direct list contains only ten documents. Against the rank-matched adaptation control, coverage is higher by point zero zero four six, but the interval crosses zero. That comparison does not establish a coverage benefit.

Sources: FIQA

## 13. Park, learn, test afresh

Target: 42 seconds.

A separate HotpotQA analysis illustrates why we separate description from confirmation. Across one thousand queries and two hundred twenty-five thousand, six hundred twenty-one documents, with ten teacher pairs per query, standard adaptation scores point seven three four six and coverage adaptation scores point seven four nine six. This is descriptive; the preregistered development interval includes zero, so that decision is also park. A useful next test would preregister a fresh holdout, compare against a rank-matched selector and the standard baseline, and count BERT work as well as teacher calls.

Sources: FIQA, H8
