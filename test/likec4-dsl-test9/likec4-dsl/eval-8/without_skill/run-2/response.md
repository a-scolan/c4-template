You can define the reusable predicate group once in `global { predicateGroup ... }` and then reuse it in multiple views with the exact form `global predicate core-services`.

```c4
specification {
  element service
}

global {
  predicateGroup `core-services` {
    include kind == service
    include id ~= /^cloud\..*/
    exclude #deprecated
  }
}

model {
  cloud = softwareSystem "Cloud" {
    auth = service "Auth"
    billing = service "Billing"
    legacy = service "Legacy" #deprecated
    gateway = system "Gateway"
  }
}

views {
  view cloudCoreStyled of cloud {
    title "Core services styled"

    global predicate core-services

    style service {
      color green
      border solid
    }

    autoLayout lr
  }

  view cloudCoreWithExtraInclude of cloud {
    title "Core services plus extra include"

    global predicate core-services
    include cloud.gateway

    autoLayout lr
  }
}
```

What this does:

- `core-services` matches only `service` elements under `cloud.*`.
- `exclude #deprecated` removes deprecated services from that reusable set.
- `cloudCoreStyled` reuses the predicate and adds a per-view `style` rule.
- `cloudCoreWithExtraInclude` reuses the same predicate and adds one more explicit `include`.
