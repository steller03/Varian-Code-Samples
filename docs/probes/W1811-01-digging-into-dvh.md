# W1811-01 — DiggingIntoDVH (native-vs-ESAPIX DVH toolkit: metrics, constraints, cohort mining, plotting)

| Field | Value |
|---|---|
| ID | W1811-01 |
| Solution | DiggingIntoDVH |
| Source event | 14 Nov 2018 Webinar (DVH) |
| ESAPI version | v15.5 (VMS API 15.5 via ESAPIX_15.5 NuGet, ESAPIX 1.5.2.6, .NET 4.5) |
| Type | Standalone exe (Application.CreateApplication entry) |
| Reuse verdict | Adaptable |

## Problem
A physicist routinely needs the same handful of DVH operations: pull cumulative/differential DVH and its min/mean/max, query D95/V100-style metrics, evaluate dose-volume constraints with pass/fail, and do it across a cohort exported to CSV for offline analysis. The native ESAPI API makes each of these verbose and easy to get wrong (presentation enums, unit handling, structure lookups). This sample is a side-by-side tour contrasting the raw native calls against the open-source ESAPIX helper library that wraps them.

## Approach
`_Program.cs` is a flat standalone `Main` that calls each demo in sequence — there is no orchestration, just paired native-then-ESAPIX examples on the same patient (`DA00005`) and plan (`ABD ARC1/2`). Every demo opens its own `Application.CreateApplication()` in a `using` block and finds the plan via `Courses.SelectMany(c => c.PlanSetups)` + `FirstOrDefault`.

- **Native (`StandardFunctionsDemo.cs`)** — the raw path: `plan.GetDVHCumulativeData(ptv, D.Absolute, V.Relative, 0.1)` then reads `DVHData.MinDose/MeanDose/MaxDose` and walks `CurveData` points (`DoseValue`, `Volume`, `VolumeUnit`). Dose-at-volume and volume-at-dose go through `GetDoseAtVolume(...)` / `GetVolumeAtDose(plan.TotalDose, V.Relative)` with explicit presentation enums.
- **ESAPIX (`ESAPIXFunctionsDemo.cs`)** — same metrics, terser. A differential DVH is one extension call: `cumulative.Differential()` on the native `CurveData`. Metrics collapse to a string DSL: `plan.ExecuteQuery("D95%[Gy]", "PTV_3000")` and `plan.ExecuteQuery("V100%[%]", "PTV_3000")` — no presentation enums, structure resolved by Id string.
- **Constraints (`PlanConstraintsDemo.cs`)** — shows the native protocol path `plan.GetProtocolPrescriptionsAndMeasures()` (returns rxs/measures tuple), then ESAPIX's `plan.GetConstraints()`. The authoring framework: `ConstraintBuilder.Build("PTV_3000", "D95%[cGy] >= 2800", PriorityType.PRIORITY_2)` yields `IConstraint`s; each is gated with `con.CanConstrain(plan)` (returns success/message) before `con.Constrain(plan).ResultType` gives the pass/fail. This guard-then-evaluate pattern is the reusable core.
- **Mining (`DVHMiningDemo.cs`)** — the cohort pattern: `new ESAPIX.Helpers.DVH.Miner()`, `AddPatientId(...)` per patient, `SetStructureSetFilter("ABDOM", CLOSEST_MATCH)` (fuzzy structure-set matching), then `GetMetrics(app, new StructureQuery("PTV_3000", "D95%[Gy]", "D99%[Gy]"))` returns a CSV object with `.Write(path)`. Whole cohort-to-CSV in ~8 lines.
- **Plotting (`PlottingDemo.cs` + `PlotView.xaml`)** — builds an OxyPlot `PlotModel` with dose/volume `LinearAxis`, then per-structure a `LineSeries` colored from `Structure.Color.R/G/B`, points from `CurveData` (`pt.DoseValue.GetDoseCGy()` extension, `pt.Volume`), shown in a WPF `Window`.

## ESAPI surfaces
- **Scope/entry:** `VMS.TPS.Common.Model.API.Application.CreateApplication`, `OpenPatientById`, `Patient.Courses`, `Course.PlanSetups`, `PlanSetup.StructureSet.Structures`, `Structure.Id/.Color`, `PlanSetup.TotalDose`
- **Native metrics:** `PlanningItem.GetDVHCumulativeData(...) -> DVHData.MinDose/MeanDose/MaxDose/CurveData`, `DVHPoint.DoseValue/Volume/VolumeUnit`, `GetDoseAtVolume`, `GetVolumeAtDose`, `GetProtocolPrescriptionsAndMeasures`
- **Types/enums:** `DoseValuePresentation` (Absolute), `VolumePresentation` (Relative), `DoseValue`
- **ESAPIX helpers (non-Varian, open source):** `ESAPIX.Extensions` (`ExecuteQuery`, `Differential`, `GetDoseCGy`, `GetConstraints`); `ESAPIX.Constraints` / `.Constraints.DVH` (`IConstraint`, `ConstraintBuilder.Build`, `PriorityType`, `CanConstrain`, `Constrain().ResultType`); `ESAPIX.Helpers.DVH` (`Miner`, `StructureQuery`); `ESAPIX.Helpers.Filters.MatchType.CLOSEST_MATCH`
- **Plumbing:** OxyPlot (`PlotModel`, `LinearAxis`, `LineSeries`, `DataPoint`, `OxyColor`), WPF `Window`

## Reusability
The native `StandardFunctionsDemo` block is fully **liftable** and version-agnostic back to v11 — `GetDVHCumulativeData`/`GetDoseAtVolume`/`GetVolumeAtDose` with presentation enums are stable, evergreen ESAPI. The OxyPlot DVH plotter is also liftable as a self-contained recipe. Everything else (the prize: query DSL, constraint framework, cohort Miner-to-CSV) depends on **ESAPIX**, a third-party NuGet, not Varian code — so "adaptable," not liftable: you must take the dependency (`ESAPIX_15.5.1.5.2.6`, pinned to v15.5 VMS assemblies) and accept its version coupling. Hardcoded patient/plan IDs and `D:\Examples\minerExample.csv` are demo stubs to parameterize. If you don't want the dependency, the `CanConstrain`-then-`Constrain` guard pattern and the `AddPatientId -> SetStructureSetFilter -> GetMetrics -> Write` mining flow are cheap to reimplement against native calls. Note ESAPIX targets specific VMS versions, so on v16+ you'd re-source a matching ESAPIX build or drop it.

## Idea sparks
- Build a clinic constraint table as `ConstraintBuilder.Build(...)` strings (TG-263 ids) and run `CanConstrain`/`Constrain` as a headless plan check — the missing-structure path (`PTV_NA`) already demonstrates graceful failure.
- Drive the `Miner` over a treatment-site cohort with a `StructureQuery` of your reporting metrics to produce a constraint-compliance spreadsheet for a protocol audit.
- Reuse the OxyPlot per-structure `LineSeries` builder as a batch DVH-overlay generator (plan-vs-plan, or pre/post replan) exported to PNG instead of a dialog.
