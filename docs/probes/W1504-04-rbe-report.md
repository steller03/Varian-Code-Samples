# W1504-04 — RBEReport (interactive EQD2 radiobiology report → PDF → ARIA)

| Field | Value |
|---|---|
| ID | W1504-04 |
| Solution | RBEReport |
| Source event | 21 Apr 2015 Webinar |
| ESAPI version | v13.6 |
| Type | Binary plugin (`Execute(ScriptContext, Window)`), WPF/MVVM |
| Reuse verdict | Adaptable |

## Problem
A physician/physicist evaluating a multi-phase or mixed-modality course wants the biologically
equivalent dose (EQD2) summed across all plans, with the freedom to try different α/β assumptions
per target and see the total move. This plugin builds that as an interactive, editable report on
the plans/plan-sums in scope, exports it to PDF, and posts the PDF back into the patient's ARIA
record as a clinical document.

## Approach
`RBEReport.cs` (`Script`) is mostly plumbing: it gathers every `PlanSetup` in `PlansInScope` plus
`PlanSumsInScope` into a `List<PlanningItem>`, fills header fields (patient, course, approval, history)
on the view model, and calls `AddPlanningItem` for each plan (expanding a plan sum into its member
plans). `RBEViewModel` is the substance. For each plan it classifies technique (`GetTechnique`:
VMAT/ARC/IMRT/STATIC from beam `GantryDirection` + `MLCPlanType`, or HDR/PDR for brachy from
`BrachyPlanSetup` catheters) and computes EQD2 from `UniqueFractionation` (dose-per-fraction × #fx)
via the standard linear-quadratic identity: `BED = n·d·(1 + d/(α/β))`, then `EQD2 = BED/(1 + 2/(α/β))`,
default α/β = 10. **PDR brachy gets a genuinely specialized model** (`CalculateEQ2DoseForPDR`) — an
incomplete-repair pulsed-dose-rate correction with repair half-time, pulse width and period feeding a
repair factor `fp` into the BED, not just the plain LQ. Results populate two observable collections
(a grid row + a detail block) bound to the WPF UI; the grid's `CellEditEnding` handler lets the user
**edit α/β inline**, recomputes that plan's EQD2 and the running total live. `ExportToPDF` builds the
document with **MigraDoc/PdfSharp** (header table + plan-summary table + per-plan detail tables,
rendered via `PdfDocumentRenderer`). `PostToAria` writes the PDF to `C:\temp` then hands it to
`AriaDocumentPost.Post`, which uploads it through the **ARIA Document Service web client**
(`DocumentService.InsertDocument`, patient keyed as `#<id>`, `FileFormat="PDF"`).

## ESAPI surfaces
- `ScriptContext.PlansInScope` / `PlanSumsInScope` / `PlanSetup` / `Course` / `StructureSet` / `CurrentUser`
- `PlanSetup.UniqueFractionation` → `PrescribedDosePerFraction`, `NumberOfFractions`; `TotalPrescribedDose`, `PrescribedPercentage`, `ApprovalStatus`, `HistoryUserName/DateTime`
- `ExternalPlanSetup` vs `BrachyPlanSetup` (`NumberOfPdrPulses`, `Catheters` → `TreatmentUnit.DoseRateMode`), `Beam.GantryDirection`, `Beam.MLCPlanType`
- Non-ESAPI: MigraDoc/PdfSharp (PDF), `VMS.ARIA.DocumentService.WebService` (post back to ARIA)

## Reusability
Three liftable, separable pieces. (1) **The LQ/EQD2 math** is clean and correct — copy it as a
standalone helper; the **PDR incomplete-repair model is rare and worth keeping**. (2) **The
MigraDoc report-builder** is a reusable template for any "summary table + per-item detail" plan
report. (3) **`AriaDocumentPost`** is the reference for programmatically filing a PDF into ARIA —
but as-shipped it is a security liability: hard-coded service URL/IP, `SysAdmin`/`SysAdmin`
credentials, and a `ServerCertificateValidationCallback => true` that trusts all SSL certs. Move
endpoint+creds to config and fix cert handling before any real use. EQD2 normalizes on prescription
dose-per-fraction (not voxel/DVH dose), so it's a prescription-level estimate, not a spatial EQD2
map. v13.6-era APIs are stable; verify the Document Service contract against your ARIA version.

## Idea sparks
- A shop-wide "EQD2 across the whole course" button that sums external + brachy phases with the
  inline-α/β editor, for re-treatment and combined-modality decisions.
- Reuse `AriaDocumentPost` (hardened) as the generic "file this generated PDF into the chart" sink
  for every reporting plugin — plan checks, QA summaries, etc.
- Extend the LQ helper to a *spatial* EQD2: voxel-wise BED across a plan sum (pair with DW16-18's
  DVH bio-correction) to compare biological vs physical dose distributions.
