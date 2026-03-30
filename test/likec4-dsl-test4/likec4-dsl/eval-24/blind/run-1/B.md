Correct matcher: extend frontend -[async]-> api 'streams'

## Why `extend frontend -> api 'streams'` is insufficient

The bare arrow `->` in an `extend` matcher is a wildcard — it matches any relationship from `frontend` to `api` with the title `'streams'`, regardless of kind. Since two relationships exist (`async` and `sync`), this matcher is ambiguous: it would match both simultaneously, making it impossible to target only the `async` one. LikeC4 requires the matcher to uniquely identify a single relationship; using `->` when multiple relationships share the same endpoints and title violates that uniqueness requirement.

## Why `extend frontend -[sync]-> api 'streams'` targets the wrong relationship

The matcher `frontend -[sync]-> api 'streams'` explicitly specifies the `sync` kind. That matches **only** the synchronous relationship, not the asynchronous one. Since the goal is to extend the `async` relationship, using `-[sync]->` selects the wrong edge entirely.

## Exact extension snippet

```likec4
extend frontend -[async]-> api 'streams' {
  // add properties here, e.g.:
  description 'Server-sent event stream from frontend to API'
  technology 'SSE'
}
```

The kind selector `-[async]->` combined with the matching title `'streams'` uniquely identifies the asynchronous relationship, leaving the synchronous one untouched.
