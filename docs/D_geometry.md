# Dispatch D — Beam / Collimator / Jaw Geometry

**Subject:** `CSMayoLab/SRSAutoPlan` (standalone WPF app, GPL-3, U-Michigan / Chuck Mayo Lab).
**Reviewer:** Stephen Eller, DABR — for the Pscripts ecosystem (ESAPI v16.1, cGy-native).
**Scope of this dispatch:** all beam / collimator / jaw / arc geometry and the supporting coordinate math. The dose-shaping structures & objectives (Dispatch C) and the mechanical beam-API plumbing (Dispatch B) are out of scope; this file owns *the geometry and why it works*.
**Read-only:** nothing in the cloned tree was modified, built, or "fixed."

> **Units note:** every geometric quantity in this subsystem is in **mm** (WPF `Point3D` / ESAPI `VVector` carry DICOM mm). There is no cGy/Gy boundary in the geometry code, so the cGy-conversion discipline doesn't bite here — but I keep every margin and threshold named so I can lift them cleanly. Dose only appears where geometry hands off to objectives (Dispatch C).

---

## 1. Summary

The app builds a **single-isocenter, multi-target (SIMT)** VMAT geometry. One isocenter is placed at the **bounding-box center of all prescribed targets** (with an override that snaps it onto an important OAR when a target abuts one). For each arc it then computes a **static jaw rectangle and a collimator angle** that are guaranteed to keep *every* target inside the field at *every* gantry angle of that arc. The guarantee comes from a brute-force trick: rotate all target centers through a full 360° gantry sweep, accumulate the whole rotated point cloud, and bound it — the union envelope is gantry-invariant by construction, so static jaws set to it can never clip a target. A portrait-vs-landscape test on that envelope then picks one of two collimator angles (**10° or 80°**) so the MLC leaf-travel axis aligns with the longer target spread.

There are in fact **two** jaw-optimization implementations in the tree. The one wired into the running app is the simple full-sweep bounding box (`SRSBeamSetup.CollRect` → `GetCollsettings`). A second, more sophisticated **projected-limit scan** (`AP_lib/Jaw_Width.Rotate_n_Scan_Limits`) projects targets onto collimator-aligned axes over the *actual* arc angles and is structured to support searching for the area-minimizing collimator rotation — **but it is never called from the app**; it is library/research scaffolding (its `Console.WriteLine` betrays a console test harness). Likewise the MLC aperture analysis (`MLC_misc`) and the barycentric/`CollSpan` helpers are present but unreferenced by the live flow.

Arc layout is config-driven: **three arcs** — one ~full coplanar arc at couch 0° and two ~half non-coplanar arcs at couch kicks of ±45° — plus three setup beams (KV AP, KV RLAT, CBCT).

---

## 2. How it works (mechanism, in my words)

### 2.1 The live runtime path

The call chain that actually executes:

```
AutoPlan (SRS_Auto_Structures.cs)
  → center = ptvList.FindGeometricCenter()          // bounding-box center, mm, rounded to 1 mm
  → [override] GetOverlapStructuresInfo(...)         // if a PTV is ≤0.5 cm from an important OAR,
                                                     //   move iso to that OAR's center
  → PTVCenters = { ptv.Center − center }             // target offsets relative to isocenter
  → Create_beams_from_config(BeamsParameters, ...)   // loops the 3 arc rows from App.config
        → Add_SRS_Beam(tableAngle, PTVCenters, ...)   // PTVCenters overload (the live one)
              → collrect    = CollRect(PTVCenters, 360 − tableAngle)
              → collsettings = GetCollsettings(collrect)   // margin + coll-angle heuristic
              → AddArcBeam(jaws = collsettings, coll = 10°|80°, gantryStart→Stop, couch, iso)
  → Create_SetupBeams_from_config(...)               // KV AP / KV RLAT / CBCT
```

