No — that extension is not correct for targeting the async relationship.

Relationship identity matching is based on **source + target + title + kind**. Here you have two different relationships with the same source (`frontend`), target (`api`), and title (`'streams'`), but different kinds:
- `frontend -[async]-> api 'streams'` (kind = `async`)
- `frontend -> api 'streams'` (kind = default/unspecified kind)

So if you write:

`extend frontend -> api 'streams' { ... }`

you are omitting the kind, which is **ambiguous/wrong in this case** because kind is required to uniquely identify the intended relationship among duplicates that share source, target, and title.

Use this exact unambiguous extension:

`extend frontend -[async]-> api 'streams' { metadata { qos 'high' } }`
