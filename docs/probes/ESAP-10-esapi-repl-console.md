# ESAP-10 — Uab.VMS.Console (interactive ESAPI REPL)

| Field | Value |
|---|---|
| ID | ESAP-10 |
| Solution | Uab.VMS.Console |
| Source event | Eclipse Scripting API — projects |
| ESAPI version | unknown (binary-plugin entry `Execute(ScriptContext, Window)`) |
| Type | Standalone exe / binary plugin (WPF REPL) |
| Reuse verdict | Adaptable |

## Problem
Exploring ESAPI normally means editing a script, recompiling, and re-launching Eclipse for every probe. This
solution (UAB Medicine) gives a physicist a **live C# REPL with code completion** wired to the current
`ScriptContext` — type `Context.Patient.Courses…`, press Enter, see the result immediately. It uniquely
collapses the write-build-run loop to an interactive prompt, making it the best learning/exploration tool in
the repo.

## Approach
A WPF console front-end over the **ScriptCs** scripting engine (Roslyn backend), with a custom code-completion
provider (`Cardan.CodeCompletion`) built on the AvalonEdit editor and Roslyn's workspace APIs.
- **Context bridge** — the plugin `Script.Execute(context, window)` stashes the live context in a static
  singleton `ScriptContextX.Instance`, then shows the console dialog. The ScriptCs host
  (`WPFScriptHost : ScriptHost`) exposes that context to every typed command as `Context`, so REPL code reaches
  the real ARIA session; `WPFScriptHost.Application` wraps `V.Application.CreateApplication(user,pwd)` for the
  standalone path.
- **REPL engine (`ConsoleViewModel`)** — `StartScriptCs()` builds a `ScriptServicesBuilder(...).Repl()` with
  `RoslynScriptEngine` and the custom `WPFScriptHostFactory`, then `AddReferenceAndImportNamespaces` for the
  ESAPI `ScriptContext` type (plus `IConsole`, Json) so users can call ESAPI without manual `using`s. Each
  submitted line runs through `_service.Executor.ExecuteScript(command)`; the `ScriptResult`'s return value or
  `ExecuteExceptionInfo` is rendered. Console output is marshalled back to the WPF text area through a Prism
  `EventAggregator` (`WriteLineEvent`/`WriteEvent`) and a `WPFConsoleRelay` that stands in for `System.Console`.
- **Code completion (`Cardan.CodeCompletion`)** — an in-memory Roslyn workspace (`InteractiveWorkspace`,
  `InteractiveTextContainer`) tracks the typed buffer; `CompletionProvider` asks Roslyn for member/enum/LINQ
  completions at the caret and feeds an AvalonEdit completion window, with an `OverloadInsightWindow` for
  method signatures. This is what makes the prompt usable for discovering ESAPI surfaces.
- **Editor/UI** — AvalonEdit `TextEditor` with a read-only section provider (so prompt history can't be edited),
  syntax highlighting from an embedded `Highlight.xml`, MVVM via Prism (`ConsoleViewModel`).

## ESAPI surfaces
- **The only direct ESAPI coupling is thin and deliberate:** `Script.Execute(ScriptContext, Window)` entry,
  `ScriptContext` held in `ScriptContextX.Instance` and surfaced as `Context`, and
  `V.Application.CreateApplication(username, password)` for the standalone host. Everything reachable through
  `Context` (Patient, Course, PlanSetup, StructureSet, Image…) is then available **at runtime** in the REPL.
- **Heavy non-ESAPI stack (the actual substance):** ScriptCs (`ScriptServices`, `ScriptHost`, `Executor`,
  `ScriptCs.Engine.Roslyn.RoslynScriptEngine`), Roslyn workspaces/completion, ICSharpCode AvalonEdit,
  Prism MVVM + EventAggregator, Newtonsoft.Json.

## Reusability
Not a lift-the-feature sample — it's a lift-the-*capability* sample, and the capability is large. The
genuinely reusable patterns: (1) the **static-singleton context bridge** (`ScriptContextX`) for handing a live
`ScriptContext` to code that runs outside Eclipse's call stack; (2) the **ScriptCs/Roslyn REPL host** wired to
inject ESAPI references/namespaces so typed snippets "just work". Costs/caveats: a deep third-party dependency
tree (ScriptCs is itself effectively unmaintained; modern equivalents are the Roslyn C# Scripting API
`Microsoft.CodeAnalysis.CSharp.Scripting` / `dotnet-script` / C# Interactive), AvalonEdit + Prism, and an
unknown/older ESAPI version. Running ESAPI inside a long-lived interactive session also raises concurrency and
write-access concerns (no `BeginModifications` discipline at the prompt). Treat it as a reference design for an
internal "ESAPI scratchpad," rebuilt on the current Roslyn scripting stack.

## Idea sparks
- A modern ESAPI scratchpad: re-implement the context-bridge + REPL on `Microsoft.CodeAnalysis.CSharp.Scripting`
  for fast interactive exploration and one-off queries without a build.
- A "snippet runner" plugin: a trimmed version that just evaluates a pasted expression against `Context` and
  prints the result — handy at the console for ad-hoc D/V lookups.
- A teaching tool: ship the REPL with ESAPI pre-imported so trainees can explore the object model live with
  completion, lowering the on-ramp this whole probe registry is meant to shorten.
