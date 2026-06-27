# DW14-04 — SimpleUIDemoApp (reusable generic selection-box library for ESAPI objects)

**Cluster 18 delta** — exemplar [W2001-01 DoseMetricExample](W2001-01-dose-metric-mvvm.md).

- **Problem:** ship a reusable WPF library (`ESAPISimpleUI`) that pops a generic selection dialog —
  list-box or data-grid — over *any* collection of Eclipse `ApiDataObject`s (pick a Course /
  PlanSetup / Structure / Beam / StructureSet) and returns the chosen items, plus a fuller MVVM
  `DemoApp` that consumes it.
- **Differs from the exemplar:** this is the **2014 (v13.5) hand-rolled MVVM** answer to the same
  "structure a reusable ESAPI UI" problem that W2001-01 solves with the modern Autofac + Prism +
  OxyPlot stack. The reusable asset is a **type-dispatching ViewModel factory**
  (`ViewModelFactory.CreateViewModel` switches on the `ApiDataObject` runtime type → a typed VM)
  feeding a generic `ListBoxWindow(title, label, SelectionMode, ViewType, IEnumerable<ApiDataObject>)`
  that exposes `SelectedItems`. No DI container and no event aggregator — classic `ViewModelBase` /
  `RelayCommand` and a `ViewType` enum to pick list-box vs data-grid.
- **Surfaces it adds:** `VMS.TPS.Common.Model.API.ApiDataObject` — the common base type used for the
  generic runtime dispatch; the rest is WPF/MVVM plumbing.
- **Reuse note:** genuinely liftable — the `ListBoxWindow` generic selection dialog plus the
  `ApiDataObject → VM` factory are a handy "let the user pick an ESAPI object" widget you can drop
  into any plugin, lighter than the full W2001-01 scaffolding. Caveat: it's v13.5-era hand-rolled
  MVVM; if you want DI/testability, modernize it with the Prism/Autofac idioms from W2001-01. Verdict
  Adaptable.
