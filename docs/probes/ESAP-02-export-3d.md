# ESAP-02 — Export3D (structures/dose/bolus -> portable 3D mesh + VTK volume)

| Field | Value |
|---|---|
| ID | ESAP-02 |
| Solution | Export3D |
| Source event | Eclipse Scripting API — projects |
| ESAPI version | v11 / v13 |
| Type | Binary plugin (Script.cs Execute) |
| Reuse verdict | Liftable |

## Problem
A physicist wants to inspect, share, or 3D-print Eclipse geometry outside the TPS: contoured
structures, isodose surfaces, and especially a bolus you intend to physically print. ESAPI keeps this
geometry locked behind its object model; this script pours it into standard mesh/volume files that
MeshLab, ParaView, or a slicer can open.

## Approach
The whole job rides on ESAPI already exposing a triangulated surface per structure — the script never
contours or marching-cubes anything itself; it just transcodes `MeshGeometry3D` (WPF
`System.Windows.Media.Media3D`) into file formats.

- **Entry (`Execute`)** — requires a 3D `StructureSet`, builds an output folder under `%TEMP%\Export3D\<patientId>`, then fans out to three exporters. If a `PlanSetup.Dose` exists it forces `DoseValuePresentation.Absolute` first.
- **`ExportStructures`** — iterates `ss.Structures`, skips any without `HasSegment`, and writes each `structure.MeshGeometry` (colored with `structure.Color`) to an **ASCII PLY** via `SaveTriangleMeshToPlyFile`. Per-vertex RGBA is written, alpha hardcoded to 0.6.
- **`ExportDose`** — dumps the dose grid as an **ASCII VTK STRUCTURED_POINTS** volume (`SaveDoseOrImageToVTKStructurePoints`), then walks `dose.Isodoses`, writing each `isodose.MeshGeometry` as a colored PLY. The VTK writer reads voxels plane-by-plane with `dose.GetVoxels(z, buffer)`, derives spacing signs from `XDirection`/`YDirection` and a hand-rolled cross-product `GetZDirection`, and rescales dose to 0–100 against a full-volume `FindMaxValue` pass. The same method handles `Image` (unscaled UInt16) — only one of dose/image is non-null.
- **`ExportBolus`** — same structure loop but filters `DicomType == "BOLUS"` and writes a *normals-bearing* PLY (overload that calls `CalculateVertexNormal`, averaging adjacent face normals) suitable for Poisson reconstruction. An STL writer (`SaveTriangleMeshtoStlFile`, ASCII `solid`/`facet normal`/`outer loop`) is present but commented out — the intended 3D-print path.

Geometry helpers `CalculateSurfaceNormal` (face cross product) and `CalculateVertexNormal` (averaged, O(n²) over triangle indices) are plain math, no ESAPI.

## ESAPI surfaces
- Scope: `ScriptContext.Patient/StructureSet/PlanSetup`, `PlanSetup.Dose`, `DoseValuePresentation.Absolute`
- Structures: `StructureSet.Structures`, `Structure.HasSegment/Id/Color/DicomType`, `Structure.MeshGeometry`
- Dose/isodose: `Dose.Isodoses`, `Isodose.MeshGeometry/Color/Level`, `Dose.XSize/YSize/ZSize`, `XRes/YRes/ZRes`, `Origin`, `XDirection/YDirection`, `Dose.GetVoxels(z, int[,])`
- Image (parallel path): `Image.XSize/.../XDirection`, `Image.GetVoxels`
- Types: `VVector` (.x/.y/.z), `Color`
- Non-ESAPI plumbing: `System.Windows.Media.Media3D.MeshGeometry3D` (`Positions`/`TriangleIndices`), `Point3D`, `Vector3D`, `Point3DCollection`, `Int32Collection`; `System.IO` StreamWriter

## Reusability
Highly liftable, and the prize is small and self-contained. `SaveTriangleMeshToPlyFile` and
`SaveTriangleMeshtoStlFile` take a bare `MeshGeometry3D` — copy them into any plugin and you have a
structure/isodose/bolus-to-PLY-or-STL exporter, version-agnostic because `Structure.MeshGeometry`
and `Isodose.MeshGeometry` are stable across v11–v16. To actually print a bolus, just uncomment the
STL call in `ExportBolus`. Watch-outs a physicist must handle: PLY/STL coordinates are written in raw
ESAPI mm (DICOM frame) with no recentering, so slicers may place the part oddly; ASCII float output
(`"e"` format) bloats files for fine meshes — switch to binary PLY/STL for large structures. The VTK
dose writer rescales dose to 0–100 (lossy) and infers axis sign flips manually rather than using a
full orientation matrix, so it assumes near-axis-aligned acquisition — fine for standard HFS scans,
fragile otherwise. `GetVoxels` signature and the `int[,]` buffer are unchanged in modern ESAPI, so
the VTK path still compiles.

## Idea sparks
- Bolus-to-printer pipeline: uncomment STL, add binary output, and feed straight into a slicer for in-house bolus/immobilization printing.
- Cohort surface export: drive `SaveTriangleMeshToPlyFile` headlessly over a patient set to build a mesh library for shape/auto-segmentation QA in MeshLab/ParaView.
- Reuse the `MeshGeometry3D` walker to compute surface area / volume / centroid metrics from structures without touching DVH machinery.
