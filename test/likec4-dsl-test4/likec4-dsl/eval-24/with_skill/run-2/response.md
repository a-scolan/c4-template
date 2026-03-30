Correct matcher: extend frontend -[async]-> api 'streams'

## Why `extend frontend -> api 'streams'` is insufficient

When you omit the relationship kind, LikeC4 matches on source, target, and title only. Both `frontend -[async]-> api 'streams'` and `frontend -[sync]-> api 'streams'` share the same source (`frontend`), target (`api`), and title (`'streams'`). Without the kind to disambiguate, the extension is ambiguous — it does not uniquely identify which of the two relationships should receive the additional metadata.

## Why `extend frontend -[sync]-> api 'streams'` targets the wrong relationship

This form does include the kind, which makes it unambiguous, but it specifies kind `sync`. That matches the synchronous relationship, not the asynchronous one. The relationship you want to extend is `frontend -[async]-> api 'streams'`, so using `sync` extends the wrong relationship and leaves the `async` one untouched.

## Exact extension snippet

```likec4
extend frontend -[async]-> api 'streams' {
  metadata {
    qos 'high'
  }
}
```
