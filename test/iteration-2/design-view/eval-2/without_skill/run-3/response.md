For an upload journey “step by step” with highlighted critical elements, combine two views:

1. **Dynamic view** for sequence clarity
   - Show the exact flow: user -> web app -> API -> queue/worker -> storage/database
   - Include key branches (success/failure/retry) only if they are essential

2. **Static view styling** for emphasis
   - Apply tags to critical elements (e.g., API, queue, worker, data store)
   - Use targeted styles/colors in the relevant static view to highlight those tagged elements
   - Keep non-critical nodes muted to preserve readability

This gives you clear temporal behavior (dynamic) plus durable visual emphasis (styled static view).# Design View – Eval 2 – Without Skill – Run 3

## Task

Design a filtered view that shows only cloud-hosted elements, using tag-based predicates to narrow the scope.

## Response

In LikeC4, views can be filtered using element predicate syntax. For cloud-hosted elements:

```likec4
views {
  view cloud_landscape {
    title 'Cloud-Hosted Components'

    include element.tag == #Cloud

    autoLayout TopBottom
  }
}
```

### Understanding `element.tag ==`

The `element.tag == #Cloud` predicate matches any element that carries the `#Cloud` tag. In this workspace's spec (`spec-global.c4`), `#Cloud` is defined with colour `rgb(14, 165, 233)`. All matched elements inherit this colour in the view unless overridden.

### Filtering by deployment environment

Similar to `#Cloud`, you can filter by environment:

```likec4
views {
  view prod_cloud {
    title 'Production Cloud Services'

    include element.tag == #Cloud and element.tag == #Production

    autoLayout LeftRight
  }
}
```

### Including relationships to non-cloud elements

If cloud elements communicate with on-premise systems, you can show those connections:

```likec4
views {
  view cloud_with_context {
    title 'Cloud Services with Dependencies'

    include element.tag == #Cloud
    include element.tag == #Cloud -> *    // what cloud elements call
    include * -> element.tag == #Cloud    // what calls into cloud elements

    autoLayout TopBottom
  }
}
```

This creates a richer view showing the integration context around cloud-hosted services.
