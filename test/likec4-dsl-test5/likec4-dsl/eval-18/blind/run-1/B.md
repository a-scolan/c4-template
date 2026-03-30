No—you should not do that. Relationship identity matching is by source, target, title, and kind; with both `frontend -[async]-> api 'streams'` and `frontend -> api 'streams'` present, omitting kind is wrong here (not just ambiguous) because it can match the unkinded relationship instead of the async one.

```likec4
extend frontend -[async]-> api 'streams' {
  metadata { qos 'high' }
}
```