Targets are expressed **relative to the isocenter** before any geometry runs (`center.FromTo(ptv.Center)` = `ptv.Center − center`), so the jaw rectangle that comes out is already in beam/iso-relative coordinates — exactly what `AddArcBeam` wants.

### 2.2 The full-sweep collimator box (`CollRect`) — the heart of the SIMT guarantee

Two nested rotations build one big point cloud:

1. **Couch rotation.** Every relative target center is rotated about the **Y axis** `(0,1,0)` by the couch angle. (The live caller passes `360 − tableAngle` — a deliberate sign fix for an Eclipse V15 angle-mirroring quirk, flagged in the source.)
2. **Gantry sweep.** For gantry `g = 0°…359°` in **1° steps**, each couch-rotated point is rotated about the **Z axis** `(0,0,1)` by `g`, and *every* rotated copy is appended to one accumulating list (≈ `360 × N_targets` points).
3. **Bound.** The result is bounding-boxed in **(X, Z)** only — world Y is discarded. The returned `Rect` has `Width = X-extent`, `Height = Z-extent`.

**Why discarding Y is correct, and why this can't clip a target.** Gantry rotation here is about Z (the patient sup-inf axis = the gantry rotation axis). For a beam at gantry `g`, the BEV X axis (MLC leaf-travel direction) is the in-plane axis perpendicular to both the beam and sup-inf; a target at in-plane radius `r` in the world X–Y plane projects onto BEV-X with magnitude up to `r`. As the sweep turns that target through all `g`, it visits the world-X axis at its full radius `r` for some angle — so `max|X|` over the cloud equals the **maximum in-plane radius**, the worst-case BEV-X excursion across the whole arc. The Z coordinate (sup-inf) is *invariant* under gantry rotation, so the Z-extent is simply the sup-inf spread of the targets and maps to the BEV-Y (cross-leaf) extent. Therefore the (X, Z) box is the tight envelope of every target's BEV footprint over a full revolution. Set static jaws to that box (plus margin) and **no target can leave the field at any gantry angle** — the union already covers the whole rotation. That is the entire correctness argument, and it's why a *static* jaw set is legitimate for a rotational SIMT plan.

### 2.3 Margin + collimator heuristic (`GetCollsettings`)

A fixed **20 mm** margin is added on all four sides. Then a portrait/landscape test picks the collimator angle and maps box axes to jaw axes:

- **Portrait** (`Width < Height`, i.e. sup-inf spread exceeds in-plane spread) → **collimator 10°**, with a *direct* mapping: X-jaws from the box X-range ± margin, Y-jaws from the box Z-range ± margin.
- **Landscape** (`Width ≥ Height`) → **collimator 80°**, with a *swapped, sign-flipped* mapping: the in-plane (world-X) content goes onto the **Y-jaws negated**, and the sup-inf (Z) content goes onto the **X-jaws**.

The collimator is **only ever 10° or 80°** — never continuously optimized. The choice orients the MLC so the **leaf-travel axis runs along the longer target distribution** (finer conformality where the targets are most spread out). The ~10° offset *off* the cardinal 0°/90° is a deliberate SIMT collimator kick: it de-aligns inter-leaf leakage / tongue-and-groove from target boundaries and from the streak direction between separated targets, which improves homogeneity in multi-met fields.

**On the landscape sign flips (the dispatch asked me to verify them).** The branch sets:
```
Y2 = −(Xmin − m)        Y1 = −(Xmax + m)        X1 = Zmin − m        X2 = Zmax + m
```
Check ordering: since `Xmax + m > Xmin − m`, we get `−(Xmax+m) < −(Xmin−m)`, so `Y1 < Y2` ✓; and `Zmax + m > Zmin − m` so `X1 < X2` ✓. The rectangle is well-ordered and preserves the correct *magnitudes* (extents), and the negation is what a ~90° collimator rotation requires to keep the field's handedness consistent. So the flips are **internally correct** (valid, ordered, extent-preserving). What I *cannot* confirm statically is whether the absolute sign matches Eclipse's collimator-angle handedness on a real machine — that is bound up with the same `360 − tableAngle` couch fix and must be verified on real plans (see §10). My read: it's correct, but it's exactly the kind of convention-locked sign I'd pin with one real case before trusting.

