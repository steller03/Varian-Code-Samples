# DW16-28 / DW16-29 — Proton1 & Proton2 (uncertainty-DVH robustness metrics)

| Field | Value |
|---|---|
| ID | DW16-28 (Proton1) + DW16-29 (Proton2) — combined probe |
| Solution | Proton1 / Proton2 |
| Source event | Developer Workshop 2016 — katas Proton.1 & Proton.2 |
| ESAPI version | v13.7+ (13.7 / 15.0 / 15.1) |
| Type | Binary plugin (`Execute(ScriptContext)`) |
| Reuse verdict | Adaptable |

## Problem
A spot-scanning proton plan ships not just a nominal dose but a family of **uncertainty
scenarios** (isocenter shifts, range/calibration-curve errors) that Eclipse stores alongside the
plan. To judge robustness you need a DVH metric evaluated across that whole family, not just the
nominal curve. These two paired katas do exactly that for one structure each: Proton.1 reports the
spread of **max dose** on CORD across all scenarios; Proton.2 reports the spread of **D95%** on
CTV_5200. Both answer "how much does this metric move under uncertainty?"

## Approach
The shared core is `GetDVHDataWithUncertainties(IonPlanSetup, Structure, …)`: it builds the
nominal cumulative DVH via `IonPlanSetup.GetDVHCumulativeData(...)` (labelled `U0`), then iterates
`IonPlanSetup.PlanUncertainties` and calls **`PlanUncertainty.GetDVHCumulativeData(...)`** — same
signature as the plan's — once per scenario, collecting them all into a list of a small `curve`
POCO. That POCO bundles the `DVHPoint[]` curve data with the metadata needed to query it later
(`PrescribedDose`, `AbsoluteStructureVolume`, the two presentation enums, plus the scenario's
`IsocenterShift` / `CalibrationCurveError`). Each per-scenario extraction is wrapped in a
swallowing `try/catch` so a scenario that can't produce a DVH doesn't kill the run.

From that curve family the two katas diverge only in the reduction. **Proton.1** takes
`CurveData.Max(p => p.DoseValue.Dose)` per curve and reports Min / Max / Average of those maxima.
**Proton.2** needs an arbitrary point (D95%) off each *stored* curve — the built-in
`GetDoseAtVolume` works on a live plan, not on a saved `DVHPoint[]` — so it hand-rolls
`GetDoseAtVolumeForUncertainties`: locate the bracketing DVH points, linearly `Interpolate`, and
convert between relative/absolute volume and dose using the stored metadata. It then reports
Min / Max / Average D95% across the family. Both gate on
`PlanSetup.PlanType == ExternalBeam_Proton` and surface results in a `MessageBox`.

## ESAPI surfaces
- `ScriptContext.PlanSetup` / `PlanSetup.PlanType` (`PlanType.ExternalBeam_Proton`), `ScriptContext.IonPlanSetup`
- **`IonPlanSetup.PlanUncertainties`** (`PlanUncertaintyCollection` → `PlanUncertainty`)
- **`PlanUncertainty.GetDVHCumulativeData(Structure, DoseValuePresentation, VolumePresentation, binWidth)`** — the robustness workhorse; `IonPlanSetup.GetDVHCumulativeData(...)` for the nominal curve
- `PlanUncertainty.Id` / `.DisplayName` / `.IsocenterShift` (`VVector`) / `.CalibrationCurveError`
- `DVHData.CurveData` → `DVHPoint` (`.Volume`, `.DoseValue.Dose`)
- `IonPlanSetup.TotalDose`, `.TreatmentPercentage` (used to derive prescribed dose), `Structure.Volume`
- `VolumePresentation` / `DoseValuePresentation` enums (presentation conversion math)

## Reusability
The **uncertainty-DVH walk is the keeper** and lifts as-is: enumerate `PlanUncertainties`, call
`GetDVHCumulativeData` per scenario, and you have the full robustness family for any metric. The
`curve` POCO is a sensible model for a stored DVH plus its provenance and is worth adapting. The
hand-rolled `GetDoseAtVolumeForUncertainties` / `GetVolumeAtDoseForUncertainties` /
`Interpolate` helpers are useful in principle (querying an arbitrary saved curve) but the
bracket-index arithmetic — `Count() − Count(where …) − 1` — is brittle at curve endpoints and on
empty/short curves and should be hardened or replaced before production use. Other rough edges:
hard-coded structure IDs (`CORD`, `CTV_5200`), `MessageBox` output (not batchable), the silent
`catch`, and deriving Rx as `TotalDose / TreatmentPercentage`. `Ion*` and `PlanUncertainty` APIs
need v13.7+ and a proton-licensed environment to compile/run.

## Idea sparks
- **Robust DVH band**: at each volume take min/max dose across all scenarios to draw a worst-case
  envelope, and flag any target whose worst-case D95 drops below Rx or OAR whose worst-case Dmax
  exceeds tolerance.
- A batch **robustness QA check** over a course: assert worst-case D95 ≥ tol and worst-case OAR
  Dmax ≤ tol across scenarios, CSV out — the read side of a proton plan-check.
- Promote the `curve` + interpolation helpers into a small **stored-DVH query library** reusable
  for nominal curves, uncertainty scenarios, plan sums, and imported DVHs alike (after fixing the
  endpoint indexing).
