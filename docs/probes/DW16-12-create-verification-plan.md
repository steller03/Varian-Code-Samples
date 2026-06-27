# DW16-12 — CreateVerificationPlan (IMRT QA composite)

| Field | Value |
|---|---|
| ID | DW16-12 |
| Solution | CreateVerificationPlan |
| Source event | Developer Workshop 2016 — kata Intermediate.5 |
| ESAPI version | v13.6 (declared good through 15.1) |
| Type | Binary plugin (`Execute(ScriptContext)`, `IsWriteable = true`) |
| Reuse verdict | Liftable |

## Problem
The Intermediate.5 kata asks for an automation script that builds a new QA course, a composite
verification plan for the selected clinical plan (optionally one per beam too), and calculates dose
on all of them — the recurring pre-treatment IMRT QA chore, scripted.

## Approach
From the active `ExternalPlanSetup` it calls `BeginModifications`, copies the QA phantom image into the
patient via `CopyImageFromOtherPatient` (`$QAGeometry` / `CT MATRIXXEVO`), and gets-or-creates the
`IMRTQA` course. `AddExternalPlanSetupAsVerificationPlan` links a new plan against the verified plan on
the phantom structure set; isocenter is taken as the body-structure center. Each clinical beam is
rebuilt with `AddSlidingWindowBeam` carrying its control-point meterset weights, then
`LeafPositions`/`JawPositions` are copied per control point through `GetEditableParameters` →
`ApplyParameters`. Per-beam `MetersetValue`s are gathered, a 1-fraction prescription is set from the
verified plan's `DosePerFraction`, the photon calculation model is copied across, and
`CalculateDoseWithPresetValues` recomputes QA dose at the clinical MU. A round-trip check confirms
`VerifiedPlan`. A per-beam (field-by-field) variant is present but `#if`-disabled.

## ESAPI surfaces
- `ScriptContext.ExternalPlanSetup`, `Patient.CopyImageFromOtherPatient`, `Patient.AddCourse`
- `Course.AddExternalPlanSetupAsVerificationPlan`, `ExternalPlanSetup.VerifiedPlan`
- `ExternalPlanSetup.AddSlidingWindowBeam`, `Beam.GetEditableParameters` / `ApplyParameters`
- `ControlPoint.LeafPositions` / `JawPositions` / `MetersetWeight`, `Beam.Meterset`, `MetersetValue`
- `PlanSetup.SetPrescription` / `SetCalculationModel` / `GetCalculationModel`, `ExternalPlanSetup.CalculateDoseWithPresetValues`

## Reusability
Liftable and current — `AddExternalPlanSetupAsVerificationPlan` + `CalculateDoseWithPresetValues` is
the supported verification-plan idiom. **This is the same source as W1804-03** (the 2018 webinar
shipped this kata verbatim), so treat the two as one lineage; the only deltas are the surrounding
project files, not the technique. Same caveats apply: hard-coded phantom IDs, dynamic-MLC assumption
in `AddSlidingWindowBeam`, brittle body-name lookup, and the disabled per-beam loop.

## Idea sparks
- Turn on the disabled loop to emit per-field verification plans alongside the composite.
- Wire the resulting QA dose into a planar-dose export (cf. DW16-16) for array/film comparison.
- Parameterize the phantom by QA device so a single script covers MatriXX, ArcCHECK, etc.
