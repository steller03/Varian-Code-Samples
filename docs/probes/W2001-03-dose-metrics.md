# W2001-03 — DoseMetrics (interactive D-at-V / V-at-D metric builder with pass/fail)

| Field | Value |
|---|---|
| ID | W2001-03 |
| Solution | DoseMetrics (16 Jan 2020 "SeparatedApps") |
| Source event | 16 Jan 2020 Webinar |
| ESAPI version | v15.6 ("Eclipse V115.6 MR3") |
| Type | Binary plugin (WPF/MVVM, `Execute(ScriptContext, Window, ScriptEnvironment)`) |
| Reuse verdict | Adaptable |

## Problem
Build ad-hoc dose metrics interactively — pick a structure, choose "Dose at Volume" or "Volume at Dose", enter the input value and units plus a tolerance, and get the computed value with a green/red pass-fail. The metric slice of the same SeparatedApps trio that fuses into W2001-01.

## Approach
Same Autofac + Prism-event skeleton as DVHPlot (W2001-02). `DoseMetricSelectionViewModel` seeds two `DoseMetricModel` templates — "Dose At Volume" (input units cc/%, output cGy/%) and "Volume At Dose" (input cGy/%, output cc/%) — exposes the plan's `Structures`, and gates an `AddMetricCommand` (`DelegateCommand` with `CanExecuteChanged`) on having both a structure and a metric selected. On add it sets the metric's `Structure`, calls `GetOutputValue()`, and publishes a fresh `DoseMetricModel` over an `AddDoseMetricEvent` for the results VM to collect.

The computation lives in `DoseMetricModel.GetOutputValue`: it null-checks the structure, branches on metric name to `_plan.GetDoseAtVolume(structure, InputValue, vol-pres, dose-pres).Dose` or `_plan.GetVolumeAtDose(structure, new DoseValue(InputValue, unit), vol-pres)`, with presentation enums chosen by ternaries on the `%` / `cc` / `cGy` unit strings. The tolerance string (`<` / `>` / `=` + number) is parsed with `TrimStart` and compared to set the `ToleranceMet` bool that drives a `PassFailColorConverter`.

## ESAPI surfaces
- `ScriptContext.PlanSetup`, `PlanSetup.StructureSet.Structures`, `Structure.Id`
- `PlanSetup.GetDoseAtVolume(structure, double, VolumePresentation, DoseValuePresentation)` → `DoseValue.Dose`
- `PlanSetup.GetVolumeAtDose(structure, DoseValue, VolumePresentation)`
- Types: `DoseValue` (+`DoseUnit.Percent`/`cGy`), `VolumePresentation` (Relative/AbsoluteCm3), `DoseValuePresentation` (Relative/Absolute)
- Non-ESAPI: Prism (`BindableBase`, `DelegateCommand`, `IEventAggregator`, `PubSubEvent`), Autofac

## Reusability
`GetOutputValue` is the liftable nugget: a compact, correct mapping of a metric name + unit strings to the right native call and presentation enums — exactly the boilerplate everyone rewrites. The template-seeding pattern (a `DoseMetricModel` per metric type carrying its valid unit lists) and the tolerance-string → `ToleranceMet` → color-converter chain are reusable for any constraint UI. Watch the demo edges: tolerance parsing assumes a well-formed `<n`/`>n` string and `Convert.ToDouble` throws otherwise; `==` equality on a `double` tolerance is fragile; a missing structure yields a sentinel `-1.0` rather than an error. `GetDoseAtVolume`/`GetVolumeAtDose` are current through v16. The full MVVM architecture is documented in the W2001-01 probe — this is the isolated metric slice.

## Idea sparks
- Lift `GetOutputValue` as a tiny shared metric-evaluation helper across plan-check tools, fed by a saved constraint list instead of UI input.
- Replace the `==`/`TrimStart` tolerance parser with the DW16-02 regex evaluator for proper goal/variation/not-met grading.
- Persist the built metric list to JSON as a reusable per-site template (the path W2001-01 takes).
