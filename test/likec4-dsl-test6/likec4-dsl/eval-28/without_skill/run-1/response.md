Wrong: extend frontend -> api 'streams'
With both `frontend -> api 'streams'` and `frontend -[async]-> api 'streams'` present, omitting the kind is non-unique and can resolve to the wrong relationship, so the kind must be specified explicitly.
extend frontend -[async]-> api 'streams' { metadata { qos 'high' } }