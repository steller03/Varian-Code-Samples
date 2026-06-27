# ESAP-05 — GetDicomCollection (DCMTK C-MOVE of a plan's objects)

| Field | Value |
|---|---|
| ID | ESAP-05 |
| Solution | GetDicomCollection |
| Source event | Eclipse Scripting API — `projects/` reference set |
| ESAPI version | v11 / v13 |
| Type | Binary plugin (`Execute(ScriptContext)`) |
| Reuse verdict | Adaptable |

## Problem
A physicist needs the full DICOM bundle for the selected plan — CT series, structure set, RT plan,
and all RT dose — pulled out of ARIA to a local folder for an external tool (independent dose check,
research, archival). ESAPI has no direct DICOM export, so this script bridges to DCMTK's `movescu`
and the Varian DICOM DB Daemon via C-MOVE.

## Approach
The script is essentially a **code generator**: it reads UIDs from the live ESAPI model and emits a
DCMTK command (`.cmd`) script, then executes it. `GenerateDicomMoveScript` builds a `movescu`
invocation per object using the right query-retrieve level and key tags: the CT by **Series**
(`0008,0052=SERIES` + `0020,000E=Series UID`), the structure set and plan by **Image/Instance**
(`0008,0052=IMAGE` + `0008,0018=SOP Instance UID` from `StructureSet.UID` / `plan.UID`), and — since
ESAPI can't tell which RTDose maps to the plan — *all* RT dose in any study containing an RTDOSE
series, keyed by Study UID plus the RTDoseStorage SOP Class UID (`1.2.840.10008.5.1.4.1.1.481.2`).
Local/remote AE titles, daemon IP/port, and the DCMTK bin path are compile-time constants near the top.
The generated script is run through `PowerShell.exe` with `tee-object` so stdout is both shown and
logged; stderr is captured via a `DataReceivedEventHandler` and written to a side file. Output filename
is sanitized against `Path.GetInvalidFileNameChars()` and written under `%TEMP%`.

## ESAPI surfaces
- `ScriptContext.Patient`, `ScriptContext.PlanSetup`
- `PlanSetup.UID`, `PlanSetup.StructureSet`, `StructureSet.UID`, `StructureSet.Image`, `Image.Series.UID`, `Image.Id`
- `Patient.Studies`, `Study.Series`, `Series.Modality` (`SeriesModality.RTDOSE`), `Study.UID`
- `System.Diagnostics.Process` (PowerShell host), `StreamWriter` (DCMTK script emission)

## Reusability
The *pattern* — read UIDs from ESAPI, generate a DCMTK/movescu script, shell out — is the durable,
adaptable asset; it is the standard workaround for "ESAPI has no DICOM C-MOVE." What must be ported:
every AE title, the daemon IP/port, and the DCMTK path are hard-coded constants — externalize to
config. The PowerShell-`tee` wrapping and `ReadToEnd()`-before-`WaitForExit()` ordering is fragile
(deadlock-prone for large stderr); prefer async reads on both streams. Requires a separately
installed/licensed DCMTK and a configured VMS DB Daemon, and the companion article ("Scripting the
Varian DICOM DB Daemon with ESAPI + DCMTK") for daemon setup. Sending *all* dose in the study is a
deliberate over-fetch — fine for bundling, wasteful if you only want the plan's dose. Newer ESAPI/
Eclipse may offer more direct export routes worth checking before lifting this wholesale.

## Idea sparks
- A "send this plan to my research PACS" one-click plugin, parameterized by destination AE.
- Batch variant: drive it from the ESAP-01 patient walk to export a whole cohort's plan bundles.
- Swap the C-MOVE targets to also grab registration / approved imaging objects for offline review.
