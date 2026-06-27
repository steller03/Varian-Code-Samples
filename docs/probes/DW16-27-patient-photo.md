# DW16-27 — PatientPhoto (WPF plugin fetching photo from ARIA DB via Entity Framework)

**Tier D lightweight.** WPF binary plugin showing a patient's photo, demographics, and physician — but
the photo and physician name are pulled **not via ESAPI** but by querying the ARIA SQL DB directly
through an Entity Framework `DbContext` (`AriaEntityContext` → `Patients`/`Doctors`/`Photos`).

- **ESAPI surface:** only `Execute(ScriptContext, Window)` + `ScriptContext.Patient` (id, name, DOB,
  `PrimaryOncologistId`) for identity; all data access is EF against a hardcoded `VARIAN` connection
  string.
- **Pointer:** an EF-DB-access scaffolding template — cluster 18 (exemplar [W2001-01
  DoseMetricExample](W2001-01-dose-metric-mvvm.md)); the only sample in the catalogue reaching the ARIA
  DB through Entity Framework.
