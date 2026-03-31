A minimal LikeC4 deployment snippet with two **named** instances of `cloud.api` inside the same VM node looks like this:

```likec4
deploymentNode vm {
  instance apiPrimary of cloud.api
  instance apiSecondary of cloud.api
}
```

This creates two separate deployed instances, `apiPrimary` and `apiSecondary`, both inside the existing `vm` deployment node.