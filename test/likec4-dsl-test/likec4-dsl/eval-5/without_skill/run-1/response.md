```likec4
deployment {
  deploymentNode vm {
    instanceOf cloud.api as api1 'API – Primary'
    instanceOf cloud.api as api2 'API – Secondary'
  }
}
```

- `deploymentNode vm` references the already-declared node (the keyword echoes its existing kind/name; omit the body-level re-declaration of the node itself if it was already given a title elsewhere).
- `instanceOf cloud.api as api1` / `as api2` creates two distinct named deployed instances of the same logical element `cloud.api` inside that single VM node.
- The `as <identifier>` alias is required when the same element is instantiated more than once in the same scope, so each instance has a unique handle for relationship declarations.
