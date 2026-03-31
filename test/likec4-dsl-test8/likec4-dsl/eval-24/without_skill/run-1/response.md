Correct matcher: extend frontend -[async]-> api 'streams'

`extend frontend -> api 'streams'` is insufficient because it matches only the source, target, and title. Here, both existing relationships share those three parts, so that matcher is ambiguous and does not uniquely select the asynchronous relationship.

`extend frontend -[sync]-> api 'streams'` targets the wrong relationship because it explicitly matches the `sync` relationship kind, so it selects the synchronous relationship instead of the asynchronous one.

```likec4
extend frontend -[async]-> api 'streams' {
}
```