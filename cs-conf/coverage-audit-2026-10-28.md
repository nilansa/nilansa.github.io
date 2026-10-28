# CS Conf — dated track coverage and prerequisite audit

**Audit date:** 28 Oct 2026 (Asia/Kolkata)  
**Stable task:** `cs-confs-deadline-tracker-repair-20261028-001`  
**Canonical public site:** https://nilansa.github.io/cs-conf/  
**Track-aware 90-day dashboard:** https://nilansa.github.io/cs-conf/opportunities.html  
**Structured dataset:** [opportunities.json](opportunities.json)  
**Original research schedule:** [data.json](data.json)

## Scope and counts

| Evidence pool | Count |
| --- | ---: |
| Existing dated deadline actions (unchanged) | 109 |
| Existing industry academic-affiliation records (unchanged) | 18 |
| Hugging Face conference-definition files previously imported | 68/68 |
| Distinct track-level records in new opportunity catalogue | 122 |
| Tracks with at least one dated official milestone | 88 |
| Tracks without a currently recorded actionable submission date | 37 |
| Initial coverage/model gaps specifically audited | 20 |
| Confirmed personal missed mandatory abstracts | **Unknown** — personal submission status cannot be inferred or published |

The above denominator is the actual repository's existing catalogue, plus a **selected official-source gap audit**. It is **not** every worldwide CS conference or workshop. A Hugging Face conference definition is a discovery record, not an officially verified 2027 track CFP.

## Present before this repair

- [x] NAACL 2027 Industry Track (31 Oct 2026): ✓ academic author eligibility in existing industryTracks
- [x] NAACL 2027 System Demonstrations (4 Dec 2026): dated action existed
- [x] ACL 2027 main ARR (4 Jan 2027): dated action existed
- [x] COLING 2027 Industry Track (30 Nov 2026): dated action and student eligibility existed
- [x] EACL 2027 Industry Track (11 Sep 2026, expired): eligibility catalogue existed
- [x] MLSys 2027 research and Industrial Track: research deadline and separate industrial-eligibility record existed
- [x] MICCAI venue and computational-biology/speech subject catalogues existed, but not 2027 track-specific MICCAI deadlines
- [x] FAccT 2027 and RECOMB 2027 mandatory abstracts and papers: separate dates existed but without a unified gate UI
- [x] Interspeech 2027 speech main, challenge proposals, special sessions and Show & Tell were dated actions
- [x] CVPR 2027 and RSS 2027 staged paper deadlines existed

## Missing or incomplete in the prior representation

- [ ] **P0** ACL 2027 Industry Track — TBA (official 2027 track CFP not verified)
- [ ] **P0** EMNLP 2027 Industry / Research / Demonstrations — TBA (2027 track-specific CFP not verified)
- [ ] **P0** NAACL 2027 Main ARR / Findings and commitment as one gated route — missing distinct route (industry/demo previously present)
- [ ] **P0** EACL 2027 contributed workshop papers — tentative joint schedule only
- [ ] **P0** COLING 2027 contributed workshop papers — tentative joint schedule only
- [ ] **P0** NAACL 2027 contributed workshop papers — tentative joint schedule only
- [ ] **P0** ACL 2027 contributed workshop papers — tentative joint schedule only
- [ ] **P0** MICCAI 2027 main research and workshops — official paper date TBA
- [ ] **P1** ICLR 2027 individual workshops (not organizer proposals) — not independently announced
- [ ] **P1** NeurIPS 2027 individual workshops — not independently announced
- [ ] **P1** RSS 2027 individual workshops — not independently announced
- [ ] **P1** NAACL 2027 Student Research Workshop — individual CFP/deadline unverified
- [ ] **P1** ACL 2027 systems demos — individual CFP/deadline unverified
- [ ] **P1** Interdisciplinary pretraining / mechanistic interpretability / AI safety / agents / memory / speech / medical / neuro / biology workshop CFPs — specific names and calls require verified discovery
- [ ] **P0** Unified stage, mandatory abstract gate, archive, personal decision UI — missing from prior flat dated-action table
- [ ] **P1** MIDL 2027 Short Papers — Published official 2027 track; paper date TBD; now retained as separate TBA record
- [ ] **P1** ICML 2027 and NeurIPS 2027 main CFP — 2027 track-specific deadlines not verified; TBA routes retained
- [ ] **P0** NAACL 2027 Student Research Workshop — Now verified official 16 Nov mentorship and 11 Jan student-paper dates
- [ ] **P0** EACL 2027 Student Research Workshop and System Demos — Separate official student mentorship and workshop-paper dates; demos already expired but retained
- [ ] **P0** EACL 2027 accepted named workshops — Official program lists 14 workshops; named TBA rows and individually verified LoResLM 7 Jan paper submission

The checkboxes above record the **pre-repair audit**, not whether the present release has now added a scaffold, nor whether a call is live. Where an official 2027 CFP remains unannounced, the new planner shows **TBA**, not an invented deadline.

## Verified priority corrections

