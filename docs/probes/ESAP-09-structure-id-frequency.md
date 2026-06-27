# ESAP-09 — StructureIdFrequency (database-wide structure-naming histogram)

| Field | Value |
|---|---|
| ID | ESAP-09 |
| Solution | StructureIdFrequency |
| Source event | Eclipse Scripting API — `projects/` reference set |
| ESAPI version | v13.5 (binary references `Varian\Vision\13.5\Bin64`; header notes "v11+") |
| Type | Standalone exe (`Application.CreateApplication`) |
| Reuse verdict | Liftable |

## Problem
Structure naming drifts across planners, protocols, and years, which frustrates any downstream automation that keys off `Structure.Id` and blocks TG-263 standardization. Before you can clean up or map names, you need to know what is actually in use and how often. This tool produces an enterprise-wide frequency census of structure IDs so the physics team can see the long tail of naming variants and prioritize a rename/mapping effort.

## Approach
The console app opens ARIA with `Application.CreateApplication(null, null)` (interactive sign-in — no credentials are baked in), wrapped in a `using` so the application disposes cleanly. `Execute` builds a case-insensitive `Dictionary<string,int>` (`StringComparer.CurrentCultureIgnoreCase`) as the histogram, then iterates the entire database via `app.PatientSummaries`, calling `OpenPatient(ps)` / `ClosePatient()` around each patient — the mandatory open/close discipline for a full-DB scan, since you cannot hold every patient open at once. For each patient it walks `p.StructureSets`, filtered by a LINQ predicate on `StructureSet.HistoryDateTime` against a hardcoded `searchSince` date (default 2013-06-01) so only recently-created sets count, then walks `ss.Structures` filtering out `DicomType == "MARKER"`. Each surviving `Structure.Id` is tallied with the usual `TryGetValue`/increment-or-add pattern.

The only throttling is a console progress line every 100th patient (`iIndex % 100`); there is no checkpointing or cooperative stop. After the scan, the dictionary is flattened to a `List<KeyValuePair>` and sorted descending by count via a custom comparator, then written to a fixed CSV path (`c:\temp\structureids-...csv`) with a `Structure Id,Count` header through a `StreamWriter`. The author flags a known bug: structure IDs containing a comma corrupt the CSV (no quoting/escaping).

## ESAPI surfaces
- `Application.CreateApplication(null, null)` (`IDisposable`, `using`)
- `Application.PatientSummaries` → `PatientSummary`
- `Application.OpenPatient(PatientSummary)` → `Patient`; `Application.ClosePatient()`
- `Patient.StructureSets` → `StructureSet`
- `StructureSet.HistoryDateTime` (date filter)
- `StructureSet.Structures` → `Structure`
- `Structure.Id`, `Structure.DicomType` (marker exclusion)
- Namespaces: `VMS.TPS.Common.Model.API`, `VMS.TPS.Common.Model.Types`

## Reusability
The skeleton is liftable as-is and is essentially the canonical minimal full-DB mining loop: open-app → iterate `PatientSummaries` with open/close → accumulate into a dictionary → sort → write CSV. Nothing here is deprecated; `PatientSummaries`, `OpenPatient`/`ClosePatient`, `StructureSets`, and `Structure.Id`/`DicomType` are all current through modern ESAPI, so the v13.5-vs-v11 distinction is immaterial for this surface. Port effort to a newer version is near zero. To harden it: parameterize `ReportPath`, `searchSince`, and the marker filter (currently all hardcoded constants); add CSV quoting/escaping to fix the documented comma bug; and consider counting distinct *patients* per ID, not raw occurrences, if you want prevalence rather than volume. Performance is the main caveat — a full-DB scan is slow and database-load-sensitive; the open/close-per-patient idiom is correct and necessary, but you should run off-hours and may want checkpointing or a cooperative stop (neither is present), plus a try/catch inside the patient loop so one bad patient does not abort the whole run.

## Idea sparks
- A TG-263 compliance audit: join this histogram against the TG-263 nomenclature table to auto-flag non-conforming IDs and surface a ranked rename worklist.
- A structure-naming linter that, given the frequency table, suggests the canonical variant for each near-duplicate cluster (e.g. `Cord`/`SpinalCord`/`cord`).
- Extend the same walk to emit `(DicomType, Id)` pairs to detect mislabeled structures (e.g. an OAR tagged `PTV`) and feed an OAR-coverage / completeness report per site.
