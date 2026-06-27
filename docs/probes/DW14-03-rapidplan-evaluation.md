# DW14-03 — RapidPlanEvaluation (standard-vs-RapidPlan DVH/NTCP comparison)

| Field | Value |
|---|---|
| ID | DW14-03 |
| Solution | RapidPlanEvaluation |
| Source event | Developer Workshop 2014 — guru track |
| ESAPI version | v13.5 |
| Type | Binary plugin (Execute(ScriptContext, Window)) + standalone twin + PluginTester host |
| Reuse verdict | Adaptable |

## Problem
When a clinic adopts RapidPlan (model-based DVH estimation), a physicist needs to judge whether the
knowledge-based plan actually beats the conventional one — and whether either plan is consistent with
the model's own predicted DVH band. This tool puts a standard plan and a RapidPlan side by side and
scores both against a panel of per-structure DVH and biological metrics, including the RapidPlan
upper/lower DVH *estimate* as a third reference column.

## Approach
Three-column comparison driven by a config-defined per-site metric panel.

- **Entry / plan triage (RapidPlanEvaluation.cs).** `Execute` rejects plan sums, requires exactly two
  `PlansInScope`, and verifies each has `Dose`. It distinguishes the two plans heuristically: the one
  with `plan.DVHEstimates.Count() == 0` is tagged the standard plan, the one with estimates is the
  RapidPlan. Both, plus the `StructureSet`, are handed to the WPF `MainControl`.
- **Metric dispatch (MainControl.xaml.cs).** `UpdateDoseMetrics` computes each `VMMetric` three times:
  `CalculateDoseMetric(StdPlan,...)`, `CalculateDoseMetric(RapidPlan,...)`, and the same RapidPlan with
  `UseRapPlanEstimate=true`. The view-model (`VMMetric`) then exposes the differences `StdMinusRp`,
  `StdMinusEst`, `RpMinusEst` as bindable deltas. Dispatch is a string switch over a `DoseMetrics`
  enum (DMean, DMax, D0.1cc, D95%, D5%, V33%, NTCP) falling through to `Calc.CustomMetric`.
- **DVH access (MyDVHData.cs).** `LoadDVH` has two paths. The actual-plan path calls
  `plan.GetDVHCumulativeData(structure, dosePresentation, volPresentation, BinSize)` and copies
  `CurveData`, `MaxDose.Dose`, `MeanDose.Dose` into a plain `DVHPoint[]`. The estimate path pulls
  `plan.DVHEstimates` filtered by `Structure.Id` and `DVHEstimateType.Upper`/`Lower`, then builds a
  curve as the *mean* of the upper and lower band volumes at each dose bin.
- **Metric math (Calc.cs).** D-at-volume / V-at-dose are hand-interpolated off the `DVHPoint[]` array
  rather than via `GetDoseAtVolume`/`GetVolumeAtDose`. The eight `D#/V#` custom bases switch on
  absolute-vs-relative dose and volume `Presentation` enums.
- **Biological model (BioDose.cs + Calc.NTCP).** This is a Lyman-Kutcher-Burman NTCP. `Calc.NTCP`
  differentiates the cumulative DVH into a differential one, EQD2-corrects every bin via
  `BioDose.bioCorrectEQD2` (`EQD2 = D * (1 + (D/n)/(α/β)) / (1 + 2/(α/β))`, n = `plan.UniqueFractionation.NumberOfFractions`,
  reference dose-per-fraction 2 Gy), computes gEUD with exponent `a = 1/n_LKB`, then
  `NTCP = Φ((gEUD − D50)/(m·D50))` using a series-expansion `Erf`/`NormSDist` (capped at z=4.89). LKB
  parameters (α/β, n, m, D50) come from the site config.
- **Config (MyConfig.cs, ConfigResolveHelper.cs, App.config).** Custom `ConfigurationSection` classes
  define DefaultMetrics, CustomMetrics, **Sites** (name → structure, metric, goal, α/β, LKB n/m/d50),
  and BioDose default α/β (Target 2.5, Organ 10). `ConfigResolveHelper` redirects config resolution to
  the plugin assembly's own directory so `ConfigurationManager.OpenExeConfiguration` works under
  Eclipse's host process. `SiteChooser` is the picker that seeds NTCP params per structure.

## ESAPI surfaces
- Scope: `ScriptContext.PlanSetup`, `PlansInScope`, `PlanSumsInScope`, `Patient`, `Course`,
  `CurrentUser`, `PlanSetup.StructureSet`, `PlanSetup.Dose`, `PlanSetup.Id`
- DVH (actual): `PlanSetup.GetDVHCumulativeData(Structure, DoseValuePresentation, VolumePresentation, binSize)`
  → `DVHData.CurveData` (`DVHPoint.DoseValue`, `.Volume`), `DVHData.MaxDose`, `.MeanDose`
- DVH (estimate): `PlanSetup.DVHEstimates` → `EstimatedDVH` (`.Structure.Id`, `.Type`,
  `.CurveData[i].DoseValue`, `.Volume`), `DVHEstimateType.Upper/Lower`
- Fractionation: `PlanSetup.UniqueFractionation.NumberOfFractions`
- Types: `Structure` (`.Id`, `.Volume`), `DoseValue` (`.Dose`, `.Unit`), `DoseValuePresentation`,
  `VolumePresentation` (Absolute/AbsoluteCm3/Relative)
- Non-ESAPI plumbing: WPF MVVM (`BindableBase`, `ObservableCollection`), `System.Configuration`
  custom `ConfigurationSection`/`ConfigurationElementCollection`, reflection-based config resolver

## Reusability
**Adaptable, not liftable.** Two pieces are genuinely portable. (1) The `DVHEstimates` /
`EstimatedDVH` upper-lower band reader in `MyDVHData.LoadDVH` is the rare reusable bit — anyone
building RapidPlan QC tooling can lift the filter-by-`Structure.Id`-and-`DVHEstimateType` pattern and
the band-mean curve construction as-is. (2) The LKB-NTCP + EQD2 chain in `Calc.NTCP`/`BioDose` is a
self-contained, ESAPI-light biological calculator you can drop into any cohort script. Caveats: the
D-at-volume / V-at-dose interpolation is hand-rolled off `CurveData`; modern code should prefer
`PlanningItem.GetDoseAtVolume` / `GetVolumeAtDose` (both exist in v13.5+) for correctness and to drop
~80 lines. The plugin assumes exactly two open plans and infers std-vs-RapidPlan purely from estimate
presence — fragile if both plans carry estimates. NTCP differentiates by simple bin subtraction, so it
inherits the configured `DVHBinSize`. The `ConfigResolveHelper` shim is needed because the binary
plugin can't see its own App.config under the Eclipse host — keep it if you go binary, drop it for a
standalone/CLI port. Excel export is commented out.

## Idea sparks
- A RapidPlan commissioning dashboard: run the `DVHEstimates` band reader headlessly over a validation
  cohort and flag plans whose achieved DVH falls outside the model's upper/lower envelope.
- A reusable NTCP/EQD2 library: extract `BioDose` + `Calc.NTCP` into a tested DLL with site LKB tables,
  shared across plan-check and retrospective-outcomes scripts.
- A "did RapidPlan actually help?" batch report computing `StdMinusRp` deltas per OAR across a month of
  cases to quantify clinical benefit of model-based planning.
