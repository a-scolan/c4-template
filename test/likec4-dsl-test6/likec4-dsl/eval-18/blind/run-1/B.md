No. That extension does not reliably target the async relationship, because relationship identity matching is based on source, target, and—when needed for disambiguation—title and kind. Here both relationships have the same source (`frontend`), target (`api`), and title (`'streams'`), so omitting the kind is wrong, not merely ambiguous: it can match the unkinded relationship instead of the async one.

```likec4
extend frontend -[async]-> api 'streams' {
  metadata { qos 'high' }
}
```