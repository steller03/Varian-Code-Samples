# Dispatch 1b — Batch triage (all remaining folders → all shards)

Produce a registry shard for **every** remaining event folder in one session. Same method as
Dispatch 1, looped — this dispatch adds the work list, resumability, and a hard completion gate
so it does **not** stop after one folder.

## Before you start
Read `/docs/taxonomy.md` (the contract) and `/docs/dispatches/1-triage.md` (the per-folder
procedure). For each folder below, apply Dispatch 1's per-unit procedure exactly. Don't restate
it — reuse it. This dispatch only wraps it in a loop.

## Unit definition (per folder)
- Each `.sln` is one unit.
- A standalone `.cs` script with **no** same-named `.sln` in its folder is its own unit.
- A `.cs` that is only the single-file *twin* of a `.sln` already catalogued in the same folder
  is the same problem → **one** entry, do not double-count.

The `loose .cs` column flags where standalone scripts live. When you reach a flagged folder,
reconcile each loose script (twin → skip, unique → add as its own unit).

## Work list — process ALL 15 (DW16 is already done)
Ordered small→large so most of the tracker turns green fast and an interruption costs at most
one big folder. Counts are from the tree; treat `.sln` as the minimum unit count.

| Folder (literal path, quote in shell) | Slug | .sln | loose .cs | Note |
|---|---|---:|---:|---|
| `webinars & workshops/20 Aug 2020 Webinar - Constraint Export` | W2008 | 1 | 0 | |
| `webinars & workshops/31 Mar 2021 Webinar - Beam Data Visualization` | W2103 | 1 | 0 | |
| `webinars & workshops/17 Dec 2017 Webinar` | W1712 | 1 | 4 | reconcile loose scripts |
| `webinars & workshops/14 Nov 2018 Webinar (DVH)` | W1811 | 1 | 0 | |
| `webinars & workshops/22 Jul 2023 Developer Symposium` | DS23 | 1 | 0 | |
| `webinars & workshops/23 Mar 2020 Webinar_ARIAAccess` | W2003 | 1 | 0 | |
| `webinars & workshops/Research Symposium 2015` | RS15 | 2 | 1 | |
| `webinars & workshops/16 Oct 2018 Webinar` | W1810 | 2 | 0 | |
| `webinars & workshops/06 Apr 2018 Webinar` | W1804 | 3 | 0 | |
| `webinars & workshops/16 Jan 2020 Webinar` | W2001 | 4 | 1 | |
| `webinars & workshops/21 Apr 2015 Webinar` | W1504 | 4 | 4 | reconcile loose scripts |
| `Eclipse Scripting API/plugins` | ESPL | 0 | 4 | **script-only**: 4 units, no `.sln` |
| `webinars & workshops/Developer Workshop 2018` | DW18 | 9 | 2 | |
| `webinars & workshops/Developer Workshop 2014` | DW14 | 9 | 13 | reconcile loose scripts |
| `Eclipse Scripting API/projects` | ESAP | 10 | 9 | reconcile loose scripts |

## Loop behavior (this is the part that fixes "it stopped after one")
1. Go through the work list **top to bottom and do not stop until every folder is done.**
2. If `registry/<slug>.md` already exists, **skip** it. (Idempotent — so DW16 is untouched and a
   re-run resumes where you left off.)
3. Write each shard to `registry/<slug>.md` the moment that folder is finished, **before** starting
   the next one. Partial progress must persist on disk.
4. If you are running low on room, finish the current folder's shard, then stop cleanly. Re-running
   this dispatch picks up the rest.

## Verify each folder (observed green, not asserted)
Immediately after writing each shard, run:

```
python docs/verify_shard.py . "<folder>" docs/registry/<SLUG>.md
```

Require `MISSED 0` and `PHANTOM 0`. Read every `INFO` loose-`.cs` line and confirm it is either a
twin of a catalogued unit (skip) or a unique script you have added. For **ESPL** (no `.sln`), the
verifier can't diff against solutions, so confirm by hand that the shard has one row per `INFO`
script (4). Fix any discrepancy before moving to the next folder.

## Done when
A shard exists for all 15 slugs and each passes the verifier. End with a completion report — a
table of `slug → row count → verifier result (OK / REVIEW)`. Optionally flip the matching
`Triaged` boxes to ☑ in `README.md`.
