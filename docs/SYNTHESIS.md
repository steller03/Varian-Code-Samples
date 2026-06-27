# SYNTHESIS — Varian Code-Samples Catalog

The master, problem-first map of the
[VarianAPIs/Varian-Code-Samples](https://github.com/VarianAPIs/Varian-Code-Samples)
repository. Generated from the triage shards in [`registry/`](registry/); regenerate it
whenever the shards (or their `Probe` links) change.

## Intro

The repo is ~80 Visual Studio solutions plus a handful of standalone plugin scripts,
overwhelmingly C# ESAPI (Eclipse Scripting API) code, spread across two top folders:
`webinars & workshops` (14 dated events) and `Eclipse Scripting API`. It is a teaching and
reference corpus — worked solutions to the recurring physics-automation problems a clinical
medical physicist hits in Eclipse: DVH/dose metrics, structure ops, beam/MLC geometry,
plan QA, automated planning, reporting, DICOM interop, and ARIA data access.

This catalog reorganizes that corpus by **the problem each unit solves**, not by folder.
Three views, by zoom level:

- **This file (`SYNTHESIS.md`)** — the cohesive overview: a curated "start here," counts,
  the clickable problem-category index, duplicate clusters, the ranked shortlist, and a
  coverage ledger. Start here if you don't yet know what you're looking for.
- **[`probe_queue.md`](probe_queue.md)** — the tier-ranked table of contents plus the
  **Events reference** (meeting / date / presenter captured once per event). Use it as the
  ranked TOC into the deep dives.
- **[`probes/`](probes/)** — the ~1-page deep dives, one per probed unit (88 units → 84 files;
  four are twins that share a probe). Each entry below links straight into its probe.
- **[`registry/`](registry/)** — the per-event source of truth: one table row per unit, with
  exact path, ESAPI version, type, verdict, the ≤15-word problem, and the `Probe` link these
  entries are rendered from. Use it for the complete searchable index and exact paths.

IDs follow `<EVENT-SLUG>-NN` and are cross-referenced throughout. Verdicts and scores are
defined in [`taxonomy.md`](taxonomy.md): score = value to a physicist hunting automation ideas
(1 trivial → 5 high-leverage); verdict = `Liftable` / `Adaptable` / `Illustrative` / `Obsolete`.

## Start here

If you read six things, read these. The four end-to-end planning pipelines show the full
automation arc; the two dev-tooling standouts change how you write and debug everything else.

- **DW18-04 · [AutomatedPlanningDemo](probes/DW18-04-automated-planning-mco.md)** — newest full
  photon auto-plan: MCO optimization, verification plans, and a plan-quality report end to end (v15.6).
- **RS15-01 · [AutomatedPlanningDemo](probes/RS15-01-automated-planning-pipeline.md)** — the
  fullest prescription→DVH-estimation→optimization→dose→reporting→QA pipeline in one script.
- **DS23-01 · [ProtonFeaturesDemo](probes/DS23-01-proton-features-demo.md)** — the repo's most
  complete proton automation: full v18 IMPT build with robust optimization, RapidPlan, DECT verification, exports.
- **DW16-22 · [Advanced_5](probes/DW16-22-automated-vmat-planning.md)** — end-to-end automated
  VMAT (structures→beams→optimization→dose calc); the highest-leverage teaching kata.
- **ESAP-07 · [PluginTester](probes/ESAP-07-plugin-tester.md)** — run and debug binary plugins
  standalone outside Eclipse; a major dev-loop accelerator.
- **ESAP-10 · [Uab.VMS.Console](probes/ESAP-10-esapi-repl-console.md)** — interactive C# REPL for
  live ESAPI scripting with code completion; uniquely lowers the exploration barrier.

## At a glance

**Total units cataloged: 88** across all 16 event folders (every shard triaged).

### By problem category (taxonomy §1 order)

| Category | Units |
|---|---:|
| Plan QA & verification | 8 |
| DVH & dose metrics | 24 |
| Structure & contour ops | 7 |
| Optimization & planning | 8 |
| Reporting & documents | 5 |
| DICOM I/O & interop | 3 |
| Image & registration | 3 |
| Beam, MLC & geometry | 9 |
| ARIA & database query | 10 |
| Workflow & process | 0 |
| Plugin scaffolding & UI | 9 |
| Machine & commissioning | 0 |
| Research & algorithmic | 2 |
| Other | 0 |
| **Total** | **88** |

DVH & dose metrics dominate (~27%); the long tail of `Reporting`, `DICOM`, `Image`, and
`Research` reflects secondary categories carried by units primarily classed elsewhere.
`Workflow & process` and `Machine & commissioning` have no *primary* members (commissioning
shows up only as W2103-01's secondary).

### By reuse verdict

| Verdict | Units |
|---|---:|
| Liftable | 31 |
| Adaptable | 40 |
| Illustrative | 17 |
| Obsolete | 0 |

No unit was judged outright `Obsolete` at triage — even the v11 samples still illustrate
current API surfaces. `Liftable`+`Adaptable` = 71/88 (~81%) carry reusable patterns.

### ESAPI version spread

| Version | Units |
|---|---:|
| v11 | 25 |
| v13 | 10 |
| v13.5 | 6 |
| v13.6 | 12 |
| v13.7 | 4 |
| v15 | 3 |
| v15.1 | 1 |
| v15.5 | 4 |
| v15.6 | 8 |
| v18 | 1 |
| unknown | 14 |

Weighted toward the v11–v13.x era (57 units ≤ v13.7). The v15.x cluster (16 units) is the
modern MVVM/binary-plugin material; v18 is the single DS23 proton sample. `unknown` (14) is
mostly the DW18 ARIA web-service stack and the loose single-file stubs, which carry no VMS
version reference.

## By problem category

The browsable index, now clickable: each Solution name links to its probe deep dive.
Entry format: `ID · [Solution](probes/<file>) · ≤15-word problem · score · path`.
Secondary categories noted where a unit also lives elsewhere.

### Plan QA & verification (8)

- **DW16-09 · [PlanQualityCheck](probes/DW16-09-plan-quality-check.md)** · Check lung-plan dose metrics against criteria, pass/fail · 4 · `…/Developer Workshop 2016/katas/intermediate.2/…/PlanQualityCheck`
- **DW16-12 · [CreateVerificationPlan](probes/DW16-12-create-verification-plan.md)** · Automate QA course and verification-plan creation with dose calc · 4 · `…/Developer Workshop 2016/katas/intermediate.5/…/CreateVerificationPlan`
- **DW16-25 · [PlanIndices](probes/DW16-25-plan-indices.md)** · Compute conformity, gradient, heterogeneity indices for a plan · 3 · `…/Developer Workshop 2016/katas/Advanced.7`
- **DW18-08 · [PlanInfo](probes/DW18-08-plan-info.md)** · Summarize plan prescription, beams, structures and dose metrics · 3 · `…/Developer Workshop 2018/ESAPI Introduction/…/PlanInfo` _(also DVH)_
- **W1804-03 · [CreateVerificationPlan](probes/W1804-03-create-verification-plan.md)** · Create IMRT QA course and composite verification plan with dose · 4 · `…/06 Apr 2018 Webinar/…/CreateVerificationPlan`
- **W1810-02 · [PlanChecker](probes/W1810-02-plan-checker.md)** · Visual Scripting element checking target, max-dose location, IMRT MU renorm · 4 · `…/16 Oct 2018 Webinar/ActionPacks/Projects/PlanChecker`
- **W2008-01 · [DVH_Evaluator](probes/W2008-01-dvh-evaluator.md)** · Evaluate CSV DVH constraints, compare plans, export HTML report · 4 · `…/20 Aug 2020 Webinar - Constraint Export/DVHEvaluator_Main` _(also DVH)_
- **ESAP-06 · [PlanQualityMetrics](probes/ESAP-06-plan-quality-metrics.md)** · Evaluate configurable plan-quality metrics, emit HTML pass/fail report · 5 · `Eclipse Scripting API/projects/PlanQualityMetrics` _(also Reporting)_

### DVH & dose metrics (24)

- **DW16-01 · [DVHMetrics](probes/DW16-01-dvh-metrics.md)** · Extract and display DVH metrics for plan structures · 3 · `…/katas/newbie.1/…/DVHMetrics`
- **DW16-02 · [CSVDVHMetrics](probes/DW16-02-csv-dvh-metrics.md)** · Evaluate DVH constraints from a CSV template · 3 · `…/katas/Newbie.2/TextDVHMetrics`
- **DW16-08 · [DVHExtract](probes/DW16-08-dvh-extract.md)** · Extract a structure's DVH and write to CSV · 3 · `…/katas/intermediate.1/…/DVHExtract`
- **DW16-15 · [VolumeAtPercentDose](probes/DW16-15-volume-at-percent-dose.md)** · Compute volume receiving a given percent of prescription · 3 · `…/katas/intermediate.8/…/VolumeAtPercentDose`
- **DW16-16 · [ExtractDosePlane](probes/DW16-16-extract-dose-plane.md)** · Export a beam's planar dose to CSV for QA · 4 · `…/katas/intermediate.9/…/ExtractDosePlane` _(also Reporting)_
- **DW16-18 · [DvhBioCorrection](probes/DW16-18-dvh-bio-correction.md)** · Apply linear-quadratic biological correction to DVHs across a dataset · 5 · `…/katas/Advanced.1/DvhBioCorrection` _(also Research)_
- **DW16-28 · [Proton1](probes/DW16-28-29-proton-uncertainty-dvh.md)** · Report plan and uncertainty DVH max-dose stats for structure · 4 · `…/katas/Proton.1/…/Proton1`
- **DW16-29 · [Proton2](probes/DW16-28-29-proton-uncertainty-dvh.md)** · Report D95% from plan/uncertainty DVHs for proton plans · 4 · `…/katas/Proton.2/…/Proton2`
- **DW14-05 · [DVHExport](probes/DW14-05-dvh-export.md)** · Extract PTV cumulative DVH and export to CSV · 2 · `…/Developer Workshop 2014/hands-on exercises/exercise 1/…/DVHExport`
- **DW14-07 · [DoseProfiles](probes/DW14-07-dose-profiles.md)** · Extract dose at isocenter and a dose profile to file · 2 · `…/Developer Workshop 2014/hands-on exercises/exercise 3/…/DoseProfiles`
- **DW18-07 · [DoseProfile](probes/DW18-07-dose-profile.md)** · Extract a line dose profile and export to CSV · 2 · `…/Developer Workshop 2018/ESAPI Introduction/…/DoseProfile`
- **W2001-01 · [DoseMetricExample](probes/W2001-01-dose-metric-mvvm.md)** · Combined MVVM app: DVH plot, dose-metric table, dose parameters · 4 · `…/16 Jan 2020 Webinar/AppsCombined/DoseMetricExample` _(also UI)_
- **W2001-02 · [DVHPlot](probes/W2001-02-dvh-plot.md)** · Plot cumulative DVH curves for selected structures with OxyPlot · 3 · `…/16 Jan 2020 Webinar/SeparatedApps/Projects/DVHPlot`
- **W2001-03 · [DoseMetrics](probes/W2001-03-dose-metrics.md)** · Compute dose-at-volume and volume-at-dose metrics in MVVM table · 3 · `…/16 Jan 2020 Webinar/SeparatedApps/Projects/DoseMetrics`
- **W2001-04 · [DoseParameters](probes/W2001-04-dose-parameters.md)** · Display plan dose-calculation and prescription parameters in MVVM view · 3 · `…/16 Jan 2020 Webinar/SeparatedApps/Projects/DoseParameters` _(also Reporting)_
- **W1504-01 · [EQD2_1](probes/W1504-01-eqd2.md)** · Compute EQD2 equivalent dose for each plan in scope · 3 · `…/21 Apr 2015 Webinar/…/EQD2_1` _(also Research)_
- **W1504-02 · [EQD2_2](probes/W1504-02-eqd2-plan-sum-pdr.md)** · Compute EQD2 per plan sum, including PDR brachy modeling · 4 · `…/21 Apr 2015 Webinar/…/EQD2_2` _(also Research)_
- **W1712-01 · [Example_DVH](probes/W1712-01-example-dvh.md)** · Plot DVH curves and dose stats for user-selected plan structures · 3 · `…/17 Dec 2017 Webinar/DoseReview/Projects/Example_DVH`
- **W1811-01 · [DiggingIntoDVH](probes/W1811-01-digging-into-dvh.md)** · Extract DVH metrics, run plan constraints, mine cohort DVHs, plot · 4 · `…/14 Nov 2018 Webinar (DVH)/DiggingIntoDVH`
- **ESAP-03 · [ExportBatchDVHs](probes/ESAP-03-export-batch-dvhs.md)** · Batch-export DVH curves across plans for offline analysis · 4 · `Eclipse Scripting API/projects/ExportBatchDVHs`
- **ESAP-04 · [GenerateWebDVH](probes/ESAP-04-generate-web-dvh.md)** · Generate an interactive web/HTML DVH chart for selected structures · 3 · `Eclipse Scripting API/projects/GenerateWebDVH` _(also Reporting)_
- **ESAP-11 · [ProfileSamples](probes/ESAP-11-profile-samples.md)** · Extract 1D dose/depth profiles and run unscaled gamma analysis · 4 · `Eclipse Scripting API/projects/ProfileSamples` _(also Research)_
- **ESPL-01 · [DvhLookups](probes/ESPL-01-dvh-lookups.md)** · Interactively look up dose-at-volume and volume-at-dose for a structure · 3 · `Eclipse Scripting API/plugins/DvhLookups.cs`
- **ESPL-03 · [GenerateWebDVH](probes/ESPL-03-generate-web-dvh.md)** · Render selected-structure DVHs as a browser HTML/JavaScript chart · 2 · `Eclipse Scripting API/plugins/GenerateWebDVH.cs` _(also Reporting)_

### Structure & contour ops (7)

- **DW16-05 · [ShowTargetStructures](probes/DW16-05-show-target-structures.md)** · List target structures assigned to plan or plan sum · 2 · `…/katas/Newbie.5/ShowTargetStructures`
- **DW16-13 · [Intermediate_6](probes/DW16-13-ptv-ring-structures.md)** · Create ring/control structures around all PTVs via margins · 3 · `…/katas/intermediate.6/Intermediate_6`
- **DW16-23 · [ExtractBodySection](probes/DW16-23-extract-body-section.md)** · Copy a body section bounded by structure margins · 3 · `…/katas/Advanced.6/Seppo.1/…/ExtractBodySection`
- **DW16-24 · [SplitStructure](probes/DW16-24-split-structure.md)** · Split normal tissue into target-proximal and target-distal volumes · 3 · `…/katas/Advanced.6/solution/…/SplitStructure`
- **W1804-02 · [CreateOptStructures](probes/W1804-02-create-opt-structures.md)** · Build optimization structures via PTV margin and rectum buffer Boolean · 3 · `…/06 Apr 2018 Webinar/…/CreateOptStructures`
- **ESAP-02 · [Export3D](probes/ESAP-02-export-3d.md)** · Export structures, dose and bolus as 3D meshes for external viewers · 4 · `Eclipse Scripting API/projects/Export3D` _(also DICOM)_
- **ESAP-09 · [StructureIdFrequency](probes/ESAP-09-structure-id-frequency.md)** · Mine all patients for structure-naming frequency to drive TG-263 cleanup · 4 · `Eclipse Scripting API/projects/StructureIdFrequency` _(also ARIA)_

### Optimization & planning (8)

- **DW16-22 · [Advanced_5](probes/DW16-22-automated-vmat-planning.md)** · Automated VMAT planning: structures, beams, optimization, dose calc · 5 · `…/katas/Advanced.5/Projects/Advanced_5`
- **DW14-03 · [RapidPlanEvaluation](probes/DW14-03-rapidplan-evaluation.md)** · Compare a standard plan against a RapidPlan with DVH/biological metrics · 4 · `…/Developer Workshop 2014/guru track projects/RapidPlanEvaluation` _(also DVH)_
- **DW14-08 · [Superplan](probes/DW14-08-superplan.md)** · Scripted plan creation with course, beams and structure objectives · 3 · `…/Developer Workshop 2014/hands-on exercises/exercise 5/…/Superplan`
- **DW18-04 · [AutomatedPlanningDemo](probes/DW18-04-automated-planning-mco.md)** · Automated MCO planning with verification plans and quality reporting · 5 · `…/Developer Workshop 2018/AutoPlanningWithMCO`
- **DW18-06 · [AutoPlan](probes/DW18-06-autoplan.md)** · Auto-create PTV, plan, MLC beams, calculate dose and prescribe · 4 · `…/Developer Workshop 2018/ESAPI Introduction/…/AutoPlan`
- **W1804-01 · [CreateAPPA](probes/W1804-01-create-appa.md)** · Auto-create AP/PA plan with opposed MLC beams fitted to PTV · 3 · `…/06 Apr 2018 Webinar/…/CreateAPPA` _(also Beam)_
- **RS15-01 · [AutomatedPlanningDemo](probes/RS15-01-automated-planning-pipeline.md)** · End-to-end auto-planning: beams, DVH estimation, optimization, dose, QA · 5 · `…/Research Symposium 2015/…/AutomatedPlanningDemo`
- **DS23-01 · [ProtonFeaturesDemo](probes/DS23-01-proton-features-demo.md)** · End-to-end automated IMPT plan: robust optimization, RapidPlan, dose, exports · 5 · `…/22 Jul 2023 Developer Symposium/ProtonFeaturesDemo` _(also Beam)_

### Reporting & documents (5)

- **DW16-06 · [MSExcelForm](probes/DW16-06-excel-demographics.md)** · Export patient demographics and prescription dose to Excel · 2 · `…/katas/newbie.6/Projects/MSExcelForm`
- **DW16-07 · [MSExcelFormBinary](probes/DW16-07-excel-demographics-binary.md)** · Export demographics and dose to Excel, binary-plugin variant · 2 · `…/katas/newbie.6/Projects/MSExcelFormBinary`
- **DW16-10 · [PatientSummary](probes/DW16-10-patient-summary.md)** · Generate treatment-history report across all courses and plans · 3 · `…/katas/Intermediate.3/PatientSummary`
- **W1504-04 · [RBEReport](probes/W1504-04-rbe-report.md)** · Build interactive EQD2 radiobiological report, export PDF, post to ARIA · 5 · `…/21 Apr 2015 Webinar/…/RBEReport` _(also Research)_
- **ESPL-02 · [Export3D](probes/ESAP-02-export-3d.md)** · Export structures, dose, isodoses to VTK/PLY meshes for viewing or 3D printing · 4 · `Eclipse Scripting API/plugins/Export3D.cs` _(also Image)_

### DICOM I/O & interop (3)

- **DW14-01 · [ESAPIAnon](probes/DW14-01-esapi-anon.md)** · Retrieve patient DICOM via C-MOVE and anonymize tags by profile · 5 · `…/Developer Workshop 2014/guru track projects/DICOM Anonymizer/ESAPIAnon`
- **ESAP-05 · [GetDicomCollection](probes/ESAP-05-get-dicom-collection.md)** · Retrieve a plan's DICOM objects from ARIA via DCMTK C-MOVE · 4 · `Eclipse Scripting API/projects/GetDicomCollection`
- **ESPL-04 · [GetDicomCollection](probes/ESAP-05-get-dicom-collection.md)** · Generate and run a DCMTK C-MOVE to retrieve a plan's CT, structures, dose · 4 · `Eclipse Scripting API/plugins/GetDicomCollection.cs`

### Image & registration (3)

- **DW16-14 · [MeanCTNumber](probes/DW16-14-mean-ct-number.md)** · Compute mean/SD of CT numbers within a structure · 3 · `…/katas/intermediate.7/solution/MeanCTNumber`
- **DW16-26 · [Advanced8Kata](probes/DW16-26-4d-gating-hu.md)** · Extract HU from 4D gating phases, validate MIP/average · 2 · `…/katas/Advanced.8/Advanced8Kata`
- **DW14-09 · [TRE](probes/DW14-09-tre-registration.md)** · Compute target registration error and report registration accuracy · 3 · `…/Developer Workshop 2014/hands-on exercises/exercise 6/…/TRE`

### Beam, MLC & geometry (9)

- **DW16-03 · [Newbie3](probes/DW16-03-beam-jaw-readout.md)** · Extract beam parameters and jaw positions from approved plan · 2 · `…/katas/newbie.3/Newbie3`
- **DW16-04 · [ShowControlPointInfo](probes/DW16-04-control-point-info.md)** · Display MLC control-point info for a beam · 2 · `…/katas/newbie.4/…/ShowControlPointInfo`
- **DW16-17 · [Intermediate_10](probes/DW16-17-collimator-clearance.md)** · Compute minimum clearance from structures to collimator geometry · 4 · `…/katas/Intermediate.10/Projects/Intermediate_10`
- **DW16-19 · [A3_Plugin](probes/DW16-19-control-point-report.md)** · Report control-point details (MU, angles, jaws) for plans · 4 · `…/katas/Advanced.3/Projects/A3_Plugin`
- **DW16-20 · [A3_StandAlone](probes/DW16-19-control-point-report.md)** · Same control-point report as A3_Plugin, standalone form · 4 · `…/katas/Advanced.3/Projects/A3_StandAlone`
- **DW16-30 · [SpotWeightReporting](probes/DW16-30-spot-weight-reporting.md)** · Report min/max spot weights per energy layer · 4 · `…/katas/Proton.3/…/SpotWeightReporting`
- **DW16-31 · [CustomPostProcessing](probes/DW16-31-proton-spot-mu-limits.md)** · Apply energy-dependent spot-MU limits to proton spot-scanning plans · 5 · `…/katas/Proton.4/…/CustomPostProcessing`
- **W1810-01 · [BeamOrder](probes/W1810-01-beam-order.md)** · Visual Scripting element reordering plan beams by number or MU · 2 · `…/16 Oct 2018 Webinar/ActionPacks/Projects/BeamOrder`
- **W2103-01 · [BeamDataVisualization](probes/W2103-01-beam-data-visualization.md)** · Plot and export beam scan profiles by energy and field size · 4 · `…/31 Mar 2021 Webinar - Beam Data Visualization` _(also Machine)_

### ARIA & database query (10)

- **DW16-11 · [FindLargestVolume](probes/DW16-11-find-largest-volume.md)** · Mine all patients to find largest-volume structure · 3 · `…/katas/intermediate.4/…/FindLargestVolume`
- **DW16-21 · [Advanced_4](probes/DW16-21-data-mine-by-anatomy.md)** · Data-mine patients by anatomy, export dose/DVH metrics to CSV · 5 · `…/katas/Advanced.4/Advanced_4` _(also DVH)_
- **DW14-06 · [DataMining](probes/DW14-06-data-mining.md)** · Mine the patient database for plan and structure data · 3 · `…/Developer Workshop 2014/hands-on exercises/exercise 2/…/DataMining`
- **DW18-01 · [Dev Workshop 2018 (VAIS)](probes/DW18-01-vais-aria-webservice.md)** · Authenticate via OAuth/FHIR and query ARIA over web services · 4 · `…/Developer Workshop 2018/Accessing ARIA with VAIS` _(also UI)_
- **DW18-02 · [AppRoleSample](probes/DW18-02-app-role-sample.md)** · Acquire SQL application role and query ARIA database securely · 3 · `…/Developer Workshop 2018/ApplicationRoleSample`
- **DW18-03 · [ARIAAccessSample](probes/DW18-03-aria-access-sample.md)** · Authenticate and retrieve patient data via ARIA FHIR web service · 3 · `…/Developer Workshop 2018/Aria Access Sample` _(also UI)_
- **DW18-05 · [DocumenServiceSample](probes/DW18-05-document-service.md)** · Retrieve patient documents from ARIA local document web service · 3 · `…/Developer Workshop 2018/DocumenServiceSample` _(also Reporting)_
- **W1504-03 · [FindBrachyPlans](probes/W1504-03-find-brachy-plans.md)** · Scan all patients to find and list brachytherapy plans · 3 · `…/21 Apr 2015 Webinar/…/FindBrachyPlans`
- **W2003-01 · [AAWebServiceTests](probes/W2003-01-aria-access-appointments.md)** · Query ARIA Access web service for weekly machine appointments per patient · 3 · `…/23 Mar 2020 Webinar_ARIAAccess/AAWebServiceTests`
- **ESAP-01 · [DataMining](probes/ESAP-01-data-mining.md)** · Iterate all ARIA patients and write a treatment report per patient · 4 · `Eclipse Scripting API/projects/DataMining` _(also Reporting)_

### Workflow & process (0)

_No unit carries this as its primary category._

### Plugin scaffolding & UI (9)

- **DW16-27 · [PatientPhoto](probes/DW16-27-patient-photo.md)** · WPF binary-plugin template using Entity Framework DB access · 2 · `…/katas/Advanced.X/PatientPhoto`
- **DW14-02 · [MVVM_Demo](probes/DW14-02-mvvm-print-report.md)** · Demonstrate MVVM-pattern WPF app printing a treatment-plan report · 2 · `…/Developer Workshop 2014/guru track projects/MVVM` _(also Reporting)_
- **DW14-04 · [SimpleUIDemoApp](probes/DW14-04-simple-ui-selection-box.md)** · Reusable generic selection-box UI for Eclipse data objects · 3 · `…/Developer Workshop 2014/guru track projects/SimpleUIDemoApp`
- **DW18-09 · [ESAPIX_Demos](probes/DW18-09-esapix-demos.md)** · Demonstrate the ESAPIX facade library for ESAPI access and DVH queries · 3 · `…/Developer Workshop 2018/ESAPIX-Demo` _(also DVH)_
- **W2001-05 · [sampleLauncher](probes/W2001-05-sample-launcher.md)** · Launch a standalone exe from Eclipse passing patient/course/plan context · 2 · `…/16 Jan 2020 Webinar`
- **W1504-05 · [hello](probes/W1504-05-hello.md)** · Display a hello-world message box with current user · 1 · `…/21 Apr 2015 Webinar/…/Plugins/hello.cs`
- **W1504-06 · [test](probes/W1504-06-test.md)** · Show the active plan ID in a message box · 1 · `…/21 Apr 2015 Webinar/…/Plugins/test.cs`
- **ESAP-07 · [PluginTester](probes/ESAP-07-plugin-tester.md)** · Debug and run binary plugins standalone outside Eclipse · 5 · `Eclipse Scripting API/projects/PluginTester`
- **ESAP-10 · [Uab.VMS.Console](probes/ESAP-10-esapi-repl-console.md)** · Interactive C# REPL console for live ESAPI scripting with completion · 5 · `Eclipse Scripting API/projects/Uab.VMS.Console`

### Machine & commissioning (0)

_No primary member; appears only as W2103-01's secondary (beam scan data)._

### Research & algorithmic (2)

- **RS15-02 · [EUDScript](probes/RS15-02-eud-tcp-ntcp.md)** · Compute EUD-based TCP/NTCP from plan DVHs via Gay-Niemierko · 4 · `…/Research Symposium 2015/…/EUDScript` _(also DVH)_
- **ESAP-08 · [RBEReport](probes/ESAP-08-rbe-report.md)** · Generate a proton radiobiological-effect PDF report and post to ARIA · 4 · `Eclipse Scripting API/projects/RBEReport` _(also Reporting)_

### Other (0)

_None — every unit fit a defined category._

## Duplicate & evolution clusters

Groups of units solving the same problem across events. **Use** = the best/latest exemplar
(linked to its probe); the rest are "see also."

1. **DVH metric extraction (D-at-V / V-at-D tables → CSV).** Use
   **[W1811-01](probes/W1811-01-digging-into-dvh.md)** (DiggingIntoDVH — broadest: native + ESAPIX
   metrics, constraints, cohort mining, plotting). See also DW16-01, DW16-08, DW16-15, DW14-05,
   W2001-03, ESPL-01, ESAP-03 (best for batch/offline).

2. **DVH constraint / template evaluation (CSV/template → pass-fail report).** Use
   **[ESAP-06](probes/ESAP-06-plan-quality-metrics.md)** (PlanQualityMetrics — configurable
   XML/XSLT HTML engine) or **[W2008-01](probes/W2008-01-dvh-evaluator.md)** (DVH_Evaluator — adds
   multi-plan comparison GUI). See also DW16-02, DW16-09.

3. **DVH plotting / charts.** Use **[W2001-02](probes/W2001-02-dvh-plot.md)** (DVHPlot — clean
   OxyPlot MVVM). See also W1712-01 (canvas-drawn), ESAP-04 / ESPL-03 (browser HTML chart — same
   author, project vs single-file).

4. **Dose profile / line-dose extraction.** Use **[ESAP-11](probes/ESAP-11-profile-samples.md)**
   (ProfileSamples — adds gamma analysis). See also DW14-07, DW18-07 (near-identical
   line-profile-to-CSV).

5. **EQD2 / BED / biological-dose correction.** Use
   **[W1504-02](probes/W1504-02-eqd2-plan-sum-pdr.md)** (EQD2_2 — plan sums + PDR brachy) for EQD2;
   **[DW16-18](probes/DW16-18-dvh-bio-correction.md)** (DvhBioCorrection) for dataset-wide LQ DVH
   correction. See also W1504-01, RS15-02 (EUD/TCP/NTCP angle).

6. **Radiobiological PDF report → ARIA.** Use **[ESAP-08](probes/ESAP-08-rbe-report.md)** (RBEReport,
   project form) ≈ **[W1504-04](probes/W1504-04-rbe-report.md)** (RBEReport, the interactive webinar
   version with editable α/β). Effectively the same tool.

7. **End-to-end automated planning (photon).** Use
   **[DW18-04](probes/DW18-04-automated-planning-mco.md)** (AutomatedPlanningDemo — MCO +
   verification + quality reporting, newest at v15.6) or
   **[RS15-01](probes/RS15-01-automated-planning-pipeline.md)** (the fullest prescription-to-QA
   pipeline). See also DW16-22 (VMAT), DW18-06 (compact AutoPlan), DW14-08 (Superplan), W1804-01
   (AP/PA only).

8. **End-to-end automated planning (proton).** Use
   **[DS23-01](probes/DS23-01-proton-features-demo.md)** (ProtonFeaturesDemo — full v18 IMPT with
   robust optimization). The proton counterpart to cluster 7; no competing duplicate.

9. **Verification / QA plan creation.** Use
   **[W1804-03](probes/W1804-03-create-verification-plan.md)** (CreateVerificationPlan — composite
   IMRT QA). See also DW16-12 (same problem, earlier).

10. **Control-point / MLC / beam-parameter reporting.** Use
    **[DW16-19](probes/DW16-19-control-point-report.md)** (A3_Plugin). See also DW16-20 (A3_StandAlone
    — same report, standalone twin, shares the probe), DW16-04, DW16-03.

11. **Optimization / control structures via margins & Boolean.** Use
    **[W1804-02](probes/W1804-02-create-opt-structures.md)** (CreateOptStructures). See also DW16-13
    (PTV rings), DW16-23, DW16-24 (body-section splits).

12. **DICOM C-MOVE retrieval (DCMTK).** Use **[ESAP-05](probes/ESAP-05-get-dicom-collection.md)**
    (GetDicomCollection, project) ≈ **ESPL-04** (single-file twin, shares the probe). See also
    **[DW14-01](probes/DW14-01-esapi-anon.md)** (ESAPIAnon — adds profile-driven anonymization, the
    richest of the three).

13. **3D structure/dose mesh export.** Use **[ESAP-02](probes/ESAP-02-export-3d.md)** (Export3D,
    project) ≈ **ESPL-02** (single-file twin, adds isodose/PLY/STL for 3D printing; shares the probe).

14. **ARIA web-service / external access (FHIR, AppRole, AAccess, document service).** Use
    **[DW18-01](probes/DW18-01-vais-aria-webservice.md)** (VAIS — OAuth/OIDC + FHIR, the template).
    See also DW18-02 (SQL app role), DW18-03 (FHIR patient data), DW18-05 (document service),
    W2003-01 (scheduling via ARIA Access REST).

15. **Patient / database data mining (cohort iteration → CSV/report).** Use
    **[ESAP-01](probes/ESAP-01-data-mining.md)** (DataMining — per-patient treatment report) or
    **[DW16-21](probes/DW16-21-data-mine-by-anatomy.md)** (Advanced_4 — anatomy-filtered dose/DVH
    export). See also DW16-11, DW14-06, ESAP-09 (TG-263 naming histogram), W1504-03 (brachy finder).

16. **Patient / plan summary report.** Use **[DW16-10](probes/DW16-10-patient-summary.md)**
    (PatientSummary — full treatment history). See also DW18-08 (PlanInfo), ESAP-01.

17. **Patient demographics → Excel.** Use **[DW16-06](probes/DW16-06-excel-demographics.md)**
    (MSExcelForm) ≈ **[DW16-07](probes/DW16-07-excel-demographics-binary.md)** (binary-plugin twin of
    the same export).

18. **MVVM / plugin scaffolding templates.** Use **[W2001-01](probes/W2001-01-dose-metric-mvvm.md)**
    (DoseMetricExample — fullest combined MVVM template). See also DW14-04 (reusable selection-box
    library), DW18-09 (ESAPIX facade), DW14-02 (print-report MVVM), DW16-27 (EF-backed WPF),
    W2001-05 (exe launcher).

19. **Proton DVH / uncertainty stats.** Use
    **[DW16-29](probes/DW16-28-29-proton-uncertainty-dvh.md)** (Proton2, D95%) with **DW16-28**
    (Proton1, max-dose) — paired uncertainty-DVH reporting exercises sharing one probe.

## Most interesting (top ~20)

Ranked by score, then judgment. Each Solution links to its probe.

| # | ID | Solution | Why it's worth attention |
|--:|---|---|---|
| 1 | DW18-04 | [AutomatedPlanningDemo](probes/DW18-04-automated-planning-mco.md) | Newest full photon auto-plan: MCO + verification plans + quality report |
| 2 | RS15-01 | [AutomatedPlanningDemo](probes/RS15-01-automated-planning-pipeline.md) | Fullest prescription→optimization→dose→QA pipeline in one script |
| 3 | DS23-01 | [ProtonFeaturesDemo](probes/DS23-01-proton-features-demo.md) | Repo's most complete proton automation; full v18 IMPT + robust optimization |
| 4 | DW16-22 | [Advanced_5](probes/DW16-22-automated-vmat-planning.md) | End-to-end automated VMAT (structures→beams→opt→calc), highest-leverage kata |
| 5 | ESAP-06 | [PlanQualityMetrics](probes/ESAP-06-plan-quality-metrics.md) | Configurable QUANTEC-style metric engine with HTML reporting; near-clinical plan check |
| 6 | ESAP-10 | [Uab.VMS.Console](probes/ESAP-10-esapi-repl-console.md) | Interactive ESAPI REPL with code completion; uniquely lowers exploration barrier |
| 7 | ESAP-07 | [PluginTester](probes/ESAP-07-plugin-tester.md) | Run/debug binary plugins outside Eclipse; major dev-loop accelerator |
| 8 | DW14-01 | [ESAPIAnon](probes/DW14-01-esapi-anon.md) | Full C-MOVE retrieval + profile-driven DICOM anonymization, the richest app |
| 9 | W1504-04 | [RBEReport](probes/W1504-04-rbe-report.md) | Interactive radiobiological report: editable α/β, PDF export, ARIA post |
| 10 | DW16-18 | [DvhBioCorrection](probes/DW16-18-dvh-bio-correction.md) | Linear-quadratic biological DVH correction across a multi-patient dataset |
| 11 | DW16-21 | [Advanced_4](probes/DW16-21-data-mine-by-anatomy.md) | Anatomy-driven cohort data-mining with dose/DVH CSV export |
| 12 | DW16-31 | [CustomPostProcessing](probes/DW16-31-proton-spot-mu-limits.md) | Energy-dependent spot-MU limit enforcement, a real proton spot-scanning need |
| 13 | W2008-01 | [DVH_Evaluator](probes/W2008-01-dvh-evaluator.md) | Template-driven DVH evaluation + multi-plan comparison + HTML report |
| 14 | W2001-01 | [DoseMetricExample](probes/W2001-01-dose-metric-mvvm.md) | Fullest combined-MVVM template; strongest scaffolding to lift |
| 15 | W1811-01 | [DiggingIntoDVH](probes/W1811-01-digging-into-dvh.md) | Broad DVH toolkit: native+ESAPIX, constraints, cohort mining, OxyPlot |
| 16 | DW14-03 | [RapidPlanEvaluation](probes/DW14-03-rapidplan-evaluation.md) | Standard-vs-RapidPlan two-plan comparison with biological dose metrics |
| 17 | ESAP-01 | [DataMining](probes/ESAP-01-data-mining.md) | Database-wide per-patient treatment-report generation |
| 18 | ESAP-05 | [GetDicomCollection](probes/ESAP-05-get-dicom-collection.md) | Clean DCMTK C-MOVE retrieval of a plan's full DICOM set |
| 19 | ESAP-02 | [Export3D](probes/ESAP-02-export-3d.md) | Structure/dose/bolus → 3D meshes for external viewers |
| 20 | RS15-02 | [EUDScript](probes/RS15-02-eud-tcp-ntcp.md) | EUD-based TCP/NTCP (Gay-Niemierko) from plan DVHs, reusable radiobiology |

Honorable mentions (score 4, not in top 20): DW16-09, DW16-12, DW16-16, DW16-17, DW16-19/20,
DW16-28/29/30, DW18-01, DW18-06, W1504-02, W1810-02, W2103-01, ESAP-03, ESAP-08, ESAP-09,
ESAP-11.

## Coverage ledger

| Metric | Count |
|---|---:|
| Event folders triaged | 16 / 16 |
| Units cataloged | 88 |
| Tracker baseline (`.sln` + standalone) | 80 + 4 = 84 |
| Overage | +4 |
| Probes written (distinct files) | 84 |
| Units with a probe | 88 / 88 |

**All 16 shards present and complete** — every event folder in the triage tracker is triaged,
and every unit now carries a `Probe` link in its registry row.

**Why 88 vs the ~84 baseline (+4):** four sub-units were catalogued as their own rows rather
than folded into a `.sln`:
- W2001-05 (`sampleLauncher.cs`) — root standalone launcher script, no `.sln`.
- W1504-05 / W1504-06 (`hello.cs`, `test.cs`) — two loose single-file plugin stubs, no `.sln`.
- ESAP-11 (`ProfileSamples`) — a `.csproj` with its own `Script.cs` Execute entry, no `.sln`.

These are genuine units (each its own entry point), not double-counts. Per-shard counts:
DW16 31, DW14 9, DW18 9, ESAP 11, W1504 6, W2001 5, W1804 3, RS15 2, W1810 2, and seven
single-unit folders (W2008, W2103, W1712, W1811, DS23, W2003 + nothing else) = 88.

**Probes: 88 units → 84 distinct files.** Four units are twins that share a probe with their
sibling: DW16-20 → DW16-19's probe (standalone twin of the control-point report); DW16-28 and
DW16-29 share one proton-uncertainty-DVH probe; ESPL-02 → ESAP-02 (Export3D project/single-file
siblings); ESPL-04 → ESAP-05 (GetDicomCollection project/single-file siblings). No unit is
without a deep dive.

**Known dedup decisions (already reconciled in shards, not gaps):** single-file `Plugins/*.cs`
twins of same-named `.sln` projects were skipped across DW14, DW18, W1504, W1804, RS15;
`DvhLookups` is catalogued once under ESPL (not double-listed in ESAP); the DW16
`visualscripting/` kata is no-code (excluded). The ESAP-02/ESPL-02, ESAP-04/ESPL-03,
ESAP-05/ESPL-04 pairs are deliberate project-vs-single-file siblings in *different* folders,
catalogued in both shards (see clusters 3, 12, 13).

**Gaps:** none. All 16 shards triaged, all 88 units cataloged, all 88 carry a probe link, and
every linked probe file exists under `probes/`. The companion [`probe_queue.md`](probe_queue.md)
holds the tier-ranked TOC and the per-event presenter/date reference.
