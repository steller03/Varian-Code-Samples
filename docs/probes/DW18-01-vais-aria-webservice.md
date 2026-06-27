# DW18-01 — VAIS (OAuth/OIDC bearer-token access to ARIA over web services)

| Field | Value |
|---|---|
| ID | DW18-01 |
| Solution | Dev Workshop 2018 (VAIS) |
| Source event | Developer Workshop 2018 |
| ESAPI version | unknown (web-service stack, not local ESAPI) |
| Type | Standalone exe |
| Reuse verdict | Adaptable |

## Problem
Reach ARIA data from *outside* the local Eclipse scripting model — a web app, a service, or a machine with no Eclipse install — by going through Varian's VAIS / Shared Framework gateway over authenticated HTTP instead of the in-process ESAPI object model. The sample shows the two OAuth shapes a client can use to get a token and then read framework settings (shared settings, data source, privileges, app roles) over the wire. It's the seed pattern for cross-machine ARIA integrations where `Application.CreateApplication` isn't an option.

## Approach
Two client flavors demonstrate the two OAuth grant types. **InteractiveClient** (WPF) runs the OpenID Connect *authorization-code* flow for a human user: `SystemBrowser` grabs a random unused loopback port, builds a `http://127.0.0.1:{port}` redirect URI, and `OidcClient.LoginAsync` (IdentityModel.OidcClient) opens the system browser to the authority. A `LoopbackHttpListener` — a tiny Kestrel `IWebHost` bound to that loopback URL — captures the redirect callback (GET query string or form POST), completes a `TaskCompletionSource`, and hands the authorization response back to OidcClient, which exchanges it for `AccessToken` / `IdentityToken` / `RefreshToken`. `RefreshTokenAsync` renews silently. **TrustedClient** (console) instead runs the *client-credentials* flow for a service identity: `DiscoveryClient.GetAsync` reads the OIDC discovery doc, then `TokenClient.RequestClientCredentialsAsync(scope)` (client id + secret) returns the access token with no browser at all.

With a token in hand, both call into a reader (`SharedFrameworkReader` / `SFSettingsReader`) that POSTs to the gateway URI with an `Authorization: Bearer <token>` header. Requests/responses are the VAIS `VMS.SF.Gateway.Contracts` types (`GetSettingsRequest`/`GetSettingsResponse`, `GetPrivilegesRequest`), serialized via `DataContractJsonSerializer`; the embedded XML setting payloads are then `XmlSerializer`-deserialized into `SharedSettings` / `DataSource` POCOs. `JWTTokenHelper` decodes the JWT (`JwtSecurityTokenHandler`) for display and checks `exp` (via NodaTime) to gate calls behind `IsTokenExpired`; `JsonHelper` is just pretty-printing. Note: despite the "FHIR" label, the data plane here is the Shared Framework settings gateway (JSON request/response contracts), not literal FHIR resources.

## Key surfaces (web-service / auth — not ESAPI)
- **IdentityModel.OidcClient**: `OidcClient`, `OidcClientOptions`, `LoginRequest`, `LoginAsync` / `RefreshTokenAsync`, `IBrowser` (`SystemBrowser`), `Policy`/`DiscoveryPolicy`.
- **IdentityModel.Client**: `DiscoveryClient.GetAsync`, `TokenClient.RequestClientCredentialsAsync` (client-credentials grant).
- **Loopback redirect capture**: `LoopbackHttpListener` over `WebHostBuilder`/Kestrel (`UseUrls`, `Configure`), `TaskCompletionSource<string>`, random-port via `TcpListener`.
- **Gateway query**: `WebRequest`/`HttpWebResponse` POST with `Authorization: Bearer`, `DataContractJsonSerializer`, `VMS.SF.Gateway.Contracts` (`GetSettingsRequest/Response`, `GetPrivilegesRequest`), `VMS.SF.Infrastructure.Contracts`.
- **JWT**: `System.IdentityModel.Tokens.Jwt` (`JwtSecurityTokenHandler`, `JwtSecurityToken`, `exp` claim), NodaTime `Instant`/`Duration`.
- **Config keys (`ConfigurationManager.AppSettings`)**: `Authority`, `ClientIdentifier`, `ClientSecret`, `Scope`, `GatewayTokenUri`.

## Reusability
The high-value liftable pieces are deployment-agnostic: the **OIDC authorization-code + loopback-listener pattern** (`SystemBrowser` + `LoopbackHttpListener` + `OidcClient`) is a clean, reusable desktop-app sign-in you can drop into any native client that needs an interactive token, and the **bearer-token gateway client** (build request, attach `Bearer`, POST, deserialize) is the reusable read path. The client-credentials variant in TrustedClient is the template for unattended services. What must be ported is everything environment-specific: the `Authority`, `GatewayTokenUri`, `ClientIdentifier`/`ClientSecret`, and `Scope` in app config all point at a particular VAIS gateway, and the request/response shapes are bound to that `VMS.SF.Gateway.Contracts` version — this is a 2018 VAIS deployment, so contract names, scopes, and the IdentityModel API surface (pre-`TokenClient`-deprecation) will need updating against the current gateway/SDK. The hard-coded `ClientSecret = "secret"` and disabled discovery validation (`ValidateEndpoints/ValidateIssuerName = false`) are demo shortcuts to fix before any real use.

## Idea sparks
- A read-only web/mobile **ARIA dashboard** that authenticates users via the OIDC flow and pulls framework/settings data without a local Eclipse box.
- **Cross-system integration** (RIS/EMR/analytics) using the client-credentials service identity to query ARIA over the gateway from a back-end with no scripting host.
- A reusable **`.auth` library**: factor the loopback-listener + OidcClient sign-in out as a NuGet-style helper shared by every internal tool that needs an ARIA bearer token.
