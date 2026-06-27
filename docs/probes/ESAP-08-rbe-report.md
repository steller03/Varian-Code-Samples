# ESAP-08 — RBEReport (proton/biological-dose EQD2 report → PDF → ARIA)

| Field | Value |
|---|---|
| ID | ESAP-08 |
| Solution | RBEReport |
| Source event | Eclipse Scripting API — projects |
| ESAPI version | v13 |
| Type | Binary plugin (`Script.cs` `Execute`) |
| Reuse verdict | Adaptable |

## Problem
A physicist evaluating a course wants a radiobiological-effect summary — the biologically equivalent dose (EQD2) of each plan, with the freedom to vary the α/β assumption per target and watch the total move — and then wants that summary filed back into the patient's chart as a clinical document, not left as a loose file. This plugin builds that report interactively over the plans/plan-sums in scope, renders it to PDF, and pushes the PDF into ARIA. (Despite the "RBE/proton" framing in the registry, the shipped math is the standard photon linear-quadratic EQD2 keyed off prescription dose-per-fraction; there is no proton-specific RBE weighting in the code — see Approach.)

## Approach
`RBEReport.cs` (`Script.Execute(ScriptContext, Window)`) is plumbing: it collects every `PlanSetup` in `PlansInScope` plus `PlanSumsInScope` into a `List<PlanningItem>`, sets the WPF window content to a `UserControl1`, fills header fields (patient id/name/DOB, course, plan id, approval status, history user/date) on the bound `RBEViewModel`, and calls `AddPlanningItem` per plan — expanding a `PlanSum` into its member `PlanSetups`. `RBEViewModel` is the substance. Per plan it classifies technique (`GetTechnique`: VMAT/ARC/IMRT/STATIC from `Beam.GantryDirection` + `MLCPlanType`, or HDR/PDR brachy from `BrachyPlanSetup`), then computes EQD2 from `UniqueFractionation` via the textbook LQ identity `BED = n·d·(1 + d/(α/β))`, `EQD2 = BED/(1 + 2/(α/β))`, default α/β = 10. Two `ObservableCollection`s (a `DataGrid` row + a detail block) drive the UI; a `CellEditEnding` handler lets the user **edit α/β inline**, recomputes that plan's EQD2 and the live running total. `ExportToPDF` builds the document with **MigraDoc/PdfSharp** (header table + summary table + per-plan detail tables, rendered through `PdfDocumentRenderer`).

The ARIA leg is the distinctive piece. `PostToAria` writes the PDF to `C:\temp\RBEReport.pdf`, then `AriaDocumentPost.Post` reads the bytes and uploads them through the **ARIA Document Service web client** (`VMS.ARIA.DocumentService.WebService`). It constructs a `DocumentService(SERVICE_URL, USERID, PASSWORD)` and calls `service.InsertDocument(new InsertDocumentParameters { PatientId, BinaryContentAsBytes, FileFormat="PDF", DateOfService })`. The patient identifier is keyed as `"#" + patientId` (the leading `#` selects the id1 lookup; `$` and `~` are documented alternatives for other patient-key schemes). Known service faults surface as `WebClientBaseException` with a `ServiceError.ErrorCode` (e.g. `ECB_000` for bad credentials).

## ESAPI surfaces
- `Script.Execute(ScriptContext, System.Windows.Window)` — binary plugin entry; `window.Content = UserControl1`
- `ScriptContext`: `PlansInScope`, `PlanSumsInScope`, `PlanSetup`, `Patient`, `Course`, `StructureSet`, `CurrentUser`
- `PlanningItem` / `PlanSetup` / `PlanSum.PlanSetups`; `ExternalPlanSetup` vs `BrachyPlanSetup` (`NumberOfPdrPulses`, `Catheters` → `Catheter.TreatmentUnit.DoseRateMode`)
- `PlanSetup.UniqueFractionation` → `PrescribedDosePerFraction` (`DoseValue.Dose`/`.Unit`), `NumberOfFractions`; `TotalPrescribedDose`, `PrescribedPercentage`, `TargetVolumeID`, `ApprovalStatus`, `HistoryUserName`/`HistoryDateTime`
- `Beam.GantryDirection`, `Beam.MLCPlanType` (`VMAT`/`DoseDynamic`) for technique classification
- **Non-ESAPI:** MigraDoc/PdfSharp (PDF); `VMS.ARIA.DocumentService.WebService.WebClient.DocumentService.InsertDocument` + `InsertDocumentParameters` (ARIA post)

## Reusability
Two cleanly separable, liftable pieces. (1) **`AriaDocumentPost` is the high-value reusable artifact** — a working reference for filing any generated PDF into ARIA via the Document Service web client, including the patient-key prefix convention and `WebClientBaseException` error handling. But as-shipped it is a security liability: hard-coded service URL/IP, `SysAdmin`/`SysAdmin` credentials, and a `ServerCertificateValidationCallback => true` that blindly trusts all SSL certs. Externalize endpoint + credentials to config and fix certificate handling before any real use. (2) **The LQ/EQD2 helper** (`CalculateEQ2Dose`) is small and correct — copy it standalone; note it normalizes on **prescription dose-per-fraction**, so it's a prescription-level estimate, not a voxel/DVH-based spatial map, and it carries a latent unit bug (the BED term mixes `dosePerFraction` raw with `dosePerFractionInGy`, so cGy plans are mis-scaled). For genuine **proton** use you would replace this with an RBE-weighted model (constant 1.1 or a variable-RBE LET-dependent scheme); the code does not do that today. v13 APIs here are stable; verify the Document Service contract against your ARIA version. **Relationship to sibling W1504-04:** this is essentially the same RBEReport solution as the webinar version (W1504-04, v13.6), but a leaner snapshot — W1504-04 additionally carries a specialized PDR incomplete-repair model (`CalculateEQ2DoseForPDR`); this ESAP-08 copy only branches HDR/PDR in `GetTechnique` and throws on unsupported brachy types.

## Idea sparks
- Harden `AriaDocumentPost` (config-driven endpoint/creds, proper cert trust) into a generic "file this PDF into the chart" sink shared by every reporting plugin — plan checks, QA summaries, weekly chart-rounds packets.
- A proton-specific variant: swap the photon LQ for an RBE-weighted dose summary (1.1 default plus optional variable-RBE/LET overlay) and auto-archive the resulting biological-dose report to ARIA.
- Reuse the MigraDoc "header + summary table + per-item detail" template plus the ARIA post as a turnkey proton-QA document generator (machine/output QA, patient-specific QA results) that lands automatically in the record.
