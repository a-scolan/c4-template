```likec4
deployment {
  deploymentNode vm {
    instance apiA of cloud.api
    instance apiB of cloud.api
  }
}
```

This creates two separately named instances (`apiA`, `apiB`) of the same logical element `cloud.api` inside a single VM node.