# DW14-06 — DataMining (database walk → plan/beam/control-point readout)

**Cluster 15 delta** — exemplar [ESAP-01 DataMining](ESAP-01-data-mining.md).

- **Problem:** mine the patient database for plan and beam data — here, for every course named
  `"Varian"`, print each plan's approval status, max dose, and per-beam control-point metersets.
- **Differs from the exemplar:** the earliest (2014, v11) form of the mining loop. Same
  `Application.CreateApplication` → `PatientSummaries` → `OpenPatient`/`ClosePatient` walk, but filters
  courses by exact `Id == "Varian"`, then drills `PlanSetup → Beams → ControlPoints`. Sets
  `DoseValuePresentation.Absolute` and prints `Dose.DoseMax3D`; console-only, no export. Uses
  hardcoded demo credentials `CreateApplication("allrights","allrights")`.
- **ESAPI surfaces it adds:** `PlanSetup.ApprovalStatus`, `Dose.DoseMax3D`, `Beam.ControlPoints` / `ControlPoint.MetersetWeight`, `DoseValuePresentation`.
- **Reuse note:** the liftable bit is the course→plan→beam→control-point drill-down; ESAP-01 is the
  modern, better-guarded skeleton — prefer interactive (`null,null`) sign-in over baked-in creds. Verdict Illustrative.
