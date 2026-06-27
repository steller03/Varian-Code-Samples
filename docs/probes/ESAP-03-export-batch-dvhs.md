# ESAP-03 — ExportBatchDVHs (batch target-DVH dump to CSV)

| Field | Value |
|---|---|
| ID | ESAP-03 |
| Solution | ExportBatchDVHs |
| Source event | Eclipse Scripting API — `projects/` reference set |
| ESAPI version | v13.5 |
| Type | Standalone exe (`Application.CreateApplication`) |
| Reuse verdict | Liftable |

## Problem
A physicist needs cumulative DVH curves pulled in bulk — every plan with valid dose across the whole Eclipse database — so they can be opened in Excel/Python for offline analysis rather than read one plan at a time in the GUI. This is the minimal "get the curve points out" pattern: one CSV per plan's target structure, ready to plot, fit, or aggregate.

## Approach
A console app opens Eclipse with `Application.CreateApplication(null, null)` (no credentials → interactive sign-in), wrapped in a `using` so the session disposes cleanly, with all work inside a try/catch that prints exceptions to stderr. `Execute` ensures an output directory (`c:\temp\dvhdump`) exists, then walks `app.PatientSummaries`, calling `OpenPatient(ps)` / `ClosePatient()` around each patient — the open-close discipline that keeps a full-database sweep from holding everyone in memory at once. Per patient it iterates `Course.PlanSetups` filtered to `x.IsDoseValid`, and for each plan resolves the target by matching `plan.TargetVolumeID` against the structure set (`FirstOrDefault`, so a missing/blank target ID is simply skipped). Guarded on `plan.Dose != null && target != null`, it computes the curve with `plan.GetDVHCumulativeData(target, DoseValuePresentation.Absolute, VolumePresentation.Relative, 0.1)` — absolute dose (Gy/cGy), volume as percent, 0.1-unit bins.

The export is deliberately thin. `DumpDVH` opens a `StreamWriter`, writes a `Dose,Volume` header, then one row per `DVHPoint` in `dvh.CurveData` as `pt.DoseValue.Dose,pt.Volume`. Files are named `{patientId}_{courseId}_{planId}_{targetId}-dvh.csv`, which makes the cohort self-describing on disk and trivially groupable downstream. Only the target structure is exported — no OARs, no metrics, no thresholds — so the unit is a clean two-column curve extractor rather than a metrics reporter.

## ESAPI surfaces
- `Application.CreateApplication(null, null)`, `Application.PatientSummaries`, `OpenPatient(PatientSummary)`, `ClosePatient()`
- `Patient.Courses`, `Course.PlanSetups`, `PlanSetup.IsDoseValid`, `PlanSetup.Dose`, `PlanSetup.TargetVolumeID`
- `PlanSetup.StructureSet.Structures`, `Structure.Id`
- `PlanSetup.GetDVHCumulativeData(structure, DoseValuePresentation, VolumePresentation, binWidth)` → `DVHData`
- `DVHData.CurveData` → `DVHPoint` (`DoseValue.Dose`, `Volume`)
- `DoseValuePresentation.Absolute`, `VolumePresentation.Relative`

## Reusability
The whole loop is liftable: open-app → iterate `PatientSummaries` with open/close → filter to valid-dose plans → export. To scope it (single patient, course filter, approved-only), swap `app.PatientSummaries` for `OpenPatientById` plus a LINQ predicate on `PlanSetups`. The two presentation choices are the load-bearing gotcha: `Absolute`/`Relative` here gives **dose in Gy/cGy vs volume in %**; for cohort comparison across differing prescriptions you usually want `DoseValuePresentation.Relative` (% of Rx) and/or `VolumePresentation.AbsoluteCm3` — and you must record which combination produced a given file, because the CSV itself carries no units. `GetDVHCumulativeData`/`DVHData`/`DVHPoint` are the legacy DVH path; still fully supported in v13.5 and modern builds, but for single-point queries newer API offers `GetVolumeAtDose`/`GetDoseAtVolume`. Hard-coded `c:\temp\dvhdump` and the interactive `null, null` sign-in should be parameterized for unattended runs. Note the source banner says "v11+" while the project references the **13.5** binaries — recompile against your site's `VMS.TPS.Common.Model.API.dll` version.

## Idea sparks
- A cohort DVH database: redirect output to per-structure tables (export all OARs, not just the target) and ingest into SQLite/pandas for institutional dose-distribution statistics.
- Plan-comparison ingestion: emit both `Relative` and absolute presentations so an offline tool can normalize and overlay competing plans for the same patient/course.
- Auto-feed an NTCP/EUD model: stream the curve points straight into a Lyman-Kutcher-Burman or gEUD calculator (e.g. RS15-02) instead of (or alongside) writing CSV.
