# W1804-03 — CreateVerificationPlan (IMRT QA)

| Field | Value |
|---|---|
| ID | W1804-03 |
| Solution | CreateVerificationPlan |
| Source event | 06 Apr 2018 Webinar — Eclipse Scripting API |
| ESAPI version | v13.6 (declared good through 15.1) |
| Type | Binary plugin (`Execute(ScriptContext)`, `IsWriteable = true`) |
| Reuse verdict | Liftable |

## Problem
Pre-treatment IMRT/VMAT QA requires recomputing the clinical plan on a phantom geometry so the
delivery can be measured against a detector array. Doing this by hand — copy the phantom CT, make a
QA course, recreate every field, recalculate — is tedious and error-prone; this script automates the
whole composite-verification-plan creation.

## Approach
It takes the active `ExternalPlanSetup`, calls `BeginModifications`, and pulls the QA phantom into the
patient with `CopyImageFromOtherPatient` (IDs `$QAGeometry` / `CT MATRIXXEVO`). It gets-or-creates a
course `IMRTQA`, then `AddExternalPlanSetupAsVerificationPlan` links a new plan to the verified plan
over the phantom structure set. Isocenter is the body-structure center. Each clinical beam is rebuilt
via `AddSlidingWindowBeam` (preserving control-point meterset weights), and the original
`LeafPositions`/`JawPositions` are copied control-point-by-control-point through
`GetEditableParameters` → `ApplyParameters`. It collects per-beam `MetersetValue`s, sets a 1-fraction
prescription from the verified plan's `DosePerFraction`, copies the photon calculation model, and runs
`CalculateDoseWithPresetValues` so the QA dose reflects the clinical MU. A round-trip check confirms
`verificationPlan.VerifiedPlan` points back at the loaded plan. (A per-beam loop for field-by-field QA
plans is present but `#if`-disabled.)

## ESAPI surfaces
- `ScriptContext.ExternalPlanSetup`, `Patient.CopyImageFromOtherPatient`, `Patient.AddCourse`
- `Course.AddExternalPlanSetupAsVerificationPlan`, `ExternalPlanSetup.VerifiedPlan`
- `ExternalPlanSetup.AddSlidingWindowBeam`, `Beam.GetEditableParameters` / `ApplyParameters`
- `ControlPoint.LeafPositions` / `JawPositions` / `MetersetWeight`, `Beam.Meterset`, `MetersetValue`
- `PlanSetup.SetPrescription` / `SetCalculationModel` / `GetCalculationModel`, `ExternalPlanSetup.CalculateDoseWithPresetValues`

## Reusability
High — this is the canonical QA-plan automation idiom, and `AddExternalPlanSetupAsVerificationPlan`
plus `CalculateDoseWithPresetValues` remain the supported way to build a verification plan with the
clinical meterset. Caveats: the phantom patient/study/image IDs are hard-coded to a site setup;
`AddSlidingWindowBeam` assumes dynamic-MLC delivery (static/3D fields need a different add call); the
body-structure lookup by name prefix is brittle. **This is the same code as DW16-12** (the 2018
webinar reused the 2016 kata) — see that probe for the kata framing; the technique is identical.

## Idea sparks
- Enable the disabled per-beam loop to generate field-by-field verification plans for composite + per-field QA.
- Export the QA plan's planar dose (cf. DW16-16 ExtractDosePlane) straight into MapCheck/MatriXX comparison.
- Select the phantom automatically by treatment machine / detector so one script serves multiple QA devices.
