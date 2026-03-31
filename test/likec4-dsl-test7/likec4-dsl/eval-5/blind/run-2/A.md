```likec4
deployment {
  vm appVm {
    primary = instanceOf cloud.api
    secondary = instanceOf cloud.api
  }
}
```