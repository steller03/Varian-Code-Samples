# DW16-25 — PlanIndices (conformity, gradient, heterogeneity indices)

| Field | Value |
|---|---|
| ID | DW16-25 |
| Solution | PlanIndices (DW2016 kata Advanced.7) |
| Source event | Developer Workshop 2016 — katas |
| ESAPI version | v11 (header: v11–15.0) |
| Type | Binary plugin (`Execute(ScriptContext)`) |
| Reuse verdict | Liftable |

## Problem
Compute the three standard plan-quality indices for the selected plan's target and display them:
**Conformity Index (CI)**, **Gradient Index (GI)**, and **Heterogeneity Index (HI)**. These are the
everyday SRS/SBRT conformality numbers a physicist reads off a conformal plan, and this is the
catalogue's only dedicated plan-indices unit.

## Approach
A binary plugin that guards `PlanSetup.IsDoseValid`, resolves the target via
`PlanSetup.TargetVolumeID`, and guards a non-zero `Structure.Volume`. It then computes, with dose
levels expressed as `DoseValue(…, Percent)` so they track the prescription:
- **CI = V100% / TV** — `GetVolumeAtDose(ptv, 100%, AbsoluteCm3)` ÷ `ptv.Volume`.
- **GI = V50% / V100%** — `GetVolumeAtDose` at 50% and 100% (relies on C# divide-by-zero → infinity
  rather than guarding).
- **HI = Dmax / Dp** — Dmax via `GetDoseAtVolume(ptv, 0%, Relative, Absolute)` (the near-max, dose to
  0 % volume); Dp = `DosePerFraction.Dose × NumberOfFractions`.

Results go to a `MessageBox`. Worth flagging the **definitions**: these are the RTOG-style ratio forms
(V100/TV is a coverage-flavoured CI, not the Paddick `TV_PIV²/(TV·PIV)`; HI is Dmax/Dp, not the ICRU
`(D2−D98)/D50`) — pick the definition your protocol expects.

## ESAPI surfaces
- `ScriptContext.PlanSetup`, `PlanSetup.IsDoseValid`, `PlanSetup.TargetVolumeID`
- `StructureSet.Structures`, `Structure.Volume`
- `PlanSetup.GetVolumeAtDose(structure, DoseValue, VolumePresentation)`
- `PlanSetup.GetDoseAtVolume(structure, volume, VolumePresentation, DoseValuePresentation)`
- `PlanSetup.DosePerFraction`, `PlanSetup.NumberOfFractions`
- `DoseValue` / `DoseValue.DoseUnit.Percent`, `VolumePresentation.AbsoluteCm3`

## Reusability
Pure, liftable index math over standard dose-query calls — drop the three formulas into any plan-QA
report or cohort exporter. The reusable pattern is `GetVolumeAtDose` / `GetDoseAtVolume` driven by
**percent-of-prescription** `DoseValue`s. To productionize: parameterize the index definitions (offer
Paddick CI and ICRU HI alongside these), let the caller choose the dose levels, and write to a report
sink instead of a `MessageBox`. It derives Dp from `DosePerFraction × NumberOfFractions`; standardize
on `TotalPrescribedDose` if you want one source of truth. All surfaces current.

## Idea sparks
- Add CI/GI/HI columns to PlanQualityMetrics (ESAP-06) or the DVH cohort exports (DW16-21, W1811-01).
- An SRS plan-quality scorecard that checks CI/GI against protocol thresholds and flags outliers.
- Compute the same indices across rival plans to drive an automated plan comparison.
