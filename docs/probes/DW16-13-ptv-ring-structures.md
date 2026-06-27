# DW16-13 — Intermediate_6 (ring/control structures around every PTV)

**Cluster 11 delta** — exemplar [W1804-02 CreateOptStructures](W1804-02-create-opt-structures.md).

- **Problem:** auto-create a 5 mm ring ("control") structure around *each* PTV in the structure set.
- **Differs from the exemplar:** loops all `Structures.Where(DicomType=="PTV")` instead of one named
  PTV, and builds a true **annulus** via `ptv.Margin(5).And(ptv.SegmentVolume.Not())` (the expansion
  *minus the PTV itself*) rather than a single `Sub`. Guards each add with `CanAddStructure` and
  truncates the ring `Id` to ESAPI's 16-char limit; DICOM type `"CONTROL"`.
- **ESAPI surfaces it adds:** `SegmentVolume.Not()` + `.And()` for the ring shell, `DicomType` filtering, 16-char structure-Id truncation.
- **Reuse note:** the `Margin().And(.Not())` ring formula and the per-PTV loop are the liftable bits — drop-in for generating dose-falloff control rings across a whole plan. Verdict Liftable.
