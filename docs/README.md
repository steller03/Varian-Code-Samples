# Varian Code-Samples Catalog

Working docs for cataloging **every problem solved** across the
[VarianAPIs/Varian-Code-Samples](https://github.com/VarianAPIs/Varian-Code-Samples)
repository, then organizing them into one browsable summary with selective deep dives.

The repo is ~80 Visual Studio solutions (plus a handful of standalone plugin scripts)
across two top folders: `webinars & workshops` (14 dated events) and `Eclipse Scripting API`.
It is overwhelmingly C# (~470 `.cs`, 69 `.xaml`); there is no slide-deck layer to speak of.

## How this works

Three dispatches, run against the repo from a Claude Code session:

1. **Triage** (`dispatches/1-triage.md`) — one run per event folder. Skims every solution,
   records *the problem it solves* (not the code), assigns one category, scores it 1–5,
   and writes a registry shard to `registry/<slug>.md`. Covers ALL solutions.
2. **Synthesis** (`dispatches/2-synthesis.md`) — run after triage (or as shards land).
   Reads every shard and produces `SYNTHESIS.md`: the categorized master summary,
   duplicate clusters, and a ranked "most interesting" shortlist. Re-runnable.
3. **Depth** (`dispatches/3-depth.md`) — on demand, for solutions flagged in the synthesis.
   Writes a ~1-page probe to `probes/<id>-<slug>.md` and back-links it in the registry.

`taxonomy.md` is the shared contract every dispatch reads first: the closed category list,
field vocabularies, the scoring rubric, the ID scheme, and the registry column schema.
Edit it there once and every dispatch inherits the change.

## Folder map

```
docs/
├── README.md          ← this file (also the triage tracker, below)
├── taxonomy.md        ← shared contract: categories, schema, rubric, slugs
├── registry/          ← triage shards, one per event   (the search surface)
├── SYNTHESIS.md       ← generated master summary        (the cohesive doc)
├── probes/            ← selective deep dives
└── dispatches/        ← the three dispatch prompts
```

## Triage tracker

One shard per row — check it off when `registry/<slug>.md` exists. Start with **DW16**:
its 31 solutions are the workshop "katas," the densest and cheapest teaching vein in the repo.

| Event | Slug | Solutions | Triaged |
|---|---|---:|:---:|
| Developer Workshop 2016 (katas) | DW16 | 31 | ☑ |
| Developer Workshop 2014 | DW14 | 9 | ☐ |
| Developer Workshop 2018 | DW18 | 9 | ☐ |
| 16 Jan 2020 Webinar | W2001 | 4 | ☐ |
| 21 Apr 2015 Webinar | W1504 | 4 | ☐ |
| 06 Apr 2018 Webinar | W1804 | 3 | ☐ |
| Research Symposium 2015 | RS15 | 2 | ☐ |
| 16 Oct 2018 Webinar | W1810 | 2 | ☐ |
| 20 Aug 2020 Webinar — Constraint Export | W2008 | 1 | ☐ |
| 31 Mar 2021 Webinar — Beam Data Visualization | W2103 | 1 | ☐ |
| 17 Dec 2017 Webinar | W1712 | 1 | ☐ |
| 14 Nov 2018 Webinar (DVH) | W1811 | 1 | ☐ |
| 22 Jul 2023 Developer Symposium | DS23 | 1 | ☐ |
| 23 Mar 2020 Webinar — ARIA Access | W2003 | 1 | ☐ |
| Eclipse Scripting API / projects | ESAP | 10 | ☐ |
| Eclipse Scripting API / plugins | ESPL | 4* | ☐ |

\*ESPL holds 4 single-file plugins (no `.sln`); catalog each file as its own unit.
**Total: 80 solutions + 4 standalone plugins ≈ 84 units.**
