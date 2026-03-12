Keep the main production tiers readable by treating the cross-cutting pieces as **explicit complements**, not replacements for the core layout.

## Primary production layout

Keep the core deployment centered on:

- **Dmz** — edge entry points
- **AppTier** — synchronous business services
- **DataTier** — persistent stores
- **ProcTier** — add this explicitly if you run queues/workers or other async processing

That preserves the main story of the production path.

## Audit / security zone

Add a separate **SecZone** beside the main tier stack.

Use it for:

- audit log collection
- SIEM / security analytics
- metrics and alerting
- centralized monitoring dashboards

Why this helps:

- it keeps security/observability visible
- it avoids overloading AppTier or DataTier with unrelated responsibilities
- it stays readable because it is clearly labeled as a supporting zone, not a fuzzy fifth application tier

## Standby disaster-recovery site

Model DR as a **separate environment** or a clearly distinct DR tier set, for example:

- `Prod` — primary site
- `ProdDr` or `DisasterRecovery` — standby site

Do **not** fold the standby site into the same tier stack as the primary environment. A separate environment makes replication, failover, and reduced-capacity standby behavior much easier to understand.

Typical DR structure:

- minimal mirrored **DataTier** for replicated storage/database
- optional reduced **AppTier** / **ProcTier** if warm standby is required
- explicit replication and failover relationships from primary to DR

## Readability rule of thumb

- keep the main tiers focused on request flow and data flow
- keep **SecZone** clearly complementary
- keep **DR** clearly separate as another environment/site

For exact VM names, `Node_App` structure, Markdown spec tables, and `instanceOf` wiring, hand off to **`model-deployment-infrastructure`**.