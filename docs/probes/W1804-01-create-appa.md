# W1804-01 — CreateAPPA (auto AP/PA plan with MLC beams fitted to the PTV)

**Cluster 7 delta** — exemplar [DW18-06 AutoPlan](DW18-06-autoplan.md).

- **Problem:** auto-create a simple opposed AP/PA plan (gantry 0°/180°) whose two MLC beams are jaw- and
  MLC-fitted to the PTV, prescribed, and saved — the minimal field-shaping planning member.
- **Differs from the exemplar:** a **standalone exe** (`Application.CreateApplication` + `OpenPatientById`,
  `[assembly: ESAPIScript(IsWriteable = true)]`) rather than a plugin, and it foregrounds the
  **geometry-fitting** surfaces DW18-06 only touches lightly. After two `AddMLCBeam` at 0°/180° it calls
  `FitCollimatorToStructure` (asymmetric X/Y jaws + collimator-rotation optimization) and
  `FitMLCToStructure` with `JawFitting.FitToRecommended`, `OpenLeavesMeetingPoint` and
  `ClosedLeavesMeetingPoint` settings, then renames each field from `GantryAngleToUser` /
  `CollimatorAngleToUser` and `SaveModifications`.
- **Surfaces it adds:** `ExternalPlanSetup.AddMLCBeam`, `Beam.FitCollimatorToStructure`,
  `Beam.FitMLCToStructure` (+`FitToStructureMargins`, `JawFitting`, `OpenLeavesMeetingPoint`,
  `ClosedLeavesMeetingPoint`), `GantryAngleToUser`/`CollimatorAngleToUser`, `Application.SaveModifications`.
- **Reuse note:** the `FitCollimatorToStructure` / `FitMLCToStructure` calls are the liftable gem — the
  canonical way to auto-shape fields to a target and the piece most reusable in any auto-planning tool.
  Hardcoded patient id `exercise5-0`, structure `PTV`, structure set `CT_1`, and machine need porting.
  Verdict Adaptable.
