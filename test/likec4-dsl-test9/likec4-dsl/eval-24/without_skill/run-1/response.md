Correct matcher: extend frontend -[async]-> api 'streams'

`extend frontend -> api 'streams'` is insufficient because it matches only the source, target, and title. In this case, there are already two relationships with the same endpoints and the same title, so that matcher does not uniquely identify which one to extend.

`extend frontend -[sync]-> api 'streams'` targets the wrong relationship because it explicitly matches the `sync` relationship, while the relationship that must be extended is the `async` one.

Exact extension snippet:

```likec4
extend frontend -[async]-> api 'streams' {
}
```