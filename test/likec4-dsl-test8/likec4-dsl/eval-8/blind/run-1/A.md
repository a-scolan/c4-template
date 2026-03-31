You can define the reusable predicate group in `global { predicateGroup ... }` and then apply it in each view with the exact form `global predicate core-services`.

```likec4
model {
  cloud = system 'Cloud Platform' {
    api = service 'API'
    billing = service 'Billing' #deprecated
    auth = service 'Auth'
    web = frontend 'Web UI'
  }
}

global {
  predicateGroup core-services = kind(service) and element.id.startsWith('cloud.') and not tag(#deprecated)
}

views {
  view coreServicesStyled of cloud {
    global predicate core-services

    style {
      element "*" {
        color green
        border solid
      }
    }
  }

  view coreServicesExtended of cloud {
    global predicate core-services
    include cloud.web
  }
}
```

In this example:

- `core-services` matches all `service` elements under `cloud.*`
- `not tag(#deprecated)` excludes deprecated services
- `coreServicesStyled` applies the shared predicate and adds a per-view `style` rule
- `coreServicesExtended` applies the same shared predicate and adds an extra `include` rule

That gives you two different views reusing the same predicate group with the exact mechanism and keyword form you requested.
