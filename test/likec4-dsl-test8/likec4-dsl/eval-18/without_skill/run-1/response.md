No — `extend frontend -> api 'streams' { ... }` is **wrong here**, not merely “a bit vague”.

Relationship identity matching is based on the combination of:
- source
- target
- title
- kind

In your example, both of these already exist:
- `frontend -[async]-> api 'streams'`
- `frontend -> api 'streams'`

They have the same:
- source: `frontend`
- target: `api`
- title: `'streams'`

But they differ in **kind**:
- one is `async`
- one uses the default/direct relationship kind

So if you write:

`extend frontend -> api 'streams' { metadata { qos 'high' } }`

that omits the kind and therefore does **not** uniquely identify which existing relationship you mean. Because relationship identity includes **kind**, leaving it out is ambiguous in this situation, and thus the extension is wrong for targeting the async relationship specifically.

Use the kind explicitly so the match is unambiguous:

`extend frontend -[async]-> api 'streams' { metadata { qos 'high' } }`
