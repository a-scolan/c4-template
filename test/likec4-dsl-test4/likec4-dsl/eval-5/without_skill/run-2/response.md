In LikeC4, you can give each deployed instance an explicit name by prefixing the `instanceOf` declaration with an identifier. Here is a minimal snippet:

```likec4
deploymentNode vm {
  apiInstance1 = instanceOf cloud.api
  apiInstance2 = instanceOf cloud.api
}
```

- `apiInstance1` and `apiInstance2` are the distinct names for the two instances.
- Both reference the same logical element `cloud.api`.
- You can now address them independently in relationships or views using their fully-qualified deployment IDs (e.g. `vm.apiInstance1`, `vm.apiInstance2`).
