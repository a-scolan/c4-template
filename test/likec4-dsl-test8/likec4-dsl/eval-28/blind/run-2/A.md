Wrong: extend frontend -> api 'streams'

Omitting the kind is wrong because there are two distinct relationships between the same source, target, and title, and LikeC4 matches relationship identity by source + target + kind, adding title when needed; without `-[async]->`, this does not uniquely target the async relationship.

extend frontend -[async]-> api 'streams' { metadata { qos 'high' } }
