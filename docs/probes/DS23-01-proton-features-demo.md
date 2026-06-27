# DS23-01 — ProtonFeaturesDemo (end-to-end automated IMPT)

| Field | Value |
|---|---|
| ID | DS23-01 |
| Solution | ProtonFeaturesDemo |
| Source event | 22 Jul 2023 Developer Symposium |
| ESAPI version | v18 |
| Type | Standalone exe (writeable, `Application.CreateApplication`) |
| Reuse verdict | Adaptable |

## Problem
A physicist wants to build a modulated-scanning IMPT proton plan from nothing and exercise
**every** v18 proton automation surface in one place — beam/range-shifter geometry, proton calc-model
selection, robust optimization, RapidPlan, dose + uncertainty + delivery-dynamics calculation, a DECT
verification plan, and CSV export of spot/mesh/geometry data. It's the repo's reference implementation
for "what the v18 proton API can do, scripted start to finish."

## Approach
A single linear `Main` driven by four command-line args (patient / course / plan / structure-set IDs),
wrapped in Serilog logging and an optional `SaveAndPause` step-debugger (`App.SaveModifications()` then
`Console.ReadLine()`). After `OpenPatientById` + `BeginModifications`, it walks the full pipeline:
1. **Plan + beams** — `AddCourse`, `course.AddIonPlanSetup(sset, "Table")`, `SetTargetStructureIfNoDose`,
   `SetPrescription(35 fx, 2 Gy)`. Three beams via `plan.AddModulatedScanningBeam(ProtonBeamMachineParameters,
   snoutId, snoutPos, gantryAngle, couchAngle, target.CenterPoint)`, then per-beam `GetEditableParameters` /
   `ApplyParameters` to set the target structure and a pre-selected range shifter (`RS_5CM`, setting `IN`),
   plus proximal/distal/lateral target margins.
2. **Calc models** — `SetCalculationModel` for each `CalculationType` (ProtonVolumeDose `PCS_18`,
   ProtonOptimization/BeamDeliveryDynamics `NUPO_18`, DVH-estimation, post-processing, beamline-modifiers).
3. **Objectives + robustness** — clears existing objectives, adds point upper/lower + mean-dose objectives
   and a **proton NTO** (`AddProtonNormalTissueObjective`). Robust scenarios are the triple cross-product of
   `{RobustOptimizationUncertainty, RangeUncertainty} × {+3%,-3%} × {0, ±0.5 cm shift}` fed to
   `AddPlanUncertaintyWithParameters`.
4. **RapidPlan** — `CalculateDVHEstimates(modelId, targetDoseLevels, structureMatches)` with explicit
   model-structure↔plan-structure name maps; bails if `!Success`.
5. **Optimize + dose** — optional APT grid/GPU calc options, `SetOptimizationMode(MultiFieldOptimization)`,
   `CalculateBeamLine`, `OptimizeIMPT(new OptimizationOptionsIMPT(200, RestartOptimization))`,
   `PostProcessAndCalculateDose`, normalize so D98 = 95% via `PlanNormalizationValue`, recalc, then
   `CalculatePlanUncertaintyDoses` and `CalculateBeamDeliveryDynamics`.
6. **DECT + exports** — finds `DERHOZ\RHO` / `…\Z` images and builds `CreateDectVerificationPlan`. Exports
   three CSVs: per-spot energy/MU/(x,y,z) (MU = `spot.Weight × Meterset/lastCP.MetersetWeight`), target
   `MeshGeometry` node positions + triangle indices, and beam source/target coordinates.

## ESAPI surfaces
- **IonPlanSetup:** `AddIonPlanSetup`, `AddModulatedScanningBeam`, `SetTargetStructureIfNoDose`,
  `SetPrescription`, `SetCalculationModel`/`GetCalculationModel`, `SetCalculationOption`,
  `SetOptimizationMode(IonPlanOptimizationMode)`, `CalculateBeamLine`, `OptimizeIMPT(OptimizationOptionsIMPT)`,
  `PostProcessAndCalculateDose`, `CalculatePlanUncertaintyDoses`, `CalculateBeamDeliveryDynamics`,
  `CalculateDVHEstimates`, `AddPlanUncertaintyWithParameters`, `CreateDectVerificationPlan`, `GetDoseAtVolume`
- **IonBeam:** `GetEditableParameters` / `ApplyParameters` (`IonBeamParameters.PreSelectedRangeShifter1Id/Setting`,
  `TargetStructure`), `ProximalTargetMargin`, `DistalTargetMargin`, `LateralMargins`, `Meterset`,
  `IonControlPoints` → `FinalSpotList` (`spot.Weight`, `spot.Position`), `GetSourceLocation`, `IsocenterPosition`
- **OptimizationSetup:** `AddPointObjective`, `AddMeanDoseObjective`, `AddProtonNormalTissueObjective`,
  `RemoveObjective`/`RemoveParameter`
- **Types:** `ProtonBeamMachineParameters`, `CalculationType`, `PlanUncertaintyType`, `OptimizationOptionsIMPT`,
  `IonPlanOptimizationMode`, `VRect<double>`, `VVector`, `Structure.MeshGeometry`

## Reusability
This is the canonical proton recipe — the **beam-build → calc-models → objectives+NTO → robust scenarios →
RapidPlan → optimize → dose/uncertainty/delivery → verification → export** sequence is liftable as a
skeleton, and the robust-scenario cross-product and spot-MU conversion are the two reusable nuggets. It is
heavily pinned, though: every ID (machine `ProBeam_RH`, technique `MODULAT_SCANNING`, model strings `*_18`,
RapidPlan model, structure names, range shifter `RS_5CM`) is a literal, and the proton calc-model names are
v18-specific — re-validate the model strings and `CalculationType` enum members against your ESAPI version
before porting. Requires a proton machine, RapidPlan model, proton + robust-optimization licensing, and (for
the DECT branch) DECT-derived ρ/Z images. Pull args/IDs into config and this becomes a real batch IMPT builder.

## Idea sparks
- A robustness harness: drive `AddPlanUncertaintyWithParameters` from a clinic scenario table, then dump
  per-scenario DVH band extents to characterize plan robustness across a cohort.
- A spot-data exporter (the CSV block alone) feeding an external QA/leakage or delivery-time analysis tool.
- A proton auto-planner: pair the beam-build + RapidPlan + OptimizeIMPT core with a goal table to batch-create
  starting IMPT plans for review.
