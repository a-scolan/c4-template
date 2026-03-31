Here is a concise example using the exact reusable-predicate mechanism you requested:

```likec4
global {
  predicateGroup core-services {
    kind == service
    id ~= 'cloud.*'
    !#deprecated
  }
}

view coreServicesStyled of cloud {
  title 'Core services with a per-view style'

  global predicate core-services

  style * {
    borderColor '#3B82F6'
    backgroundColor '#EFF6FF'
  }
}

view coreServicesWithExtraInclude of cloud {
  title 'Core services plus an extra include'

  global predicate core-services
  include cloud.gateway
}
```

- `core-services` matches `service` elements under `cloud.*` and excludes anything tagged `#deprecated`.
- Both views reuse it with the exact form `global predicate core-services`.
- The first view adds a per-view `style` rule.
- The second view adds an extra `include` rule.