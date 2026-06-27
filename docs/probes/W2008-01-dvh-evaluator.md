# W2008-01 — DVH_Evaluator (CSV-template-driven DVH constraint evaluator + multi-plan comparison)

| Field | Value |
|---|---|
| ID | W2008-01 |
| Solution | DVH_Evaluator (DVH Evaluator / Plan Comparison Tool) |
| Source event | 20 Aug 2020 Webinar — Constraint Export |
| ESAPI version | v11+ (read-only; code paths annotated "valid for V15") |
| Type | Binary plugin (.esapi), two thin entries over one shared library |
| Reuse verdict | Adaptable (parser is Liftable) |

## Problem
A physicist wants to score a calculated plan against a clinic- or patient-specific constraint table written in the Mayo-et-al DVH analysis nomenclature (D95%[cGy], V60Gy[%], Max[cGy], DC700cc, CI30Gy...), classify each objective Goal / Variation / Not met / Not evaluated, and produce a shareable, color-coded HTML report. The same engine should also run across several plans/plansums at once for a side-by-side comparison.

## Approach
The interesting part is that constraints are *data* (a CSV), not code, and the nomenclature is parsed at runtime into ESAPI calls.

- **CSV as constraint template** (`DataModel.CreateObjectives` / `ParseCSV` / `ReadObjectives`) — columns are `StructureName, StructureCode, Aliases, DVHObjective, Evaluator, VariationAcceptable, Priority`. Pipe-delimited `Aliases` give TG-263-style fallback IDs. Files are auto-located by MRN glob (`*patientId*`) in a configured directory; multiple matches trigger an `OpenFileDialog`.
- **Mayo-nomenclature parser** (`StructureObjective.DetermineMetricType`) — the prize. A `Dictionary<Regex,string>` maps objective strings to nine metric types, capturing named groups `evalpt` / `unit` / `evalunit` (e.g. `D95%[cGy]` -> Dose at Volume, evalpt 95, unit %, evalunit cGy). A second regex parses the `Evaluator` (`<|<=|=|>=|>` + value) and a third the variation value.
- **Evaluation dispatch** (`EvaluateObjectiveAchieved` switch) — each metric type routes to a helper: `EvaluateDoseAtVolume`, `EvaluateVolumeAtDose`, `EvaluateMinMaxMean`, `EvaluateVolume`, plus derived metrics built by recursing with a temp `StructureObjective`: Covered Dose/Volume (`DCxcc = D(Vtot−x)cc`), and Conformality Index (isodose volume in Body/External ÷ target volume).
- **Pass/fail logic** (`EvaluateObjectiveMet`) — cheekily evaluates the assembled string (e.g. `"4000<5000"`) via a `System.Data.DataTable` computed-column expression rather than parsing operators by hand.
- **Single vs comparison split** — `DVHEvaluator/Script.cs` and `PlanComparisonTool/Script.cs` are near-identical entries differing only by a `mode` string ("singlePlan" / "planComparison") passed into the shared `DVHEvaluator_Main` ctor; `DataModel` branches on mode, launching the WPF `PlanChooserViewModel` (Course/Plan tree, INotifyPropertyChanged, modal `ShowDialog`) only for comparison.
- **Report** (`ExportToHtml`) — fills an embedded `Template_HTML.txt` via `###`-token string replacement, one column-triple (Met/Achieved/Warnings) per plan, CSS classes `pass`/`variation`/`fail`/`notEval`/`warning`, numbered warning legend; written to temp and `Process.Start`-ed.

## ESAPI surfaces
- Scope: `ScriptContext.{CurrentUser, Patient, Image, StructureSet, PlanSetup, PlansInScope, PlanSumsInScope}`; `Patient.Courses`, `Course.Patient`
- Items/types: `PlanningItem`, `PlanSetup`, `PlanSum.PlanSetups`, `Structure`, `StructureSet.Structures`, `Structure.{Id, Volume, IsEmpty, DicomType}`, `PlanSetup.{IsDoseValid, DosePerFraction}`
- Metrics: `PlanningItem.GetDoseAtVolume`, `GetVolumeAtDose`, `GetDVHCumulativeData(...) -> DVHData.{MinDose, MaxDose, MeanDose, CurveData, Volume, Coverage, SamplingCoverage}`, `DVHPoint`
- Value types: `DoseValue` (+`DoseUnit.{Gy,cGy,Percent,Unknown}`, `IsUndefined`, `UndefinedDose`), `VolumePresentation`, `DoseValuePresentation`
- Non-ESAPI plumbing: `Regex`/named groups, `System.Data.DataTable` expression eval, `StreamReader` CSV split, WPF (`Window`, `INotifyPropertyChanged`, `OpenFileDialog`/`SaveFileDialog`), embedded-resource HTML templating, `Process.Start`

## Reusability
The nomenclature parser (`StructureObjective` regex dictionary + the four core `Evaluate*` helpers) is genuinely liftable and is the reason to clone this — drop in your own CSV and you have a TG-263-aware constraint engine. The CSV-as-template and HTML-token-templating patterns also lift cleanly. Caveats: this is read-only, so `IsWriteable` stays commented. Unit handling is brittle and V15-specific — multiple branches hand-convert cGy<->Gy and special-case PlanSum (relative dose unsupported; `GetVolumeAtDose` wrapped in try/catch to dodge "Dose Units do not match system settings"); a modern port should normalize on `DoseValuePresentation`/`VolumePresentation` and current default-unit behavior rather than these string-compares on `UnitAsString`. CSV parsing is a naive `Split(',')` that breaks on embedded commas (handled only by flagging a "Parsing Error" row) — swap in a real CSV reader. The custom `DvhExtensions.DoseAtVolume`/`VolumeAtDose` bin-interpolation is legacy plumbing for plansums; prefer the native `GetDoseAtVolume`/`GetVolumeAtDose` where supported.

## Idea sparks
- Wire the parser to a standing departmental QUANTEC/protocol CSV library keyed by site for a one-click batch plan-check across a cohort (headless, skip the WPF chooser).
- Reuse the regex dictionary as a standalone "constraint-string -> ESAPI call" microservice feeding a knowledge-based-planning or auto-planning QA dashboard.
- Extend the metric set (add gEUD, homogeneity index, R50) by adding one regex row + one `Evaluate*` helper — the dispatch switch makes it cheap.
