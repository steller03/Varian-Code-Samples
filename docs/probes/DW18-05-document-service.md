# DW18-05 — DocumenServiceSample (retrieve patient documents from ARIA's local document service)

**Cluster 14 delta** — exemplar [DW18-01 VAIS](DW18-01-vais-aria-webservice.md).

- **Problem:** a WPF testbed that POSTs a `GetDocumentsRequest` (by patient `PtId`) to ARIA's local
  document web service over the gateway REST API and shows the JSON response — a hand-driven harness
  for the document-retrieval slice of the ARIA web-service stack.
- **Differs from the exemplar:** DW18-01's clean `OidcClient` + loopback flow is replaced by a
  two-mode auth **switch** the operator toggles: **AD/basic** —
  `Authorization: Basic base64(user:pass)` (`SecureString`) plus an `ApiKey` header; or **STS** —
  `Authorization: Bearer <token>` where the token comes from `STSHelper.GetHeadlessToken` (the
  client-credentials grant; the *interactive* client is left as a commented `TODO`). The data plane
  is a raw `HttpWebRequest`/`HttpWebResponse` POST of a literally-typed JSON request (no
  `DataContractJsonSerializer`/typed contracts like DW18-01), with 401/400/404 mapped to friendly
  hints. The acquired JWT is decoded with `JwtSecurityTokenHandler.ReadJwtToken` for display.
- **Surfaces it adds:** the document-service `GetDocumentsRequest` JSON shape, Basic-auth header
  construction from a `SecureString`, raw `HttpWebRequest` POST, `JwtSecurityTokenHandler`.
- **Reuse note:** the liftable bits are the **dual-auth switch** (Basic+ApiKey vs Bearer) and the
  minimal `HttpWebRequest` JSON-POST helper with status-code messaging; the `GetDocumentsRequest`
  payload is the one new request type. DW18-01 remains the cleaner OIDC template — prefer its
  interactive flow (this sample's is a TODO) and heed its own warning not to store secrets/ApiKeys
  in `app.config`. Verdict Adaptable.
