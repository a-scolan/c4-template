Correct matcher: extend frontend -[async]-> api 'streams'
`extend frontend -> api 'streams'` is insufficient because it omits the relationship kind, so it is ambiguous when both `async` and `sync` edges share the same endpoints and title.
`extend frontend -[sync]-> api 'streams'` targets the wrong relationship because it matches the synchronous edge, not the asynchronous one you want to extend.

```likec4
extend frontend -[async]-> api 'streams' {}
```