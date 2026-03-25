`extend` on relationships matches an **existing** relationship; it does not create a new one.

For relationship matching, LikeC4 uses the same identifying parts as the relationship declaration:
- source (`frontend`)
- target (`api`)
- and, when needed to disambiguate, relationship kind and title/label

So with an existing relationship:
`frontend -[async]-> api 'streams'`

you should extend it with the same signature (especially when there could be multiple `frontend -> api` relationships):

`extend frontend -[async]-> api 'streams' {
  metadata {
    qos 'high'
  }
}`

Using `extend frontend -> api 'streams' { ... }` may be ambiguous if multiple relationships exist between the same endpoints; include `-[async]->` for a precise match.