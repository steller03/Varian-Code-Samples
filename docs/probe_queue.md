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
| B7 | DW18-06 | AutoPlan | 4 | queued | |
| B8 | W1504-02 | EQD2_2 — plan sums + PDR brachy | 4 | queued | |
| B9 | W1804-03 | CreateVerificationPlan — IMRT QA | 4 | queued | |
| B10 | DW16-09 | PlanQualityCheck | 4 | queued | |
| B11 | DW16-12 | CreateVerificationPlan | 4 | queued | |
| B12 | DW16-17 | Intermediate_10 — collimator clearance | 4 | queued | |
| B13 | DW16-19 | A3_Plugin — control-point report | 4 | queued | |
| B14 | DW16-30 | SpotWeightReporting | 4 | queued | |
| B15 | DW16-28 | Proton1 — uncertainty DVH max | 4 | queued | |
| B16 | DW16-29 | Proton2 — uncertainty DVH D95 | 4 | queued | |
| B17 | W1810-02 | PlanChecker — Visual Scripting | 4 | queued | |

Note: B15 + B16 are a paired proton-DVH exercise — consider one combined probe.

## Tier C — score 3 (probe on request only) — 31

Most are duplicate-cluster members superseded by a Tier A/B exemplar (see SYNTHESIS clusters);
probe one individually only if you want that specific variant.

DW16-01, DW16-02, DW16-08, DW16-15 (DVH-extract katas → cluster 1, use W1811-01) · W2001-02,
W2001-03, W2001-04 (MVVM DVH/metrics → clusters 1, 3) · DW16-13, DW16-23, DW16-24, W1804-02
(opt / control structures → cluster 11) · DW16-10, DW18-08 (plan / patient summary → cluster 16) ·
DW16-11, DW14-06, DW18-02, DW18-03, DW18-05, W1504-03, W2003-01 (ARIA mining / access →
clusters 14, 15) · DW14-04, DW18-09 (scaffolding → cluster 18) · DW16-14, DW14-09 (image / CT) ·
DW16-25 (plan indices) · W1504-01 (EQD2 → cluster 5) · W1712-01 (DVH plot → cluster 3) ·
ESAP-04, ESPL-01 (web DVH / lookups → clusters 1, 3) · DW14-08, W1804-01 (compact planning →
cluster 7).

## Tier D — score 2 / 1 (skip unless curious) — 16

Hello-worlds, basic readouts, and project / standalone twins:
DW16-03, DW16-04, DW16-05, DW16-06, DW16-07, DW16-26, DW16-27, DW14-02, DW14-05, DW14-07,
DW18-07, W2001-05, W1810-01, ESPL-03, W1504-05, W1504-06.

## Excluded as twins (covered by a queued sibling — no separate probe)

- **DW16-20** (A3_StandAlone) — standalone twin of **DW16-19** (A3_Plugin, B13).
- **ESPL-02** (Export3D single-file) — twin of **ESAP-02** (A20).
- **ESPL-04** (GetDicomCollection single-file) — twin of **ESAP-05** (A3).

A probe for any of these would only note the project-vs-single-file delta.
