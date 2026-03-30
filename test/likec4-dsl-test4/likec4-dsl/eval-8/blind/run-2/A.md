# Global Predicate Group `core-services`

## Definition

Define the reusable predicate group in a `global { ... }` block (any `.c4` file in the project):

```likec4
global {
  predicateGroup core-services {
    include cloud.* where kind is service
    exclude * where tag is #deprecated
  }
}
```

- `include cloud.* where kind is service` — selects direct children of `cloud` whose kind is `service`.
- `exclude * where tag is #deprecated` — removes any element tagged `#deprecated` from the accumulated result.

## Applying in Views

Use exactly `global predicate core-services` inside each view to apply the group.

### View 1 — applies `core-services` then adds a per-view style rule

```likec4
views {
  view services-overview of cloud {
    title "Core Services"
    global predicate core-services
    style cloud.* { color primary }
  }
}
```

The `style` rule is a per-view addition on top of the predicate group result; it does not belong to the group itself.

### View 2 — applies `core-services` then adds an extra `include` rule

```likec4
views {
  view services-with-gateway of cloud {
    title "Core Services + Gateway"
    global predicate core-services
    include cloud.gateway
  }
}
```

The extra `include cloud.gateway` adds that element to whatever `core-services` already resolved in this view.

## Key Points

| Concern | Answer |
|---------|--------|
| Block that hosts the group | `global { predicateGroup core-services { ... } }` |
| Per-view application keyword | `global predicate core-services` (not `global style`) |
| Identifier format | `core-services` — hyphens are valid in LikeC4 identifiers |
| Predicate evaluation order | Rules inside the group execute top-to-bottom; `exclude` only removes what was already included |
| Composability | Each view can add its own `include`, `exclude`, or `style` rules after `global predicate` |
