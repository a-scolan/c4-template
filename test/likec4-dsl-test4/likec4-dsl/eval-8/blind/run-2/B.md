# Reusable Predicate Group `core-services`

Below is a complete example demonstrating the `global { predicateGroup ... }` mechanism and its use with `global predicate core-services` in two distinct views.

## Global predicate group definition

```likec4
global {
  predicateGroup core-services {
    include cloud.* where kind == service and not #deprecated
  }
}
```

This predicate group selects all elements whose FQN matches `cloud.*`, restricts to those of kind `service`, and excludes any element tagged `#deprecated`.

## View 1 — applies the global predicate and adds a per-view style rule

```likec4
view cloud_services_styled {
  title "Cloud Core Services (styled)"

  global predicate core-services

  style cloud.* where kind == service {
    color amber
    shape roundedBox
  }
}
```

Here `global predicate core-services` first brings in every non-deprecated `service` from `cloud.*`. The `style` rule then overrides the visual appearance of those elements directly inside this view, without affecting any other view.

## View 2 — applies the global predicate and adds an extra `include` rule

```likec4
view cloud_services_extended {
  title "Cloud Core Services (with gateway)"

  global predicate core-services

  include cloud.apiGateway
}
```

Here `global predicate core-services` still controls the base set of services. The additional `include cloud.apiGateway` line pulls in one more specific element (e.g. an API gateway that is not of kind `service`) exclusively for this view.

## Key points

| Concept | Syntax |
|---|---|
| Declare a reusable predicate group | `global { predicateGroup <name> { ... } }` |
| Apply it inside a view | `global predicate <name>` |
| Filter by kind | `where kind == service` |
| Exclude a tag | `and not #deprecated` |
| Per-view style override | `style <selector> { ... }` inside the view |
| Per-view extra include | `include <element>` inside the view |

The two views share the same underlying selection logic (`core-services`) while each customises the diagram independently.
