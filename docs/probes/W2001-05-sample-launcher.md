# W2001-05 — sampleLauncher (shell a standalone exe from Eclipse with context)

**Tier D lightweight.** Single-file script that `Process.Start`s a fixed standalone `.exe`, passing
`Patient.Id;Course.Id;PlanSetup.Id` as one quoted argument, so a full-trust WPF app can run outside the
Eclipse script sandbox.

- **ESAPI surface:** `Execute(ScriptContext)` reading `Patient.Id` / `Course.Id` / `PlanSetup.Id`; the
  work is `System.Diagnostics.Process.Start`.
- **Pointer:** the launcher half of the W2001 MVVM set (exemplar [W2001-01
  DoseMetricExample](W2001-01-dose-metric-mvvm.md)) — the standard "escape the script sandbox" trick.
