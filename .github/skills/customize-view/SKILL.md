---
name: customize-view
description: Advanced view features: styling (colors, shapes, style predicates), layout control (autoLayout, rank hints), and navigation (navigateTo, links).
---

# Customize View

Use this skill for advanced view features: styling, layout, and navigation.

## Visual Styling

### View-Level Style Overrides

```likec4
view myView {
  include cloud.backend with {
    title 'Backend Services'
    color primary
    shape browser
    icon tech:java
  }
}
```

### Style Predicates

```likec4
view apiView {
  include *
  
  style * { color muted; opacity 10% }
  style api.*, gateway.* { color primary; opacity 100% }
  style element.tag = #deprecated { color muted }
  style element.tag != #production { color secondary }
}
```

### Global Style Groups

```likec4
global {
  styleGroup theme_production {
    style * { color primary }
    style element.tag = #external { color muted }
  }
}

views {
  global style theme_production
  
  view myView {
    include *
  }
}
```

**Style Properties:**  
Elements: color, shape, icon, opacity, border, size, textSize, multiple  
Colors: primary, secondary, muted, amber, gray, green, indigo, red  
Shapes: rectangle, storage, cylinder, browser, mobile, person, queue, bucket, document  
Icons: tech:*, aws:*, gcp:*, azure:*

## Layout Control

### Auto-Layout Direction

```likec4
view layered {
  include *
  autoLayout TopBottom  // or LeftRight
}
```

### Rank Hints

```likec4
view requestFlow {
  include *
  
  include client with { rank source }           // Entry point
  include service1, service2 with { rank same } // Parallel
  include database with { rank sink }           // Endpoint
  
  autoLayout TopBottom
}
```

### Directed Includes

```likec4
view dataFlow {
  include frontend, backend, database
  include frontend -> backend ->  // Direction hints
  include -> database
  
  autoLayout LeftRight
}
```

### Common Layout Patterns

**Layered (TopBottom):**
```likec4
view layered {
  include *
  include presentation.* with { rank source }
  include data.* with { rank sink }
  autoLayout TopBottom
}
```

**Request Flow (LeftRight):**
```likec4
view flow {
  include *
  include client with { rank source }
  include external.* with { rank sink }
  autoLayout LeftRight
}
```

**Load Balanced:**
```likec4
view balanced {
  include *
  include loadBalancer with { rank source }
  include backend1, backend2, backend3 with { rank same }
  include database with { rank sink }
  autoLayout TopBottom
}
```

### Layout Troubleshooting

- **Overlapping elements:** Add rank hints to separate layers
- **Wrong flow direction:** Use directed includes or change autoLayout
- **Elements spread out:** Group related elements with `rank same`

## Navigation

### View-to-View Navigation

```likec4
view systemOverview {
  include *
  
  include cloud.backend with {
    navigateTo backendDetails
  }
}

view backendDetails of cloud.backend {
  include *
}
```

### Navigation Patterns

**Drill-down:** Context → Container → Component (navigateTo on parent elements)
```likec4
view contextView {
  include *
  include cloud with { navigateTo cloudContainers }
}

view cloudContainers of cloud {
  include *
  include cloud.backend with { navigateTo backendComponents }
}
```

**Hub-spoke:** Central index with links to specialized views
```likec4
view index {
  title "Architecture Index"
  include *
  include cloud.api with { navigateTo apiServices }
  include cloud.storage with { navigateTo dataArchitecture }
}
```

### External Documentation Links

```likec4
view epic12 {
  title "System Changes - Epic 12"
  
  description """
    Implementation details.
    See linked resources.
  """
  
  link https://my.jira/epic/12 'Epic-12'
  link https://docs.internal/spec 'Specification'
  
  include *
}
```

### View Metadata

```likec4
view myView {
  title "Clear, Descriptive Title"
  
  description """
    This view shows:
    - **Component A**: Handles requests
    - **Component B**: Processes data
    
    See [deployment guide](https://docs.internal/deploy).
  """
  
  #production, #deployment
  
  include *
}
```

## Validation

- [ ] Style predicates use `element.tag = #name` syntax
- [ ] AutoLayout direction matches flow (TopBottom for layers, LeftRight for sequences)
- [ ] Source rank = entry points, Sink rank = endpoints
- [ ] No conflicting rank hints (can't be both source and sink)
- [ ] Navigation targets reference valid view IDs
- [ ] External links use HTTPS with descriptive text
- [ ] View titles unique and descriptive

**MCP:** Use `open-view` to preview layout and navigation interactively

**Context7:** Query `/likec4/likec4` for syntax validation if uncertain

## Output

Polished views with appropriate styling, logical layout, and clear navigation paths.
