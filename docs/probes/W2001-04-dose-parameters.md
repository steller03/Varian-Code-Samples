# W2001-04 — DoseParameters (surface Rx + dose-calculation parameters in an MVVM table)

| Field | Value |
|---|---|
| ID | W2001-04 |
| Solution | DoseParameters (16 Jan 2020 "SeparatedApps") |
| Source event | 16 Jan 2020 Webinar |
| ESAPI version | v15.6 ("Eclipse V115.6 MR3") |
| Type | Binary plugin (WPF/MVVM, `Execute(ScriptContext, Window, ScriptEnvironment)`) |
| Reuse verdict | Adaptable |

## Problem
Show the plan's prescription and dose-calculation settings — dose/fraction, #fractions, total dose, treatment %, algorithm model, grid size, heterogeneity, DLG, leaf transmission — on one read-only panel, so a reviewer can sanity-check calc parameters without digging through Eclipse dialogs. The third slice of the SeparatedApps trio.

## Approach
The simplest of the three: `Script.Execute` news up a `DoseParametersView` with a `DoseParametersViewModel(context.PlanSetup)` and sets it as `window.Content` — no DI container needed. The VM fills two `ObservableCollection<TableDisplayModel>` (Property/Value rows). **Rx data** reads directly: `DosePerFraction`, `NumberOfFractions`, `TotalDose`, `TreatmentPercentage * 100`. **Calc data** mixes a typed call — `GetCalculationModel(CalculationType.PhotonVolumeDose)` — with log-scraping: `GetFromLogs(key)` reaches into the first non-setup beam's `CalculationLogs`, finds the `Category == "Dose"` log, and pulls grid size / normalization / heterogeneity / DLG / leaf transmission via `MessageLines.FirstOrDefault(Contains(key)).Split('=').Last()`.

## ESAPI surfaces
- `ScriptContext.PlanSetup`
- `PlanSetup.DosePerFraction`, `NumberOfFractions`, `TotalDose`, `TreatmentPercentage`
- `PlanSetup.GetCalculationModel(CalculationType.PhotonVolumeDose)`
- `PlanSetup.Beams`, `Beam.IsSetupField`, `Beam.CalculationLogs`, `CalculationLog.Category`, `.MessageLines`
- Non-ESAPI: Prism `BindableBase`, WPF `ObservableCollection`

## Reusability
The Rx-parameter readout (dose/fx, fractions, total dose, treatment %) and `GetCalculationModel` are clean, liftable, version-stable. The value — and the risk — is `GetFromLogs`: scraping `CalculationLogs.MessageLines` is the only way to recover grid size / heterogeneity / DLG / leaf transmission programmatically, but it's brittle. The code chains `FirstOrDefault(...)` without null guards (no non-setup beam, or a key absent from `MessageLines`, throws an NPE), and the log keys and `=` formatting vary by algorithm and Eclipse version. Treat the scrape as illustrative and harden with null checks + algorithm-aware key lookups before clinical use. No deprecated calls. The shared MVVM architecture is covered in the W2001-01 probe.

## Idea sparks
- Build a headless "calc-parameter audit" that flags plans whose grid size / heterogeneity / DLG deviate from clinic standard — the scrape is the data source.
- Reuse the Property/Value `TableDisplayModel` + two-column DataGrid as the house pattern for any read-only plan-info panel.
- Combine with W2001-02/03 (or just use the merged W2001-01) for a one-window plan-review surface.
