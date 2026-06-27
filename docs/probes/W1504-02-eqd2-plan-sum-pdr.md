# W1504-02 — EQD2_2 (EQD2 over plan sums, with PDR brachy)

| Field | Value |
|---|---|
| ID | W1504-02 |
| Solution | EQD2_2 |
| Source event | 21 Apr 2015 Webinar — Eclipse Scripting API |
| ESAPI version | v13.6 |
| Type | Binary plugin (`Execute(ScriptContext)`) |
| Reuse verdict | Liftable |

## Problem
A physicist combining multiple treatment courses (plan sums) needs each component and the total
expressed as EQD2 — dose equivalent delivered in 2 Gy fractions — so disparate fractionations can be
added on a common biological scale. Pulsed-dose-rate (PDR) brachytherapy breaks the simple
linear-quadratic picture because sublethal damage repairs between pulses, so it needs its own
incomplete-repair correction.

## Approach
It walks `context.PlanSumsInScope`, and within each `PlanSum` walks the member `PlanSetup`s,
computing EQD2 per plan and accumulating both prescribed dose and EQD2 to a sum row. The standard
path applies the LQ formulas with α/β = 10: `BED = n·d·(1 + d/(α/β))` then `EQD2 = BED/(1 + 2/(α/β))`,
reading `UniqueFractionation.PrescribedDosePerFraction` and `NumberOfFractions`. When a plan is a
`BrachyPlanSetup` with a non-null `NumberOfPdrPulses`, it diverts to a PDR model: with repair rate
`μ = ln2/T_repair` and hard-coded pulse timing (repair 1.5 h, pulse 0.1 h, period 1 h), it builds the
Dale incomplete-repair g-factor (`s`, `y`, `fp` terms over the pulse train) and folds it into the BED
before the same EQD2 conversion. Output is a tab-delimited table in a `MessageBox`.

## ESAPI surfaces
- `ScriptContext.PlanSumsInScope`, `PlanSum.PlanSetups`, `PlanSum.Id`
- `PlanSetup.TotalPrescribedDose`, `PlanSetup.UniqueFractionation` (`PrescribedDosePerFraction`, `NumberOfFractions`)
- `DoseValue` / `DoseValue.DoseUnit` (cGy↔Gy handling)
- `BrachyPlanSetup.NumberOfPdrPulses`

## Reusability
The LQ EQD2/BED math is pure C# and lifts directly; the genuinely valuable piece is the PDR
incomplete-repair model, which encodes a published radiobiology formula not available anywhere in
ESAPI. Caveats to address before reuse: α/β is hard-coded to 10 (should be tissue-specific), the PDR
timing constants are hard-coded, and the cGy/Gy conversion is applied a bit inconsistently between
`dosePerFraction` and `dosePerFractionInGy` — worth auditing units before trusting the number. The
`PlanSumsInScope` / `UniqueFractionation` / `BrachyPlanSetup` surfaces are still current. Replace the
`MessageBox` with a CSV/report sink for batch use.

## Idea sparks
- Drive α/β from a tissue/structure table for organ-specific EQD2.
- Fold this calculation into the interactive RBEReport (W1504-04) UI for editable α/β and PDF export.
- A re-treatment dose-accumulation dashboard that sums EQD2 across historical plan sums per OAR.
