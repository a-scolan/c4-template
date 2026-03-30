```likec4
global {
  predicateGroup core-services =
    kind is service and
    id startsWith 'cloud.' and
    not tag is #deprecated
}

views {
  view cloud-services-styled of cloud {
    global predicate core-services

    style * {
      color '#2F80ED'
      border solid
    }
  }

  view cloud-services-plus-db of cloud {
    global predicate core-services
    include cloud.db
  }
}
```

This uses the exact reusable predicate mechanism via `global { predicateGroup ... }` and applies it in both views with the exact keyword form `global predicate core-services`.