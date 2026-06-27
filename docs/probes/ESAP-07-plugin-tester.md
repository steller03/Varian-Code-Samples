# ESAP-07 — PluginTester (standalone binary-plugin debug harness)

| Field | Value |
|---|---|
| ID | ESAP-07 |
| Solution | PluginScriptExample / PluginTester |
| Source event | Eclipse Scripting API — projects |
| ESAPI version | v13.5 |
| Type | Standalone exe (host) + binary plugin (the example) |
| Reuse verdict | Adaptable |

## Problem
Developing a binary plugin means rebuilding the DLL and re-launching it inside Eclipse to test every change —
no breakpoints, no fast iteration. This solution (UAB / U-Michigan) is a **standalone WPF host that runs your
plugin's UI outside Eclipse**, letting you pick a patient/course/plans-in-scope, launch the plugin under the
Visual Studio debugger, and persist recent selections — a major dev-loop accelerator.

## Approach
Two projects sharing one plugin entry point — that shared entry is the whole trick:
- **The plugin (`PluginScriptExample`)** factors its real work into a context-free static method
  `Main.Start(patient, course, plansInScope, plan, currentUser, window)` that builds a `MainControl` UserControl
  into the host `Window`. The Eclipse entry `Script.Execute(ScriptContext, Window)` simply unpacks the context
  (`context.Patient`, `context.Course`, `context.PlansInScope` + `PlanSumsInScope`, `context.PlanSetup`,
  `context.CurrentUser`) and calls `Main.Start(...)`. So the plugin never hard-depends on `ScriptContext` for
  its logic — it depends on plain ESAPI objects.
- **The host (`PluginTester.exe`)** does what Eclipse does, manually. `Program.Main` (`[STAThread]`,
  global `UnhandledException` handler that suppresses the known Varian "OSP" exception) opens
  `Application.CreateApplication()` and shows a `MainWindow`. The window lets the user browse
  `_application.PatientSummaries`, `OpenPatientById` / `OpenPatient(summary)`, choose a course, an open plan,
  and a set of plans-in-scope (assembled into a `List<PlanningItem>`), then calls the **same**
  `StartPlugin(patient, courses, plansInScope, pItem, _application.CurrentUser, window)` shim, which forwards to
  `PluginScriptExample.Main.Start(...)`. It `ClosePatient()`s when done.
- **Recent-selection persistence** — selections (patient, courses, plans-in-scope, open plan) are serialized to
  `PluginTesterRecent.xml` and reloaded, so re-testing is one click. This is the productivity layer over the
  bare host.

To test your own plugin you point `StartPlugin` at your plugin's `Main.Start` equivalent — the contract is
"refactor your plugin so its body takes ESAPI objects, not `ScriptContext`," after which both Eclipse and the
tester can drive it.

## ESAPI surfaces
- **Standalone app lifecycle:** `Application.CreateApplication()`, `PatientSummaries`, `OpenPatientById`,
  `OpenPatient(PatientSummary)`, `ClosePatient`, `CurrentUser`
- **Context decomposition (the shim contract):** `ScriptContext.Patient`, `Course`, `PlansInScope`,
  `PlanSumsInScope`, `PlanSetup`, `CurrentUser` → passed as `Patient`, `Course`, `List<PlanningItem>`,
  `PlanSetup`, `User`, `Window`
- **Plugin entry forms:** `Script.Execute(ScriptContext, System.Windows.Window)` (Eclipse) vs.
  `Main.Start(...)` (host) — both terminate in the same WPF `UserControl`
- Plumbing: WPF (`Window`/`UserControl`/`DockPanel`), `AppDomain.UnhandledException`, `System.Xml` persistence

## Reusability
The reusable asset is **the pattern, not the code**: refactor a binary plugin so its logic lives in a
context-free `Start(...)` taking plain ESAPI objects, and you get free standalone debuggability plus a path to
batch invocation. The host's patient/scope picker + recent-selection persistence are a usable starting skeleton
for any "run my plugin outside Eclipse" tool. Caveats: it requires standalone-app licensing
(`Application.CreateApplication` needs a research/standalone license, which not every site has), it's pinned to
v13.5 and an older WPF/Prism (`BindableBase`) stack, the example plugin only forwards a single open plan, and
the "ignore the OSP exception" hack signals version-specific fragility. Re-validate `PatientSummaries`/`OpenPatient`
and the context properties against your ESAPI version. Eclipse's own newer debugging support has narrowed the
gap, but the context-shim refactor remains good hygiene.

## Idea sparks
- A team plugin template: scaffold every new plugin with the `Script.Execute → Main.Start(plain objects)`
  split so it's debuggable standalone from day one.
- A batch driver: reuse the host's open-patient/scope-build loop to run a plugin's `Start(...)` headlessly over
  a patient list (drop the WPF window for a no-UI variant).
- A regression harness: feed known patient/plan selections from `PluginTesterRecent.xml` to re-run a plugin and
  diff its outputs after an ESAPI version upgrade.
