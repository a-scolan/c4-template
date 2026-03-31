Wrong: extend frontend -> api 'streams'

Omitting the kind is wrong here because LikeC4 matches relationship identity by source and target, plus kind when a typed relationship exists, and title when needed for further disambiguation. Since `frontend -[async]-> api 'streams'` and `frontend -> api 'streams'` both already exist, leaving out `-[async]->` does not uniquely target the async relationship and can match the wrong one.

extend frontend -[async]-> api 'streams' { metadata { qos 'high' } }
