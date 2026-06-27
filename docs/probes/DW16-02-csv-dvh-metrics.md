# DW16-02 — CSVDVHMetrics / TextDVHMetrics (CSV-template DVH constraint evaluator, Mayo nomenclature DSL)

| Field | Value |
|---|---|
| ID | DW16-02 |
| Solution | CSVDVHMetrics (TextDVHMetrics v2.1) |
| Source event | Developer Workshop 2016 (kata Newbie.2) |
| ESAPI version | v11+ |
| Type | Binary plugin (`Execute(ScriptContext)`, single-file) |
| Reuse verdict | Liftable |

## Problem
Planners and physicists keep their dose-volume goals in a spreadsheet. They want to point a script at that template, have it evaluate every objective against the loaded plan (or plan sum), mark each goal / variation / not-met, and write the filled-in results back as a CSV they can archive. This is the kata that turns the hardcoded panel of DW16-01 into a data-driven, template-based plan-QA report — implementing the DVH analysis-description language of Mayo et al. (PRRO 2016).

## Approach
The template's columns are Structure ID, Code, Aliases, DVH Objective, Evaluator, Priority. It parses with VB's `TextFieldParser`, builds a `StructureObjective[]`, then runs a two-pass evaluate:

1. **Parse + normalize units** — every objective expression is internally coerced to Gy (`ConvertUnitToGy` / `ConvertValueToGy` via regex), so the engine works in one unit system and converts back to the template's cGy only on output — sidestepping the cGy/Gy presentation traps that bite most DVH scripts.
2. **Resolve + evaluate (`EvaluateMetrics`)** — `FindStructureFromAlias` resolves the structure by id or any `|`-separated alias (case-insensitive). The objective string is decomposed by a regex cascade into metric families: min/max/mean/Volume, **Dose-at-Volume** (`D95%`, `D2cc`), **Volume-at-Dose** (`V40Gy`, `V98%`), and covered-dose/volume (`DC…`/`CV…`, parsed but flagged "Not supported"). Each family maps to the right native call — `GetDoseAtVolume` / `GetVolumeAtDose` / `GetDVHCumulativeData` (`.Min/Max/MeanDose`) — with `VolumePresentation` / `DoseValuePresentation` chosen from the parsed `%` / `cc` / `Gy` units.
3. **Score (`Met`)** — the Evaluator string (`<`, `<=`, `=`, `>=`, `>` + goal) is regex-parsed and the achieved value compared, yielding `Goal` / `Variation` / `Not met` (variation as a secondary tolerance).

Results merge back into the sheet (`UpdateWorkbook`), write to `%TEMP%\{patient}-{plan}.csv`, and the file is shelled open. A `DvhExtensions` helper makes the whole thing **plan-sum aware**: `GetDoseAtVolume` / `GetVolumeAtDose` / `IsDoseValid` are reimplemented for `PlanSum` (which lacks them natively) by interpolating off `GetDVHCumulativeData`, with cGy/Gy fallback retries.

## ESAPI surfaces
- `ScriptContext.PlanSetup` / `.PlanSumsInScope` / `.StructureSet` / `.Patient`
- `PlanSetup.GetDoseAtVolume`, `GetVolumeAtDose`, `GetDVHCumulativeData`; `DVHData.Min/Max/MeanDose`, `CurveData`, `DVHPoint.Volume/VolumeUnit`
- `PlanningItem`/`PlanSum.GetDVHCumulativeData`, `PlanSum.StructureSet`, `PlanSum.PlanSetups`
- `Structure.Id` / `.Volume`; `DoseValue` (+`DoseUnit`, `UnitAsString`), `VolumePresentation`, `DoseValuePresentation`
- Non-ESAPI: `Microsoft.VisualBasic.FileIO.TextFieldParser`, `System.Text.RegularExpressions`, `Microsoft.Win32.OpenFileDialog`

## Reusability
The liftable gem of cluster 1. The DVH-DSL parser (regex families → native calls), the alias-based structure resolution, and the goal/variation scoring are reusable as a headless plan-QA engine; the normalize-to-Gy strategy is the right way to avoid presentation bugs. The plan-sum extension methods are independently valuable — they are the standard workaround for `PlanSum` not exposing `GetDoseAtVolume`/`GetVolumeAtDose`. Caveats: `DC`/`CV` (covered dose/volume) are parsed but unimplemented; the manual `VolumeAtDose` interpolation off `CurveData` is index-based and coarse vs. the native call; output is comma-joined with no CSV escaping (a comma inside a structure id corrupts the row); and it shells the result via `Process.Start` + `Thread.Sleep(3000)`. ESAPIX and PlanQualityMetrics (ESAP-06) are the modern maintained equivalents — but this self-contained version takes no third-party dependency.

## Idea sparks
- Adopt the CSV template + regex DSL as a version-controlled, clinic-wide constraint library, run headlessly to batch-score a cohort into one results CSV.
- Lift the `PlanSum` `GetDoseAtVolume`/`GetVolumeAtDose` extensions into any tool that must evaluate metrics on plan sums.
- Wire the `Met` (Goal/Variation/Not met) output into a pass/fail dashboard or an automated second-check report.
