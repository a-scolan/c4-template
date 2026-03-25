```likec4
global {
  predicateGroup core-services {
    include cloud.* where kind is service
    exclude * where tag is #deprecated
  }
}

views {
  view core-services-styled {
    global predicate core-services
    style * { color primary }
  }

  view core-services-with-neighbors {
    global predicate core-services
    include cloud.* -> * where source.kind is service and source.tag is not #deprecated
  }
}
```

- `core-services` is defined once in the `global { ... }` block as a reusable `predicateGroup`.
- Both views apply it with `global predicate core-services`.
- `core-services-styled` adds a **per-view style rule** (`style * { ... }`).
- `core-services-with-neighbors` adds an **extra include rule** on top of the group (`include cloud.* -> * ...`).