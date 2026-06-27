# Eclipse Scripting API — Projects (ESAP)

The `projects/` folder is Varian's reference set of fuller ESAPI sample applications — larger than the
single-concept katas, each one a working solution to a recurring physics-automation need. The spread is
broad: database-wide data mining (patient reports, structure-naming histograms), DVH and dose export (batch
CSV, web DVH, 3D meshes), DICOM retrieval via DCMTK, a configurable plan-quality-metric engine with
HTML reporting, proton RBE reporting, 1D profile/gamma analysis, and two developer-tooling standouts — a
standalone plugin debug harness and an interactive C# scripting console for ESAPI.

| ID | Solution | Path | Ver | Type | Category | Verdict | Problem | Score | Probe |
|---|---|---|---|---|---|---|---|---|---|
| ESAP-01 | DataMining | Eclipse Scripting API/projects/DataMining | v13 | Standalone exe | ARIA & database query (Reporting & documents) | Liftable | Iterate all ARIA patients and write a treatment report per patient | 4 | |
| ESAP-02 | Export3D | Eclipse Scripting API/projects/Export3D | v13 | Binary plugin | Structure & contour ops (DICOM I/O & interop) | Liftable | Export structures, dose and bolus as 3D meshes for external viewers | 4 | |
| ESAP-03 | ExportBatchDVHs | Eclipse Scripting API/projects/ExportBatchDVHs | v13.5 | Standalone exe | DVH & dose metrics | Liftable | Batch-export DVH curves across plans for offline analysis | 4 | |
| ESAP-04 | GenerateWebDVH | Eclipse Scripting API/projects/GenerateWebDVH | v13 | Binary plugin | DVH & dose metrics (Reporting & documents) | Adaptable | Generate an interactive web/HTML DVH chart for selected structures | 3 | |
| ESAP-05 | GetDicomCollection | Eclipse Scripting API/projects/GetDicomCollection | v13 | Binary plugin | DICOM I/O & interop | Adaptable | Retrieve a plan's DICOM objects from ARIA via DCMTK C-MOVE | 4 | |
| ESAP-06 | PlanQualityMetrics | Eclipse Scripting API/projects/PlanQualityMetrics | v11 | Binary plugin | Plan QA & verification (Reporting & documents) | Liftable | Evaluate configurable plan-quality metrics and emit HTML pass/fail report | 5 | flag |
| ESAP-07 | PluginScriptExample / PluginTester | Eclipse Scripting API/projects/PluginTester | v13.5 | Standalone exe | Plugin scaffolding & UI | Adaptable | Debug and run binary plugins standalone outside Eclipse | 5 | flag |
| ESAP-08 | RBEReport | Eclipse Scripting API/projects/RBEReport | v13 | Binary plugin | Research & algorithmic (Reporting & documents) | Adaptable | Generate a proton radiobiological-effect PDF report and post to ARIA | 4 | |
| ESAP-09 | StructureIdFrequency | Eclipse Scripting API/projects/StructureIdFrequency | v13.5 | Standalone exe | Structure & contour ops (ARIA & database query) | Liftable | Mine all patients for structure-naming frequency to drive TG-263 cleanup | 4 | |
| ESAP-10 | Uab.VMS.Console | Eclipse Scripting API/projects/Uab.VMS.Console | unknown | Standalone exe | Plugin scaffolding & UI | Adaptable | Interactive C# REPL console for live ESAPI scripting with code completion | 5 | flag |
| ESAP-11 | ProfileSamples | Eclipse Scripting API/projects/ProfileSamples | v15 | Binary plugin | DVH & dose metrics (Research & algorithmic) | Adaptable | Extract 1D dose/depth profiles and run unscaled gamma analysis | 4 | |

## Standouts
- **ESAP-06 (PlanQualityMetrics)** — configurable QUANTEC-style metric engine with XML/XSLT HTML reporting; a near-clinical plan-check pattern.
- **ESAP-10 (Uab.VMS.Console)** — interactive ESAPI REPL with code completion; uniquely lowers the barrier to live exploration.
- **ESAP-07 (PluginTester)** — standalone harness to run/debug binary plugins outside Eclipse, a major dev-loop accelerator.

## Coverage
11 units catalogued = 10 `.sln` solutions + the standalone `ProfileSamples` (a `.csproj` with its own
`Script.cs` Execute entry and supporting source, no `.sln`). `PluginTester/PluginScriptExample.sln` is
counted as ONE unit (ESAP-07) although it builds two projects — `PluginScriptExample` (the demo plugin)
plus `PluginTester` (the standalone debug host) — together forming the plugin-testing harness.

The three `Export3D` / `GenerateWebDVH` / `GetDicomCollection` solutions compile their source from the
sibling `../../plugins/` directory; here each is treated as its `.sln` project unit. Loose `.cs` files
inside the catalogued solution folders (`DataMining.cs`, `ExportBatchDVHs.cs`, `StructureIdFrequency.cs`,
`PlanQualityMetrics/*.cs`, `RBEReport/*.cs`, etc.) are sources or single-file twins of their same-named
`.sln`, not separate units.

Skipped: `Eclipse Scripting API/projects/DvhLookups/` — a `.csproj`-only shell with no `.cs` source; the
actual `DvhLookups.cs` lives under `Eclipse Scripting API/plugins/` and is catalogued in the ESPL shard,
so cataloguing it here would double-count.
