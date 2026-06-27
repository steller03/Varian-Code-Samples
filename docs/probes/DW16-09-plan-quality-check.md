# DW16-09 — PlanQualityCheck (constraint pass/fail → CSV)

| Field | Value |
|---|---|
| ID | DW16-09 |
| Solution | PlanQualityCheck |
| Source event | Developer Workshop 2016 — kata Intermediate.2 |
| ESAPI version | v11 (declared good through 15.0) |
| Type | Binary plugin (`Execute(ScriptContext)`) |
| Reuse verdict | Liftable |

## Problem
A physicist reviewing a lung plan wants the standard dose constraints checked automatically and a
pass/fail record written out, instead of reading each DVH metric by hand against a protocol
checklist. The kata extracts the key target and OAR metrics and emits a CSV scorecard.

## Approach
After guarding on `PlanSetup != null` and `IsDoseValid`, it locates structures by case-insensitive Id
substring (PTV, TOTAL LUNG, HEART, CORD, ESOPHAGUS), bailing with a message if any is missing or
empty. It then computes target coverage `D95` with `GetDoseAtVolume`; `V20`/`V40`/`V60` with
`GetVolumeAtDose`; and mean lung dose plus cord/esophagus max dose from `GetDVHCumulativeData`
(`DVHData.MeanDose` / `MaxDose`). Each value is compared to a hard-coded criterion — D95 ≥ prescribed,
MLD < 20 Gy, lung V20 < 40 %, cord Dmax < 45 Gy, heart V40 < 50 %, esophagus V60 < 50 % and Dmax <
75 Gy — and written as `Structure, Parameter, Value, Criteria, Result(Pass/Fail)` rows to
`c:\temp\PlanQualityCheck_i2.csv`.

## ESAPI surfaces
- `ScriptContext.PlanSetup` / `StructureSet`, `PlanSetup.IsDoseValid`, `PlanSetup.TotalDose`
- `PlanSetup.GetDoseAtVolume`, `PlanSetup.GetVolumeAtDose`
- `PlanSetup.GetDVHCumulativeData` → `DVHData.MeanDose` / `DVHData.MaxDose`
- `VolumePresentation`, `DoseValuePresentation`, `DoseValue`

## Reusability
The metric-extraction calls are fully liftable and still current; the architecture
(extract → compare to criteria → pass/fail → CSV) is a clean template for any protocol scorecard. The
weakness is that both the structure names and the constraints are hard-coded — productionizing means
externalizing the criteria into a protocol file (cf. DW16-02, which reads constraints from a CSV
template) and using TG-263-aware structure matching instead of substring search. `GetDoseAtVolume` /
`GetVolumeAtDose` are preferred over hand-rolling from a DVH; `GetDVHCumulativeData`/`DVHData` is older
but still supported (newer code may prefer the dose-metric helpers directly).

## Idea sparks
- Drive the criteria from a site-protocol table so one engine serves many disease sites.
- Batch the check across a whole course or cohort (cf. DW16-21 data-mining) into a QA dashboard.
- Add automatic flagging/email when a plan fails, as a pre-review gate.
