Wrong: extend frontend -> api 'streams'

Omitting the kind is wrong because there are already two different relationships with the same source, target, and title, so the kind is needed to disambiguate which one you are extending; otherwise the extension is ambiguous and can apply to the wrong relationship.

extend frontend -[async]-> api 'streams' { metadata { qos 'high' } }