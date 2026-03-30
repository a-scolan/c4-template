```likec4
deploymentNode vm {
  instanceOf cloud.api {
    title 'API Instance 1'
  }
  api2 = instanceOf cloud.api {
    title 'API Instance 2'
  }
}
```

Wait — LikeC4 uses named deployed instances like this:

```likec4
deploymentNode vm {
  api1 = instanceOf cloud.api
  api2 = instanceOf cloud.api
}
```

Each named identifier (`api1`, `api2`) creates a distinct deployed instance of `cloud.api` inside the same `vm` node. The names (`api1`, `api2`) are unique within the deployment scope and serve as the FQN leaf for each instance.
