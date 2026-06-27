# DW16-26 — Advanced8Kata (4D-phase HU at body center via voxel access)

**Tier D lightweight.** Standalone exe that gathers all 3D images sharing the planning image's frame of
reference (the 4D gating phases), reads the HU at the BODY center point in each, and compares the
across-phase max/average against the MIP and average scans.

- **ESAPI surface:** `Image.GetVoxels(slice, buffer)` + `Image.VoxelToDisplayValue`, with
  `Image.FOR/Origin/XRes/XDirection` for voxel↔coordinate mapping; `Series.Study.Series` to enumerate
  same-FOR images.
- **Pointer:** the 4D-phase variant of the voxel/CT-number theme — see [DW16-14
  MeanCTNumber](DW16-14-mean-ct-number.md) for the probed voxel-access exemplar.
