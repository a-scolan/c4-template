Add them as separate, explicit concerns instead of folding them into existing tiers.

- `SecZone`: place it as a sibling zone under the same production environment, alongside `Dmz`, `AppTier`, `ProcTier`, and `DataTier`. Use it for audit, security monitoring, SIEM/log aggregation, metrics, dashboards, and alerting. It stays internal-only.
- DR capability:
  - If you only need backup/replication tooling inside the primary environment, add an `InfraZone` as another sibling zone under `Production`.
  - If this is a true standby site or second region, model it as a separate environment such as `Dr` or `Standby`, with its own tier hierarchy, rather than hiding standby nodes inside primary `DataTier`.

This preserves readability because the main runtime flow still reads cleanly as `Dmz -> AppTier -> ProcTier -> DataTier`, while cross-cutting security/observability and DR remain visible but separate. Avoid mixing audit tools into `DataTier` or putting DR hosts into `Dmz`/`AppTier`.
