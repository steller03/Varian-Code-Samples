# DW18-04 — AutomatedPlanningDemo (auto-planning + Multicriteria Optimization)

| Field | Value |
|---|---|
| ID | DW18-04 |
| Solution | AutomatedPlanningDemo (AutoPlanningWithMCO) |
| Source event | Developer Workshop 2018 |
| ESAPI version | v15.6 |
| Type | Standalone exe (writeable, `Application.CreateApplication`) |
| Reuse verdict | Adaptable |

## Problem
The v15.6 evolution of the prostate auto-planning demo (cf. RS15-01): same prescription→geometry→
DVH-estimate→optimize→dose→report→QA pipeline, **plus a Multicriteria Optimization (MCO) trade-off
exploration stage** driven entirely from script. It's the reference for automating ESAPI's
trade-off / Pareto navigation API and turning the result into a deliverable plan.

## Approach
The orchestration is the RS15-01 skeleton with two changes — Windows-auth sign-in
(`CreateApplication()`), the demo patient `RapidPlan-01` / structure set `Prost30Oct2012`, and an
inserted `RunMCO(patient, courseId, planId)` call after optimization and before final dose calc. The
MCO stage is the novel content and exercises the `PlanSetup.TradeoffExplorationContext` surface end to
end:
1. Copy the optimized plan (`Course.CopyPlanSetup`) into `MyMCOPlanV1` so MCO runs on a duplicate.
2. Inspect readiness (`HasPlanCollection`, `TradeoffObjectives`), pick a trade-off structure from
   `TradeoffStructureCandidates`, and `AddTradeoffObjective`.
3. `CreatePlanCollection(false, TradeoffPlanGenerationIntermediateDoseMode.NotUsed)` to generate the
   Pareto plan collection, then read per-objective cost / lower / upper limits and current DVHs
   (`GetObjectiveCost`, `GetObjectiveLowerLimit/UpperLimit`, `GetStructureDvh`, `CurrentDose`).
4. **Navigate** the Pareto surface: move an upper restrictor halfway between current cost and the
   upper limit (`SetObjectiveUpperRestrictor`), set an objective cost (`SetObjectiveCost`), re-read the
   resulting DVHs to show the trade-off effect.
5. `ApplyTradeoffExplorationResult` then `CreateDeliverableVmatPlan(false)` to bake the navigated
   point into a deliverable plan.
Everything is `Trace.WriteLine`-instrumented. After MCO it calculates dose, normalizes, writes the SVG
DVH + `report.xml` scorecard, and offers per-field + "All fields" verification plans, identical to
RS15-01. Output paths are `C:\Temp\dvh_mco.svg` / `C:\Temp`.

## ESAPI surfaces
- **MCO (the differentiator):** `PlanSetup.TradeoffExplorationContext` → `HasPlanCollection`,
  `CanCreatePlanCollection`, `TradeoffStructureCandidates`, `AddTradeoffObjective`,
  `CreatePlanCollection(bool, TradeoffPlanGenerationIntermediateDoseMode)`, `TradeoffObjectives`,
  `GetObjectiveCost` / `GetObjectiveLowerLimit` / `GetObjectiveUpperLimit`,
  `SetObjectiveUpperRestrictor` / `SetObjectiveCost`, `TargetStructures`, `GetStructureDvh`,
  `CurrentDose`, `ApplyTradeoffExplorationResult`, `CreateDeliverableVmatPlan(bool)`
- `Course.CopyPlanSetup`
- Plus the full RS15-01 set (geometry, `CalculateDVHEstimates`, `Optimize`, `CalculateDose`,
  normalization, verification plans) — see that probe.

## Reusability
The MCO block is the reason to read this file: it's a rare worked example of scripting trade-off
exploration, and the **inspect → create-collection → navigate-by-restrictor → apply → make-deliverable**
sequence is the liftable recipe. As written it's demo-grade — it grabs `TradeoffStructureCandidates.
First()` and moves a restrictor to an arbitrary halfway point rather than toward a clinical goal; a
real tool would choose objectives and restrictor targets from DVH constraints. All the
clinic-specific constants and licensing caveats from RS15-01 apply, now pinned to v15.6 (algorithm
strings `… 15.6.03`). MCO requires the trade-off/MCO license and a model that supports it; verify the
`TradeoffExplorationContext` API shape against your ESAPI version, as it evolved after 15.6.

## Idea sparks
- A goal-driven MCO navigator: instead of halfway restrictor moves, drive `SetObjectiveUpperRestrictor`
  from a table of OAR constraints until met, then `CreateDeliverableVmatPlan`.
- Batch trade-off studies: run `CreatePlanCollection` across a cohort and log Pareto extents per
  structure to characterize achievable OAR sparing.
- Diff tool: compare pre-MCO vs navigated DVHs (`GetStructureDvh`) to quantify the sparing a given
  trade-off buys.
