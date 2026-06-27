# DW16-31 — CustomPostProcessing (energy-dependent spot-MU limits on a proton plan)

| Field | Value |
|---|---|
| ID | DW16-31 |
| Solution | CustomPostProcessing |
| Source event | Developer Workshop 2016 — kata Proton.4 |
| ESAPI version | v15.1 (research v13.7/15.0/15.1) |
| Type | Binary plugin (writeable, `[assembly: ESAPIScript(IsWriteable = true)]`) |
| Reuse verdict | Liftable |

## Problem
Spot-scanning proton plans can come out of optimization with individual spot weights (MU) too low or
too high to deliver reliably on a given nozzle — and the deliverable limits are **energy-dependent**
(a low-energy layer tolerates different spot MU than a high-energy one). This script post-processes an
optimized IMPT plan, clamping every spot's weight into an energy-interpolated [min, max] window and
reporting what it changed per layer.

## Approach
This is the rare **writeable** ESAPI plugin: it declares `IsWriteable`, calls
`patient.BeginModifications()`, and then mutates plan data. For each `IonBeam` in the
`IonPlanSetup`, it pulls an **editable copy** of the beam's parameters
(`ionBeam.GetEditableParameters()`) and walks the energy layers via
`IonControlPointPairs`. The energy-dependence is a simple linear interpolation between user-set
limits at 70 MeV and 250 MeV — for each layer's `NominalBeamEnergy` it computes a per-layer lower and
upper spot-weight bound. Then it iterates the layer's `RawSpotList` and **edits `IonSpotParameters.Weight`
in place**: spots below the lower bound are either zeroed (if below half the bound — i.e. too small to
keep) or raised to the bound; spots above the upper bound are clamped down. It tracks pre/post min and
max spot weights per layer for a report. Crucially, the mutation only takes effect when it calls
**`ionBeam.ApplyParameters(beamParameters)`** — the editable-parameters object is a staging buffer
that must be applied back. A per-beam `MessageBox` prints a table (energy, raw min/max, post-processed
min/max) so the user sees the effect of the clamp.

## ESAPI surfaces
- `[assembly: ESAPIScript(IsWriteable = true)]`, `Patient.BeginModifications()` — required to edit
- `ScriptContext.IonPlanSetup` → `IonPlanSetup.IonBeams` (`IonBeam`)
- **`IonBeam.GetEditableParameters()` → `IonBeamParameters`** (the editable staging copy)
- `IonBeamParameters.IonControlPointPairs` (`IonControlPointPairCollection` → `IonControlPointPair`)
- `IonControlPointPair.NominalBeamEnergy`, `IonControlPointPair.RawSpotList` (`IonSpotParameters.Weight`, settable)
- **`IonBeam.ApplyParameters(IonBeamParameters)`** — commits the edits back to the beam

## Reusability
Directly liftable as the **template for any scripted IMPT spot manipulation**: the
`GetEditableParameters` → walk `IonControlPointPairs`/`RawSpotList` → mutate `Weight` →
`ApplyParameters` round-trip is the supported write path for proton spots and the single most useful
thing to take away. The clamping policy itself is demo-grade (linear 70↔250 MeV interpolation with
arbitrary constants; the "zero if below half the bound" rule is a heuristic) — replace the limits and
the interpolation with your machine's actual deliverability table. Caveats: this needs a **writeable
research license**, mutates the open plan (work on a copy and re-run dose afterward — the script does
neither), and the per-beam `MessageBox` is unsuitable for batch. `Ion*` APIs are stable from v13.7+
but require a proton-licensed environment to even compile/run.

## Idea sparks
- A "minimum-MU enforcer" QA tool that flags or fixes undeliverable spots against the real
  machine deliverability curve before plan approval, then recalculates dose and reports the dose
  change the clamp caused.
- Generalize the spot-walk into a library for arbitrary spot transforms: spot thinning/merging,
  robustness perturbations, or per-layer MU re-weighting studies.
- Pair with DW16-30 (SpotWeightReporting) — report-only — to make a read→decide→write loop: detect
  out-of-range layers, then apply the clamp only where needed.
