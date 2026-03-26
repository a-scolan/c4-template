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

Keep regular business traffic modeled in logical relationships and use deployment relationships for infrastructure-specific routing/security details.# Design View – Eval 1 – Without Skill – Run 2

## Task

Design a container (C2) view scoped to a single internal system, showing all its containers and their data-flow relationships.

## Response

For a container-level view in LikeC4:

```likec4
views {
  view mySystem_containers of mySystem {
    title 'MySystem – Container View'

    include mySystem, mySystem.*

    autoLayout LeftRight
  }
}
```

This creates a scoped view showing `mySystem` as the boundary and all its child containers inside it. LikeC4 automatically renders relationships between included elements.

### Scoping in practice

The `of <element>` clause:
- Sets the scope element for the view  
- Enables drill-down navigation from a parent context view
- The view title defaults to the element title if `title` is not set

### Showing external actors that interact with the system

```likec4
views {
  view mySystem_containers of mySystem {
    title 'MySystem – Containers with External Users'

    include mySystem.*
    include element.tag == #Actor -> mySystem.*
    include mySystem.* -> element.tag == #System_External

    autoLayout TopBottom
  }
}
```

This adds actors that call the system and external systems the containers call.

### Common mistakes to avoid

- Forgetting `include mySystem.*` (only including `mySystem` shows an empty boundary box)
- Including `*` instead of `mySystem.*` (pulls in unrelated elements)