### 2.4 The refined projected-limit scan (`Rotate_n_Scan_Limits`) — present but dormant

This is the more elegant algorithm, and it differs from `CollRect` in four ways:

| | `CollRect` (live) | `Rotate_n_Scan_Limits` (dormant) |
|---|---|---|
| Angles scanned | brute-force 0–359° @ 1° | a supplied `rotangles[]` (meant to be the *actual* arc angles) |
| What's measured | accumulate all points, then bound (X,Z) | per-angle **min/max projection** onto MLC-aligned X and Y axes, then min-of-mins / max-of-maxes |
| Collimator | fixed 10°/80° heuristic afterward | `mlc_rotation_angle` is an **input**; axes are pre-rotated by it |
| Margins / limits | single 20 mm, no jaw clamp | separate `Margin_X`, `Margin_Y`, and a hard **clamp to ±200 mm** (jaw travel limit) |

Mechanically: for each arc angle it rotates the targets about the gantry axis, then projects onto the MLC Y axis `(0,0,1)` and MLC X axis `(−1,0,0)` *after those axes are themselves rotated by `mlc_rotation_angle` about Y*. It keeps the running min/max of each projection across all angles, pads by the per-axis margins, clamps to ±200 mm, and returns a `JW_iso_angle` bundle `{ mlc_rotation_angle, proj_x_Min/Max, proj_y_Min/Max, isocenter }` exposing `x_width` / `y_width` getters.

**Does it search over `mlc_rotation_angle` to minimize jaw area?** The *function* evaluates exactly **one** collimator angle and returns its rectangle — it does not loop. But its shape is purpose-built for an outer search: it returns the collimator angle alongside the resulting widths, so a caller can sweep `mlc_rotation_angle` (e.g. 0–90°), compute `x_width × y_width` for each, and pick the minimum-area collimator + jaws + iso bundle. **That outer loop does not exist anywhere in the repo.** So the optimal-collimator capability is *scaffolded but not wired*; the `Console.WriteLine("Jaw Width Test Summary…")` confirms it lived in a console test harness, not the WPF app.

**Which does the app use at runtime, and when?** **Always the simple `CollRect`/`GetCollsettings` path**, for every arc, unconditionally (the only branch is `if_use_existing_beams`, which skips beam creation entirely). The refined scan is never reached in production.

### 2.5 `CollSpan` (dead helper, noted for completeness)

Computes the pairwise maximum **in-plane** and **out-of-plane** spans between targets (out-of-plane = component along sup-inf `(0,0,1)`; in-plane = the perpendicular remainder via Pythagoras). It would feed a "do the targets fit one field / should I split the arc" decision. It is **not called**, and it contains a latent bug: it builds a couch-rotated list `PTVCentersRot` but then computes spans from the *un-rotated* `PTVCenters`, so the couch rotation is silently discarded. Mentioning it only so I don't resurrect the bug if I lift the idea.

---

## 3. The interesting ideas, distilled & parameterized

### Idea A — the rotation-union jaw envelope (the keeper)

The genuinely clever, reusable kernel:

```
INPUT:  targetCenters[]  (relative to isocenter, mm)
        couchAngle       (deg)
        gantryStep        = 1°        // sweep resolution
        margin            = 20 mm     // jaw padding, all sides
PROCESS:
  cloud = []
  for each c in targetCenters:
      c' = Rotate(c, axis=Y, couchAngle)
      for g in 0..360 step gantryStep:
          cloud += Rotate(c', axis=Z_gantry, g)
  box  = BoundingBox_in(X, Z)(cloud)              // world-Y dropped on purpose
OUTPUT: box  →  jaw rectangle (+margin) that never clips any target across a full arc
```

