```likec4
global {
  predicateGroup core-services {
    include cloud.**
    include kind:service
    exclude #deprecated
  }
}

view core-services-styled {
  include global predicate core-services

  style {
    element "tag=core" {
      color green
    }
  }
}

view core-services-plus-extra {
  include global predicate core-services
  include cloud.gateway
}
```

Both views reuse the same `core-services` predicate group via the required form `global predicate core-services`.
- `core-services-styled` adds a per-view style rule.
- `core-services-plus-extra` adds an additional `include` on top of the shared predicate.
# Reusable Predicate Group: `core-services`

## Global predicate group definition

```likec4
global {
  predicateGroup core-services {
    include cloud.* where kind is service
    exclude #deprecated
  }
}
```

- `include cloud.* where kind is service` — selects all elements nested under `cloud` whose kind is `service`
- `exclude #deprecated` — removes any element tagged `#deprecated` from the set

---

## View 1 — applies the predicate group + a per-view style rule

```likec4
view coreServicesStyled {
  title "Core Services – styled"

  global predicate core-services

  style * {
    color green
    shape rectangle
  }
}
```

The `style *` block is a per-view override; it only affects this view and does not touch the global predicate group.

---

## View 2 — applies the predicate group + an extra `include` rule

```likec4
view coreServicesExtended {
  title "Core Services – extended"

  global predicate core-services

  include cloud.gateway
}
```

The additional `include cloud.gateway` brings in a specific element (e.g. an API gateway) that is not a `service` kind but is still relevant to this context, layered on top of what `core-services` already includes.

---

## How they fit together

| Aspect | View 1 | View 2 |
|---|---|---|
| Predicate applied | `global predicate core-services` | `global predicate core-services` |
| Extra rule | `style *` (per-view colour/shape) | `include cloud.gateway` (extra element) |
| Effect | Same element set, different visual rendering | Broader element set, default styling |

Both views reuse the same `predicateGroup` definition unchanged; each view then layers its own local rule on top without duplicating the include/exclude logic.
