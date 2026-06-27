# ESPL-01 — DvhLookups (live dose-at-volume / volume-at-dose calculator, plan-sum aware)

**Cluster 1 delta** — exemplar [W1811-01 DiggingIntoDVH](W1811-01-digging-into-dvh.md) (see also
[DW16-02 CSVDVHMetrics](DW16-02-csv-dvh-metrics.md) for the same PlanSum workaround).

- **Problem:** an interactive in-Eclipse panel where the user picks a structure and types either a volume
  (→ dose-at-volume) or a dose (→ volume-at-dose) and sees the reciprocal metric recomputed live, with
  absolute/relative toggles for both dose and volume.
- **Differs from the exemplar:** W1811-01 (and DW16-02) batch-evaluate a *table/template* of constraints;
  this is a single-structure **live calculator** built from raw WPF controls (a `ComboBox` of structures
  plus two `TextBox`es) that recomputes on every keystroke via `GetDoseAtVolume`/`GetVolumeAtDose`.
  It carries the same `PlanSum` extension-method workaround as DW16-02 — `PlanSum` lacks native
  `GetDoseAtVolume`/`GetVolumeAtDose`, so a `DvhExtensions` static class interpolates them off
  `GetDVHCumulativeData` — and additionally **cross-checks** the native vs interpolated result, popping a
  `MessageBox` if they diverge by >0.1%.
- **Surfaces it adds:** `PlanningItem.GetDVHCumulativeData`, `PlanSetup.GetDoseAtVolume` /
  `GetVolumeAtDose`, `ScriptContext.PlanSumsInScope`, and live toggling of `DoseValuePresentation` /
  `VolumePresentation` (`AbsoluteCm3` ↔ `Relative`).
- **Reuse note:** the `PlanSum` DVH extension methods and the abs/rel-aware live lookup are **liftable**
  into any interactive metric tool; the hand-built WPF layout is illustrative. Note the same caveat as
  DW16-02 — the `VolumeAtDose` interpolation is coarse index-based math off `CurveData`, not the native
  call. Verdict Liftable (the extensions).
