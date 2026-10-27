# CC-18 — Anycast census measurement-regime sensitivity

*Public-safe protocol, 27 October 2026.* Status: source-feasible **proposal**, not a published new scientific result. Private exploratory measurements remain in the private CS Conf decision inbox and are **not** reproduced here.

## Why this question exists

The authors of [LACeS: an Open, Fast, Responsible and Efficient Longitudinal Anycast Census System (accepted IMC 2025)](https://doi.org/10.1145/3730567.3764484) publish [daily public IPv4 and IPv6 anycast results and count summaries](https://github.com/ut-dacs/Anycast-Census). The **primary dataset README** itself documents two changes:

1. Before **3 October 2026**, geolocation `locations[].id` used airport codes. The current schema uses city identifiers. Location identities must not be compared across the change without canonical mapping.
2. Starting **17 October 2026**, detection began scanning **IPv6 aliased prefixes at /40 granularity**. Before treating longitudinal differences as changes in physical deployments, an analyst must account for the changed observation units and sample coverage.

**This documentation is prior art.** A graph of daily counts around either date cannot independently establish a new scientific finding or true deployment growth.

## One falsifiable scientific question

At fixed **/48 prefix identities, protocol and comparable active target set**, is an observed change in IPv6 anycast detections substantially smaller than the corresponding change in the *unmatched all-observed count*?

**Null/control:** differences remain after fixing the cohort and compatible /48 units, or equivalent changes appear in unaffected matched IPv4 protocol controls. **Alternative:** the apparent aggregate change is concentrated in newly covered aliased IPv6 prefix ranges or observation units.

Do not conflate a change in the source's **count of detected candidate prefixes** with a measured increase in **true physical anycast deployments**.

## A reproducible minimal test — not yet run

**Data sources:** the authors' [README/schema and public daily snapshots](https://github.com/ut-dacs/Anycast-Census), specifically version-pinned `YYYY/MM/DD/IPv4.parquet`, `IPv6.parquet`, and `stats`. Repository directory metadata confirms Oct 2/4/16/18 2026 archive file names and sizes; the actual Parquet records were **not decoded in this environment**.

**Frozen design before any matched-prefix data inspection:**

- Compare seven pre-change days (**10–16 October**) with seven post-change days (**18–24 October**), leaving **17 October** out as the announced transition date. This window was chosen *after* an initial exploratory aggregate count inspection; it is not an untouched preregistration and should not be presented as one.
- For matching `/48` prefixes, keep a stable observation population (the **intersection** of eligible prefixes), annotate aliased `/40` blocks, and evaluate protocol-specific `AB_ICMPv6`, `AB_TCPv6`, `GCD_ICMPv6`, `GCD_TCPv6` classifications. Check the exact daily archive schema before coding.
- Compare the **same original /48 denominator** across pre and post. If new scans operate at /40, explain precisely how /40 observations are translated back to /48. Do not count a /40 and all of its children as independent new /48 results.
- Report added and removed observed-prefix counts, same-cohort transitions, unknown/missing targets, and raw-versus-comparable denominators. Separate a pipeline change from underlying route/host variation as far as data allow.
- Recompute matched IPv4 counterparts as **negative controls**; retain identical time windows, classification thresholds, and inclusion rules. Keep the unrelated **3 October airport/city geolocation-ID change** in a *different* protocol and analysis.
- Report sensitivity to high-confidence and comprehensive filters defined by the upstream README, and distinguish AB versus GCD rules. Include immutable source commit IDs, per-file digests and exact CPU/decompression costs.

**Hard boundaries:** Do not initiate traceroute, ping, DNS or address sweeps. Reuse only historical public data with license and ethical-use requirements respected. Initial budget **≤1 CPU core-hour, no GPU, no paid API**. The current authorized reading route could inspect the public text `stats` files and GitHub Parquet *metadata* but did not provide a safely decoded binary archive; there is no matched-prefix experiment yet.

## Closest work and conflicts

- **LACeS (IMC 2025)** is the direct accepted baseline and already declares both relevant dataset changes. Any result that only repeats those documentation facts is **not novel**.
- [MAnycastR](https://github.com/rhendriks/MAnycastR) and [MiGreedy](https://github.com/rhendriks/MiGreedy) are the public measurement/geolocation tools used in the ecosystem, not a new CS Conf algorithm.
- [Replication: Characterizing MPLS Tunnels over Internet Paths](https://conferences.sigcomm.org/imc/2025/program/) (accepted IMC 2025) provides a real replication precedent. Its released [PyTNT source](https://github.com/jehuddleston/PyTNT) uses Scamper active probes; no zero-cost independent replay is reported here.
- [IMC 2027 Replicability Track](https://conferences.sigcomm.org/imc/2027/cfp/) requires an **exact prior network measurement claim**, legal independent observations, and a new lesson in a one-page Expression of Interest **13 January 2027**. This general method-change question is **not automatically an eligible EoI**.

## Stop or pivot

**Stop the standalone CC-18 paper route** if fixed-cohort adjustment accounts for the already documented observation-unit change without producing a distinct new measurement insight; if source schema/coverage cannot be reconciled; if sampling differences cannot be separated from network changes; or if any claimed effect rests only on unpaired public aggregates.

Retain the warning as a reproducibility lesson in the research checklist even if CC-18 is retired. Do not draft an empirical abstract until a prospectively controlled independent test and prior-art comparison exist. No paper submission is authorized.