Named parameters I'd expose: `gantryStep` (1° is overkill for centers-only; 5° is indistinguishable and 5× faster), `margin` (their 20 mm), and **whether to sweep the full 360° or only the arc's actual angular range** — sweeping only the arc is tighter (smaller jaws, less normal-tissue dose) and is exactly what the dormant `Rotate_n_Scan_Limits` was reaching for.

### Idea B — portrait/landscape collimator selection

```
if   box.Z_extent > box.X_extent:  coll = baseAngle + kick      // ≈ 10°, leaves along sup-inf
else:                              coll = baseAngle + kick + 90  // ≈ 80°, leaves along in-plane
```
Parameters: `kick` (10°, the off-cardinal de-leakage offset) and the implicit decision metric (longer-axis → leaf-travel alignment). Two discrete angles is crude but robust; the principled version is Idea C.

### Idea C — area-minimizing collimator (the upgrade their dormant code implies)

```
best = argmin over coll in [0..90° step Δ] of:
           (x_width(coll) · y_width(coll))
       where widths come from per-arc-angle projected limits (clamped to ±200 mm)
return { coll, jawRect, iso }
```
This replaces the binary 10/80 with a continuous optimum and uses the *arc's real angles* rather than a full revolution — strictly tighter fields. Parameters: collimator search grid `Δ`, per-axis margins `Margin_X`/`Margin_Y`, jaw clamp `±200 mm`.

### Idea D — OAR-aware isocenter override

```
iso = boundingBoxCenter(prescribedTargets)            // default
if any target within ovlpThresh (= 0.5 cm) of an important OAR:
    iso = center(nearest such OAR)                    // snap onto the OAR
```
Parameter: `ovlpThresh` (0.5 cm). Rationale: putting iso *on* the critical OAR minimizes the rotational setup-error lever arm where it matters most.

---

## 4. Coordinate-system machinery & conventions

- **Rotation primitive** (`Point3D.RotCoordSys` / `Rect3D.RotCoordSys` in `SRSBeamSetup.cs` and `Vector_Operations.cs`): normalizes the axis, builds a `Quaternion(axis, angleDeg)`, and applies it via `Matrix3D` — a right-handed, axis-angle active rotation in WPF Media3D. `Rect3D.RotCoordSys` rotates the 8 box corners and re-bounds (axis-aligned re-box), so a rotated box grows to enclose the rotated original — fine for envelopes, lossy as an exact transform.
- **Axis assignment used by the geometry:**
  - **Couch / table** rotation → about **Y** `(0,1,0)`.
  - **Gantry** rotation → about **Z** `(0,0,1)` (= patient sup-inf, the physical gantry axis).
  - **MLC / collimator** rotation in the dormant scan → about **Y** `(0,1,0)`; projection axes are MLC-Y `(0,0,1)` and MLC-X `(−1,0,0)`.
- **Handedness / direction:** quaternion rotations are right-handed about the given axis with degrees. The `360 − tableAngle` adjustment in the live caller, plus the couch values in config being the *mirror* of the labels (couch `45` labelled `T315`, couch `315` labelled `T045`), together encode an **Eclipse V15 angle-mirroring idiosyncrasy** — i.e., the app's internal couch sign is the negative of what Eclipse displays. This is the single most convention-fragile spot in the subsystem and the thing most likely to differ on my v16.1.
- **`BaryCentricCoordinates`** (in both `SRSBeamSetup` and `Vector_Operations`): standard area-ratio barycentrics of a point vs a triangle (`u, v, 1−u−v`) built from the cross-product area helper. **Not used** by the live flow; it's a general geometry utility (likely intended for point-in-triangle / interpolation work that never landed). Note it's *duplicated* verbatim across two files — exactly the DRY violation I'd collapse on reimplementation.
- **`Vector_Operations`** also carries `Round_up_relative_coordinate` (snap iso to a 5 mm grid relative to UserOrigin) — **not** used by the live iso placement, which instead rounds to 1 mm in `FindGeometricCenter`. So there are two competing rounding policies in the tree; the 1 mm one wins at runtime.

