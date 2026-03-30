Correct matcher: extend frontend -[async]-> api 'streams'

`extend frontend -> api 'streams'` is insufficient because it does not disambiguate between multiple relationships with the same source, target, and title, while `extend frontend -[sync]-> api 'streams'` explicitly selects the other existing relationship kind.

```likec4
extend frontend -[async]-> api 'streams' {
  technology 'WebSocket'
}
```# Extending a Specific Relationship When Multiple Relationships Share the Same Label

Correct matcher: extend frontend -[async]-> api 'streams'

## Why `extend frontend -> api 'streams'` is insufficient

The bare arrow `->` does not carry a relationship kind. When two relationships exist between the same pair of elements — one with kind `async` and one with kind `sync` — the matcher `extend frontend -> api 'streams'` is ambiguous: it cannot uniquely identify which of the two relationships should receive the extension. Depending on the implementation, it may match both, match neither, or produce an error. Either way, it fails to target only the async relationship as intended.

## Why `extend frontend -[sync]-> api 'streams'` targets the wrong relationship

Both the kind and the label together form the identity key used to select a relationship for extension. The matcher `extend frontend -[sync]-> api 'streams'` explicitly selects the relationship whose kind is `sync` and whose label is `'streams'`. Because we want to extend the **async** relationship, using `[sync]` points at the other relationship and leaves the async one unmodified.

## Exact extension snippet

```likec4
extend frontend -[async]-> api 'streams' {
  // additional properties, e.g.:
  description 'Streams events asynchronously to the API'
}
```

This matcher combines the kind `[async]` with the label `'streams'` to uniquely identify and extend the correct relationship.
