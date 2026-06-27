# DW14-07 — DoseProfiles (dose at isocenter + profile to dose max)

**Tier D lightweight.** Binary plugin that shows the first beam's isocenter coordinates and the dose
there, then samples a dose profile along the line from isocenter to the 3D dose-max location and writes
the points to a file.

- **ESAPI surface:** `Dose.GetDoseToPoint`, `Dose.GetDoseProfile(start, end, double[])`,
  `Dose.DoseMax3DLocation`; iterates `ProfilePoint.Position/Value`.
- **Pointer:** cluster 4 (line/profile extraction) — exemplar [ESAP-11
  ProfileSamples](ESAP-11-profile-samples.md); near-twin of [DW18-07 DoseProfile](DW18-07-dose-profile.md).
