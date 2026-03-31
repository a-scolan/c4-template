No — `extend frontend -> api 'streams' { ... }` does **not** unambiguously target the async relationship in that situation.

Relationship identity matching is based on the tuple:

- source
- target
- title
- kind

Here you already have two distinct relationships with the same:

- source: `frontend`
- target: `api`
- title: `'streams'`

but with different kinds:

- `async` for `frontend -[async]-> api 'streams'`
- the default/direct kind for `frontend -> api 'streams'`

So if you write:

`extend frontend -> api 'streams' { metadata { qos 'high' } }`

then you are **omitting the kind**, which means the extension matches the relationship whose identity also has the default/direct kind — **not** the `async` one.

So omitting the kind here is not just “a bit ambiguous”; it is **wrong for the goal of extending the async relationship**, because kind is part of the relationship identity and must match exactly.

Use this exact snippet instead to unambiguously target the async relationship:

`extend frontend -[async]-> api 'streams' {
  metadata {
    qos 'high'
  }
}`
