Wrong: extend frontend -> api 'streams'

Omitting the relationship kind is wrong here because two different relationships already share the same source, target, and title, so `extend frontend -> api 'streams'` does not uniquely identify the async one and can match the untyped relationship instead. To extend the intended relationship exactly, the matcher must include the kind.

extend frontend -[async]-> api 'streams' { metadata { qos 'high' } }
