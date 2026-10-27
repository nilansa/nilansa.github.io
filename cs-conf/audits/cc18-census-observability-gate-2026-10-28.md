# CC-18 — Source-data observability gate and negative-control plan

Checked: **28 October 2026** · Task `20261026-csconf-research` · **SOURCE AUDIT ONLY, NOT A NEW EXPERIMENT**

This record is a public-safe methods audit. It contains no unpublished measurements, private correspondence, or experimental results.

## Scientific question

Can a change in what an Internet census **scans** cause a change in its published anycast-positive prefix counts, even without a change in real-world anycast deployment?

The underlying public system, [LACeS](https://doi.org/10.1145/3730567.3764484), was **accepted at IMC 2025**. It already measures longitudinal anycast and validates its output with multiple techniques. A change in a published count alone is **not** evidence of a new Internet trend or a novel research result.

## Confirmed source revisions and confounders

The dataset authors' [README](https://github.com/ut-dacs/anycast-census/blob/main/README.md) and [CHANGELOG](https://github.com/ut-dacs/anycast-census/blob/main/CHANGELOG.md) report:

| Source date | Documented change | Implication |
|---|---|---|
| 3 Oct 2026 | Location representation changed from airport/IATA identifiers to city/GeoNames identifiers | Cross-date geolocation IDs cannot be joined without a consistent mapping |
| 10 Oct 2026 | DNS target lists gained records from a dependency graph, and ICMPv4 target priority changed | DNS comparisons and some IPv4 comparisons may not be stable negative controls |
| 17 Oct 2026 | IPv6 aliased prefixes moved to **/40 sampling granularity** | Published /48 positive counts may reflect changed observation coverage |
| Each week | Protocol-specific target lists are rebuilt | Matching a published prefix does not guarantee that the same IP target was scanned |

The authors explicitly note that an aliased /40 may contain both anycast and unicast /48 ranges. The [official attribution file](https://github.com/ut-dacs/anycast-census/blob/main/ATTRIBUTION.md) says the published dataset does **not** contain the full target hitlists. The README states weekly target lists may be shared **on request, subject to upstream permissions**. No such permission or complete target list has been obtained.

## What the public data can and cannot establish

The [author-provided Python helper](https://github.com/ut-dacs/anycast-census/blob/main/census_helper.py) loads daily Parquet snapshots and filters by the authors' existing confidence rules. The high-confidence predicate is `(max AB > 3) OR (max GCD > 1)`; a weaker comprehensive filter is also provided. The [manycast REST interface](https://manycast.net/) supports dates, prefix lookups, and historical exports. Those are useful public positive-detection observations.

**But the list of positively published /48 rows does not, by itself, establish all /48 prefixes or exact addresses examined on every day.** Intersecting rows from two published snapshots selects *survivors*. Without a full tested-target denominator, such an intersection cannot estimate deployment prevalence or prove whether changing probe selection produced a jump.

## Prospective minimal test (not executed)

1. Pin author-documented snapshots **16 and 18 October 2026** for IPv6 and IPv4. Use 11 and 24 October only for a predeclared sensitivity check. Public GitHub directory listings confirm the snapshots exist; **binary content and Parquet schema have not been independently processed**.
2. Before outcomes, obtain the licensed week-specific protocol target lists and aliased-prefix membership, or an equivalent author-approved **complete sample frame**. Match **/48 prefix + IP target + protocol**, not just positive-prefix IDs. Record missing/added targets and sampling changes. If target lists are not available, stop at descriptive source-coverage checks.
3. Compute the author's high-confidence AB/GCD decisions on a **fixed observed sample frame**, reporting aliased vs non-aliased IPv6 separately, ICMP and TCP separately, and an IPv4 comparator. Report actual scan costs, response coverage, positive counts, and missingness before interpreting any changes.
4. Treat the **3 October location-ID migration** as a separate intervention; never conflate it with the **17 October alias-sampling change**. Because the **10 October target-list change** also occurred, do not treat all IPv4/DNS measurements as unaffected controls.
5. Define one withheld later-day stability test only if suitable complete scan-frame metadata is obtained and the original analysis plan is frozen. No p-values or causal attribution from a short aggregate-only time series.

**Budget ceiling:** Four initial snapshots total about **5.1 MB** by GitHub size metadata. Allow up to **2 CPU core-hours**, no GPU, no paid API, no active Internet scanning. If any copying to a user's local/Codex system becomes necessary, first satisfy the private task's sync-first transfer and Codex-owned index requirements.

## Closest prior art and stopping decision

- **LACeS, IMC 2025:** longitudinal active anycast census, published methodology and validated dataset — [accepted work](https://doi.org/10.1145/3730567.3764484).
- **MAnycast², IMC 2020:** measurement using anycast, with known false positives — [authors' technical account](https://blog.apnic.net/2020/12/15/manycast2-using-anycast-to-measure-anycast/).
- **RIPE Atlas Measurements and Geolocation Providers: A Longitudinal Consistency Evaluation**, **19 Oct 2026 preprint**, not confirmed peer-reviewed — [arXiv:2610.27318](https://arxiv.org/abs/2610.27318). Its authors already report that changes in daily target mix can affect apparent longitudinal consistency.

**Current decision:** downgrade CC-18 to a **source-quality and reproducibility audit**. Do **not** pursue a standalone IMC/SIGCOMM paper on the documented count change unless authorized complete sample-frame data and a genuinely different new inference become available. **Stop/retire the publication branch** if the sample frame cannot be audited, if normalized comparisons remove the effect, or if any finding only restates these sources. Keep a research-quality warning internally when useful.

No standalone abstract, dataset-benchmark result, network probe, GPU experiment, or submission is claimed.
