# ESAP-11 — ProfileSamples (1D dose/depth profiles + unscaled gamma)

| Field | Value |
|---|---|
| ID | ESAP-11 |
| Solution | ProfileSamples |
| Source event | Eclipse Scripting API — projects |
| ESAPI version | v15 |
| Type | Binary plugin (`Script.cs` `Execute`) |
| Reuse verdict | Adaptable |

## Problem
A physicist commissioning or QAing a beam model needs to pull 1D dose lines out of Eclipse — a
lateral/transverse profile across the field, a percent-depth-dose (PDD) along the beam axis — and
then compare a calculated profile against measured points to judge agreement. This sample harvests
those profiles in proper gantry-relative geometry and supplies two comparison operators (a 1D gamma
surrogate and a point dose-difference) so a calculated profile can be scored against measured data.

## Approach
Sampling is funneled through `PlanningItemDose.GetDoseProfile(start, stop, double[] buffer)`, which
interpolates dose along the line and writes into a caller-preallocated buffer whose length sets the
sample count (`Math.Ceiling(|stop - start| / stepSizeInmm)`). `Profile.getBeamDoseProfile` takes a
direction in *gantry* coordinates, scales it to unit length, builds symmetric start/stop endpoints
about isocenter (optionally offset toward the source), then rotates them into DICOM patient
coordinates via `Helpers.GantryToDICOM` (a RotateY-by-gantry, RotateZ-by-couch, axis-swap, plus
isocenter translation) before sampling `beam.Dose`. The depth-dose variant
(`getBeamDepthDoseProfileAlongBeamAxis`) instead derives the beam-axis direction from
`beam.GetSourceLocation`, then clips the line to the BODY by walking a `Structure.GetSegmentProfile`
to find first entry / last exit, so the PDD only spans patient anatomy.

Comparison is built around an `IDifferenceCalculator` strategy. Profiles are first *flattened* to
`double[][]` of `{distance-from-start, doseValue}`. `Helpers.distanceVec` sorts measured points by
position, marches the profile index forward once, and for each measurement calls the chosen
calculator. `PointDifference` linearly interpolates the calculated dose at the measurement abscissa
and returns measured − interpolated (NaN if outside the segment). `Unscaled1DGamma` is the headline
move: for each measurement it scans a ±N-point neighborhood and, treating each profile segment as a
line in the (distance, dose) plane, computes the true Euclidean point-to-segment distance via scalar
projection (clamping the projection to the segment endpoints). It is "unscaled" because the classic
gamma normalizes the distance and dose-difference axes by the DTA and dose-difference criteria before
combining — here both axes are taken in raw units with no per-criterion scaling, so it is a geometric
nearest-point distance rather than a dimensionless gamma index. The file also includes a profile-scan
DVH (`DVH.StructureDVH`) that rasterizes a structure with dose profiles plus `GetSegmentProfile`
masks, supporting a pluggable `IDoseValueConverter` (e.g. EQD2) — illustrative of the profile idiom
but not the core of this probe.

## ESAPI surfaces
- `Beam.Dose` / `PlanningItemDose.GetDoseProfile(VVector start, VVector stop, double[] buffer)` → `DoseProfile`
- `DoseProfile` / `ProfilePoint { Value, Position }`; `Dose.DoseMax3D`, `Dose.XRes/YRes/ZRes`
- `Image.GetImageProfile(...)` → `ImageProfile` (parallel image-profile sampling through isocenter)
- `Structure.GetSegmentProfile(start, stop, BitArray)` → `SegmentProfilePoint { Value, Position }`; `Structure.MeshGeometry.Bounds`, `Structure.Volume`
- `Beam.ControlPoints` (`GantryAngle`, `PatientSupportAngle`), `Beam.IsocenterPosition`, `Beam.GetSourceLocation(gantryAngle)`
- `VVector` (`ScaleToUnitLength`, `Length`, `ScalarProduct`, operator overloads), `PlanSetup.DoseValuePresentation`

## Reusability
The valuable, liftable part is pure C# with zero ESAPI dependency: `Unscaled1DGamma` (point-to-segment
distance via scalar projection), `PointDifference` (segment-interpolated dose diff), the
flatten/unflatten helpers, and the single-pass `distanceVec` matcher all operate on `double[]`/`double[][]`
and drop straight into any profile-comparison tool fed by film, diode array, or water-tank data. The
coordinate math (`GantryToDICOM`/`DICOMToGantry`, RotateY/RotateZ, CrossProduct) is also portable and
useful anywhere you need gantry↔DICOM transforms. ESAPI-bound is only the sampling layer
(`GetDoseProfile`/`GetSegmentProfile`/`GetImageProfile`), which is current and unchanged through v15 —
the preallocated-buffer contract still holds. Caveats: the unscaled gamma is explicitly *not* a
normalized gamma index (rename or add DTA/dose-difference scaling before calling it "gamma" in a
report); `Plane.OrthogonalDoseCrossSection` is self-described as "tried not tested" and has a suspect
`end` endpoint (`xDir * 0.5` without the `xSize` factor); `Script.cs` hard-codes structure Ids
(`BODY`, `CTV`, `Plan2`) and dumps to a Matlab path on a developer's machine, so the entry point is
demo scaffolding to be replaced.

## Idea sparks
- Drop the unscaled-distance/point-difference engine behind a real normalized 1D gamma (scale each
  axis by DTA and %dose-difference) for measured-vs-TPS commissioning profile QA.
- Reuse `getBeamDepthDoseProfileAlongBeamAxis` + BODY clipping as a PDD extractor that exports
  TPS PDDs for side-by-side comparison against water-tank scans.
- Pair the flatten/`distanceVec` matcher with array-detector (MapCheck/MatriXX) exports — or with
  ESAP DW16-16's planar dose CSV — to auto-score calculated vs measured lines.
