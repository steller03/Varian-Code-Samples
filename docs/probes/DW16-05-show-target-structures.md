# DW16-05 — ShowTargetStructures (list target structures in scope)

**Tier D lightweight.** Binary plugin that, for every plan and plan sum in scope, lists the structures
whose `DicomType` is PTV / CTV / GTV (or "No targets.").

- **ESAPI surface:** `Structure.DicomType` filtering over `ScriptContext.PlansInScope` /
  `PlanSumsInScope`, resolving each item's `StructureSet`.
- **Pointer:** a trivial target-query utility (Structure & contour ops); no probed exemplar — distinct
  small readout.
