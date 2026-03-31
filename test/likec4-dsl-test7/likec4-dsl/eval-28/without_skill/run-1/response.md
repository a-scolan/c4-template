Wrong: extend frontend -> api 'streams'
Omitting the relationship kind is wrong because there are two existing `frontend` → `api` relationships with the same title `'streams'` but different kinds (`async` and default), so leaving the kind out makes the target ambiguous and may extend the wrong relationship.
extend frontend -[async]-> api 'streams' { metadata { qos 'high' } }