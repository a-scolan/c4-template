Correct matcher: extend frontend -[async]-> api 'streams'

`extend frontend -> api 'streams'` is insufficient because source, target, and title are not enough to uniquely identify the relationship here: both an `async` and a `sync` relationship already exist between `frontend` and `api` with the same title `'streams'`. When typed relationships exist for the same source/target pair, the kind must be part of the matcher.

`extend frontend -[sync]-> api 'streams'` targets the wrong relationship because it matches the separate `sync` edge, not the existing `async` edge you want to extend.

```likec4
extend frontend -[async]-> api 'streams' {
}
```