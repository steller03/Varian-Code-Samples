# DW16-23 — ExtractBodySection (axial body slab bounded by a structure's z-extent)

**Cluster 11 delta** — exemplar [W1804-02 CreateOptStructures](W1804-02-create-opt-structures.md).

- **Problem:** copy a section of the EXTERNAL/body bounded by an existing structure's superior and
  inferior slices, extended by ± margins — i.e. isolate an axial body slab around a target.
- **Differs from the exemplar:** works in **image/slice space**, not pure Boolean margins. Scans
  slices for the first/last where the source structure has contours (`GetContoursOnImagePlane`),
  extends up/down by mm→slices using `Image.ZRes`, draws a giant full-plane rectangle contour
  (±10000 mm `VVector` corners) on every slice in range via `AddContourOnImagePlane`, then `.And`s
  with the EXTERNAL body to clip to patient outline. Ships a small WPF structure-picker window.
- **ESAPI surfaces it adds:** `Image.ZSize`/`ZRes`, `Structure.GetContoursOnImagePlane(z)`, `AddContourOnImagePlane(VVector[], z)`, `VVector`.
- **Reuse note:** the "find slice range → stamp full-plane rectangles → intersect with body" trick is the reusable recipe for carving an axial slab when a margin/Boolean won't express it. Verdict Adaptable.
