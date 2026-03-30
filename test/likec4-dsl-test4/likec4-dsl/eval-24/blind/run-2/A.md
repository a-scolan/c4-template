Correct matcher: extend frontend -[async]-> api 'streams'

## Why `extend frontend -> api 'streams'` is insufficient

When two relationships exist between the same source and target with the same title (`'streams'`) but different kinds (`async` and `sync`), using `extend frontend -> api 'streams'` is ambiguous — it matches on source, target, and title, but omits the relationship kind. LikeC4 cannot determine which of the two relationships you intend to extend, which may produce unexpected results or an error.

## Why `extend frontend -[sync]-> api 'streams'` targets the wrong relationship

The `[sync]` kind selector explicitly matches the relationship typed as `sync`. Since the goal is to extend the `async` relationship, using `-[sync]->` selects the wrong one.

## Exact extension snippet

```c4
extend frontend -[async]-> api 'streams' {
  // your additions here, e.g.:
  description 'Asynchronous event stream from frontend to API'
}
```

By specifying `-[async]->` alongside the title `'streams'`, the matcher uniquely identifies the asynchronous relationship and leaves the synchronous one untouched.
