# DW16-01 — DVHMetrics (read a fixed panel of DVH metrics against goals)

| Field | Value |
|---|---|
| ID | DW16-01 |
| Solution | DVHMetrics |
| Source event | Developer Workshop 2016 (kata newbie.1) |
| ESAPI version | v11 (header: 11 / 13.6 / 13.7 / 15.0 / 15.1) |
| Type | Binary plugin (`Execute(ScriptContext)`) |
| Reuse verdict | Liftable (the calls) / Illustrative (hardcoded ids & goals) |

## Problem
The simplest recurring physics task: for a loaded prostate plan, read out the handful of DVH numbers a planner checks by hand — target near-max, target mean (absolute and %), and two OAR volume-at-dose constraints — and show them next to their goals. This kata is the "hello world" of DVH-metric evaluation: the minimal native ESAPI path with no abstraction layer.

## Approach
Guards first: `context.PlanSetup` non-null and `plan.IsDoseValid`. It then walks `StructureSet.Structures` binding four hardcoded ids (`PTV_6800`, `PTV_5600`, `Rectum`, `Bladder`), each with its own null-check and early `MessageBox`. The metrics are three native calls:
- `GetDoseAtVolume(ptv68, 0.03, VolumePresentation.AbsoluteCm3, DoseValuePresentation.Absolute)` → D0.03cc[Gy] (near-max).
- `GetVolumeAtDose(rectum, new DoseValue(56, Gy), VolumePresentation.Relative)` and the same for bladder at 40 Gy → V56Gy[%], V40Gy[%].
- `GetDVHCumulativeData(ptv56, …)` called **twice** — once `DoseValuePresentation.Absolute`, once `Relative` — reading `DVHData.MeanDose.Dose` to get the mean in Gy and in %.

Results drop into a fixed format string (structure / metric / goal / actual columns) shown in a `MessageBox`. No file output, no parameterization — the value is the canonical call signatures and presentation enums.

## ESAPI surfaces
- `ScriptContext.PlanSetup` / `.StructureSet`
- `PlanSetup.IsDoseValid`, `StructureSet.Structures`, `Structure.Id`
- `PlanSetup.GetDoseAtVolume`, `GetVolumeAtDose`, `GetDVHCumulativeData`
- `DVHData.MeanDose` (`DoseValue.Dose`)
- Types/enums: `DoseValue` (+`DoseValue.DoseUnit.Gy`), `VolumePresentation` (AbsoluteCm3 / Relative), `DoseValuePresentation` (Absolute / Relative)

## Reusability
The three metric calls are evergreen ESAPI (unchanged v11→v16) and lift verbatim — this is the reference for exact argument order and the abs/rel presentation choice. Everything around them is demo scaffolding: structure ids, goals, and the column layout are hardcoded, and the lookup loop has a latent idiom bug (the `PTV_6800` test is a standalone `if` while `PTV_5600`/`Rectum`/`Bladder` are chained `else if`, so the first match short-circuits the rest — harmless on this data but the wrong shape). To productionize you'd table-drive the structure/metric/goal triples — which is exactly what DW16-02 (CSV template) does. Contrast W1811-01, which wraps these same calls behind the ESAPIX query DSL.

## Idea sparks
- Promote the fixed panel to a per-site constraint table (TG-263 ids, goal, variation) and render pass/fail — the natural bridge to DW16-02.
- Wrap the same three calls in a headless batch loop to emit a cohort metric CSV.
- Keep the abs+rel `GetDVHCumulativeData` double-call trick wherever you need "mean dose in Gy and % of Rx" in one readout.
