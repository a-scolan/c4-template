Correct matcher: extend frontend -[async]-> api 'streams'

`extend frontend -> api 'streams'` is insufficient because LikeC4 matches a relationship by source + target + kind, and adds the title when needed for further disambiguation. Here, both existing relationships have the same source (`frontend`), target (`api`), and title (`'streams'`), but different kinds (`async` vs `sync`). Omitting the kind does not uniquely identify the async relationship, so it is the wrong matcher for a strict disambiguation case.

`extend frontend -[sync]-> api 'streams'` targets the wrong relationship because it explicitly selects the `sync` edge, while the relationship you want to extend is the `async` one.

```likec4
extend frontend -[async]-> api 'streams' {
  metadata { retries '3' }
}
```