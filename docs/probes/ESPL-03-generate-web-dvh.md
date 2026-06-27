# ESPL-03 — GenerateWebDVH (single-file browser HTML/JS DVH chart)

**Tier D lightweight.** The single-file `plugins/` version of the browser DVH chart: writes the cumulative
DVHs of hardcoded structures to an HTML file embedding a Google Charts `LineChart`, then shells it to the
browser.

- **ESAPI surface:** `PlanSetup.GetDVHCumulativeData` → `DVHData.CurveData` → `DVHPoint.DoseValue/Volume`;
  the rest is `System.Xml` HTML generation + Google Charts.
- **Pointer:** identical-source twin of [ESAP-04 GenerateWebDVH](ESAP-04-generate-web-dvh.md) (project
  form) — cluster 3, exemplar [W2001-02 DVHPlot](W2001-02-dvh-plot.md). Obsolete as-is (dead
  `google.com/jsapi`, Chrome+internet only).
