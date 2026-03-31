Wrong: extend frontend -> api 'streams'

Omitting the kind is wrong here because there are already two distinct relationships with the same source, target, and title, so `extend frontend -> api 'streams'` is ambiguous and could match the sync relationship instead of the async one. You must include the relationship kind to target the intended existing relationship unambiguously.

extend frontend -[async]-> api 'streams' { metadata { qos 'high' } }