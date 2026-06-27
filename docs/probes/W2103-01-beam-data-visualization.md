# W2103-01 — BeamDataVisualization (synthetic beam scans from ESAPI dose profiles, charted in OxyPlot)

| Field | Value |
|---|---|
| ID | W2103-01 |
| Solution | BeamDataVisualization |
| Source event | 31 Mar 2021 Webinar — Beam Data Visualization |
| ESAPI version | v15.6 |
| Type | Standalone exe (`Application.CreateApplication`) |
| Reuse verdict | Adaptable |

## Problem
A physicist commissioning or QA-ing a machine wants to review beam scan profiles — percentage depth-dose, crossline, and diagonal profiles — pulled from a calculated plan, sorted by energy, field size, and scan type. This app navigates to a plan in a virtual-phantom verification setup, samples its 3D dose into 1-D scans, charts them interactively with togglable grouping, and exports each scan to CSV for offline comparison against measured tank-scan or golden-beam data.

## Approach
The architecture is lighter than the canonical W2001-01 build: there is no Autofac and no Prism regions/modules — `App.Application_Startup` parses the `"patId;course;plan"` arg string, calls `VMS.TPS.Common.Model.API.Application.CreateApplication()`, news up a single `EventAggregator`, and hand-wires two child ViewModels into `MainViewModel` (a plain aggregator) via constructor injection. The live `Application` object is passed straight into `PatientNavigationViewModel`. ViewModels derive from Prism's `BindableBase` and use `DelegateCommand`; the one Prism pattern doing real work is the **event aggregator**. `PatientNavigationViewModel` walks `Patient.Courses` → `Course.PlanSetups` (selection cascades through `SelectedCourse`/`SelectedPlan` setters), and when a plan is selected it publishes a `PlanSelectedEvent : PubSubEvent<PlanSetup>`. `ScanPlotViewModel` subscribes in its constructor and never references the navigation VM directly — the only coupling between the two panes is the typed event.

The interesting move is that the "scan data" is **not** read from a commissioning beam-data API; it is **synthesized from the plan's calculated 3D dose** via `Beam.Dose.GetDoseProfile(start, end, double[])`. For each beam, `ScanPlotViewModel.PlanSelected` derives field size from `Beam.ControlPoints.First().JawPositions` (X1/X2/Y1/Y2, /10 to cm), reads a per-energy `d_max` depth and a `PhantomThickness` from `App.config` `AppSettings`, and builds `VVector` start/end pairs (with a beam-divergence scaling factor `(1000+depth*10)/1000`) to sample crossline profiles at several depths, a diagonal profile, and a PDD along the central axis. Each profile's `ProfilePoint`s are copied into a `BeamScanModel` (carrying `Energy`, `BeamScanTypeEnum`, `FieldX/Y`, `Depth`) holding a list of `BeamDataPointModel` (Position, DoseValue). `SetPlotModels` then builds OxyPlot `PlotModel`s on the fly, grouping by two boolean toggles (`bScanType`, `bFieldSize`) via LINQ `GroupBy(x => x.BeamScanType)` / `GroupBy(x => x.FieldX)` — four grouping modes total — normalizing each curve (`Max` dose for PDDs, central-axis value for profiles) to percent before adding `LineSeries`. Export (`OnExportScans`) writes one `Position,Dose` CSV per scan via a `SaveFileDialog`.

## ESAPI surfaces
- Scope/boot: `Application.CreateApplication`, `Application.OpenPatientById`, `ClosePatient`, `Dispose`
- Navigation: `Patient.Courses`, `Course.PlanSetups`, `PlanSetup`, `PlanSetup.Beams`
- Beam geometry: `Beam.EnergyModeDisplayName`, `Beam.ControlPoints` → `ControlPoint.JawPositions` (`X1/X2/Y1/Y2`)
- Dose sampling (the core call): `Beam.Dose.GetDoseProfile(VVector start, VVector stop, double[] preallocatedBuffer)` → `DoseProfile` of `ProfilePoint` (`.Position`, `.Value`)
- Types: `VVector` (`.x/.y/.z`), `VMS.TPS.Common.Model.Types`
- Non-ESAPI plumbing: Prism (`BindableBase`, `DelegateCommand`, `EventAggregator`, `PubSubEvent<T>`), OxyPlot (`PlotModel`, `LineSeries`, `LinearAxis`, `DataPoint`), `ConfigurationManager.AppSettings`, `SaveFileDialog`/`StreamWriter`

## Reusability
The liftable asset is the **scaffold, not the algorithm**: the standalone `CreateApplication` + arg-string boot, the patient/course/plan cascade in `PatientNavigationViewModel`, the `PubSubEvent<PlanSetup>` decoupling between a navigation pane and a plot pane, and the OxyPlot-driven `SetPlotModels` pattern that rebuilds chart models from a grouping toggle. All of that is version-agnostic and drops into any v15+ desktop tool. `Beam.Dose.GetDoseProfile` and the `JawPositions`/`ControlPoints` navigation are likewise current and reusable as a generic "sample dose along a line" primitive.

What you'd port or harden: this is **not** a reader of stored commissioning/measured beam data — it manufactures profiles from a *calculated* plan that must already have valid 3D dose (`Beam.Dose` is null otherwise; there is no null guard), and the geometry assumes a specific water-phantom verification plan with the beams arranged so the divergence/shift math holds. The magic constants — `PhantomThickness`, per-energy `d_max` keyed by `EnergyModeDisplayName` in `App.config`, the `±50 mm` jaw padding, the `(1000+depth*10)/1000` SSD/divergence factor, fixed depths `{5,10,20,30}` cm — are all clinic/phantom-specific and must be re-derived for your setup. `GetNormFromScan` and `FirstOrDefault(x => x.Position >= 0)` can divide-by-zero / NRE on sparse profiles. Treat the DI as illustrative: there's no container, so for an in-Eclipse binary plugin you'd inject `ScriptContext` and delete the `OpenPatientById` plumbing. No deprecated calls.

## Idea sparks
- Generalize the navigation-VM + `PubSubEvent<PlanSetup>` + OxyPlot-grouping shell into a reusable house template for any ESAPI "pick a plan, plot something" data explorer.
- Wrap `GetDoseProfile` sampling + CSV export into a machine-data trending / QA dashboard that batch-exports profiles across a cohort of verification plans for periodic-QA drift tracking.
- Diff the exported CSVs against measured tank scans or golden-beam-data to flag commissioning/beam-model deviations automatically.
