# Dispatch 3 — Depth (selected IDs → probe files)

Deep-dive the solutions flagged in `SYNTHESIS.md` (or named below). Go deeper than triage, but
stay on technique and reusability — still not a line-by-line transcript.

## Before you start
Read `/docs/taxonomy.md`.

## Target (fill in)
- **PROBE_IDS:** «IDs to probe, e.g. `DW16-07, W2008-01`»

## For each ID, write `/docs/probes/<ID>-<short-slug>.md`
- **Header** — ID, solution name, source event, ESAPI version, reuse verdict.
- **Problem** (2–3 sentences) — the real-world need it addresses.
- **Approach** (1–2 paragraphs) — how it solves the problem and the key moves, at the level of
  "pulls the structure set, computes DVH via `GetDVHCumulativeData`, thresholds, then exports."
  Enough to judge the technique and reuse it — not a code dump.
- **ESAPI surfaces** — bulleted key classes / namespaces / methods it relies on. (This is the
  one place an API-symbol list belongs.)
- **Reusability** — what's liftable vs needs porting; version caveats and any deprecated calls
  with their modern equivalent if obvious.
- **Idea sparks** — 1–3 adjacent problems in our own practice this could seed.

Then update the registry: in the source shard, set this ID's `Probe` cell to `→ probes/<file>`.

Keep each probe to ~1 page. Depth on the idea and the technique, not exhaustive code.
