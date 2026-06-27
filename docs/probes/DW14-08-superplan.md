# DW14-08 — Superplan (scripted plan: fields → objectives → optimize → LMC → dose)

**Cluster 7 delta** — exemplar [DW18-06 AutoPlan](DW18-06-autoplan.md) (see also
[DW18-04 AutomatedPlanningDemo](DW18-04-automated-planning-mco.md) for the full MCO pipeline).

- **Problem:** create a complete external plan from a structure set entirely in script — course, fields,
  optimization objectives, leaf motion, and final dose — the earliest/simplest end-to-end planning kata.
- **Differs from the exemplar:** where DW18-06 fits MLC beams and W1804-01 does opposed AP/PA, Superplan
  uses **five fixed `AddStaticBeam` 10×10 cm fields** at `Round(360/n)` gantry angles (no jaw/MLC fitting)
  and is the only cluster-7 member that scripts the **optimization objectives** explicitly:
  `OptimizationSetup.AddPointObjective` for PTV (lower 49.5 Gy / upper 52 Gy) and Rectum (upper 20 Gy @
  40 %), then `Optimize(30)` → `CalculateLeafMotions()` → `CalculateDose()`. On dose-calc failure it dumps
  each beam's `CalculationLogs` to a temp file and opens it. Requires structures named exactly
  `BODY`/`PTV`/`Rectum1`.
- **Surfaces it adds:** `OptimizationSetup.AddPointObjective` (+`OptimizationObjectiveOperator`),
  `ExternalPlanSetup.Optimize` / `CalculateLeafMotions` / `CalculateDose`,
  `UniqueFractionation.SetPrescription`, `AddStaticBeam`, and `Beam.CalculationLogs` /
  `BeamCalculationLog.MessageLines` for failure diagnostics.
- **Reuse note:** a good minimal template for the **objective-setup → optimize → LMC → dose** chain; the
  `AddPointObjective` block and the calc-log dump are the liftable bits. Hardcoded machine `Varian 23EX`
  and structure ids need porting. Superseded by DW18-04/RS15-01 for any production use. Verdict
  Illustrative (the chain is liftable).
