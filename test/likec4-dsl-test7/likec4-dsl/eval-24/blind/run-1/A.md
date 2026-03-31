Correct matcher: extend frontend -[async]-> api 'streams'

`extend frontend -> api 'streams'` is insufficient because it matches only by source, target, and title, which is ambiguous when two relationships share the same endpoints and label but differ by kind (`async` vs `sync`).

`extend frontend -[sync]-> api 'streams'` targets the wrong relationship because it explicitly selects the `sync` edge, not the `async` one you need to extend.

```likec4
extend frontend -[async]-> api 'streams' {
}
```