## Global Predicate Group `core-services`

### Definition

```likec4
global {
  predicateGroup core-services {
    include cloud.* where kind is service
    exclude * where tag is #deprecated
  }
}
```

- `include cloud.* where kind is service` — selects direct children of `cloud` whose kind is `service`.
- `exclude * where tag is #deprecated` — removes any previously included element tagged `#deprecated`.

---

### View 1 — applies `core-services` + per-view style rule

```likec4
views {
  view core-overview {
    title "Core Services"

    global predicate core-services

    style * { color primary }
  }
}
```

The `style` rule is local to this view and overrides colours for every element the predicate group brought in.

---

### View 2 — applies `core-services` + extra `include` rule

```likec4
views {
  view core-with-gateway {
    title "Core Services + Gateway"

    global predicate core-services

    include cloud.gateway
  }
}
```

The extra `include cloud.gateway` adds the gateway element (and its relationships to the already-included elements) on top of what the predicate group selected.
