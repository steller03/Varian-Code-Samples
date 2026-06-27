# DW16-21 — Advanced_4 (data-mine patients by structure → DVH metrics CSV)

| Field | Value |
|---|---|
| ID | DW16-21 |
| Solution | Advanced_4 |
| Source event | Developer Workshop 2016 — kata Advanced.4 |
| ESAPI version | v11 (declared v11–15.0) |
| Type | Standalone exe (console) |
| Reuse verdict | Adaptable |

## Problem
A physicist wants a cohort-level answer: across the whole patient database, find every plan that
contains a given structure (e.g. `Bladder`) and tabulate its mean dose, max dose, and a
volume-at-dose metric (V50Gy). It's the canonical "walk the database, filter by anatomy, export DVH
stats to CSV" automation — the seed for any retrospective dose-outcome study.

## Approach
A standalone exe (`Application.CreateApplication`) iterates **every** `app.PatientSummaries`, opening
each patient in turn (`OpenPatient` / `ClosePatient` per iteration — mandatory, since only one patient
can be open at a time). For each patient it filters to **completed courses**
(`CompletedDateTime != null`) and **planning-approved plans that have dose**
(`Dose != null && ApprovalStatus == PlanningApproved`), so the scan only reports clinically meaningful,
calculated plans. For each such plan it looks up the structure of interest by exact Id
(`Structures.FirstOrDefault(o => o.Id.Equals("Bladder"))`); when present it sets absolute dose
presentation and pulls two things: `GetVolumeAtDose(roi, 50 Gy, Relative)` for the V50 metric, and
`GetDVHCumulativeData(...)` for `MeanDose` / `MaxDose`. Rows are appended to a `StringBuilder` and
written once at the end to `Advanced_4_Bladder.csv` in My Documents. A per-plan try/catch logs and
skips on error so one bad plan doesn't abort the whole multi-hour scan. All parameters
(structure, dose level, output path) are hard-coded with comments flagging them as the things a real
tool would take as input.

## ESAPI surfaces
- `Application.CreateApplication`, `Application.PatientSummaries`, `OpenPatient(PatientSummary)`, `ClosePatient()`
- `Patient.Courses` → `Course.CompletedDateTime`, `Course.PlanSetups`
- `PlanSetup.Dose`, `PlanSetup.ApprovalStatus` (`PlanSetupApprovalStatus.PlanningApproved`), `DoseValuePresentation`, `TotalDose`
- **`PlanSetup.GetVolumeAtDose(Structure, DoseValue, VolumePresentation)`**
- **`PlanSetup.GetDVHCumulativeData(Structure, DoseValuePresentation, VolumePresentation, binWidth)`** → `MeanDose`, `MaxDose`
- `StructureSet.Structures`, `DoseValue`

## Reusability
The **database-walk skeleton is the liftable asset** and is essentially timeless:
`PatientSummaries` → open → filter courses/plans → measure → close → CSV. It is the same idiom used
by every mining script in the repo (cf. DW16-11 FindLargestVolume, ESAP-01 DataMining), and this is a
clean, well-guarded instance of it (completed+approved+has-dose filtering, per-plan error isolation).
To productionize: parameterize structure/dose/output (args or a small UI), and — most importantly —
**match by a TG-263 / synonym set, not exact-Id equality**, since real databases have `Bladder`,
`Bladder_O`, `bladder`, etc. (cf. ESAP-09 StructureIdFrequency for the naming reality). The full-DB
scan is inherently slow and read-only; run it off-hours. APIs used are the oldest, most stable ESAPI
surfaces — no deprecation concerns.

## Idea sparks
- A general "cohort DVH harvester": pass a structure synonym list + a list of DVH metrics, emit one
  tidy CSV row per (patient, plan, structure) for import into R/Python outcome analysis.
- Feed this directly into DW16-18: have the walk emit the (patient, course, plan, structure) job
  file that DvhBioCorrection consumes, chaining database mining → biological metrics.
- Add diagnosis/site filtering (via ARIA query) so the scan targets a clinical cohort rather than the
  entire database, cutting runtime and sharpening the dataset.
