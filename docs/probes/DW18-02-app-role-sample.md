# DW18-02 — AppRoleSample (secure ARIA SQL access via application role)

**Cluster 14 delta** — exemplar [DW18-01 VAIS](DW18-01-vais-aria-webservice.md).

- **Problem:** query the ARIA SQL database from an external app *without* embedding DB credentials —
  acquire a SQL **application role** instead, gated by an OAuth token.
- **Differs from the exemplar:** reuses DW18-01's bearer-token + Shared-Framework gateway
  (`GetSettingsRequest`/`Response`, `DataContractJsonSerializer`, `Authorization: Bearer`) but to
  fetch the **encrypted app-role password** (XPath into the `approles` settings, keyed by workstation
  id). It then **RSA-decrypts** it (`RSACryptoServiceProvider`, KeyContainer `"VarianClient"`, machine
  keystore) into a `SecureString`, opens an ODBC or ADO.NET pooled connection (DB host/port discovered
  from SF `DataSource` settings), runs **`sp_setapprole`** to elevate the connection, and finally
  `ExecuteScalar` queries (e.g. `ss_code_table`). A five-state workflow enum sequences it.
- **Surfaces it adds (auth/DB, not ESAPI):** `AppRoleHelper` over the SF gateway, RSA decrypt + `SecureString`, `sp_setapprole` (T-SQL), ADO.NET/ODBC pooled-connection DAL, SF `GetDataSource`.
- **Reuse note:** the **get-encrypted-approle-password → decrypt → `sp_setapprole` → query** chain is
  the reusable secure-DB-access template (DW18-01 reads settings; this one reaches the database). Port
  the gateway URIs, key container, and DSN to the target deployment. Verdict Adaptable.
