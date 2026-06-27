# DW14-01 — ESAPIAnon (C-MOVE retrieve + profile-driven DICOM anonymizer)

| Field | Value |
|---|---|
| ID | DW14-01 |
| Solution | ESAPIAnon |
| Source event | Developer Workshop 2014 — guru track |
| ESAPI version | v13.5 |
| Type | Binary plugin (`Execute(ScriptContext, Window)`), WPF/MVVM |
| Reuse verdict | Adaptable |

## Problem
A physicist or researcher needs to export a patient's images, plans, structures and dose out of
ARIA and hand them off de-identified — for a teaching set, a vendor support case, or a research
cohort. This plugin launches from inside Eclipse on the open patient, pulls that patient's full
study via DICOM C-MOVE, scrubs identifiers by a configurable profile, and writes the cleaned files
to a folder the user picks.

## Approach
A thin ESAPI `Script.cs` just hosts a WPF/MVVM UI (MvvmLight `ViewModelLocator`) in the plugin
window; all work lives in `MainViewModel.AnonymizeCommand`. The retrieval step shells out to DCMTK's
`movescu.exe` (`CMove.GenerateDicomFiles`) with the open patient's MRN as the `(0010,0020)` match key
and `(0008,0052)=STUDY` retrieve level — i.e. ESAPI supplies *which* patient, DCMTK does the actual
C-MOVE pull into a working folder. Files are then parsed with the **EvilDICOM** library
(`DICOMFileReader.Read`) into `DICOMObject`s. The anonymization core is a composable pipeline:
`AnonymizationQue` is itself an `IAnonymizer` holding an ordered list of smaller `IAnonymizer`s
(UID, study-id, private-tag, patient-id, date, profile), built from a settings object and run over
every object (`que.Anonymize(d)`). The clever piece is **consistency across the study**: `UIDAnonymizer`
makes two passes — an `AddDICOMObject` pre-pass that walks every `VR.UniqueIdentifier` element and
builds a `Dictionary<oldUID,newUID>` (skipping protected UIDs like transfer-syntax and SOP-class),
then an `Anonymize` pass that rewrites each UID through that map, so cross-references between image /
structure / plan / dose objects stay internally linked after scrubbing. `ProfileAnonymizer` blanks a
fixed list of ~25 identifying tags (names, institution, physicians, comments, accession, plus
zeroing patient size/weight) via `DICOMObject.Replace`. Cleaned objects are written back out with
`DICOMFileWriter.WriteLittleEndian` to a user-chosen folder, and the temp retrieval dir is deleted.

## ESAPI surfaces
- `Script.Execute(ScriptContext, System.Windows.Window)` — binary-plugin entry, hosts WPF content in `window`
- `ScriptContext.Patient`, `Patient.Id` — the only ESAPI data actually consumed (identifies the C-MOVE target)
- Everything else is **non-ESAPI**: DCMTK `movescu.exe` for C-MOVE, EvilDICOM (`DICOMObject`, `DICOMFileReader`/`Writer`, `TagHelper`, `UIDHelper.GenerateUID`, `VR`), MvvmLight, WinForms `FolderBrowserDialog`

## Reusability
The **anonymizer architecture is the liftable gem**: a queue of single-responsibility `IAnonymizer`s
plus the two-pass consistent-UID remap is a clean, extensible de-identification pattern you can drop
into any DICOM tool. The DCMTK-by-shell C-MOVE works but is the weak seam — hard-coded binary path
(`C:\variandeveloper\tools\...`), AE title, and `--port 106`, with IP/port/AE strings baked into the
view model; a modern rewrite would use a managed DICOM stack (fo-dicom) for both the C-MOVE *and* the
tag editing, dropping the DCMTK dependency and the temp-file round-trip entirely. EvilDICOM is dated
but still functional. The `ProfileAnonymizer` tag list predates current guidance — align it with
DICOM PS3.15 / the basic confidentiality profile before clinical use. Note the swallowed exception in
`CMove` (empty catch) hides retrieval failures.

## Idea sparks
- A reusable `IAnonymizer`-queue NuGet/shared lib used by every export tool in the shop, with a
  config-file-driven tag profile instead of the hard-coded list.
- "De-identify the active patient's plan to a research folder" one-click button, swapping DCMTK for
  fo-dicom C-GET/C-MOVE so there's no external binary to deploy.
- Reuse the consistent-UID remap to build paired anonymized longitudinal sets (same patient over
  time keeps stable—but-fake—study/series links for registration research.)
