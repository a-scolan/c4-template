Correct matcher: extend frontend -[async]-> api 'streams'

`extend frontend -> api 'streams'` is insufficient because both relationships already share the same source, target, and title, so omitting the relationship kind leaves the matcher ambiguous. `extend frontend -[sync]-> api 'streams'` targets the synchronous relationship, which is a different edge from the asynchronous one you want to extend.

```likec4
extend frontend -[async]-> api 'streams' {
}
```