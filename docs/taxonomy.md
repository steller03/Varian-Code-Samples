# Taxonomy & Schema — the shared contract

Every dispatch reads this file first and treats it as binding. Change a definition here and
all dispatches inherit it. Keep additions backward-compatible — don't renumber existing items.

## 1. Problem categories (closed list)

Assign exactly **one primary** category per solution. If a second clearly applies, add it in
parentheses. Do not invent categories — if nothing fits, use `Other` and say why.

| Category | Scope |
|---|---|
| Plan QA & verification | QA plans, plan checks, second-check, MU / integrity checks |
| DVH & dose metrics | DVH extraction, D/V metrics, dose-at-point, dose statistics |
| Structure & contour ops | Create / edit structures, Boolean, margins, TG-263 naming, cropping |
| Optimization & planning | Optimization objectives, RapidPlan, auto-planning, field setup |
| Reporting & documents | PDF / Word / Excel / CSV reports, plan summaries, exports |
| DICOM I/O & interop | DICOM read / write, C-STORE / FIND / MOVE, import / export, anonymization |
| Image & registration | CT / CBCT handling, image registration, fusion, voxel access |
| Beam, MLC & geometry | Beams, control points, MLC, gantry / collimator geometry, fluence |
| ARIA & database query | Patient / course / plan navigation, scheduling data, ARIA Access, SQL |
| Workflow & process | Clinical workflow automation, batch ops, status / QA tracking |
| Plugin scaffolding & UI | App framework, WPF / binary-plugin scaffolding, context handling |
| Machine & commissioning | Beam data, machine config, TPS / commissioning / golden data |
| Research & algorithmic | NTCP / TCP, radiomics, custom models, experimental analysis |
| Other | Genuinely outside the above (note why) |

## 2. Field vocabularies

**Plugin type** (one): `Standalone exe` · `Binary plugin` · `Script (single-file)` · `Library/shared` · `Other`

**ESAPI version**: e.g. `v11`, `v13.6`, `v15.5`, `v16`, or `unknown`. Detect from the project's
VMS reference version / HintPath, or infer from the entry signature — `Execute(ScriptContext)`
≈ early single-file; `Execute(ScriptContext, Window)` ≈ binary plugin; `Application.CreateApplication`
≈ standalone exe. Record `unknown` rather than guessing wildly.

**Reuse verdict** (one — a first-pass estimate at triage, refined at probe time):
- `Liftable` — usable largely as-is in a modern project.
- `Adaptable` — sound pattern, needs porting / cleanup to reuse.
- `Illustrative` — teaches a concept; not meant for production lift.
- `Obsolete` — superseded by a modern ESAPI capability or deprecated API.

## 3. Interest score (1–5)

Score **value to a practicing physicist looking for automation ideas** — NOT code quality.

- **5** — Novel, high-leverage; solves a real clinical / physics need; technique worth stealing.
- **4** — Useful, clearly applicable pattern; good candidate to adapt.
- **3** — Solid reference for a common need; worth knowing it exists.
- **2** — Basic / hello-world; teaches one API surface; low novelty.
- **1** — Trivial, or redundant with a better example elsewhere.

## 4. ID scheme

`<SLUG>-NN` — the event slug from the tracker plus a two-digit number assigned within that
shard (DW16-01, DW16-02, …). Numbers are local to each shard, so dispatches never coordinate.

## 5. Registry column schema

Each triage shard is a markdown table with exactly these columns, in this order:

| Col | Meaning |
|---|---|
| ID | `<SLUG>-NN` |
| Solution | Solution / project name (the unit) |
| Path | Repo-relative path to the solution folder |
| Ver | ESAPI version (§2) |
| Type | Plugin type (§2) |
| Category | One primary from §1 (secondary in parens if needed) |
| Verdict | Reuse verdict (§2) |
| Problem | The problem solved, **≤ 15 words, outcome-focused — never code-focused** |
| Score | 1–5 (§3) |
| Probe | Blank · `flag` (mark for depth) · `→ probes/<file>` (once probed) |
