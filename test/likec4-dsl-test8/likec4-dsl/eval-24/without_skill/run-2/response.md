Correct matcher: extend frontend -[async]-> api 'streams'

`extend frontend -> api 'streams'` is insufficient because it does not uniquely identify the relationship: both existing relationships have the same source (`frontend`), target (`api`), and title (`'streams'`). Without the relationship kind, the matcher is ambiguous.

`extend frontend -[sync]-> api 'streams'` targets the wrong relationship because it explicitly selects the `sync` relationship, while the one you want to extend is the `async` relationship.

Exact extension snippet:

```likec4
extend frontend -[async]-> api 'streams' {
}
```