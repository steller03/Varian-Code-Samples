# Dispatch 4 — Enrich the TOC (links + event metadata)

Turn `probe_queue.md` into a linked catalogue TOC and add an event reference. The links are
deterministic (a script); the metadata needs reading the repo. Nothing existing is removed.

## Part 1 — Links (run the script)
```
python docs/enrich_toc.py docs
```
It rewrites `docs/probe_queue.md`, linking each Solution to its source folder (from the registry
shards' `Path`) and each Probe filename to `probes/<file>`, and prints a validation summary.
**Require 0 warnings** — every source path and probe file must resolve (`UNMAPPED` / `NOPATH` /
`NOPROBE` all zero). A `probe_queue.md.bak` is written; diff it to eyeball the change. Re-running
is safe (it won't double-link).

## Part 2 — Events reference table (research, then append)
Meeting / date / presenter is **event-level (16 events), not per-unit** — capture it once here
rather than repeating it on 88 rows. Add this table directly under the intro of `probe_queue.md`:

```
## Events

| Slug | Event / meeting | Date | Presenter(s) | Notes |
|---|---|---|---|---|
```

Fill one row per slug (DW16, DW14, DW18, W2001, W1504, W1804, RS15, W1810, W2008, W2103, W1712,
W1811, DS23, W2003, ESAP, ESPL):
- **Date** — from the folder name where dated ("16 Jan 2020", "22 Jul 2023"); year only for the
  workshops (DW14/16/18). ESAP/ESPL are an undated standing collection — mark `n/a`.
- **Event / meeting** — the folder's event title, tidied.
- **Presenter(s)** — ONLY if documented in the repo (a README, a slide/track-details PDF, or an
  author tag in code). **Do not guess or web-search names** — an attributed presenter must come
  from repo evidence. If none is found, put `—`.
- **Notes** — series/track/venue if evident, else blank.

(The script ignores this table — its rows are keyed by slug, not unit ID — so Part 1 and Part 2
can run in either order.)

## Part 3 — Close the registry loop
While the links are fresh, make sure each registry shard's `Probe` cell also points to its probe
(`→ probes/<file>`), so the source of truth carries the link too, not just the queue.

## Done when
`probe_queue.md` has linked Solution + Probe cells (script: 0 warnings) and an Events table
covering all 16 slugs, every presenter either repo-sourced or `—` (none invented), and each
registry shard's `Probe` cells filled.
