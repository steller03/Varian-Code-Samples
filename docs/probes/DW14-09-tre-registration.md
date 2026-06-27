# DW14-09 — TRE (target registration error from match points → HTML report)

| Field | Value |
|---|---|
| ID | DW14-09 |
| Solution | TRE (DW2014 hands-on exercise 6) |
| Source event | Developer Workshop 2014 — SmartAdapt Scripting API |
| ESAPI version | v13 (SmartAdapt scripting, not Eclipse ESAPI) |
| Type | Binary plugin (`Execute(ScriptContext)`) |
| Reuse verdict | Adaptable (technique) / Illustrative (API) |

## Problem
Quantify how accurate an image registration is. Given user-placed corresponding match points on the
fixed and moving images, compute the **Target Registration Error** — the residual distance between
each fixed landmark and the moving landmark after it is pushed through the registration transform —
and present a per-point + summary HTML report. This is the catalogue's only registration-accuracy /
fusion-QA worked example.

## Approach
A SmartAdapt plugin (note the namespaces `VMS.CA.Scripting` / `VMS.IRS.Scripting`, **not** the Eclipse
`VMS.TPS` model). It requires a registration in context: it pulls `context.Registration` (an
`MIRSRegistration`) and its `RegisteredImage` (fixed) and `SourceImage` (moving). On each image's
structure set it finds the `PointsStructure` whose `StructureType == StructureType.Registration` — the
match points. The moving points are mapped through the registration by an extension method
`TransformPoints` that dispatches on the registration kind:
`MIRSRigidRegistration.RigidRegistration.TransformPoint` vs
`MIRSNonRigidRegistration.NonRigidRegistration.TransformPoint`. `RegStats.computeStats` then computes
min / max / mean Euclidean distance (`VVector.Distance`) between each registered (fixed) point and its
derived (transformed) point — that distance **is** the per-landmark TRE. Finally it writes a
`%TEMP%\reg_report.html` table (per-point source/registered/derived coords + distance, plus the
min/max/mean) and launches it in the browser.

## ESAPI surfaces (SmartAdapt)
- `ScriptContext.Registration` / `CurrentUser` / `Patient`
- `MIRSRegistration` (`RegisteredImage`, `SourceImage`, `Id`), `MIRSImage.Image.StructureSets`
- `MIRSRigidRegistration.RigidRegistration.TransformPoint`,
  `MIRSNonRigidRegistration.NonRigidRegistration.TransformPoint`
- `PointsStructure.Points` / `PointCollection`, `Structure.StructureType == StructureType.Registration`
- `VVector`, `VVector.Distance`; namespaces `VMS.CA.Scripting`, `VMS.IRS.Scripting`

## Reusability
The **technique** lifts cleanly — landmark TRE = distance between known-corresponding fixed points and
transformed moving points; the rigid/deformable `TransformPoint` dispatch and the `RegStats`
min/max/mean computation port directly. The **API does not**: this is the SmartAdapt `MIRS*` surface,
a separate and largely retired scripting model. A modern port would target Eclipse ESAPI's own
`Registration` / `Registration.TransformPoint` (the current registration object), keeping the same
math. The HTML-string-builder report is the same idiom seen across the catalogue (cf. ESAP-06,
W2008-01, the DVH evaluators). Caveat: it assumes both images carry a `Registration`-typed
`PointsStructure` with the landmarks in corresponding order.

## Idea sparks
- A deformable-registration QA dashboard scoring TRE across a standard landmark set per case.
- A per-fraction CBCT→planning-CT registration-accuracy log to trend setup/fusion drift.
- Generalize the rigid/deformable `TransformPoint` dispatch into a shared point-mapping helper
  (dose-point follow, fiducial/marker tracking, structure propagation checks).
