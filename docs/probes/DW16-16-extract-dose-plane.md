# DW16-16 — ExtractDosePlane (planar dose → CSV)

| Field | Value |
|---|---|
| ID | DW16-16 |
| Solution | ExtractDosePlane |
| Source event | Developer Workshop 2016 — kata Intermediate.9 |
| ESAPI version | v11 (declared good through 13.6 / 13.7 / 15.x) |
| Type | Binary plugin (`Execute(ScriptContext)`) |
| Reuse verdict | Liftable |

## Problem
A physicist doing IMRT/VMAT QA wants the calculated dose over a flat plane exported as a
grid they can open in Excel or feed to a phantom/array comparison (MapCheck, MatriXX). The
kata extracts the planar dose of a verification plan as a row × column CSV bounded by two
user-placed marker points.

## Approach
The user pre-places two point structures — `TopLeft` and `BottomRight` — in the structure set to
define the scan rectangle. The script pulls them by Id, reads their `CenterPoint`, and derives the
other two corners by mixing coordinates (`topRight = {bottomRight.x, topLeft.y, topLeft.z}`, etc.).
It then rasterizes a fixed 255 × 255 grid: for each row it computes a constant-z start/end vector and
calls `plan.Dose.GetDoseProfile(start, end, buffer)` to sample a 1-D dose line across the plane,
writing each `ProfilePoint.Value` into a CSV cell (rows = z, columns = x, with cm coordinates as the
header row/lead column). The file is written to `c:\temp\doseplane.csv` and launched via
`Process.Start`. Note the plane is axial-ish (x–z extent at fixed y) and the grid count is hard-coded
to what Excel historically tolerated, not to the dose grid resolution.

## ESAPI surfaces
- `ScriptContext.PlanSetup`, `ScriptContext.StructureSet`
- `PlanSetup.IsDoseValid`, `PlanSetup.Dose`
- `PlanningItemDose.GetDoseProfile(VVector start, VVector stop, double[] preallocatedBuffer)` → `DoseProfile`
- `DoseProfile` enumerates `ProfilePoint { Value, Position }`
- `Structure.CenterPoint`, `VVector`, `VVector.Distance`

## Reusability
The `GetDoseProfile` row-scan idiom is the liftable core and still current — it is the supported way
to sample dose along arbitrary lines. To productionize: take the plane geometry from real arguments
(plane orientation + spacing) instead of two manually placed markers; size the grid to the dose
matrix or a requested resolution rather than a magic 255; replace the hard-coded `c:\temp` path and
the `Process.Start` auto-launch. `GetDoseProfile` interpolates and needs a caller-allocated buffer
sized to the sample count — that contract is unchanged across versions. Marker-point lookup by exact
Id is brittle; a modern version would accept an isocenter/plane spec directly.

## Idea sparks
- Generalize into a "dose plane at isocenter for beam N" exporter (coronal/sagittal/axial) for film
  or detector-array comparison, emitting native MapCheck/MatriXX formats as the kata title hints.
- Pair with a gamma routine (cf. ESAP-11 ProfileSamples) to auto-compare exported planar dose
  against measured QA arrays.
- Reuse the row-scan to build dose-difference heatmaps between two plans or two algorithms.
