# Coeus recording edition — sources

The prior 20-page source ledger remains at the staged source site. This recording edition uses the primary papers below and the two local experiment reports. Narration source links are also available through each slide's Sources panel.

- [TOuR](https://aclanthology.org/2023.findings-acl.354/) — method, frozen encoders, and passage retrieval update setting.
- [ReFIT](https://arxiv.org/abs/2305.11744) — test-time query refinement, cached teacher scores, and 100 optimization steps in its experimental setting.
- [TTT-Embed](https://arxiv.org/abs/2608.12569) — residual objective, global/task/query scopes, and variable feedback budgets.
- [DISCo](https://proceedings.iclr.cc/paper_files/paper/2026/file/6ded182245f8e4db3963d2027174133d-Paper-Conference.pdf) — collective coverage. The local fixed-pool BERT selector is inspired by this work, not the official retrieval system.
- **FiQA local report:** internal Coeus experiment record (not publicly distributed). Exposed queries; coverage minus standard −0.0253, paired 95% interval [−0.0438, −0.0070]; PARK. Direct teacher sorts return ten documents; querywise TTT performs full-corpus re-search.
- **HotpotQA H8 local report:** internal Coeus experiment record (not publicly distributed). Pooled 1,000-query values are descriptive; DEV400 difference +0.0103, paired 95% interval [−0.0041, +0.0251], preregistered PARK. The post-decision 600-query split is exploratory and spent.

The experiment values are transcribed from reports; they were not recomputed for this presentation. Existing paper figures and these local results are different evidence and should not be conflated.
