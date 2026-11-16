# COEOUS — recording script

Estimated nine minutes with deliberate pacing and transitions.

## 01. Can retrieval improve with only black-box reranker feedback?

Target: 25 seconds.

We investigate whether a frozen dense retriever can improve at inference time using only black-box reranker scores. The retriever produces query and document vectors; the reranker evaluates a few query–document pairs. We do not have access to either model’s trainable parameters. The precise goal is to adapt the accessible query representation so that a second search can find better documents in the full corpus. This is different from Microsoft Research’s broader post-training research question. Our project COEOUS evaluates both established test-time adaptation and a complementary-feedback selection hypothesis, including negative results.

Sources: FIQA

## 02. Why reranking cannot recover missing documents

Target: 40 seconds.

A dense retriever turns a query and documents into vectors, then uses similarity to find a shortlist. A reranker reads each query and candidate together and gives a relevance score. It can reorder that shortlist, but it cannot return a document that never entered it. Feedback offers another possibility: change the query representation and search the full collection again. The second search can reach a different neighborhood.

Sources: REFIT, TOUR

## 03. TOuR: optimize the query using reranker feedback

Target: 50 seconds.

TOuR turns that idea into a procedure. It retrieves candidates, asks a cross-encoder for scores, and uses those scores as pseudo-feedback to update the query vector. The query and document encoders stay fixed. The updated query then searches again. The paper uses different iteration settings for different tasks: its passage retrieval setting uses one step. This is test-time adaptation of a representation, not post-training the model weights.

Sources: TOUR, LEDGER

## 04. ReFIT: distill reranker scores into the query

Target: 50 seconds.

ReFIT also makes the reranker's preferences useful beyond the original shortlist. It scores the candidates once, then adjusts the query vector to make the retriever's candidate scores agree with the teacher. In the paper's experimental setting, it uses one hundred optimization steps on those scores before searching again. Those steps are not one hundred new teacher calls or searches. The point is to transfer information from a costly pairwise judge into a query that can be compared with every indexed document.

Sources: REFIT, LEDGER

## 05. TTT-Embed: three scopes for residual adaptation

Target: 50 seconds.

TTT-Embed asks how to reuse this kind of feedback. It learns an external residual: a vector added to an embedding, while the embedding model and document index remain fixed. The same idea can operate at three scopes. A global residual is shared across tasks; a task residual is shared within a task; and a query-wise residual belongs to one query. Our experiment uses the last one. The paper studies budgets that vary with scope, so its settings should not be collapsed into a single budget.

Sources: TTT, LEDGER

## 06. TTT-Embed: the teacher–student KL objective

Target: 45 seconds.

Here is the learning signal. For the same candidate documents, turn the teacher's scores into a probability distribution: numbers that sum to one. Do the same with similarities from the current query vector. Imagine the teacher places sixty percent of its weight on the first candidate, while the student places only twenty percent there. The loss measures their disagreement using forward KL divergence, from teacher to student. A second term penalizes a large residual vector, so agreement must be balanced against moving too far. The teacher stays fixed; only the external vector is optimized.

Sources: TTT, LEDGER

## 07. How the query residual is fitted with Adam

Target: 40 seconds.

For each query, we initialize a 1,024-dimensional correction vector v at zero. Ten Qwen3-reranked candidates provide a fixed teacher probability target. We minimize KL divergence from teacher to student, plus a squared-norm regularizer of strength 0.3. At each of 300 Adam steps we compute a gradient only with respect to v. Adam maintains moving first and second gradient moments and uses bias-corrected moment estimates to update the vector with learning rate 0.01. We finally use half the fitted vector, normalize x plus 0.5v, and perform the full 57,638-document similarity search. No encoder, reranker, or document parameters change.

Sources: TTT, FIQA

## 08. Our FiQA-200 experiment: complete pipeline

Target: 45 seconds.

Now to our experiment. We preselect two hundred FiQA queries without relevance labels and search all fifty-seven thousand, six hundred and thirty-eight documents using Qwen three embedding, zero point six billion. The first search gives a common pool of fifty. Each selection method chooses ten documents from that pool. Qwen three reranker, four billion, scores each query-document pair; a softmax over its Yes and No outputs gives the probability of Yes, which is our teacher score. We fit a separate residual for each query, search the full corpus again, and evaluate the returned ranking. Neither model's weights are fine-tuned.

Sources: FIQA

## 09. DISCo-inspired selection: collective query-token coverage

Target: 45 seconds.

Our selection is inspired by the DISCo paper’s idea of collective contextual-token coverage. We use frozen BERT-base-uncased query and document token embeddings. For every query token, a candidate contributes its maximum contextual-token cosine similarity. Greedy selection chooses a document for the extra coverage it adds to the set already selected. ColBERT-style independent MaxSim ranks each document by its own score instead; MMR balances relevance and inter-document similarity. Our implementation applies coverage only inside the Qwen dense top-fifty pool, rather than implementing DISCo’s corpus-wide specialized indexing. Coverage alone is not a learning objective; the relevance scores must also produce informative gradients.

Sources: DISCO, FIQA

## 10. FiQA-200 results: dense feedback is strongest

Target: 50 seconds.

We measure ranking quality with normalized discounted cumulative gain at ten, or nDCG at ten. It rewards placing judged relevant documents near the top. Raw dense retrieval scores point four six one eight. Standard query-wise adaptation, using the dense top ten for feedback, reaches point five zero six zero. Greedy coverage reaches point four eight zero seven. Independent BERT MaxSim selection reaches point four eight eight one, and the rank-matched control averages point four seven six one. The queries were previously exposed, so this is an exploratory comparison, not blind confirmation or a reproduction of the paper's aggregate.

Sources: FIQA

## 11. FiQA-200: complementary coverage did not help TTT

Target: 45 seconds.

The main comparison is coverage minus standard adaptation. The difference is minus point zero two five three. Its paired ninety-five percent bootstrap interval runs from minus point zero four three eight to minus point zero zero seven zero. Both ends are below zero in this sample. The planned improvement was not demonstrated, and this configuration is parked. Ten teacher scores were matched, but BERT encoding and selection add work; equal teacher calls do not mean equal total cost. The interval measures uncertainty under this resampling procedure, not a guarantee about other collections.

Sources: FIQA

## 12. Controls: coverage alone does not explain improvement

Target: 45 seconds.

The controls help locate the uncertainty. Directly sorting the dense ten by teacher score gives point four eight five six; sorting the coverage-selected ten gives point three eight five seven. Those are different sets as well as different rankings, and each direct list contains only ten documents. Against the rank-matched adaptation control, coverage is higher by point zero zero four six, but the interval crosses zero. That comparison does not establish a coverage benefit.

Sources: FIQA

## 13. Conclusion: feedback quality matters, not coverage alone

Target: 42 seconds.

A separate HotpotQA analysis illustrates why we separate description from confirmation. Across one thousand queries and two hundred twenty-five thousand, six hundred twenty-one documents, with ten teacher pairs per query, standard adaptation scores point seven three four six and coverage adaptation scores point seven four nine six. This is descriptive; the preregistered development interval includes zero, so that decision is also park. A useful next test would preregister a fresh holdout, compare against a rank-matched selector and the standard baseline, and count BERT work as well as teacher calls.

Sources: FIQA, H8
