# DW16-24 — SplitStructure (split an OAR into target-proximal / -distal halves)

**Cluster 11 delta** — exemplar [W1804-02 CreateOptStructures](W1804-02-create-opt-structures.md).

- **Problem:** split a normal-tissue ROI (e.g. `LIVER`) into target-proximal and target-distal
  volumes relative to a PTV — useful for differential objectives on the near vs far side of an OAR.
- **Differs from the exemplar:** a **geometry-driven** split rather than a fixed margin. Computes the
  distance between target and ROI `CenterPoint`s, uses `GetSegmentProfile` (a ray from target center
  toward the ROI) to find the distance to the target *surface*, then grows the target by
  `dist − surfaceDist` so the expansion crosses the ROI's mass center: `spl1 = expansion.And(roi)`
  (proximal), `spl2 = roi.Sub(spl1)` (distal). Ships a `LargeMargin` extension that **chains 50 mm
  `Margin` calls** to beat ESAPI's 50 mm margin ceiling.
- **ESAPI surfaces it adds:** `Structure.CenterPoint`, `GetSegmentProfile` → `SegmentProfile` / `SegmentProfilePoint`, plus the `LargeMargin` 50 mm-cap workaround.
- **Reuse note:** `LargeMargin` and the profile-based "distance to surface" measure are the reusable nuggets; the split itself is approximate (segment-model coverage gaps, noted in-source). Verdict Adaptable.
