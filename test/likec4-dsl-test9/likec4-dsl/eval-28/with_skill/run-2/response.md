Wrong: extend frontend -> api 'streams'

Omitting the kind is wrong because both a plain and an `async` relationship already exist between the same source, target, and title, so `extend` must match the exact relationship identity; otherwise it selects the untyped relationship instead of the async one.

extend frontend -[async]-> api 'streams' { metadata { qos 'high' } }
