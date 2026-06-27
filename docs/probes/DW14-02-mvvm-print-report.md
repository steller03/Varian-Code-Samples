# DW14-02 — MVVM_Demo (standalone MVVM/WPF app with multipage report printing)

**Tier D lightweight.** Standalone MVVM/WPF demo that opens a `DVHPlot` window (OxyPlot) from a stand-alone
ESAPI exe and demonstrates multipage report printing through a `DocumentPaginator` (`PrintReport.cs`);
much of the data-mining / `DrawDVH` body is commented out, leaving the scaffolding as the point.

- **ESAPI surface:** the standalone `Application.CreateApplication(args[0], args[1])` entry, and
  `PlanSetup.GetDVHCumulativeData` inside the `DrawDVH` helper.
- **Pointer:** an early MVVM-scaffolding + print-report sample — cluster 18 (exemplar [W2001-01
  DoseMetricExample](W2001-01-dose-metric-mvvm.md)).
