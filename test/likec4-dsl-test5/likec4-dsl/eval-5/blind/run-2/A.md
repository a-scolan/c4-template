```likec4
deploymentNode vm {
  instance apiA = cloud.api
  instance apiB = cloud.api
}
```

This creates two separately named instances of `cloud.api` in the same `vm` node.
# Two Named Instances of `cloud.api` in One VM Node

```likec4
deployment {
  vm {
    api_blue = instanceOf cloud.api
    api_green = instanceOf cloud.api
  }
}
```

Each instance gets its own identifier (`api_blue`, `api_green`), allowing them to be referenced independently in views and relationships while both residing inside the same `vm` deployment node.
