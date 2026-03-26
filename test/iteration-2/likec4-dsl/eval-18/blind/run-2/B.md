`extend` on relationships must match the existing relationship identity (source, target, and relationship signature—including explicit kind/title when present).

Given `frontend -[async]-> api 'streams'`, the correct extension is:

```likec4
model {
  extend frontend -[async]-> api 'streams' {
    metadata {
      qos 'high'
    }
  }
}
```

So `extend frontend -> api 'streams'` is too weak/mismatched because it omits the explicit `async` kind used by the original relation.