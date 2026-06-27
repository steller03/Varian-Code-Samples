# DW16-08 — DVHExtract (one structure's cumulative DVH → CSV)

| Field | Value |
|---|---|
| ID | DW16-08 |
| Solution | DVHExtract |
| Source event | Developer Workshop 2016 (kata intermediate.1) |
| ESAPI version | v11 (header: 11 / 13 / 13.5 / 13.6 / 13.7 / 15.0) |
| Type | Binary plugin (`Execute(ScriptContext)`) |
| Reuse verdict | Liftable |

## Problem
Get the full dose-volume curve for one organ out of Eclipse and into a file you can open in Excel or feed to an external analysis. The kata's narrow ask: extract the Bladder DVH for the loaded plan and write it as CSV.

## Approach
Guard `PlanSetup` and `StructureSet`; find `Bladder` by id in `StructureSet.Structures`. Pull the curve with `GetDVHCumulativeData(bladder, DoseValuePresentation.Absolute, VolumePresentation.Relative, 0.1)` (0.1-unit dose bins). Open a `StreamWriter` to `c:\temp\bladder_dvh-{user}.csv`, write a `Dose,Volume` header, then iterate `dvh.CurveData` writing `pt.DoseValue.Dose, pt.Volume` per `DVHPoint`; a `MessageBox` confirms the path. That's the whole recipe: resolve structure → `GetDVHCumulativeData` → walk `CurveData` → CSV. (It also shows `Structure.Volume` in a confirmation box.)

## ESAPI surfaces
- `ScriptContext.PlanSetup` / `.StructureSet` / `.CurrentUser.Name`
- `StructureSet.Structures`, `Structure.Id`, `Structure.Volume`
- `PlanSetup.GetDVHCumulativeData` → `DVHData.CurveData`
- `DVHPoint.DoseValue` (`.Dose`), `DVHPoint.Volume`
- Enums: `DoseValuePresentation.Absolute`, `VolumePresentation.Relative`

## Reusability
The extract-and-serialize core is fully liftable and version-stable. Two demo warts to fix for reuse: the output path is hardcoded to `c:\temp\…` (and the plugin doesn't request write access — fine for a desktop `StreamWriter`, but parameterize the folder), and the structure id is a literal. The bin width (0.1) and the absolute-dose / relative-volume presentation are the two knobs that change the CSV's meaning — make them explicit if you batch. Generalize trivially by looping `StructureSet.Structures` to emit one file (or one column block) per structure — see ESAP-03 (ExportBatchDVHs) for the cohort version, W1811-01 for the same extract behind the ESAPIX helper.

## Idea sparks
- Loop all non-empty structures to dump a full-plan DVH workbook for offline QA.
- Swap the relative-volume presentation for `AbsoluteCm3` to feed NTCP models that need absolute organ volumes.
- Emit both cumulative and `Differential()` curves side by side for peak-dose / spectral inspection.
