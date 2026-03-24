```likec4
deployment {
  vm myVm {
    api1 = instanceOf cloud.api
    api2 = instanceOf cloud.api
  }
}
```

Two named instances (`api1`, `api2`) of the same logical element `cloud.api` are placed inside a single `vm` node. Named instance syntax (`IDENTIFIER = instanceOf ELEMENT`) is required when deploying the same element more than once in the same parent node; unnamed `instanceOf` would conflict.
