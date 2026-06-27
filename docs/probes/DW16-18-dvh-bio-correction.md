# DW16-18 — DvhBioCorrection (voxel-sampled LQ biological DVH metrics, batch)

| Field | Value |
|---|---|
| ID | DW16-18 |
| Solution | DvhBioCorrection |
| Source event | Developer Workshop 2016 — kata Advanced.1 |
| ESAPI version | v13.6 (declared v11–15.1) |
| Type | Standalone exe (console) + reusable library (`DvhBioCorrection.DvhMetric`) |
| Reuse verdict | Liftable |

## Problem
A researcher wants dose metrics computed on the **biologically corrected** dose rather than physical
dose — e.g. mean LQ-equivalent dose for a structure — and wants to run it over a list of
(patient, course, plan, structure, metric) jobs in batch. The kata shows how to apply a
linear-quadratic transform voxel-by-voxel inside a structure and reduce it to a metric, factored
cleanly into a reusable library.

## Approach
The console `Program` reads a tab-separated job file (one line = patientId, courseId, planId,
structureId, metricName), opens each patient once (reusing the handle when the next line is the same
patient), and delegates each job to `DoseMetricCalculator.Calculate`, printing the result. The
library is the interesting part and is nicely decomposed:
- **`DoseExtractor`** turns a 3-D `Dose` into a flat list of physical doses *inside a structure*.
  It walks the dose grid in (y, z) steps of 2 mm and, for each line across x, calls **two parallel
  profiles**: `Structure.GetSegmentProfile(start, stop, BitArray)` (a boolean in/out mask along the
  line) and `Dose.GetDoseProfile(start, stop, double[])` (the dose along the same line). Where the
  segment mask is true, it keeps that voxel's dose. The result is a `double[]` of all in-structure
  dose samples — effectively a hand-rolled differential DVH sample set.
- **`LqBioDoseConverter`** maps each physical dose `d` to a biological dose via
  `d·(d/n + α/β)/(2 + α/β)` (the per-voxel LQ-to-EQD2 form for `n` fractions) — applied element-wise
  across the dose array.
- **`DoseMetricCalculator`** orchestrates: extract in-structure physical doses, and if the metric
  name matches `LQ, a/b=<x>` (parsed by regex), pull `NumberOfFractions` and run the converter;
  otherwise leave physical. Then a small `IDoseMetric` strategy (`MeanDoseMetric` = `Average()`)
  reduces the array to one number. The `IDoseConverter` / `IDoseMetric` interfaces make both the
  biology model and the reduction pluggable.

## ESAPI surfaces
- `Application.CreateApplication`, `Application.OpenPatientById`, `ClosePatient`
- `PlanSetup.Dose` (`Dose.Origin`, `XSize/YSize/ZSize`, `XRes/YRes/ZRes`), `DoseValuePresentation.Absolute`
- **`Structure.GetSegmentProfile(VVector, VVector, BitArray)`** — in/out mask along a line (the key idiom)
- **`Dose.GetDoseProfile(VVector, VVector, double[])`** → `DoseProfile` of `ProfilePoint.Value`
- `PlanSetup.NumberOfFractions`, `StructureSet.Structures`, `VVector`

## Reusability
Highly liftable — it's already a clean library, not a script. The **paired `GetSegmentProfile` +
`GetDoseProfile` line-scan is the reusable core**: a supported, version-stable way to enumerate the
dose voxels inside a structure when you need per-voxel math the built-in DVH can't give you (custom
biology, equivalent-uniform dose, voxel histograms). The strategy interfaces invite extension —
add a `BedConverter`, `EudMetric`, `D95Metric` without touching the extractor. Caveats: the 2 mm
sampling is hard-coded and independent of the dose grid resolution (tune or derive it); the LQ form
assumes uniform fractionation and a single α/β; and full-grid line scanning is O(voxels) — fine for
one structure, slow over a big cohort. For pure DVH metrics the native `GetDVHCumulativeData` is far
cheaper; this technique earns its cost only when you need the **biological transform before
histogramming**.

## Idea sparks
- A voxel-wise EUD / gEUD calculator reusing `DoseExtractor` and a new `IDoseMetric`.
- Biologically-corrected DVHs for plan comparison: run the converter across two plans' in-structure
  doses and diff the resulting histograms (complements W1504-04's prescription-level EQD2).
- A batch "bio-metric harvester" over a research cohort: extend the TSV job format with α/β and
  metric columns, emit a CSV — combine with DW16-21's database walk to auto-generate the job list.
