# DW16-03 — Newbie3 (console beam/jaw/MU readout)

**Tier D lightweight.** Standalone console exe that opens a fixed patient and prints, for the first
course's first plan, each beam's gantry / collimator / table angle, X1/X2 & Y1/Y2 jaws, and MU.

- **ESAPI surface:** `Beam.ControlPoints.First()` → `.GantryAngle` / `.CollimatorAngle` /
  `.PatientSupportAngle` / `.JawPositions` / `.MetersetWeight`.
- **Pointer:** read-only console sibling of the cluster-10 control-point reporters — exemplar
  [DW16-19 A3_Plugin](DW16-19-control-point-report.md).
