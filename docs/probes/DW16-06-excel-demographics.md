# DW16-06 — MSExcelForm (demographics + Rx dose → Excel)

**Tier D lightweight.** Binary plugin that writes patient name, MRN, today's date, and total prescribed
dose into a fresh Excel workbook via Office Interop, then shows it for the user to edit.

- **ESAPI surface:** `Patient.LastName/FirstName/Id` and `PlanSetup.TotalDose.Dose`; everything else is
  `Microsoft.Office.Interop.Excel`.
- **Pointer:** exemplar of cluster 17 (patient demographics → Excel); [DW16-07
  MSExcelFormBinary](DW16-07-excel-demographics-binary.md) is the byte-identical twin.
