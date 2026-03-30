No. Relationship identity matching is based on source, target, title, and kind, and here both existing relationships share the same source, target, and title but differ by kind. Omitting the kind is wrong here, not just ambiguous, because it can match the unkinded `frontend -> api 'streams'` relationship instead of the async one.

```likec4
extend frontend -[async]-> api 'streams' {
  metadata { qos 'high' }
}
```