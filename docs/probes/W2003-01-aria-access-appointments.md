# W2003-01 — AAWebServiceTests (ARIA Access REST → weekly machine appointments per patient)

**Cluster 14 delta** — exemplar [DW18-01 VAIS](DW18-01-vais-aria-webservice.md); sibling
[DW18-03 ARIAAccessSample](DW18-03-aria-access-sample.md) (same contract family).

- **Problem:** query the ARIA Access web service (a REST/JSON gateway, not ESAPI) for one machine's
  appointments over a week, then tally appointment count per patient — a template for pulling
  scheduling data out of ARIA over the web-service link.
- **Differs from the exemplar:** **no OAuth at all.** Where DW18-01 runs the OIDC bearer-token flow,
  this authenticates with a static **`ApiKey`** request header plus `UseDefaultCredentials = true`
  (Windows integrated auth) on a plain `HttpClient`. The data plane is the strongly-typed
  `GetMachineAppointmentsRequest` from the `services.varian.com.AriaWebConnect.Link` contracts (the
  844 KB auto-generated `Gateway.cs` proxy — same ARIA-Access family DW18-03 uses), serialized with
  Newtonsoft, POSTed synchronously (`Task.WaitAll`), and deserialized into
  `GetMachineAppointmentsResponse`; results are bucketed into a `patientId → count` dictionary. The
  `__type` JSON discriminator is spliced onto the serialized body by hand.
- **Surfaces it adds:** `GetMachineAppointmentsRequest`/`Response` and the
  `services.varian.com.AriaWebConnect.Link` / `.Common` typed contracts; `HttpClient` with an
  `ApiKey` header + `UseDefaultCredentials`.
- **Reuse note:** liftable as the **minimal ARIA-Access REST template** — api-key + typed request +
  POST + deserialize — and the appointment-tally is a clean scheduling-analytics seed (machine load,
  no-show rates, utilization). For production prefer DW18-01's token auth over a baked-in `ApiKey`,
  and replace the brittle `__type` string-splicing with proper contract serialization. Verdict
  Adaptable.
