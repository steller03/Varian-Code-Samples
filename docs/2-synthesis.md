# Dispatch 2 — Synthesis (all shards → SYNTHESIS.md)

Build the cohesive master summary from the triage shards. This is a reorganization of the
registry — work from the shards, do not re-read source code.

## Before you start
Read `/docs/taxonomy.md` and every file in `/docs/registry/`. Each unit's registry row now carries
a `Probe` cell naming its probe file — you'll render those as links (step 4), so this run depends on
the registry `Probe` cells being filled (Dispatch 4).

## Produce `/docs/SYNTHESIS.md`
1. **Intro** — one short section: what the repo is, what this catalog covers, and how to use it.
   Point to the two companion views: `probe_queue.md` (the tier-ranked TOC + Events reference) and
   `probes/` (the deep dives); note `registry/` is the per-event source of truth.
2. **Start here** — a curated entry point so a first-time reader isn't facing 88 equal-weight rows.
   List these, each linked to its probe with a one-line "why," and nothing else:
   - the four end-to-end planning pipelines — **DW18-04, RS15-01, DS23-01, DW16-22**
   - the two dev-tooling standouts — **ESAP-07, ESAP-10**
3. **At a glance** — compact tables: total units, counts by category, by reuse verdict, version spread.
4. **By problem category** — the heart. For each category (taxonomy §1 order), one terse entry per
   unit: `ID · [Solution](probes/<file>) · ≤15-word problem · score · path`. Link the **Solution
   name to its probe**, using the filename from that unit's registry `Probe` cell (the path is
   `probes/<file>` — SYNTHESIS sits in `/docs/`). If a unit has no probe, leave the name as plain
   text. This turns the by-problem index into a clickable analysis index.
5. **Duplicate & evolution clusters** — group units solving the same problem across events; name the
   best/latest exemplar (linked to its probe); list the rest as "see also."
6. **Most interesting (top ~20)** — ranked by score then judgment, each Solution linked to its probe.
7. **Coverage ledger** — units cataloged, probes written, version spread; flag any gaps.

Keep every entry terse — a map, not a manual. Cross-reference IDs throughout. Re-runnable:
regenerate from the current shards (and their `Probe` cells) each time, so the links stay in sync.
