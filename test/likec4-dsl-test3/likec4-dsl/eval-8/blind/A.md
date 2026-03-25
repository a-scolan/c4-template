```likec4
global {
  predicateGroup core-services {
    include cloud.* where kind is service
    exclude * where tag is #deprecated
  }
}

views {
  // View 1: applies the reusable predicate group + per-view styling
  view core-services-styled {
    global predicate core-services
    style * { color primary }
  }

  // View 2: applies the same group + an extra include rule
  view core-services-plus {
    global predicate core-services
    include cloud.*
  }
}
```

- `core-services` is defined in the `global { ... }` block as a reusable `predicateGroup`.
- Both views apply it via `global predicate core-services`.
- The first view adds a **per-view `style` rule**.
- The second view adds an **additional `include` rule** on top of the group.