Correct matcher: extend frontend -[async]-> api 'streams'

`extend frontend -> api 'streams'` is insufficient because it does not uniquely identify the relationship when more than one relationship already exists between the same source and target with the same title. In this case, both an `async` and a `sync` relationship from `frontend` to `api` are named `'streams'`, so omitting the relationship kind leaves the matcher ambiguous.

`extend frontend -[sync]-> api 'streams'` targets the wrong relationship because it explicitly matches the `sync` relationship, while the relationship you want to extend is the existing `async` one.

Exact extension snippet:

```likec4
extend frontend -[async]-> api 'streams' {
  // extension content here
}
```