# Probe queue — depth-phase worklist

Ranked probe candidates, the input to [`dispatches/3b-probe-batch.md`](dispatches/3b-probe-batch.md).
Tiers are derived from the triage scores and the duplicate clusters in
[`SYNTHESIS.md`](SYNTHESIS.md) (score = value to a physicist hunting automation ideas). **You own
this file** — prune, reorder, or re-tier freely; the dispatch just walks it top to bottom and skips
anything already `done`.

`Status`: `queued` → `done` (the dispatch flips it and fills the `Probe` link).

## Tier A — probe these (top 20 + requested) — 21 units

Your explicit picks lead the queue (A1–A3), then the rest of the top 20 in rank order.

| # | ID | Solution | Score | Status | Probe |
|--:|---|---|:--:|---|---|
| A1 | DW16-16 | ExtractDosePlane — planar dose → CSV | 4 | done | DW16-16-extract-dose-plane.md |
| A2 | ESAP-01 | DataMining — per-patient treatment report | 4 | done | ESAP-01-data-mining.md |
| A3 | ESAP-05 | GetDicomCollection — DCMTK C-MOVE | 4 | done | ESAP-05-get-dicom-collection.md |
| A4 | DW18-04 | AutomatedPlanningDemo (MCO) | 5 | done | DW18-04-automated-planning-mco.md |
| A5 | RS15-01 | AutomatedPlanningDemo (full pipeline) | 5 | done | RS15-01-automated-planning-pipeline.md |
| A6 | DS23-01 | ProtonFeaturesDemo (v18 IMPT) | 5 | done | DS23-01-proton-features-demo.md |
| A7 | DW16-22 | Advanced_5 — automated VMAT | 5 | done | DW16-22-automated-vmat-planning.md |
| A8 | ESAP-06 | PlanQualityMetrics | 5 | done | ESAP-06-plan-quality-metrics.md |
| A9 | ESAP-10 | Uab.VMS.Console — ESAPI REPL | 5 | done | ESAP-10-esapi-repl-console.md |
| A10 | ESAP-07 | PluginTester | 5 | done | ESAP-07-plugin-tester.md |
| A11 | DW14-01 | ESAPIAnon — C-MOVE + anonymize | 5 | done | DW14-01-esapi-anon.md |
| A12 | W1504-04 | RBEReport — interactive radiobiology | 5 | done | W1504-04-rbe-report.md |
| A13 | DW16-18 | DvhBioCorrection — LQ DVH correction | 5 | done | DW16-18-dvh-bio-correction.md |
| A14 | DW16-21 | Advanced_4 — cohort mining | 5 | done | DW16-21-data-mine-by-anatomy.md |
| A15 | DW16-31 | CustomPostProcessing — spot-MU limits | 5 | done | DW16-31-proton-spot-mu-limits.md |
| A16 | W2008-01 | DVH_Evaluator | 4 | done | W2008-01-dvh-evaluator.md |
| A17 | W2001-01 | DoseMetricExample (MVVM) | 4 | done | W2001-01-dose-metric-mvvm.md |
| A18 | W1811-01 | DiggingIntoDVH | 4 | done | W1811-01-digging-into-dvh.md |
| A19 | DW14-03 | RapidPlanEvaluation | 4 | done | DW14-03-rapidplan-evaluation.md |
| A20 | ESAP-02 | Export3D | 4 | done | ESAP-02-export-3d.md |
| A21 | RS15-02 | EUDScript — EUD/TCP/NTCP | 4 | done | RS15-02-eud-tcp-ntcp.md |

## Tier B — next: remaining score-4 units — 17

Ordered by judgment. Probe after Tier A, or cherry-pick.

