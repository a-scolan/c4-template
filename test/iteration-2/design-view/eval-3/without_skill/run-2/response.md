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

So the minimal complete documentation is: Deployment for `SecZone` + one focused C2 for container interactions.# Design View – Eval 3 – Without Skill – Run 2

## Task

Design a component-level (C3) view for a specific container, showing all its components and their relationships, with a layout that reflects logical grouping.

## Response

For a C3 (component) view in LikeC4:

```likec4
views {
  view myContainer_components of mySystem.myContainer {
    title 'MyContainer – Component View'

    include mySystem.myContainer.*

    autoLayout TopBottom
  }
}
```

This includes all components inside `myContainer` and renders their relationships.

### Setting the view scope

The `of <element>` declaration:
- Associates the view with a model element for navigation
- Allows the LikeC4 engine to generate breadcrumb paths (e.g., landscape → system → container → component)
- Makes the view accessible via `link` navigation from parent views

### Adding styling to differentiate component roles

```likec4
views {
  view myContainer_components of mySystem.myContainer {
    title 'MyContainer – Components with Roles'

    include mySystem.myContainer.*

    style mySystem.myContainer.controller {
      color blue
    }

    style mySystem.myContainer.validator {
      color green
    }

    style mySystem.myContainer.repository {
      color amber
    }

    autoLayout LeftRight
  }
}
```

Using in-view `style` blocks to colour elements by their role makes the diagram easier to read.

### Layout consideration

- `TopBottom`: best when components form a processing pipeline
- `LeftRight`: best for request-handling chains (controller → service → repository)
