# DW16-14 — MeanCTNumber (mean/SD of CT numbers inside a structure)

| Field | Value |
|---|---|
| ID | DW16-14 |
| Solution | MeanCTNumber (DW2016 kata Intermediate.7) |
| Source event | Developer Workshop 2016 — katas |
| ESAPI version | v11 (header: v11–15.0) |
| Type | Standalone exe (`Application.CreateApplication`) |
| Reuse verdict | Liftable |

## Problem
Compute the mean and standard deviation of CT numbers within a named RT structure. This is the basic
image-analysis primitive behind density audits — verifying a contour's tissue composition, QA of HU
overrides, or checking that an override region holds the expected value. It is also the catalogue's
only worked example of **iterating image voxels that fall inside a contour**.

## Approach
A console exe takes `args: id pw pt structure_set rtstruct` (passing `id == "null"` forces the
interactive `CreateApplication(null, null)` sign-in). It opens the patient by id, finds the matching
`StructureSet`, and calls `GetInterior(image, structure)`. That helper triple-loops the CT grid over
`image.XSize/YSize/ZSize`, converting each voxel index to patient coordinates
(`p = index·Res + image.Origin`), **trimming** by the structure's `MeshGeometry.Bounds` and then
testing `Structure.IsPointInsideSegment(p)` (commented "expensive"); for interior points it reads the
raw stored value via `image.GetVoxels(z, voxels[,])`. Mean is `voxels.Average()`; SD is
`sqrt(Σ(v-mean)²/(n-1))`. It calls `GC.Collect()` once per z-slice to dodge the script timeout, and
prints the two numbers plus elapsed time. Note the collected ints are **raw voxel values**, not
calibrated HU — true Hounsfield numbers need the CT calibration / display-value mapping.

## ESAPI surfaces
- `Application.CreateApplication`, `Patient.StructureSets`, `StructureSet.Image`
- `Image.XSize/YSize/ZSize`, `Image.XRes/YRes/ZRes`, `Image.Origin`, `Image.GetVoxels(int z, int[,])`
- `Structure.IsPointInsideSegment(VVector)`, `Structure.MeshGeometry.Bounds` (`Rect3D`)
- `VVector`

## Reusability
The reusable core is the **voxel-in-structure iteration**: bounds-trim, then `IsPointInsideSegment`,
then read the voxel — the canonical recipe for any per-voxel metric (dose-in-voxel, density stats,
simple radiomics). Lift `GetInterior` and swap the accumulation. Caveats before production: it walks
the **entire** image grid with an expensive point-in-segment test per voxel — restrict the loops to
the structure's bounding box (`MeshGeometry.Bounds`) instead, and hoist `GetVoxels(z, …)` out of the
inner x/y loop (it is re-fetched per voxel here). The `GC.Collect()`-per-slice is a timeout band-aid
that disappears once the loop is bounded. And calibrate raw voxel values to HU if you need true
density. All surfaces are current.

## Idea sparks
- HU-override QA: flag structures whose mean voxel value deviates from the expected override.
- Mean density per OAR feeding a proton stopping-power sanity check.
- Factor `GetInterior` into a shared "voxels inside structure" utility reused by every per-voxel
  analysis (dose, density, texture).
