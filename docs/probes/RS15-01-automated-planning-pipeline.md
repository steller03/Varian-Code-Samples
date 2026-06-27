# RS15-01 — AutomatedPlanningDemo (prescription → QA, full pipeline)

| Field | Value |
|---|---|
| ID | RS15-01 |
| Solution | AutomatedPlanningDemo |
| Source event | Research Symposium 2015 — Eclipse Scripting API |
| ESAPI version | v13.6 |
| Type | Standalone exe (writeable, `Application.CreateApplication`) |
| Reuse verdict | Adaptable |

## Problem
The reference end-to-end prostate auto-planning demo: from a CTV and a typed prescription, build a
full IMRT plan — PTV creation, 7-field geometry with auto-fit jaws, RapidPlan DVH estimation,
optimization, dose calc, normalization — then auto-generate a DVH report, a plan-quality scorecard,
and per-field + combined QA verification plans. It's the canonical "what a complete scripted planning
workflow looks like" skeleton.

## Approach
`Execute` opens the patient, calls `BeginModifications`, validates structures, clears prior script
output (old plan + generated structures), and pops a `PrescriptionDialog` (WPF) for dose/fraction/
margin/CTV. It then drives a pipeline of static `PlanGeneration` helpers:
1. **Geometry** — `SetPrescription`; `CreatePTVFromCTV` via `Structure.Margin`; match plan structures
   to RapidPlan-model ids with a regex dictionary (`GetStructureMatches`); subtract spared OARs
   (rectum) from PTV with `SegmentVolume.Sub`; **fit jaws per gantry angle** by projecting every PTV
   contour point into beam's-eye-view (`GetContoursOnImagePlane` → trig projection → min/max rect +
   margin) and `AddStaticBeam` at 7 fixed angles.
2. **DVH estimation** — `SetCalculationModel(DVHEstimation, …)` + `CalculateDVHEstimates(model,
   targetDoseLevels, matches)`; add a normal-tissue objective (`AddNormalTissueObjective`).
3. **Optimize** — `Optimize` (IMRT, 2500 iters, restart) → `CalculateLeafMotions` → `CalculateDose`.
4. **Normalize** — adjust `PlanNormalizationValue` so V100%Rx ≥ 98% using `GetVolumeAtDose` /
   `GetDoseAtVolume`.
5. **Report** — `SVGFromDVH` writes an SVG DVH chart; `PlanQualityReporter` emits `report.xml` with an
   embedded XSLT stylesheet (pulled from assembly resources) that renders pass/fail clinical points.
6. **QA** — optionally copy a QA-phantom image from another patient
   (`CopyImageFromOtherPatient`) and build a verification plan per beam plus an "All fields" plan that
   recomputes dose with preset meterset values (`AddExternalPlanSetupAsVerificationPlan`,
   `CalculateDoseWithPresetValues`).
`app.SaveModifications()` is called at each stage. Credentials come from `ESAPI_USERNAME`/`_PASSWORD`
env vars.

## ESAPI surfaces
- `Application.CreateApplication`, `OpenPatientById`, `Patient.BeginModifications`, `SaveModifications`
- `Course.AddExternalPlanSetup`, `ExternalPlanSetup.SetPrescription`, `SetCalculationModel(CalculationType.*)`
- `StructureSet.AddStructure`, `Structure.Margin`, `SegmentVolume.Sub`, `Structure.GetContoursOnImagePlane`, `Structure.CenterPoint`
- `ExternalPlanSetup.AddStaticBeam(ExternalBeamMachineParameters, VRect jaws, coll, gantry, couch, iso)`
- `CalculateDVHEstimates`, `OptimizationSetup.AddNormalTissueObjective`, `Optimize(OptimizationOptionsIMRT)`, `CalculateLeafMotions`, `CalculateDose`
- `PlanNormalizationValue`, `GetVolumeAtDose`, `GetDoseAtVolume`
- `Course.AddExternalPlanSetupAsVerificationPlan`, `AddSlidingWindowBeam`, `Beam.GetEditableParameters`/`ApplyParameters` (control-point copy), `CalculateDoseWithPresetValues`, `Patient.CopyImageFromOtherPatient`

## Reusability
High-value but **environment-bound**: every algorithm string (`AAA 15.6.03`, `Photon Optimizer …`,
`DVH Estimation Algorithm …`, MLC id, leaf-motion calc), the RapidPlan model name, machine id,
gantry-angle list, and structure-match regexes are constants tuned to one clinic and one ESAPI build —
treat the file as a *blueprint*, port the constants. The genuinely liftable sub-techniques are
modular: **BEV jaw-fitting** (`FitJawsToTarget` / `ProjectToBeamEyeView`), **regex structure→model
matching**, **PTV-minus-OAR via `SegmentVolume` Booleans**, **normalization-to-V%** , and the
**verification-plan-from-beams** copy loop. Requires a writeable-enabled standalone context
(`BeginModifications` + research license). Version note: this is the v13.6 baseline; DW18-04 is the
same skeleton upgraded to v15.6 with an added MCO stage (see that probe).

## Idea sparks
- Lift `FitJawsToTarget` alone as a "re-fit jaws to target + margin" utility for any plan.
- Turn the structure-match regex dictionary into a configurable site-template engine for auto-planning
  multiple disease sites.
- Reuse the verification-plan loop to mass-produce IMRT/VMAT QA plans for an existing treated cohort.
