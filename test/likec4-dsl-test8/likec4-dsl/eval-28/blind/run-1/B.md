Wrong: extend frontend -> api 'streams'
Because both an untyped and an `async` relationship exist between the same source and target with the same title, omitting the kind makes the matcher ambiguous and can target the wrong relationship; you must include the exact relationship kind to extend the intended one.

`extend frontend -[async]-> api 'streams' { metadata { qos 'high' } }`