```likec4
global {
  predicateGroup core-services {
    include cloud.* where kind == 'service' and !hasTag('#deprecated')
  }
}

view core-services-styled {
  global predicate core-services

  style {
    element kind == 'service' {
      color '#2E86DE'
      border solid
    }
  }
}

view core-services-plus-extra {
  global predicate core-services
  include cloud.shared.logging
}
```

Both views reuse the same global predicate group via `global predicate core-services`; the first adds a view-local style, and the second adds an extra include rule.
# Reusable Predicate Group: `core-services`

## 1. Global predicate group definition

```likec4
global {
  predicateGroup core-services {
    include cloud.* where kind == service
    exclude #deprecated
  }
}
```

- `include cloud.* where kind == service` — selects all elements nested under `cloud` whose kind is `service`.
- `exclude #deprecated` — removes from that set any element tagged `#deprecated`.

---

## 2. View A — applies `core-services` and adds a per-view style rule

```likec4
view cloud-services-styled {
  title "Cloud Core Services (styled)"

  global predicate core-services

  style element {
    color green
    shape rectangle
  }
}
```

The `style element { ... }` block is a **per-view** style that only affects this view; it is not part of the predicate group.

---

## 3. View B — applies `core-services` and adds an extra `include` rule

```likec4
view cloud-services-extended {
  title "Cloud Core Services (extended)"

  global predicate core-services

  include cloud.gateway
}
```

The extra `include cloud.gateway` adds the `cloud.gateway` element on top of whatever `core-services` already brings in, without modifying the global predicate group itself.

---

## Key points

| Concern | Approach |
|---|---|
| Reusable predicate mechanism | `global { predicateGroup ... }` |
| Applying in a view | `global predicate core-services` (exact keyword form) |
| Kind filter | `where kind == service` inside the predicate group |
| Exclusion by tag | `exclude #deprecated` inside the predicate group |
| Per-view style (View A) | `style element { ... }` after the global predicate line |
| Extra include (View B) | `include <element>` after the global predicate line |
