Use two named deployed instances inside the existing `vm` node, for example:

```likec4
deploymentNode vm {
  apiPrimary = instanceOf cloud.api
  apiSecondary = instanceOf cloud.api
}
```

Both `apiPrimary` and `apiSecondary` are separate named instances of the same logical element `cloud.api` within the same VM node.