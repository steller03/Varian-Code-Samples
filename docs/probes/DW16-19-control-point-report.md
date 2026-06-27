# DW16-19 — A3_Plugin (control-point report)

| Field | Value |
|---|---|
| ID | DW16-19 |
| Solution | A3_Plugin |
| Source event | Developer Workshop 2016 — kata Advanced.3 |
| ESAPI version | v11 (declared good through 15.0) |
| Type | Binary plugin (`Execute(ScriptContext)`) |
| Reuse verdict | Liftable |

## Problem
A physicist reviewing a plan wants a quick structural fingerprint pulled straight from the control
points: how many beams, total MU, how many distinct gantry / collimator / table angles, how many jaw
configurations, and the control-point count. Useful for plan review, technique classification, and
spotting anomalies.

## Approach
It flattens every beam's `ControlPoints` into a single `List<ControlPoint>`, which lets all the
summaries be expressed as one-line LINQ over that flat list. Distinct beam count comes from
`Distinct()` on `Beam.Id`; total MU sums the distinct per-beam `Meterset.Value`; distinct
`GantryAngle`, `CollimatorAngle`, `PatientSupportAngle`, and `JawPositions` counts each fall out of
`Select().Distinct().Count()`; and the total control-point count is the list size. As a bonus it lists
the distinct (beam, jaw-position) pairs. Output is a tab-delimited `MessageBox`.

## ESAPI surfaces
- `ScriptContext.ExternalPlanSetup`, `ExternalPlanSetup.Beams`, `ExternalPlanSetup.Course` / `Patient`
- `Beam.ControlPoints` (`ControlPointCollection`), `ControlPoint.Beam`
- `ControlPoint.GantryAngle` / `CollimatorAngle` / `PatientSupportAngle` / `JawPositions`
- `Beam.Meterset.Value`

## Reusability
Pure read-only LINQ over the control-point model — fully liftable and version-stable, an ideal
building block. `DW16-20` (A3_StandAlone) is the standalone twin of this plugin (excluded from the
queue as a project-vs-standalone delta). Two small notes for reuse: `Distinct()` on `JawPositions`
relies on value-equality of the jaw struct, so verify it distinguishes the way you expect; and MU is
read via `Beam.Meterset.Value`, which is per-beam, hence the distinct-by-beam sum.

## Idea sparks
- Build a plan "fingerprint" string for QA comparison or duplicate-plan detection across a course.
- Classify technique automatically (3D vs IMRT vs VMAT) from control-point count and distinct-angle counts.
- Export the same aggregates to CSV across a cohort to audit jaw/angle/MU usage patterns.
