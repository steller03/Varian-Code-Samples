# DW16-10 — PatientSummary (treatment-history panel across courses; cluster 16 anchor)

| Field | Value |
|---|---|
| ID | DW16-10 |
| Solution | PatientSummary |
| Source event | Developer Workshop 2016 (kata Intermediate.3) |
| ESAPI version | v11 (declared 11 / 13.6 / 13.7 / 15.0 / 15.1) |
| Type | Binary plugin (WPF/MVVM, `Execute(ScriptContext, Window)`) |
| Reuse verdict | Liftable |

## Problem
Give a clinician a "treatment history" at a glance: every plan the open patient has, across all
their courses, with the course, target, prescription, creation date, and approval status in one
list. The anchor for cluster 16 (patient/plan summaries) — a read-only navigation panel, not a
single-plan deep dive (that's DW18-08) nor a headless cohort census (ESAP-01).

## Approach
A clean MVVM binary plugin. `Script.Execute(scriptContext, mainWindow)` is a four-line shim: build
`MainViewModel(scriptContext.Patient)`, wrap it in a `MainView`, drop the view into
`mainWindow.Content`, size the window. `MainViewModel` flattens the object model — iterate
`patient.Courses`, and for each `course.PlanSetups` collect every `PlanSetup` (null-guarding both
levels) — then projects each plan to a `PlanSetupViewModel` exposing `Id`, `Course.Id`,
`CreationDateTime`, `TargetVolumeID`, `TotalPrescribedDose`, and `ApprovalStatus`. The view binds the
resulting `IEnumerable<PlanSetupViewModel>`. No dose computation, no writes — the substance is the
Patient → Courses → PlanSetups walk and the MVVM-into-host-window wiring.

## ESAPI surfaces
- Entry: `Script.Execute(ScriptContext, Window)`, `ScriptContext.Patient`, host `Window.Content`
- `Patient.Courses`, `Course.PlanSetups`, `Course.Id`
- `PlanSetup.Id` / `.CreationDateTime` / `.TargetVolumeID` / `.TotalPrescribedDose` / `.ApprovalStatus` (`PlanSetupApprovalStatus`)

## Reusability
The whole thing is liftable as a **summary-panel template**: the Courses→PlanSetups flatten + the
project-to-view-model + the MVVM-into-`Window` shim are the reusable skeleton for any per-patient
review plugin, and none of the surfaces are version-fragile. To extend, add columns (dose totals,
completion dates), a `DataGrid` with sorting, or export. Contrast ESAP-01 (same walk, headless, one
CSV row per plan) and DW18-08 (one plan, every field).

## Idea sparks
- A printable treatment-history report (PDF/Word) generated from the same view-model list.
- Add `Course.CompletedDateTime`, total delivered dose, and fraction progress for a chart-review panel.
- Reuse the MVVM-into-`Window` shim as the house pattern for every review-only binary plugin.
