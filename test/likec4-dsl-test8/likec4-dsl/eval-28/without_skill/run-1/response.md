Wrong: extend frontend -> api 'streams'

Omitting the kind is wrong because both a default relationship and an `async` relationship already exist between the same source, target, and title, so `extend frontend -> api 'streams'` is ambiguous and targets the wrong edge instead of the specific async one you want to modify.

extend frontend -[async]-> api 'streams' { metadata { qos 'high' } }