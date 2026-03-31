Wrong: extend frontend -> api 'streams'

Omitting the kind is wrong because two relationships here share the same source, target, and title, so `extend frontend -> api 'streams'` can match the untyped relationship instead of the async one; when typed relationships exist, the matcher must include the kind to identify the intended relationship exactly.

extend frontend -[async]-> api 'streams' { metadata { qos 'high' } }
