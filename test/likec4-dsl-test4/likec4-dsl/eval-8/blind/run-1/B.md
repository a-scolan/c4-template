# LikeC4 DSL – Reusable Predicate Group Example

Below is a complete example showing how to define a reusable predicate group called `core-services` in a `global` block, and then apply it in two different views using `global predicate core-services`.

---

## Global predicate group definition

```likec4
global {
  predicateGroup core-services {
    include cloud.*, where kind == service and not #deprecated
  }
}
```

**Explanation:**
- `global { predicateGroup <name> { ... } }` declares a reusable predicate group.
- `include cloud.*, where kind == service` selects all elements under the `cloud` namespace whose kind is `service`.
- `and not #deprecated` excludes any element tagged `#deprecated`.

---

## View 1 – applies the predicate group and adds a per-view style rule

```likec4
view cloud_services_styled {
  title "Cloud Services (styled)"

  global predicate core-services

  style cloud.*, where kind == service {
    color green
    shape rectangle
  }
}
```

**What this does:**
- `global predicate core-services` pulls in the shared include/exclude rules.
- The `style` rule inside the view overrides the visual appearance of matched `service` elements with a green rectangle — this is local to this view only.

---

## View 2 – applies the predicate group and adds an extra `include` rule

```likec4
view cloud_services_extended {
  title "Cloud Services (extended)"

  global predicate core-services

  include cloud.gateway
}
```

**What this does:**
- `global predicate core-services` again brings in all non-deprecated `service`-kind elements from `cloud.*`.
- The additional `include cloud.gateway` adds a specific element (`cloud.gateway`) that may not match the predicate (e.g., it could be a different kind or an entry-point component), extending the view beyond what the predicate alone would include.

---

## Summary

| Mechanism | Syntax |
|---|---|
| Declare reusable predicate group | `global { predicateGroup <name> { include ..., where ... } }` |
| Apply in a view | `global predicate <name>` |
| Add per-view styling on top | `style ..., where ... { ... }` inside the view |
| Add extra elements on top | `include <element>` inside the view |

The `global predicate <name>` keyword form is the exact mechanism for applying a pre-declared `predicateGroup` inside any view, and multiple rules can be combined with it freely.
