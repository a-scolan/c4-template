Keep the primary tier stack intact and add the new concerns **beside** it, not **inside** it.

Recommended placement:

- Keep `Dmz`, `AppTier`, and `DataTier` as the main production readability spine.
- Add the cross-cutting audit/security capabilities as a **separate shared zone** at the same level as those tiers, for example `SecurityZone` or `SharedSecurity`, tagged with things like `#Security`, `#Monitoring`, or `#SharedInfra` as appropriate.
- Model the standby disaster-recovery site as a **second site/environment** sibling to primary production, not as a child inside one tier.

Why this stays readable:

1. **Audit/security is cross-cutting**. It should not be buried inside `Dmz` or `DataTier`, because it spans ingress, application, and data concerns.
2. **DR is geographic/topological**, not a functional tier. A standby site should sit as a peer to the primary site, usually with a simplified mirrored tier structure.

Practical modeling pattern:

- `PrimaryProd`
  - `Dmz`
  - `AppTier`
  - `DataTier`
  - `SharedSecurity`
- `StandbyDr`
  - `Dmz` (only if externally reachable during failover)
  - `AppTier`
  - `DataTier`

Relationship guidance:

- Let all primary tiers send logs/audit/security events to `SharedSecurity`.
- Let `DataTier` replicate to the standby site's `DataTier`.
- Keep failover/control links between primary and standby explicit and minimal.

If one diagram becomes crowded, split it into two views: one **primary tier view** and one **DR/failover view**. That preserves tier readability without flattening important operational concerns.