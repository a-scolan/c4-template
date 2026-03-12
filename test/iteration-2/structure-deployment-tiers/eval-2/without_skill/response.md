Keep the main production tiers easy to scan, and add the extra concerns as explicit complements instead of folding them into the core tier split.

Recommended layout for the primary site:

- `Dmz` — ingress, reverse proxy, WAF, public edge
- `AppTier` — application and business services
- `ProcTier` — add this only if you have async workers, queues, schedulers, or batch processors
- `DataTier` — databases, object storage, caches, backup targets
- `SecZone` or `AuditZone` — separate, cross-cutting security/audit area

How to place the audit/security capability:

- Model it as a distinct `SecZone` / `AuditZone`, not as a fuzzy replacement for `AppTier` or `DataTier`.
- Put SIEM, audit collectors, vulnerability scanners, secrets/security services, or privileged admin tooling there.
- Allow tightly controlled flows from the main tiers into that zone for logs, events, scans, or security controls.
- Avoid turning it into a catch-all bucket for random shared services.

How to place the disaster-recovery site:

- Model it as a separate environment, site, or clearly labeled standby deployment, not mixed into the primary production tiers.
- Mirror the same tier structure there when needed: `Dmz`, `AppTier`, optional `ProcTier`, `DataTier`.
- Show replication/failover links explicitly between primary and DR, especially `DataTier` replication and any configuration/queue recovery flows.
- Keep normal user traffic aimed at the primary `Dmz`; DR activation should be represented as a failover path, not steady-state production traffic.

A readable pattern is:

- Primary site: main tiers
- Cross-cutting security: explicit side zone
- DR site: second, clearly named environment with its own tier set

Leave exact VM names, `Node_App` nesting, and `instanceOf` mappings for the detailed deployment model so the tier diagram stays readable.