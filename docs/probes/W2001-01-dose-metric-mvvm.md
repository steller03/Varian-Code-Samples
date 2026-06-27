# W2001-01 — DoseMetricExample (canonical MVVM ESAPI WPF scaffolding)

| Field | Value |
|---|---|
| ID | W2001-01 |
| Solution | DoseMetricExample (combined MVVM ESAPI app) |
| Source event | 16 Jan 2020 Webinar |
| ESAPI version | v15.6 (header says "Eclipse V115.6 MR3") |
| Type | Binary plugin (WPF/MVVM, standalone Application_Startup) |
| Reuse verdict | Adaptable |

## Problem
A physicist wants an interactive plan-review surface: pick structures to plot on a DVH, build ad-hoc dose metrics (D at volume, V at dose) with pass/fail tolerances, and see prescription / dose-calculation parameters — all in one window, savable as a reusable metric template. More importantly for the catalogue, this is the webinar's reference build for *how to structure a maintainable ESAPI WPF plugin* (DI container, MVVM, event aggregator) instead of a code-behind monolith.

## Approach
The prize is the architecture, not the dose math. The app boots as a standalone WPF `Application` (not the `Script.Execute` entry point): `App.Application_Startup` calls `VMS.TPS.Common.Model.API.Application.CreateApplication()`, parses `e.Args[0]` (a `"patId;course;plan"` string) to `OpenPatientById` → `Courses` → `PlanSetups`, then hands the resolved `PlanSetup` to a `Bootstrapper`.

- **DI / composition root** (`Startup/Bootstrapper.cs`) — uses **Autofac**. Registers every View and ViewModel, registers `EventAggregator` as a singleton `IEventAggregator`, and crucially `RegisterInstance<PlanSetup>(plan)` so the live ESAPI object is constructor-injected everywhere. `container.Resolve<MainView>()` + `Resolve<MainViewModel>()` wires the tree.
- **MVVM** — ViewModels derive from Prism's `BindableBase` (`SetProperty`), commands are Prism `DelegateCommand` with `CanExecuteChanged` gating (`DoseMetricSelectionViewModel.AddMetricCommand`). `MainViewModel` is a pure aggregator holding the five child VMs.
- **Event-aggregator decoupling** (Prism `PubSubEvent<T>`) — `StructureSelectionEvent` carries a `StructureSelectionModel`; toggling its `bIsChecked` setter publishes, and `DVHViewModel` subscribes to add/remove the curve. `AddDoseMetricEvent` carries a `DoseMetricModel`; `DoseMetricSelectionViewModel` publishes, `DoseMetricViewModel` appends to its `ObservableCollection`. Selection VMs never touch the plot/table VMs directly.
- **DVH → OxyPlot** (`DVHViewModel`) — on selection, `_plan.GetDVHCumulativeData(structure, DoseValuePresentation.Absolute, VolumePresentation.Relative, 1)`, then iterates `dvh.CurveData` into an OxyPlot `LineSeries` (`DataPoint(point.DoseValue.Dose, point.Volume)`), coloring from `structure.Color`. View binds `oxy:PlotView Model="{Binding DVHPlotModel}"`.
- **Dose metrics** (`Models/DoseMetricModel.GetOutputValue`) — branches on metric name: `_plan.GetDoseAtVolume(...).Dose` or `_plan.GetVolumeAtDose(...)`, units chosen via `VolumePresentation`/`DoseValuePresentation` ternaries, tolerance parsed from a `<`/`>`/`=` string into a `ToleranceMet` bool (driving `PassFailColorConverter` → green/pink).
- **Rx / calc params** (`DoseParametersViewModel`) — surfaces `DosePerFraction`, `NumberOfFractions`, `TotalDose`, `TreatmentPercentage`, `GetCalculationModel(CalculationType.PhotonVolumeDose)`, and scrapes grid size / heterogeneity / DLG / leaf transmission out of `Beams.CalculationLogs` `MessageLines`.
- Templates persist via Newtonsoft JSON of the `DoseMetricModel` list; `MainViewModel.OnPrint` renders the VMs into a `FlowDocument` and exports the plot via OxyPlot `PngExporter`.

## ESAPI surfaces
- Scope/boot: `Application.CreateApplication`, `OpenPatientById`, `Patient.Courses`, `Course.PlanSetups`, `PlanSetup`
- Structures: `PlanSetup.StructureSet.Structures`, `Structure.Id/Color/IsEmpty/DicomType`, `StructuresSelectedForDvh`
- DVH/metrics: `GetDVHCumulativeData`, `DVHData.CurveData` (`.DoseValue.Dose`, `.Volume`), `GetDoseAtVolume`, `GetVolumeAtDose`
- Types: `DoseValue` (+`DoseValue.DoseUnit`), `DoseValuePresentation`, `VolumePresentation`, `CalculationType`
- Plan params: `DosePerFraction`, `TotalDose`, `NumberOfFractions`, `TreatmentPercentage`, `GetCalculationModel`, `Beams`, `Beam.CalculationLogs.MessageLines/Category`, `Beam.IsSetupField`
- Non-ESAPI plumbing: Autofac (`ContainerBuilder`, `RegisterType`/`RegisterInstance`), Prism (`BindableBase`, `DelegateCommand`, `IEventAggregator`, `PubSubEvent<T>`), OxyPlot (`PlotModel`, `LineSeries`, `PlotView`, `PngExporter`), Newtonsoft.Json

## Reusability
The scaffolding is the liftable asset: the Autofac composition root, the `RegisterInstance<PlanSetup>` trick that injects the live ESAPI object into VMs, and the event-aggregator pattern that keeps selection VMs ignorant of the plot/table VMs. Copy `Bootstrapper`, the `PubSubEvent<T>` pair, and the `BindableBase`/`DelegateCommand` idioms wholesale into any v15+ plugin — none of it is version-fragile. The DVH→OxyPlot translation loop is also drop-in.

What you'd change: the `App.Application_Startup` boot is the *standalone* launcher (parses a `patId;course;plan` arg string and calls `CreateApplication`); for an in-Eclipse binary plugin you'd instead inject `ScriptContext.PlanSetup` from a `Script.Execute` shim and delete the `OpenPatientById` plumbing. `GetCalculationModel` and `CalculationLogs` log-scraping are brittle (string `Split('=')`, exact label matches, `MessageLines.FirstOrDefault(... Contains ...)` will NPE if absent) and the algorithm log keys differ by version/algorithm — treat as illustrative. Tolerance parsing assumes well-formed `<n`/`>n` strings and throws otherwise. No deprecated calls; `GetDVHCumulativeData`/`GetDoseAtVolume`/`GetVolumeAtDose` remain current.

## Idea sparks
- Use the Autofac + event-aggregator skeleton as the house template for every new review/QA plugin, so selection panels, plots, and report tables stay independently testable.
- Extend the JSON metric-template save/load into a clinic-wide constraint library (per-site `.json`), loaded headlessly to batch-score a cohort.
- Reuse the `Beams.CalculationLogs` scrape — hardened with key/algorithm lookups — as a standalone "calc parameter audit" check across plans.
