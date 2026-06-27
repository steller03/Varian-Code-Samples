# DW16-07 — MSExcelFormBinary (demographics + Rx dose → Excel, binary variant)

**Tier D lightweight.** The same demographics-and-prescription-dose export to a new Excel workbook as
DW16-06, packaged as a binary-plugin project — the only code difference is the commented
`[assembly: ESAPIScript(IsWriteable = true)]` line.

- **ESAPI surface:** identical to DW16-06 — `Patient.LastName/FirstName/Id`, `PlanSetup.TotalDose.Dose`
  + Office Interop Excel.
- **Pointer:** byte-for-byte twin of [DW16-06 MSExcelForm](DW16-06-excel-demographics.md) (cluster 17),
  differing only in project packaging.
