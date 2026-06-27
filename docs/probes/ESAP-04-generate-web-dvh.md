# ESAP-04 — GenerateWebDVH (browser HTML/JS DVH chart via Google Charts)

**Cluster 3 delta** — exemplar [W2001-02 DVHPlot](W2001-02-dvh-plot.md). Project-folder unit that
compiles the same `plugins/GenerateWebDVH.cs` as its single-file twin **ESPL-03**.

- **Problem:** render the cumulative DVHs of selected structures as an interactive chart a physicist
  can open in a web browser, instead of inside the Eclipse plugin window.
- **Differs from the exemplar:** W2001-02 plots in-app with OxyPlot/MVVM; this writes a self-contained
  **HTML file** and shells it to the browser. Per structure it calls `GetDVHCumulativeData(..., Absolute,
  Relative, 0.1)`, packs the dose/volume points into a JavaScript `arrayToDataTable` matrix, emits the
  page with `XmlWriter` + `XElement` to `%TEMP%`, then `Process.Start`s it. The plot itself is drawn by
  **Google Charts `LineChart`** loaded from `https://www.google.com/jsapi`. Structure ids are hardcoded
  (line 64: `Parotid LT`/`Parotid RT`).
- **Surfaces it adds:** none beyond the exemplar's DVH calls — `PlanSetup.GetDVHCumulativeData`,
  `DVHData.CurveData`, `DVHPoint.DoseValue/Volume`. The novelty is non-ESAPI: `System.Xml`
  (`XmlWriter`/`XElement`) HTML generation and the Google Charts embed.
- **Reuse note:** the *idea* (export a DVH as a portable HTML chart) is reusable, but this implementation
  is **obsolete** as-is — `google.com/jsapi` is long deprecated/dead, it is Chrome-and-internet-only, and
  the structures are hardcoded. Lift the GetDVHCumulativeData → JS-matrix shaping but swap Google Charts
  for a modern offline JS lib (Chart.js/Plotly) or just use W2001-02's OxyPlot. ESPL-03 is the identical
  single-file version.
