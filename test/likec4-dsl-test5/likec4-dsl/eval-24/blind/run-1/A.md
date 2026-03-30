Correct matcher: extend frontend -[async]-> api 'streams'

`extend frontend -> api 'streams'` is insufficient because the matcher is ambiguous when multiple relationships share the same endpoints and title, and `extend frontend -[sync]-> api 'streams'` selects a different relationship kind than the async one.

```likec4
extend frontend -[async]-> api 'streams' {
  tags #extended
}
```Correct matcher: extend frontend -[async]-> api 'streams'

## Why `extend frontend -> api 'streams'` is insufficient

The bare arrow `->` (no kind bracket) does not match a relationship that was declared with an explicit kind like `-[async]->` or `-[sync]->`. In LikeC4, a relationship's kind is part of its identity. Because both existing relationships carry an explicit kind (`async` and `sync`), a kind-less matcher `->` does not resolve to either of them — it would target a hypothetical untyped relationship, which does not exist in this model. The extension would either fail silently or match nothing.

## Why `extend frontend -[sync]-> api 'streams'` targets the wrong relationship

The bracket `-[sync]->` is a precise kind filter. When two relationships share the same source, target, and title but differ in kind, the kind becomes the sole discriminator. Specifying `sync` selects the second relationship (`frontend -[sync]-> api 'streams'`), not the first. The `async` relationship is left untouched.

## Exact extension snippet

```likec4
extend frontend -[async]-> api 'streams' {
  technology 'WebSocket'
  description 'Continuous event stream from frontend to API over an async channel'
}
```

Replace the body with whatever properties you need to add or override; the matcher `frontend -[async]-> api 'streams'` is what uniquely identifies the target relationship.
