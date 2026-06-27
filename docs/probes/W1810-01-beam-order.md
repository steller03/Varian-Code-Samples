# W1810-01 — BeamOrder (Visual Scripting element: reorder beams)

**Tier D lightweight.** A Visual Scripting custom element (`VisualScriptElement`) that receives the beam
list and returns it ordered by `BeamNumber` or by MU, selectable from an `AllowedOptions` dropdown in the
Visual Scripting UI.

- **ESAPI surface:** the ActionPack element-authoring pattern — `[ActionPackExecuteMethod]`,
  `AllowedOptions`, `SetOption`, `DisplayName`; sorts on `Beam.BeamNumber` / `Beam.Meterset.Value`.
- **Pointer:** the simpler twin of [W1810-02 PlanChecker](W1810-02-plan-checker.md) — same
  `VisualScriptElement` authoring pattern (the probed exemplar).
