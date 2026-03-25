A reusable predicate group is defined in the top-level `global { ... }` block using the `predicateGroup` keyword. The group name follows identifier rules (letters, digits, hyphens, underscores). It is consumed inside a view with `global predicate <name>`.

```likec4
global {
  predicateGroup core-services {
    include cloud.* where kind is service
    exclude * where tag is #deprecated
  }
}
```

**View 1 — applies the group, then adds a per-view `style` rule on top:**

```likec4
views {
  view core-services-overview {
    title "Core Services"
    global predicate core-services
    // per-view style rule applied on top of the predicate group result
    style * where kind is service { color primary; border dashed }
  }
}
```

**View 2 — applies the group, then adds an extra `include` rule:**

```likec4
views {
  view core-services-with-consumers {
    title "Core Services and Their Consumers"
    global predicate core-services
    // extra include: pull in any element that has a relationship to these services
    include -> cloud.* where kind is service
  }
}
```

**Key points:**
- `predicateGroup` lives in `global { ... }`, not in `views { ... }` or `model { ... }`.
- Inside the group, `include` and `exclude` follow the standard predicate + filter syntax (`where kind is …`, `where tag is …`).
- `exclude * where tag is #deprecated` removes from the accumulated result any already-included element bearing `#deprecated`; it runs after the `include`, so the ordering within the group matters.
- Inside a view, `global predicate core-services` is expanded in place, and subsequent rules (`style`, `include`, `exclude`) compose on top as normal — the style cascade is: spec defaults → element properties → local styles → global styles → view-level styles → customized predicates.
