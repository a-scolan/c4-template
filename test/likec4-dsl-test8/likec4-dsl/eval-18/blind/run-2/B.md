No.

In LikeC4, an `extend` must match an existing relationship by its full identity:

- source
- target
- title
- kind

So these are **two different relationships**:

- `frontend -[async]-> api 'streams'` → source=`frontend`, target=`api`, title=`streams`, kind=`async`
- `frontend -> api 'streams'` → source=`frontend`, target=`api`, title=`streams`, kind=`omitted/default`

Because `kind` is part of the identity, this:

`extend frontend -> api 'streams' { metadata { qos 'high' } }`

does **not** target the async relationship. It targets the relationship whose kind is also omitted/default — in your example, the plain `frontend -> api 'streams'` relationship.

So omitting the kind here is **wrong**, not merely ambiguous: it describes a different relationship identity than the async one.

The exact extension snippet that unambiguously targets the async relationship is:

`extend frontend -[async]-> api 'streams' { metadata { qos 'high' } }`
