# Eclipse Scripting API — Plugins (ESPL)

A loose collection of standalone single-file ESAPI plugin scripts (no Visual Studio solution),
each dropped into Eclipse's scripting folder to solve one focused problem: an interactive DVH
lookup tool, a 3D structure/dose mesh exporter for external viewers and 3D printing, a
browser-rendered DVH chart, and a DCMTK-driven DICOM C-MOVE retrieval helper. Together they
illustrate the early single-file plugin pattern (`Execute(ScriptContext)` / `Execute(ScriptContext, Window)`)
across DVH metrics, geometry export, web reporting, and DICOM interop.

| ID | Solution | Path | Ver | Type | Category | Verdict | Problem | Score | Probe |
|---|---|---|---|---|---|---|---|---|---|
| ESPL-01 | DvhLookups | Eclipse Scripting API/plugins/DvhLookups.cs | v11 | Script (single-file) | DVH & dose metrics | Liftable | Interactively look up dose-at-volume and volume-at-dose for a structure | 3 | → probes/ESPL-01-dvh-lookups.md |
| ESPL-02 | Export3D | Eclipse Scripting API/plugins/Export3D.cs | v11 | Script (single-file) | Reporting & documents (Image & registration) | Adaptable | Export structures, dose and isodoses to VTK/PLY meshes for external viewing or 3D printing | 4 | → probes/ESAP-02-export-3d.md (twin of ESAP-02) |
| ESPL-03 | GenerateWebDVH | Eclipse Scripting API/plugins/GenerateWebDVH.cs | v11 | Script (single-file) | DVH & dose metrics (Reporting & documents) | Illustrative | Render selected-structure DVHs as a browser HTML/JavaScript chart | 2 | → probes/ESPL-03-generate-web-dvh.md |
| ESPL-04 | GetDicomCollection | Eclipse Scripting API/plugins/GetDicomCollection.cs | v11 | Script (single-file) | DICOM I/O & interop | Adaptable | Generate and run a DCMTK C-MOVE to retrieve a plan's CT, structures and dose | 4 | → probes/ESAP-05-get-dicom-collection.md (twin of ESAP-05) |

## Standouts
- **ESPL-04 (GetDicomCollection)** — scripts the VMS DICOM DB Daemon via DCMTK to pull a full plan dataset, a real interop workflow.
- **ESPL-02 (Export3D)** — exports structure/dose/isodose geometry to VTK/PLY/STL for visualization and 3D printing.

## Coverage
4 units found — 4 standalone single-file plugin scripts, no `.sln` present in this folder.
One row per script: `DvhLookups.cs`, `Export3D.cs`, `GenerateWebDVH.cs`, `GetDicomCollection.cs`.
All 4 are catalogued. Nothing skipped. Note: same-named projects exist under
`Eclipse Scripting API/projects` but that is a separate folder catalogued in its own shard.
