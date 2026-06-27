# DW18-07 — DoseProfile (horizontal line dose profile → CSV)

**Tier D lightweight.** Binary plugin that samples a 201-point horizontal dose profile across the dose
grid (x = −100…+100 mm at y = −100, z = 0) and writes `Position,Dose` to a desktop CSV.

- **ESAPI surface:** `Dose.GetDoseProfile(VVector start, VVector end, double[])` → `DoseProfile` /
  `ProfilePoint.Position.x/Value`.
- **Pointer:** cluster 4 (line/profile extraction) — exemplar [ESAP-11
  ProfileSamples](ESAP-11-profile-samples.md); near-identical to [DW14-07
  DoseProfiles](DW14-07-dose-profiles.md) (this one samples a fixed horizontal line vs iso→max).
