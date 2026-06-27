# DW16-30 — SpotWeightReporting (per-layer min/max spot MU on a proton plan)

| Field | Value |
|---|---|
| ID | DW16-30 |
| Solution | SpotWeightReporting |
| Source event | Developer Workshop 2016 — kata Proton.3 |
| ESAPI version | v13.7+ (13.7 / 15.0 / 15.1) |
| Type | Binary plugin (`Execute(ScriptContext)`) |
| Reuse verdict | Adaptable |

## Problem
In spot-scanning (IMPT) delivery, every energy layer is a cloud of pencil-beam spots, each with a
weight in MU. Spots that come out of optimization too light or too heavy are a deliverability and
QA concern, and the acceptable window is energy-dependent. Before you can enforce anything you have
to *see* the spread — what are the lowest and highest spot weights in each layer? This kata is the
read-only inspection step: walk every layer of every ion beam and report its min and max raw spot
weight.

## Approach
For each `IonBeam` in `IonPlanSetup.IonBeams` it pulls
`ionBeam.GetEditableParameters()` and reads `beamParameters.IonControlPointPairs` — note it uses
the **editable-parameters object purely for read access**, because the raw optimization spot list
(`RawSpotList`) hangs off the control-point pairs reached that way. It never calls
`ApplyParameters`, so nothing is written. For each `IonControlPointPair` (one per energy layer) it
records `NominalBeamEnergy`, then scans `RawSpotList` tracking the running min/max of
`IonSpotParameters.Weight`. The per-layer triples (energy, raw min, raw max) accumulate into a list
and print as a formatted table in a per-beam `MessageBox`.

This is the **read-only sibling of DW16-31 (CustomPostProcessing)**, which uses the identical
`GetEditableParameters` → walk `IonControlPointPairs` → iterate `RawSpotList` traversal but then
mutates `IonSpotParameters.Weight` and commits with `ApplyParameters`. Read this one first to
understand the spot model; DW16-31 closes the loop by writing.

## ESAPI surfaces
- `ScriptContext.IonPlanSetup` → `IonPlanSetup.IonBeams` (`IonBeam`)
- **`IonBeam.GetEditableParameters()` → `IonBeamParameters.IonControlPointPairs`** (`IonControlPointPairCollection` → `IonControlPointPair`) — the access path to the raw spot list
- `IonControlPointPair.NominalBeamEnergy`, `IonControlPointPair.RawSpotList` (`IonSpotParameters.Weight`)
- `System.Windows.MessageBox` (report sink)

## Reusability
The **per-layer spot scan is directly liftable** and is the canonical way to read IMPT spot
weights. Two correctness caveats to fix before reuse: the min/max are seeded with magic constants
(`min = 1000`, `max = 0`), so a layer with a spot above 1000 MU, or an empty layer, reports
nonsense — seed from the first spot or use `RawSpotList.Min/Max(s => s.Weight)` instead. And the
`MessageBox`-per-beam output is unsuitable for batch or for any real analysis; swap it for a CSV
(energy, layer index, min, max, spot count) keyed by beam id. Using `GetEditableParameters()` for a
read-only task is mildly surprising but is the supported route to `RawSpotList`. Needs v13.7+ and a
proton-licensed environment.

## Idea sparks
- A **spot-weight QA flag**: report layers whose min spot MU falls below the machine's deliverable
  floor (or whose max exceeds the ceiling) — the detection half of the read→decide→write loop that
  DW16-31 completes by clamping.
- **CSV export of per-layer spot statistics** for commissioning and plan-to-plan comparison across
  energies, beam angles, or optimization settings.
- Extend the scan to spot **count and spacing** per layer to characterize plan complexity /
  deliverability time, not just weight extremes.