| # | ID | Solution | Score | Status | Probe |
|--:|---|---|:--:|---|---|
| B1 | ESAP-09 | StructureIdFrequency — TG-263 histogram | 4 | done | ESAP-09-structure-id-frequency.md |
| B2 | ESAP-03 | ExportBatchDVHs | 4 | done | ESAP-03-export-batch-dvhs.md |
| B3 | ESAP-11 | ProfileSamples — profiles + gamma | 4 | done | ESAP-11-profile-samples.md |
| B4 | ESAP-08 | RBEReport (project form) | 4 | done | ESAP-08-rbe-report.md |
| B5 | W2103-01 | BeamDataVisualization | 4 | done | W2103-01-beam-data-visualization.md |
| B6 | DW18-01 | VAIS — OAuth/FHIR ARIA | 4 | done | DW18-01-vais-aria-webservice.md |
| B7 | DW18-06 | AutoPlan | 4 | done | DW18-06-autoplan.md |
| B8 | W1504-02 | EQD2_2 — plan sums + PDR brachy | 4 | done | W1504-02-eqd2-plan-sum-pdr.md |
| B9 | W1804-03 | CreateVerificationPlan — IMRT QA | 4 | done | W1804-03-create-verification-plan.md |
| B10 | DW16-09 | PlanQualityCheck | 4 | done | DW16-09-plan-quality-check.md |
| B11 | DW16-12 | CreateVerificationPlan | 4 | done | DW16-12-create-verification-plan.md |
| B12 | DW16-17 | Intermediate_10 — collimator clearance | 4 | done | DW16-17-collimator-clearance.md |
| B13 | DW16-19 | A3_Plugin — control-point report | 4 | done | DW16-19-control-point-report.md |
| B14 | DW16-30 | SpotWeightReporting | 4 | done | DW16-30-spot-weight-reporting.md |
| B15 | DW16-28 | Proton1 — uncertainty DVH max | 4 | done | DW16-28-29-proton-uncertainty-dvh.md |
| B16 | DW16-29 | Proton2 — uncertainty DVH D95 | 4 | done | DW16-28-29-proton-uncertainty-dvh.md |
| B17 | W1810-02 | PlanChecker — Visual Scripting | 4 | done | W1810-02-plan-checker.md |

Note: B15 + B16 are a paired proton-DVH exercise — consider one combined probe.

## Tier C — score 3 — 31

All score 3. Most are duplicate-cluster members superseded by a Tier A/B exemplar (see SYNTHESIS
clusters) — the **Cluster / note** column records which, so you can cherry-pick the distinctive
ones (e.g. C23–C25: the only Image & registration and plan-index units in the catalogue) instead
of walking duplicates. Now tabled in listed order so the dispatch can walk it top to bottom once
Tiers A/B are done.

| # | ID | Solution | Cluster / note | Status | Probe |
|--:|---|---|---|---|---|
| C1 | DW16-01 | DVHMetrics | DVH-extract → cluster 1 (W1811-01) | done | DW16-01-dvh-metrics.md |
| C2 | DW16-02 | CSVDVHMetrics | DVH-extract → cluster 1 (W1811-01) | done | DW16-02-csv-dvh-metrics.md |
| C3 | DW16-08 | DVHExtract | DVH-extract → cluster 1 (W1811-01) | done | DW16-08-dvh-extract.md |
| C4 | DW16-15 | VolumeAtPercentDose | DVH-extract → cluster 1 (W1811-01) | done | DW16-15-volume-at-percent-dose.md |
| C5 | W2001-02 | DVHPlot | MVVM DVH/metrics → clusters 1, 3 | done | W2001-02-dvh-plot.md |
| C6 | W2001-03 | DoseMetrics | MVVM DVH/metrics → clusters 1, 3 | done | W2001-03-dose-metrics.md |
| C7 | W2001-04 | DoseParameters | MVVM DVH/metrics → clusters 1, 3 | done | W2001-04-dose-parameters.md |
| C8 | DW16-13 | Intermediate_6 | opt / control structures → cluster 11 | done | DW16-13-ptv-ring-structures.md |
| C9 | DW16-23 | ExtractBodySection | opt / control structures → cluster 11 | done | DW16-23-extract-body-section.md |
| C10 | DW16-24 | SplitStructure | opt / control structures → cluster 11 | done | DW16-24-split-structure.md |
| C11 | W1804-02 | CreateOptStructures | opt / control structures → cluster 11 | done | W1804-02-create-opt-structures.md |
| C12 | DW16-10 | PatientSummary | plan / patient summary → cluster 16 | done | DW16-10-patient-summary.md |
| C13 | DW18-08 | PlanInfo | plan / patient summary → cluster 16 | done | DW18-08-plan-info.md |
| C14 | DW16-11 | FindLargestVolume | ARIA mining / access → clusters 14, 15 | done | DW16-11-find-largest-volume.md |
| C15 | DW14-06 | DataMining | ARIA mining / access → clusters 14, 15 | done | DW14-06-data-mining.md |
| C16 | DW18-02 | AppRoleSample | ARIA mining / access → clusters 14, 15 | done | DW18-02-app-role-sample.md |
| C17 | DW18-03 | ARIAAccessSample | ARIA mining / access → clusters 14, 15 | done | DW18-03-aria-access-sample.md |
| C18 | DW18-05 | DocumenServiceSample | ARIA mining / access → clusters 14, 15 | done | DW18-05-document-service.md |
| C19 | W1504-03 | FindBrachyPlans | ARIA mining / access → clusters 14, 15 | done | W1504-03-find-brachy-plans.md |
| C20 | W2003-01 | AAWebServiceTests | ARIA mining / access → clusters 14, 15 | done | W2003-01-aria-access-appointments.md |
| C21 | DW14-04 | SimpleUIDemoApp | scaffolding → cluster 18 | done | DW14-04-simple-ui-selection-box.md |
| C22 | DW18-09 | ESAPIX_Demos | scaffolding → cluster 18 | done | DW18-09-esapix-demos.md |
| C23 | DW16-14 | MeanCTNumber | image / CT (no probed exemplar) | done | DW16-14-mean-ct-number.md |
| C24 | DW14-09 | TRE | image / registration (no probed exemplar) | done | DW14-09-tre-registration.md |
| C25 | DW16-25 | PlanIndices | plan indices (distinct) | done | DW16-25-plan-indices.md |
| C26 | W1504-01 | EQD2_1 | EQD2 → cluster 5 | done | W1504-01-eqd2.md |
| C27 | W1712-01 | Example_DVH | DVH plot → cluster 3 | done | W1712-01-example-dvh.md |
| C28 | ESAP-04 | GenerateWebDVH | web DVH / lookups → clusters 1, 3 | done | ESAP-04-generate-web-dvh.md |
| C29 | ESPL-01 | DvhLookups | web DVH / lookups → clusters 1, 3 | done | ESPL-01-dvh-lookups.md |
| C30 | DW14-08 | Superplan | compact planning → cluster 7 | done | DW14-08-superplan.md |
| C31 | W1804-01 | CreateAPPA | compact planning → cluster 7 | done | W1804-01-create-appa.md |

