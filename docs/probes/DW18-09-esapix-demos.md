# DW18-09 — ESAPIX_Demos (showcase of the ESAPIX facade/helper library)

**Cluster 18 delta** — exemplar [W2001-01 DoseMetricExample](W2001-01-dose-metric-mvvm.md).

- **Problem:** demonstrate **ESAPIX**, a third-party facade over ESAPI that adds a managed STA-thread
  context, Mayo-format DVH query strings, a cohort DVH "miner," and facade serialization for
  offline / unit-test development.
- **Differs from the exemplar:** not an MVVM app — a set of console demos over the ESAPIX library, so
  it answers "scaffolding" from the *library* angle rather than W2001-01's WPF-template angle. Key
  moves: `StandAloneContext(() => Application.CreateApplication())` wraps ESAPI so calls marshal onto
  the correct STA thread via `sac.Thread.Invoke(...)` — letting you `await Task.Run` against a facade
  where raw ESAPI throws (the demo deliberately contrasts `MultithreadDemo` vs `MultithreadFailDemo`).
  `firstPlan.ExecuteQuery("D99%[Gy]", ptv)` runs Mayo-syntax DVH queries; a `Miner` with
  `StructureQuery` specs + a `CsvFile` of patient IDs mines cohort DVH metrics to CSV; and
  `FacadeSerializer.Serialize/Deserialize<PlanSetup>` detaches an ESAPI object to JSON for unit
  testing.
- **Surfaces it adds (ESAPIX, wrapping ESAPI):** `ESAPIX.Common.StandAloneContext` / `Thread.Invoke`,
  `ESAPIX.Facade.API`, `FacadeSerializer`, `ExecuteQuery` (Mayo string), `ESAPIX.Helpers.DVH.Miner` /
  `StructureQuery`, `MagicStrings.DICOMType` — over the usual
  `Application.CreateApplication` / `OpenPatientById` / `GetDVHCumulativeData`.
- **Reuse note:** ESAPIX itself is the takeaway — the STA-thread `StandAloneContext` (fixes the #1
  standalone-ESAPI threading pitfall), Mayo `ExecuteQuery` strings, and facade serialization for
  testable/offline dev are all worth adopting. It's an external, non-Varian-supported dependency, so
  vet and pin a version; for the *UI* side, a v15+ native stack like W2001-01 needs no third party.
  Verdict Illustrative (the library it teaches is Adaptable).
