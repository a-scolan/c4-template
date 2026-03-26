For an upload journey “step by step” with highlighted critical elements, combine two views:

1. **Dynamic view** for sequence clarity
   - Show the exact flow: user -> web app -> API -> queue/worker -> storage/database
   - Include key branches (success/failure/retry) only if they are essential

2. **Static view styling** for emphasis
   - Apply tags to critical elements (e.g., API, queue, worker, data store)
   - Use targeted styles/colors in the relevant static view to highlight those tagged elements
   - Keep non-critical nodes muted to preserve readability

This gives you clear temporal behavior (dynamic) plus durable visual emphasis (styled static view).# Design View – Eval 2 – Without Skill – Run 2

## Task

Design a filtered view that shows only cloud-hosted elements, using tag-based predicates to narrow the scope.

## Response

Tag-based filtering in LikeC4 uses `element.tag == #TagName` inside `include`:

```likec4
views {
  view cloud_services {
    title 'Cloud Services'
    description 'Elements tagged #Cloud'

    include element.tag == #Cloud

    autoLayout LeftRight
  }
}
```

The `#Cloud` tag is defined in `spec-global.c4` with color `rgb(14, 165, 233)`.

### Multiple tag filters

To show both Cloud and SaaS elements:

```likec4
views {
  view external_services {
    title 'External Cloud & SaaS'

    include element.tag == #Cloud
    include element.tag == #Saas
    include element.tag == #External

    autoLayout TopBottom
  }
}
```

### Tag + kind combination

To show only cloud-hosted containers (not systems or actors):

```likec4
views {
  view cloud_containers {
    title 'Cloud Containers'

    include element.tag == #Cloud and element.tag == #Container

    autoLayout TopBottom
  }
}
```

The `and` operator allows combining predicates on the same line.

### Practical tips

- If no elements match the predicate, the view will render empty — verify tags are correctly applied in the model.
- Tag filtering works across all element kinds; scope further with kind predicates if needed.
- For deployment views that filter by environment, use `#Production` or `#Development` tags instead.
