# W1804-02 — CreateOptStructures (margin + Boolean optimization-structure prep; cluster 11 anchor)

| Field | Value |
|---|---|
| ID | W1804-02 |
| Solution | CreateOptStructures |
| Source event | 06 Apr 2018 Webinar |
| ESAPI version | v15.1 (declared 15.1.1 / 15.5) |
| Type | Binary plugin (`Execute(ScriptContext)`) |
| Reuse verdict | Liftable |

## Problem
Before IMRT/VMAT optimization a planner hand-builds helper structures: a PTV expansion to drive
coverage, and "buffer" avoidance volumes that carve the target out of an OAR so the optimizer can
push dose off the OAR only where it abuts the target. This is the canonical **margin → Boolean**
structure-prep step, and the anchor for cluster 11 (rings, body-section slabs, target splits).

## Approach
Guards `Patient`/`StructureSet`, calls `Patient.BeginModifications()`, and resolves `Rectum` and
`PTV` by exact `Id`. It then does two operations: (1) create a `PTV` structure `PTV+5mm` and set
its `SegmentVolume = ptv.Margin(5.0)` (uniform 5 mm 3-D expansion); (2) create an `AVOIDANCE`
structure `RectumOpt5mm` and set it to `rectum.Sub(ptv_5mm)` — the rectum with the expanded-PTV
overlap subtracted out, i.e. the part of rectum the optimizer may freely spare. It prints the four
volumes to a `MessageBox`, then `RemoveStructure(ptv_5mm)` as demo cleanup, leaving only the buffer.
All ids are `const` strings flagged "change to match your clinical conventions."

## ESAPI surfaces
- `Patient.BeginModifications`, `StructureSet.Structures`, `StructureSet.AddStructure(dicomType, id)`, `RemoveStructure`, `CanAddStructure`
- `Structure.Margin(double mm)` (uniform expansion; **capped at 50 mm** — see DW16-24's `LargeMargin` workaround)
- `SegmentVolume` Boolean operators: `.Sub` (used here), also `.And` / `.Or` / `.Not`
- `Structure.Volume`, `Structure.DicomType` / `Id`; DICOM types `"PTV"`, `"AVOIDANCE"`

## Reusability
The margin-then-Boolean idiom is timeless ESAPI (unchanged v11→v16) and lifts verbatim — this is the
clean reference for *expand a target, then `Sub`/`And` to form a buffer*. The AVOIDANCE-buffer
pattern is exactly the pre-optimization helper most clinics build by hand. To productionize: replace
exact-`Id` lookups with a TG-263 / synonym resolver, table-drive the (source, op, margin, output-id)
recipe, and don't delete the expansion if you actually want it for coverage objectives. Note the
50 mm `Margin` ceiling and that `AddStructure` needs `BeginModifications` + a writeable script.

## Idea sparks
- A clinic-standard opt-structure generator: one recipe table → rings, PRV expansions, ring-buffers, OAR carve-outs, generated headlessly per site.
- Wire as the structure-prep stage feeding auto-planning (DW16-22 / DW18-06) so a plan is built end-to-end from a bare structure set.
- Extend to a full ring set around every PTV (the DW16-13 generalization) for dose-falloff control.
