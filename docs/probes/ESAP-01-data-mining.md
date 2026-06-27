# ESAP-01 — DataMining (per-patient treatment report across ARIA)

| Field | Value |
|---|---|
| ID | ESAP-01 |
| Solution | DataMining |
| Source event | Eclipse Scripting API — `projects/` reference set |
| ESAPI version | v11 (standalone) |
| Type | Standalone exe (`Application.CreateApplication`) |
| Reuse verdict | Liftable |

## Problem
A physicist wants a database-wide census: one tab-delimited row per treated/approved plan across
*every* patient in ARIA, capturing prescription, fields, machines, energies, accessories,
isocenters, and a target DVH summary. This is the seed pattern for cohort analytics, machine-load
audits, and QA-population studies.

## Approach
A console app opens ARIA with `Application.CreateApplication(null, null)` (forces manual sign-in),
then walks `app.PatientSummaries`, calling `OpenPatient` / `ClosePatient` around each — the critical
scaling idiom, since you can't hold every patient open at once. Per patient it LINQ-filters courses ×
plan setups to the clinically relevant ones (`TreatmentApproved`, treated, or retired-with-`#`), and
writes one line per plan. `ReportOnePlan` is the substance: it sets `DoseValuePresentation.Absolute`,
emits course/plan/approval/date/normalization, then loops `ps.Beams` accumulating setup-vs-treatment
field counts, distinct machines, distinct energies, accessory types (wedge subclass name, compensator,
block, applicator, `MLC-<MLCPlanType>`, bolus), and a distinct-isocenter count (via vector distance
threshold). It resolves a target structure through a robust fallback ladder — `TargetVolumeID` →
`DicomType` ending in "TV" → a regex scan over a hand-curated id list (PTV/GTV/CTV/cord/lung…) →
`ORGAN` → `EXTERNAL` — then pulls `GetDVHCumulativeData` for Max/Mean/Min. A cooperative `StopNow()`
polls the keyboard so a long mining run can be interrupted.

## ESAPI surfaces
- `Application.CreateApplication`, `Application.PatientSummaries`, `OpenPatient` / `OpenPatient(PatientSummary)` / `ClosePatient`
- `Patient.Courses`, `Course.PlanSetups`, `PlanSetup.ApprovalStatus` (`PlanSetupApprovalStatus`), `IsTreated`
- `PlanSetup.UniqueFractionation` (`NumberOfFractions`, `PrescribedDosePerFraction`), `DoseValuePresentation`
- `Beam.IsSetupField`, `EnergyModeDisplayName`, `TreatmentUnit`, `Wedges`, `Compensator`, `Blocks`, `Applicator`, `MLC`, `MLCPlanType`, `Boluses`, `IsocenterPosition`
- `PlanSetup.GetDVHCumulativeData(structure, DoseValuePresentation, VolumePresentation, binWidth)` → `DVHData` (`MaxDose`/`MeanDose`/`MinDose`)
- `Structure.DicomType`, `PlanSetup.TargetVolumeID`, `Course.PlanSums`

## Reusability
The whole skeleton is liftable as-is: open-app → iterate `PatientSummaries` with open/close discipline
→ accumulate → write. Two pieces are independently valuable: the **target-structure fallback ladder**
(`FindTargetStructure`) and the **accessory/energy/machine accumulation** loop — both drop into any
cohort tool. Caveats: `DVHData`/`GetDVHCumulativeData` is the legacy DVH path (still supported; modern
code may prefer `GetDVHCumulativeData` results or `DVHEstimates`/`GetVolumeAtDose` for specific
points). `null,null` sign-in is interactive — for unattended runs pass real credentials. Database-wide
iteration is slow and load-sensitive; run off-hours and consider checkpointing.

## Idea sparks
- A machine-utilization / energy-mix dashboard fed by this row format (group by `TreatmentUnit`).
- A TG-263 / naming-hygiene audit reusing the structure-resolution ladder to flag patients where no
  target could be identified.
- A QA-population baseline: same walk, but emit DVH metrics for a fixed OAR set to build
  institutional dose-distribution statistics.
