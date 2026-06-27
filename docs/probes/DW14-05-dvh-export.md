# DW14-05 — DVHExport (PTV cumulative DVH → CSV)

**Tier D lightweight.** Binary plugin that finds the `PTV` structure, pulls its cumulative DVH, and writes
`Dose,Volume` rows to a hardcoded CSV (`c:\temp\keranen_dvh.csv`).

- **ESAPI surface:** `PlanSetup.GetDVHCumulativeData(..., Absolute, Relative, 0.1)` → `DVHData.CurveData`
  → `DVHPoint.DoseValue/Volume`.
- **Pointer:** the minimal single-structure member of cluster 1 — exemplar [W1811-01
  DiggingIntoDVH](W1811-01-digging-into-dvh.md); see also [DW16-08 DVHExtract](DW16-08-dvh-extract.md).
