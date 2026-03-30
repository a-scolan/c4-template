Use two **named deployment instances** inside the same `vm` node:

```likec4
deployment {
  node vm {
    apiA = instanceOf cloud.api
    apiB = instanceOf cloud.api
  }
}
```

This creates two separate instances (`apiA`, `apiB`) of `cloud.api` in one VM node.
# Two Named Instances of `cloud.api` in One VM Node

Assign an identifier to each instance by prefixing `instanceOf` with a name:

```c4
deployment {
  vm {
    api_blue = instanceOf cloud.api
    api_green = instanceOf cloud.api
  }
}
```

`api_blue` and `api_green` are distinct named deployment instances of the same logical element (`cloud.api`) hosted inside the single `vm` deployment node. They can each be referenced independently in views and relationships.
