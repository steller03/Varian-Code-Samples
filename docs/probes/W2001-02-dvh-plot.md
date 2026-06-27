# W2001-02 — DVHPlot (event-driven DVH→OxyPlot, the plot slice of the MVVM trio)

| Field | Value |
|---|---|
| ID | W2001-02 |
| Solution | DVHPlot (16 Jan 2020 "SeparatedApps") |
| Source event | 16 Jan 2020 Webinar |
| ESAPI version | v15.6 ("Eclipse V115.6 MR3") |
| Type | Binary plugin (WPF/MVVM, `Execute(ScriptContext, Window, ScriptEnvironment)`) |
| Reuse verdict | Adaptable |

## Problem
Let a user tick structures and see their cumulative DVH curves overlaid, live, inside an Eclipse binary plugin — built the maintainable MVVM way rather than as code-behind. This is one of three single-purpose "SeparatedApps" the 16 Jan 2020 webinar later fuses into the combined `DoseMetricExample` (W2001-01); it isolates the **DVH-plot** slice so the Autofac + Prism-event wiring is legible on its own.

## Approach
`Script.Execute` is a thin shim: if `context.PlanSetup != null` it calls `Bootstrapper.Bootstrap(plan)` and drops the resolved `MainView` into the host `window.Content` (plus the well-known `OxyPlot.Wpf.AngleAxis` dummy instantiation that forces the OxyPlot.Wpf assembly to load for a binary plugin). `Bootstrapper` is an Autofac composition root: `RegisterType`s the views/VMs, registers `EventAggregator` as a single-instance `IEventAggregator`, and `RegisterInstance(plan)` so the live `PlanSetup` is constructor-injected everywhere.

Two VMs, decoupled only by an event. `DVHSelectionViewModel` builds an `ObservableCollection<StructureSelectionModel>` from `plan.StructureSet.Structures`, filtering empties and `MARKER`/`SUPPORT` DICOM types and pre-checking those already in `plan.StructuresSelectedForDvh`. Toggling a model's checkbox publishes a `StructureSelectionEvent`. `DVHViewModel` subscribes; on check it resolves the structure, calls `GetDVHCumulativeData(s, Absolute, Relative, 1)`, and builds an OxyPlot `LineSeries` (points `DataPoint(dvhPoint.DoseValue.Dose, dvhPoint.Volume)`, color from `Structure.Color` via `OxyColor.FromArgb`); on uncheck it removes the series by title. Axes/legend are configured once; `InvalidatePlot(true)` refreshes.

## ESAPI surfaces
- Entry: `Script.Execute(ScriptContext, Window, ScriptEnvironment)`, `ScriptContext.PlanSetup`
- `PlanSetup.StructureSet.Structures`, `Structure.Id/Color/IsEmpty/DicomType`, `PlanSetup.StructuresSelectedForDvh`, `PlanSetup.DosePerFraction.UnitAsString`
- `PlanSetup.GetDVHCumulativeData` → `DVHData.CurveData`, `DVHPoint.DoseValue.Dose` / `.Volume`
- Enums `DoseValuePresentation.Absolute`, `VolumePresentation.Relative`
- Non-ESAPI: Autofac (`ContainerBuilder`, `RegisterType`/`RegisterInstance`), Prism (`BindableBase`, `IEventAggregator`, `PubSubEvent`), OxyPlot (`PlotModel`, `LineSeries`, `LinearAxis`, OxyPlot.Wpf)

## Reusability
The DVH→`LineSeries` translation loop and the `RegisterInstance(plan)` DI trick lift verbatim into any v15+ plugin and aren't version-fragile. The `IsEmpty`/`DicomType` structure filter and the `StructuresSelectedForDvh` pre-check are reusable hygiene. Because this is the separated precursor to W2001-01, the full architectural treatment (Autofac root, event-aggregator decoupling) lives in that probe — here it's the minimal, copyable plot slice. The `AngleAxis` dummy is a genuine binary-plugin gotcha (forces OxyPlot.Wpf to load) worth remembering. Hardcoded bin width 1 and relative-volume presentation are the obvious knobs.

## Idea sparks
- Use this as the drop-in DVH panel for any review plugin; publish the selection event from a plan-comparison list to overlay plan-vs-plan curves.
- Add a `Differential()` toggle or a `PngExporter` export to make it report-ready.
- Reuse the structure-filter predicate (`!IsEmpty && DicomType != MARKER/SUPPORT`) as the house standard for "structures worth showing."
