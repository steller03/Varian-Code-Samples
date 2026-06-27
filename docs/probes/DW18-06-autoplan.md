# DW18-06 — AutoPlan (compact auto-planning chain)

| Field | Value |
|---|---|
| ID | DW18-06 |
| Solution | AutoPlan |
| Source event | Developer Workshop 2018 — ESAPI Introduction (Completed Projects) |
| ESAPI version | v15.6 |
| Type | Binary plugin (`Execute(ScriptContext)`, `IsWriteable = true`) |
| Reuse verdict | Liftable |

## Problem
A teaching baseline that runs the entire automated-planning chain in one short script: grow a
target from an existing CTV, stand up a course and plan, drop in a conformal four-field box,
compute dose, normalize, and prescribe. It is the minimal "structures → beams → dose →
prescription" skeleton a physicist can read in one sitting and then specialize.

## Approach
After `Patient.BeginModifications`, it finds the CTV by `DicomType == "CTV"` and creates a PTV as
`ctv.Margin(8)` (8 mm isotropic), assigning the result to `ptv.SegmentVolume`. It adds a new course
and an `ExternalPlanSetup` on the current structure set, then builds an
`ExternalBeamMachineParameters` (TrueBeam, 6X, 600 MU/min, STATIC). Looping over four gantry angles
(270/0/90/180), each beam is created with `AddMLCBeam` (an empty `float[2,60]` leaf array plus a
±10 cm jaw rectangle, isocenter at `ptv.CenterPoint`) and then conformed with `FitMLCToStructure`
using a 10 mm fit margin and recommended jaw fitting. Finally `CalculateDose`, a normalization of
`Beams.Count() * 100`, and `SetPrescription(30, 180 cGy, 1)`. The real work is `FitMLCToStructure`,
which shapes the leaves and jaws to the PTV outline at each angle.

## ESAPI surfaces
- `Patient.BeginModifications`, `Patient.AddCourse`, `Course.AddExternalPlanSetup`
- `StructureSet.Structures` / `AddStructure`, `Structure.Margin`, `Structure.SegmentVolume`, `Structure.CenterPoint`, `Structure.DicomType`
- `ExternalBeamMachineParameters`, `ExternalPlanSetup.AddMLCBeam(... float[2,60], VRect<double>, ...)`
- `Beam.FitMLCToStructure(FitToStructureMargins, Structure, bool, JawFitting, OpenLeavesMeetingPoint, ClosedLeavesMeetingPoint)`
- `ExternalPlanSetup.CalculateDose`, `PlanSetup.PlanNormalizationValue`, `PlanSetup.SetPrescription`, `DoseValue`

## Reusability
Liftable as a template. The hard-coded machine name, energy, dose rate, gantry set, margins, and
prescription are exactly the knobs to parameterize. `AddMLCBeam` requires a leaf array sized to the
MLC model (`float[2,60]` is Millennium-120); `FitMLCToStructure` does the actual conforming so the
initial leaf array can be empty. The `[assembly: ESAPIScript(IsWriteable = true)]` attribute is
mandatory for plan creation. The API is unchanged through v15/16; swap `AddMLCBeam` for
`AddArcBeam`/`AddVMATBeam` to make it an arc plan. No error handling and a single-CTV assumption are
the obvious gaps before clinical use.

## Idea sparks
- Turn it into a parameterized "four-field box" or site-specific quick-plan template driven by a small config.
- Pair with DW16-22 (Advanced_5) to add a VMAT-arc variant of the same skeleton.
- Chain into verification-plan creation (W1804-03 / DW16-12) for an end-to-end auto-plan → QA pipeline.
