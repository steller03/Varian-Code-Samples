# Dispatch 3b — Batch probe (walk the queue → probes + back-links)

Generate ~1-page probes sequentially from `probe_queue.md`. Same per-unit method as Dispatch 3,
looped — this dispatch adds the queue walk, resumability, and the registry / queue back-links.

## Before you start
Read `/docs/taxonomy.md`, `/docs/dispatches/3-depth.md` (the per-probe procedure — reuse it, don't
restate), and `/docs/probe_queue.md` (the queue).

## Scope (default + override)
- **Default:** the next `queued` units in `probe_queue.md`, top to bottom.
- **Cap:** probes are deep — do **~5 per run**, then stop cleanly (see Resumability). Re-running
  continues down the queue, so the top 20 lands over ~4 runs.
- **Override:** if an ID list is given here, probe exactly those instead.
  PROBE_IDS (optional): «e.g. DW16-16, ESAP-01, ESAP-05»

## Per unit
1. Resolve the ID to its registry shard (shard = the ID's slug — e.g. DW16-16 → `registry/DW16.md`)
   and read the **Path** cell to locate the solution in the repo.
2. Read the actual code at that path and apply Dispatch 3's procedure to write
   `/docs/probes/<ID>-<short-slug>.md` (Header, Problem, Approach, ESAPI surfaces, Reusability,
   Idea sparks). ~1 page — technique and reuse, not a line-by-line transcript.

## After each probe (back-links)
- In the unit's **registry shard**, set its `Probe` cell to `→ probes/<file>`.
- In **`probe_queue.md`**, set that unit's `Status` to `done` and put the filename in its `Probe`
  column.
- **Do not edit `SYNTHESIS.md`.** It is regenerated from the registry by Dispatch 2; probe links
  live in the registry (the source of truth) and the queue (the live index). Re-run Dispatch 2 when
  you want the summary refreshed.

## Resumability
Skip any unit whose probe file already exists or whose `Status` is `done`. Write each probe — and
its two back-links — before starting the next. If low on room, finish the current probe, update its
back-links, then stop. Re-run to continue.

## Done when
The targeted batch (the cap, or the PROBE_IDS list) is probed, with registry + queue back-links
written for each. End with a report: IDs probed this run, files written, and the count still
`queued`.
