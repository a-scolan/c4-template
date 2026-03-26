Use **both**, with distinct responsibilities:

- **Deployment view** (mandatory for this request):
  - Model `SecZone` explicitly with bastion, firewall, and dedicated services
  - Keep infrastructure boundaries and network controls visible

- **C2 view** (recommended companion):
  - Show how security-facing application containers interact with core containers
  - Keep system-level responsibilities understandable to non-infra readers

Cleanest approach:
- Deployment view answers “where and how secured in production”
- C2 answers “what interacts with what at container level”

So the minimal complete documentation is: Deployment for `SecZone` + one focused C2 for container interactions.# Design View – Eval 3 – Without Skill – Run 3

## Task

Design a component-level (C3) view for a specific container, showing all its components and their relationships, with a layout that reflects logical grouping.

## Response

Component views zoom into a container to reveal its internal structure:

```likec4
views {
  view detail_myContainer of mySystem.myContainer {
    title 'MyContainer – Component Detail'
    description 'Shows the internal components of MyContainer'

    include mySystem.myContainer.*

    autoLayout LeftRight
  }
}
```

### Key patterns

1. **Minimal scope**: `include mySystem.myContainer.*` is usually sufficient — it brings in direct children only.
2. **Deep nesting**: If components themselves have sub-components, use `include mySystem.myContainer.**` (double glob) to include all descendants.

```likec4
views {
  view detail_myContainer of mySystem.myContainer {
    title 'MyContainer – Deep Components'

    include mySystem.myContainer.**   // all descendants recursively

    autoLayout TopBottom
  }
}
```

### Linking for navigation

To make this view reachable from the container view, add a `link` on the container element in the model:

```likec4
myContainer = Container_Api 'My Container' {
  link detail_myContainer
}
```

This enables click-through navigation in the rendered diagram.

### Style summary

Component nodes use `shape component` by default (from `spec-components.c4`). In-view style overrides let you colour specific components:

```likec4
style mySystem.myContainer.authService {
  color red  // highlight security-critical component
}
```
