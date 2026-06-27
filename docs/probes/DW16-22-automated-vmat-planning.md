# DW16-22 — Advanced_5 (automated VMAT planning)

| Field | Value |
|---|---|
| ID | DW16-22 |
| Solution | Advanced_5 |
| Source event | Developer Workshop 2016 (kata Advanced.5) |
| ESAPI version | v11 (author notes v11–15) |
| Type | Standalone exe (writeable, `Application.CreateApplication`) |
| Reuse verdict | Adaptable |

## Problem
The reference for **fully scripted prostate VMAT planning**: given a structure set, generate the
optimization helper structures, build the course/plan and arc beams, set objectives, optimize, calculate
dose, and read back DVH metrics — the whole "blank patient → deliverable-ish plan" loop. The highest-leverage
auto-planning pattern in the DW16 katas (Charles Mayo / U-Michigan).

## Approach
`Execute` hard-codes a demo patient/course/structure-set, then hands a target map and an allowed-OAR list to a
`Planning(...)` method that does the work. Targets are passed as `Tuple<role, structureId, RxDose, unit>`
(e.g. `PTV_High`→`PTV_6800`@68 Gy) so the generic planning logic is decoupled from clinic structure IDs.
1. **Nomenclature check** — iterates structures, classifies by `DicomType` (PTV/CTV/GTV vs OAR), and flags
   each as standard/non-standard against the target map and allowed-OAR list, surfaced in a `MessageBox`.
2. **Optimization structures** — builds four helpers with `AddStructure("ORGAN", id)` (deleting any prior copy
   first): `zPTV_High^Opt` = PTV_High minus Rectum; `zPTV_Low^Opt` = PTV_Low minus (PTV_High+1 cm); and two
   **dose-limiting annuli** `zDLA__Low`/`zDLA__High` built by margining the opt-PTV out 10 mm and subtracting
   the inner volumes. All geometry is Boolean algebra on `SegmentVolume` via `Margin()` and `Sub()`.
3. **Course + plan + beams** — reuses-or-creates course `AutoPlan`, removes/recreates plan `AutoPlanVMAT`
   (`AddExternalPlanSetup`). Isocenter is `ptv_high.CenterPoint` rounded to the nearest cm. Two
   `AddArcBeam(ExternalBeamMachineParameters("Truebeam","6X",600,"ARC",null), …)` arcs (CW 181→179, CCW
   179→181), each `FitCollimatorToStructure` to PTV_Low. Sets `PhotonVMATOptimization` model and prescription.
4. **Optimize + report** — adds point upper/lower objectives on the opt-PTVs and DLAs plus a
   `AddNormalTissueObjective`, runs `OptimizeVMAT(OptimizationOptionsVMAT(NoIntermediateDose,…))`, reports
   iterations / objective value, calls `OptimizeVMAT()` again (continue), `CalculateDose`, then reads
   `GetVolumeAtDose(Rectum, 65 Gy)` and `GetDoseAtVolume(PTV_High, 95%)`. `SaveModifications` at each stage.

## ESAPI surfaces
- **Structure ops:** `StructureSet.AddStructure("ORGAN", id)`, `RemoveStructure`, `Structure.SegmentVolume`,
  `Margin(mm)`, `Sub(...)`, `DicomType`, `CenterPoint`
- **Planning:** `Course.AddExternalPlanSetup`, `RemovePlanSetup`, `ExternalPlanSetup.AddArcBeam`,
  `Beam.FitCollimatorToStructure(FitToStructureMargins, …)`, `SetCalculationModel(PhotonVMATOptimization)`,
  `SetPrescription`
- **Optimization:** `OptimizationSetup.AddPointObjective(OptimizationObjectiveOperator, DoseValue, vol, prio)`,
  `AddNormalTissueObjective`, `OptimizeVMAT(OptimizationOptionsVMAT)` → `OptimizerResult`
- **Readout:** `GetVolumeAtDose`, `GetDoseAtVolume`; **Types:** `ExternalBeamMachineParameters`, `VVector`,
  `VRect<double>`, `GantryDirection`, `DoseValue`

## Reusability
The **opt-structure recipe** (target-minus-OAR cores + margin-and-subtract dose-limiting annuli) and the
**arc-build + objective-set + optimize** sequence are the liftable techniques — and the Tuple-based target map
is a clean idea for separating clinic IDs from planning logic. As written it's demo-grade: patient/course IDs
and the `"Truebeam"/"6X"/600/PO_15014` machine/model strings are literals, it relies on blocking `MessageBox`
prompts (unusable in batch), and it leans on a specific `z…^Opt` naming convention. The double `OptimizeVMAT`
call (options-form then arg-less continue) and model string `PO_15014` are version-sensitive — verify the
VMAT optimizer signature and model names for your Eclipse version. Strip the dialogs and externalize the
constants and it becomes a genuine batch VMAT starter generator.

## Idea sparks
- A reusable "optimization-structure builder" library: feed target/OAR roles + margins, emit the standard
  `^Opt` cores and dose-limiting annuli for any site.
- A batch auto-plan seeder: run this headless across a cohort to create first-pass VMAT plans for planner review.
- A nomenclature linter (step 1 alone) that audits a structure set against a TG-263/clinic standard before
  planning — pairs naturally with ESAP-09 (StructureIdFrequency).