## Tier D — score 2 / 1 (skip unless curious) — 16

Hello-worlds, basic readouts, and project / standalone twins. Probed as **lightweight** delta entries
(what it does, single ESAPI surface, twin/cluster pointer).

| # | ID | Solution | Note | Status | Probe |
|--:|---|---|---|---|---|
| D1 | DW16-03 | Newbie3 | console beam/jaw/MU readout → cluster 10 | done | DW16-03-beam-jaw-readout.md |
| D2 | DW16-04 | ShowControlPointInfo | MLC leaf positions → cluster 10 | done | DW16-04-control-point-info.md |
| D3 | DW16-05 | ShowTargetStructures | list PTV/CTV/GTV in scope (distinct) | done | DW16-05-show-target-structures.md |
| D4 | DW16-06 | MSExcelForm | demographics → Excel, cluster 17 exemplar | done | DW16-06-excel-demographics.md |
| D5 | DW16-07 | MSExcelFormBinary | twin of DW16-06 (binary packaging) | done | DW16-07-excel-demographics-binary.md |
| D6 | DW16-26 | Advanced8Kata | 4D-phase HU via voxel access → see DW16-14 | done | DW16-26-4d-gating-hu.md |
| D7 | DW16-27 | PatientPhoto | EF DB-access WPF template → cluster 18 | done | DW16-27-patient-photo.md |
| D8 | DW14-02 | MVVM_Demo | MVVM + print-report scaffolding → cluster 18 | done | DW14-02-mvvm-print-report.md |
| D9 | DW14-05 | DVHExport | PTV DVH → CSV → cluster 1 | done | DW14-05-dvh-export.md |
| D10 | DW14-07 | DoseProfiles | dose-at-iso + profile → cluster 4 | done | DW14-07-dose-profiles.md |
| D11 | DW18-07 | DoseProfile | line profile → CSV, near-twin of DW14-07 | done | DW18-07-dose-profile.md |
| D12 | W2001-05 | sampleLauncher | exe launcher → cluster 18 | done | W2001-05-sample-launcher.md |
| D13 | W1810-01 | BeamOrder | Visual Scripting element, twin of W1810-02 | done | W1810-01-beam-order.md |
| D14 | ESPL-03 | GenerateWebDVH | single-file twin of ESAP-04 → cluster 3 | done | ESPL-03-generate-web-dvh.md |
| D15 | W1504-05 | hello | hello-world message box | done | W1504-05-hello.md |
| D16 | W1504-06 | test | active-plan-id message box | done | W1504-06-test.md |

## Excluded as twins (covered by a queued sibling — no separate probe)

- **DW16-20** (A3_StandAlone) — standalone twin of **DW16-19** (A3_Plugin, B13).
- **ESPL-02** (Export3D single-file) — twin of **ESAP-02** (A20).
- **ESPL-04** (GetDicomCollection single-file) — twin of **ESAP-05** (A3).

A probe for any of these would only note the project-vs-single-file delta.
