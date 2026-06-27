# W1810-02 — PlanChecker (custom Visual Scripting plan-QA element)

| Field | Value |
|---|---|
| ID | W1810-02 |
| Solution | PlanChecker |
| Source event | 16 Oct 2018 Webinar — Visual Scripting ActionPacks |
| ESAPI version | v15.5 (Visual Scripting `ElementInterface`) |
| Type | Visual Scripting custom element (`VisualScriptElement`) |
| Reuse verdict | Adaptable |

## Problem
Physicists want plan checks that live *inside* the Eclipse Visual Scripting UI as drop-in,
configurable nodes — no standalone plugin, no separate launch. This webinar element shows the
authoring pattern by implementing a small "Plan Checker 9000" that runs a few real plan-QA checks
and returns a pass/fail table the Visual Scripting canvas renders.

## Approach
The class derives from `VisualScriptElement` and is wired into the canvas by the element-authoring
contract rather than a `Script.Execute`. The reusable scaffold is: an `[ActionPackExecuteMethod]`
`Execute(PlanSetup ps)` that returns `IEnumerable<check>` (each `check` = Name / Evaluation /
Result, surfaced as a row); a `DisplayName` override (the node's label); an `AllowedOptions`
property exposing user-selectable dropdowns (here **Site** = Prostate/H&N/Lung and **Modality** =
IMRT/VMAT/SRS); and a `SetOption(key, value)` that stashes the user's picks into an `m_options`
dictionary the `Execute` body reads. `RequiresRuntimeConsole` / `RequiresDatabaseModifications`
are overridden to declare the element's needs.

The checks themselves are the interesting payload. **(1) Target present** — `ps.TargetVolumeID`
non-empty. **(2) Max dose in target** — `target.IsPointInsideSegment(ps.Dose.DoseMax3DLocation)`,
i.e. is the global dose maximum geometrically inside the target structure. **(3) IMRT MU
renormalization** (only when the Modality option is `IMRT`) — it mines the first beam's **LMC
calculation log** (`Beam.CalculationLogs` where `Category == "LMC"`), parses the "Maximum MU" and
"Lost MU factor" lines, multiplies them, and checks the product is within 5% of
`Beam.Meterset.Value`. Mining a TPS calculation log for a QA assertion is the clever, transferable
move here.

## ESAPI surfaces
- `VMS.TPS.VisualScripting.ElementInterface`: `VisualScriptElement`, `IVisualScriptElementRuntimeHost`, `[ActionPackExecuteMethod]`, `DisplayName`, `AllowedOptions`, `SetOption`, `RequiresRuntimeConsole`, `RequiresDatabaseModifications`
- `PlanSetup.TargetVolumeID`, `PlanSetup.StructureSet.Structures`
- **`Structure.IsPointInsideSegment(VVector)`** — point-in-structure test
- `PlanSetup.Dose.DoseMax3D`, `Dose.DoseMax3DLocation`
- `PlanSetup.Beams` → `Beam.CalculationLogs` (`.Category`, `.MessageLines`), `Beam.Meterset.Value`

## Reusability
The **element scaffold is directly liftable** as a template for any custom Visual Scripting QA node
— copy the `DisplayName` / `AllowedOptions` / `SetOption` / `Execute → IEnumerable<row>` shape and
drop in your own checks. The three checks are each good adaptable patterns, the max-dose-in-target
(`IsPointInsideSegment`) and the calculation-log mining especially. Caveats before reuse:
`Structures.First(x => x.Id == ps.TargetVolumeID)` throws if the target is missing even though
check (1) just detected that case — reorder so a failed target check short-circuits; the LMC-log
parsing is brittle to log wording / number formatting / locale and only inspects the first beam;
and it requires the Visual Scripting 15.5+ `ElementInterface` assembly, so it won't load in a plain
binary-plugin or standalone context.

## Idea sparks
- Build a **library of reusable Visual Scripting QA nodes** (TG-263 target naming, isocenter sanity,
  prescription checks) physicists compose on the canvas without writing standalone plugins.
- Generalize the **calculation-log mining** beyond LMC — surface hidden optimization / dose-calc
  warnings as explicit pass/fail checks at plan-check time.
- A **site-aware tolerance element**: switch the constraint table off the `Site` option via the
  `AllowedOptions` / `SetOption` mechanism, making per-protocol QA configurable in the UI.
