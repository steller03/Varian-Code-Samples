# W1504-03 — FindBrachyPlans (database scan → list every brachytherapy plan)

**Cluster 15 delta** — exemplar [ESAP-01 DataMining](ESAP-01-data-mining.md).

- **Problem:** scan every patient in ARIA and print a locator (`patient/course/plan`) for every
  brachytherapy plan found — a one-purpose database census for brachy cases.
- **Differs from the exemplar:** the bare-minimum form of the mining walk. Same
  `Application.CreateApplication(null, null)` → `PatientSummaries` → `OpenPatient`/`ClosePatient`
  discipline, but the body is a single predicate — `plan.PlanType == PlanType.Brachy` — with a
  one-line `Console.WriteLine`. None of ESAP-01's per-plan reporting, accessory/energy accumulation,
  or target-structure fallback ladder.
- **Surfaces it adds:** `PlanSetup.PlanType` / the `PlanType.Brachy` enum value (the one new surface).
- **Reuse note:** the takeaway is `PlanType.Brachy` as a cohort filter — drop it into ESAP-01's
  richer skeleton (or the Advanced_4 / DW16-21 exporter) to build a brachy-specific census with real
  per-plan metrics. Interactive `null,null` sign-in is already the right default. Verdict Liftable
  (illustrative on its own).
