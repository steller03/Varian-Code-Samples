# ESAP-06 — PlanQualityMetrics (configurable QUANTEC-style plan check)

| Field | Value |
|---|---|
| ID | ESAP-06 |
| Solution | PlanQualityMetrics |
| Source event | Eclipse Scripting API — projects |
| ESAPI version | v11 / v13 (compile-time `v13_ESAPI` flag) |
| Type | Binary plugin (`Execute(ScriptContext)`) |
| Reuse verdict | Liftable |

## Problem
A physicist wants an automated, **clinic-configurable** plan-quality report: evaluate a calculated plan
(or plan sum) against a library of dose/volume constraints (QUANTEC-derived), classify each as
PASS/WARN/FAIL, and produce a formatted, shareable report. This is the repo's closest thing to a real
second-check / plan-quality engine, and the metric definitions are pure data, so a clinic can retune it
without touching the evaluation code.

## Approach
A clean three-layer design — **metrics as data → calculators → reporter → XSLT** — that's the reusable idea:
1. **Metrics as data (`UserDefinedMetrics.cs`)** — each OAR is a static class with a `PQMs[]` array of metric
   objects and a `searchIds[]` list of clinic name variants (case-insensitive). E.g. Rectum carries
   `V50<50%, V60<35%, …`; targets get a coverage metric parameterized by prescription. Adding/retuning a
   constraint is editing this file — no logic changes.
2. **Calculators (`PQMs.cs`)** — four structs implement a `PlanQualityMetric` interface
   (`addPQMInfo(PlanningItem, Structure, XmlWriter)`): `VolumeAtDose`, `DoseAtVolume`, `MaxDoseLimit`,
   `MeanDoseLimit`. Each computes its value via DVH (`GetVolumeAtDose`/`GetDoseAtVolume` extensions, or
   `GetDVHCumulativeData(...).MaxDose/MeanDose`), compares to the constraint with an upper/lower tolerance
   multiplier, and emits a `<PQM>` element with the calculated value and a PASS/WARN/FAIL verdict
   (WARN = over limit but within tolerance band, FAIL = past the band).
3. **Reporter (`PQMReporter.cs`)** — abstract base with `PlanSetupReporter` / `PlanSumReporter` subclasses.
   `generateReport` writes `%TEMP%\<patientId>\PQMReport-<planId>.xml`, matches each structure in the set
   against the `searchIds` registry, invokes its metrics, then runs an `XslCompiledTransform` to produce HTML.
   The XSLT stylesheets (`gen_report.xsl` / `gen_report_plansum.xsl`) ship as **embedded resources**, loaded
   via `Assembly.GetManifestResourceStream`. The `v13_ESAPI` compile flag adds a synthesized "Parotid Combined"
   structure (create → evaluate → remove) not possible in v11.
4. **Entry (`PlanQualityMetrics.cs`)** — validates scope (plan/plansum has structure set + dose), picks the
   right reporter + stylesheet, generates the report, and `Process.Start`s the HTML to open it in a browser.

## ESAPI surfaces
- **Scope:** `ScriptContext.PlanSetup`, `PlanSumsInScope`, `PlanSetup.StructureSet`, `Dose`, `CurrentUser.Id`
- **Metrics:** `PlanningItem.GetDoseAtVolume`, `GetVolumeAtDose`, `GetDVHCumulativeData(Structure,
  DoseValuePresentation, VolumePresentation, binWidth)` → `DVHData.MaxDose/MeanDose`
- **Types:** `DoseValue` (+`DoseUnit`), `VolumePresentation` (Relative / AbsoluteCm3), `DoseValuePresentation`,
  `Structure.Id`, `PlanSum.StructureSet`
- **Non-ESAPI plumbing:** `System.Xml` `XmlWriter`/`XElement`, `System.Xml.Xsl.XslCompiledTransform`,
  embedded-resource stylesheets, `Assembly.GetName().Version` for version stamping

## Reusability
Highly liftable — the **metric-as-data + interface-based calculators + XML→XSLT report** architecture is the
prize and is largely ESAPI-version-agnostic (only the v13 combined-parotid block and the DVH-extension helpers
need attention). To adopt: replace `UserDefinedMetrics` content with your clinic's constraints and the
`searchIds` with your TG-263 naming, and restyle the XSLT. Caveats: it only wires up Prostate and H&N metric
sets (you extend `WriteDoseStatisticsXML_*` to add sites), it depends on the bundled `DvhExtensions`
`GetDoseAtVolume`/`GetVolumeAtDose` wrappers, and the `GetDVHCumulativeData` bin-width/relative-volume calls
are the v11/v13 idiom — fine on modern ESAPI but worth confirming. Output and browser-launch assume a Windows
clinical workstation.

## Idea sparks
- A clinic plan-check plugin: swap in your constraint table + TG-263 `searchIds`, run at plan approval, archive
  the HTML/XML to the patient's documents.
- A batch QA dashboard: drive the reporter headlessly across a cohort and aggregate the XML PASS/WARN/FAIL
  results into a population plan-quality scorecard.
- A protocol-compliance gate: extend the metric structs (e.g. conformity/homogeneity indices) and fail-gate
  approval automation on any FAIL.
