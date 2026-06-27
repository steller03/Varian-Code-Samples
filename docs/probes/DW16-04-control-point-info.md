# DW16-04 — ShowControlPointInfo (MLC leaf positions for one control point)

**Tier D lightweight.** Binary plugin that finds the first *PlanningApproved* external plan, takes its
first non-setup beam's control point 0, and message-boxes the meterset weight, gantry angle, and a
formatted Bank A / Bank B leaf-position table.

- **ESAPI surface:** `ControlPoint.LeafPositions` (`float[2,n]`) with `MetersetWeight` / `GantryAngle`;
  `Beam.IsSetupField`; `PlanSetupApprovalStatus.PlanningApproved`.
- **Pointer:** the MLC-leaf slice of cluster 10 — exemplar
  [DW16-19 A3_Plugin](DW16-19-control-point-report.md).
