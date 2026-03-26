Use a deployment-focused view with explicit tier boundaries and deployed instances.

LikeC4 approach aligned with workspace conventions:

- Environment: `Production`
- Zones:
  - `Dmz` (internet edge, gateway/reverse proxy)
  - `AppTier` (application services)
  - `DataTier` (database/storage)
- Nodes:
  - DMZ VM(s): gateway/web entry
  - App VM(s): API/app services (`instanceOf` logical containers)
  - Data VM(s): database/storage (`instanceOf` logical containers)
- Deployment relationships:
  - Internet/DMZ ingress (HTTPS)
  - DMZ -> AppTier (internal app protocol)
  - AppTier -> DataTier (DB/storage protocol)

Keep regular business traffic modeled in logical relationships and use deployment relationships for infrastructure-specific routing/security details.# Design View – Eval 1 – Without Skill – Run 3

## Task

Design a container (C2) view scoped to a single internal system, showing all its containers and their data-flow relationships.

## Response

Container views in LikeC4 are scoped with `of <system>`:

```likec4
views {
  view containers_mySystem of mySystem {
    title 'MySystem – Container Detail'
    description 'Shows all application containers within MySystem'

    include mySystem.*

    autoLayout LeftRight
  }
}
```

### What gets rendered

- Each child of `mySystem` (containers, databases, queues) appears as a node.
- All relationships between those children are rendered as edges automatically.
- No explicit relationship include is needed unless cross-boundary flows must be shown.

### Expanding to cross-boundary flows

```likec4
views {
  view containers_mySystem of mySystem {
    title 'MySystem – Full Data Flows'

    include mySystem.*

    // Show what calls the API container from outside
    include * -> mySystem.api

    // Show what the queue consumers write to
    include mySystem.consumer -> *

    autoLayout LeftRight
  }
}
```

### Applying layout hints

For systems with many containers, LikeC4 supports `autoLayout` directions:
- `LeftRight` — good for request/response chains
- `TopBottom` — good for layered architectures (frontend → backend → db)
