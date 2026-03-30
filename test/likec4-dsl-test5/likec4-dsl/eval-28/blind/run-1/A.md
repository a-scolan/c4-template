Wrong: extend frontend -> api 'streams'

That is wrong because there are two existing relationships with the same source, target, and title, and omitting the kind makes the extend target ambiguous; specifying `-[async]->` is required to bind metadata to the async edge.

extend frontend -[async]-> api 'streams' { metadata { qos 'high' } }
Wrong: extend frontend -> api 'streams'

When both `frontend -[async]-> api 'streams'` and `frontend -> api 'streams'` exist, there are two distinct relationships between the same source and target sharing the same title. Omitting the relationship kind in the `extend` expression makes the reference ambiguous — LikeC4 cannot determine which of the two relationships should receive the metadata, so the statement targets the wrong (untyped) relationship instead of the intended async one.

```likec4
extend frontend -[async]-> api 'streams' { metadata { qos 'high' } }
```
