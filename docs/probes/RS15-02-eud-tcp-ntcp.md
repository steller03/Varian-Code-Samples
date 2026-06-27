# RS15-02 — EUDScript (EUD-based TCP/NTCP from plan DVHs via Gay-Niemierko)

| Field | Value |
|---|---|
| ID | RS15-02 |
| Solution | EUDScript |
| Source event | Research Symposium 2015 — Eclipse Scripting API |
| ESAPI version | v11 |
| Type | Script (single-file) |
| Reuse verdict | Adaptable |

## Problem
Physicists want to compare rival plans by predicted *biological* outcome, not just dose-volume points — how likely is tumor control (TCP) and how likely is normal-tissue complication (NTCP) for each structure. This script answers that directly inside Eclipse: it reads the active plan's DVHs and reports a per-structure gEUD plus its associated probability. It is a faithful C#/ESAPI port of the Gay & Niemierko Matlab reference (Phys Med 2007;23(3-4):115–25).

## Approach
`Execute` grabs the active `ExternalPlanSetup` (after validating patient/course/dose are present via `GetPlan`), then walks `Plan.StructureSet.Structures`. For each structure it pulls a cumulative DVH with `GetDVHCumulativeData` (absolute dose, relative volume, 0.01 bin width) and hands the curve to `CalculateEUDandProbability` along with that structure's four radiobiology parameters (`a`, `gamma50`, `D50`, `alpha/beta`). The parameters live in two dictionaries: a hard-coded `ParameterLibrary` of literature values keyed by tissue type (Breast, Lung, Spinal cord, Heart, …), and a patient-specific map that binds each plan structure `Id` (`"body"`, `"cord"`, `"left lung"`, `"PTV (breast tis)"`) to a library entry — this binding is the part you re-author per case.

The core routine reproduces Gay-Niemierko exactly. It differentiates the cumulative DVH into a differential histogram (bin-center dose, volume slab), converts each bin to a 2-Gy-equivalent biological dose using the LQ model (`d·(α/β + d/n)/(α/β + d_ref)`, where `n` is `UniqueFractionation.NumberOfFractions` and `d_ref` is `PrescribedDosePerFraction`), normalizes the volume slabs to sum to 1, then computes the generalized EUD as the volume-weighted power mean `gEUD = (Σ vᵢ·BEDᵢ^a)^(1/a)`. The sign of `a` makes the same formula serve targets (negative `a`, EUD→min dose, used for TCP) and serial OARs (large positive `a`, EUD→max dose, used for NTCP). gEUD is mapped to probability with the Niemierko logistic `P = 100 / (1 + (D50/gEUD)^(4·gamma50))`. Results are collected into a dictionary and `ReportResults` renders them in a hand-built WPF `Window` (a scrollable `Grid` of Structure / EUD(Gy) / TCP-or-NTCP(%) rows), sorted by descending probability.

## ESAPI surfaces
- `ScriptContext` → `Patient`, `Course`, `ExternalPlanSetup` (read-only plug-in entry, `Execute(ScriptContext)`)
- `ExternalPlanSetup.GetDVHCumulativeData(Structure, DoseValuePresentation.Absolute, VolumePresentation.Relative, binWidth)`
- `DVHData.CurveData` → `DVHPoint.DoseValue.Dose`, `DVHPoint.Volume`
- `PlanSetup.UniqueFractionation` → `PrescribedDosePerFraction.Dose`, `NumberOfFractions`
- `StructureSet.Structures`, `Structure.Id`; `PlanSetup.Dose` (null-check)
- Types namespace: `VMS.TPS.Common.Model.Types.DoseValuePresentation`, `VolumePresentation`

## Reusability
The numerical engine — DVH differentiation, LQ/BED conversion, gEUD power-mean, logistic TCP/NTCP — is pure math over a `double[,]` and lifts cleanly into any ESAPI version or even outside ESAPI; only the single `GetDVHCumulativeData` call and the `UniqueFractionation` reads touch the API, both of which still exist in v15/v16. The friction is configuration, not code: the patient-specific `parameters` dictionary is keyed by literal structure `Id` strings (`"left lung"`, `"PTV (breast tis)"`) and will throw `KeyNotFoundException` on any structure not pre-listed, so the foreach over *all* structures is effectively a foreach over the ones you remembered to register. To productionize, replace that with a lookup that skips/flags unmatched structures and source parameters from a config file or the literature table rather than inline constants (the flat `α/β = 10 Gy` for every tissue is a demonstrator simplification, not clinically defensible). No deprecated calls; as a read-only plug-in it needs no write license. WPF report is throwaway — swap for CSV/clipboard export if you want the numbers downstream.

## Idea sparks
- Wire the gEUD/TCP/NTCP engine into a plan-comparison tool that scores two `PlanSetup`s side by side and flags the biologically better trade-off, feeding a scorecard like the RS15-01 `PlanQualityReporter`.
- Drive the parameter library from a maintained, peer-reviewed table (QUANTEC / Emami) with per-site `α/β`, turning this into a defensible NTCP screening report across a treated cohort.
- Reuse the cumulative→differential→BED pipeline as a shared "biological DVH" utility for other models (LKB-NTCP, EUD-based optimization objectives) that need a fraction-corrected differential histogram.
