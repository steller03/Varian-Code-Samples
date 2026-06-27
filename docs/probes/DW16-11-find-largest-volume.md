# DW16-11 — FindLargestVolume (database mining: largest normal structure)

**Cluster 15 delta** — exemplars [DW16-21 Advanced_4](DW16-21-data-mine-by-anatomy.md) / [ESAP-01 DataMining](ESAP-01-data-mining.md).

- **Problem:** across the whole ARIA database, find the single largest-volume normal structure.
- **Differs from the exemplars:** the **barest** instance of the mining skeleton —
  `Application.CreateApplication()` → walk `app.PatientSummaries` → `OpenPatient`/`ClosePatient`
  per patient (in a `finally`) → for each `StructureSet.Structures` filter `DicomType` to
  `ORGAN`/`AVOIDANCE` and track a running max `Volume`. No DVH, no CSV, no course/approval filtering;
  results print to `Console`.
- **ESAPI surfaces it adds:** nothing beyond the skeleton + `Structure.Volume` / `DicomType` — that minimalism is the point.
- **Reuse note:** the cleanest teaching baseline for the open-app → iterate-summaries → open/close
  loop; the `finally`-guarded `ClosePatient` is the right shape to copy. Productionize with a
  TG-263/synonym filter rather than two hardcoded DICOM types. Verdict Liftable.
