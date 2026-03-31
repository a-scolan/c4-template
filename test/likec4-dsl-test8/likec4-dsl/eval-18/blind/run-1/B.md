No. `extend frontend -> api 'streams' { ... }` is wrong here, because relationship identity matching uses **source + target + kind**, and **title** is only an extra disambiguator when needed.

In your example, both relationships have the same:
- source: `frontend`
- target: `api`
- title: `'streams'`

But they differ by **kind**:
- `frontend -[async]-> api 'streams'`
- `frontend -> api 'streams'`

So omitting the kind does **not** uniquely identify the async relationship. Here, omitting the kind is **ambiguous and wrong** if your intent is to extend the async edge specifically.

```likec4
extend frontend -[async]-> api 'streams' {
  metadata {
    qos 'high'
  }
}
```