| Route | Organizer-confirmed or qualified milestone | Prerequisite / status | Source |
| --- | --- | --- | --- |
| NAACL 2027 Industry Track | **31 Oct 2026** paper, 23:59 AoE | Academic-only authors **allowed**; genuine external users/deployment evidence still needed; does **not** use ARR | https://2027.naacl.org/calls/industry_track/ |
| NAACL 2027 System Demonstrations | **4 Dec 2026** demo paper, 23:59 AoE | Demo evaluation and live system requirements; not industry research paper | https://2027.naacl.org/calls/system_demonstration/ |
| NAACL 2027 Student Research Workshop | Optional mentorship **16 Nov 2026**; paper/proof of student status **11 Jan 2027** | Mentorship optional; first author must be student; not an ARR commitment route | https://2027.naacl.org/calls/srw/ |
| ACL 2027 Main / Findings | ARR paper latest **4 Jan 2027** | Findings is automatically considered from reviewed submissions, not a separate independent paper deadline | https://2027.aclweb.org/calls/main/ |
| EACL 2027 Student Research Workshop | Optional mentorship **6 Nov 2026**; paper **15 Dec 2026** | First author must be student; workshop paper direct submission possible without mentorship | https://2027.eacl.org/calls/srw/ |
| EACL 2027 System Demonstrations | **23 Sep 2026**, expired | Archived, not shown as an open submission; archival demo with video + live package | https://2027.eacl.org/calls/demos/ |
| EACL 2027 LoResLM Workshop | **7 Jan 2027** direct paper or ARR commitment, 23:59 AoE | **Individual official workshop** deadline overrides the tentative joint EACL 15 Dec calendar | https://loreslm.github.io/ |
| EACL 2027 accepted workshop catalogue | **14** named accepted workshops, several still without published individual CFP | Specific venue/track call required; do not silently apply the generic schedule to each | https://2027.eacl.org/program/workshops/ |
| Joint 2027 ACL workshop organizer proposals | **4 Sep 2026** (expired) | This was the **organizer proposal** cutoff for EACL/COLING/NAACL/ACL/EMNLP, **not** a submitted paper cutoff | https://www.aclweb.org/portal/content/joint-call-workshops-proposals-2027 |
| Joint 2027 workshop contributed papers | EACL **15 Dec 2026**; COLING **5 Jan 2027**; NAACL **5 Feb 2027**; ACL **25 Apr 2027** | **TENTATIVE** shared timeline; individual accepted workshop overrides | https://2027.eacl.org/calls/workshops/ |
| CVPR 2027 | Paper enrollment **10 Nov 2026**; full paper **16 Nov 2026** | Enrollment must be addressed before the paper deadline | https://cvpr.thecvf.com/Conferences/2027/Dates |
| MIDL 2027 | Mandatory abstract **30 Nov 2026**; full paper **4 Dec 2026**; short papers **TBA** | Separate main full-paper vs short-paper routes | https://2027.midl.io/important-dates |
| MICCAI 2027 | Main paper **TBA** | MICCAI Society gives 2027 venue/date but explicitly no paper deadline yet | https://miccai.org/upcoming-conferences/ |
| Interspeech 2027 | Challenge proposals **3 Nov 2026**; special-session proposals **10 Nov 2026**; main paper **9 Feb 2027**; Show & Tell **9 Mar 2027** | Four distinct contributions with different evidence and artifacts | https://interspeech2027.org/important_dates.html |
| FAccT 2027 | Mandatory abstract **27 Oct 2026 23:59 AoE = 28 Oct 2026 17:29 IST**; full paper **3 Nov 2026** | Without registered abstract full-paper route is blocked; when personal abstract status unknown, mark **VERIFY**, not presumed missed | https://facctconference.org/2027/cfp.html |
| RECOMB 2027 | Mandatory abstract **28 Oct 2026**; paper **4 Nov 2026** | Separate mandatory gate and paper date | https://recomb.org/recomb2027/keydates_and_deadlines.html |
| MLSys 2027 Industrial Track | **30 Oct 2026** paper with official source-hour discrepancy | Industry-first-author and industry-majority required. **Official Dates** says noon PDT = 19:00 UTC; **official CFP** says 20:00 UTC. Use earlier planning bound; verify with organizers. | https://mlsys.org/Conferences/2027/Dates |

## Unresolved official source conflict: MLSys 2027

The [organizer's 2027 Dates page](https://mlsys.org/Conferences/2027/Dates) gives **30 Oct 2026, 12:00 PDT** (19:00 UTC, **31 Oct 00:30 IST**). Its [2027 CFP](https://mlsys.org/Conferences/2027/CallForResearchPapers) instead gives **30 Oct 2026, 20:00 UTC** (**31 Oct 01:30 IST**). Both are live official pages. The dashboard flags the conflict and conservatively displays the earlier cutoff; this is **not** an independently resolved organizer correction.

## Private decision status and persistence

Public GitHub Pages cannot write to a private repository from an ordinary static page without authenticated integration. New status selectors therefore store decisions in **the current browser only**, are clearly labeled as such, can strike through local dismissed records, and can export a stable `CS_CONF_PRIVATE_DECISIONS v1` text for manual posting in the existing authenticated **private CS Conf issue #1**. Do not publish personal status, research discussions, credentials or private issue contents to the public website. Daily editorial automation should read the private issue before reconciling user decisions, **without copying personal choices into public JSON**. If a mandatory abstract is past and personal status is unknown, show VERIFY; do not assert that a person missed it. When explicitly marked missed, show BLOCKED.

## Daily editorial continuation

Reconcile these files by current blob SHA before edits. Check official CFPs for the 20 original audit gaps, prioritizing missing/tentative: ACL 2027 Industry and Demos, EMNLP 2027 Industry/Main/Demos, individual accepted EACL workshops, workshops on pretraining/representation learning, mechanistic interpretability, AI safety, agents/memory, speech, robotics, medical, neuro and computational biology. Keep TBA until a cited individual call exists. Preserve manual statuses and exclusions, and do not restart the retired hourly research scout.

## Discovery references (not deadline authorities)

- Hugging Face: https://github.com/huggingface/ai-deadlines
- CCFDDL: https://ccfddl.com/
- CS Deadlines: https://cs-deadlines.cin.ufpe.br/
- CSPicks: https://cspicks.roars.dev/csconfs.html?start=2026&end=2027
