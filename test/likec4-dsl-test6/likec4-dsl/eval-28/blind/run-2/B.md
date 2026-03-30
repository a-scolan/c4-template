Wrong: extend frontend -> api 'streams'

Because both `frontend -[async]-> api 'streams'` and `frontend -> api 'streams'` already exist, omitting the kind does not identify a single relationship, so the matcher is not unique and you must include `-[async]->` to target the async edge explicitly.

extend frontend -[async]-> api 'streams' { metadata { qos 'high' } }