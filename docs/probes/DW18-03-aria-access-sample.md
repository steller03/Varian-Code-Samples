# DW18-03 — ARIAAccessSample (patient/appointment search over ARIA-Access + FHIR)

**Cluster 14 delta** — exemplar [DW18-01 VAIS](DW18-01-vais-aria-webservice.md).

- **Problem:** a WinForms client that searches ARIA patients and machine appointments, creates
  patient/appointment records, and additionally does a FHIR patient search — all over web services.
- **Differs from the exemplar:** same OIDC **authorization-code** login as DW18-01 (`SystemBrowser`
  loopback + `OidcClient.LoginAsync` / `RefreshTokenAsync`), but the data plane is the **ARIA Access**
  contract set (`PatientSelectionRequest`, `GetMachineAppointmentsRequest`, `VMS.AWC.Link.*.WebService.Contracts`)
  POSTed via `ARIAAccessHelper.SendRequestData(request, url, bearerToken)`; create-patient/appointment
  bodies are read from files. It also demos a genuine **FHIR** path (DW18-01 only labelled it):
  `Hl7.Fhir.Rest.FhirClient.Search<Patient>(family=…, given=…)` with the `Bearer` token injected via
  an `OnBeforeRequest` handler and the bundle serialized with `FhirJsonSerializer`.
- **Surfaces it adds:** `VMS.AWC.Link` ARIA-Access request/response contracts, `Hl7.Fhir` `FhirClient` / `FhirJsonSerializer`.
- **Reuse note:** beyond DW18-01's settings gateway, the two reusable read paths here are the
  ARIA-Access `SendRequestData` request/response shape and the **FHIR-client-with-bearer** search
  (`OnBeforeRequest` header injection is the clean way to authenticate Hl7.Fhir). Verdict Adaptable.
