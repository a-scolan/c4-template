```likec4
deploymentNode vm {
  api1 = instanceOf cloud.api
  api2 = instanceOf cloud.api
}
```

This creates two separately named deployed instances of the same logical element, `cloud.api`, inside the existing `vm` deployment node.