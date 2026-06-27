# DW16-17 — Intermediate_10 (collimator/couch clearance via mesh geometry)

| Field | Value |
|---|---|
| ID | DW16-17 |
| Solution | Intermediate_10 |
| Source event | Developer Workshop 2016 — kata Intermediate.10 |
| ESAPI version | v11 (declared good through 15.0) |
| Type | Standalone exe (`Application.CreateApplication`) |
| Reuse verdict | Adaptable |

## Problem
Collision/clearance checking: for each beam, how close does the treatment head come to the patient's
body and to the couch at its gantry and table angles? This is a real safety question for non-coplanar
and SRS setups, and ESAPI exposes enough geometry to estimate it without an external CAD package.

## Approach
The standalone app opens a hard-coded patient/course/plan and pulls the `BODY` and `CouchSurface`
structures. The key move is `Structure.MeshGeometry.Positions` — the surface mesh vertices as
`Point3D`s. Isocenter-to-table clearance is the minimum distance from the beam isocenter over all
couch vertices. For each beam it models the collimator face center as a single point 35 cm from
isocenter along the beam axis, projecting that offset into patient coordinates from the gantry and
table angles (`FaceCenter = origin + 350·[cos(table)·sin(gantry), −cos(gantry), sin(table)·sin(gantry)]`,
with angles wrapped to ±180°). It then takes the minimum distance from that face point to every body
vertex and every couch vertex, tabulating body/couch clearance per beam (mm → cm).

## ESAPI surfaces
- `Application.CreateApplication`, `Application.OpenPatientById`, `Patient.Courses`, `Course.ExternalPlanSetups`
- `ExternalPlanSetup.StructureSet` / `Beams`, `Structure.MeshGeometry` (`MeshGeometry3D.Positions` → `System.Windows.Media.Media3D.Point3D`)
- `Beam.IsocenterPosition` (`VVector`), `Beam.ControlPoints` → `GantryAngle`, `PatientSupportAngle`

## Reusability
The liftable gem is using `Structure.MeshGeometry.Positions` for brute-force nearest-vertex distance —
clearance estimation with no external geometry library. It is `Adaptable` rather than `Liftable`
because the model is coarse: the head is approximated as one point at a fixed 35 cm, with no extended
collimator body, no gantry/couch sag, and no accessories or immobilization; the patient/course/plan
IDs are hard-coded; and the gantry/table → Cartesian projection assumes a specific IEC convention
worth re-deriving for your geometry. `MeshGeometry` is still available; for finer contours consider
`Structure.GetContoursOnImagePlane`. The min-over-all-vertices loop is O(N) per beam but fine in
practice.

## Idea sparks
- Sweep a full gantry × couch grid to produce a collision map for non-coplanar / SRS pre-checks.
- Add fixed couch rails or immobilization devices as extra meshes to clear against.
- Replace the single face point with a CAD mesh of the actual treatment head for a true clearance check.
