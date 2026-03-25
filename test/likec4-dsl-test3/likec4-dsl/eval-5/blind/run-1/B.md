```likec4
deployment {
  appVm = vm {
    apiA = instanceOf cloud.api
    apiB = instanceOf cloud.api
  }
}
```

This creates one VM node with two **named** deployed instances of the same logical element (`cloud.api`).