# Traceability Matrix

This matrix shows the traceability from the database tables to the API endpoints.

| DB Table | Model | Serializer | ViewSet | URL Example |
|---|---|---|---|---|
| `api_cloudprovider` | `CloudProvider` | `CloudProviderSerializer` | `CloudProviderViewSet` | `/api/cloudproviders/` |
| `api_account` | `Account` | `AccountSerializer` | `AccountViewSet` | `/api/accounts/` |
| `api_scan` | `Scan` | `ScanSerializer` | `ScanViewSet` | `/api/scans/` |
| `api_finding` | `Finding` | `FindingSerializer` | `FindingViewSet` | `/api/findings/` |
| `api_ruleset` | `RuleSet` | `RuleSetSerializer` | `RuleSetViewSet` | `/api/rulesets/` |
| `api_rule` | `Rule` | `RuleSerializer` | `RuleViewSet` | `/api/rules/` |
| `api_ruleexception` | `RuleException` | `RuleExceptionSerializer` | `RuleExceptionViewSet` | `/api/exceptions/` |

## Custom API Actions

| ViewSet | Action | URL Example | Description |
|---|---|---|---|
| `AccountViewSet` | `scan` | `/api/accounts/{id}/scan/` | Triggers a new scan for the account. |

## Gaps and Areas for Improvement

*   **Incomplete Port:** This matrix only covers the models created for the initial Django port. The original `ScoutSuite` application has a much richer data model, including concepts like rules, services, and detailed resource information. A full port of the application would require expanding the database schema and API to cover these concepts.
*   **Read-Only Endpoints:** Several of the endpoints are currently read-only (`CloudProvider`, `Scan`, `Finding`). In a full-featured application, there might be a need for write operations on some of these models (e.g., managing rules).
