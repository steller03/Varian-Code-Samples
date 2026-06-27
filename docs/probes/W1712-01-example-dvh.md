# W1712-01 — Example_DVH (canvas-drawn DVH plot + DQM template table)

**Cluster 3 delta** — exemplar [W2001-02 DVHPlot](W2001-02-dvh-plot.md).

- **Problem:** an in-Eclipse plugin that lets a user tick structures and draws their cumulative DVH
  curves, plus a combo-box that fills a dose-quality-metric (DQM) template table.
- **Differs from the exemplar:** the **hand-drawn-canvas** version of the DVH plot (vs W2001-02's
  clean OxyPlot/MVVM). It uses the legacy parameterized `Script.Run(User, Patient, Image,
  StructureSet, PlanSetup, …, Window)` entry, bridged from `Execute(ScriptContext, Window)`. Per
  structure it builds a `CheckBox` whose `Checked` handler calls
  `GetDVHCumulativeData(s, Absolute, Relative, 1)`, then `DrawDVH` manually scales each `CurveData`
  point to canvas pixels (`Canvas.Width / Dose.DoseMax3D`, `Height / 100`) and adds WPF `Line`
  segments colored by `Structure.Color` — no plotting library, no pan/zoom/export. A `Models/DQM.cs`
  drives a `DataGrid` of `GetDoseAtVolume` lookups from a named template, a metric-table slice
  W2001-02 leaves to its sibling DoseMetrics.
- **Surfaces it adds:** `Dose.DoseMax3D` (manual axis scaling), `PlanSetup.GetDoseAtVolume` (DQM
  table), and the legacy `Script.Run(...)` parameterized entry signature.
- **Reuse note:** prefer W2001-02's OxyPlot MVVM for any new plot — the `Line`-on-`Canvas` drawing
  here is illustrative and lacks interaction/export, though it is a dependency-free fallback when
  OxyPlot can't be referenced. The reusable ideas are the checkbox-per-structure →
  `GetDVHCumulativeData` wiring and the DQM-template `DataGrid`. Verdict Adaptable (the plot drawing,
  Illustrative).
