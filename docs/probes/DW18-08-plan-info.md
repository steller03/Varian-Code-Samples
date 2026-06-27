# DW18-08 — PlanInfo (single-plan everything-readout + target DVH→CSV)

**Cluster 16 delta** — exemplar [DW16-10 PatientSummary](DW16-10-patient-summary.md).

- **Problem:** dump everything about *one* loaded plan — prescription, approval history, calc model,
  beams, structures, a few custom dose metrics — and export the target DVH to CSV.
- **Differs from the exemplar:** single-plan **deep detail** (not multi-course navigation) built as a
  classic `MessageBox` string-builder (not MVVM). Reads `NumberOfFractions`/`DosePerFraction`/
  `TotalDose`, loops `ApprovalHistory`, prints `PhotonCalculationModel`, iterates
  `Beams.OrderBy(BeamNumber)` for `Meterset.Value` + first control-point gantry/collimator, lists
  every structure's `Volume`/`DicomType`, then computes target D95/D2 and cord max via
  `GetDoseAtVolume`, parotid V30Gy via `GetVolumeAtDose`, and writes the target DVH
  (`GetDVHCumulativeData`) to `Desktop\dvh.csv`.
- **ESAPI surfaces it adds (vs DW16-10):** `PlanSetup.ApprovalHistory`, `PhotonCalculationModel`,
  `Beam.Meterset` / `ControlPoint.GantryAngle` / `CollimatorAngle`, `GetDoseAtVolume`,
  `GetVolumeAtDose`, `GetDVHCumulativeData`, `TargetVolumeID`.
- **Reuse note:** a compact "everything about one plan" readout; the beam-table, dose-metric, and
  DVH-export blocks each lift independently. Hardcoded `"Cord"`/`"Parotid"` lookups and `.Single()`
  on `TargetVolumeID` will throw on real data — guard before reuse. Verdict Liftable.
