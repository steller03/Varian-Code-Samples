# Dispatch 2 — Synthesis (all shards → SYNTHESIS.md)

Build the cohesive master summary from the triage shards. This is a **reorganization of the
registry** — work from the shards, do not re-read source code.

## Before you start
Read `/docs/taxonomy.md` and every file in `/docs/registry/`.

## Produce `/docs/SYNTHESIS.md`
1. **Intro** — one short section: what the repo is, what this catalog covers, and how to use
   it (shards for the full index, `probes/` for deep dives).
2. **At a glance** — compact tables: total units cataloged, counts by category, by reuse
   verdict, and the ESAPI version spread.
3. **By problem category** — the heart. For each category (taxonomy §1 order), list its
   solutions as terse entries: `ID · Solution · ≤15-word problem · score · path`. This makes
   the entire repo browsable by the problem solved.
4. **Duplicate & evolution clusters** — group solutions that solve the same problem across
   events (DVH lookup, plan sum, dose-at-point, etc.). Name the best / latest exemplar to
   use; list the rest as "see also."
5. **Most interesting (top ~20)** — ranked by score then judgment. One line each on why it's
   worth attention; mark `probe?` for the strongest deep-dive candidates.
6. **Coverage ledger** — total cataloged vs the ~80 solutions / 16 event folders; flag gaps.

Keep every entry terse — this is a map, not a manual. Cross-reference IDs throughout.
Re-runnable: regenerate from whatever shards currently exist, so partial triage still yields
a partial summary.
