Keep the primary production tiers easy to scan, and add the extra concerns in a way that does not blur their purpose.

## Recommended structure

For the main production site, keep the core layout as:

- `Dmz`
- `AppTier`
- `ProcTier` *(if asynchronous processing exists)*
- `DataTier`

Then add the new concerns explicitly:

- `SecZone` or `AuditZone` for cross-cutting security, audit, secrets, policy, and compliance services
- a separate `DR Site` or `Standby Site` modeled as its own environment, with its own tier set

## How to place the audit/security zone

Treat the security or audit area as a complement to the main tiers, not as a replacement for them.

Use it for things like:

- audit trail collection
- security monitoring
- centralized policy enforcement
- secret management
- compliance exports or evidence collection

Do not move ordinary business services or databases into that zone just because they produce audit data. Keep those systems in their original tiers and show controlled flows into the security/audit area.

## How to place the disaster-recovery site

Do not fold the standby site into the same tier list as the primary site.

Instead, model it as a distinct environment, for example:

- `Primary Site`
  - `Dmz`
  - `AppTier`
  - `ProcTier`
  - `DataTier`
  - `SecZone`
- `DR Site`
  - `Dmz`
  - `AppTier`
  - `ProcTier`
  - `DataTier`

This keeps failover structure clear and avoids making the main production tiers unreadable.

## Network and readability guidance

- Keep Internet ingress only in the primary `Dmz` unless DR activation or testing explicitly requires otherwise.
- Keep `DataTier` private in both sites.
- Show replication or backup flows between the primary `DataTier` and the DR `DataTier` explicitly.
- Show security and audit collection flows into `SecZone` explicitly instead of scattering security components across every tier.
- Avoid mixing normal request paths with failover or replication paths in the same visual group.

## Scope boundary

This level should stop at tier roles, isolation, and allowed flows. Detailed VM names, node hierarchies, and `instanceOf` wiring should be added later in a separate infrastructure-modeling step.