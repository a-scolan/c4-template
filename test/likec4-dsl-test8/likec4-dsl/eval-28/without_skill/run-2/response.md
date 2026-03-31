Wrong: extend frontend -> api 'streams'

When both `frontend -> api 'streams'` and `frontend -[async]-> api 'streams'` already exist, omitting the kind is ambiguous because it targets the plain relationship instead of the specific `async` one, so you would extend the wrong edge.

extend frontend -[async]-> api 'streams' { metadata { qos 'high' } }
