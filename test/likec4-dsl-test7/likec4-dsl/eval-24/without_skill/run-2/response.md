Correct matcher: extend frontend -[async]-> api 'streams'
`extend frontend -> api 'streams'` is insufficient because it omits the relationship kind, so it is ambiguous when both `async` and `sync` relationships exist with the same source, target, and title.

`extend frontend -[sync]-> api 'streams'` targets the wrong relationship because it explicitly matches the `sync` edge, not the `async` one you want to extend.

```likec4
extend frontend -[async]-> api 'streams' {
  // extension properties here
}
```