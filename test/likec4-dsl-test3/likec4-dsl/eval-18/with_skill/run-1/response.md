Yes—**but only if the `extend` selector matches the original relationship identity**.

Given the original relationship:

`frontend -[async]-> api 'streams'`

the safest/correct extension is:

```likec4
model {
  extend frontend -[async]-> api 'streams' {
    metadata { qos 'high' }
  }
}
```

### Matching rules for `extend` on relationships

`extend` is not just a loose “same endpoints” match when multiple relationships can exist between the same source/target.
Use the same relationship identity as the declaration:
- `source`
- `target`
- and, when present/needed to disambiguate, **kind** and **title**.

So `extend frontend -> api 'streams' { ... }` may be ambiguous or fail to match the intended `async` relationship. Including `-[async]->` makes the match explicit.