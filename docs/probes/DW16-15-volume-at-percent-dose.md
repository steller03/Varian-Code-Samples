# DW16-15 — VolumeAtPercentDose (isodose volume by brute-force voxel counting)

| Field | Value |
|---|---|
| ID | DW16-15 |
| Solution | VolumeAtPercentDose |
| Source event | Developer Workshop 2016 (kata intermediate.8) |
| ESAPI version | v11 (header: 11 / 13 / 13.5 / 13.6 / 13.7 / 15.0) |
| Type | Binary plugin (`Execute(ScriptContext)`) |
| Reuse verdict | Illustrative |

## Problem
Find the total volume of the dose grid receiving at least a given percent of the prescription (here 50%) — i.e., the volume enclosed by an isodose surface, independent of any structure. Useful for low-dose-bath / integral-dose questions where there's no contour to query against.

## Approach
The instructive part is that it does **not** use `GetVolumeAtDose` (which needs a structure); it integrates the 3D dose grid by hand. It sets `plan.DoseValuePresentation = Absolute`, grabs `plan.Dose`, and computes the threshold as `TotalDose.Dose * percent/100`. Then it raster-scans the dose matrix: nested loops over z (slices) and y (rows) build a line from `Dose.Origin + YDirection*y + ZDirection*z` to the far x edge, and `Dose.GetDoseProfile(start, stop, buffer)` samples one x-row of doses into a preallocated `double[]`. Each `profilePoint.Value >= threshold` increments a counter; final volume = `XRes*YRes*ZRes*count/1000` cm³. The reusable idea is the geometry math: stepping `Origin` by `YDirection*YRes` / `ZDirection*ZRes` and sampling rows with `GetDoseProfile` to traverse the entire matrix.

## ESAPI surfaces
- `ScriptContext.Patient` / `.PlanSetup`
- `PlanSetup.IsDoseValid`, `PlanSetup.TotalDose`, `PlanSetup.DoseValuePresentation`, `PlanSetup.Dose`
- `Dose.XSize/YSize/ZSize`, `XRes/YRes/ZRes`, `Origin`, `XDirection/YDirection/ZDirection`
- `Dose.GetDoseProfile(VVector start, VVector stop, double[] preallocated)` → `DoseProfile` (iterate `ProfilePoint.Value`)
- `VVector` arithmetic; `DoseValue.Dose`

## Reusability
Illustrative, not liftable as-is. Its real value is teaching the `Dose` geometry API (origin + direction vectors + per-axis resolution) and row-wise `GetDoseProfile` sampling — that traversal pattern reuses for any voxel-level scan (gradient, gamma, masking). But the algorithm is O(slices × rows) profile calls and approximate (counts voxels whose sampled centre exceeds threshold, no partial-volume), so it's slow and coarse versus the right tools: for a structure use `GetVolumeAtDose`; for a whole-grid isodose volume in v15+, read the voxel array directly (`Dose.GetVoxels` + `VoxelToDoseValue`) instead of thousands of `GetDoseProfile` calls. Watch the loop-bound math (`< ZSize*ZRes` stepping by `ZRes`) for an off-by-one at the last plane.

## Idea sparks
- Reuse the Origin + direction raster as a generic "dose-grid visitor" for integral dose, low-dose-bath volume, or a custom isodose metric.
- Gate the same scan with `Structure.IsPointInsideSegment` to get isodose volume *within* a region without building a Boolean structure.
- Port it to `Dose.GetVoxels` for a ~100× faster, exact version and keep both as a teaching benchmark.
