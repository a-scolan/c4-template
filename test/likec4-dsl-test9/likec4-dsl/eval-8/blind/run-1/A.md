Here is one way to define the reusable predicate group and apply it in two different views using the exact mechanisms you requested.

```likec4
global {
  predicateGroup core-services {
    kind service
    id startsWith "cloud."
    not #deprecated
  }
}

view cloudCoreServicesStyled of cloud {
  global predicate core-services

  style {
    element {
      border solid
      color "#0f766e"
    }
  }
}

view cloudCoreServicesWithExtraInclude of cloud {
  global predicate core-services
  include cloud.shared.*
}
```

- `core-services` matches only `service` elements whose id is under `cloud.*`.
- `not #deprecated` excludes any element tagged `#deprecated`.
- `cloudCoreServicesStyled` applies the global predicate and then adds a per-view style rule.
- `cloudCoreServicesWithExtraInclude` applies the same global predicate and also adds an extra `include` rule.
