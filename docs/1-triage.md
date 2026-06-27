# Dispatch 1 — Triage (one event folder → one registry shard)

You are cataloging part of the VarianAPIs/Varian-Code-Samples repo. Goal: record **what
problem each solution solves**, not how the code works. Fast, wide, problem-focused.

## Before you start
Read `/docs/taxonomy.md` in full and treat it as binding — categories, field vocabularies,
the scoring rubric, the ID scheme, and the registry column schema all come from there.

## Target (fill these in)
- **TARGET_FOLDER:** «one event folder, e.g. `webinars & workshops/Developer Workshop 2016`»
- **SLUG:** «its slug from the tracker, e.g. `DW16`»

The unit to catalog is each Visual Studio solution (`.sln`) under TARGET_FOLDER. If a folder
has plugin scripts without a `.sln` (e.g. ESPL), treat each plugin file as its own unit.

## For each unit
1. Identify the solution and its repo-relative folder path.
2. Determine the problem it solves. Read just enough — README, top-of-file comments, the
   `Execute` / `Main` entry point, class and method names — to state the real-world purpose.
   **Do not** walk the code line by line or describe method internals.
3. Fill every schema column. One primary category. Score per the rubric. Verdict is a
   first-pass estimate. Keep `Problem` to ≤ 15 words, outcome-focused —
   "Bulk-export plan DVH constraints to CSV," never "iterates Beams and reads ControlPoints."

## Output
Write a single file: `/docs/registry/<SLUG>.md`, containing —
- `# <Event name> (<SLUG>)`
- One short paragraph: what this event / folder covered overall.
- The registry table (exact columns from taxonomy §5), one row per unit, IDs `<SLUG>-NN`.
- `## Standouts` — the 1–3 highest-scored IDs, one-clause reason each.
- `## Coverage` — number of units found, confirm it matches the `.sln` (plus standalone
  plugins) present, and list anything skipped and why (empty / non-ESAPI / build artifact).

No code blocks. No per-method narration. The shard is a scannable index, not a manual.

## Done when
`/docs/registry/<SLUG>.md` exists and its coverage count matches the folder. Run once per
event folder; small webinars can run back-to-back in one session (each writes its own shard).