---

## 5. MLC aperture analysis (`AP_lib/MLC.MLC_misc`)

`test_open_leaves_range_inMM(Beam)` measures the **actual open aperture (sup-inf / Y extent)** of a finished beam *from its delivered MLC*, not from the jaws:

1. For each leaf pair `j`, scan all control points and keep the **maximum opening** `LeafPositions[1,j] − LeafPositions[0,j]` (bank-B minus bank-A) seen anywhere along the arc.
2. `find_Y_limits(dists[60])` finds the **first** and **last** leaf pair that is ever open (`> 1e-6`) and maps those indices to physical Y positions in mm.
3. The index→mm map hard-codes a **Millennium-120 leaf geometry**: pairs 0–9 are 10 mm, pairs 10–49 are 5 mm, pairs 50–59 are 10 mm (it `throw`s if the array isn't length 60 — "the only MLC geometry we know"). Two maps (`map_i_lower`/`map_i_upper`) give the inner/outer edge of the boundary leaves.

**What it's for:** it's an independent, MLC-derived check on the **realized Y aperture** — i.e., did the optimizer actually use the field the jaw box promised? Its natural uses are QA / reporting / validating the jaw fit after optimization. Like the refined scan, it is **defined but never called** in the app — pure analysis/QA scaffolding.

**Relevance to my CreateQAPlan:** this is the seed of a useful verification primitive — "reconstruct the true open aperture from delivered leaf positions and compare to the planned jaws." But the hard-coded Millennium-120 map is a liability; my QA work spans HD-120 (2.5 mm center) and other geometries, so I'd drive the index→mm map from the machine's actual leaf-boundary table rather than constants.

---

## 6. Isocenter placement (`FindGeometricCenter`)

- It collects, for each target, the **min and max corners of that target's mesh bounds**, then takes the **min-of-mins and max-of-maxes across all targets**, and returns the **midpoint of that overall bounding box**, rounded to 1 mm.
- So it is a **bounding-box center, NOT a volume centroid** — it is not mass-weighted. A large or peripheral target pulls the box; many small central targets do not anchor it.
- **Override:** `AutoPlan` then runs `GetOverlapStructuresInfo` and, if any prescribed PTV is within `Imp_OAR_PTV_distanceInCM` (= 0.5 cm) of an important OAR, **relocates iso to that OAR's center**, ordered by nearest. Otherwise iso stays at the box center.
- **Implications for off-axis targets (real SIMT concern):** a single iso means peripheral targets sit far off-axis. Rotational setup error scales with distance-to-iso, so the bounding-box center (which sits between extremes rather than where the targets *are*) can leave outliers with larger off-axis lever arms than a centroid would. This is the classic SIMT trade-off (one iso, many mets) and the box-center choice is the simplest defensible pick — but it's worth measuring max off-axis distance and flagging it, which the app does not do.

---

## 7. Overlap analysis (`GetOverlapStructuresInfo`)

For every **PTV × OAR** pair:

- Compute the Boolean **intersection** (`And`). If non-empty → record `overlap% = intersectionVolume / OAR_volume × 100` and distance `0`.
- If empty → estimate **minimum surface distance** by sampling both meshes' vertices with an **adaptive stride** (`stride = max(1, ⌊volume^(1/3) × 20⌋)` per structure, so bigger structures are sampled more coarsely — a speed/accuracy trade), taking the min squared vertex-to-vertex distance, and converting mm → cm (`× 0.1`).
- High-res/low-res mismatches are handled by promoting the lower-res structure to high-res before the Boolean.
- Returns `List<OverlapStructuresInfo>{ PTV, OAR, Distance_cm, OverlapFracRelStruct2 }`.

**How it feeds beam setup:** the *only* geometric consumer in this dispatch is the **isocenter override** in §6 — pairs with `Distance_cm ≤ 0.5` trigger the snap-to-OAR. (Whether the same overlap info also drives buffer/ring creation is Dispatch C's call; I see it consumed for iso placement here, not for jaw geometry.) Note the distance is an **approximate, sub-sampled vertex-to-vertex min**, not an exact surface distance — fine for a 0.5 cm gate, not something I'd report as a precise gap.

---

## 8. Arc / beam geometry (as configured)

From `App.config` (`BeamsParameters`, format `Name,couch,gantryStart,gantryStop`):

| Beam | Couch (internal) | Eclipse label | Gantry start→stop | Direction | Span | Plane |
|---|---|---|---|---|---|---|
| `CCW`       | 0°   | 0°   | 179° → 181° | CCW | ≈ 358° (near-full) | coplanar |
| `CW1_T315`  | 45°  | 315° | 181° → 0°   | CW  | ≈ 179° (half)      | non-coplanar (couch kick) |
| `CW2_T045`  | 315° | 45°  | 345° → 179° | CW  | ≈ 194° (half)      | non-coplanar (couch kick) |

So: **3 VMAT arcs** = one full coplanar arc + two half non-coplanar arcs at ±45° couch kicks — a manual, HyperArc-like SIMT geometry. Direction is parsed from the **beam name prefix** (`CW`/`CCW`); each arc gets its **own** `CollRect`/`GetCollsettings` (different couch → different envelope → independently 10° or 80° collimator and its own jaw box). Gantry direction is also why the names start with CW/CCW — `Add_SRS_Beam` throws if a name doesn't.

**Setup beams** (`SetupBeamsParameters`, format `Name,couch,gantry,x1,y1,x2,y2`): `KV AP`, `KV RLAT`, `CBCT` — all couch 0°, gantry 0°, jaws ±75 mm (15 × 15 cm), collimator 0°.

**Machine:** `6X` FFF, 1400 MU/min, ARC technique (`ExternalBeamMachineParameters = 6X;1400;ARC;FFF`), on `UM_TB5`/`UM_TB3` (TrueBeam).

**`if_4_beams`:** a ViewModel `bool` (default `false`) whose XAML checkbox is **commented out**. It is get/set only and **wired to nothing** — beam count comes entirely from the config string (3). It's a vestigial "use 4 arcs" toggle that was abandoned; the live arc count is fixed by config, not by this flag.

**Alternate (unused) beam overload.** `Add_SRS_Beam` has a *second*, commented-out overload that takes a single corner vector `tp` and uses a different collimator rule: `colrotation = (|tp × n| < tp·n) ? 15° : 105°` (where `n` is the table-plane normal `(sin θ, 0, cos θ)`), followed by `FitCollimatorToStructure(margin 40 mm)`. This is the older "fit to the union structure" approach (note the same ~15° off-cardinal kick idea). It's superseded by the `PTVCenters` overload and not used — but it documents that the team tried a fit-to-structure strategy before settling on the analytic rotation-union box.

---

## 9. Generalized SIMT jaw/collimator spec (reusable utility)

This is the lift-and-own deliverable — clean, parameterized, machine-agnostic, my own restatement:

```
SimtFieldFor(targetCentersIsoRelative, couchAngle, opts) -> { collAngle, jawRect }

  parameters (named, not magic):
     opts.margin        = 20 mm        // jaw padding each side
     opts.gantrySweep   = arc range    // FULL 360 (their live choice) OR the arc's real [start,stop]
     opts.gantryStep    = 1°           // 5° is plenty for centers-only
     opts.collKick      = 10°          // off-cardinal de-leakage offset
     opts.jawLimit      = ±200 mm      // clamp to hardware travel
     opts.collStrategy  = BINARY | MIN_AREA

  1. cloud = ⋃_{g in gantrySweep step gantryStep} Rotate( Rotate(targets, Y, couchAngle), Z, g )
  2. box   = BoundingBox(cloud) projected to (X = in-plane, Z = sup-inf)
  3. collStrategy:
       BINARY:                       // their live heuristic
          coll = (box.Zext > box.Xext) ? collKick : collKick + 90
          jawRect = mapBoxToJaws(box, coll, margin)   // direct or swap+flip per coll
       MIN_AREA:                     // the upgrade their dormant scan implies
          coll = argmin_{c in [0,90] step Δ} width_x(box@c)·width_y(box@c)
          jawRect = clamp( pad( projectedLimits(targets, gantrySweep, c), margin ), jawLimit )
  4. return { coll, jawRect }   // iso-relative; never clips any target across the arc
```

Design decisions surfaced for me to make *deliberately*:
- **Full-360 sweep vs arc-only projection.** Full-360 (live) is bullet-proof and trivial but over-opens for partial arcs; arc-only (dormant) is tighter — material dose savings on the two half-arcs. I'd default to **arc-only**.
- **Binary vs min-area collimator.** Binary is robust and explainable; min-area is tighter but needs the off-cardinal kick re-imposed (a pure min-area optimum will happily sit at 0°/90° and reintroduce leakage alignment). I'd run **min-area constrained away from cardinals**, keeping the kick.
- **Jaw clamp.** The live path has **no ±200 mm clamp** — for widely separated mets the 20 mm-padded box can exceed jaw travel and the API call would fail or silently saturate. I'd always clamp and warn.
- **Centers-only is an approximation.** Both algorithms use target *centers*, not surfaces, then rely on the margin (20 mm) to cover target radius + setup. For my reimplementation I'd either pad by per-target radius or feed surface points, so the margin is purely a setup/penumbra term rather than secretly absorbing target size.

---

## 10. Transfer to Pscripts

- **`Pscripts.Esapi` — new SIMT geometry utility.** Lift §9 as a self-contained `static` utility: input target centroids + couch angle, output collimator angle + iso-relative jaw `VRect`. Their methods are hundreds of lines; mine should be the ≤20-line decomposition — `BuildEnvelope`, `MapBoxToJaws`, `PickCollimator`, each pure and unit-testable against synthetic target clouds (a single off-axis point at known radius has an analytic answer, so the rotation-union is easy to test). Drop the duplicated barycentric/cross-product helpers into one vector module (they're copy-pasted across three files here).
- **`Pscripts.Esapi` / `EsapiPluginContextHost`.** The couch-sign / `360 − tableAngle` quirk is **version-specific (Eclipse V15)**. On my v16.1 I must re-derive the couch and collimator sign empirically, not copy theirs — bake a one-time "convention probe" into the host rather than trust a constant.
- **`CreateQAPlan` ↔ MLC aperture analysis (§5).** Adopt the *concept* — reconstruct realized aperture from delivered leaf positions and diff against planned jaws — as a QA assertion. **Reject** the hard-coded Millennium-120 index→mm table; drive it from the machine's leaf-boundary metadata so it works for HD-120 and others.
- **Isocenter strategy.** Their box-center + OAR-snap is a reasonable default, but for my apps I'd offer **centroid vs box-center** as an explicit choice and always compute/flag **max off-axis distance** (the SIMT quality metric they never surface).
- **Overlap/distance (§7).** The adaptive cube-root vertex stride is a nice cheap-distance trick worth keeping for coarse gates; for anything reported as a real gap I'd use exact `DistanceToPoint`-style surface distance, not sub-sampled vertices.

---

## 11. Adopt / Adapt / Avoid

| Item | Verdict | Why |
|---|---|---|
| **Rotation-union jaw envelope** (`CollRect` core) | **Adopt** (re-implement) | Elegant, provably non-clipping, trivially testable. The keeper of this dispatch. |
| Drop world-Y, bound only (X, Z) | **Adopt** | Correct and efficient — gantry rotation maps in-plane radius into X; Z is invariant. |
| Arc-only angular sweep | **Adopt** (from the dormant scan) | Tighter fields / less normal-tissue dose than full-360. |
| OAR-snap isocenter override (0.5 cm gate) | **Adopt** | Sound rationale — shortens the rotational lever arm on the critical OAR. |
| Adaptive cube-root vertex stride for min-distance | **Adopt** (coarse gates only) | Cheap, good enough for a 5 mm threshold. |
| Off-cardinal collimator kick (~10°) | **Adopt** the idea | Real SIMT benefit (de-aligns leakage / streaks). |
| Binary 10°/80° collimator selection | **Adapt → MIN_AREA, kick-constrained** | Continuous area-minimization (their dormant scan) is strictly better; keep the kick so the optimum doesn't snap to a cardinal. |
| Box-center isocenter | **Adapt** | Offer centroid as an option; always report max off-axis distance. |
| MLC aperture reconstruction (`MLC_misc`) | **Adapt** for `CreateQAPlan` | Good QA primitive; replace hard-coded Millennium-120 map with machine-driven leaf table. |
| 20 mm jaw margin with **no ±200 mm clamp** | **Adapt — add the clamp** | Live path can exceed jaw travel for widely separated mets. |
| Centers-only (no target-radius padding) | **Adapt** | Pad by per-target radius / use surfaces so margin is purely setup+penumbra. |
| `360 − tableAngle` / mirrored couch labels | **Avoid copying** | Eclipse V15-specific; re-derive sign on v16.1. |
| Hundreds-of-line methods, duplicated helpers (barycentric ×3, RotCoordSys ×2) | **Avoid** | Against my ≤20-line / DRY standard; collapse to one vector module. |
| `CollSpan` | **Avoid** | Dead, and buggy (computes spans from un-rotated points; couch rotation discarded). |
| `if_4_beams` flag | **Avoid** | Vestigial, wired to nothing. |
| First `Add_SRS_Beam` overload (`FitCollimatorToStructure`, coll 15/105) | **Avoid** (note only) | Superseded fit-to-structure approach; documents history, not the live design. |

---

## 12. Open questions / verify-on-real-data

1. **Collimator sign on v16.1.** The landscape-branch negations and the `360 − tableAngle` couch fix are correct *internally* but convention-locked to Eclipse V15. Confirm on one real multi-met plan that coll 80° + the flipped jaws actually encloses the landscape targets (and that couch 45 vs 315 lands where intended).
2. **Jaw-travel saturation.** Find the max target separation at which the live path's 20 mm-padded, unclamped box exceeds ±200 mm — does `AddArcBeam` throw, clamp, or silently truncate? (Drives whether the clamp is a nicety or a safety fix.)
3. **Centers-only adequacy.** How much of the 20 mm margin is actually consumed by target radius vs setup? On large targets the field could be tighter than it looks because the center sweep ignores the target's own extent. Measure on real targets.
4. **Was the projected-limit scan ever validated?** `Rotate_n_Scan_Limits` + the min-area collimator search are scaffolded but unwired. Confirm whether the team benchmarked it against `CollRect` (tighter fields? better OAR sparing?) before shelving it — that tells me whether MIN_AREA is worth the complexity.
5. **Gantry-step sensitivity.** Does 1° vs 5° change the box at all for centers-only? (I expect not — relevant only to compute cost.)
6. **Off-axis dosimetric penalty.** Quantify, on a spread multi-met case, how far the box-center iso sits from the centroid and whether outliers' off-axis distance materially degrades conformality vs a centroid iso.

---

## 13. Clean-room attestation

This document is my own original analysis — mechanism, geometry, and design intent restated in my words, with all algorithms reconstructed and re-parameterized. No GPL-3 source from `CSMayoLab/SRSAutoPlan` was copied, transcribed, translated, or closely paraphrased into this output; the only verbatim fragments are the short identifier/signature references and the two single-line config strings strictly necessary to point at locations, clearly marked as quotation. The cloned repository's working tree was not modified, built, or executed.
