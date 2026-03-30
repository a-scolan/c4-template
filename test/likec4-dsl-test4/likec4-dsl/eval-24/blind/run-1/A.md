Correct matcher: extend frontend -[async]-> api 'streams'

## Why `extend frontend -> api 'streams'` is insufficient

The model contains two distinct relationships between the same endpoints with the same title:
- `frontend -[async]-> api 'streams'`
- `frontend -[sync]-> api 'streams'`

LikeC4 matches an `extend` to an existing relationship by identity: **source + target + kind + title**. Using `extend frontend -> api 'streams'` omits the kind entirely. Since both existing relationships carry explicit kinds (`async` and `sync`), the kindless form does not unambiguously resolve to either of them — LikeC4 cannot determine which relationship to extend, making this matcher insufficient.

## Why `extend frontend -[sync]-> api 'streams'` targets the wrong relationship

Specifying `-[sync]->` correctly includes the kind in the identity match, but it resolves to the `frontend -[sync]-> api 'streams'` relationship — the synchronous one — not the async one we intend to extend.

## Exact extension snippet

```likec4
extend frontend -[async]-> api 'streams' {
  metadata { qos 'high' }
}
```

This unambiguously targets the `async`-kinded relationship between `frontend` and `api` with title `'streams'`, leaving the `sync` relationship untouched.
